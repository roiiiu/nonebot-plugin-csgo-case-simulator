import base64
from io import BytesIO
import math
import os
from PIL import Image, ImageFont, ImageDraw, ImageFilter
import requests

rarity_color = {
    "工业级": (96, 152, 217),
    "军规级": (76, 105, 255),
    "受限": (136, 70, 255),
    "保密": (177, 46, 194),
    "隐秘": (235, 75, 75),
    "及其罕见的特殊物品": (201, 171, 5),
    "非凡": (201, 171, 5),
}


def merge_images(items):
    ttf_path = "仓耳舒圆体W03.ttf"
    font = ImageFont.truetype(ttf_path, 40)
    image_list = []
    for i in range(len(items)):
        img = Image.open(
            BytesIO(requests.get(items[i]["image"]).content))
        image_list.append(img)

    width = image_list[0].width
    height = image_list[0].height
    number = len(items)
    rows = math.ceil(number / 5)
    columns = number if number < 5 else 5
    padding = 200
    info_height = 200
    bg_color = (255, 255, 255)
    font_color = (255, 255, 255)

    path = os.path.dirname(os.path.abspath(__file__))
    bg_file = os.path.join(path, "background2.png")
    background_img = Image.open(bg_file)
    background_img = background_img.filter(ImageFilter.GaussianBlur(radius=50))
    background_img = background_img.resize((width * columns + padding,
                                            (height + info_height) * rows + padding))

    canvas = background_img
    # Image.new(
    #     "RGBA",
    #     (
    #         width * columns + padding,
    #         (height + info_height) * rows + padding
    #     ),
    #     bg_color
    # )

    for i in range(len(items)):
        row = math.ceil((i + 1) / 5)
        canvas.paste(
            image_list[i],
            (
                width * (i % 5)+100,
                (height + info_height) * (row - 1) + 100
            ),
            image_list[i]
        )

    draw = ImageDraw.Draw(canvas)
    for i in range(len(items)):
        row = math.ceil((i + 1) / 5)
        draw.text(
            (
                width * (i % 5)+100 + width / 4,
                100 + height * row + (row - 1) * info_height
            ),
            items[i]["name"],
            font=font,
            fill=font_color
        )
        draw.text(
            (
                width * (i % 5)+100 + width / 4,
                100 + height * row + (row - 1) * info_height + 50
            ),
            items[i]["rarity"],
            font=font,
            fill=rarity_color[items[i]["rarity"]]
        )
        draw.text(
            (
                width * (i % 5)+100 + width / 4,
                100 + height * row + (row - 1) * info_height + 100
            ),
            f"磨损: {items[i]['wear_rating']}",
            font=font,
            fill=font_color
        )

    return img_to_b64(canvas)


def img_to_b64(pic: Image.Image) -> str:
    buf = BytesIO()
    pic.save(buf, format="PNG")
    base64_str = base64.b64encode(buf.getbuffer()).decode()
    return "base64://" + base64_str
