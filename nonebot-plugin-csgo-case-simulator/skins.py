import json
import random
from os.path import dirname
from typing import List
from .model import SelectedSkin, Skin

import httpx


JSON_DIR = dirname(__file__) + "/json"


class Skins:
    def __init__(self):
        self.skins: List[Skin] = []
        self.skins_api = "https://bymykel.github.io/CSGO-API/api/zh-CN/skins.json"

    async def get_skins_json(self):
        async with httpx.AsyncClient(verify=False) as client:
            return await client.get(self.skins_api)
        # with open(f"{JSON_DIR}/skins.json", 'rb') as f:
        #     data = f.read()
        #     return json.loads(data)

    def get_skins(self, name: str) -> SelectedSkin:
        for skin in self.skins:
            if skin.name == name:
                return SelectedSkin(
                    id=skin.id,
                    name=skin.name,
                    image=skin.image,
                    rarity=skin.rarity.name,
                    wear=random.choice(skin.wears).name,
                )

    def search_skin(self, skin_name: str) -> List[Skin]:
        found_skin_list = []
        for skin in self.skins:
            if skin.pattern and skin_name.lower() in skin.pattern:
                found_skin_list.append(skin)
        return found_skin_list
