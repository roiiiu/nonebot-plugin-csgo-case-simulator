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

        self.rarity_list = ["消费级", "工业级", "军规级", "受限", "保密", "隐秘", "特殊"]
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

    def open_case(self, case: Crate, probability_list) -> Contains:
        if random.random() > probability_list[-1] or not case.contains_rare:
            return random.choices(case.contains, probability_list)[0]
        else:
            return random.choice(case.contains_rare)

    def open_souvenir(self, sv: Crate, probability_list) -> Contains:
        return random.choices(sv.contains, probability_list)[0]

    def open_crate_multiple(self, crate: Crate, amount: int) -> List[Contains]:
        items: List[Contains] = []
        if (crate.type == "Case"):
            contains_pob_list = self.calculate_prob_list(crate)
            for _ in range(amount):
                items.append(self.open_case(crate, contains_pob_list))
        else:
            contains_pob_list = self.calculate_prob_list(crate)
            for _ in range(amount):
                items.append(self.open_souvenir(crate, contains_pob_list))
        return items

    def calculate_prob_list(self, crate: Crate):
        has_rarity = {key: False for key in self.rarity_list}
        for item in crate.contains:
            has_rarity[item.rarity] = True
        if crate.type == "Case":
            has_rarity["特殊"] = True

        crate_rarity_list = [key for key, value in has_rarity.items() if value]
        result_list = []
        has_mil_ind = False
        if "军规级" in crate_rarity_list and "工业" in crate_rarity_list:
            has_mil_ind = True
        x = 1
        for i in range(len(crate_rarity_list)):
            if i == 0:
                result_list.append(x)
                continue
            elif has_mil_ind and crate_rarity_list[i] == "工业级":
                result_list.append(result_list[i-1] * (5 / 24))
                continue
            elif crate_rarity_list[i] == "特殊":
                result_list.append(result_list[i-1] * (2 / 5))
                continue
            else:
                result_list.append(result_list[i-1] / 5)

        result_list = [x / sum(result_list) for x in result_list]
        contains_prob_list = []
        for item in crate.contains:
            contains_prob_list.append(
                result_list[crate_rarity_list.index(item.rarity)])

        return contains_prob_list
