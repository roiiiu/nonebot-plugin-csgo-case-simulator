import random
import httpx


class Skins:
    def __init__(self):
        self.skins_api = "https://bymykel.github.io/CSGO-API/api/zh-CN/skins.json"
        self.skins = []

    async def get_skins_json(self):
        async with httpx.AsyncClient() as client:
            return await client.get(self.skins_api)

    def get_skins(self, name: str) -> dict:
        # print(name)
        for skin in self.skins:
            if skin["name"] == name:
                wear_rating = round(
                    random.uniform(skin["min_float"], skin["max_float"]), 5
                )
                return {
                    "id": skin["id"],
                    "name": skin["name"],
                    "image": skin["image"],
                    "rarity": skin["rarity"],
                    "wear_rating": wear_rating,
                }
        # return self.check_if_wrong_name(name)

    # temp fix
    # def check_if_wrong_name(self, name: str):
    #     if name.find("M4A1 消音型") != -1:
    #         skin_name = name.replace("M4A1 消音型", "M4A4")
    #         for skin in self.skins:
    #             if skin["name"] == skin_name:
    #                 wear_rating = round(
    #                     random.uniform(skin["min_float"], skin["max_float"]), 5
    #                 )
    #                 return {
    #                     "id": skin["id"],
    #                     "name": name,
    #                     "image": skin["image"],
    #                     "rarity": skin["rarity"],
    #                     "wear_rating": wear_rating,
    #                 }

    def search_skin(self, skin_name: str) -> dict:
        found_skin_list = []
        for skin in self.skins:
            if skin["pattern"].find(skin_name.lower()) != -1:
                found_skin_list.append(skin)
        return found_skin_list
