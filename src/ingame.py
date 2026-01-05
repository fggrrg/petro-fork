import sys
import json
import random
import time
from logic import pull_state

class Battle:
    def __init__(self, battle_id, player1_name, player2_name):
        self.battle_id = battle_id
        self.player1_name = player1_name
        self.player2_name = player2_name
    
    def process_command(self, username, command):
        parts = command.strip().lower().split()
        action = parts[0] if parts else ""
        
        if action == "get_state":
            self.send_state("Battle in progress")
        elif action == "attack":
            self.execute_attack(username)
        elif action == "switch":
            if len(parts) < 2:
                self.send_state("Specify pet index to switch")
                return
            try:
                pet_index = int(parts[1])
                if username == self.player1_name:
                    if 0 <= pet_index < len(self.player1_pets) and self.player1_pets[pet_index]['alive']:
                        self.p1_active = pet_index
                        self.add_log(f"{username} switched to {self.player1_pets[pet_index]['name']}")
                        self.send_state(f"{username} switched pets")
                else:
                    if 0 <= pet_index < len(self.player2_pets) and self.player2_pets[pet_index]['alive']:
                        self.p2_active = pet_index
                        self.add_log(f"{username} switched to {self.player2_pets[pet_index]['name']}")
                        self.send_state(f"{username} switched pets")
            except (ValueError, IndexError):
                self.send_state("Invalid pet index")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(json.dumps({"type": "error", "message": "Invalid arguments"}))
        sys.exit(1)
    
    battle_id = sys.argv[1]
    player1 = sys.argv[2]
    player2 = sys.argv[3]
    
    battle = Battle(battle_id, player1, player2)
    battle.send_state(f"Battle started! {player1} vs {player2}")
    
    try:
        for line in sys.stdin:
            command = line.strip()
            if not command or command == "exit":
                break
            
            if ':' in command:
                username, cmd = command.split(':', 1)
                battle.process_command(username, cmd)
            else:
                battle.send_state("Invalid command format")
                
    except Exception as e:
        print(json.dumps({"type": "error", "message": str(e)}))
        sys.stderr.write(f"Battle error: {str(e)}\n")