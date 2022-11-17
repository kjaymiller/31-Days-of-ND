import logging
import textwrap

from PIL import Image, ImageDraw, ImageFont


def overlay_text(day: int, text: str, image_path=str) -> None:
    image = Image.open(image_path)
    wrap_caps = (
                # max_length, line_cap, ratio
                (305, 47, 0.010),
                (225, 38, 0.012),
                (100, 29, 0.014),
                (0, 21,  0.020),
    )
    font_text = "assets/Lato-BoldItalic.ttf"

    for max_length, Image_width, ratio in wrap_caps:
        if (text_length := len(text)) >= max_lenth:
            text = textwrap.fill(text, width=line_cap)
            image_size_ratio = image.size[0] * ratio
            break	
    draw = ImageDraw.Draw(image)
    font_size = 1
    font = ImageFont.truetype(font_text, font_size)

    while font.getbbox(text)[1] < image_size_ratio:
        font_size += 1
        font = ImageFont.truetype(font_text, font_size)

    smallerfont = ImageFont.truetype(font_text, 30)
    draw.text(
            (10, 100),
            f"#{day}",
            font=smallerfont,
            fill=(50, 50, 50, 5),
    )
    draw.text(
            (90, 100),
            text,
            font=font,
            fill=(50, 50, 50, 255),
    )
    draw.text(
            (400, 550),
            "#31DaysofNeurodivergence",
            font=smallerfont,
            fill=(250, 250, 250, 255),
    )
    return image