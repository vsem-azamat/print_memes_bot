import io
import math
import textwrap
from PIL import Image, ImageDraw, ImageFont


class TextFormatter:
    """
    Text justification.

    source: https://qna.habr.com/q/953259
    """
    @staticmethod
    def __justify(line, width):
        gap_width, max_replace = divmod(width - len(line) + line.count(' '), line.count(' '))
        return line.replace(' ', ' ' * gap_width).replace(' ' * gap_width, ' ' * (gap_width + 1), max_replace)

    @classmethod
    def lines_formatter(cls, text, width):
        lines = textwrap.wrap(text, width, break_long_words=False)
        for i, line in enumerate(lines[:-1]):
            if len(line) <= width and line.count(' '):
                lines[i] = cls.__justify(line, width).rstrip()
        return '\n'.join(lines)


async def edit_photo(io_image: io.BytesIO,
                     text_up: str = None, text_down: str = None,
                     selected_font: str = None) -> io.BytesIO:
    """
    The function insert a caption into an image.
    """
    im = Image.open(io.BytesIO(io_image.getbuffer().tobytes()))
    draw_text = ImageDraw.ImageDraw(im)

    W_image, H_image = im.size
    W_text = int(W_image / 10)
    text_size = int(H_image / 15)
    stroke_width = int(text_size / 10)
    font_name = {
        "A": "Arial",
        "F": "Fixedsys",
        "L": "Lobster"
    }.get(selected_font, "Arial")
    font = ImageFont.truetype(f'./app/utils/{font_name}.ttf', size=text_size, encoding='UTF-8')

    # UP
    if text_up:
        text_up = TextFormatter.lines_formatter(text_up.strip(), W_text).strip()
        text_up_length, _ = font.getsize(text_up.split('\n')[0])
        while text_up_length >= W_image * 0.9:
            W_text *= 0.9
            text_up = TextFormatter.lines_formatter(text_up.strip(), math.floor(W_text)).strip()
            text_up_length, _ = font.getsize(text_up.split('\n')[0])

        W_text_up = int(draw_text.textlength(text_up.split('\n')[0], font))

        H_indent_up = int(H_image/50)
        W_ident_up = int((W_image-W_text_up)/2)

        draw_text.multiline_text(
            (W_ident_up, H_indent_up),
            text_up,
            font=font,
            stroke_width=stroke_width,
            stroke_fill='BLACK'
        )

    # DOWN
    if text_down:
        text_down = TextFormatter.lines_formatter(text_down.split('\n')[0], W_text).strip()
        text_down_length, _ = font.getsize(text_up.split('\n')[0])
        while text_down_length >= W_image * 0.9:
            W_text *= 0.9
            text_down = TextFormatter.lines_formatter(text_up.strip(), math.floor(W_text)).strip()
            text_down_length, _ = font.getsize(text_up.split('\n')[0])

        text_down_quantity_lines = text_down.count('\n')
        W_text_down = int(draw_text.textlength(text_down.split('\n')[0], font))

        H_indent_down = int(H_image*0.9-text_down_quantity_lines*1.1)
        W_ident_down = int((W_image-W_text_down)/2)

        draw_text.multiline_text(
            (W_ident_down, H_indent_down),
            text_down,
            font=font,
            stroke_width=stroke_width,
            stroke_fill='BLACK'
        )

    output = io.BytesIO()
    im.save(output, format="PNG")
    return output
