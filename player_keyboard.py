class PlayerKeyboard():
    def pick_action(self, dices, actions: list[str]) -> str:
        print(f"Dices: {dices}")
        print(f"Select an action:")
        print(f"{actions}")
        action = input("> ")

        return action
