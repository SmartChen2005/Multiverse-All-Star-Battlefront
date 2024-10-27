import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from Agent import Agent
import ast
import random

def extract_list(input_string):
    """Extracts a list from a string representation within square brackets."""
    # Find the indices of the first `[` and the last `]`
    start_index = input_string.index('[')
    end_index = input_string.rindex(']')
    
    # Extract the substring that represents the list
    list_str = input_string[start_index:end_index + 1]
    
    # Convert the extracted substring to an actual list
    try:
        contents_list = ast.literal_eval(list_str)
        if isinstance(contents_list, list):
            return contents_list
        else:
            print("The extracted content is not a list.")
            return None
    except (ValueError, SyntaxError):
        print("The input string does not contain a valid list format.")
        return None

def extract_dictionary(input_string):
    """Extracts a dictionary from a string representation within curly braces."""
    # Find the indices of the first `{` and the last `}`
    start_index = input_string.index('{')
    end_index = input_string.rindex('}')
    
    # Extract the substring that represents the dictionary
    dict_str = input_string[start_index:end_index + 1]
    
    # Convert the extracted substring to an actual dictionary
    try:
        contents_dict = ast.literal_eval(dict_str)
        if isinstance(contents_dict, dict):
            return contents_dict
        else:
            print("The extracted content is not a dictionary.")
            return None
    except (ValueError, SyntaxError):
        print("The input string does not contain a valid dictionary format.")
        return None

def load_character_from_dict(diction):
    character = Character(
        name=diction["name"],
        hp = diction["hp"],
        attack = diction["attack"],
        speed = diction["speed"],
        defense = diction["defense"],
        weapons=diction["weapons"],
        ability=diction["abilities"],
        description=diction["description"], 
        image = diction["image"],
        score = diction["score"]
    )
    return character

agent = Agent(api_key="")
agent.start_new_chat()

def generate_character_names(agent=agent, num_names=8):
    """
    Generates a specified number of character names suitable for a battle arena game.
    
    Parameters:
        agent (Agent): The Agent instance to make API calls.
        num_names (int): The number of character names to generate.
    
    Returns:
        list: A list of generated character names.
    """
    prompt = (
        f"Generate {num_names} existing famous character names that suit a battle arena game "
        "(e.g., Superman, Tony Stark, Batman). Names only, and don't give those already appeared "
        "from previous chat. Try to be more versatile in terms of the cinema they are created. "
        "Return as python list: characters = []"
    )
    response = agent.call(prompt)
    return extract_list(response)

# character_names = generate_character_names(agent)
# print(character_names)

def generate_character_based_on_name(agent=agent, character_name=""):
    """
    Generates detailed character information based on the provided character name.

    Parameters:
        agent (Agent): The Agent instance to make API calls.
        character_name (str): The name of the character to generate information for.

    Returns:
        Character: An instance of the Character class containing background info, weapons, abilities, and stats.
    """
    # Generate stats dictionary
    stats_prompt = f"hp(range 30-60), attack(10-30), speed(30-40), and defense(20-40) based on your understanding of {character_name} (with a total of 100 points). Return as python dictionary: stats={{}}"
    character_stats = extract_dictionary(agent.call(stats_prompt))

    # Generate background info
    background_prompt = f"Give me a one-line description of {character_name}'s basic background information, limited to 30 words"
    character_bg_info = agent.call(background_prompt)
    
    # Generate weapons list
    weapons_prompt = "Give me a list of 5 possible weapons (ways) for normal attack, return as python list: weapons=[]"
    character_weapons = extract_list(agent.call(weapons_prompt))
    
    # Generate abilities dictionary
    abilities_prompt = "Give me a list of 2 possible abilities (ultimate). return as python dictionary: ability={} with ability name as key and 15-words description as value"
    character_ability = extract_dictionary(agent.call(abilities_prompt))

    character = Character(
        name=character_name,
        hp = max(character_stats.get('hp', 0), 1),
        attack = max(character_stats.get('attack', 0), 1),
        speed = max(character_stats.get('speed', 0), 1),
        defense = max(character_stats.get('defense', 0), 1),
        weapons=character_weapons,
        ability=character_ability,
        description=character_bg_info
    )
    
    return character

def generate_character_based_on_description(agent=agent, character_description=""):
    """
    Generates detailed character information based on a provided character description.

    Parameters:
        agent (Agent): The Agent instance to make API calls.
        character_description (str): A brief description of the character's features.

    Returns:
        Character: An instance of the Character class containing background info, weapons, abilities, and stats.
    """
    # Generate character name based on description
    name_prompt = f"Based on the description '{character_description}', generate a suitable name for the character. Give me the name only"
    character_name = agent.call(name_prompt).strip()

    # Generate stats dictionary based on description
    stats_prompt = f"Using the description '{character_description}', assign hp(range 30-60), attack(10-30), speed(30-40), and defense(20-40) with a total of 100 points. Return as a Python dictionary: stats={{}}"
    character_stats = extract_dictionary(agent.call(stats_prompt))

    # Generate background info
    background_prompt = f"Provide a one-line background for a character described as '{character_description}', limited to 30 words."
    character_bg_info = agent.call(background_prompt)

    # Generate weapons list based on description
    weapons_prompt = f"List 5 possible weapons or attack methods suitable for a character with features like '{character_description}'. Return as a Python list: weapons=[]"
    character_weapons = extract_list(agent.call(weapons_prompt))

    # Generate abilities dictionary based on description
    abilities_prompt = f"Suggest 2 unique abilities for a character described as '{character_description}', formatted as a Python dictionary: ability={{}} with ability name as key and 15-words description as value."
    character_ability = extract_dictionary(agent.call(abilities_prompt))

    # Create an instance of the Character class
    character = Character(
        name=character_name,
        hp = max(character_stats.get('hp', 0), 1),
        attack = max(character_stats.get('attack', 0), 1),
        speed = max(character_stats.get('speed', 0), 1),
        defense = max(character_stats.get('defense', 0), 1),
        weapons=character_weapons,
        ability=character_ability,
        description=character_bg_info
    )

    # Print or log background info for reference
    # print(f"Generated character: {character_name} - {character_bg_info}")

    return character


class Character:
    
    def __init__(self, name, hp, attack, speed, defense, weapons, ability, description, image="", score=0):
        self.description = description
        self.name = name
        self.hp = hp
        self.attack = attack
        self.speed = speed
        self.defense = defense
        self.weapons = weapons
        self.ability = ability
        self.max_hp = hp
        self.image = image
        self.score = score


        self.agent = Agent(api_key="")
        self.sd_promt = self.agent.call(f"""Generate a set of various Stable Diffusion keywords from the desciption here "{self.__str__()}" to plug into a SD model in order to visual the character above. Be concise and focus on the physical appearances. If you already know the character, please use your own knowledge about the character to be more detailed in order to help SD to draw them. Focus more on physical appearances such as hair colour, eye colour and body shapes. More is better. Use the exact format as what SD used.""")

    def normal_attack(self, characterToBeAttacked):
        # randomly select one weapon from weapon list 
        # use LLM agent to generate an attack description with the weapon to characterToBeAttacked 
        # apply attack damage to enemy
        # return type should be a list of with index 0 being the description(string), and index 1 being attack damage (int)
        weapon = random.choice(self.weapons)

        # Using the LLM agent to generate a vivid attack description
        # prompt = (
        #     f"{self.name} prepares to strike with their {weapon}. Describe an intense and cinematic attack on "
        #     f"{characterToBeAttacked.name}, including the attack's effects and any reactions from the target."
        # )
        # description = self.agent.call(prompt)

        description = f"{self.name} attacks {characterToBeAttacked.name} with {weapon}."
        damage = self.attack
        characterToBeAttacked.take_damage(damage)
        return [description, damage]

    def ability_attack(self, characterToBeAttacked):
        # ability attack damage is double the basic attack damage
        # basically works the same as attack
        weapon = random.choice(self.weapons)
        
        # Using the LLM agent for a powerful, ability-focused attack description
        # prompt = (
        #     f"{self.name} channels a unique ability, unleashing an extraordinary attack with their {weapon}. "
        #     f"Describe a powerful and visually striking ability attack on {characterToBeAttacked.name} with heightened effects."
        # )
        # description = self.agent.call(prompt)
        
        description = f"{self.name} uses their special ability with {weapon} against {characterToBeAttacked.name}."
        damage = 2 * self.attack
        characterToBeAttacked.take_damage(damage)
        return [description, damage]

    def take_damage(self, damage):
        # damage reduce peercentage is decided by formula defense/(defense+hp)
        # apply damage to myself in reducing max_hp
        reduction_percentage = self.defense / (self.defense + self.max_hp)
        effective_damage = int(damage * (1 - reduction_percentage))
        self.hp -= effective_damage
        
        # Generate a description for taking damage
        # prompt = (
        #     f"{self.name} endures an attack, losing {effective_damage} HP after accounting for their defenses. "
        #     f"Describe {self.name}'s reaction to the damage and any signs of struggle."
        # )
        # description = self.agent.call(prompt)
        description = f"""{self.name} endures an attack, losing {effective_damage} HP after accounting for their defenses. "
                      Describe {self.name}'s reaction to the damage and any signs of struggle."""

        return [description, effective_damage]
    
    def dodge(self):
        # dodge is for dodging basic attack, not ability attack
        # the logic of dodge is based on speed of character, speed value of 30 means 30% chance of dodge, 20 means 20% chance
        dodge_chance = self.speed * 0.9 / 100
        dodged = random.random() < dodge_chance
        
        if dodged:
            # Generate a description for a successful dodge
            # prompt = (
            #     f"{self.name} attempts a quick dodge to evade an incoming attack. Describe a successful, agile dodge, "
            #     f"highlighting {self.name}'s speed and skill."
            # )
            # description = self.agent.call(prompt)
            description = f"""{self.name} attempts a quick dodge to evade an incoming attack. Describe a successful, agile dodge, "
                            highlighting {self.name}'s speed and skill."""
        else:
            # Generate a description for a failed dodge
            # prompt = (
            #     f"{self.name} tries to dodge an incoming attack but is too slow. Describe {self.name}'s near miss and frustration."
            # )
            # description = self.agent.call(prompt)
            description = f"{self.name} tries to dodge an incoming attack but is too slow. Describe {self.name}'s near miss and frustration."
        
        return [description, dodged]

    def revive(self):
        # when a new round starts, revie character for new battle, hp reset to hp_max
        self.hp = self.max_hp

    def __str__(self):
        """Returns a string representation of the character's details."""
        abilities_str = '\n  '.join([f"{name}: {desc}" for name, desc in self.ability.items()])
        weapons_str = ', '.join(self.weapons)
        return (f"Character Name: {self.name}\n"
                f"HP: {self.hp}\n"
                f"Attack: {self.attack}\n"
                f"Speed: {self.speed}\n"
                f"Defense: {self.defense}\n"
                f"Weapons: {weapons_str}\n"
                f"Abilities:\n  {abilities_str}")
    
    def to_dict(self):
        # {"name": "Character 1", "image": cwd+"1.jpeg", "hp": 100, "attack": 30, "speed": 10, "defense": 20, "description": "Description of Character 1.","score":0, "weapons":[], "abilities":"abilities"},
        return {"name":self.name, "image":self.image, "hp":self.hp, "attack":self.attack, "speed":self.speed, "defense":self.defense, "description":self.description, "score":self.score, "weapons":self.weapons, "abilities":self.ability}


# character_name = "Steph Curry"  # Replace with your desired character name
# character = generate_character_based_on_name(agent, character_name)

# character1 = generate_character_based_on_name(agent, "Steph Curry")
# # print(character1)
# character2 = generate_character_based_on_name(agent, "Asuka from Evangelion")
# # print(character2)
# # print(character2.sd_promt)

# print(character1.normal_attack(character2))
