import pygame
import sys
import os
import random
import sounddevice as sd
from transformers import pipeline
from CharacterDesign import Character, generate_character_based_on_name, generate_character_names, load_character_from_dict
from BattleSimulation import BattleSimulation

cwd = os.getcwd() +"/picture/"


WIDTH, HEIGHT = 1000, 800 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Character Selection Screen")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


CARD_WIDTH, CARD_HEIGHT = 200, 300  
CARD_SPACING = 30  
CARD_RADIUS = 20

characters_name_list_s = generate_character_names()
character_list = []
for c_name in characters_name_list_s:
    character_list.append(generate_character_based_on_name(character_name=c_name).to_dict())

for index in range(len(character_list)):
    character_list[index]["image"] = f"{cwd}{index+1}.jpeg"

characters = character_list


# characters = [
#     {"name": "Character 1", "image": cwd+"1.jpeg", "hp": 100, "attack": 30, "speed": 10, "defense": 20, "description": "Description of Character 1.","score":0, "weapons":[], "abilities":"abilities"},
#     {"name": "Character 2", "image": cwd+"2.jpeg", "hp": 120, "attack": 25, "speed": 15, "defense": 30, "description": "Description of Character 2.","score":0, "weapons":[], "abilities":"abilities"},
#     {"name": "Character 3", "image": cwd+"3.jpeg", "hp": 90, "attack": 40, "speed": 5, "defense": 15, "description": "Description of Character 3.","score":0, "weapons":[], "abilities":"abilities"},
#     {"name": "Character 4", "image": cwd+"4.jpeg", "hp": 110, "attack": 35, "speed": 12, "defense": 25, "description": "Description of Character 4.","score":0, "weapons":[], "abilities":"abilities"},
#     {"name": "Character 5", "image": cwd+"5.jpeg", "hp": 95, "attack": 38, "speed": 14, "defense": 22, "description": "Description of Character 5.","score":0, "weapons":[], "abilities":"abilities"},
#     {"name": "Character 6", "image": cwd+"6.jpeg", "hp": 115, "attack": 28, "speed": 16, "defense": 28, "description": "Description of Character 6.","score":0, "weapons":[], "abilities":"abilities"},
#     {"name": "Character 7", "image": cwd+"7.jpeg", "hp": 105, "attack": 32, "speed": 11, "defense": 26, "description": "Description of Character 7.","score":0, "weapons":[], "abilities":"abilities"},
#     {"name": "Character 8", "image": cwd+"8.jpeg", "hp": 125, "attack": 22, "speed": 18, "defense": 35, "description": "Description of Character 8.","score":0, "weapons":[], "abilities":"abilities"},
# ]


pygame.init()

for character in characters:
    character["image"] = pygame.image.load(character["image"]).convert_alpha()
    character["image"] = pygame.transform.scale(character["image"], (CARD_WIDTH - 20, CARD_HEIGHT - 100))  # Resize to fit in card


font = pygame.font.Font(None, 24)

def draw_text_centered(text, x, y, max_width):
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:

        test_line = f"{current_line} {word}".strip()
        line_width = font.size(test_line)[0]
        
        if line_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    

    if current_line:
        lines.append(current_line)


    for i, line in enumerate(lines):
        line_surface = font.render(line, True, BLACK)
        line_x = x + (max_width - line_surface.get_width()) // 2  
        screen.blit(line_surface, (line_x, y + i * line_surface.get_height()))

def draw_card(character, x, y, hover=False):

    pygame.draw.rect(screen, WHITE, (x, y, CARD_WIDTH, CARD_HEIGHT), border_radius=CARD_RADIUS)
    pygame.draw.rect(screen, BLACK, (x, y, CARD_WIDTH, CARD_HEIGHT), 2, border_radius=CARD_RADIUS)


    if hover:

        attributes = [
            f"HP: {character['hp']}",
            f"Attack: {character['attack']}",
            f"Speed: {character['speed']}",
            f"Defense: {character['defense']}"
        ]
        

        attribute_start_y = y + 20  

        for attribute in attributes:

            attribute_surface = font.render(attribute, True, BLACK)
            attribute_x = x + (CARD_WIDTH - attribute_surface.get_width()) // 2  # Cen
            screen.blit(attribute_surface, (attribute_x, attribute_start_y))
            attribute_start_y += 25  


        description_text = character["description"]
        draw_text_centered(description_text, x + 10, y + 120, CARD_WIDTH - 20) 
    else:
        image = character["image"]
        screen.blit(image, (x + 10, y + 40)) 


    text = font.render(character["name"], True, BLACK)
    screen.blit(text, (x + (CARD_WIDTH - text.get_width()) // 2, y + CARD_HEIGHT - 30)) 



"""

Combat Visualization

"""
def wrap_text(text, font, max_width):
    """Wraps the text to fit within the specified width."""
    words = text.split(' ')
    lines = []
    current_line = ""
    
    for word in words:
        test_line = current_line + (word if not current_line else ' ' + word)
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines


def display_rankings(combat_screen, sorted_characters, font, screen_width):
    """Displays character rankings on the screen's top-right corner."""
    score_title = "Score"
    score_surface = font.render(score_title, True, (0, 0, 0))
    combat_screen.blit(score_surface, (screen_width - 55, 20))

    for index, character in enumerate(sorted_characters):
        combat_screen.blit(character["image"], (screen_width - 60, 50 + index * 60))
        score_text = f"{character['score']}"
        score_surface = font.render(score_text, True, (0, 0, 0))
        combat_screen.blit(score_surface, (screen_width - 75, 50 + index * 60))

def display_current_match(combat_screen, character1, character2, combat_text, font, title_font, screen_width, screen_height):
    """Displays the current match information on the screen."""
    battle_title = "Multiverse All-Star Battlefront"
    font = pygame.font.Font(None, 36)
    score_surface = font.render(battle_title, True, (0, 0, 0))
    combat_screen.blit(score_surface, (screen_width//2-175, 20))

    font = pygame.font.Font(None, 30)
    versus_symbol = "V.S."
    versus_surface = font.render(versus_symbol, True, (0, 0, 0))
    combat_screen.blit(versus_surface, (screen_width//2-25, 100))


    # print(f"combat_text: {combat_text}, Type: {type(combat_text)}")
    combat_screen.blit(character1["image"], (screen_width // 4 - 25, screen_height // 4 - 110))
    combat_screen.blit(character2["image"], (screen_width * 3 // 4 - 25, screen_height // 4 - 110))

    char1_text = title_font.render(f"{character1['name']} - Score: {character1['score']}", True, (0, 0, 0))
    char2_text = title_font.render(f"{character2['name']} - Score: {character2['score']}", True, (0, 0, 0))
    combat_screen.blit(char1_text, (screen_width // 4 - char1_text.get_width() // 2, screen_height // 4 - 40))
    combat_screen.blit(char2_text, (screen_width * 3 // 4 - char2_text.get_width() // 2, screen_height // 4 - 40))


    rect_x = screen_width // 2 - 375
    rect_y = screen_height // 2 - 160
    rect_width = 725
    rect_height = 450

    pygame.draw.rect(combat_screen, (240, 240, 240), (rect_x, rect_y, rect_width, rect_height), border_radius=20)

    wrapped_lines = wrap_text(combat_text if combat_text else "Get ready for battle!", font, rect_width - 20)

    total_text_height = sum(font.get_height() for _ in wrapped_lines) + (len(wrapped_lines) - 1) * 5 
    start_y = rect_y + (rect_height - total_text_height) // 2

    for i, line in enumerate(wrapped_lines):
        line_surface = font.render(line, True, (0, 0, 0))
        combat_screen.blit(line_surface, (rect_x + 10, start_y + i * (font.get_height() + 5)))


"""

Combat Logic

"""


def combat(character1, character2):
    c_character1 = load_character_from_dict(character1)
    c_character2 = load_character_from_dict(character2)
    battle = BattleSimulation(c_character1, c_character2)
    combat_process = battle.run_battle()
    winner = battle.winner
    if winner == battle.character1:
        character1["score"]+=1
        return character1, combat_process
    else:
        character2["score"]+=1
        return character2, combat_process


def start_combat(characters):
    pygame.init()
    combat_screen_width, combat_screen_height = 1000, 800
    combat_screen = pygame.display.set_mode((combat_screen_width, combat_screen_height))
    pygame.display.set_caption("Combat Screen")

    font = pygame.font.Font(None, 24)
    title_font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()


    for character in characters:
        character["image"] = pygame.transform.scale(character["image"], (50, 50))


    match_pairs = []
    current_match = 0
    combat_text = ""
    combat_complete = False

    def new_round():
        nonlocal match_pairs, current_match
        shuffled = random.sample(characters, len(characters))
        match_pairs = [(shuffled[i], shuffled[i + 1]) for i in range(0, len(shuffled), 2)]
        current_match = 0

    new_round()

    # Main combat loop
    while True:
        combat_screen.fill((220, 220, 220))

        sorted_characters = sorted(characters, key=lambda c: c["score"], reverse=True)
        display_rankings(combat_screen, sorted_characters, font, combat_screen_width)

        if current_match < len(match_pairs):
            character1, character2 = match_pairs[current_match]
            display_current_match(combat_screen, character1, character2, combat_text, font, title_font, combat_screen_width, combat_screen_height)

            next_button_rect = pygame.Rect(combat_screen_width - 120, combat_screen_height - 60, 100, 40)
            pygame.draw.rect(combat_screen, WHITE, next_button_rect, border_radius=10)
            next_text = font.render("Next", True, BLACK)
            combat_screen.blit(next_text, (combat_screen_width - 120 + 50 - next_text.get_width() // 2, combat_screen_height - 60 + 20 - next_text.get_height() // 2))
            
            if not combat_complete:
                combat_button_rect = pygame.Rect(combat_screen_width - 560, combat_screen_height - 60, 100, 40)
                pygame.draw.rect(combat_screen, WHITE, combat_button_rect, border_radius=10)
                combat_button_text = font.render("Combat", True, BLACK)
                combat_screen.blit((combat_button_text), (combat_screen_width - 560 + 50 - combat_button_text.get_width() // 2, combat_screen_height - 60 + 20 - combat_button_text.get_height() // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if current_match < len(match_pairs) and combat_button_rect.collidepoint(event.pos):
                    winner, combat_process = combat(character1, character2)
                    combat_text = combat_process
                    combat_complete = True

                if current_match < len(match_pairs) and next_button_rect.collidepoint(event.pos):
                    match_pairs[current_match] = (character1, character2)  
                    current_match += 1
                    combat_text = ""
                    combat_complete = False


                    if any(character["score"] >= 10 for character in characters):
                        winner = max(characters, key=lambda c: c["score"])
                        victory_text = title_font.render(f"Winner: {winner['name']}!", True, (0, 0, 0))
                        combat_screen.fill((220, 220, 220))
                        combat_screen.blit(victory_text, (combat_screen_width // 2 - victory_text.get_width() // 2, combat_screen_height // 2))
                        pygame.display.flip()
                        pygame.time.wait(3000)
                        pygame.quit()
                        sys.exit()


                if current_match >= len(match_pairs):
                    new_round()

        pygame.display.flip()
        clock.tick(30)




# Main loop
while True:
    screen.fill((220, 220, 220)) 
    
    mouse_pos = pygame.mouse.get_pos()
    

    for i, character in enumerate(characters):
        x = (i % 4) * (CARD_WIDTH + CARD_SPACING) + 50
        y = (i // 4) * (CARD_HEIGHT + CARD_SPACING) + 50
        

        hover = x < mouse_pos[0] < x + CARD_WIDTH and y < mouse_pos[1] < y + CARD_HEIGHT
        draw_card(character, x, y, hover)

 
    button_width, button_height = 300, 50
    button_rect = pygame.Rect((WIDTH - button_width) // 2, HEIGHT - button_height - 20, button_width, button_height)  # Centered at bottom
    pygame.draw.rect(screen, WHITE, button_rect)
    pygame.draw.rect(screen, BLACK, button_rect, 2)
    start_text = font.render("Start Game", True, BLACK)
    screen.blit(start_text, (button_rect.x + (button_rect.width - start_text.get_width()) // 2,
                              button_rect.y + (button_rect.height - start_text.get_height()) // 2))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and button_rect.collidepoint(event.pos):
            print("Start Game")
            start_combat(characters)
    
    pygame.display.flip()



