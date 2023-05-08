import json
import random
from os.path import dirname


JSON_DIR = dirname(__file__) + "/json"


class Skins:
    def __init__(self):
        self.skins = []

    async def get_skins_json(self):
        # async with httpx.AsyncClient() as client:
        #     return await client.get(self.skins_api)
        with open(f"{JSON_DIR}/skins.json", 'rb') as f:
            data = f.read()
            return json.loads(data)

    def get_skins(self, name: str) -> dict:
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

    def search_skin(self, skin_name: str) -> dict:
        found_skin_list = []
        for skin in self.skins:
            if skin["pattern"].find(skin_name.lower()) != -1:
                found_skin_list.append(skin)
        return found_skin_list
