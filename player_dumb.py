from utils import pick_rand


class PlayerDumb():
    def pick_action(self, actions: list[str]) -> str:
        return pick_rand(actions)
