import random
import httpx


class Cases:
    def __init__(self):
        self.cases_api = "https://bymykel.github.io/CSGO-API/api/zh-CN/crates/cases.json"

        self.cases = []

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

    async def get_cases_json(self):
        async with httpx.AsyncClient() as client:
            return await client.get(self.cases_api)

    def get_case_name_list(self) -> list:
        return [case["name"] for case in self.cases]

    def get_random_case(self) -> dict:
        return random.choice(self.cases)

    def get_case_by_name(self, case_name: str) -> dict:
        raw_name = case_name.replace("武器箱", "")
        for case in self.cases:
            if case["name"].replace(" ", "").find(raw_name) != -1:
                return case
        return None

    def open_case(self, case_id: str) -> dict:
        hasUncommon = False
        hasRare = False
        for case in self.cases:
            if case["id"] == case_id:
                if random.random() > 0.00256:
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
        return None

    def open_case_multiple(self, case_id: str, open_case_multiple: int) -> list:
        items = []
        for i in range(open_case_multiple):
            items.append(self.open_case(case_id))
        return items
