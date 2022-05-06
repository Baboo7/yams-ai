from utils import pick_rand


class PlayerDumb():
    def pick_action(self, dices, actions: list[str]) -> str:
        return pick_rand(actions)
