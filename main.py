from game_engine import GameEngine
from player_dumb import PlayerDumb


def main():
  player = PlayerDumb()

  engine = GameEngine(player)
  engine.start_game()


main()