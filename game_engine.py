from config import DICE_VAL_MAX, DICE_VAL_MIN, DICES_COUNT, THROW_COUNT_MAX

from score_sheet import ScoreSheet
from utils import concat, has, rand_int


def score_item_id_to_action(score_item_id: str) -> str:
    return "SCORE_" + score_item_id.upper().replace("-", "_")


def action_to_score_item_id(action: str) -> str:
    return action.replace("SCORE_", "").lower().replace("_", "-")


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
        self.player = player
        self.last_action = ""

    def start_game(self):
        self.running = True
        while self.running:
            self.run_game()
        self.end_game()

    def end_game(self):
        print("game ended")
        print("score: ", self.score_sheet.compute_score())
        print(self.score_sheet)

    def run_game(self):
        action: str = self.pick_action()
        print("selected action: ", action)

        if action == None:
            self.running = False
        elif action == "THROW_DICES":
            dice_count = DICES_COUNT if len(
                self.dices) == DICES_COUNT else DICES_COUNT - len(self.dices)
            dices_rolled = roll_dices(dice_count)
            self.dices = concat(self.dices, dices_rolled)
            print("dices: ", self.dices)
            self.throws += 1
        elif action == "PICK_DICES":
            dices_picked = self.player.pick_dices(self.dices)
            print("dices picked: ", dices_picked)
            self.dices = dices_picked
        elif action.startswith("SCORE_"):
            self.score(action_to_score_item_id(action))
        elif action == "CROSS_OUT_ITEM":
            items_crossable = self.score_sheet.get_crossable_items()
            item_to_cross_out = self.player.pick_item_to_cross_out(
                items_crossable)
            print("crossing item ", item_to_cross_out)
            self.score_sheet.cross_out_item(item_to_cross_out)
            self.end_turn()

        self.last_action = action

    def list_actions(self):
        if len(self.dices) < DICES_COUNT:
            return ["THROW_DICES"]

        actions = []
        if self.throws < THROW_COUNT_MAX and len(self.dices) < DICES_COUNT:
            actions.append('THROW_DICES')

        if self.throws < THROW_COUNT_MAX and len(self.dices) == DICES_COUNT and self.last_action != "PICK_DICES":
            actions.append('PICK_DICES')

        for id in self.score_sheet.get_scorable_items(self.dices):
            actions.append(score_item_id_to_action(id))

        if self.score_sheet.can_cross_out_item():
            actions.append('CROSS_OUT_ITEM')

        return actions

    def end_turn(self):
        self.dices = []
        self.throws = 0

    def score(self, item_id):
        self.score_sheet.set_score(item_id, self.dices)
        score = self.score_sheet.get_score(item_id, self.dices)
        print("scoring ", item_id, " (", score, " pts)")
        self.end_turn()

    def pick_action(self):
        actions = self.list_actions()

        if len(actions) == 0:
            return None

        return self.player.pick_action(actions)
