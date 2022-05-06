from config import DICE_VAL_MAX, DICE_VAL_MIN, DICES_COUNT, THROW_COUNT_MAX

from score_sheet import ScoreSheet
from utils import concat, has, rand_int


def score_item_id_to_action(score_item_id: str) -> str:
    return "SCORE_" + score_item_id.upper().replace("-", "_")


def action_to_score_item_id(action: str) -> str:
    return action.replace("SCORE_", "").lower().replace("_", "-")


CROSS_OUT_PREFIX = "CROSS_OUT_"


def cross_out_item_id_to_action(cross_out_item_id: str) -> str:
    return CROSS_OUT_PREFIX + cross_out_item_id.upper().replace("-", "_")


def action_to_cross_out_item_id(action: str) -> str:
    return action.replace(CROSS_OUT_PREFIX, "").lower().replace("_", "-")


def roll_dices(nb: int):
    dices = []
    for i in range(0, nb):
        dices.append(rand_int(DICE_VAL_MIN, DICE_VAL_MAX))
    return dices


class GameEngine():
    def __init__(self, player):
        self.running = False
        self.score_sheet = ScoreSheet()
        self.throws = 0
        self.dices = []
        self.dices_picked = []
        self.player = player
        self.last_action = ""

    def start_game(self):
        self.running = True
        turn = 1
        while self.running:
            self.run_game(turn)
            turn += 1
        self.end_game()

    def end_game(self):
        print("game ended")
        print("score: ", self.score_sheet.compute_score())
        print(self.score_sheet)

    def run_game(self, turn):
        print(f"------ TURN {turn} ------")
        print(
            f"dices: {self.dices} / picked: {self.dices_picked} / throw: {self.throws}")
        actions = self.list_actions()
        print(f"available actions: {actions}")

        action: str = self.pick_action(actions)
        print("selected action: ", action)

        if action == None:
            self.running = False
        elif action == "THROW_DICES_ALL":
            self.dices = roll_dices(DICES_COUNT)
            self.dices_picked = []
            print(f"dices: {self.dices}")
            self.throws += 1
        elif action == "THROW_DICES_REMAINING":
            dices_rolled = roll_dices(len(self.dices))
            self.dices = concat(self.dices_picked, dices_rolled)
            self.dices_picked = []
            print(f"dices: {self.dices}")
            self.throws += 1
        elif action.startswith("PICK_VALUE_"):
            value = int(action.replace("PICK_VALUE_", ""))
            print(f"value picked: {value}")
            self.dices_picked.append(value)
            self.dices.remove(value)
        elif action.startswith("SCORE_"):
            self.score(action_to_score_item_id(action))
        elif action.startswith(CROSS_OUT_PREFIX):
            self.cross_out(action_to_cross_out_item_id(action))

        self.last_action = action

        print("")

    def list_actions(self):
        actions = []

        if self.throws < THROW_COUNT_MAX:
            for value in self.get_pickable_values():
                actions.append(f"PICK_VALUE_{value}")

        if len(self.dices) == DICES_COUNT:
            for id in self.score_sheet.get_scorable_items(self.dices):
                actions.append(score_item_id_to_action(id))

            for id in self.score_sheet.get_crossable_items():
                actions.append(cross_out_item_id_to_action(id))

        if 0 < len(self.dices) and len(self.dices) < DICES_COUNT and self.throws < THROW_COUNT_MAX:
            actions.append('THROW_DICES_REMAINING')

        if self.throws < THROW_COUNT_MAX:
            actions.append("THROW_DICES_ALL")

        return actions

    def end_turn(self):
        self.dices = []
        self.dices_picked = []
        self.throws = 0

    def score(self, item_id):
        self.score_sheet.set_score(item_id, self.dices)
        score = self.score_sheet.get_score(item_id, self.dices)
        print("scoring ", item_id, " (", score, " pts)")
        self.end_turn()

    def cross_out(self, item_id):
        print("crossing out ", item_id)
        self.score_sheet.cross_out_item(item_id)
        self.end_turn()

    def pick_action(self, actions):
        if len(actions) == 0:
            return None

        prompt = True
        while prompt:
            try:
                action = self.player.pick_action(self.dices, actions)

                if action.lower() == "q" or action.lower() == "quit":
                    self.running = False
                else:
                    actions.index(action)
                prompt = False
            except:
                print(f"action {action} is invalid")
                pass

        return action

    def get_pickable_values(self) -> list[int]:
        return list(set(self.dices))
