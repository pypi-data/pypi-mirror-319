from pipeline_ui import FileOutput, ImageParameter, PipelineUI, node, AudioParameter, VideoParameter

pui = PipelineUI()

@node()
def load_image(mask = ImageParameter(description="The mask to use for inpainting")) -> FileOutput:
    return FileOutput(description="The mask to use for inpainting")

@node()
def load_audio(audio = AudioParameter(description="test")):
    pass

@node()
def load_video(video = VideoParameter(description="hello")):
    pass



pui.start()