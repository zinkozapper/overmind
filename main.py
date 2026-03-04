import os
import sc2
from datetime import datetime
from sc2 import maps
from sc2.player import Bot, Computer
from sc2.data import Race
from bots.terran_bot import TerranBot
from bots.zerg_bot import ZergBot
from bots.protoss_bot import ProtossBot

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    role = os.getenv("ROLE", "bot")
    map_path = "PersephoneAIE_v4"
    replay_dir = "/StarCraftII/Replays"
    replay_name = f"Match_{timestamp}.SC2Replay"
    full_replay_path = os.path.join(replay_dir, replay_name)
    if role == "coordinator":
        print("Coordinator: Setting up the match...")
        # This function acts as the 'Coordinator'

        sc2.main.run_game(
            maps.get(map_path),
            [
                Bot(Race.Terran, TerranBot()), # Bot 1
		Bot(Race.Protoss, ProtossBot())
                #Computer(Race.Protoss, Difficulty.Normal)      # Bot 2
            ],
            realtime=False,
            save_replay_as=full_replay_path
        )
    elif role == "bot":
        # In this specific 'run_game' setup, the coordinator 
        # actually launches the bots. You might not even 
        # need the 'bot' role containers if you run them all in one process.
        print("Bot container started (waiting for coordinator)...")

if __name__ == "__main__":
    main()
