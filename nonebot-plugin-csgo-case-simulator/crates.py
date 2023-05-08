import json
import random
from os.path import dirname

JSON_DIR = dirname(__file__) + "/json"


class Crates:
    def __init__(self):
        self.cases = []
        self.souvenirs = []

        self.probabilities = {
            "工业级": 0.63435,
            "军规级": 0.16693,
            "受限": 0.15985,
            "保密": 0.03205,
            "隐秘": 0.00640,
        }
        self.probabilities2 = {
            "军规级": 0.80128,
            "受限": 0.15985,
            "保密": 0.03205,
            "隐秘": 0.00640,
        }

        self.prob_s1 = {
            "消费级": 0.80537,
            "工业级": 0.16107,
            "军规级": 0.03356,
        }
        self.prob_s2 = {
            "工业级": 0.8,
            "军规级": 0.16107,
            "受限": 0.03333
        }
        self.prob_s3 = {
            "消费级": 0.8,
            "工业级": 0.16,
            "军规级": 0.03333,
            "受限": 0.00667
        }
        self.prob_s4 = {
            "消费级": 0.79893,
            "工业级": 0.15979,
            "军规级": 0.03329,
            "受限": 0.00666,
            "保密": 0.00133
        }
        self.prob_s5 = {
            "消费级": 0.79872,
            "工业级": 0.15974,
            "军规级": 0.03328,
            "受限": 0.00666,
            "保密": 0.00133,
            "隐秘": 0.00027
        }

    async def get_cases_json(self):
        with open(f"{JSON_DIR}/cases.json", 'rb') as f:
            data = f.read()
            return json.loads(data)

    async def get_souvenirs_json(self):
        with open(f"{JSON_DIR}/souvenir.json", 'rb') as f:
            data = f.read()
            return json.loads(data)

    def get_case_name_list(self) -> list:
        return [case["name"] for case in self.cases]

    def get_souvenir_name_list(self) -> list:
        return [sv["name"] for sv in self.souvenirs]

    def get_random_case(self) -> dict:
        return random.choice(self.cases)

    def get_case_by_name(self, case_name: str) -> dict:
        raw_name = case_name.replace("武器箱", "")
        for case in self.cases:
            if case["name"].replace(" ", "").find(raw_name) != -1:
                return case
        return None

    def get_souvenir_by_name(self, sv_name: str) -> dict:
        raw_name = sv_name.replace("纪念包", "")
        for sv in self.souvenirs:
            if sv["name"].replace(" ", "").find(raw_name) != -1:
                return sv
        return None

    def open_case(self, case: dict) -> dict:
        hasUncommon = False
        hasRare = False
        if random.random() > 0.00256 or not case["contains_rare"]:
            probability_dic = {}
            probability_list = []
            for item in case["contains"]:
                if item["rarity"] == "工业级":
                    hasUncommon = True
                if item["rarity"] == "军规级":
                    hasRare = True
            if hasUncommon and hasRare:
                probability_dic = self.probabilities
            else:
                probability_dic = self.probabilities2

            for item in case["contains"]:
                probability_list.append(
                    probability_dic[item["rarity"]])
            return random.choices(case["contains"], probability_list)[0]
        else:
            return random.choice(case["contains_rare"])

    def open_souvenir(self, sv: dict) -> dict:
        has_rarity = {
            "消费级": False,
            "工业级": False,
            "军规级": False,
            "受限": False,
            "保密": False,
            "隐秘": False
        }
        for item in sv["contains"]:
            has_rarity[item["rarity"]] = True
        probability_dic = {}
        probability_list = []
        if has_rarity["消费级"] and has_rarity["工业级"] and has_rarity["军规级"] and has_rarity["受限"] and has_rarity["保密"] and has_rarity["隐秘"]:
            probability_dic = self.prob_s5
        elif has_rarity["消费级"] and has_rarity["工业级"] and has_rarity["军规级"] and has_rarity["受限"] and has_rarity["保密"]:
            probability_dic = self.prob_s4
        elif has_rarity["消费级"] and has_rarity["工业级"] and has_rarity["军规级"] and has_rarity["受限"]:
            probability_dic = self.prob_s3
        elif has_rarity["工业级"] and has_rarity["军规级"] and has_rarity["受限"]:
            probability_dic = self.prob_s2
        elif has_rarity["消费级"] and has_rarity["工业级"] and has_rarity["军规级"]:
            probability_dic = self.prob_s1
        else:
            return None
        for item in sv["contains"]:
            probability_list.append(
                probability_dic[item["rarity"]])
        return random.choices(sv["contains"], probability_list)[0]

    def open_crate_multiple(self, crate: dict, open_crate_multiple: int) -> list:
        items = []
        if (crate["type"] == "Case"):
            for i in range(open_crate_multiple):
                items.append(self.open_case(crate))
        elif (crate["type"] == "Souvenir"):
            for i in range(open_crate_multiple):
                items.append(self.open_souvenir(crate))
        else:
            return None
        return items
