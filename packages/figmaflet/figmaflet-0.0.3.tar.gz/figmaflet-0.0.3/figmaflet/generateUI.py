from jinja2 import Template
from figmaflet.template import TEMPLATE
from figmaflet.figma.frame import Frame
from figmaflet.figma import endpoints
from pathlib import Path


class UI:
    def __init__(self, token: str, file_key: str, local_path: Path):

        self.figma_file = endpoints.Files(token, file_key)
        self.file_data = self.figma_file.get_file()
        self.local_path = local_path

    def to_code(self):
        # frames = []
        # Generate Flet code for each frame

        for f in self.file_data["document"]["children"][0]["children"]:
            frame = Frame(f, figma_file=self.figma_file, output_path=self.local_path)
            # frames.append(frame)
            # Render the template
            t = Template(TEMPLATE)
            rendered_code = t.render(elements=frame.to_code())
            return rendered_code

    def generate(self):
        code = self.to_code()
        self.local_path.joinpath("main.py").write_text(code, encoding="UTF-8")
