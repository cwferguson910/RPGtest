#!/usr/bin/env python3
import pygame
import sys
import random
import math

# ---------------------------
# Pygame Initialization & Constants
# ---------------------------
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fantasy JRPG Battle")
clock = pygame.time.Clock()

# Colors (RGB)
WHITE       = (255, 255, 255)
BLACK       = (0, 0, 0)
RED         = (200, 0, 0)
GREEN       = (0, 200, 0)
BLUE        = (0, 0, 200)
YELLOW      = (255, 255, 0)
PURPLE      = (100, 0, 100)
GRAY        = (50, 50, 50)
ORANGE      = (255, 165, 0)
LIGHT_GREEN = (144, 238, 144)

# UI Layout Constants (we only fix MENU_X and MENU_WIDTH; the menu height will be computed dynamically)
MENU_X = 50
MENU_WIDTH = 700

# Game States
STATE_TURN_START       = 0
STATE_PLAYER_CHOICE    = 1
STATE_TARGET_SELECTION = 2
STATE_ANIMATION        = 3
STATE_NEXT_TURN        = 4
STATE_VICTORY          = 5
STATE_GAME_OVER        = 6

# ---------------------------
# Background Setup – Dramatic Gradient
# ---------------------------
def draw_background(surface):
    """Draw a dramatic vertical gradient background (deep purple to black)."""
    top_color = (30, 0, 30)
    bottom_color = (0, 0, 0)
    for y in range(SCREEN_HEIGHT):
        ratio = y / SCREEN_HEIGHT
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))

background_img = None  # We are not loading an external image now.

# ---------------------------
# Character Classes & Stats
# ---------------------------
class Character:
    def __init__(self, name, hp, attack, defense, magic, speed):
        self.name    = name
        self.max_hp  = hp
        self.hp      = hp
        self.attack  = attack
        self.defense = defense
        self.magic   = magic
        self.speed   = speed
        self.alive   = True
        self.pos     = (0, 0)   # Screen position (top-left)
        self.sprite  = None     # Pygame Surface for the sprite

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.hp = 0
            self.alive = False

    def heal(self, amount):
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp

class Warrior(Character):
    def __init__(self):
        super().__init__("Warrior", 120, 25, 15, 5, 8)

class Mage(Character):
    def __init__(self):
        super().__init__("Mage", 80, 10, 8, 30, 12)

class Healer(Character):
    def __init__(self):
        super().__init__("Healer", 90, 8, 10, 25, 10)

class Thief(Character):
    def __init__(self):
        super().__init__("Thief", 70, 15, 10, 5, 20)

class Boss(Character):
    def __init__(self):
        super().__init__("Final Boss", 300, 30, 20, 20, 15)

def calculate_damage(attacker, target, multiplier=1.0, is_magic=False):
    stat = attacker.magic if is_magic else attacker.attack
    base = stat * multiplier - target.defense
    base = max(1, base)
    return int(base * random.uniform(0.85, 1.15))

# ---------------------------
# Sprite Generation Functions
# ---------------------------
def generate_warrior_sprite(size):
    """Generate a fantasy–anime–styled warrior sprite."""
    surf = pygame.Surface(size, pygame.SRCALPHA)
    surf.fill((120, 120, 120))
    # Draw a sword: a vertical red rectangle with a yellow hilt.
    pygame.draw.rect(surf, RED, (size[0]//2 - 5, size[1]//4, 10, size[1]//2))
    pygame.draw.rect(surf, YELLOW, (size[0]//2 - 8, size[1]//4 + size[1]//2, 16, 5))
    font = pygame.font.SysFont("Arial", 14)
    text = font.render("Warrior", True, WHITE)
    surf.blit(text, (5, 5))
    return surf

def generate_mage_sprite(size):
    """Generate a fantasy–anime–styled mage sprite."""
    surf = pygame.Surface(size, pygame.SRCALPHA)
    surf.fill((50, 50, 100))
    # Draw a mage hat (a triangle) at the top.
    points = [(size[0]//2, 0), (0, size[1]//2), (size[0], size[1]//2)]
    pygame.draw.polygon(surf, BLUE, points)
    # Draw a wand in the bottom-right corner.
    pygame.draw.rect(surf, YELLOW, (size[0]-15, size[1]-30, 5, 20))
    font = pygame.font.SysFont("Arial", 14)
    text = font.render("Mage", True, WHITE)
    surf.blit(text, (5, 5))
    return surf

def generate_healer_sprite(size):
    """Generate a fantasy–anime–styled healer sprite."""
    surf = pygame.Surface(size, pygame.SRCALPHA)
    surf.fill((50, 100, 50))
    # Draw a heart shape using two circles and a triangle.
    r = size[0] // 4
    pygame.draw.circle(surf, GREEN, (size[0]//3, size[1]//3), r)
    pygame.draw.circle(surf, GREEN, (2*size[0]//3, size[1]//3), r)
    points = [(size[0]//6, size[1]//3), (size[0]//2, size[1]), (5*size[0]//6, size[1]//3)]
    pygame.draw.polygon(surf, GREEN, points)
    font = pygame.font.SysFont("Arial", 14)
    text = font.render("Healer", True, WHITE)
    surf.blit(text, (5, 5))
    return surf

def generate_thief_sprite(size):
    """Generate a fantasy–anime–styled thief sprite."""
    surf = pygame.Surface(size, pygame.SRCALPHA)
    surf.fill((80, 80, 80))
    # Draw a masked face: a black ellipse with two white eyes.
    pygame.draw.ellipse(surf, BLACK, (size[0]//4, size[1]//4, size[0]//2, size[1]//2))
    pygame.draw.circle(surf, WHITE, (size[0]//3, size[1]//2), 5)
    pygame.draw.circle(surf, WHITE, (2*size[0]//3, size[1]//2), 5)
    font = pygame.font.SysFont("Arial", 14)
    text = font.render("Thief", True, WHITE)
    surf.blit(text, (5, 5))
    return surf

def generate_boss_sprite(size):
    """Generate a fantasy–anime–styled boss sprite."""
    surf = pygame.Surface(size, pygame.SRCALPHA)
    surf.fill((100, 0, 100))
    # Draw a menacing face: a large circle with red eyes.
    pygame.draw.circle(surf, PURPLE, (size[0]//2, size[1]//2), size[0]//2)
    pygame.draw.circle(surf, RED, (size[0]//3, size[1]//3), 10)
    pygame.draw.circle(surf, RED, (2*size[0]//3, size[1]//3), 10)
    font = pygame.font.SysFont("Arial", 18)
    text = font.render("Boss", True, WHITE)
    surf.blit(text, (size[0]//4, 5))
    return surf

# ---------------------------
# Moves Data & Action Class
# ---------------------------
moves_data = {
    "Warrior": [
        {"name": "Strike",       "type": "physical", "multiplier": 1.0, "hit_chance": 1.0},
        {"name": "Heavy Slash",  "type": "physical", "multiplier": 1.5, "hit_chance": 0.75}
    ],
    "Mage": [
        {"name": "Magic Missile", "type": "magical",  "multiplier": 1.0, "hit_chance": 1.0},
        {"name": "Fireball",      "type": "magical",  "multiplier": 1.5, "hit_chance": 1.0}
    ],
    "Healer": [
        {"name": "Attack",        "type": "physical", "multiplier": 1.0, "hit_chance": 1.0},
        {"name": "Heal",          "type": "heal",     "multiplier": 1.5, "hit_chance": 1.0}
    ],
    "Thief": [
        {"name": "Quick Strike",  "type": "physical", "multiplier": 1.0, "hit_chance": 1.0},
        {"name": "Backstab",      "type": "physical", "multiplier": 2.0, "hit_chance": 0.60}
    ]
}

class Action:
    def __init__(self, attacker, target, move_name, damage, move_type, is_heal=False, hit=True):
        self.attacker  = attacker
        self.target    = target
        self.move_name = move_name
        self.damage    = damage
        self.move_type = move_type   # "physical", "magical", or "heal"
        self.is_heal   = is_heal
        self.hit       = hit

# ---------------------------
# Animation Classes – Bespoke for Each Action
# ---------------------------
class BaseAnimation:
    def __init__(self, attacker, target, duration):
        self.attacker = attacker
        self.target   = target
        self.duration = duration  # in milliseconds
        self.start_time = pygame.time.get_ticks()
        self.finished = False
        self.progress = 0

    def update(self, current_time):
        self.progress = (current_time - self.start_time) / self.duration
        if self.progress >= 1:
            self.progress = 1
            self.finished = True

    def draw(self, screen):
        pass

# --- Warrior Animations ---
class WarriorStrikeAnimation(BaseAnimation):
    def __init__(self, attacker, target):
        super().__init__(attacker, target, 600)
        self.start_pos = self.get_center(attacker)
        self.end_pos   = self.get_center(target)

    def get_center(self, char):
        if char.sprite:
            return (char.pos[0] + char.sprite.get_width()//2,
                    char.pos[1] + char.sprite.get_height()//2)
        else:
            return (char.pos[0] + 40, char.pos[1] + 40)

    def draw(self, screen):
        x = self.start_pos[0] + (self.end_pos[0] - self.start_pos[0]) * self.progress
        y = self.start_pos[1] + (self.end_pos[1] - self.start_pos[1]) * self.progress
        thickness = max(1, int(8 * (1 - self.progress)))
        pygame.draw.line(screen, RED, self.start_pos, (x, y), thickness)

class WarriorHeavySlashAnimation(BaseAnimation):
    def __init__(self, attacker, target):
        super().__init__(attacker, target, 800)
        self.start_pos = WarriorStrikeAnimation(attacker, target).get_center(attacker)
        self.end_pos   = WarriorStrikeAnimation(attacker, target).get_center(target)

    def draw(self, screen):
        progress = self.progress
        thickness = max(1, int(12 * (1 - progress)))
        x = self.start_pos[0] + (self.end_pos[0] - self.start_pos[0]) * progress
        y = self.start_pos[1] + (self.end_pos[1] - self.start_pos[1]) * progress
        pygame.draw.line(screen, RED, self.start_pos, (x, y), thickness)
        if 0.4 < progress < 0.6:
            flash_pos = ((self.start_pos[0] + self.end_pos[0]) // 2,
                         (self.start_pos[1] + self.end_pos[1]) // 2)
            pygame.draw.circle(screen, WHITE, flash_pos, 20)

# --- Mage Animations ---
class MageMagicMissileAnimation(BaseAnimation):
    def __init__(self, attacker, target):
        super().__init__(attacker, target, 500)
        self.start_pos = self.get_center(attacker)
        self.end_pos   = self.get_center(target)

    def get_center(self, char):
        if char.sprite:
            return (char.pos[0] + char.sprite.get_width()//2,
                    char.pos[1] + char.sprite.get_height()//2)
        else:
            return (char.pos[0] + 40, char.pos[1] + 40)

    def draw(self, screen):
        x = self.start_pos[0] + (self.end_pos[0] - self.start_pos[0]) * self.progress
        y = self.start_pos[1] + (self.end_pos[1] - self.start_pos[1]) * self.progress
        pygame.draw.circle(screen, BLUE, (int(x), int(y)), 8)

class MageFireballAnimation(BaseAnimation):
    def __init__(self, attacker, target):
        super().__init__(attacker, target, 700)
        self.start_pos = MageMagicMissileAnimation(attacker, target).get_center(attacker)
        self.end_pos   = MageMagicMissileAnimation(attacker, target).get_center(target)

    def draw(self, screen):
        x = self.start_pos[0] + (self.end_pos[0] - self.start_pos[0]) * self.progress
        y = self.start_pos[1] + (self.end_pos[1] - self.start_pos[1]) * self.progress
        radius = int(10 + 10 * (1 - abs(0.5 - self.progress) * 2))
        pygame.draw.circle(screen, ORANGE, (int(x), int(y)), radius)

# --- Healer Animations ---
class HealerAttackAnimation(BaseAnimation):
    def __init__(self, attacker, target):
        super().__init__(attacker, target, 500)
        self.start_pos = MageMagicMissileAnimation(attacker, target).get_center(attacker)
        self.end_pos   = MageMagicMissileAnimation(attacker, target).get_center(target)

    def draw(self, screen):
        x = self.start_pos[0] + (self.end_pos[0] - self.start_pos[0]) * self.progress
        y = self.start_pos[1] + (self.end_pos[1] - self.start_pos[1]) * self.progress
        thickness = max(1, int(6 * (1 - self.progress)))
        pygame.draw.line(screen, LIGHT_GREEN, self.start_pos, (x, y), thickness)

class HealerHealAnimation(BaseAnimation):
    def __init__(self, target):
        super().__init__(None, target, 800)
        if target.sprite:
            self.center = (target.pos[0] + target.sprite.get_width()//2,
                           target.pos[1] + target.sprite.get_height()//2)
        else:
            self.center = (target.pos[0] + 40, target.pos[1] + 40)

    def draw(self, screen):
        radius = int(20 + 30 * self.progress)
        alpha = int(255 * (1 - self.progress))
        aura_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(aura_surface, (0, 255, 0, alpha), (radius, radius), radius, 3)
        screen.blit(aura_surface, (self.center[0] - radius, self.center[1] - radius))

# --- Thief Animations ---
class ThiefQuickStrikeAnimation(BaseAnimation):
    def __init__(self, attacker, target):
        super().__init__(attacker, target, 400)
        self.start_pos = MageMagicMissileAnimation(attacker, target).get_center(attacker)
        self.end_pos   = MageMagicMissileAnimation(attacker, target).get_center(target)

    def draw(self, screen):
        x = self.start_pos[0] + (self.end_pos[0] - self.start_pos[0]) * self.progress
        y = self.start_pos[1] + (self.end_pos[1] - self.start_pos[1]) * self.progress
        thickness = max(1, int(4 * (1 - self.progress)))
        pygame.draw.line(screen, YELLOW, self.start_pos, (x, y), thickness)

class ThiefBackstabAnimation(BaseAnimation):
    def __init__(self, attacker, target):
        super().__init__(attacker, target, 600)
        if target.sprite:
            self.center = (target.pos[0] + target.sprite.get_width()//2,
                           target.pos[1] + target.sprite.get_height()//2)
        else:
            self.center = (target.pos[0] + 40, target.pos[1] + 40)

    def draw(self, screen):
        radius = int(10 + 30 * self.progress)
        alpha = int(255 * (1 - self.progress))
        flash_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(flash_surface, (0, 0, 0, alpha), (radius, radius), radius)
        screen.blit(flash_surface, (self.center[0] - radius, self.center[1] - radius))

# --- Boss Animations ---
class BossSmashAnimation(BaseAnimation):
    def __init__(self, attacker, target):
        super().__init__(attacker, target, 800)
        if target.sprite:
            self.center = (target.pos[0] + target.sprite.get_width()//2,
                           target.pos[1] + target.sprite.get_height()//2)
        else:
            self.center = (target.pos[0] + 40, target.pos[1] + 40)

    def draw(self, screen):
        radius = int(20 + 50 * self.progress)
        alpha = int(255 * (1 - self.progress))
        shock_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(shock_surface, (255, 0, 0, alpha), (radius, radius), radius, 3)
        screen.blit(shock_surface, (self.center[0] - radius, self.center[1] - radius))

class BossDarkBlastAnimation(BaseAnimation):
    def __init__(self, attacker, target):
        super().__init__(attacker, target, 700)
        self.start_pos = MageMagicMissileAnimation(attacker, target).get_center(attacker)
        self.end_pos   = MageMagicMissileAnimation(attacker, target).get_center(target)

    def draw(self, screen):
        x = self.start_pos[0] + (self.end_pos[0] - self.start_pos[0]) * self.progress
        y = self.start_pos[1] + (self.end_pos[1] - self.start_pos[1]) * self.progress
        radius = 10
        angle = self.progress * math.pi * 4
        offset_x = int(15 * math.cos(angle))
        offset_y = int(15 * math.sin(angle))
        pygame.draw.circle(screen, (75, 0, 130), (int(x + offset_x), int(y + offset_y)), radius)

def create_animation(action):
    if action.attacker.name == "Warrior":
        if action.move_name == "Strike":
            return WarriorStrikeAnimation(action.attacker, action.target)
        elif action.move_name == "Heavy Slash":
            return WarriorHeavySlashAnimation(action.attacker, action.target)
    elif action.attacker.name == "Mage":
        if action.move_name == "Magic Missile":
            return MageMagicMissileAnimation(action.attacker, action.target)
        elif action.move_name == "Fireball":
            return MageFireballAnimation(action.attacker, action.target)
    elif action.attacker.name == "Healer":
        if action.move_name == "Attack":
            return HealerAttackAnimation(action.attacker, action.target)
        elif action.move_name == "Heal":
            return HealerHealAnimation(action.target)
    elif action.attacker.name == "Thief":
        if action.move_name == "Quick Strike":
            return ThiefQuickStrikeAnimation(action.attacker, action.target)
        elif action.move_name == "Backstab":
            return ThiefBackstabAnimation(action.attacker, action.target)
    elif action.attacker.name == "Final Boss":
        if action.move_name == "Smash":
            return BossSmashAnimation(action.attacker, action.target)
        elif action.move_name == "Dark Blast":
            return BossDarkBlastAnimation(action.attacker, action.target)
    return BaseAnimation(action.attacker, action.target, 500)

# ---------------------------
# Utility Functions for UI & Art
# ---------------------------
def assign_positions(party, boss):
    x = 50
    start_y = 100
    gap = 100
    for i, member in enumerate(party):
        member.pos = (x, start_y + i * gap)
    boss.pos = (600, 250)

def draw_characters(screen, party, boss):
    for member in party:
        if member.sprite:
            screen.blit(member.sprite, member.pos)
        else:
            pygame.draw.rect(screen, WHITE, (*member.pos, 80, 80))
    if boss.sprite:
        screen.blit(boss.sprite, boss.pos)
    else:
        pygame.draw.rect(screen, WHITE, (*boss.pos, 120, 120))

def draw_health(screen, character):
    sprite_width = character.sprite.get_width() if character.sprite else 80
    bar_width = sprite_width
    bar_height = 10
    x, y = character.pos
    pygame.draw.rect(screen, RED, (x, y - 15, bar_width, bar_height))
    ratio = character.hp / character.max_hp if character.max_hp > 0 else 0
    pygame.draw.rect(screen, GREEN, (x, y - 15, int(bar_width * ratio), bar_height))

def draw_turn_order(screen, turn_queue):
    font = pygame.font.SysFont("Arial", 20)
    order_names = " -> ".join([actor.name for actor in turn_queue if actor.alive])
    label = font.render("Turn Order: " + order_names, True, WHITE)
    screen.blit(label, (50, 20))

def draw_menu(screen, options, selected_index, prompt="Choose an action:"):
    # Compute dynamic height: 
    n_log = min(3, len(action_log))
    log_height = n_log * 18 + 10  # top padding + log lines
    prompt_height = 30
    options_height = len(options) * 30
    menu_height = log_height + 10 + prompt_height + options_height + 10
    menu_y = SCREEN_HEIGHT - menu_height
    pygame.draw.rect(screen, GRAY, (MENU_X, menu_y, MENU_WIDTH, menu_height))
    pygame.draw.rect(screen, WHITE, (MENU_X, menu_y, MENU_WIDTH, menu_height), 2)
    log_font = pygame.font.SysFont("Arial", 16)
    for i, log_entry in enumerate(action_log[-n_log:]):
        label = log_font.render(log_entry, True, WHITE)
        screen.blit(label, (MENU_X + 10, menu_y + 10 + i * 18))
    prompt_y = menu_y + log_height + 10
    font = pygame.font.SysFont("Arial", 20)
    prompt_label = font.render(prompt, True, WHITE)
    screen.blit(prompt_label, (MENU_X + 10, prompt_y))
    for i, option in enumerate(options):
        option_y = prompt_y + prompt_height + i * 30
        color = YELLOW if i == selected_index else WHITE
        option_label = font.render(f"{i+1}. {option}", True, color)
        screen.blit(option_label, (MENU_X + 10, option_y))

def recalc_turn_queue(party, boss):
    actors = []
    if boss.alive:
        actors.append(boss)
    actors.extend([member for member in party if member.alive])
    actors.sort(key=lambda c: c.speed, reverse=True)
    return actors

# ---------------------------
# Global Variables
# ---------------------------
game_state         = STATE_TURN_START
turn_queue         = []
turn_index         = 0
current_actor      = None
current_animation  = None
pending_action     = None
selected_menu_index= 0
current_menu_options  = []  # For the action selection menu
current_prompt         = ""
action_log = []  # Global gamelog (list of strings)

def add_log_entry(text):
    """Append an entry to the gamelog (keep up to 5 entries)."""
    action_log.append(text)
    if len(action_log) > 5:
        del action_log[0]

# ---------------------------
# Main Game Loop
# ---------------------------
def main():
    global game_state, turn_queue, turn_index, current_actor
    global current_animation, pending_action, selected_menu_index
    global current_menu_options, current_prompt

    # Create characters.
    party = [Warrior(), Mage(), Healer(), Thief()]
    boss = Boss()

    # Generate sprites.
    party[0].sprite = generate_warrior_sprite((80, 80))
    party[1].sprite = generate_mage_sprite((80, 80))
    party[2].sprite = generate_healer_sprite((80, 80))
    party[3].sprite = generate_thief_sprite((80, 80))
    boss.sprite     = generate_boss_sprite((120, 120))

    assign_positions(party, boss)
    turn_queue = recalc_turn_queue(party, boss)
    turn_index = 0
    current_actor = turn_queue[turn_index] if turn_queue else None
    game_state = STATE_TURN_START

    running = True
    while running:
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            # Handle input for action selection.
            if game_state in [STATE_PLAYER_CHOICE, STATE_TARGET_SELECTION]:
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_1, pygame.K_KP1]:
                        selected_menu_index = 0
                        event.key = pygame.K_RETURN
                    elif event.key in [pygame.K_2, pygame.K_KP2]:
                        selected_menu_index = 1
                        event.key = pygame.K_RETURN
                    elif event.key in [pygame.K_3, pygame.K_KP3]:
                        selected_menu_index = 2
                        event.key = pygame.K_RETURN
                    elif event.key in [pygame.K_4, pygame.K_KP4]:
                        selected_menu_index = 3
                        event.key = pygame.K_RETURN

                    if event.key == pygame.K_UP:
                        selected_menu_index = (selected_menu_index - 1) % len(current_menu_options)
                    elif event.key == pygame.K_DOWN:
                        selected_menu_index = (selected_menu_index + 1) % len(current_menu_options)
                    elif event.key == pygame.K_RETURN:
                        if game_state == STATE_PLAYER_CHOICE:
                            move = moves_data[current_actor.name][selected_menu_index]
                            if move["type"] == "heal":
                                alive_party = [member for member in party if member.alive]
                                current_menu_options = [f"{member.name} ({member.hp}/{member.max_hp})" for member in alive_party]
                                if not current_menu_options:
                                    current_menu_options = [f"{current_actor.name}"]
                                selected_menu_index = 0
                                current_prompt = "Select target to heal:"
                                pending_action = {"move": move}
                                game_state = STATE_TARGET_SELECTION
                            else:
                                hit = random.random() <= move["hit_chance"]
                                dmg = calculate_damage(current_actor, boss, move["multiplier"], is_magic=(move["type"]=="magical"))
                                pending_action = Action(current_actor, boss, move["name"], dmg, move["type"], is_heal=False, hit=hit)
                                current_animation = create_animation(pending_action)
                                game_state = STATE_ANIMATION
                        elif game_state == STATE_TARGET_SELECTION:
                            alive_party = [member for member in party if member.alive]
                            target = alive_party[selected_menu_index] if alive_party else current_actor
                            move = pending_action["move"]
                            dmg = int(current_actor.magic * move["multiplier"] * random.uniform(0.85, 1.15))
                            pending_action = Action(current_actor, target, move["name"], dmg, "heal", is_heal=True)
                            current_animation = create_animation(pending_action)
                            game_state = STATE_ANIMATION

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    # Determine dynamic menu_y and menu_height inside draw_menu.
                    # For simplicity, re-calculate here the same way:
                    n_log = min(3, len(action_log))
                    log_height = n_log * 18 + 10
                    prompt_height = 30
                    options_height = len(current_menu_options) * 30
                    menu_height = log_height + 10 + prompt_height + options_height + 10
                    menu_y = SCREEN_HEIGHT - menu_height
                    if MENU_X <= mx <= MENU_X + MENU_WIDTH and menu_y <= my <= menu_y + menu_height:
                        option_index = (my - (menu_y + log_height + 10 + prompt_height)) // 30
                        if 0 <= option_index < len(current_menu_options):
                            selected_menu_index = option_index
                            fake_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
                            pygame.event.post(fake_event)

            elif game_state in [STATE_VICTORY, STATE_GAME_OVER]:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    main()  # Restart
                    return

        # Update animation.
        if game_state == STATE_ANIMATION and current_animation:
            current_animation.update(current_time)
            if current_animation.finished:
                if pending_action.hit:
                    if pending_action.is_heal:
                        pending_action.target.heal(pending_action.damage)
                    else:
                        pending_action.target.take_damage(pending_action.damage)
                if pending_action.hit:
                    if pending_action.is_heal:
                        add_log_entry(f"{pending_action.attacker.name} uses {pending_action.move_name} on {pending_action.target.name}, healing {pending_action.damage} HP!")
                    else:
                        add_log_entry(f"{pending_action.attacker.name} uses {pending_action.move_name} on {pending_action.target.name}, dealing {pending_action.damage} damage!")
                else:
                    add_log_entry(f"{pending_action.attacker.name} used {pending_action.move_name} on {pending_action.target.name} but missed!")
                current_animation = None
                pending_action = None
                game_state = STATE_NEXT_TURN

        # State transitions.
        if game_state == STATE_TURN_START:
            if not boss.alive:
                game_state = STATE_VICTORY
            elif not any(member.alive for member in party):
                game_state = STATE_GAME_OVER
            else:
                turn_queue = recalc_turn_queue(party, boss)
                if turn_index >= len(turn_queue):
                    turn_index = 0
                current_actor = turn_queue[turn_index]
                if current_actor in party:
                    current_menu_options = [move["name"] for move in moves_data[current_actor.name]]
                    selected_menu_index = 0
                    current_prompt = f"{current_actor.name}'s turn: Choose an action:"
                    game_state = STATE_PLAYER_CHOICE
                else:
                    boss_move = random.choice([
                        {"name": "Smash",      "type": "physical", "multiplier": 1.2, "hit_chance": 1.0},
                        {"name": "Dark Blast", "type": "magical",  "multiplier": 1.2, "hit_chance": 1.0}
                    ])
                    hit = random.random() <= boss_move["hit_chance"]
                    target = random.choice([member for member in party if member.alive])
                    dmg = calculate_damage(boss, target, boss_move["multiplier"], is_magic=(boss_move["type"]=="magical"))
                    pending_action = Action(boss, target, boss_move["name"], dmg, boss_move["type"], is_heal=False, hit=hit)
                    current_animation = create_animation(pending_action)
                    game_state = STATE_ANIMATION

        if game_state == STATE_NEXT_TURN:
            turn_index += 1
            game_state = STATE_TURN_START

        # Drawing.
        if background_img:
            screen.blit(background_img, (0, 0))
        else:
            draw_background(screen)

        draw_characters(screen, party, boss)
        for member in party:
            draw_health(screen, member)
        draw_health(screen, boss)
        turn_queue = recalc_turn_queue(party, boss)
        draw_turn_order(screen, turn_queue)

        if game_state == STATE_ANIMATION and current_animation:
            current_animation.draw(screen)

        if game_state in [STATE_PLAYER_CHOICE, STATE_TARGET_SELECTION]:
            draw_menu(screen, current_menu_options, selected_menu_index, prompt=current_prompt)

        font = pygame.font.SysFont("Arial", 40)
        if game_state == STATE_VICTORY:
            msg = font.render("Victory! Press Enter to play again.", True, WHITE)
            screen.blit(msg, (SCREEN_WIDTH//2 - msg.get_width()//2, SCREEN_HEIGHT//2))
        elif game_state == STATE_GAME_OVER:
            msg = font.render("Game Over! Press Enter to try again.", True, WHITE)
            screen.blit(msg, (SCREEN_WIDTH//2 - msg.get_width()//2, SCREEN_HEIGHT//2))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
