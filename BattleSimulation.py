import random
from CharacterDesign import Character, generate_character_based_on_name
from Agent import Agent
agent = Agent(api_key="sk-")

class BattleSimulation:
    def __init__(self, character1, character2):
        self.character1 = character1
        self.character2 = character2
        self.round_number = 1
        self.battle_log = []
        self.winner = None

    def decide_turn(self):
        """Determine which character attacks first based on their speed."""
        prob_char1 = self.character1.speed / (self.character1.speed + self.character2.speed)
        return self.character1 if random.random() < prob_char1 else self.character2

    def simulate_turn(self, attacker, defender):
        """Simulate an attack turn with dodge and attack choices."""
        
        # Dodge check for defender
        dodge_description, dodged = defender.dodge()
        if dodged:
            self.battle_log.append(f"Round {self.round_number}: {dodge_description}")
            print(f"Round {self.round_number}: {dodge_description}")
            return

        # Decide between normal and ability attack (20% chance of ability attack)
        if random.random() < 0.2:
            attack_description, damage = attacker.ability_attack(defender)
            action_type = "ability"
        else:
            attack_description, damage = attacker.normal_attack(defender)
            action_type = "normal"

        # Log and print attack result
        self.battle_log.append(f"Round {self.round_number}: {attack_description}")
        print(f"Round {self.round_number}: {attack_description}")

        # Apply damage to defender and log remaining HP
        damage_description, effective_damage = defender.take_damage(damage)
        self.battle_log.append(f"{damage_description} {defender.name} takes {effective_damage} damage. Remaining HP: {defender.hp}")
        print(f"{damage_description} {defender.name} takes {effective_damage} damage. Remaining HP: {defender.hp}")

        # Log summary of turn with attacker, damage, and remaining HP for both characters
        self.battle_log.append(
            f"{attacker.name} ({attacker.hp} HP) vs. {defender.name} ({defender.hp} HP) | "
            f"Attack Type: {action_type} | Damage: {effective_damage}\n"
        )
        print(
            f"{attacker.name} ({attacker.hp} HP) vs. {defender.name} ({defender.hp} HP) | "
            f"Attack Type: {action_type} | Damage: {effective_damage}\n"
        )

    def run_battle(self):
        """Run the battle until one character's HP reaches zero."""
        print(f"Battle Start: {self.character1.name} vs {self.character2.name}\n")
        self.battle_log.append(f"Battle Start: {self.character1.name} vs {self.character2.name}\n")

        while self.character1.hp > 0 and self.character2.hp > 0:
            # Round header
            self.battle_log.append(f"\n--- Round {self.round_number} ---")
            # print(f"\n--- Round {self.round_number} ---")

            # Determine attacking character for this round
            attacker = self.decide_turn()
            defender = self.character2 if attacker == self.character1 else self.character1

            # Simulate the attack turn
            self.simulate_turn(attacker, defender)

            # Check for winner
            if defender.hp <= 0:
                self.battle_log.append(f"\n{attacker.name} has won the battle!")
                # print(f"\n{attacker.name} has won the battle!")
                break

            # Increment round number
            self.round_number += 1
        if self.character1.hp>0:
            self.winner = self.character1
        else:
            self.winner = self.character2
        
        # Print battle log summary after the battle
        log_str = "\n".join(self.battle_log)
        log_plot = agent.call(f"""
        Use the following battle log to create an interesting story of this battle in nearly 80 words, do not use any special symbols in your response:
        {log_str}
        """)
        return log_plot


# Example usage with your `CharacterDesign.py` Character class
# Generate two characters using the `generate_character_based_on_name` function
# character1 = generate_character_based_on_name(agent, "Steph Curry")
# character2 = generate_character_based_on_name(agent, "Asuka")

# # Initialize the battle simulation with generated characters
# battle = BattleSimulation(character1, character2)

# # Run the battle, which will print each action in real time
# battle_result = battle.run_battle()

