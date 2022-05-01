from config import BONUS_THRESHOLD, BONUS_VALUE, DICE_VAL_MAX
from utils import has


def get_value_x_of_a_kind(x: int, list: list[any]) -> int:
    values = set(list)
    for v in values:
        if list.count(v) >= x:
            return v
    return None


def has_x_of_a_kind(x: int, list: list[any]) -> bool:
    values = set(list)
    for v in values:
        if list.count(v) >= x:
            return True
    return False


def has_full_house(list: list[any]) -> bool:
    values = set(list)

    if len(values) != 2:
        return False

    v1 = values.pop()
    v1_count = list.count(v1)
    if v1_count < 2 or v1_count > 3:
        return False

    return True


def create_score_sheet():
    return [
        {
            "id": "1",
            "score": None,
            "scorable": lambda score_sheet, dices: not score_sheet.has_item_been_scored("1") and has(dices, 1),
            "compute_score": lambda dices: dices.count(1) * 1,
        },
        {
            "id": "2",
            "score": None,
            "scorable": lambda score_sheet, dices: not score_sheet.has_item_been_scored("2") and has(dices, 2),
            "compute_score": lambda dices: dices.count(2) * 2,
        },
        {
            "id": "3",
            "score": None,
            "scorable": lambda score_sheet, dices: not score_sheet.has_item_been_scored("3") and has(dices, 3),
            "compute_score": lambda dices: dices.count(3) * 3,
        },
        {
            "id": "4",
            "score": None,
            "scorable": lambda score_sheet, dices: not score_sheet.has_item_been_scored("4") and has(dices, 4),
            "compute_score": lambda dices: dices.count(4) * 4,
        },
        {
            "id": "5",
            "score": None,
            "scorable": lambda score_sheet, dices: not score_sheet.has_item_been_scored("5") and has(dices, 5),
            "compute_score": lambda dices: dices.count(5) * 5,
        },
        {
            "id": "6",
            "score": None,
            "scorable": lambda score_sheet, dices: not score_sheet.has_item_been_scored("6") and has(dices, 6),
            "compute_score": lambda dices: dices.count(6) * 6,
        },
        {
            "id": "three-of-a-kind",
            "score": None,
            "scorable": lambda score_sheet, dices: not score_sheet.has_item_been_scored("three-of-a-kind") and has_x_of_a_kind(3, dices),
            "compute_score": lambda dices: get_value_x_of_a_kind(3, dices) * 3,
        },
        {
            "id": "four-of-a-kind",
            "score": None,
            "scorable": lambda score_sheet, dices: not score_sheet.has_item_been_scored("four-of-a-kind") and has_x_of_a_kind(4, dices),
            "compute_score": lambda dices: get_value_x_of_a_kind(4, dices) * 4,
        },
        {
            "id": "full-house",
            "score": None,
            "scorable": lambda score_sheet, dices: not score_sheet.has_item_been_scored("full-house") and has_full_house(dices),
            "compute_score": lambda dices: 25,
        },
        {
            "id": "small-run",
            "score": None,
            "scorable": lambda score_sheet, dices: not score_sheet.has_item_been_scored("small-run") and has(dices, 1) and has(dices, 2) and has(dices, 3) and has(dices, 4) and has(dices, 5),
            "compute_score": lambda dices: 30,
        },
        {
            "id": "big-run",
            "score": None,
            "scorable": lambda score_sheet, dices: not score_sheet.has_item_been_scored("big-run") and has(dices, 2) and has(dices, 3) and has(dices, 4) and has(dices, 5) and has(dices, 6),
            "compute_score": lambda dices: 40,
        },
        {
            "id": "yams",
            "score": None,
            "scorable": lambda score_sheet, dices: not score_sheet.has_item_been_scored("yams") and has_x_of_a_kind(5, dices),
            "compute_score": lambda dices: 50,
        },
        {
            "id": "luck",
            "score": None,
            "scorable": lambda score_sheet, dices: not score_sheet.has_item_been_scored("luck"),
            "compute_score": lambda dices: sum(dices)
        },
    ]


class ScoreSheet():
    def __init__(self):
        self.sheet = create_score_sheet()

    def __str__(self) -> str:
        return str([(it["id"], it["score"]) for it in self.sheet])

    def compute_score(self) -> int:
        score = 0
        for item in self.sheet:
            score += item["score"]

        if self.has_bonus():
            score += BONUS_VALUE

        return score

    def has_bonus(self) -> bool:
        sum = 0
        for i in range(1, DICE_VAL_MAX + 1):
            item = self.find_score_item(str(i))
            sum += item["score"]

        return sum >= BONUS_THRESHOLD

    def get_score(self, id, dices):
        item = self.find_score_item(id)
        return item["compute_score"](dices)

    def set_score(self, id, dices):
        item = self.find_score_item(id)
        item["score"] = self.get_score(id, dices)

    def has_item_been_scored(self, id) -> bool:
        item = self.find_score_item(id)
        return item["score"] != None

    def cross_out_item(self, id):
        item = self.find_score_item(id)
        item["score"] = 0

    def get_scorable_items(self, dices: list[int]) -> list[str]:
        item_ids = [it["id"]
                    for it in self.sheet if it["scorable"](self, dices)]
        return item_ids

    def get_crossable_items(self) -> list[str]:
        crossable_items = []
        for item in self.sheet:
            if (item["score"] == None):
                crossable_items.append(item["id"])
        return crossable_items

    def can_cross_out_item(self) -> bool:
        return len(self.get_crossable_items()) > 0

    def find_score_item(self, id: str):
        i = 0
        while i < len(self.sheet):
            item = self.sheet[i]
            if (item["id"] == id):
                return item
            i += 1
        raise Exception(f"Could not find score item w/ id {id}")
