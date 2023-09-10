import json
import random
from os.path import dirname
from typing import List, Optional

import httpx
from .model import Contains, Crate

JSON_DIR = dirname(__file__) + "/json"


class Crates:
    def __init__(self):
        self.cases: List[Crate] = []
        self.souvenirs: List[Crate] = []

        self.rarity_list = ["消费级", "工业级", "军规级", "受限", "保密", "隐秘", "非凡", "违禁"]
        self.cases_api = "https://bymykel.github.io/CSGO-API/api/zh-CN/crates/cases.json"
        self.souvenirs_api = "https://bymykel.github.io/CSGO-API/api/zh-CN/crates/souvenir.json"

    async def get_cases_json(self):
        # with open(f"{JSON_DIR}/cases.json", 'rb') as f:
        #     data = f.read()
        #     return json.loads(data)
        async with httpx.AsyncClient(verify=False) as client:
            return await client.get(self.cases_api)

    async def get_souvenirs_json(self):
        # with open(f"{JSON_DIR}/souvenir.json", 'rb') as f:
        #     data = f.read()
        #     return json.loads(data)
        async with httpx.AsyncClient(verify=False) as client:
            return await client.get(self.souvenirs_api)

    def get_case_name_list(self) -> list:
        return [case.name.replace(' ', '') for case in self.cases]

    def get_souvenir_name_list(self) -> list:
        return [sv.name.replace(' ', '') for sv in self.souvenirs]

    def get_random_case(self) -> dict:
        return random.choice(self.cases)

    def get_case_by_name(self, case_name: str) -> Crate:
        raw_name = case_name.replace("武器箱", "")
        for case in self.cases:
            if raw_name in case.name.replace(" ", ""):
                return case
        return None

    def get_souvenir_by_name(self, sv_name: str) -> Crate:
        raw_name = sv_name.replace("纪念包", "")
        for sv in self.souvenirs:
            if raw_name in sv.name.replace(" ", ""):
                return sv
        return None

    def open_case(self, case: Crate, probability_list, has_rare: bool) -> Contains:
        if has_rare and random.random() > probability_list[-1]:
            return random.choices(case.contains, probability_list, k=1)[0]
        else:
            return random.choices(case.contains_rare, k=1)[0]

    def open_souvenir(self, sv: Crate, probability_list) -> Contains:
        return random.choices(sv.contains, probability_list, k=1)[0]

    def open_crate_multiple(self, crate: Crate, amount: int) -> List[Contains]:
        items: List[Contains] = []
        result = self.calculate_prob_list(crate)
        for _ in range(amount):
            if (crate.type == "Case"):
                items.append(self.open_case(
                    crate, result["contains"], result["has_rare"]))
            else:
                items.append(self.open_souvenir(crate, result["contains"]))
        return items

    def calculate_prob_list(self, crate: Crate):
        all_rarities = [key.rarity for key in crate.contains]
        rare_amount_dict = {
            key: all_rarities.count(key) for key in all_rarities
        }
        unique_rarities = []
        [unique_rarities.append(x)
         for x in all_rarities if x not in unique_rarities]
        rare_prob_dict = {
            key: 0 for key in unique_rarities
        }

        has_mil_ind = False
        has_rare = False
        if "军规级" in unique_rarities and "工业" in unique_rarities:
            has_mil_ind = True
        if "隐秘" in unique_rarities:
            has_rare = True
        x = 1
        for i in range(len(unique_rarities)):
            if i == 0:
                rare_prob_dict[unique_rarities[i]] = 1
                continue
            elif has_mil_ind and unique_rarities[i] == "工业级":
                rare_prob_dict[unique_rarities[i]
                               ] = rare_prob_dict[unique_rarities[i-1]] * (5 / 24)
                continue
            elif has_rare and unique_rarities[i] == "隐秘":
                rare_prob_dict[unique_rarities[i]
                               ] = rare_prob_dict[unique_rarities[i-1]] * (2 / 5)
                continue
            else:
                rare_prob_dict[unique_rarities[i]
                               ] = rare_prob_dict[unique_rarities[i-1]] / 5
        # sum_prob = sum(rare_prob_dict.values())
        # for key in rare_prob_dict.keys():
        #     rare_prob_dict[key] = rare_prob_dict[key] / sum_prob
        contains_prob_list = []
        # 计算箱子品质的概率 / 计算箱子内品质的数量
        for item in crate.contains:
            contains_prob_list.append(
                rare_prob_dict[item.rarity] / rare_amount_dict[item.rarity])
        return {
            "contains": contains_prob_list,
            "has_rare": unique_rarities.index("隐秘") != -1
        }
