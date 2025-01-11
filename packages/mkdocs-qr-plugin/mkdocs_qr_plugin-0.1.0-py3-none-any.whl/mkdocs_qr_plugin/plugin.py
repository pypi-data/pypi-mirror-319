import base64
import io
import logging

import mkdocs.utils
import qrcode
from mkdocs.plugins import BasePlugin
from qrcode.main import QRCode

log = logging.getLogger(f"mkdocs.plugins.{__name__}")
log.addFilter(mkdocs.utils.warning_filter)


class Size:
    def __init__(self, width, height):
        self.width = width
        self.height = height


class QRPlugin(BasePlugin):

    @staticmethod
    def generate_qr_code_data(data: str, size: Size = None) -> str:
        """
        Generates a QR code as an SVG string.

        Args: data: The data to be encoded in the QR code.
        Returns:str: The SVG string representing the QR code.
        """
        if size is None:
            size = Size(400, 400)

        qr = QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        img = img.resize((size.width, size.width))

        img_io = io.BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        img_bytes = img_io.read()
        base64_str = base64.b64encode(img_bytes).decode('utf-8')
        img_tag = f'<img src="data:image/png;base64,{base64_str}" alt="Image">'
        return base64_str

    def on_page_markdown(self,
                         markdown,
                         page,
                         config,
                         site_navigation=None,
                         **kwargs):
        import re

        def generate_image(match):
            title = match.group(1).strip()
            content = match.group(2).strip()
            content = QRPlugin.generate_qr_code_data(content)

            return f'<img src="data:image/png;base64,{content}" alt="{title}">'

        markdown = re.sub(r":::QR\n(.*?)\n(.*?)\n:::", generate_image, markdown)

        return markdown
