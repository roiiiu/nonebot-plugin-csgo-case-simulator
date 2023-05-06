from enum import Enum
import os
from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Message, MessageSegment, MessageEvent
from .cases import Cases
from .skins import Skins
from .utils import merge_images
from supabase import create_client, Client

cases = Cases()
skins = Skins()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

rarities = {
    "工业级": 1,
    "军规级": 2,
    "受限": 3,
    "保密": 4,
    "隐秘": 5,
    "非凡": 6,
}

rarities_reverse = {
    1: "工业级",
    2: "军规级",
    3: "受限",
    4: "保密",
    5: "隐秘",
    6: "非凡",
}


case_opening = on_command("open", priority=5)
# case_open_multiple = on_command("open_mul", priority=5)
list_cases = on_command("cases", priority=5)
contains = on_command("contains", priority=10, block=True)
radom_case = on_command("random", priority=5)
search_skin = on_command("s_skin", priority=5)
storage = on_command("storage", priority=5)


@list_cases.handle()
async def handle_list_cases():
    cases = cases.get_case_name_list()
    cases_list_str = ""
    for case in cases:
        cases_list_str += f"{case}\n"
    await list_cases.finish(f"{cases_list_str}")


@contains.handle()
async def handle_case_contains(args: Message = CommandArg()):
    if case_name := args.extract_plain_text():
        cases_contains = cases.get_case_contains(case_name)
        await contains.finish(f"{cases_contains}")
    else:
        await contains.finish("请输入箱子名称")


@radom_case.handle()
async def handle_random_case():
    case = cases.get_random_case()
    await radom_case.send(f"正在开启{case['name']}...")
    item = cases.open_case(case["id"])
    skin = skins.get_skins(item["id"])
    await radom_case.finish(get_skink_message(skin))


@case_opening.handle()
async def handle_open_case(event: MessageEvent, args: Message = CommandArg()):
    user_id = event.get_user_id()
    response = supabase.table('CSGOPlayer').select(
        "*").eq('id', user_id).execute()
    if not response.data:
        supabase.table('CSGOPlayer').insert({"id": user_id}).execute()

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
            await case_opening.send(MessageSegment.image(case["image"])+f"正在开启{case['name']}...")
            items = cases.open_case_multiple(case["id"], amount)
            opened_skins = []
            for item in items:
                skin = skins.get_skins(item["name"])
                opened_skins.append(skin)
            image = merge_images(opened_skins)

            skin_to_insert = []
            for skin in opened_skins:
                if (rarities[skin["rarity"]] > 3):
                    skin_to_insert.append(
                        {
                            "rarity": rarities[skin["rarity"]],
                            "name": skin["name"],
                            "wear_rating": skin["wear_rating"],
                            "image": skin["image"]
                        }
                    )
            skin_data = supabase.table('CSGOSkins').insert(
                skin_to_insert).execute()

            player_skins_list = []
            for skin in skin_data.data:
                player_skins_list.append(
                    {
                        "player_id": user_id,
                        "skin_id": skin["id"]
                    }
                )
            supabase.table('PlayerSkins').insert(player_skins_list).execute()
            await case_opening.finish(MessageSegment.image(image))
        else:
            await case_opening.finish("箱子不存在")
    else:
        await case_opening.finish("请输入箱子名称")


# @case_open_multiple.handle()
# async def handle_open_multiple_case(args: Message = CommandArg()):
#     if case_name := args.extract_plain_text().strip():
#         case = cases.get_case_by_name(case_name)
#         if case:
#             await case_open_multiple.send(MessageSegment.image(case["image"])+f"正在开启{case['name']}...")
#             items = cases.open_case_multiple(case["id"], 20)
#             opened_skins = []
#             for item in items:
#                 skin = skins.get_skins(item["name"])
#                 opened_skins.append(skin)
#             image = merge_images(opened_skins)
#             await case_open_multiple.finish(MessageSegment.image(image))
#         else:
#             await case_open_multiple.finish("箱子不存在")
#     else:
#         await case_open_multiple.finish("请输入箱子名称")


@search_skin.handle()
async def handle_search_skin(args: Message = CommandArg()):
    if skin_name := args.extract_plain_text().strip():
        found_skin_list = skins.search_skin(skin_name)
        if len(found_skin_list) == 0:
            await search_skin.finish("没找到捏")
        for skin in found_skin_list:
            await search_skin.send(MessageSegment.image(skin["image"])+f"找到饰品{skin['name']}")
    else:
        await search_skin.finish("请输入皮肤名称")


@storage.handle()
async def handle_storage(event: MessageEvent):
    user_id = event.get_user_id()
    response = supabase.table('CSGOPlayer').select(
        "*").eq('id', user_id).execute()
    if not response.data:
        await storage.finish("你的库存是空的")
    else:
        # 查询palyerSkins表中 user_id的所有皮肤数据
        skins_data = supabase.table('PlayerSkins').select(
            "*").eq('player_id', user_id).execute()
        skins_id = []
        for skin in skins_data.data:
            skins_id.append(skin["skin_id"])
        # 查询CSGOSkins表中所有皮肤rarity大于3的数据
        skins_data = supabase.table('CSGOSkins').select(
            "*").in_('id', skins_id).gt('rarity', 3).execute()
        skins = []
        for skin in skins_data.data:
            skins.append({
                "name": skin["name"],
                "rarity": rarities_reverse[skin["rarity"]],
                "wear_rating": skin["wear_rating"],
                "image": skin["image"],
            })
        if (len(skins) >= 0):
            image = merge_images(skins)
            await storage.finish(MessageSegment.image(image))
        else:
            await storage.finish("你的库存是空的")


def get_skink_message(skin: dict):
    return (MessageSegment.image(skin["image"]) +
            f"""获得 {skin['rarity']}\n{skin['name']}\n磨损度{skin['wear_rating']}""")
