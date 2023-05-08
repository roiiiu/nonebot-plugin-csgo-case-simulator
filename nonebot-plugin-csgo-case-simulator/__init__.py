import asyncio
import time
from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Message, MessageSegment, MessageEvent
from .crates import Crates
from .skins import Skins
from .utils import Utils

crates = Crates()
skins = Skins()
utils = Utils()


async def get_all_json():
    res = await asyncio.gather(
        crates.get_cases_json(),
        crates.get_souvenirs_json(),
        skins.get_skins_json(),
    )
    crates.cases = res[0]
    crates.souvenirs = res[1]
    skins.skins = res[2]

asyncio.run(get_all_json())

rarities = {
    "工业级": 1,
    "军规级": 2,
    "受限": 3,
    "保密": 4,
    "隐秘": 5,
    "非凡": 6,
}

rarities_reverse = {value: key for key, value in rarities.items()}

crate_opening = on_command("open", priority=5)
list_cases = on_command("cases", priority=5)
list_souvenir = on_command("svs", priority=5)
search_skin = on_command("s_skin", priority=5)
help = on_command("help", priority=5)


@list_cases.handle()
async def handle_list_cases():
    cases_list = crates.get_case_name_list()
    cases_list_str = ""
    for case in cases_list:
        cases_list_str += f"{case}\n"
    await list_cases.finish(f"{cases_list_str}")


@list_souvenir.handle()
async def handle_list_souvenir():
    svs_list = crates.get_souvenir_name_list()
    svs_list_str = ""
    for sv in svs_list[0:len(svs_list) // 2]:
        svs_list_str += f"{sv}\n"
    await list_souvenir.send(f"{svs_list_str}")
    svs_list_str = ""
    for sv in svs_list[len(svs_list)//2:]:
        svs_list_str += f"{sv}\n"
    await list_souvenir.finish(f"{svs_list_str}")


@help.handle()
async def handle_help():
    await help.finish(
        """
    开箱指令：    
    /open [数量] [箱子名] 开箱    
    /cases 查看所有箱子    
    /svs 查看所有纪念包    
    /s_skin [皮肤名] 搜索皮肤    
    /help 查看帮助    
    """
    )

# @radom_case.handle()
# async def handle_random_case():
#     case = cases.get_random_case()
#     await radom_case.send(f"正在开启{case['name']}...")
#     item = cases.open_case(case["id"])
#     skin = skins.get_skins(item["id"])
#     await radom_case.finish(get_skink_message(skin))


@crate_opening.handle()
async def handle_open_crate(event: MessageEvent, args: Message = CommandArg()):
    (amount, name) = extract_args(args)
    if name:
        crate = get_crate(name)
        if crate:
            if not crate["contains"]:
                await crate_opening.finish("箱子里面是空的")
            img_base64 = await utils.url_to_b64(crate["image"])
            await crate_opening.send(MessageSegment.image(img_base64)+f"正在开启{amount}个{crate['name']}...")
            items = crates.open_crate_multiple(
                crate, amount
            )
            opened_skins = []
            for item in items:
                skin = skins.get_skins(item["name"])
                opened_skins.append(skin)
            image = await utils.merge_images(opened_skins)
            await crate_opening.finish(MessageSegment.image(image))
        else:
            await crate_opening.finish("箱子不存在")
    else:
        await crate_opening.finish("请输入箱子名称")


@search_skin.handle()
async def handle_search_skin(args: Message = CommandArg()):
    if skin_name := args.extract_plain_text().strip():
        found_skin_list = skins.search_skin(skin_name)
        if len(found_skin_list) == 0:
            await search_skin.finish("没找到捏")
        for skin in found_skin_list:
            img_base64 = await utils.url_to_b64(skin["image"])
            await search_skin.send(MessageSegment.image(img_base64)+f"找到饰品{skin['name']}")
    else:
        await search_skin.finish("请输入皮肤名称")


def extract_args(args: Message = CommandArg()):
    arg_list = args.extract_plain_text().split(" ")
    if len(arg_list) > 0 and arg_list[0] != "":
        if len(arg_list) == 2:
            arg_amount = int(arg_list[0])
            amount = arg_amount if arg_amount < 20 else 20
            crate_name = arg_list[1]
        else:
            amount = 1
            crate_name = arg_list[0]
        return amount, crate_name
    else:
        return 1, None


def get_crate(name: str):
    return crates.get_case_by_name(name) or crates.get_souvenir_by_name(name)


def get_skink_message(skin: dict):
    return (MessageSegment.image(skin["image"]) +
            f"""获得 {skin['rarity']}\n{skin['name']}\n磨损度{skin['wear_rating']}""")
