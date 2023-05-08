import asyncio
import base64
from io import BytesIO
import math
import os
from os.path import dirname
from PIL import Image, ImageFont, ImageDraw, ImageFilter
import httpx


FONT_DIR = dirname(__file__) + "/font/font.ttf"


class Utils:
    def __init__(self):
        self.client = httpx.Client()
        self.rarity_color = {
            "消费级": (130, 130, 130),
            "工业级": (96, 152, 217),
            "军规级": (76, 105, 255),
            "受限": (136, 70, 255),
            "保密": (177, 46, 194),
            "隐秘": (235, 75, 75),
            "及其罕见的特殊物品": (201, 171, 5),
            "非凡": (201, 171, 5),
        }

    async def merge_images(self, items):
        ttf_path = FONT_DIR
        font = ImageFont.truetype(ttf_path, 40)
        image_list = []

        image_tasks = [self.download_image(item["image"]) for item in items]
        image_list = await asyncio.gather(*image_tasks)

        width = image_list[0].width
        height = image_list[0].height
        number = len(items)
        rows = math.ceil(number / 5)
        columns = number if number < 5 else 5
        padding = 200
        info_height = 200
        bg_color = (255, 255, 255)
        font_color = (0, 0, 0)

        path = os.path.dirname(os.path.abspath(__file__))
        bg_file = os.path.join(path, "background3.jpeg")
        background_img = Image.open(bg_file)
        background_img = background_img.filter(
            ImageFilter.GaussianBlur(radius=50))
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
                fill=self.rarity_color[items[i]["rarity"]]
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

        return self.img_to_b64(canvas)

    async def download_image(self, url):
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            img = Image.open(BytesIO(response.content))
            return img

    def img_to_b64(self, pic: Image.Image) -> str:
        buf = BytesIO()
        pic.save(buf, format="PNG")
        base64_str = base64.b64encode(buf.getbuffer()).decode()
        return "base64://" + base64_str

    async def url_to_b64(self, url: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            base64_str = base64.b64encode(response.content).decode()
            return "base64://" + base64_str
