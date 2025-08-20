from Game import Game

def main():
    game = Game()
    game.initialize(mission_count=1, npc_count=1)
    game.play_mission()

if __name__=="__main__":
    main()