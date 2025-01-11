class KSampler:
    SCHEDULERS = ["karras", "normal", "simple"]
    SAMPLERS = ["sample_euler", "sample_euler_ancestral", "sample_heun", "sample_dpm_2", "sample_dpm_2_ancestral",
                "sample_lms", "sample_dpm_fast", "sample_dpm_adaptive", "sample_dpmpp_2s_ancestral", "sample_dpmpp_sde",
                "sample_dpmpp_2m"]

    def __init__(self, model, steps, device, sampler=None, scheduler=None, denoise=None):
        self.model = model
        if self.model.parameterization == "v":
            self.model_wrap = k_diffusion_external.CompVisVDenoiser(self.model, quantize=True)
        else:
            self.model_wrap = k_diffusion_external.CompVisDenoiser(self.model, quantize=True)
        self.model_k = CFGDenoiserComplex(self.model_wrap)
        self.device = device
        if scheduler not in self.SCHEDULERS:
            scheduler = self.SCHEDULERS[0]
        if sampler not in self.SAMPLERS:
            sampler = self.SAMPLERS[0]
        self.scheduler = scheduler
        self.sampler = sampler
        self.sigma_min=float(self.model_wrap.sigmas[0])
        self.sigma_max=float(self.model_wrap.sigmas[-1])
        self.set_steps(steps, denoise)

    def _calculate_sigmas(self, steps):
        sigmas = None

        discard_penultimate_sigma = False
        if self.sampler in ['sample_dpm_2', 'sample_dpm_2_ancestral']:
            steps += 1
            discard_penultimate_sigma = True

        if self.scheduler == "karras":
            sigmas = k_diffusion_sampling.get_sigmas_karras(n=steps, sigma_min=self.sigma_min, sigma_max=self.sigma_max, device=self.device)
        elif self.scheduler == "normal":
            sigmas = self.model_wrap.get_sigmas(steps).to(self.device)
        elif self.scheduler == "simple":
            sigmas = simple_scheduler(self.model_wrap, steps).to(self.device)
        else:
            print("error invalid scheduler", self.scheduler)

        if discard_penultimate_sigma:
            sigmas = torch.cat([sigmas[:-2], sigmas[-1:]])
        return sigmas

    def set_steps(self, steps, denoise=None):
        self.steps = steps
        if denoise is None:
            self.sigmas = self._calculate_sigmas(steps)
        else:
            new_steps = int(steps/denoise)
            sigmas = self._calculate_sigmas(new_steps)
            self.sigmas = sigmas[-(steps + 1):]


    def sample(self, noise, positive, negative, cfg, latent_image=None, start_step=None, last_step=None, force_full_denoise=False):
        sigmas = self.sigmas
        sigma_min = self.sigma_min

        if last_step is not None and last_step < (len(sigmas) - 1):
            sigma_min = sigmas[last_step]
            sigmas = sigmas[:last_step + 1]
            if force_full_denoise:
                sigmas[-1] = 0

        if start_step is not None:
            if start_step < (len(sigmas) - 1):
                sigmas = sigmas[start_step:]
            else:
                if latent_image is not None:
                    return latent_image
                else:
                    return torch.zeros_like(noise)

        noise *= sigmas[0]
        if latent_image is not None:
            noise += latent_image

        positive = positive[:]
        negative = negative[:]
        #make sure each cond area has an opposite one with the same area
        for c in positive:
            create_cond_with_same_area_if_none(negative, c)
        for c in negative:
            create_cond_with_same_area_if_none(positive, c)

        if self.model.model.diffusion_model.dtype == torch.float16:
            precision_scope = torch.autocast
        else:
            precision_scope = contextlib.nullcontext

        with precision_scope(self.device):
            if self.sampler == "sample_dpm_fast":
                samples = k_diffusion_sampling.sample_dpm_fast(self.model_k, noise, sigma_min, sigmas[0], self.steps, extra_args={"cond":positive, "uncond":negative, "cond_scale": cfg})
            elif self.sampler == "sample_dpm_adaptive":
                samples = k_diffusion_sampling.sample_dpm_adaptive(self.model_k, noise, sigma_min, sigmas[0], extra_args={"cond":positive, "uncond":negative, "cond_scale": cfg})
            else:
                samples = getattr(k_diffusion_sampling, self.sampler)(self.model_k, noise, sigmas, extra_args={"cond":positive, "uncond":negative, "cond_scale": cfg})
        return samples.to(torch.float32)