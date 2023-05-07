import asyncio
from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Message, MessageSegment, MessageEvent
from .cases import Cases
from .skins import Skins
from .utils import Utils

cases = Cases()
skins = Skins()
utils = Utils()


async def get_all_json():
    res = await asyncio.gather(cases.get_cases_json(), skins.get_skins_json())
    cases.cases = res[0].json()
    skins.skins = res[1].json()

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

case_opening = on_command("open", priority=5)
list_cases = on_command("cases", priority=5)
# radom_case = on_command("random", priority=5)
search_skin = on_command("s_skin", priority=5)


@list_cases.handle()
async def handle_list_cases():
    cases_list = cases.get_case_name_list()
    cases_list_str = ""
    for case in cases_list:
        cases_list_str += f"{case}\n"
    await list_cases.finish(f"{cases_list_str}")


# @radom_case.handle()
# async def handle_random_case():
#     case = cases.get_random_case()
#     await radom_case.send(f"正在开启{case['name']}...")
#     item = cases.open_case(case["id"])
#     skin = skins.get_skins(item["id"])
#     await radom_case.finish(get_skink_message(skin))


@case_opening.handle()
async def handle_open_case(event: MessageEvent, args: Message = CommandArg()):
    arg_list = args.extract_plain_text().split(" ")
    if len(arg_list) > 0:
        if len(arg_list) == 2:
            arg_amount = int(arg_list[0])
            amount = arg_amount if arg_amount < 20 else 20
            case_name = arg_list[1]
        else:
            amount = 1
            case_name = arg_list[0]

        case = cases.get_case_by_name(case_name)
        if case:
            img_base64 = await utils.url_to_b64(case["image"])
            await case_opening.send(MessageSegment.image(img_base64)+f"正在开启{case['name']}...")
            items = cases.open_case_multiple(case["id"], amount)
            opened_skins = []
            for item in items:
                skin = skins.get_skins(item["name"])
                opened_skins.append(skin)

            image = await utils.merge_images(opened_skins)
            await case_opening.finish(MessageSegment.image(image))
        else:
            await case_opening.finish("箱子不存在")
    else:
        await case_opening.finish("请输入箱子名称")


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


def get_skink_message(skin: dict):
    return (MessageSegment.image(skin["image"]) +
            f"""获得 {skin['rarity']}\n{skin['name']}\n磨损度{skin['wear_rating']}""")
