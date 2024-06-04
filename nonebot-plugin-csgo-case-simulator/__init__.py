import io
from typing import List
from nonebot import require

require("nonebot_plugin_alconna")
require("nonebot_plugin_htmlrender")
from nonebot_plugin_htmlrender import (
    text_to_pic,
    md_to_pic,
    template_to_pic,
    get_new_page,
)
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import on_alconna, Match
from arclet.alconna import Alconna, Args
from nonebot_plugin_alconna.uniseg import Image, UniMessage
from nonebot.adapters import Message, Event
from nonebot.rule import to_me
from pathlib import Path
from .crates import Crates
from .skins import Skins
from .model import SelectedSkin
from PIL import Image as Img


creates = Crates()
skins = Skins()

__plugin_meta__ = PluginMetadata(
    name="CSGO开箱模拟器",
    description="nonebot的CS2/CSGO开箱模拟器",
    usage="输入 open 开箱",
    type="application",
    supported_adapters=None,
)

open = on_alconna(
    Alconna("open", Args["caseName?", str]),
    aliases={"开箱"},
    rule=to_me(),
)


@open.handle()
async def handle_function(caseName: Match[str], event: Event):
    if not caseName.available:
        await open.finish("请输入箱子名称")

    crate = creates.get_case_by_name(caseName.result)
    if crate is None:
        await open.finish("未找到箱子")

    items = creates.open_crate_multiple(crate, 20)
    skin_list: List[SelectedSkin] = []
    for item in items:
        skin = skins.get_skins(item.name)
        skin_list.append(skin)

    text_list = ["1", "2", "3", "4"]
    template_path = str(Path(__file__).parent / "templates")
    template_name = "index.html"
    # 设置模板
    # 模板中本地资源地址需要相对于 base_url 或使用绝对路径
    pic = await template_to_pic(
        template_path=template_path,
        template_name=template_name,
        templates={
            "skin_list": skin_list,
            "user_id": event.get_user_id(),
        },
        pages={
            "viewport": {"width": 1920, "height": 1080},
            "base_url": f"file://{template_path}",
        },
        wait=2,
    )
    # save to file
    a = Img.open(io.BytesIO(pic))
    a.save("template2pic.png", format="PNG")

    await open.finish()
    # UniMessage(Image(raw=pic))
