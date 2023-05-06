import base64
from io import BytesIO
import math
from PIL import Image, ImageFont, ImageDraw
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
    result = Image.new(
        "RGBA", (width * 5 + 200,
                 (height * math.ceil(number / 5)
                  +
                  (math.ceil(number / 5)) * 200)
                 + 250), (255, 255, 255)
    )
    for i in range(len(items)):
        result.paste(image_list[i], (width * (i %
                     5)+100, (height * (i // 5) + (i // 5) * 250) + 50), image_list[i])

    draw = ImageDraw.Draw(result)
    for i in range(len(items)):
        draw.text((width * (i % 5)+100 + width / 4, height * (i // 5) + (i // 5) *
                  250 + height + 100), items[i]["name"], font=font, fill=(0, 0, 0))
        draw.text((width * (i % 5)+100 + width / 4, height * (i // 5) + (i // 5) *
                  250 + height + 150), items[i]["rarity"], font=font, fill=rarity_color[items[i]["rarity"]])
        draw.text((width * (i % 5)+100 + width / 4, height * (i // 5) + (i // 5) *
                  250 + height + 200), f"磨损: {items[i]['wear_rating']}", font=font, fill=(0, 0, 0))

    return img_to_b64(result)


def img_to_b64(pic: Image.Image) -> str:
    buf = BytesIO()
    pic.save(buf, format="PNG")
    base64_str = base64.b64encode(buf.getbuffer()).decode()
    return "base64://" + base64_str
