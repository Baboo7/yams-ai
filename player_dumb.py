from config import DICES_COUNT
from utils import pick_rand, rand_int


class PlayerDumb():
    def pick_action(self, actions: list[str]) -> str:
        return pick_rand(actions)

    def pick_dices(self, dices):
        pick_count = rand_int(1, DICES_COUNT)
        return dices[0:pick_count - 1]
