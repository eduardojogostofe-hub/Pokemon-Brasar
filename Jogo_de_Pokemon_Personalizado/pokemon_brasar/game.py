import pygame
import random
import sys

from .battle_rules import calculate_damage as calculate_battle_damage

pygame.init()

# ============================================================
# POKÉMON BRASAR - V10
# Estilo clássico 2D / Game Boy Color
# ============================================================

WIDTH, HEIGHT = 768, 576
TILE = 48
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pokémon Brasar - V7")
clock = pygame.time.Clock()

FONT = pygame.font.Font(None, 28)
SMALL = pygame.font.Font(None, 22)
BIG = pygame.font.Font(None, 40)

# Cores
BLACK = (20, 20, 20)
WHITE = (250, 250, 245)
GREEN = (75, 175, 85)
DARK_GREEN = (35, 105, 50)
LIGHT_GREEN = (145, 205, 110)
WATER = (75, 155, 220)
PATH = (205, 175, 115)
BROWN = (130, 85, 45)
RED = (210, 70, 70)
BLUE = (65, 115, 210)
YELLOW = (240, 205, 55)
ORANGE = (235, 125, 45)
PURPLE = (145, 80, 175)
GRAY = (145, 145, 145)
DARK_GRAY = (65, 65, 65)
PANEL = (238, 238, 225)

# ============================================================
# DADOS
# ============================================================

EVOLUTIONS = {
    "Macarim": ("Macacique", 16), "Macacique": ("Guarilla", 36),
    "Flaguar": ("Flatirica", 16), "Flatirica": ("Jaguarze", 36),
    "Suriqua": ("Snariver", 16), "Snariver": ("Tsuconda", 36),
    "Grubey": ("Julifly", 8), "Julifly": ("Murizika", 20),
    "Perigreen": ("Canindarara", 14), "Canindarara": ("Alarala", 32),
    "Chloralga": ("Victeed", 20), "Brigarock": ("Briganite", 20),
    "Toxua": ("Tamantox", 32), "Phantag": ("Ghoil", 25),
    "Wooloo de Brasar": ("Dubwool de Brasar", 25), "Bellcaf": ("Bumboi", 30),
    "Chicktric": ("Rayken", 25), "Cherubi de Brasar": ("Pepperim", 25),
    "Feipig": ("Feijoar", 30), "Floatee": ("Sirenatee", 30),
    "Roseph": ("Dolphink", 30), "Aquack": ("Garsea", 22), "Garsea": ("Jabuyu", 30),
    "Pipat": ("Dellbat", 30), "Muihrite": ("Jaduitan", 30),
    "Mandimole": ("Braipim", 20), "Yamask de Brasar": ("Carrangrigus", 34),
    "Melopole": ("Melotoad", 25), "Melotoad": ("Froton", 36),
    "Canarin": ("Canangry", 25), "Fuleball": ("Armordillo", 30),
    "Vanillite de Brasar": ("Vanillish de Brasar", 30), "Vanillish de Brasar": ("Acairock", 47),
    "Fruttiny": ("Frutitti", 20), "Frutitti": ("Tropicanda", 30),
    "Scytiny": ("Scizor", 30), "Sambunny": ("Wheaster", 25),
    "Allicuca": ("Dracuca", 45), "Dracuca": ("Kuckagron", 65),
    "Howlf": ("Wolfscure", 30), "Godofear": ("Maugh", 20),
    "Lamblet": ("Corneiro", 25),
}

POKEMON = {}

def _species(name, type_name, hp=55, atk=55, defense=50, speed=50, moves=None, sp_attack=None, sp_defense=None):
    POKEMON[name] = {
        "type": type_name,
        "base_hp": hp, "attack": atk, "defense": defense, "speed": speed,
        "sp_attack": atk if sp_attack is None else sp_attack,
        "sp_defense": defense if sp_defense is None else sp_defense,
        "moves": moves or ["Investida"]
    }

# Dados já trabalhados no protótipo
_species("Macarim", "Grama", 39, 12, 11, 12, ["Folhagem", "Investida"])
_species("Macacique", "Grama", 48, 17, 14, 15, ["Folhagem", "Investida"])
_species("Guarilla", "Grama/Lutador", 65, 25, 20, 19, ["Folhagem", "Golpe Marcial", "Investida"])
_species("Flaguar", "Fogo", 38, 13, 9, 13, ["Brasa", "Investida"])
_species("Flatirica", "Fogo", 47, 18, 12, 17, ["Brasa", "Investida"])
_species("Jaguarze", "Fogo/Sombrio", 64, 27, 19, 22, ["Brasa", "Mordida Sombria", "Investida"])
_species("Suriqua", "Água", 40, 11, 12, 11, ["Jato d'Água", "Investida"])
_species("Snariver", "Água", 49, 17, 15, 15, ["Jato d'Água", "Investida"])
_species("Tsuconda", "Água/Dragão", 68, 26, 21, 18, ["Jato d'Água", "Garra Dragão", "Investida"])
_species("Grubey", "Inseto", 28, 9, 8, 10, ["Investida", "Picada"])
_species("Julifly", "Inseto/Voador", 34, 12, 10, 17, ["Picada", "Asa de Vento"])
_species("Murizika", "Inseto/Venenoso", 43, 15, 13, 15, ["Picada", "Toxina"])
_species("Perigreen", "Normal/Voador", 31, 11, 9, 16, ["Investida", "Asa de Vento"])
_species("Canindarara", "Normal/Voador", 48, 18, 14, 20, ["Asa de Vento", "Investida"])
_species("Alarala", "Normal/Voador", 72, 25, 20, 28, ["Asa de Vento", "Investida"])
_species("Canarin", "Elétrico/Voador", 30, 11, 8, 15, ["Choque", "Asa de Vento"])
_species("Canangry", "Elétrico/Lutador", 62, 27, 18, 24, ["Choque", "Golpe Marcial"])
_species("Guaramite", "Grama/Psíquico", 32, 10, 9, 9, ["Folhagem", "Confusão"])
_species("Guaraviton", "Grama/Psíquico", 70, 20, 20, 18, ["Folhagem", "Confusão"])
_species("Brigarock", "Pedra/Fada", 42, 16, 18, 9, ["Pedrada", "Vento Fada"])
_species("Briganite", "Pedra/Fada", 60, 22, 25, 12, ["Pedrada", "Vento Fada"])
_species("Chloralga", "Grama/Água", 34, 10, 11, 9, ["Folhagem", "Jato d'Água"])
_species("Victeed", "Grama/Água", 48, 16, 16, 11, ["Folhagem", "Jato d'Água", "Dreno Vital"])
_species("Toxua", "Veneno", 65, 50, 45, 65, ["Toxina", "Lodo"])
_species("Tamantox", "Veneno", 90, 70, 60, 70, ["Toxina", "Lodo", "Investida"])
_species("Melopole", "Água/Veneno", 50, 50, 40, 64, ["Jato d'Água", "Toxina"])
_species("Melotoad", "Água/Veneno", 75, 65, 55, 70, ["Jato d'Água", "Lodo", "Toxina"])
_species("Froton", "Veneno/Psíquico", 90, 75, 65, 78, ["Lodo", "Confusão"])
_species("Choralga", "Grama/Água", 34, 10, 11, 9, ["Folhagem", "Jato d'Água"])

# Espécies usadas nos ginásios, cidades e fim de jogo do material
species_data = {
    "Vulpix de Brasar":("Grama",60,25,25,25,["Folhagem"]), "Ninetales de Brasar":("Grama",95,70,65,70,["Folhagem","Dreno Vital"]),
    "Smoochum":("Gelo/Psíquico",45,35,35,65,["Confusão","Raio de Gelo"]), "Varlien":("Psíquico/Fada",75,55,55,75,["Confusão","Vento Fada"]),
    "Loudred":("Normal",78,65,50,45,["Investida","Voz Ecoante"]), "Eeveeon":("Normal",90,70,55,90,["Investida","Ataque Rápido"]), "Miltank":("Normal",85,75,70,65,["Investida","Golpe Corporal"]),
    "Caxinguelice":("Normal/Gelo",70,55,50,80,["Mordida","Raio de Gelo"]), "Froslass":("Gelo/Fantasma",75,60,55,95,["Raio de Gelo","Bola Sombria"]), "Guarartic":("Gelo",95,75,80,60,["Raio de Gelo","Mordida"]),
    "Roserade":("Grama/Veneno",75,70,60,90,["Folhagem","Lodo"]), "Tamandox":("Veneno",80,75,65,70,["Toxina","Lodo"]), "Toxtricity":("Elétrico/Veneno",80,75,65,75,["Choque","Lodo"]),
    "Pepperim":("Grama/Fogo",70,60,55,65,["Brasa","Folhagem"]), "Magmar":("Fogo",75,75,55,70,["Brasa","Investida"]), "Houndoom":("Sombrio/Fogo",85,80,55,95,["Brasa","Mordida Sombria"]), "Salazzle":("Veneno/Fogo",68,60,55,117,["Brasa","Toxina"]),
    "Carbink":("Pedra/Fada",55,40,100,35,["Pedrada","Vento Fada"]), "Rockeon":("Pedra",95,80,105,60,["Pedrada","Gema de Poder"]), "Muihrite":("Pedra/Psíquico",60,55,60,40,["Gema de Poder","Confusão"]), "Jaduitan":("Pedra/Psíquico",90,55,120,40,["Gema de Poder","Confusão"]),
    "Mismagius":("Fantasma",70,60,60,105,["Bola Sombria","Confusão"]), "Carrangrigus":("Fantasma/Sombrio",90,75,105,30,["Bola Sombria","Mordida Sombria"]), "Bumboi":("Fantasma/Fada",90,80,75,65,["Bola Sombria","Vento Fada"]),
    "Gigarucu":("Água",100,85,75,60,["Jato d'Água","Hidro Bomba"]), "Vaporeon":("Água",110,65,65,65,["Jato d'Água","Hidro Bomba"]), "Azumarill":("Água/Fada",100,80,80,50,["Jato d'Água","Vento Fada"]), "Sirenatee":("Água",130,85,65,60,["Hidro Bomba","Golpe Corporal"]), "Wailord":("Água",120,90,50,60,["Hidro Bomba","Golpe Corporal"]),
    "Bastiodon":("Pedra/Aço",75,55,130,30,["Pedrada","Cabeçada"]), "Dubwool de Brasar":("Aço",100,80,100,55,["Investida","Cabeçada"]), "Skarmory":("Aço/Voador",65,80,110,70,["Asa de Vento","Cabeçada"]), "Cabrooat":("Aço/Sombrio",90,85,95,65,["Cabeçada","Mordida Sombria"]), "Cacturne de Brasar":("Grama/Aço",90,95,75,55,["Folhagem","Cabeçada"]), "Metagross":("Aço/Psíquico",90,110,110,70,["Cabeçada","Confusão"]),
    "Fatuatah":("Fogo/Fantasma",100,90,85,95,["Brasa","Bola Sombria"]), "Nymphiara":("Água/Fada",100,80,80,90,["Jato d'Água","Vento Fada"]), "Caiflora":("Grama/Sombrio",105,95,85,105,["Folhagem","Mordida Sombria"]),
    "Chaballos":("Aço/Sombrio",120,120,110,65,["Cabeçada","Mordida Sombria"]), "Orpyja":("Voador/Psíquico",110,90,90,120,["Asa de Vento","Confusão"]), "Sarereh":("Sombrio/Fada",80,75,65,115,["Mordida Sombria","Vento Fada"]), "Kuckagron":("Dragão/Sombrio",125,120,100,90,["Garra Dragão","Mordida Sombria"]),
    "Iron Bubble":("Água",90,80,70,130,["Jato d'Água"]), "Iron Television":("Elétrico/Psíquico",95,85,80,105,["Choque","Confusão"]), "Old Bundle":("Sombrio",100,95,75,90,["Mordida Sombria","Investida"]),
    "Mr. Momo":("Psíquico/Fada",80,60,65,85,["Confusão","Vento Fada"]), "Phanteon":("Fantasma",90,75,70,100,["Bola Sombria"]), "Earthdog":("Normal/Terra",75,70,65,60,["Investida","Terremoto"]), "Mandimole":("Terra",60,85,40,68,["Terremoto","Mordida"]), "Braipim":("Terra/Veneno",95,90,85,75,["Terremoto","Lodo"]),
    "Scytiny":("Inseto",45,55,45,70,["Picada"]), "Scizor":("Inseto/Aço",70,100,100,65,["Picada","Cabeçada"]), "Mimikyu de Brasar":("Fantasma/Fada",55,90,80,96,["Bola Sombria","Vento Fada"]),
    "Maugh":("Sombrio/Veneno",104,91,63,68,["Lodo","Mordida Sombria"]), "Godofear":("Normal/Sombrio",70,60,55,65,["Mordida Sombria"]), "Falinks de Brasar":("Lutador/Terra",65,100,85,90,["Golpe Marcial","Terremoto"]),
    "Wooloo de Brasar":("Aço",55,55,65,35,["Investida"]), "Bellcaf":("Normal",50,50,45,40,["Investida"]), "Chicktric":("Elétrico",55,50,40,70,["Choque"]), "Rayken":("Elétrico",80,85,65,85,["Choque"]), "Thuncken":("Elétrico/Lutador",90,100,75,85,["Choque","Golpe Marcial"]),
    "Cherubi de Brasar":("Grama/Fogo",45,53,45,35,["Brasa","Folhagem"]), "Feipig":("Terra",50,50,40,50,["Terremoto"]), "Feijoar":("Terra/Pedra",85,80,75,55,["Terremoto","Pedrada"]), "Floatee":("Água",65,45,65,45,["Jato d'Água"]),
    "Roseph":("Fada/Água",70,65,65,70,["Jato d'Água","Vento Fada"]), "Dolphink":("Fada/Água",90,80,75,85,["Jato d'Água","Vento Fada"]), "Aquack":("Voador/Água",55,50,45,80,["Asa de Vento","Jato d'Água"]), "Garsea":("Voador/Água",75,70,60,85,["Asa de Vento","Jato d'Água"]), "Jabuyu":("Voador/Água",95,90,80,80,["Asa de Vento","Jato d'Água"]),
    "Laquid":("Água",100,70,80,55,["Jato d'Água"]), "Mousoap":("Fada/Água",55,45,55,80,["Jato d'Água","Vento Fada"]), "Piratfish":("Água",70,70,60,50,["Jato d'Água"]), "Gigarucu":("Água",100,85,75,60,["Jato d'Água","Hidro Bomba"]),
    "Aromatisse":("Fada",100,70,70,40,["Vento Fada"]), "Sylveon":("Fada",95,65,65,60,["Vento Fada"]), "Florges":("Fada",90,70,65,75,["Vento Fada"]), "Hatterene":("Psíquico/Fada",80,90,95,30,["Confusão","Vento Fada"]),
}
for _n, _d in species_data.items(): _species(_n, *_d)

MOVE_POWER = {"Investida":7,"Folhagem":9,"Brasa":9,"Jato d'Água":9,"Choque":9}

# ============================================================
# MAPAS
# ============================================================

TOWN_MAP = [
    "################",
    "#..............#",
    "#..HH......HH..#",
    "#..HH......HH..#",
    "#..............#",
    "#....N.........#",
    "#..............#",
    "#..............#",
    "#..............#",
    "#......DD......#",
    "#..............#",
    "################"
]

ROUTE2_MAP = [
    "################",
    "#..............#",
    "#..GG......GG..#",
    "#..GG......GG..#",
    "#..GG....##GG..#",
    "#........##....#",
    "#..T.........T.#",
    "#..............#",
    "#....GG........#",
    "#....GG........#",
    "#..............#",
    "################"
]

TOWN2_MAP = [
    "################",
    "#..............#",
    "#..HH......HH..#",
    "#..HH......HH..#",
    "#..............#",
    "#......GG......#",
    "#......GG......#",
    "#..............#",
    "#....HH........#",
    "#....HH........#",
    "#..............#",
    "################"
]

ROUTE3_MAP = [
    "################",
    "#......GGGG....#",
    "#......GGGG....#",
    "#..............#",
    "#..GG......GG..#",
    "#..GG......GG..#",
    "#..............#",
    "#..............#",
    "#....GG........#",
    "#....GG........#",
    "#..............#",
    "################"
]

GYMTOWN_MAP = [
    "################",
    "#..............#",
    "#..HH....HH....#",
    "#..HH....HH....#",
    "#..............#",
    "#....GG........#",
    "#....GG........#",
    "#..............#",
    "#......HH......#",
    "#......NN......#",
    "#..............#",
    "################"
]

GYM_MAP = [
    "################",
    "#..............#",
    "#..TT....TT....#",
    "#..............#",
    "#....####......#",
    "#....#..#......#",
    "#....#..#......#",
    "#....####......#",
    "#..............#",
    "#..TT......T...#",
    "#..............#",
    "######DD########"
]

ROUTE_MAP = [
    "################",
    "#..............#",
    "#..GGGG........#",
    "#..GGGG........#",
    "#..GGGG....##..#",
    "#..GGGG....##..#",
    "#..........##..#",
    "#..............#",
    "#....GGGG......#",
    "#....GGGG......#",
    "#..............#",
    "################"
]


# ============================================================
# TREINADORES DA V3
# ============================================================

BRASAR_LEADER_PATH = [
    {"leader": "Victorya da Matta", "city": "route2", "badge": "Clover Badge", "level": 20, "team": ["Vulpix de Brasar", "Victeed"]},
    {"leader": "Xuxa", "city": "route3", "badge": "Acre Badge", "level": 25, "team": ["Smoochum", "Varlien"]},
    {"leader": "Marília", "city": "town2", "badge": "Simple Badge", "level": 35, "team": ["Loudred", "Eeveeon", "Miltank"]},
    {"leader": "Luisa", "city": "gymtown", "badge": "Cold Badge", "level": 40, "team": ["Caxinguelice", "Froslass", "Guarartic"]},
    {"leader": "Rita Lee", "city": "gym", "badge": "Poisonous Badge", "level": 12, "team": ["Murizika", "Melotoad"], "leader": True},
    {"leader": "Anitta", "city": "gymtown", "badge": "Heat Badge", "level": 50, "team": ["Pepperim", "Magmar", "Houndoom", "Salazzle"]},
    {"leader": "Milton", "city": "gymtown", "badge": "Mine Badge", "level": 55, "team": ["Carbink", "Rockeon", "Jaduitan", "Briganite"]},
    {"leader": "Alcione", "city": "gymtown", "badge": "Ebony Badge", "level": 60, "team": ["Mismagius", "Carrangrigus", "Bumboi"]},
    {"leader": "Tim", "city": "gymtown", "badge": "Water Badge", "level": 65, "team": ["Gigarucu", "Vaporeon", "Azumarill", "Sirenatee", "Wailord"]},
    {"leader": "Gonzaga", "city": "gymtown", "badge": "Accordion Badge", "level": 70, "team": ["Bastiodon", "Dubwool de Brasar", "Skarmory", "Cabrooat", "Cacturne de Brasar", "Metagross"]},
]

BRASAR_LEADERS = {entry["leader"]: entry for entry in BRASAR_LEADER_PATH}
BRASAR_LEADER_ORDER = {leader: index for index, leader in enumerate([entry["leader"] for entry in BRASAR_LEADER_PATH])}

TRAINERS = {
    "Rival 1": {
        "map": "route1",
        "x": 10,
        "y": 6,
        "team": ["Grubey", "Canarin"]
    },
    "Rival 2": {
        "map": "route2",
        "x": 12,
        "y": 6,
        "team": ["Perigreen", "Briganite"]
    },
    "Treinador Veneno 1": {
        "map": "gym",
        "x": 3,
        "y": 2,
        "team": ["Murizika"]
    },
    "Treinador Veneno 2": {
        "map": "gym",
        "x": 11,
        "y": 9,
        "team": ["Melotoad"]
    },
    "Rita Lee": {
        "map": "gym",
        "x": 7,
        "y": 2,
        "team": ["Murizika", "Melotoad"],
        "leader": True
    }
}

for leader_data in BRASAR_LEADER_PATH:
    name = leader_data["leader"]
    if name not in TRAINERS:
        TRAINERS[name] = {
            "map": leader_data["city"],
            "x": 7,
            "y": 8,
            "team": leader_data["team"],
            "level": leader_data["level"],
            "leader": True,
            "badge": leader_data["badge"],
        }


def get_next_leader_name():
    beaten = len([name for name in BRASAR_LEADER_ORDER if name in trainer_defeated])
    for leader_name in [entry["leader"] for entry in BRASAR_LEADER_PATH]:
        if leader_name not in trainer_defeated:
            return leader_name
    return None


def can_challenge_leader(name):
    if name not in BRASAR_LEADER_ORDER:
        return True
    required_badges = BRASAR_LEADER_ORDER[name]
    return badges >= required_badges

trainer_battle = False
trainer_name = None
trainer_team = []
trainer_index = 0
trainer_enemy_hp = 0
trainer_enemy_max_hp = 0

def check_trainer_encounter():
    for name, trainer in TRAINERS.items():
        if (
            trainer["map"] == current_map
            and trainer["x"] == player_x
            and trainer["y"] == player_y
            and name not in trainer_defeated
        ):
            if name in BRASAR_LEADER_ORDER and not can_challenge_leader(name):
                next_leader = get_next_leader_name()
                required_badges = BRASAR_LEADER_ORDER[name]
                show_message(f"{name} é o próximo líder de Brasar. Você precisa de {required_badges} insígnias para enfrentar esta vaga.")
                if next_leader and next_leader != name:
                    show_message(f"Próximo desafio: {next_leader}.")
                return
            start_trainer_battle(name)
            return

def start_trainer_battle(name):
    global game_mode, trainer_battle, trainer_name
    global trainer_team, trainer_index
    global trainer_enemy_hp, trainer_enemy_max_hp
    global battle_state, battle_cursor

    trainer_battle = True
    trainer_name = name
    if name == "Rival 1":
        level = 5
    elif name == "Rival 2":
        level = 8
    elif name == "Treinador Veneno 1":
        level = 9
    elif name == "Treinador Veneno 2":
        level = 10
    elif name in BRASAR_LEADER_ORDER:
        level = 12 + (BRASAR_LEADER_ORDER[name] * 3)
    else:
        level = 12

    trainer_team = [
        create_pokemon(pokemon_name, level)
        for pokemon_name in TRAINERS[name]["team"]
    ]

    trainer_index = 0
    enemy = trainer_team[0]
    trainer_enemy_hp = enemy["hp"]
    trainer_enemy_max_hp = enemy["max_hp"]

    battle_state = "menu"
    battle_cursor = 0
    game_mode = "battle"

def trainer_current():
    if not trainer_team:
        return None
    return trainer_team[trainer_index]

def advance_trainer_after_defeat():
    global trainer_index
    global trainer_enemy_hp, trainer_enemy_max_hp
    global trainer_battle, trainer_name, trainer_team
    global game_mode

    if trainer_index + 1 < len(trainer_team):
        trainer_index += 1
        enemy = trainer_current()
        trainer_enemy_hp = enemy["hp"]
        trainer_enemy_max_hp = enemy["max_hp"]
        return False

    defeated_name = trainer_name
    trainer_defeated.add(defeated_name)

    if defeated_name == "Rita Lee":
        global badges
        badges = max(badges, 1)

    trainer_battle = False
    trainer_name = None
    trainer_team = []
    trainer_index = 0
    game_mode = "world"

    show_message(defeated_name + " foi derrotado!")
    return True


# ============================================================
# ESTADO DO JOGO
# ============================================================

current_map = "town"

# Insígnias conquistadas
badges = 0
player_x, player_y = 6, 7
rival_defeated = False
trainer_defeated = set()

party = []
pokeballs = 5
money = 300
pokedex = set()

game_mode = "world"  # world, menu, battle, starter
menu_cursor = 0
party_cursor = 0

message = ""
message_timer = 0

battle_enemy = None
battle_enemy_level = 3
battle_enemy_hp = 0
battle_enemy_max_hp = 0
battle_state = "menu"
battle_cursor = 0
battle_message = ""
battle_message_timer = 0
battle_turn_queue = []
battle_turn_index = 0
battle_turn_delay = 0
forced_switch = False

# ============================================================
# FUNÇÕES GERAIS
# ============================================================

def show_message(text, frames=180):
    global message, message_timer
    message = text
    message_timer = frames


def draw_text(text, x, y, font=FONT, color=BLACK):
    screen.blit(font.render(text, True, color), (x, y))


def create_pokemon(name, level=5):
    data = POKEMON[name]
    max_hp = data["base_hp"] + level * 3
    return {
        "name": name,
        "level": level,
        "max_hp": max_hp,
        "hp": max_hp,
        "attack": data["attack"] + level * 2,
        "defense": data["defense"] + level,
        "speed": data["speed"] + level,
        "type": data["type"],
        "moves": list(data["moves"]),
        "xp": 0,
        "xp_to_next": 50 + level * 20,
        "status": "Normal",
        "sleep_turns": 0,
        "ability": data.get("ability", ABILITY_BY_SPECIES.get(name, "None") if "ABILITY_BY_SPECIES" in globals() else "None")
    }


def gain_xp(pokemon, amount):
    pokemon["xp"] += amount

    while pokemon["xp"] >= pokemon["xp_to_next"]:
        pokemon["xp"] -= pokemon["xp_to_next"]
        pokemon["level"] += 1

        old_max = pokemon["max_hp"]
        pokemon["max_hp"] += 6
        pokemon["hp"] += 6
        pokemon["attack"] += 2
        pokemon["defense"] += 1
        pokemon["speed"] += 1
        pokemon["xp_to_next"] = 50 + pokemon["level"] * 20
        old_level_name = pokemon["name"]
        try_evolution(pokemon)

        if pokemon["name"] == old_level_name:
            show_message(
                pokemon["name"] + " subiu para o nível "
                + str(pokemon["level"]) + "!"
            )


def try_evolution(pokemon):
    if pokemon["name"] not in EVOLUTIONS:
        return

    next_name, required = EVOLUTIONS[pokemon["name"]]

    if pokemon["level"] >= required:
        old_name = pokemon["name"]
        old_max = pokemon["max_hp"]
        pokemon["name"] = next_name

        data = POKEMON[next_name]
        pokemon["type"] = data["type"]
        pokemon["max_hp"] = data["base_hp"] + pokemon["level"] * 3
        pokemon["hp"] = pokemon["max_hp"]
        pokemon["attack"] = data["attack"] + pokemon["level"] * 2
        pokemon["defense"] = data["defense"] + pokemon["level"]
        pokemon["speed"] = data["speed"] + pokemon["level"]
        pokemon["moves"] = list(data["moves"])

        pokedex.add(next_name)

        show_message(
            old_name + " evoluiu para " + next_name + "!"
        )

def heal_party():
    for p in party:
        p["hp"] = p["max_hp"]
        p["status"] = "Normal"


def first_alive():
    for i, p in enumerate(party):
        if p["hp"] > 0:
            return i
    return -1


# ============================================================
# MAPA / GRÁFICOS
# ============================================================

def get_map():
    if current_map == "town":
        return TOWN_MAP
    if current_map == "route1":
        return ROUTE_MAP
    if current_map == "route2":
        return ROUTE2_MAP
    if current_map == "town2":
        return TOWN2_MAP
    if current_map == "route3":
        return ROUTE3_MAP
    if current_map == "gymtown":
        return GYMTOWN_MAP
    if current_map == "gym":
        return GYM_MAP
    return TOWN_MAP


def draw_tree(rect):
    pygame.draw.rect(
        screen, BROWN,
        (rect.x + 20, rect.y + 25, 9, 20)
    )
    pygame.draw.circle(
        screen, DARK_GREEN,
        (rect.x + 24, rect.y + 18), 18
    )
    pygame.draw.circle(
        screen, GREEN,
        (rect.x + 12, rect.y + 23), 13
    )
    pygame.draw.circle(
        screen, GREEN,
        (rect.x + 36, rect.y + 23), 13
    )


def draw_house(rect):
    pygame.draw.rect(
        screen, (215, 185, 130),
        (rect.x + 5, rect.y + 18, 38, 25)
    )
    pygame.draw.polygon(
        screen, RED,
        [
            (rect.x + 2, rect.y + 20),
            (rect.x + 24, rect.y + 2),
            (rect.x + 46, rect.y + 20)
        ]
    )
    pygame.draw.rect(
        screen, BLUE,
        (rect.x + 17, rect.y + 28, 14, 15)
    )


def draw_map():
    mapa = get_map()

    screen.fill(LIGHT_GREEN)

    for y, row in enumerate(mapa):
        for x, tile in enumerate(row):
            rect = pygame.Rect(x * TILE, y * TILE, TILE, TILE)

            if tile == "#":
                pygame.draw.rect(screen, DARK_GREEN, rect)
                draw_tree(rect)

            elif tile == ".":
                pygame.draw.rect(screen, PATH, rect)

            elif tile == "G":
                pygame.draw.rect(screen, GREEN, rect)
                for dx in (12, 30):
                    pygame.draw.line(
                        screen, DARK_GREEN,
                        (rect.x + dx, rect.bottom - 6),
                        (rect.x + dx + 4, rect.y + 22),
                        3
                    )

            elif tile == "H":
                draw_house(rect)

            elif tile == "D":
                pygame.draw.rect(screen, WATER, rect)
                pygame.draw.line(
                    screen, WHITE,
                    (rect.x + 7, rect.y + 18),
                    (rect.right - 7, rect.y + 18),
                    2
                )

            elif tile == "N":
                pygame.draw.rect(screen, PATH, rect)

            elif tile == "T":
                pygame.draw.rect(screen, (175, 135, 185), rect)
                pygame.draw.rect(screen, PURPLE, rect, 3)

            pygame.draw.rect(screen, (80, 80, 70), rect, 1)

    # Construções especiais
    if current_map == "gymtown":
        # Ginásio
        pygame.draw.rect(screen, PURPLE, (6 * TILE + 5, 8 * TILE + 18, 38, 25))
        pygame.draw.polygon(
            screen, (105, 55, 135),
            [(6 * TILE + 2, 8 * TILE + 20),
             (6 * TILE + 24, 8 * TILE + 2),
             (6 * TILE + 46, 8 * TILE + 20)]
        )
        draw_text("GINÁSIO", 5 * TILE + 5, 8 * TILE - 5, SMALL, WHITE)

    # Professora Jatobá
    if current_map == "town":
        draw_character(
            5 * TILE + 24,
            5 * TILE + 24,
            PURPLE
        )

    # Treinadores
    for name, t in TRAINERS.items():
        if t["map"] == current_map and name not in trainer_defeated:
            color = PURPLE if t.get("leader") else RED
            draw_character(
                t["x"] * TILE + 24,
                t["y"] * TILE + 24,
                color
            )

    if current_map == "gym":
        draw_text("GINÁSIO VENENOSO", 270, 12, SMALL, WHITE)

    zone_label = BRASAR_PROGRESSION.get(current_map, {}).get("name", "REGIÃO")
    zone_type = BRASAR_PROGRESSION.get(current_map, {}).get("type", "regiao")
    if zone_type == "rota":
        draw_text(zone_label.upper(), 12, 12, SMALL, WHITE)
    elif zone_type == "cidade":
        draw_text(zone_label.upper(), 12, 12, SMALL, WHITE)
    elif current_map == "gym":
        draw_text("GINÁSIO DE BRASAR", 12, 12, SMALL, WHITE)
    else:
        draw_text("REGIÃO DE BRASAR", 12, 12, SMALL, WHITE)

    draw_text("Zona: " + zone_label, 520, 12, SMALL, WHITE)
    draw_text("Insígnias: " + str(badges), 610, 30, SMALL, WHITE)

    # Jogador
    draw_character(
        player_x * TILE + 24,
        player_y * TILE + 24,
        BLUE
    )


def draw_character(cx, cy, color):
    pygame.draw.circle(screen, (240, 195, 155), (cx, cy - 11), 10)
    pygame.draw.rect(screen, color, (cx - 13, cy - 3, 26, 28))
    pygame.draw.rect(screen, BLACK, (cx - 13, cy - 3, 26, 28), 2)
    pygame.draw.rect(screen, BLACK, (cx - 7, cy - 17, 14, 5))


def can_walk(x, y):
    mapa = get_map()

    if y < 0 or y >= len(mapa):
        return False
    if x < 0 or x >= len(mapa[y]):
        return False

    return mapa[y][x] in [".", "G", "D", "N", "T"]


def move_player(dx, dy):
    global player_x, player_y, current_map

    nx = player_x + dx
    ny = player_y + dy

    if not can_walk(nx, ny):
        return

    player_x, player_y = nx, ny

    for origin, ox, oy, target, tx, ty, message in BRASAR_TRANSITIONS:
        if current_map == origin and player_x == ox and player_y == oy:
            current_map = target
            player_x, player_y = tx, ty
            show_message(message)
            return

    if current_map == "gymtown" and (player_x, player_y) == (7, 8) and not story_flags["gym_leader_defeated"]:
        current_map, player_x, player_y = "gym", 7, 10
        show_message("Você entrou no Ginásio!")
        return

    if current_map == "gym" and (player_x, player_y) == (7, 10):
        current_map, player_x, player_y = "gymtown", 7, 8
        show_message("Você saiu do Ginásio.")
        return

    check_trainer_encounter()

    if current_map in ["route1", "route2", "route3"]:
        if get_map()[player_y][player_x] == "G":
            if random.random() < 0.12:
                start_battle()


# ============================================================
# NPC / INICIAL
# ============================================================

def talk():
    global game_mode

    if current_map != "town":
        return

    if abs(player_x - 5) <= 1 and abs(player_y - 5) <= 1:
        if not party:
            game_mode = "starter"
        else:
            show_message(
                "Prof. Jatobá: Continue explorando a Rota 1!"
            )


def draw_starter_screen():
    screen.fill((185, 215, 180))

    title = BIG.render("LABORATÓRIO DA PROF. JATOBÁ", True, BLACK)
    screen.blit(title, (150, 40))

    draw_text(
        "Escolha seu Pokémon inicial:",
        235, 100, FONT
    )

    starters = [
        ("Macarim", GREEN),
        ("Flaguar", ORANGE),
        ("Suriqua", WATER)
    ]

    for i, (name, color) in enumerate(starters):
        x = 130 + i * 245

        pygame.draw.rect(
            screen, WHITE,
            (x - 25, 165, 200, 280)
        )
        pygame.draw.rect(
            screen, BLACK,
            (x - 25, 165, 200, 280),
            3
        )

        draw_big_pokemon(name, x + 75, 260, color)

        draw_text(
            str(i + 1) + " - " + name,
            x, 350
        )

        draw_text(
            POKEMON[name]["type"],
            x, 385, SMALL
        )

    draw_text(
        "Pressione 1, 2 ou 3",
        285, 500
    )


# ============================================================
# DESENHO DE POKÉMON
# ============================================================

def pokemon_color(name):
    return {
        "Macarim": GREEN,
        "Flaguar": ORANGE,
        "Suriqua": WATER,
        "Grubey": (105, 180, 85),
        "Guaramite": GREEN,
        "Canarin": YELLOW,
        "Melotoad": PURPLE
    }.get(name, GRAY)


def draw_big_pokemon(name, x, y, color=None):
    """Desenhos pixel-art simples, feitos com retângulos/polígonos.
    Cada espécie possui uma silhueta diferente; nenhum usa apenas rosto.
    """
    if color is None:
        color = pokemon_color(name)

    # Pixel size
    p = 8

    if name in ("Macarim", "Macacique", "Guarilla"):
        # macaco: corpo, braços, cauda e folhas
        pygame.draw.rect(screen, color, (x-32, y-22, 64, 58))
        pygame.draw.rect(screen, color, (x-48, y-5, 16, 12))
        pygame.draw.rect(screen, color, (x+32, y-5, 16, 12))
        pygame.draw.rect(screen, color, (x+34, y+20, 30, 10))
        pygame.draw.rect(screen, DARK_GREEN, (x-22, y-42, 16, 20))
        pygame.draw.rect(screen, DARK_GREEN, (x-2, y-48, 16, 26))
        pygame.draw.rect(screen, DARK_GREEN, (x+18, y-38, 14, 18))
        pygame.draw.rect(screen, BLACK, (x-20, y-10, 8, 8))
        pygame.draw.rect(screen, BLACK, (x+12, y-10, 8, 8))

    elif name in ("Flaguar", "Flatirica", "Jaguarze"):
        # jaguar: corpo baixo, patas, orelhas e cauda em chamas
        pygame.draw.rect(screen, color, (x-48, y-25, 96, 48))
        pygame.draw.rect(screen, color, (x-38, y-38, 25, 20))
        pygame.draw.rect(screen, color, (x+13, y-38, 25, 20))
        for dx in (-30, 15):
            pygame.draw.rect(screen, color, (x+dx, y+18, 16, 30))
        pygame.draw.rect(screen, color, (x+38, y-2, 45, 12))
        pygame.draw.rect(screen, ORANGE, (x+75, y-12, 14, 30))
        pygame.draw.rect(screen, YELLOW, (x+82, y-20, 8, 12))
        # manchas
        for dx, dy in [(-28,-8),(-5,8),(18,-12),(28,5)]:
            pygame.draw.rect(screen, BLACK, (x+dx, y+dy, p, p))
        pygame.draw.rect(screen, BLACK, (x-22, y-15, 8, 8))
        pygame.draw.rect(screen, BLACK, (x+15, y-15, 8, 8))

    elif name in ("Suriqua", "Snariver", "Tsuconda"):
        # serpente aquática: corpo segmentado
        pts = [
            (x-60,y+10),(x-45,y-12),(x-20,y+8),
            (x+5,y-20),(x+30,y+4),(x+58,y-12)
        ]
        pygame.draw.lines(screen, color, False, pts, 18)
        pygame.draw.rect(screen, color, (x+42,y-30,35,28))
        pygame.draw.polygon(screen, color, [(x+70,y-30),(x+88,y-18),(x+70,y-8)])
        pygame.draw.rect(screen, BLACK, (x+60,y-22,7,7))
        pygame.draw.rect(screen, WHITE, (x+48,y-30,10,7))

    elif name == "Grubey":
        # larva
        pygame.draw.rect(screen, (100,180,85), (x-50,y-20,100,40))
        for dx in (-30,0,30):
            pygame.draw.rect(screen, (70,145,65), (x+dx-8,y+18,16,18))
        pygame.draw.rect(screen, BLACK, (x+25,y-10,8,8))
        pygame.draw.rect(screen, WHITE, (x+26,y-10,3,3))

    elif name == "Julifly":
        # libélula
        pygame.draw.rect(screen, (90,160,110), (x-10,y-45,20,90))
        pygame.draw.polygon(screen, (190,225,240), [(x-10,y-20),(x-65,y-45),(x-70,y-30),(x-10,y-5)])
        pygame.draw.polygon(screen, (190,225,240), [(x+10,y-20),(x+65,y-45),(x+70,y-30),(x+10,y-5)])
        pygame.draw.polygon(screen, (190,225,240), [(x-10,y+10),(x-55,y+40),(x-60,y+25),(x-10,y)])
        pygame.draw.polygon(screen, (190,225,240), [(x+10,y+10),(x+55,y+40),(x+60,y+25),(x+10,y)])

    elif name == "Murizika":
        # morcego insetoide
        pygame.draw.rect(screen, PURPLE, (x-18,y-15,36,50))
        pygame.draw.polygon(screen, PURPLE, [(x-15,y-5),(x-65,y-38),(x-58,y+25),(x-15,y+18)])
        pygame.draw.polygon(screen, PURPLE, [(x+15,y-5),(x+65,y-38),(x+58,y+25),(x+15,y+18)])
        pygame.draw.rect(screen, BLACK, (x-8,y-4,6,6))
        pygame.draw.rect(screen, BLACK, (x+2,y-4,6,6))

    elif name == "Perigreen":
        # ave
        pygame.draw.rect(screen, color, (x-35,y-25,70,50))
        pygame.draw.polygon(screen, color, [(x-25,y-15),(x-75,y+5),(x-35,y+12)])
        pygame.draw.polygon(screen, color, [(x+20,y-18),(x+60,y-45),(x+38,y-5)])
        pygame.draw.polygon(screen, ORANGE, [(x+35,y-10),(x+68,y),(x+35,y+8)])
        pygame.draw.rect(screen, BLACK, (x+15,y-12,7,7))

    elif name == "Canarin":
        # canário
        pygame.draw.rect(screen, YELLOW, (x-35,y-30,70,55))
        pygame.draw.polygon(screen, ORANGE, [(x+30,y-5),(x+65,y+3),(x+30,y+12)])
        pygame.draw.polygon(screen, YELLOW, [(x-15,y-20),(x-65,y-45),(x-45,y-2)])
        pygame.draw.rect(screen, BLACK, (x+10,y-16,8,8))
        pygame.draw.rect(screen, ORANGE, (x-10,y+25,10,18))
        pygame.draw.rect(screen, ORANGE, (x+10,y+25,10,18))

    elif name == "Guaramite":
        # frasco de guaraná
        pygame.draw.rect(screen, (130,70,45), (x-35,y-45,70,90))
        pygame.draw.rect(screen, GREEN, (x-18,y-65,36,20))
        pygame.draw.rect(screen, RED, (x-28,y-10,56,30))
        pygame.draw.rect(screen, WHITE, (x-18,y-4,36,14))
        pygame.draw.rect(screen, BLACK, (x-20,y+15,8,8))
        pygame.draw.rect(screen, BLACK, (x+12,y+15,8,8))

    elif name == "Melotoad":
        # sapo
        pygame.draw.rect(screen, PURPLE, (x-45,y-20,90,50))
        pygame.draw.rect(screen, PURPLE, (x-38,y-38,25,22))
        pygame.draw.rect(screen, PURPLE, (x+13,y-38,25,22))
        pygame.draw.rect(screen, WATER, (x-28,y+15,18,25))
        pygame.draw.rect(screen, WATER, (x+10,y+15,18,25))
        pygame.draw.rect(screen, BLACK, (x-28,y-18,8,8))
        pygame.draw.rect(screen, BLACK, (x+20,y-18,8,8))

    elif name == "Briganite":
        # criatura rochosa com cristal
        pygame.draw.polygon(screen, (135,135,145), [
            (x-45,y+35),(x-55,y-5),(x-20,y-45),(x+20,y-48),
            (x+55,y-5),(x+42,y+38),(x,y+52)
        ])
        pygame.draw.polygon(screen, (210,180,245), [
            (x-8,y-35),(x+8,y-35),(x+18,y+5),(x,y+22),(x-18,y+5)
        ])
        pygame.draw.rect(screen, BLACK, (x-20,y-10,8,8))
        pygame.draw.rect(screen, BLACK, (x+12,y-10,8,8))

    elif name in ("Choralga", "Victeed"):
        # vitória-régia/algas
        pygame.draw.ellipse(screen, GREEN, (x-60,y-35,120,70))
        pygame.draw.rect(screen, (40,120,90), (x-8,y-60,16,45))
        pygame.draw.rect(screen, WATER, (x-35,y+5,20,15))
        pygame.draw.rect(screen, WATER, (x+15,y-5,20,15))
        if name == "Victeed":
            pygame.draw.circle(screen, WHITE, (x,y-42), 18)
            pygame.draw.rect(screen, YELLOW, (x-5,y-47,10,10))

    else:
        # fallback diferente de rosto
        pygame.draw.rect(screen, color, (x-40,y-30,80,60))
        pygame.draw.polygon(screen, color, [(x-40,y-30),(x-10,y-65),(x+5,y-30)])
        pygame.draw.polygon(screen, color, [(x+40,y-30),(x+10,y-65),(x-5,y-30)])
        pygame.draw.rect(screen, BLACK, (x-18,y-5,8,8))
        pygame.draw.rect(screen, BLACK, (x+10,y-5,8,8))


# ============================================================
# BATALHA
# ============================================================

def choose_wild():
    if current_map == "route1":
        choices = [
            "Grubey", "Grubey", "Perigreen",
            "Canarin", "Guaramite"
        ]
    else:
        choices = [
            "Julifly", "Perigreen", "Choralga",
            "Victeed", "Briganite", "Canarin"
        ]
    return random.choice(choices)


def start_battle():
    global game_mode
    global battle_enemy, battle_enemy_level
    global battle_enemy_hp, battle_enemy_max_hp
    global battle_state, battle_cursor

    if first_alive() == -1:
        heal_party()

    alive_team = [p for p in party if p["hp"] > 0]
    player_level = (sum(p["level"] for p in alive_team) / len(alive_team)) if alive_team else 5
    lower = max(1, int(player_level) - 2)
    upper = max(lower + 1, int(player_level) + 1)

    battle_enemy = choose_wild()
    battle_enemy_level = random.randint(lower, upper)

    enemy = create_pokemon(battle_enemy, battle_enemy_level)
    battle_enemy_hp = enemy["hp"]
    battle_enemy_max_hp = enemy["max_hp"]

    battle_state = "menu"
    battle_cursor = 0
    game_mode = "battle"


def get_enemy_for_battle():
    if trainer_battle:
        return trainer_current()
    return create_pokemon(battle_enemy, battle_enemy_level)


def start_battle_turn(move_index):
    global battle_state, battle_turn_queue, battle_turn_index, battle_turn_delay

    active_idx = first_alive()
    if active_idx == -1:
        return

    own = party[active_idx]
    enemy = get_enemy()
    if enemy is None or move_index < 0 or move_index >= len(own.get("moves", [])):
        show_message("Ação de batalha inválida.")
        battle_state = "menu"
        return

    player_move = own["moves"][move_index]
    enemy_move = random.choice(enemy.get("moves", ["Investida"]))
    player_priority = MOVE_DATA.get(player_move, {}).get("priority", 0)
    enemy_priority = MOVE_DATA.get(enemy_move, {}).get("priority", 0)
    player_first = player_priority > enemy_priority or (
        player_priority == enemy_priority and battle_speed(own) >= battle_speed(enemy)
    )
    if player_first:
        battle_turn_queue = [
            {"source": "player", "move_index": move_index},
            {"source": "enemy", "move_name": enemy_move},
        ]
    else:
        battle_turn_queue = [
            {"source": "enemy", "move_name": enemy_move},
            {"source": "player", "move_index": move_index},
        ]

    battle_turn_index = 0
    battle_turn_delay = 12
    battle_state = "turn"


def run_battle_turn_step():
    global battle_state, battle_turn_queue, battle_turn_index, battle_turn_delay
    global forced_switch, party_cursor, active_index

    if not battle_turn_queue or battle_turn_index >= len(battle_turn_queue):
        battle_turn_queue = []
        battle_turn_index = 0
        battle_state = "menu"
        battle_turn_delay = 0
        return

    if 0 <= active_index < len(party) and party[active_index]["hp"] <= 0:
        available = [index for index, pokemon in enumerate(party) if pokemon["hp"] > 0]
        battle_turn_queue = []
        battle_turn_index = 0
        battle_turn_delay = 0
        if not available:
            defeat_player()
        else:
            forced_switch = True
            active_index = -1
            party_cursor = available[0]
            battle_state = "switch"
            show_message("Escolha o próximo Pokémon!")
        return

    action = battle_turn_queue[battle_turn_index]
    previous_trainer_index = trainer_index

    if action["source"] == "player":
        player_attack(action["move_index"], auto_enemy=False)
    else:
        enemy_attack(action.get("move_name"))

    if action["source"] == "player" and trainer_battle and trainer_index != previous_trainer_index:
        battle_turn_queue = []
        battle_turn_index = 0
        battle_state = "menu"
        battle_turn_delay = 0
        return

    if game_mode != "battle" or get_enemy() is None or get_enemy().get("hp", 0) <= 0:
        battle_turn_queue = []
        battle_turn_index = 0
        battle_state = "menu" if game_mode == "battle" else battle_state
        battle_turn_delay = 0
        return

    battle_turn_index += 1

    if battle_turn_index >= len(battle_turn_queue):
        own = party[active_index] if 0 <= active_index < len(party) else None
        enemy = get_enemy()
        for participant in (own, enemy):
            if participant is not None:
                status_message = apply_end_turn_status(participant)
                if status_message:
                    show_message(status_message)
        if own is not None and own.get("hp", 0) <= 0:
            battle_turn_queue = []
            battle_turn_index = 0
            if first_alive() == -1:
                defeat_player()
            else:
                forced_switch = True
                active_index = -1
                party_cursor = next(index for index, pokemon in enumerate(party) if pokemon["hp"] > 0)
                battle_state = "switch"
                show_message("Escolha o próximo Pokémon!")
            battle_turn_delay = 0
            return
        if enemy is not None and enemy.get("hp", 0) <= 0:
            battle_turn_queue = []
            battle_turn_index = 0
            finish_enemy_defeat()
            battle_turn_delay = 0
            return
        battle_turn_queue = []
        battle_turn_index = 0
        battle_state = "menu"
        battle_turn_delay = 0
        return

    battle_turn_delay = 12


def draw_hp_bar(x, y, width, hp, max_hp):
    pygame.draw.rect(screen, BLACK, (x, y, width, 18))

    ratio = 0 if max_hp <= 0 else max(0, min(1, hp / max_hp))

    if ratio > 0.5:
        color = GREEN
    elif ratio > 0.2:
        color = YELLOW
    else:
        color = RED

    pygame.draw.rect(
        screen,
        color,
        (x + 3, y + 3, int((width - 6) * ratio), 12)
    )


def draw_battle():
    screen.fill((220, 235, 205))

    active_index = first_alive()
    own = party[active_index] if active_index >= 0 else None

    # Plataformas
    pygame.draw.ellipse(screen, GREEN, (430, 110, 280, 90))
    pygame.draw.ellipse(screen, GREEN, (55, 335, 300, 95))

    # Inimigo
    enemy_name = trainer_current()["name"] if trainer_battle else battle_enemy
    enemy_level = trainer_current()["level"] if trainer_battle else battle_enemy_level
    enemy_hp = trainer_enemy_hp if trainer_battle else battle_enemy_hp
    enemy_max_hp = trainer_enemy_max_hp if trainer_battle else battle_enemy_max_hp

    draw_big_pokemon(
        enemy_name,
        565, 155
    )

    # Jogador
    if own:
        draw_big_pokemon(
            own["name"],
            205, 375
        )

    # Caixa inimigo
    pygame.draw.rect(screen, WHITE, (35, 35, 350, 120))
    pygame.draw.rect(screen, BLACK, (35, 35, 350, 120), 3)

    label = (trainer_name + ": " if trainer_battle else "") + enemy_name
    draw_text(
        label + "  Nv." + str(enemy_level),
        55, 50
    )
    draw_text(
        POKEMON[enemy_name]["type"],
        55, 78, SMALL
    )
    draw_hp_bar(
        55, 110,
        270,
        enemy_hp,
        enemy_max_hp
    )

    # Caixa do jogador
    if own:
        pygame.draw.rect(screen, WHITE, (390, 270, 340, 125))
        pygame.draw.rect(screen, BLACK, (390, 270, 340, 125), 3)

        draw_text(
            own["name"] + "  Nv." + str(own["level"]),
            410, 285
        )
        draw_text(
            own["type"],
            410, 313, SMALL
        )

        draw_hp_bar(
            410, 340,
            250,
            own["hp"],
            own["max_hp"]
        )

        draw_text(
            str(own["hp"]) + "/" + str(own["max_hp"]),
            590, 365, SMALL
        )

    # Caixa inferior
    pygame.draw.rect(screen, WHITE, (0, 450, WIDTH, 126))
    pygame.draw.rect(screen, BLACK, (0, 450, WIDTH, 126), 4)

    if battle_state == "menu":
        options = [
            "LUTAR", "POKÉMON",
            "MOCHILA", "FUGIR"
        ]

        for i, option in enumerate(options):
            x = 70 + (i % 2) * 330
            y = 465 + (i // 2) * 48

            if battle_cursor == i:
                draw_text(">", x - 25, y)

            draw_text(option, x, y)

    elif battle_state == "turn":
        draw_text("Ação em andamento...", 220, 470, BIG)

    elif battle_state == "fight":
        active = party[first_alive()]
        moves = active["moves"]

        for i in range(4):
            x = 60 + (i % 2) * 330
            y = 465 + (i // 2) * 45

            if i < len(moves):
                if battle_cursor == i:
                    draw_text(">", x - 25, y)
                draw_text(moves[i], x, y)
            else:
                draw_text("---", x, y)


def enemy_attack(move_name=None):
    global battle_enemy_hp, trainer_enemy_hp, game_mode

    idx = first_alive()
    if idx == -1:
        return

    own = party[idx]

    if trainer_battle:
        enemy = trainer_current()
    else:
        enemy = create_pokemon(battle_enemy, battle_enemy_level)

    damage = max(
        2,
        (enemy["attack"] * 2 + random.randint(1, 6)) // 3
        - (own["defense"] // 3)
        + max(0, enemy["level"] - own["level"]) // 2
    )

    ability = enemy.get("ability", "None")
    enemy_type = enemy.get("type", "Normal").split("/")[0]
    if ability == "Intimidate":
        damage = max(2, damage - 2)
    if ability == "Blaze" and enemy["hp"] * 3 <= enemy["max_hp"] and enemy_type == "Fogo":
        damage = int(damage * 1.35)
    elif ability == "Overgrow" and enemy["hp"] * 3 <= enemy["max_hp"] and enemy_type == "Grama":
        damage = int(damage * 1.35)
    elif ability == "Torrent" and enemy["hp"] * 3 <= enemy["max_hp"] and enemy_type == "Água":
        damage = int(damage * 1.35)

    own["hp"] = max(0, own["hp"] - damage)

    if own["hp"] > 0 and ability == "Static" and random.random() < 0.20:
        if own.get("status", "Normal") == "Normal":
            own["status"] = "Paralisado"
            show_message(own["name"] + " foi paralisado pela habilidade Static!")

    if own["hp"] <= 0:
        show_message(own["name"] + " desmaiou!")

        if first_alive() == -1:
            heal_party()
            game_mode = "world"
            show_message(
                "Sua equipe foi recuperada no Centro Pokémon."
            )


def player_attack(move_index, auto_enemy=True):
    global badges
    global battle_enemy_hp, game_mode, battle_state
    global trainer_enemy_hp

    idx = first_alive()
    if idx == -1:
        return

    own = party[idx]
    moves = own["moves"]

    if move_index >= len(moves):
        return

    move = moves[move_index]
    power = MOVE_POWER.get(move, 6)

    damage = max(
        2,
        (own["attack"] * 2 + power + random.randint(1, 6)) // 3
        - (get_enemy_for_battle()["defense"] // 3)
    )

    ability = own.get("ability", "None")
    move_type = MOVE_DATA.get(move, {}).get("type", own.get("type", "Normal").split("/")[0])
    ability_type = {"Blaze":"Fogo", "Overgrow":"Grama", "Torrent":"Água"}.get(ability)
    if ability_type == move_type and own["hp"] * 3 <= own["max_hp"]:
        damage = max(2, int(damage * 1.35))
        show_message(own["name"] + " ativou " + ability + "!")

    if random.random() < 0.1:
        damage = int(damage * 1.6)
        show_message("Acerto crítico!")

    if trainer_battle:
        trainer_enemy_hp = max(0, trainer_enemy_hp - damage)
        if trainer_enemy_hp <= 0:
            xp = 25 + trainer_current()["level"] * 10
            gain_xp(own, xp)

            defeated_name_before = trainer_name
            defeated = advance_trainer_after_defeat()
            if not defeated:
                show_message(
                    trainer_name + " enviou outro Pokémon!"
                )
            else:
                if defeated_name_before == "Rita Lee":
                    show_message("Você venceu o primeiro Ginásio! Recebeu a Insígnia Erva!")
                    badges += 1
                    game_mode = "world"
                    globals()["current_map"] = "gym"
                    globals()["player_x"] = 7
                    globals()["player_y"] = 10
            return
    else:
        battle_enemy_hp = max(0, battle_enemy_hp - damage)

        if battle_enemy_hp <= 0:
            xp = 20 + battle_enemy_level * 8
            gain_xp(own, xp)
            show_message(
                battle_enemy + " foi derrotado! "
                + own["name"] + " ganhou "
                + str(xp) + " EXP."
            )
            game_mode = "world"
            return

    if auto_enemy:
        enemy_attack()
        battle_state = "menu"


def try_capture():
    global pokeballs, game_mode

    if trainer_battle:
        show_message("Você não pode capturar Pokémon de um treinador!")
        return

    if pokeballs <= 0:
        show_message("Você não tem Pokébolas.")
        return

    pokeballs -= 1

    chance = 0.35
    if battle_enemy_hp <= battle_enemy_max_hp * 0.5:
        chance = 0.70

    if random.random() < chance:
        if len(party) < 6:
            new = create_pokemon(
                battle_enemy,
                battle_enemy_level
            )
            party.append(new)
            pokedex.add(battle_enemy)

            show_message(
                battle_enemy + " foi capturado!"
            )
            game_mode = "world"
        else:
            show_message(
                "Sua equipe está cheia."
            )
    else:
        show_message(
            "A Pokébola falhou!"
        )
        enemy_attack()


def battle_switch():
    global party_cursor, battle_state

    if len(party) <= 1:
        show_message("Você não tem outro Pokémon.")
        return

    alive = [i for i, p in enumerate(party) if p["hp"] > 0]

    if not alive:
        return

    party_cursor = alive[0]
    battle_state = "switch"


def perform_switch(index):
    global battle_state

    if index < 0 or index >= len(party):
        return

    if party[index]["hp"] <= 0:
        show_message("Esse Pokémon está desmaiado.")
        return

    if index == first_alive():
        show_message("Esse Pokémon já está em batalha.")
        return

    # Para este protótipo, a troca é instantânea.
    # O próximo turno pertence ao adversário.
    current = party[first_alive()]
    current["status"] = "Normal"

    # Coloca o escolhido na frente da lista.
    chosen = party.pop(index)
    party.insert(0, chosen)

    battle_state = "menu"
    enemy_attack()


# ============================================================
# MENU PRINCIPAL
# ============================================================

def draw_menu():
    screen.fill((180, 205, 175))

    pygame.draw.rect(screen, WHITE, (150, 50, 468, 470))
    pygame.draw.rect(screen, BLACK, (150, 50, 468, 470), 4)

    draw_text("MENU", 345, 75, BIG)

    options = [
        "POKÉMON",
        "POKÉDEX",
        "MOCHILA",
        "VOLTAR"
    ]

    for i, option in enumerate(options):
        y = 150 + i * 70

        if menu_cursor == i:
            draw_text(">", 220, y)

        draw_text(option, 260, y)

    draw_text(
        "Pokébolas: " + str(pokeballs),
        260, 390
    )

    draw_text(
        "Dinheiro: $" + str(money),
        260, 425
    )

    draw_text(
        "Insígnias: " + str(badges),
        260, 460
    )


def draw_party_screen():
    screen.fill((180, 205, 175))

    pygame.draw.rect(screen, WHITE, (80, 40, 608, 500))
    pygame.draw.rect(screen, BLACK, (80, 40, 608, 500), 4)

    draw_text("EQUIPE POKÉMON", 285, 65, BIG)

    if not party:
        draw_text(
            "Você ainda não possui Pokémon.",
            210, 250
        )
        return

    for i, p in enumerate(party):
        y = 130 + i * 65

        if i == party_cursor:
            pygame.draw.rect(
                screen, (220, 235, 210),
                (120, y - 8, 525, 55)
            )

        draw_text(
            p["name"] + "  Nv." + str(p["level"]),
            140, y
        )

        draw_hp_bar(
            370, y + 3,
            180,
            p["hp"],
            p["max_hp"]
        )

        draw_text(
            str(p["hp"]) + "/" + str(p["max_hp"]),
            555, y, SMALL
        )

        draw_text(
            "Status: " + p["status"],
            140, y + 27, SMALL
        )

    draw_text(
        "ENTER = selecionar   ESC = voltar",
        220, 505, SMALL
    )


def draw_pokedex_screen():
    screen.fill((180, 205, 175))

    pygame.draw.rect(screen, WHITE, (120, 50, 528, 470))
    pygame.draw.rect(screen, BLACK, (120, 50, 528, 470), 4)

    draw_text("POKÉDEX", 320, 75, BIG)

    names = list(POKEMON.keys())

    for i, name in enumerate(names):
        x = 165 + (i % 2) * 245
        y = 140 + (i // 2) * 70

        seen = name in pokedex or any(
            p["name"] == name for p in party
        )

        if seen:
            draw_text(
                "✓ " + name,
                x, y
            )
            draw_text(
                POKEMON[name]["type"],
                x, y + 25, SMALL
            )
        else:
            draw_text(
                "? " + "???",
                x, y
            )

    draw_text(
        "Descobertos: " + str(len(pokedex)) +
        "/" + str(len(POKEMON)),
        280, 460
    )

    draw_text(
        "ESC = voltar",
        325, 500, SMALL
    )


def draw_bag_screen():
    screen.fill((180, 205, 175))

    pygame.draw.rect(screen, WHITE, (180, 90, 408, 380))
    pygame.draw.rect(screen, BLACK, (180, 90, 408, 380), 4)

    draw_text("MOCHILA", 320, 115, BIG)

    draw_text(
        "Pokébolas: " + str(pokeballs),
        250, 200
    )

    draw_text(
        "Dinheiro: $" + str(money),
        250, 250
    )

    draw_text(
        "ESC = voltar",
        310, 420, SMALL
    )


# ============================================================
# INPUT
# ============================================================

def handle_menu_key(key):
    global game_mode, menu_cursor

    if key == pygame.K_UP:
        menu_cursor = (menu_cursor - 1) % 4

    elif key == pygame.K_DOWN:
        menu_cursor = (menu_cursor + 1) % 4

    elif key in [pygame.K_RETURN, pygame.K_z, pygame.K_1,
                 pygame.K_2, pygame.K_3, pygame.K_4]:

        # Também permite os números 1-4 como no protótipo anterior.
        if key == pygame.K_1:
            menu_cursor = 0
        elif key == pygame.K_2:
            menu_cursor = 1
        elif key == pygame.K_3:
            menu_cursor = 2
        elif key == pygame.K_4:
            menu_cursor = 3

        if menu_cursor == 0:
            game_mode = "party"
        elif menu_cursor == 1:
            game_mode = "pokedex"
        elif menu_cursor == 2:
            game_mode = "bag"
        elif menu_cursor == 3:
            game_mode = "world"

    elif key == pygame.K_x or key == pygame.K_ESCAPE:
        game_mode = "world"


def handle_party_key(key):
    global party_cursor, game_mode

    if key == pygame.K_UP:
        party_cursor = max(0, party_cursor - 1)

    elif key == pygame.K_DOWN:
        party_cursor = min(
            max(0, len(party) - 1),
            party_cursor + 1
        )

    elif key in [pygame.K_ESCAPE, pygame.K_x]:
        game_mode = "menu"

    elif key == pygame.K_RETURN and party:
        # Fora da batalha: cura não acontece automaticamente.
        show_message(
            party[party_cursor]["name"] +
            " está no nível " +
            str(party[party_cursor]["level"])
        )


def handle_battle_key(key):
    global battle_state, battle_cursor, party_cursor, game_mode

    if battle_state == "menu":

        if key == pygame.K_UP:
            battle_cursor = (battle_cursor - 1) % 4

        elif key == pygame.K_DOWN:
            battle_cursor = (battle_cursor + 1) % 4

        elif key == pygame.K_LEFT:
            if battle_cursor % 2 == 1:
                battle_cursor -= 1

        elif key == pygame.K_RIGHT:
            if battle_cursor % 2 == 0:
                battle_cursor += 1

        elif key in [pygame.K_RETURN, pygame.K_z]:
            if battle_cursor == 0:
                battle_state = "fight"
                battle_cursor = 0

            elif battle_cursor == 1:
                battle_switch()

            elif battle_cursor == 2:
                try_capture()

            elif battle_cursor == 3:
                if random.random() < 0.8:
                    game_mode = "world"
                    show_message("Você fugiu!")
                else:
                    show_message("Você não conseguiu fugir!")
                    enemy_attack()

    elif battle_state == "fight":

        moves = party[first_alive()]["moves"]

        if key == pygame.K_LEFT:
            if battle_cursor % 2 == 1:
                battle_cursor -= 1

        elif key == pygame.K_RIGHT:
            if battle_cursor % 2 == 0:
                battle_cursor += 1

        elif key == pygame.K_UP:
            battle_cursor = max(0, battle_cursor - 2)

        elif key == pygame.K_DOWN:
            battle_cursor = min(3, battle_cursor + 2)

        elif key in [pygame.K_RETURN, pygame.K_z]:
            if battle_cursor < len(moves):
                start_battle_turn(battle_cursor)
            else:
                show_message("Esse espaço está vazio.")

        elif key in [pygame.K_ESCAPE, pygame.K_x]:
            battle_state = "menu"
            battle_cursor = 0

    elif battle_state == "switch":

        if key == pygame.K_UP:
            party_cursor = max(0, party_cursor - 1)

        elif key == pygame.K_DOWN:
            party_cursor = min(
                max(0, len(party) - 1),
                party_cursor + 1
            )

        elif key in [pygame.K_RETURN, pygame.K_z]:
            perform_switch(party_cursor)

        elif key in [pygame.K_ESCAPE, pygame.K_x]:
            battle_state = "menu"



# ============================================================
# V5 - SISTEMAS REVISADOS
# ============================================================

# A V5 mantém o protótipo em um único arquivo para facilitar o teste,
# mas organiza os sistemas em blocos reutilizáveis.
from pathlib import Path
import json

# ---------- Mapas corrigidos ----------
# A entrada do ginásio (7,8) agora é um piso caminhável.
GYMTOWN_MAP = [
    "################",
    "#..............#",
    "#..HH....HH....#",
    "#..HH....HH....#",
    "#..............#",
    "#....GG........#",
    "#....GG........#",
    "#..............#",
    "#......N.......#",
    "#......NN......#",
    "#..............#",
    "################"
]

# ---------- Dados de golpes ----------
MOVE_DATA = {
    "Investida":   {"type": "Normal", "power": 40, "accuracy": 100, "pp": 35, "category": "Físico", "effect": None, "chance": 0},
    "Folhagem":    {"type": "Grama", "power": 40, "accuracy": 100, "pp": 25, "category": "Especial", "effect": None, "chance": 0},
    "Brasa":       {"type": "Fogo", "power": 40, "accuracy": 100, "pp": 25, "category": "Especial", "effect": "Queimado", "chance": 10},
    "Jato d'Água": {"type": "Água", "power": 40, "accuracy": 100, "pp": 25, "category": "Especial", "effect": None, "chance": 0},
    "Choque":      {"type": "Elétrico", "power": 40, "accuracy": 100, "pp": 30, "category": "Especial", "effect": "Paralisado", "chance": 10},
    "Picada":      {"type": "Inseto", "power": 40, "accuracy": 100, "pp": 30, "category": "Físico", "effect": None, "chance": 0},
    "Toxina":      {"type": "Veneno", "power": 50, "accuracy": 100, "pp": 25, "category": "Especial", "effect": "Envenenado", "chance": 30},
    "Lodo":        {"type": "Veneno", "power": 50, "accuracy": 100, "pp": 20, "category": "Especial", "effect": "Envenenado", "chance": 30},
    "Pedrada":     {"type": "Pedra", "power": 50, "accuracy": 90,  "pp": 20, "category": "Físico", "effect": None, "chance": 0},
    "Asa de Vento": {"type": "Voador", "power": 45, "accuracy": 100, "pp": 25, "category": "Físico", "effect": None, "chance": 0},
    "Mordida":      {"type": "Sombrio", "power": 60, "accuracy": 100, "pp": 25, "category": "Físico", "effect": None, "chance": 0},
    "Ataque Rápido": {"type": "Normal", "power": 40, "accuracy": 100, "pp": 30, "category": "Físico", "effect": None, "chance": 0, "priority": 1},
    "Golpe Corporal": {"type": "Normal", "power": 85, "accuracy": 100, "pp": 15, "category": "Físico", "effect": "Paralisado", "chance": 30},
}

# Atualiza golpes das espécies já existentes.
POKEMON["Grubey"]["moves"] = ["Investida", "Picada"]
POKEMON["Murizika"]["moves"] = ["Picada", "Toxina"]
POKEMON["Melotoad"]["moves"] = ["Jato d'Água", "Lodo"]
POKEMON["Perigreen"]["moves"] = ["Investida", "Asa de Vento"]
POKEMON["Briganite"]["moves"] = ["Pedrada", "Investida"]
POKEMON["Canarin"]["moves"] = ["Choque", "Asa de Vento"]

TYPE_EFFECTIVENESS = {
    ("Fogo", "Grama"): 2.0, ("Fogo", "Inseto"): 2.0,
    ("Fogo", "Água"): 0.5, ("Fogo", "Pedra"): 0.5,
    ("Água", "Fogo"): 2.0, ("Água", "Pedra"): 2.0,
    ("Água", "Grama"): 0.5,
    ("Grama", "Água"): 2.0, ("Grama", "Pedra"): 2.0,
    ("Grama", "Fogo"): 0.5, ("Grama", "Inseto"): 0.5,
    ("Elétrico", "Água"): 2.0, ("Elétrico", "Voador"): 2.0,
    ("Elétrico", "Grama"): 0.5,
    ("Veneno", "Grama"): 2.0, ("Veneno", "Pedra"): 0.5,
    ("Inseto", "Grama"): 2.0, ("Inseto", "Voador"): 0.5,
    ("Pedra", "Fogo"): 2.0, ("Pedra", "Voador"): 2.0,
    ("Voador", "Grama"): 2.0, ("Voador", "Inseto"): 2.0,
    ("Normal", "Pedra"): 0.5,
    ("Lutador", "Pedra"): 2.0, ("Lutador", "Fada"): 0.5,
    ("Normal", "Fantasma"): 0.0, ("Fantasma", "Normal"): 0.0,
    ("Elétrico", "Terra"): 0.0, ("Terra", "Voador"): 0.0,
    ("Veneno", "Aço"): 0.0, ("Dragão", "Fada"): 0.0,
    ("Psíquico", "Sombrio"): 0.0,
}

# ---------- Itens/economia ----------
items = {
    "Poção": 2,
    "Super Poção": 0,
    "Antídoto": 1,
}
shop_prices = {
    "Pokébola": 200,
    "Poção": 300,
    "Antídoto": 100,
}
shop_cursor = 0

# ---------- Estado de batalha ----------
active_index = 0
battle_enemy_obj = None
battle_enemy_status = "Normal"
battle_turn_message = ""

# ---------- Progressão ----------
story_flags = {
    "starter_received": False,
    "rival_1_defeated": False,
    "rival_2_defeated": False,
    "gym_trainers_defeated": False,
    "gym_leader_defeated": False,
}

BRASAR_PROGRESSION = {
    "town": {"name": "Guarany Town", "type": "cidade", "wild_levels": (2, 4), "encounters": [], "story": "Berço da jornada e ponto de partida da região."},
    "route1": {"name": "Rota 1", "type": "rota", "wild_levels": (3, 5), "encounters": ["Grubey", "Perigreen", "Canarin", "Guaramite"], "story": "A primeira trilha de Brasar, com florestas e pequenos desafios."},
    "route2": {"name": "Rota 2", "type": "rota", "wild_levels": (6, 8), "encounters": ["Julifly", "Perigreen", "Briganite", "Canarin", "Grubey"], "story": "A rota deixa a cidade e abre caminho para a região centro-norte."},
    "town2": {"name": "Cuiabee City", "type": "cidade", "wild_levels": (5, 7), "encounters": [], "story": "Uma cidade de mercado, treino e primeiro grande ponto de decisão."},
    "route3": {"name": "Rota 3", "type": "rota", "wild_levels": (8, 11), "encounters": ["Choralga", "Victeed", "Briganite", "Canarin", "Murizika", "Perigreen"], "story": "Ela empurra o aventureiro para o coração da região e os desafios mais fortes."},
    "gymtown": {"name": "Cidade do Ginásio", "type": "cidade", "wild_levels": (8, 11), "encounters": [], "story": "A cidade do primeiro grande confronto oficial da região."},
    "gym": {"name": "Ginásio de Brasar", "type": "ginasio", "wild_levels": (10, 12), "encounters": [], "story": "O teste de liderança e o início do caminho rumo ao topo da região."},
}

BRASAR_ROUTE_ORDER = [
    "town",
    "route1",
    "route2",
    "town2",
    "route3",
    "gymtown",
    "gym",
]

BRASAR_TRANSITIONS = [
    ("town", 7, 9, "route1", 7, 1, "Você entrou na Rota 1! A primeira etapa de Brasar começa aqui."),
    ("route1", 7, 1, "town", 7, 8, "Você voltou para a cidade inicial."),
    ("route1", 8, 1, "route2", 8, 10, "Você chegou à Rota 2! O caminho se abre para a região central."),
    ("route2", 8, 10, "route1", 8, 1, "Você voltou para a Rota 1."),
    ("route2", 8, 1, "town2", 8, 10, "Você chegou à Cuiabee City! Um ponto turístico e de treinamento da região."),
    ("town2", 8, 10, "route2", 8, 1, "Você voltou para a Rota 2."),
    ("town2", 14, 6, "route3", 1, 6, "Você entrou na Rota 3! O desafio se torna mais intenso."),
    ("route3", 1, 6, "town2", 14, 6, "Você voltou para a cidade."),
    ("route3", 7, 1, "gymtown", 7, 10, "Você chegou à cidade do ginásio! O primeiro grande caminho da região foi concluído."),
    ("gymtown", 7, 10, "route3", 7, 1, "Você voltou para a Rota 3."),
]


def get_current_zone_info():
    zone = BRASAR_PROGRESSION.get(current_map, {"name": "Brasar", "type": "regiao", "story": "Região de Brasar"})
    return zone

SAVE_FILE = Path("brasar_save.json")


def pokemon_types(type_text):
    return [t.strip() for t in type_text.split("/")]


def type_effectiveness(move_type, defender_type):
    multiplier = 1.0
    for defender in pokemon_types(defender_type):
        multiplier *= TYPE_EFFECTIVENESS.get((move_type, defender), 1.0)
    return multiplier


def status_can_act(pokemon):
    status = pokemon.get("status", "Normal")
    if status == "Paralisado" and random.random() < 0.25:
        show_message(pokemon["name"] + " está paralisado e não conseguiu atacar!")
        return False
    if status == "Adormecido":
        turns = pokemon.get("sleep_turns", 1)
        if turns > 0:
            pokemon["sleep_turns"] = turns - 1
            show_message(pokemon["name"] + " está dormindo!")
            return False
        pokemon["status"] = "Normal"
    if status == "Congelado":
        if random.random() < 0.20:
            pokemon["status"] = "Normal"
            show_message(pokemon["name"] + " descongelou!")
        else:
            show_message(pokemon["name"] + " está congelado!")
            return False
    if status == "Confuso" and random.random() < 0.33:
        damage = max(1, pokemon["attack"] // 3)
        pokemon["hp"] = max(0, pokemon["hp"] - damage)
        show_message(pokemon["name"] + " se machucou na confusão!")
        return False
    return True


def battle_speed(pokemon):
    speed = pokemon.get("speed", 0)
    if pokemon.get("status") == "Paralisado":
        return max(1, speed // 2)
    return speed


def apply_end_turn_status(pokemon):
    status = pokemon.get("status", "Normal")
    if status == "Envenenado":
        damage = max(1, pokemon["max_hp"] // 8)
        pokemon["hp"] = max(0, pokemon["hp"] - damage)
        return pokemon["name"] + " sofreu dano de veneno!"
    if status == "Queimado":
        damage = max(1, pokemon["max_hp"] // 12)
        pokemon["hp"] = max(0, pokemon["hp"] - damage)
        return pokemon["name"] + " sofreu dano da queimadura!"
    return None


def create_pokemon(name, level=5):
    data = POKEMON[name]
    max_hp = data["base_hp"] + level * 3
    moves = []
    for move in data["moves"]:
        moves.append(move)
    return {
        "name": name,
        "level": level,
        "max_hp": max_hp,
        "hp": max_hp,
        "attack": data["attack"] + level * 2,
        "defense": data["defense"] + level,
        "sp_attack": data.get("sp_attack", data["attack"]) + level * 2,
        "sp_defense": data.get("sp_defense", data["defense"]) + level,
        "speed": data["speed"] + level,
        "type": data["type"],
        "moves": moves,
        "ability": data.get("ability", ABILITY_BY_SPECIES.get(name, "None") if "ABILITY_BY_SPECIES" in globals() else "None"),
        "xp": 0,
        "xp_to_next": 50 + level * 20,
        "status": "Normal",
        "sleep_turns": 0,
        "move_pp": {m: MOVE_DATA.get(m, {"pp": 20})["pp"] for m in moves},
    }


def heal_party():
    for p in party:
        p["hp"] = p["max_hp"]
        p["status"] = "Normal"
        p["sleep_turns"] = 0
        for move in p.get("move_pp", {}):
            p["move_pp"][move] = MOVE_DATA.get(move, {"pp": 20})["pp"]


def first_alive():
    global active_index
    if party and 0 <= active_index < len(party) and party[active_index]["hp"] > 0:
        return active_index
    for i, p in enumerate(party):
        if p["hp"] > 0:
            active_index = i
            return i
    return -1


def gain_xp(pokemon, amount):
    pokemon["xp"] += amount
    messages = []
    while pokemon["xp"] >= pokemon["xp_to_next"]:
        pokemon["xp"] -= pokemon["xp_to_next"]
        pokemon["level"] += 1
        pokemon["max_hp"] += 6
        pokemon["hp"] = pokemon["max_hp"]
        pokemon["attack"] += 2
        pokemon["defense"] += 1
        pokemon["sp_attack"] += 2
        pokemon["sp_defense"] += 1
        pokemon["speed"] += 1
        pokemon["xp_to_next"] = 50 + pokemon["level"] * 20
        messages.append(pokemon["name"] + " subiu para o nível " + str(pokemon["level"]) + "!")
        if pokemon["name"] in EVOLUTIONS:
            next_name, required = EVOLUTIONS[pokemon["name"]]
            if pokemon["level"] >= required:
                old_name = pokemon["name"]
                pokemon["name"] = next_name
                data = POKEMON[next_name]
                pokemon["type"] = data["type"]
                pokemon["max_hp"] = data["base_hp"] + pokemon["level"] * 3
                pokemon["hp"] = pokemon["max_hp"]
                pokemon["attack"] = data["attack"] + pokemon["level"] * 2
                pokemon["defense"] = data["defense"] + pokemon["level"]
                pokemon["sp_attack"] = data.get("sp_attack", data["attack"]) + pokemon["level"] * 2
                pokemon["sp_defense"] = data.get("sp_defense", data["defense"]) + pokemon["level"]
                pokemon["speed"] = data["speed"] + pokemon["level"]
                pokemon["moves"] = list(data["moves"])
                pokemon["ability"] = data.get("ability", pokemon.get("ability", "None"))
                pokemon["move_pp"] = {m: MOVE_DATA.get(m, {"pp": 20})["pp"] for m in pokemon["moves"]}
                pokedex.add(next_name)
                messages.append(old_name + " evoluiu para " + next_name + "!")
    show_message(" ".join(messages) if messages else pokemon["name"] + " ganhou " + str(amount) + " EXP.")


def get_map():
    maps = {
        "town": TOWN_MAP, "route1": ROUTE_MAP, "route2": ROUTE2_MAP,
        "town2": TOWN2_MAP, "route3": ROUTE3_MAP, "gymtown": GYMTOWN_MAP,
        "gym": GYM_MAP,
    }
    return maps.get(current_map, TOWN_MAP)


def can_walk(x, y):
    mapa = get_map()
    if y < 0 or y >= len(mapa) or x < 0 or x >= len(mapa[y]):
        return False
    return mapa[y][x] in [".", "G", "D", "N", "T", "C", "S"]


def party_average_level():
    if not party:
        return 5
    living = [p for p in party if p.get("hp", 0) > 0]
    if not living:
        return 5
    return sum(p["level"] for p in living) / len(living)


def clamp_battle_level(level, map_name):
    avg = party_average_level()
    base = {
        "route1": max(3, min(8, int(avg) + 0)),
        "route2": max(4, min(10, int(avg) + 2)),
        "route3": max(6, min(12, int(avg) + 3)),
        "gymtown": max(8, min(15, int(avg) + 4)),
        "gym": max(10, min(18, int(avg) + 5)),
    }.get(map_name, max(3, min(12, int(avg) + 1)))
    return max(2, min(level, base + 2))


def choose_wild():
    encounters = BRASAR_PROGRESSION.get(current_map, {}).get("encounters", [])
    if encounters:
        return random.choice(encounters)
    return random.choice(["Choralga", "Victeed", "Briganite", "Canarin", "Murizika", "Perigreen"])


def wild_level_range():
    base_range = BRASAR_PROGRESSION.get(current_map, {}).get("wild_levels", (2, 5))
    avg = party_average_level()
    lo, hi = base_range
    adjusted_lo = max(2, min(lo, max(2, int(avg) - 1)))
    adjusted_hi = min(max(lo, hi), max(lo, min(hi, int(avg) + 3)))
    return adjusted_lo, adjusted_hi


def start_battle():
    global game_mode, battle_enemy, battle_enemy_level, battle_enemy_hp, battle_enemy_max_hp
    global battle_state, battle_cursor, battle_enemy_obj, battle_enemy_status, active_index
    if first_alive() == -1:
        return
    battle_enemy = choose_wild()
    lo, hi = wild_level_range()
    battle_enemy_level = clamp_battle_level(random.randint(lo, hi), current_map)
    battle_enemy_obj = create_pokemon(battle_enemy, battle_enemy_level)
    battle_enemy_hp = battle_enemy_obj["hp"]
    battle_enemy_max_hp = battle_enemy_obj["max_hp"]
    battle_enemy_status = "Normal"
    battle_state = "menu"
    battle_cursor = 0
    game_mode = "battle"


def start_trainer_battle(name):
    global game_mode, trainer_battle, trainer_name, trainer_team, trainer_index
    global trainer_enemy_hp, trainer_enemy_max_hp, battle_state, battle_cursor, active_index
    trainer_battle = True
    trainer_name = name
    levels = {"Rival 1": 5, "Rival 2": 8, "Treinador Veneno 1": 9, "Treinador Veneno 2": 10, "Rita Lee": 12}
    level = levels.get(name, 5)
    if name in BRASAR_LEADER_ORDER:
        level = max(8, min(12 + BRASAR_LEADER_ORDER[name] * 2, 12 + BRASAR_LEADER_ORDER[name] * 3))
    level = clamp_battle_level(level, current_map)
    trainer_team = [create_pokemon(n, level) for n in TRAINERS[name]["team"]]
    trainer_index = 0
    enemy = trainer_team[0]
    trainer_enemy_hp = enemy["hp"]
    trainer_enemy_max_hp = enemy["max_hp"]
    battle_state = "menu"
    battle_cursor = 0
    active_index = first_alive()
    game_mode = "battle"


def trainer_current():
    if not trainer_team or trainer_index >= len(trainer_team):
        return None
    return trainer_team[trainer_index]


def trainer_reward(name):
    return {"Rival 1": 300, "Rival 2": 500, "Treinador Veneno 1": 250, "Treinador Veneno 2": 300, "Rita Lee": 1200}.get(name, 100)


def advance_trainer_after_defeat():
    global trainer_index, trainer_enemy_hp, trainer_enemy_max_hp
    global trainer_battle, trainer_name, trainer_team, game_mode, badges
    if trainer_index + 1 < len(trainer_team):
        trainer_index += 1
        enemy = trainer_current()
        trainer_enemy_hp = enemy["hp"]
        trainer_enemy_max_hp = enemy["max_hp"]
        return False
    defeated_name = trainer_name
    trainer_defeated.add(defeated_name)
    money_gain = trainer_reward(defeated_name)
    globals()["money"] += money_gain
    if defeated_name == "Rival 1": story_flags["rival_1_defeated"] = True
    if defeated_name == "Rival 2": story_flags["rival_2_defeated"] = True
    if defeated_name.startswith("Treinador Veneno"): story_flags["gym_trainers_defeated"] = True
    if defeated_name == "Rita Lee":
        story_flags["gym_leader_defeated"] = True
        badges = max(badges, 1)
    if defeated_name in BRASAR_LEADER_ORDER:
        badges = max(badges, BRASAR_LEADER_ORDER[defeated_name] + 1)
    trainer_battle = False
    trainer_name = None
    trainer_team = []
    trainer_index = 0
    game_mode = "world"
    return True


def check_trainer_encounter():
    for name, trainer in TRAINERS.items():
        if trainer["map"] == current_map and trainer["x"] == player_x and trainer["y"] == player_y and name not in trainer_defeated:
            start_trainer_battle(name)
            return


def move_player(dx, dy):
    global player_x, player_y, current_map
    nx, ny = player_x + dx, player_y + dy
    if not can_walk(nx, ny):
        return
    player_x, player_y = nx, ny
    transitions = [
        ("town", 7, 9, "route1", 7, 1, "Você entrou na Rota 1!"),
        ("route1", 7, 1, "town", 7, 8, "Você voltou para a cidade inicial."),
        ("route1", 8, 1, "route2", 8, 10, "Você chegou à Rota 2!"),
        ("route2", 8, 10, "route1", 8, 1, "Você voltou para a Rota 1."),
        ("route2", 8, 1, "town2", 8, 10, "Você chegou à cidade do primeiro ginásio!"),
        ("town2", 8, 10, "route2", 8, 1, "Você voltou para a Rota 2."),
        ("town2", 14, 6, "route3", 1, 6, "Você entrou na Rota 3!"),
        ("route3", 1, 6, "town2", 14, 6, "Você voltou para a cidade."),
        ("route3", 7, 1, "gymtown", 7, 10, "Você chegou à cidade do ginásio!"),
        ("gymtown", 7, 10, "route3", 7, 1, "Você voltou para a Rota 3."),
    ]
    for a, ax, ay, b, bx, by, msg in transitions:
        if current_map == a and player_x == ax and player_y == ay:
            current_map, player_x, player_y = b, bx, by
            show_message(msg)
            return
    if current_map == "gymtown" and (player_x, player_y) == (7, 8) and not story_flags["gym_leader_defeated"]:
        current_map, player_x, player_y = "gym", 7, 10
        show_message("Você entrou no Ginásio!")
        return
    if current_map == "gym" and (player_x, player_y) == (7, 10):
        current_map, player_x, player_y = "gymtown", 7, 8
        show_message("Você saiu do Ginásio.")
        return
    check_trainer_encounter()
    if current_map in ["route1", "route2", "route3"] and get_map()[player_y][player_x] == "G" and random.random() < 0.12:
        start_battle()


def calculate_damage(attacker, defender, move_name):
    return calculate_battle_damage(attacker, defender, move_name, MOVE_DATA, TYPE_EFFECTIVENESS)


def get_enemy():
    return trainer_current() if trainer_battle else battle_enemy_obj


def sync_enemy_hp():
    global battle_enemy_hp, trainer_enemy_hp
    enemy = get_enemy()
    if enemy is None: return
    if trainer_battle: trainer_enemy_hp = enemy["hp"]
    else: battle_enemy_hp = enemy["hp"]


def defeat_player():
    global game_mode, current_map, player_x, player_y, active_index
    if first_alive() != -1:
        return False
    heal_party()
    active_index = 0
    current_map = "gymtown" if current_map == "gym" else "town"
    player_x, player_y = (3, 4) if current_map == "gymtown" else (7, 8)
    show_message("Você desmaiou e voltou ao Centro Pokémon. Sua equipe foi curada!")
    game_mode = "world"
    return True


def execute_attack(attacker, defender, move_name, is_player):
    if not status_can_act(attacker):
        return defender["hp"] > 0
    result = calculate_damage(attacker, defender, move_name)
    if result[0] is None:
        show_message(result[3]); return True
    damage, eff, crit, text = result
    defender["hp"] = max(0, defender["hp"] - damage)
    msg = attacker["name"] + " usou " + move_name + "! " + ("Dano: " + str(damage) + "." if damage else "") + text
    show_message(msg)
    return defender["hp"] > 0


def finish_enemy_defeat():
    global game_mode, battle_enemy_obj, battle_enemy_hp, trainer_enemy_hp
    own = party[first_alive()]
    enemy = get_enemy()
    if enemy is None: return
    xp = (25 + enemy["level"] * 10) if trainer_battle else (20 + enemy["level"] * 8)
    gain_xp(own, xp)
    if trainer_battle:
        defeated_name = trainer_name
        if advance_trainer_after_defeat():
            if defeated_name == "Rita Lee":
                show_message("Você venceu o primeiro Ginásio! Recebeu a Insígnia Erva!")
                game_mode = "world"
                globals()["current_map"] = "gym"
                globals()["player_x"] = 7
                globals()["player_y"] = 10
            else:
                show_message(defeated_name + " foi derrotado! Recebeu $" + str(trainer_reward(defeated_name)) + ".")
        else:
            show_message(trainer_name + " enviou outro Pokémon!")
    else:
        show_message(enemy["name"] + " foi derrotado! " + own["name"] + " ganhou " + str(xp) + " EXP.")
        game_mode = "world"
        battle_enemy_obj = None


def player_attack(move_index, auto_enemy=True):
    global battle_state
    idx = first_alive()
    if idx == -1: return
    own = party[idx]
    if move_index >= len(own["moves"]): return
    enemy = get_enemy()
    if enemy is None or enemy.get("hp", 0) <= 0:
        battle_state = "menu"
        return
    move_name = own["moves"][move_index]

    if not auto_enemy:
        if not status_can_act(own):
            return
        alive = execute_attack(own, enemy, move_name, True)
        sync_enemy_hp()
        if not alive:
            finish_enemy_defeat()
            return
        if own["hp"] <= 0:
            defeat_player()
        return

    player_speed = own["speed"]
    enemy_speed = enemy["speed"]
    if player_speed >= enemy_speed:
        alive = execute_attack(own, enemy, move_name, True)
        sync_enemy_hp()
        if not alive:
            finish_enemy_defeat(); return
        status_msg = apply_end_turn_status(enemy)
        if status_msg: show_message(status_msg)
        if enemy["hp"] <= 0: finish_enemy_defeat(); return
        enemy_move = random.choice(enemy["moves"])
        if execute_attack(enemy, own, enemy_move, False):
            status_msg = apply_end_turn_status(own)
            if status_msg: show_message(status_msg)
        sync_enemy_hp()
    else:
        enemy_move = random.choice(enemy["moves"])
        alive = execute_attack(enemy, own, enemy_move, False)
        if not alive or own["hp"] <= 0:
            if defeat_player(): return
        status_msg = apply_end_turn_status(own)
        if status_msg: show_message(status_msg)
        if own["hp"] <= 0:
            if defeat_player(): return
        alive = execute_attack(own, enemy, move_name, True)
        sync_enemy_hp()
        if not alive:
            finish_enemy_defeat(); return
        status_msg = apply_end_turn_status(enemy)
        if status_msg: show_message(status_msg)
        if enemy["hp"] <= 0: finish_enemy_defeat(); return
    if own["hp"] <= 0:
        defeat_player()
    battle_state = "menu"


def enemy_attack(move_name=None):
    enemy = get_enemy()
    idx = first_alive()
    if enemy is None or idx == -1: return
    own = party[idx]
    move = move_name or random.choice(enemy["moves"])
    execute_attack(enemy, own, move, False)
    if own["hp"] <= 0:
        show_message(own["name"] + " desmaiou!")
        defeat_player()


def try_capture():
    global pokeballs, game_mode, battle_enemy_obj
    if trainer_battle:
        show_message("Você não pode capturar Pokémon de um treinador!"); return
    if pokeballs <= 0:
        show_message("Você não tem Pokébolas!"); return
    if len(party) >= 6:
        show_message("Sua equipe está cheia!"); return
    pokeballs -= 1
    enemy = battle_enemy_obj
    hp_factor = 1 - (enemy["hp"] / enemy["max_hp"])
    status_bonus = 1.35 if enemy["status"] != "Normal" else 1.0
    chance = (0.18 + hp_factor * 0.55) * status_bonus
    chance = min(0.90, chance)
    if random.random() < chance:
        party.append(enemy)
        pokedex.add(enemy["name"])
        show_message(enemy["name"] + " foi capturado!")
        game_mode = "world"
        battle_enemy_obj = None
    else:
        show_message("A Pokébola falhou!")
        enemy_attack()


def battle_switch():
    global party_cursor, battle_state
    alive = [i for i,p in enumerate(party) if p["hp"] > 0 and i != first_alive()]
    if not alive:
        show_message("Você não tem outro Pokémon disponível!"); return
    party_cursor = alive[0]
    battle_state = "switch"


def perform_switch(index):
    global active_index, battle_state, forced_switch
    if index < 0 or index >= len(party) or party[index]["hp"] <= 0:
        show_message("Esse Pokémon não pode entrar em batalha!"); return
    if index == active_index:
        show_message("Esse Pokémon já está em batalha!"); return
    was_forced = forced_switch
    active_index = index
    forced_switch = False
    battle_state = "menu"
    show_message("Vai, " + party[index]["name"] + "!")
    if not was_forced:
        enemy_attack()


def use_item(item_name):
    global game_mode
    idx = first_alive()
    if item_name == "Poção":
        if items.get("Poção", 0) <= 0: show_message("Você não tem Poções!"); return
        target = party[idx]
        if target["hp"] >= target["max_hp"]: show_message("O HP já está cheio!"); return
        target["hp"] = min(target["max_hp"], target["hp"] + 20)
        items["Poção"] -= 1
        show_message(target["name"] + " recuperou 20 HP!")
    elif item_name == "Super Poção":
        if items.get("Super Poção", 0) <= 0: show_message("Você não tem Super Poções!"); return
        target = party[idx]
        if target["hp"] >= target["max_hp"]: show_message("O HP já está cheio!"); return
        target["hp"] = min(target["max_hp"], target["hp"] + 50)
        items["Super Poção"] -= 1
        show_message(target["name"] + " recuperou 50 HP!")
    elif item_name == "Antídoto":
        if items.get("Antídoto", 0) <= 0: show_message("Você não tem Antídotos!"); return
        target = party[idx]
        if target["status"] != "Envenenado": show_message("Nenhum veneno para curar!"); return
        target["status"] = "Normal"
        items["Antídoto"] -= 1
        show_message("O veneno foi curado!")


def save_game():
    data = {
        "current_map": current_map, "player_x": player_x, "player_y": player_y,
        "party": party, "pokeballs": pokeballs, "money": money, "pokedex": list(pokedex),
        "badges": badges, "trainer_defeated": list(trainer_defeated), "story_flags": story_flags,
        "items": items, "active_index": active_index,
    }
    try:
        SAVE_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        show_message("Jogo salvo!")
    except Exception as exc:
        show_message("Erro ao salvar: " + str(exc)[:45])


def load_game():
    global current_map, player_x, player_y, party, pokeballs, money, pokedex, badges, trainer_defeated, story_flags, items, active_index, game_mode
    if not SAVE_FILE.exists():
        show_message("Nenhum save encontrado!"); return
    try:
        data = json.loads(SAVE_FILE.read_text(encoding="utf-8"))
        current_map = data.get("current_map", "town")
        player_x, player_y = data.get("player_x", 6), data.get("player_y", 7)
        party = data.get("party", [])
        pokeballs = data.get("pokeballs", 5)
        money = data.get("money", 300)
        pokedex = set(data.get("pokedex", []))
        badges = data.get("badges", 0)
        trainer_defeated = set(data.get("trainer_defeated", []))
        story_flags.update(data.get("story_flags", {}))
        items.update(data.get("items", {}))
        active_index = data.get("active_index", 0)
        game_mode = "world"
        show_message("Jogo carregado!")
    except Exception as exc:
        show_message("Save inválido: " + str(exc)[:45])


def interact_world():
    # Professor
    if current_map == "town" and abs(player_x - 5) <= 1 and abs(player_y - 5) <= 1:
        if not party:
            globals()["game_mode"] = "starter"
            show_message(BRASAR_REGION_INFO["story_intro"])
        else:
            show_message("Prof. Jatobá: Explore a região e registre novos Pokémon em Brasar!")
        return
    # Centro Pokémon: funciona em todas as cidades através do prédio marcado pela área.
    center_positions = {
        "town": (3, 2), "town2": (3, 2), "gymtown": (3, 2)
    }
    if current_map in center_positions:
        cx, cy = center_positions[current_map]
        if abs(player_x - cx) <= 1 and abs(player_y - cy) <= 1:
            heal_party(); show_message("Centro Pokémon: sua equipe foi totalmente curada!"); return
    # PokéMart na cidade do ginásio.
    if current_map == "town2" and abs(player_x - 11) <= 1 and abs(player_y - 2) <= 1:
        globals()["game_mode"] = "shop"; return
    # Ginásio pela porta.
    if current_map == "gymtown" and (player_x, player_y) == (7, 8):
        if story_flags["gym_leader_defeated"]:
            show_message("O Ginásio já foi conquistado!")
        else:
            globals()["current_map"] = "gym"; globals()["player_x"] = 7; globals()["player_y"] = 10
            show_message("Você entrou no Ginásio!")


def draw_map():
    mapa = get_map()
    screen.fill((92, 160, 84))
    for y,row in enumerate(mapa):
        for x,tile in enumerate(row):
            rect=pygame.Rect(x*TILE,y*TILE,TILE,TILE)
            if tile=="#":
                pygame.draw.rect(screen,(56, 106, 58),rect)
                draw_tree(rect)
            elif tile==".":
                pygame.draw.rect(screen,(196, 172, 121),rect)
            elif tile=="G":
                pygame.draw.rect(screen,(111, 180, 95),rect)
                pygame.draw.line(screen,(76, 126, 69),(rect.x+12,rect.bottom-6),(rect.x+16,rect.y+22),3)
                pygame.draw.line(screen,(76, 126, 69),(rect.x+30,rect.bottom-6),(rect.x+34,rect.y+24),3)
            elif tile=="H":
                draw_house(rect)
            elif tile=="D":
                pygame.draw.rect(screen,(86, 149, 222),rect)
            elif tile=="N":
                pygame.draw.rect(screen,(209, 178, 112),rect)
            elif tile=="T":
                pygame.draw.rect(screen,(169,135,173),rect)
                pygame.draw.rect(screen,(122, 92, 141),rect,3)
            elif tile=="C":
                pygame.draw.rect(screen,(254, 250, 243),rect)
                pygame.draw.rect(screen,(200, 70, 70),(rect.x+4,rect.y+10,40,28))
                pygame.draw.circle(screen,(255,255,255),(rect.x+24,rect.y+24),8)
                draw_text("P",rect.x+19,rect.y+16,SMALL,(200,70,70))
            elif tile=="S":
                pygame.draw.rect(screen,(225,220,160),rect)
                pygame.draw.rect(screen,(70, 112, 196),(rect.x+9,rect.y+13,30,27))
                draw_text("$",rect.x+19,rect.y+16,SMALL,(255,255,255))
            pygame.draw.rect(screen,(80,80,70),rect,1)
    if current_map in ["town","town2","gymtown"]:
        cx,cy = (3,2)
        pygame.draw.rect(screen,(250,250,245),(cx*TILE+3,cy*TILE+10,42,30))
        pygame.draw.rect(screen,(200,70,70),(cx*TILE+3,cy*TILE+10,42,30),3)
        draw_text("C",cx*TILE+18,cy*TILE+15,SMALL,(200,70,70))
    if current_map=="town2":
        sx,sy=11,2
        pygame.draw.rect(screen,(80,120,220),(sx*TILE+3,sy*TILE+10,42,30))
        draw_text("SHOP",sx*TILE-4,sy*TILE-4,SMALL,(255,255,255))
    if current_map=="gymtown":
        pygame.draw.rect(screen,(125, 85, 150),(6*TILE+5,8*TILE+18,38,25))
        pygame.draw.polygon(screen,(105,55,135),[(6*TILE+2,8*TILE+20),(6*TILE+24,8*TILE+2),(6*TILE+46,8*TILE+20)])
        draw_text("GINÁSIO",5*TILE+5,8*TILE-5,SMALL,(255,255,255))
    for name,t in TRAINERS.items():
        if t["map"]==current_map and name not in trainer_defeated:
            draw_character(t["x"]*TILE+24,t["y"]*TILE+24,PURPLE if t.get("leader") else RED)
    title={"route1":"ROTA 1","route2":"ROTA 2","route3":"ROTA 3","gymtown":"CIDADE DO PRIMEIRO GINÁSIO","gym":"GINÁSIO VENENOSO"}.get(current_map,"CIDADE INICIAL")
    pygame.draw.rect(screen,(18, 35, 28),(8,8,250,28),2)
    draw_text(title,18,12,SMALL,(255,255,255))
    draw_text("Insígnias: "+str(badges),600,12,SMALL,(255,255,255))
    draw_character(player_x*TILE+24,player_y*TILE+24,BLUE)


def draw_battle():
    screen.fill((220,235,205))
    idx=first_alive(); own=party[idx] if idx>=0 else None; enemy=get_enemy()
    pygame.draw.ellipse(screen,GREEN,(430,110,280,90)); pygame.draw.ellipse(screen,GREEN,(55,335,300,95))
    if enemy: draw_big_pokemon(enemy["name"],565,155)
    if own: draw_big_pokemon(own["name"],205,375)
    if enemy:
        pygame.draw.rect(screen,WHITE,(35,35,350,125)); pygame.draw.rect(screen,BLACK,(35,35,350,125),3)
        label=(trainer_name+": " if trainer_battle else "")+enemy["name"]
        draw_text(label+" Nv."+str(enemy["level"]),55,50); draw_text(enemy["type"],55,78,SMALL); draw_hp_bar(55,108,270,enemy["hp"],enemy["max_hp"]); draw_text("Status: "+enemy["status"],55,130,SMALL)
    if own:
        pygame.draw.rect(screen,WHITE,(390,270,340,145)); pygame.draw.rect(screen,BLACK,(390,270,340,145),3)
        draw_text(own["name"]+" Nv."+str(own["level"]),410,285); draw_text(own["type"],410,313,SMALL); draw_hp_bar(410,340,250,own["hp"],own["max_hp"]); draw_text(str(own["hp"])+"/"+str(own["max_hp"]),590,365,SMALL); draw_text("Status: "+own["status"],410,388,SMALL)
        ratio=own["xp"]/max(1,own["xp_to_next"]); pygame.draw.rect(screen,BLACK,(410,405,250,8)); pygame.draw.rect(screen,BLUE,(412,407,int(246*ratio),4))
    pygame.draw.rect(screen,WHITE,(0,450,WIDTH,126)); pygame.draw.rect(screen,BLACK,(0,450,WIDTH,126),4)
    if battle_state=="menu":
        for i,opt in enumerate(["LUTAR","POKÉMON","MOCHILA","FUGIR"]):
            x=70+(i%2)*330; y=465+(i//2)*48
            if battle_cursor==i: draw_text(">",x-25,y)
            draw_text(opt,x,y)
    elif battle_state=="fight":
        active=party[first_alive()];
        for i in range(4):
            x=60+(i%2)*330; y=465+(i//2)*45
            if i<len(active["moves"]):
                if battle_cursor==i: draw_text(">",x-25,y)
                m=active["moves"][i]; pp=active.get("move_pp",{}).get(m,MOVE_DATA.get(m,{"pp":0})["pp"]); draw_text(m+" PP "+str(pp),x,y)
            else: draw_text("---",x,y)


def draw_bag_screen():
    screen.fill((180,205,175)); pygame.draw.rect(screen,WHITE,(130,55,508,465)); pygame.draw.rect(screen,BLACK,(130,55,508,465),4); draw_text("MOCHILA",315,75,BIG)
    draw_text("Pokébolas: "+str(pokeballs),180,145); draw_text("Poções: "+str(items.get("Poção",0)),180,190); draw_text("Super Poções: "+str(items.get("Super Poção",0)),180,235); draw_text("Antídotos: "+str(items.get("Antídoto",0)),180,280); draw_text("Dinheiro: $"+str(money),180,325); draw_text("ENTER = usar Poção",180,380,SMALL); draw_text("ESC = voltar",180,430,SMALL)


def draw_shop():
    screen.fill((205,215,190)); pygame.draw.rect(screen,WHITE,(150,60,468,460)); pygame.draw.rect(screen,BLACK,(150,60,468,460),4); draw_text("POKÉMART",315,80,BIG)
    goods=[("Pokébola",200),("Poção",300),("Antídoto",100)]
    for i,(name,price) in enumerate(goods):
        y=160+i*75
        if shop_cursor==i: draw_text(">",205,y)
        draw_text(name+" - $"+str(price),240,y)
    draw_text("Dinheiro: $"+str(money),240,390); draw_text("ENTER = comprar   ESC = sair",210,450,SMALL)


def handle_menu_key(key):
    global game_mode, menu_cursor
    if key==pygame.K_UP: menu_cursor=(menu_cursor-1)%6
    elif key==pygame.K_DOWN: menu_cursor=(menu_cursor+1)%6
    elif key in [pygame.K_RETURN,pygame.K_z,pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5,pygame.K_6]:
        nums={pygame.K_1:0,pygame.K_2:1,pygame.K_3:2,pygame.K_4:3,pygame.K_5:4,pygame.K_6:5}
        if key in nums: menu_cursor=nums[key]
        modes=["party","pokedex","bag","save","load","world"]
        if menu_cursor==3: save_game()
        elif menu_cursor==4: load_game()
        else: game_mode=modes[menu_cursor]
    elif key in [pygame.K_ESCAPE,pygame.K_x]: game_mode="world"


def draw_menu():
    screen.fill((180,205,175)); pygame.draw.rect(screen,WHITE,(130,35,508,505)); pygame.draw.rect(screen,BLACK,(130,35,508,505),4); draw_text("MENU",345,55,BIG)
    opts=["POKÉMON","POKÉDEX","MOCHILA","SALVAR","CARREGAR","VOLTAR"]
    for i,opt in enumerate(opts):
        y=125+i*55
        if menu_cursor==i: draw_text(">",205,y)
        draw_text(opt,245,y)
    draw_text("Pokébolas: "+str(pokeballs),245,455,SMALL); draw_text("Dinheiro: $"+str(money),430,455,SMALL); draw_text("Insígnias: "+str(badges),245,485,SMALL)


def handle_party_key(key):
    global party_cursor,game_mode
    if key==pygame.K_UP: party_cursor=max(0,party_cursor-1)
    elif key==pygame.K_DOWN: party_cursor=min(max(0,len(party)-1),party_cursor+1)
    elif key in [pygame.K_ESCAPE,pygame.K_x]: game_mode="menu"


def handle_battle_key(key):
    global battle_state,battle_cursor,party_cursor,game_mode
    if battle_state=="menu":
        if key==pygame.K_UP: battle_cursor=(battle_cursor-1)%4
        elif key==pygame.K_DOWN: battle_cursor=(battle_cursor+1)%4
        elif key==pygame.K_LEFT and battle_cursor%2: battle_cursor-=1
        elif key==pygame.K_RIGHT and battle_cursor%2==0: battle_cursor+=1
        elif key in [pygame.K_RETURN,pygame.K_z]:
            if battle_cursor==0: battle_state="fight"; battle_cursor=0
            elif battle_cursor==1: battle_switch()
            elif battle_cursor==2: use_item("Poção")
            elif battle_cursor==3:
                if trainer_battle: show_message("Você não pode fugir de uma batalha de treinador!")
                elif random.random()<0.85: game_mode="world"; show_message("Você fugiu!")
                else: show_message("Você não conseguiu fugir!"); enemy_attack()
    elif battle_state=="fight":
        moves=party[first_alive()]["moves"]
        if key==pygame.K_LEFT and battle_cursor%2: battle_cursor-=1
        elif key==pygame.K_RIGHT and battle_cursor%2==0: battle_cursor+=1
        elif key==pygame.K_UP: battle_cursor=max(0,battle_cursor-2)
        elif key==pygame.K_DOWN: battle_cursor=min(3,battle_cursor+2)
        elif key in [pygame.K_RETURN,pygame.K_z]:
            if battle_cursor<len(moves): player_attack(battle_cursor)
        elif key in [pygame.K_ESCAPE,pygame.K_x]: battle_state="menu"; battle_cursor=0
    elif battle_state=="switch":
        if key==pygame.K_UP: party_cursor=max(0,party_cursor-1)
        elif key==pygame.K_DOWN: party_cursor=min(max(0,len(party)-1),party_cursor+1)
        elif key in [pygame.K_RETURN,pygame.K_z]: perform_switch(party_cursor)
        elif key in [pygame.K_ESCAPE,pygame.K_x]: battle_state="menu"


def handle_shop_key(key):
    global shop_cursor,money,pokeballs,game_mode
    goods=[("Pokébola",200),("Poção",300),("Antídoto",100)]
    if key==pygame.K_UP: shop_cursor=(shop_cursor-1)%3
    elif key==pygame.K_DOWN: shop_cursor=(shop_cursor+1)%3
    elif key in [pygame.K_RETURN,pygame.K_z]:
        name,price=goods[shop_cursor]
        if money<price: show_message("Dinheiro insuficiente!"); return
        money-=price
        if name=="Pokébola": pokeballs+=1
        else: items[name]=items.get(name,0)+1
        show_message(name+" comprado!")
    elif key in [pygame.K_ESCAPE,pygame.K_x]: game_mode="world"


def talk():
    interact_world()


# ============================================================
# POKÉMON BRASAR - V6
# Expansão baseada na Enciclopédia Mestra fornecida pelo usuário.
# Progressão completa: 10 ginásios -> Área Zero -> Elite 4 -> Campeã.
# ============================================================

V6_MAPS = {
    "guarany": [
        "################", "#..............#", "#..CC....SS....#", "#..CC....SS....#",
        "#..............#", "#.....AA.......#", "#..............#", "#..............#",
        "#..............#", "#......D.......#", "#..............#", "################"],
    "route1v6": [
        "################", "#GGGG....GGGG..#", "#GGGG....GGGG..#", "#......TT......#",
        "#..............#", "#....GGGG......#", "#....GGGG......#", "#..............#",
        "#..............#", "#GG......GG....#", "#..............#", "################"],
    "amazon": [
        "################", "#..............#", "#..CC....SS....#", "#..CC....SS....#",
        "#..............#", "#....GGGG......#", "#....GGGG......#", "#..............#",
        "#......TT......#", "#..............#", "#..............#", "################"],
    "route2v6": [
        "################", "#GGG......GGG..#", "#GGG......GGG..#", "#....TT........#",
        "#..............#", "#......DDDD....#", "#......DDDD....#", "#..............#",
        "#....GGGG......#", "#..............#", "#..............#", "################"],
    "akre": [
        "################", "#..............#", "#..CC....SS....#", "#..CC....SS....#",
        "#......GG......#", "#......GG......#", "#....TT........#", "#..............#",
        "#..............#", "#......AA......#", "#..............#", "################"],
    "route3v6": [
        "################", "#GGGG..........#", "#GGGG..........#", "#......TT......#",
        "#..........GGGG#", "#..........GGGG#", "#..............#", "#....DDDD......#",
        "#....DDDD......#", "#..............#", "#..............#", "################"],
    "cuiabee": [
        "################", "#..............#", "#..CC....SS....#", "#..CC....SS....#",
        "#..............#", "#..GGGG........#", "#..GGGG........#", "#......TT......#",
        "#..............#", "#..............#", "#..............#", "################"],
    "route4v6": [
        "################", "#....GGGG......#", "#....GGGG......#", "#......TT......#",
        "#..............#", "#......GGGG....#", "#......GGGG....#", "#..............#",
        "#..DD..........#", "#..DD..........#", "#..............#", "################"],
    "blumenice": [
        "################", "#..............#", "#..CC....SS....#", "#..CC....SS....#",
        "#....GGGG......#", "#....GGGG......#", "#......TT......#", "#..............#",
        "#..............#", "#......AA......#", "#..............#", "################"],
    "route5v6": [
        "################", "#GGGG....GGGG..#", "#GGGG....GGGG..#", "#......TT......#",
        "#..............#", "#....GGGG......#", "#....GGGG......#", "#..............#",
        "#......DD......#", "#......DD......#", "#..............#", "################"],
    "saintpaul": [
        "################", "#..............#", "#..CC....SS....#", "#..CC....SS....#",
        "#....GG........#", "#....GG........#", "#......TT......#", "#..............#",
        "#..............#", "#......AA......#", "#..............#", "################"],
    "route6v6": [
        "################", "#......GGGG....#", "#......GGGG....#", "#....TT........#",
        "#..............#", "#....GGGG......#", "#....GGGG......#", "#..............#",
        "#..DD..........#", "#..DD..........#", "#..............#", "################"],
    "ryo": [
        "################", "#..............#", "#..CC....SS....#", "#..CC....SS....#",
        "#......GG......#", "#......GG......#", "#......TT......#", "#..............#",
        "#..............#", "#......AA......#", "#..............#", "################"],
    "route7v6": [
        "################", "#GGGG..........#", "#GGGG..........#", "#......TT......#",
        "#..........GGGG#", "#..........GGGG#", "#..............#", "#....GGGG......#",
        "#....GGGG......#", "#..............#", "#..............#", "################"],
    "turmalina": [
        "################", "#..............#", "#..CC....SS....#", "#..CC....SS....#",
        "#..AAAA........#", "#..AAAA........#", "#......TT......#", "#..............#",
        "#......AA......#", "#..............#", "#..............#", "################"],
    "route8v6": [
        "################", "#......GGGG....#", "#......GGGG....#", "#....TT........#",
        "#..............#", "#GGGG..........#", "#GGGG..........#", "#..............#",
        "#......DDDD....#", "#......DDDD....#", "#..............#", "################"],
    "soulvior": [
        "################", "#..............#", "#..CC....SS....#", "#..CC....SS....#",
        "#....GGGG......#", "#....GGGG......#", "#......TT......#", "#..............#",
        "#..............#", "#......AA......#", "#..............#", "################"],
    "route9v6": [
        "################", "#GGGG..........#", "#GGGG..........#", "#......TT......#",
        "#..............#", "#......GGGG....#", "#......GGGG....#", "#..............#",
        "#..DD..........#", "#..DD..........#", "#..............#", "################"],
    "olynda": [
        "################", "#..............#", "#..CC....SS....#", "#..CC....SS....#",
        "#......GG......#", "#......GG......#", "#......TT......#", "#..............#",
        "#..............#", "#......AA......#", "#..............#", "################"],
    "route10v6": [
        "################", "#......GGGG....#", "#......GGGG....#", "#....TT........#",
        "#..............#", "#....GGGG......#", "#....GGGG......#", "#..............#",
        "#......DDDD....#", "#......DDDD....#", "#..............#", "################"],
    "fortress": [
        "################", "#..............#", "#..CC....SS....#", "#..CC....SS....#",
        "#....AAAA......#", "#....AAAA......#", "#......TT......#", "#..............#",
        "#......AA......#", "#..............#", "#..............#", "################"],
    "area_zero": [
        "################", "#GGGGGGGGGGGG..#", "#GGGGGGGGGGGG..#", "#....TT........#",
        "#..DDDDDDDD....#", "#..DDDDDDDD....#", "#..............#", "#....GGGGGG....#",
        "#....GGGGGG....#", "#..............#", "#..............#", "################"],
    "league": [
        "################", "#..............#", "#..LLLLLLLLLL..#", "#..L........L..#",
        "#..L....TT..L..#", "#..L........L..#", "#..L....AA..L..#", "#..L........L..#",
        "#..LLLLLLLLLL..#", "#..............#", "#..............#", "################"],
}

CITY_NAMES = {
    "guarany":"Guarany Town", "amazon":"Amazon City", "akre":"Akre City", "cuiabee":"Cuiabee City",
    "blumenice":"Blumenice City", "saintpaul":"SaintPaul City", "ryo":"Ryo City", "turmalina":"Turmalina City",
    "soulvior":"Soulvior City", "olynda":"Olynda City", "fortress":"Fortress City", "area_zero":"Área Zero", "league":"Liga Pokémon"
}

BRASAR_PROFILE = {
    "region_name": "Região de Brasar",
    "subtitle": "Uma terra inspirada na cultura, fauna e flora do Brasil",
    "founder": "DiguiDex",
    "legend": "O Rei de Brasar",
    "story": "A jornada em Brasar passa por cidades, rotas, biomas e líderes regionais. O coração da região é comandado por DiguiDex, cuja equipe representa a força e a diversidade da própria terra.",
    "biomes": ["Mata Atlântica", "Cerrado", "Pantanal", "Amazônia", "Serras"],
    "bosses": ["Rita Lee", "Anitta", "Milton", "Gonzaga", "DiguiDex"]
}

BRASAR_CITY_FLOW = [
    {"city": "guarany", "name": "Guarany Town", "role": "inicial", "leader": None, "story": "A cidade inicial, o ponto de partida da jornada em Brasar."},
    {"city": "amazon", "name": "Amazon City", "role": "cidade", "leader": "Victorya da Matta", "story": "Uma cidade marcada por floresta, cultura e o primeiro grande teste regional."},
    {"city": "akre", "name": "Akre City", "role": "cidade", "leader": "Xuxa", "story": "Akre representa desafio mental, mistério e disciplina regional."},
    {"city": "cuiabee", "name": "Cuiabee City", "role": "cidade", "leader": "Marília", "story": "Uma cidade vibrante de mercado, tradição e espírito competitivo."},
    {"city": "blumenice", "name": "Blumenice City", "role": "cidade", "leader": "Luisa", "story": "A jornada se torna mais dura e a região exige preparo melhor."},
    {"city": "saintpaul", "name": "SaintPaul City", "role": "cidade", "leader": "Rita Lee", "story": "O caminho do ginásio exige força, variedade e controle da própria equipe."},
    {"city": "ryo", "name": "Ryo City", "role": "cidade", "leader": "Anitta", "story": "As lutas ganham calor, brilho e pressão na rota de elite."},
    {"city": "turmalina", "name": "Turmalina City", "role": "cidade", "leader": "Milton", "story": "A cidade dos minerais e do esgotamento físico."},
    {"city": "soulvior", "name": "Soulvior City", "role": "cidade", "leader": "Alcione", "story": "Aqui a região entra em um nível mais tenso e sombrio."},
    {"city": "olynda", "name": "Olynda City", "role": "cidade", "leader": "Tim", "story": "A cidade das águas e do último empurrão para a fase final."},
    {"city": "fortress", "name": "Fortress City", "role": "cidade", "leader": "Gonzaga", "story": "A última cidade antes da Liga, onde a força da região se concentra."},
    {"city": "league", "name": "Liga de Brasar", "role": "final", "leader": "DiguiDex", "story": "O ápice da jornada: a liga e o confronto final contra o rei de Brasar."},
]

BRASAR_REGION_INFO = {
    "region_name": "Região de Brasar",
    "subtitle": "Inspirada na fauna, flora, cidades e biomas do Brasil",
    "starter_city": "Guarany Town",
    "biomes": ["Mata Atlântica", "Cerrado", "Pantanal", "Amazônia", "Serras"],
    "featured_pokemon": [
        "Macarim", "Flaguar", "Suriqua", "Perigreen", "Canarin",
        "Vulpix de Brasar", "Victeed", "Roserade", "Mismagius",
        "Gigarucu", "Dubwool de Brasar", "Cacturne de Brasar",
        "Kuckagron"
    ],
    "cities": [
        "Guarany Town", "Amazon City", "Akre City", "Cuiabee City",
        "Blumenice City", "SaintPaul City", "Ryo City", "Turmalina City",
        "Soulvior City", "Olynda City", "Fortress City"
    ],
    "story_intro": "Bem-vindo(a) à Região de Brasar, um mundo inspirado na cultura, fauna e flora do Brasil. Cada cidade traz um pedaço desse território, e cada rota guarda desafios únicos, bichos regionais e mistérios que só a aventura de Brasar pode revelar."
}

GYMS = [
    {"leader":"Victorya da Matta","city":"amazon","type":"Grama","badge":"Clover Badge","level":20,"team":["Vulpix de Brasar","Victeed"],"reward":1400},
    {"leader":"Xuxa","city":"akre","type":"Psíquico","badge":"Acre Badge","level":25,"team":["Smoochum","Varlien"],"reward":1800},
    {"leader":"Marília","city":"cuiabee","type":"Normal","badge":"Simple Badge","level":35,"team":["Loudred","Eeveeon","Miltank"],"reward":2500},
    {"leader":"Luisa","city":"blumenice","type":"Gelo","badge":"Cold Badge","level":40,"team":["Caxinguelice","Froslass","Guarartic"],"reward":3000},
    {"leader":"Rita Lee","city":"saintpaul","type":"Veneno","badge":"Poisonous Badge","level":45,"team":["Murizika","Roserade","Tamantox","Toxtricity"],"reward":3500},
    {"leader":"Anitta","city":"ryo","type":"Fogo","badge":"Heat Badge","level":50,"team":["Pepperim","Magmar","Houndoom","Salazzle"],"reward":4200},
    {"leader":"Milton","city":"turmalina","type":"Pedra","badge":"Mine Badge","level":55,"team":["Carbink","Rockeon","Jaduitan","Briganite"],"reward":5000},
    {"leader":"Alcione","city":"soulvior","type":"Fantasma","badge":"Ebony Badge","level":60,"team":["Mismagius","Carrangrigus","Bumboi"],"reward":5800},
    {"leader":"Tim","city":"olynda","type":"Água","badge":"Water Badge","level":65,"team":["Gigarucu","Vaporeon","Azumarill","Sirenatee","Wailord"],"reward":6500},
    {"leader":"Gonzaga","city":"fortress","type":"Aço","badge":"Accordion Badge","level":70,"team":["Bastiodon","Dubwool de Brasar","Skarmory","Cabrooat","Cacturne de Brasar","Metagross"],"reward":7500},
]

BRASAR_PROGRESS_SEQUENCE = [
    ("Amazon City", "Victorya da Matta", "Clover Badge"),
    ("Akre City", "Xuxa", "Acre Badge"),
    ("Cuiabee City", "Marília", "Simple Badge"),
    ("Blumenice City", "Luisa", "Cold Badge"),
    ("SaintPaul City", "Rita Lee", "Poisonous Badge"),
    ("Ryo City", "Anitta", "Heat Badge"),
    ("Turmalina City", "Milton", "Mine Badge"),
    ("Soulvior City", "Alcione", "Ebony Badge"),
    ("Olynda City", "Tim", "Water Badge"),
    ("Fortress City", "Gonzaga", "Accordion Badge"),
]

BRASAR_CITY_ROUTE_GATES = {
    "amazon": ("route2v6", "Victorya da Matta"),
    "akre": ("route3v6", "Xuxa"),
    "cuiabee": ("route4v6", "Marília"),
    "blumenice": ("route5v6", "Luisa"),
    "saintpaul": ("route6v6", "Rita Lee"),
    "ryo": ("route7v6", "Anitta"),
    "turmalina": ("route8v6", "Milton"),
    "soulvior": ("route9v6", "Alcione"),
    "olynda": ("route10v6", "Tim"),
    "fortress": ("area_zero", "Gonzaga"),
}


def can_leave_city(city, target):
    gate = BRASAR_CITY_ROUTE_GATES.get(city)
    return not gate or gate[0] != target or gate[1] in trainer_defeated


def next_regional_gym():
    for _, leader, _ in BRASAR_PROGRESS_SEQUENCE:
        gym = next(gym for gym in GYMS if gym["leader"] == leader)
        if leader not in trainer_defeated:
            return gym
    return None


def regional_progress_complete():
    return next_regional_gym() is None

ELITE4 = [
    {"leader":"Fernanda Torres","type":"Psíquico","level":74,"team":["Varlien","Guaramite","Mr. Momo","Phanteon"],"reward":9000},
    {"leader":"Ivete","type":"Terra","level":76,"team":["Earthdog","Mandimole","Braipim","Armordillo"],"reward":9500},
    {"leader":"Alok","type":"Elétrico","level":78,"team":["Canangry","Thuncken","Guaraviton","Hummoney"],"reward":10000},
    {"leader":"Raoni","type":"Fogo","level":80,"team":["Headlesh","Jaguarze","Fatuatah"],"reward":11000},
]

CHAMPION = {"leader":"DiguiDex","type":"Lenda","level":90,"team":["Chaballos","Orpyja","Kuckagron","Metagross","Mismagius","Fatuatah"],"reward":25000}

for _n,_t,_l,_team,_r in [(g["leader"],g["type"],g["level"],g["team"],g["reward"]) for g in GYMS] + [(e["leader"],e["type"],e["level"],e["team"],e["reward"]) for e in ELITE4] + [(CHAMPION["leader"],CHAMPION["type"],CHAMPION["level"],CHAMPION["team"],CHAMPION["reward"])]:
    pass
# Species referenced by late-game teams but not in the initial compact dictionary.
for _n,_t in [("Hummoney","Aço/Voador"),("Cacnea","Grama"),("Maractus","Grama"),("Froslass","Gelo/Fantasma"),
              ("Armordillo","Pedra/Aço"),("Headlesh","Fogo/Fantasma")]:
    if _n not in POKEMON: _species(_n,_t)

TRAINERS = {}
for g in GYMS:
    TRAINERS[g["leader"]] = {"map":g["city"],"x":7,"y":8,"team":g["team"],"level":g["level"],"leader":True,"reward":g["reward"],"gym_index":GYMS.index(g)+1}
for i,e in enumerate(ELITE4):
    TRAINERS[e["leader"]] = {"map":"league","x":4+i*2,"y":4,"team":e["team"],"level":e["level"],"elite":True,"reward":e["reward"],"elite_index":i}
TRAINERS[CHAMPION["leader"]] = {"map":"league","x":10,"y":6,"team":CHAMPION["team"],"level":CHAMPION["level"],"champion":True,"reward":CHAMPION["reward"]}

V6_TRANSITIONS = [
    ("guarany",7,11,"route1v6",7,1,"Você deixou Guarany Town e entrou na Rota 1."),
    ("route1v6",7,1,"guarany",7,10,"Você voltou para Guarany Town."),
    ("route1v6",14,6,"amazon",1,6,"Amazon City surgiu no horizonte!"),
    ("amazon",1,6,"route1v6",14,6,"Você voltou à Rota 1."),
    ("amazon",14,6,"route2v6",1,6,"Rota 2: floresta e rios começam aqui."),
    ("route2v6",1,6,"amazon",14,6,"Você voltou a Amazon City."),
    ("route2v6",14,6,"akre",1,6,"Você chegou a Akre City, terra dos mistérios."),
    ("akre",1,6,"route2v6",14,6,"Você voltou à Rota 2."),
    ("akre",14,6,"route3v6",1,6,"A Rota 3 leva ao coração de Brasar."),
    ("route3v6",1,6,"akre",14,6,"Você voltou a Akre."),
    ("route3v6",14,6,"cuiabee",1,6,"Você chegou a Cuiabee City."),
    ("cuiabee",1,6,"route3v6",14,6,"Você voltou à Rota 3."),
    ("cuiabee",14,6,"route4v6",1,6,"Rumo aos pampas gelados."),
    ("route4v6",1,6,"cuiabee",14,6,"Você voltou a Cuiabee."),
    ("route4v6",14,6,"blumenice",1,6,"Você chegou a Blumenice City."),
    ("blumenice",1,6,"route4v6",14,6,"Você voltou à rota montanhosa."),
    ("blumenice",14,6,"route5v6",1,6,"Rumo a SaintPaul."),
    ("route5v6",1,6,"blumenice",14,6,"Você voltou a Blumenice."),
    ("route5v6",14,6,"saintpaul",1,6,"Você chegou a SaintPaul City."),
    ("saintpaul",1,6,"route5v6",14,6,"Você voltou à rota."),
    ("saintpaul",14,6,"route6v6",1,6,"Rumo a Ryo City."),
    ("route6v6",1,6,"saintpaul",14,6,"Você voltou a SaintPaul."),
    ("route6v6",14,6,"ryo",1,6,"Você chegou a Ryo City."),
    ("ryo",1,6,"route6v6",14,6,"Você voltou à rota."),
    ("ryo",14,6,"route7v6",1,6,"Rumo às Minas Triangulares."),
    ("route7v6",1,6,"ryo",14,6,"Você voltou a Ryo."),
    ("route7v6",14,6,"turmalina",1,6,"Você chegou a Turmalina City."),
    ("turmalina",1,6,"route7v6",14,6,"Você voltou às montanhas."),
    ("turmalina",14,6,"route8v6",1,6,"Rumo a Soulvior."),
    ("route8v6",1,6,"turmalina",14,6,"Você voltou a Turmalina."),
    ("route8v6",14,6,"soulvior",1,6,"Você chegou a Soulvior City."),
    ("soulvior",1,6,"route8v6",14,6,"Você voltou à rota."),
    ("soulvior",14,6,"route9v6",1,6,"Rumo a Olynda."),
    ("route9v6",1,6,"soulvior",14,6,"Você voltou a Soulvior."),
    ("route9v6",14,6,"olynda",1,6,"Você chegou a Olynda City."),
    ("olynda",1,6,"route9v6",14,6,"Você voltou à rota."),
    ("olynda",14,6,"route10v6",1,6,"Rumo à Fortaleza de Gonzaga."),
    ("route10v6",1,6,"olynda",14,6,"Você voltou a Olynda."),
    ("route10v6",14,6,"fortress",1,6,"Você chegou a Fortress City."),
    ("fortress",1,6,"route10v6",14,6,"Você voltou a Olynda."),
    ("fortress",14,6,"area_zero",1,6,"Uma passagem secreta leva à Área Zero."),
    ("area_zero",1,6,"fortress",14,6,"Você saiu da Área Zero."),
    ("area_zero",14,6,"league",1,6,"Você chegou à Liga Pokémon!"),
]

ROUTE_ENCOUNTERS = {
    "route1v6":(["Grubey","Perigreen","Canarin","Macarim","Capyba"],(3,6)),
    "route2v6":(["Julifly","Briganite","Chloralga","Murizika","Melopole"],(7,10)),
    "route3v6":(["Guarice","Brigarock","Canindarara","Muihrite","Toxua"],(10,15)),
    "route4v6":(["Guarice","Caxinguelice","Briganite","Pipat","Sinistea de Brasar"],(14,18)),
    "route5v6":(["Toxua","Melopole","Feipig","Canarin","Maugh"],(18,22)),
    "route6v6":(["Pepperim","Roseph","Aquack","Canangry","Dolphink"],(22,27)),
    "route7v6":(["Muihrite","Rockeon","Mandimole","Falinks de Brasar","Guaramite"],(27,32)),
    "route8v6":(["Yamask de Brasar","Foffet","Phanteon","Maugh","Mimikyu de Brasar"],(32,38)),
    "route9v6":(["Gigarucu","Dolphink","Sirenatee","Aquack","Sarereh"],(38,45)),
    "route10v6":(["Cabrooat","Dubwool de Brasar","Jaduitan","Kuckagron","Alarala"],(45,52)),
    "area_zero":(["Iron Bubble","Iron Television","Old Bundle","Kuckagron","Orpyja"],(60,68)),
}

V6_FLAGS = {
    "starter_received": False, "rival_1_defeated": False, "rival_2_defeated": False,
    "yby_helped": False, "tata_helped": False, "amana_helped": False,
    "area_zero_unlocked": False, "league_unlocked": False, "champion_defeated": False,
}
try:
    story_flags.update(V6_FLAGS)
except Exception:
    story_flags = V6_FLAGS.copy()

# Inicialize o novo estado sem destruir um save antigo.
badges = min(int(badges), 10)
game_mode = "world" if party else "starter"
v6_battle_bag = False
v6_bag_cursor = 0
v6_league_index = 0

# Complete os dados de golpes para a nova Pokédex.
MOVE_DATA.update({
    "Golpe Marcial":{"type":"Lutador","power":60,"accuracy":100,"pp":25,"category":"Físico","effect":None,"chance":0},
    "Mordida Sombria":{"type":"Sombrio","power":60,"accuracy":100,"pp":25,"category":"Físico","effect":None,"chance":10},
    "Confusão":{"type":"Psíquico","power":50,"accuracy":100,"pp":25,"category":"Especial","effect":"Confuso","chance":20},
    "Raio de Gelo":{"type":"Gelo","power":55,"accuracy":100,"pp":25,"category":"Especial","effect":"Congelado","chance":10},
    "Vento Fada":{"type":"Fada","power":50,"accuracy":100,"pp":30,"category":"Especial","effect":None,"chance":0},
    "Garra Dragão":{"type":"Dragão","power":60,"accuracy":100,"pp":20,"category":"Físico","effect":None,"chance":0},
    "Bola Sombria":{"type":"Fantasma","power":60,"accuracy":100,"pp":15,"category":"Especial","effect":None,"chance":20},
    "Dreno Vital":{"type":"Grama","power":50,"accuracy":100,"pp":20,"category":"Especial","effect":None,"chance":0},
    "Hidro Bomba":{"type":"Água","power":90,"accuracy":80,"pp":5,"category":"Especial","effect":None,"chance":0},
    "Gema de Poder":{"type":"Pedra","power":60,"accuracy":100,"pp":20,"category":"Especial","effect":None,"chance":0},
    "Terremoto":{"type":"Terra","power":80,"accuracy":100,"pp":10,"category":"Físico","effect":None,"chance":0},
    "Cabeçada":{"type":"Aço","power":70,"accuracy":100,"pp":15,"category":"Físico","effect":None,"chance":10},
    "Voz Ecoante":{"type":"Normal","power":50,"accuracy":100,"pp":15,"category":"Especial","effect":None,"chance":0},
})
TYPE_EFFECTIVENESS.update({
    ("Fogo","Gelo"):2,("Fogo","Aço"):2,("Água","Terra"):2,("Grama","Terra"):2,("Grama","Pedra"):2,
    ("Elétrico","Água"):2,("Elétrico","Voador"):2,("Gelo","Dragão"):2,("Gelo","Voador"):2,
    ("Lutador","Normal"):2,("Lutador","Aço"):2,("Lutador","Sombrio"):2,("Sombrio","Psíquico"):2,
    ("Fantasma","Psíquico"):2,("Fantasma","Fantasma"):2,("Dragão","Dragão"):2,("Fada","Dragão"):2,
    ("Terra","Elétrico"):2,("Terra","Fogo"):2,("Terra","Veneno"):2,("Pedra","Gelo"):2,
    ("Psíquico","Lutador"):2,("Psíquico","Veneno"):2,("Veneno","Fada"):2,
    ("Normal","Fantasma"):0,("Lutador","Fantasma"):0,("Elétrico","Terra"):0,("Dragão","Fada"):0,
})

# Alguns nomes têm grafias ligeiramente diferentes entre materiais; mantenha aliases jogáveis.
ALIASES = {"Sinistea de Brasar":"Sinistea de Brasar","Cacturne de Brasar":"Cacturne de Brasar"}
for _n,_t in [("Sinistea de Brasar","Fantasma/Grama"),("Polteageist de Brasar","Fantasma/Grama"),("Cacturne de Brasar","Grama/Aço"),("Corneiro","Normal")]:
    if _n not in POKEMON: _species(_n,_t)

# Novos helpers de V6.
def v6_map():
    return V6_MAPS.get(current_map, V6_MAPS["guarany"])

def v6_city_gym(city):
    for g in GYMS:
        if g["city"] == city: return g
    return None

def v6_heal_if_center():
    if current_map in CITY_NAMES and abs(player_x-3)<=1 and abs(player_y-2)<=1:
        heal_party(); show_message("Centro Pokémon: equipe completamente restaurada!"); return True
    return False

def v6_shop():
    global game_mode
    game_mode="shop"

def v6_route_wild():
    data=ROUTE_ENCOUNTERS.get(current_map)
    if not data: return "Grubey",5
    names,levels=data
    return random.choice(names), random.randint(*levels)

def get_map():
    return v6_map()

def can_walk(x,y):
    mapa=get_map()
    if y<0 or y>=len(mapa) or x<0 or x>=len(mapa[y]): return False
    return mapa[y][x] in ".GDTNSCAL"

def choose_wild():
    return v6_route_wild()[0]

def wild_level_range():
    data=ROUTE_ENCOUNTERS.get(current_map)
    return data[1] if data else (3,6)

def start_battle():
    global game_mode,battle_enemy,battle_enemy_level,battle_enemy_hp,battle_enemy_max_hp,battle_state,battle_cursor,battle_enemy_obj,battle_enemy_status
    global trainer_battle,trainer_name,trainer_team,trainer_index,battle_turn_queue,battle_turn_index,battle_turn_delay,forced_switch
    if first_alive()==-1: return
    trainer_battle=False; trainer_name=None; trainer_team=[]; trainer_index=0
    battle_turn_queue=[]; battle_turn_index=0; battle_turn_delay=0; forced_switch=False
    battle_enemy,battle_enemy_level=v6_route_wild()
    battle_enemy_obj=create_pokemon(battle_enemy,battle_enemy_level)
    if current_map == "route1v6" and battle_enemy == "Pikachu":
        battle_enemy_obj["attack"] = 14 + battle_enemy_level * 2
        battle_enemy_obj["sp_attack"] = 14 + battle_enemy_level * 2
        battle_enemy_obj["defense"] = 12 + battle_enemy_level
        battle_enemy_obj["sp_defense"] = 12 + battle_enemy_level
        battle_enemy_obj["speed"] = 20 + battle_enemy_level
    battle_enemy_hp=battle_enemy_obj["hp"]; battle_enemy_max_hp=battle_enemy_obj["max_hp"]; battle_enemy_status="Normal"
    battle_state="menu"; battle_cursor=0; game_mode="battle"

def start_trainer_battle(name):
    global game_mode,trainer_battle,trainer_name,trainer_team,trainer_index,trainer_enemy_hp,trainer_enemy_max_hp,battle_state,battle_cursor,active_index
    global battle_turn_queue,battle_turn_index,battle_turn_delay,forced_switch
    info=TRAINERS[name]
    battle_turn_queue=[]; battle_turn_index=0; battle_turn_delay=0; forced_switch=False
    trainer_battle=True; trainer_name=name; trainer_team=[create_pokemon(n,info["level"]) for n in info["team"]]; trainer_index=0
    enemy=trainer_team[0]; trainer_enemy_hp=enemy["hp"]; trainer_enemy_max_hp=enemy["max_hp"]
    battle_state="menu"; battle_cursor=0; active_index=first_alive(); game_mode="battle"

def trainer_current():
    if not trainer_team or trainer_index>=len(trainer_team): return None
    return trainer_team[trainer_index]

def trainer_reward(name): return TRAINERS.get(name,{}).get("reward",100)

def advance_trainer_after_defeat():
    global trainer_index,trainer_enemy_hp,trainer_enemy_max_hp,trainer_battle,trainer_name,trainer_team,game_mode,badges
    if trainer_index+1 < len(trainer_team):
        trainer_index+=1; enemy=trainer_current(); trainer_enemy_hp=enemy["hp"]; trainer_enemy_max_hp=enemy["max_hp"]; return False
    defeated=trainer_name; info=TRAINERS.get(defeated,{})
    trainer_defeated.add(defeated); globals()["money"] += trainer_reward(defeated)
    if info.get("leader"):
        idx=info.get("gym_index",0)
        if idx>badges: badges=idx
        story_flags["gym_leader_defeated"]=True
        if regional_progress_complete(): story_flags["area_zero_unlocked"]=True
    if info.get("elite"):
        story_flags["league_unlocked"]=True
    if info.get("champion"):
        story_flags["champion_defeated"]=True
    trainer_battle=False; trainer_name=None; trainer_team=[]; trainer_index=0
    game_mode="ending" if info.get("champion") else "world"
    return True

def check_trainer_encounter():
    for name,info in TRAINERS.items():
        if info["map"]==current_map and info["x"]==player_x and info["y"]==player_y and name not in trainer_defeated:
            # Só o líder da cidade fica no ginásio; a coordenada representa a entrada/altar do desafio.
            if info.get("leader") and info["leader"] != next_regional_gym()["leader"]: continue
            if info.get("elite") and badges<10: continue
            if info.get("champion") and len([n for n in trainer_defeated if TRAINERS.get(n,{}).get("elite")])<4: continue
            start_trainer_battle(name); return

def move_player(dx,dy):
    global player_x,player_y,current_map
    nx,ny=player_x+dx,player_y+dy
    if not can_walk(nx,ny): return
    player_x,player_y=nx,ny
    for a,ax,ay,b,bx,by,msg in V6_TRANSITIONS:
        if current_map==a and player_x==ax and player_y==ay:
            if not can_leave_city(current_map, b):
                required_leader = BRASAR_CITY_ROUTE_GATES[current_map][1]
                show_message("Derrote " + required_leader + " antes de seguir para a próxima rota."); return
            if b=="area_zero" and not regional_progress_complete():
                next_gym = next_regional_gym()
                show_message("A passagem está selada. Derrote " + next_gym["leader"] + " primeiro."); return
            if b=="league" and not story_flags.get("area_zero_unlocked",False):
                show_message("A Liga só pode ser acessada depois da Área Zero."); return
            current_map,player_x,player_y=b,bx,by; show_message(msg); return
    check_trainer_encounter()
    if current_map in ROUTE_ENCOUNTERS and get_map()[player_y][player_x]=="G" and random.random()<0.13:
        start_battle()

def finish_enemy_defeat():
    global game_mode,battle_enemy_obj,battle_enemy_hp,trainer_enemy_hp
    own=party[first_alive()]; enemy=get_enemy()
    if enemy is None: return
    xp=(25+enemy["level"]*10) if trainer_battle else (20+enemy["level"]*8)
    gain_xp(own,xp)
    if trainer_battle:
        defeated=trainer_name
        completed=advance_trainer_after_defeat()
        if completed:
            info=TRAINERS.get(defeated,{})
            if info.get("leader"):
                show_message(f"{defeated} foi derrotado! Você recebeu {info.get('reward',0)} e a {GYMS[info.get('gym_index',1)-1]['badge']}!")
            elif info.get("elite"):
                show_message(defeated+" foi derrotado! O caminho da Liga continua!")
            elif info.get("champion"):
                show_message("DiguiDex foi derrotado! Você se tornou Campeão de Brasar!")
            else: show_message(defeated+" foi derrotado!")
        else:
            show_message(trainer_name+" enviou o próximo Pokémon!")
    else:
        show_message(enemy["name"]+" foi derrotado! +"+str(xp)+" EXP."); game_mode="world"; battle_enemy_obj=None

def defeat_player():
    global game_mode,current_map,player_x,player_y,active_index
    if first_alive()!=-1: return False
    heal_party(); active_index=0; current_map="guarany"; player_x,player_y=7,7
    show_message("Você desmaiou e foi levado ao Centro Pokémon de Guarany Town."); game_mode="world"; return True

def use_item(item_name):
    global game_mode,pokeballs
    idx=first_alive()
    if idx<0: return False
    if item_name=="Pokébola":
        if not trainer_battle and game_mode=="battle": try_capture(); return True
        show_message("Pokébolas não podem ser usadas contra treinadores!"); return False
    target=party[idx]
    if item_name in ("Poção","Super Poção"):
        amount=20 if item_name=="Poção" else 50
        if items.get(item_name,0)<=0: show_message("Você não possui "+item_name+"!"); return False
        if target["hp"]>=target["max_hp"]: show_message("O HP já está cheio!"); return False
        target["hp"]=min(target["max_hp"],target["hp"]+amount); items[item_name]-=1; show_message(target["name"]+" recuperou "+str(amount)+" HP!"); return True
    if item_name=="Antídoto":
        if items.get(item_name,0)<=0: show_message("Você não possui Antídotos!"); return False
        if target["status"]!="Envenenado": show_message("Nenhum veneno para curar!"); return False
        target["status"]="Normal"; items[item_name]-=1; show_message("O veneno foi curado!"); return True
    return False

def interact_world():
    global game_mode,current_map,player_x,player_y
    if v6_heal_if_center(): return
    if current_map in CITY_NAMES and abs(player_x-11)<=1 and abs(player_y-2)<=1:
        game_mode="shop"; return
    if current_map=="guarany" and abs(player_x-6)<=1 and abs(player_y-5)<=1:
        if not party: game_mode="starter"
        else: show_message("Prof. Jatobá: a diversidade de Brasar muda conforme o bioma. Complete sua Pokédex!")
        return
    # Academias: cinco centros de formação aparecem ao longo da aventura.
    academy_text={"guarany":"Açaí Academy: humanos e Pokémon aprendem a respeitar a natureza.","akre":"Buriti Academy: determinação e força para enfrentar o cerrado.","ryo":"Mamona Academy: tecnologia e treinamento avançado.","blumenice":"Bergamota Academy: coragem nos pampas gelados.","olynda":"Caju Academy: batalhas calorosas e espírito de festa."}
    if current_map in academy_text and abs(player_x-6)<=1 and abs(player_y-5)<=1:
        show_message(academy_text[current_map]); return
    # As três aldeias aparecem como eventos de história nas rotas.
    if current_map=="route1v6" and abs(player_x-5)<=1 and abs(player_y-3)<=1 and not story_flags.get("yby_helped"):
        story_flags["yby_helped"]=True; show_message("Yby: Potyra agradece sua ajuda. A floresta foi protegida; Grassy Terrain envolve a área!"); return
    if current_map=="route3v6" and abs(player_x-6)<=1 and abs(player_y-3)<=1 and not story_flags.get("tata_helped"):
        story_flags["tata_helped"]=True; show_message("Tata: Raoni inicia o desafio das chamas. Você aprendeu a respeitar o fogo de Brasar!"); return
    if current_map=="route9v6" and abs(player_x-6)<=1 and abs(player_y-3)<=1 and not story_flags.get("amana_helped"):
        story_flags["amana_helped"]=True; show_message("Amana: Iara mostra uma visão do futuro através da água. O Grande Amazon River guarda segredos!"); return
    if current_map=="area_zero" and abs(player_x-7)<=1 and abs(player_y-3)<=1:
        story_flags["area_zero_unlocked"]=True; show_message("Área Zero: três Pokémon Paradoxo foram registrados nos relatórios de pesquisa."); return
    if current_map in CITY_NAMES:
        gym=v6_city_gym(current_map)
        if gym and abs(player_x-7)<=1 and abs(player_y-8)<=1:
            if badges >= gym.get("gym_index",1): show_message("Este ginásio já foi conquistado!"); return
            if badges < GYMS.index(gym): show_message("O caminho até este ginásio ainda não foi aberto."); return
            # O líder é encontrado na coordenada central.
            start_trainer_battle(gym["leader"]); return
        city_info = next((entry for entry in BRASAR_CITY_FLOW if entry["city"] == current_map), None)
        if city_info:
            if city_info["leader"]:
                show_message(city_info["name"] + ": " + city_info["story"] + " O líder local é " + city_info["leader"] + ".")
            else:
                show_message(city_info["name"] + ": " + city_info["story"])
            return
    if current_map=="league" and badges>=10:
        defeated_elite=sum(1 for n in trainer_defeated if TRAINERS.get(n,{}).get("elite"))
        if defeated_elite<4:
            name=ELITE4[defeated_elite]["leader"]
            start_trainer_battle(name); return
        if not story_flags.get("champion_defeated"):
            start_trainer_battle(CHAMPION["leader"]); return
        game_mode="ending"

def draw_map():
    mapa=get_map(); screen.fill(LIGHT_GREEN)
    for y,row in enumerate(mapa):
        for x,tile in enumerate(row):
            rect=pygame.Rect(x*TILE,y*TILE,TILE,TILE)
            if tile=="#": pygame.draw.rect(screen,DARK_GREEN,rect); draw_tree(rect)
            elif tile==".": pygame.draw.rect(screen,PATH,rect)
            elif tile=="G": pygame.draw.rect(screen,GREEN,rect); pygame.draw.line(screen,DARK_GREEN,(rect.x+12,rect.bottom-6),(rect.x+16,rect.y+22),3); pygame.draw.line(screen,DARK_GREEN,(rect.x+30,rect.bottom-6),(rect.x+34,rect.y+24),3)
            elif tile=="D": pygame.draw.rect(screen,WATER,rect)
            elif tile=="T": pygame.draw.rect(screen,(175,135,185),rect); pygame.draw.rect(screen,PURPLE,rect,3)
            elif tile=="C": draw_house(rect)
            elif tile=="S": pygame.draw.rect(screen,BLUE,rect); draw_text("$",rect.x+18,rect.y+14,SMALL,WHITE)
            elif tile=="A": pygame.draw.rect(screen,(220,180,95),rect); pygame.draw.rect(screen,BROWN,rect,3); draw_text("A",rect.x+18,rect.y+13,SMALL,WHITE)
            elif tile=="L": pygame.draw.rect(screen,(90,70,110),rect); pygame.draw.rect(screen,WHITE,rect,2)
            pygame.draw.rect(screen,(80,80,70),rect,1)
    if current_map in CITY_NAMES:
        title=CITY_NAMES[current_map]
    else:
        title={"route1v6":"Rota 1 — Floresta Yby","route2v6":"Rota 2 — Rios do Norte","route3v6":"Rota 3 — Desafio das Chamas","route4v6":"Rota 4 — Pampas","route5v6":"Rota 5 — Caminho de SaintPaul","route6v6":"Rota 6 — Costa de Ryo","route7v6":"Rota 7 — Minas Triangulares","route8v6":"Rota 8 — Sombras","route9v6":"Rota 9 — Grande Amazon River","route10v6":"Rota 10 — Caminho da Fortaleza"}.get(current_map,current_map)
    draw_text(title,12,10,SMALL,WHITE); draw_text("Insígnias: "+str(badges)+"/10",600,10,SMALL,WHITE)
    draw_character(player_x*TILE+24,player_y*TILE+24,BLUE)

def draw_bag_screen():
    screen.fill((180,205,175)); pygame.draw.rect(screen,WHITE,(120,45,530,485)); pygame.draw.rect(screen,BLACK,(120,45,530,485),4); draw_text("MOCHILA",320,65,BIG)
    goods=[("Pokébola",pokeballs),("Poção",items.get("Poção",0)),("Super Poção",items.get("Super Poção",0)),("Antídoto",items.get("Antídoto",0))]
    for i,(name,q) in enumerate(goods):
        y=140+i*65
        if not v6_battle_bag and menu_cursor==i: draw_text(">",165,y)
        draw_text(name+" x"+str(q),205,y)
    draw_text("Dinheiro: $"+str(money),205,415,SMALL)
    draw_text("↑ ↓ escolher | ENTER usar | ESC voltar",180,470,SMALL)

def draw_shop():
    screen.fill((205,215,190)); pygame.draw.rect(screen,WHITE,(110,45,550,490)); pygame.draw.rect(screen,BLACK,(110,45,550,490),4); draw_text("POKÉMART",300,65,BIG)
    goods=[("Pokébola",200),("Poção",300),("Super Poção",700),("Antídoto",100)]
    for i,(name,price) in enumerate(goods):
        y=135+i*65
        if shop_cursor==i: draw_text(">",150,y)
        draw_text(name+" - $"+str(price),190,y)
    draw_text("Dinheiro: $"+str(money),190,420,SMALL); draw_text("ENTER comprar | ESC sair",190,465,SMALL)

def handle_shop_key(key):
    global shop_cursor,money,game_mode
    goods=[("Pokébola",200),("Poção",300),("Super Poção",700),("Antídoto",100)]
    if key==pygame.K_UP: shop_cursor=(shop_cursor-1)%len(goods)
    elif key==pygame.K_DOWN: shop_cursor=(shop_cursor+1)%len(goods)
    elif key in [pygame.K_RETURN,pygame.K_z]:
        name,price=goods[shop_cursor]
        if money<price: show_message("Dinheiro insuficiente!"); return
        money-=price
        if name=="Pokébola": pokeballs+=1
        else: items[name]=items.get(name,0)+1
        show_message(name+" comprado!")
    elif key in [pygame.K_ESCAPE,pygame.K_x]: game_mode="world"

def v6_bag_use():
    global v6_battle_bag,battle_state,game_mode,v6_bag_cursor
    global battle_turn_queue,battle_turn_index,battle_turn_delay
    names=["Pokébola","Poção","Super Poção","Antídoto"]
    item_name = names[v6_bag_cursor]
    used=use_item(item_name)
    if used and game_mode=="battle":
        v6_battle_bag=False
        if item_name == "Pokébola":
            battle_state="menu"
            return
        battle_turn_queue=[{"source":"enemy"}]
        battle_turn_index=0
        battle_turn_delay=0
        battle_state="turn"

def handle_battle_key(key):
    global battle_state,battle_cursor,party_cursor,game_mode,v6_battle_bag,v6_bag_cursor
    if v6_battle_bag:
        if key==pygame.K_UP: v6_bag_cursor=(v6_bag_cursor-1)%4
        elif key==pygame.K_DOWN: v6_bag_cursor=(v6_bag_cursor+1)%4
        elif key in [pygame.K_RETURN,pygame.K_z]: v6_bag_use()
        elif key in [pygame.K_ESCAPE,pygame.K_x]: v6_battle_bag=False; battle_state="menu"
        return
    if battle_state=="menu":
        if key==pygame.K_UP: battle_cursor=(battle_cursor-1)%4
        elif key==pygame.K_DOWN: battle_cursor=(battle_cursor+1)%4
        elif key==pygame.K_LEFT and battle_cursor%2: battle_cursor-=1
        elif key==pygame.K_RIGHT and battle_cursor%2==0: battle_cursor+=1
        elif key in [pygame.K_RETURN,pygame.K_z]:
            if battle_cursor==0: battle_state="fight"; battle_cursor=0
            elif battle_cursor==1: battle_switch()
            elif battle_cursor==2: v6_battle_bag=True; v6_bag_cursor=0
            elif battle_cursor==3:
                if trainer_battle: show_message("Você não pode fugir de uma batalha de treinador!")
                elif random.random()<0.85: game_mode="world"; show_message("Você fugiu!")
                else: show_message("Você não conseguiu fugir!"); enemy_attack()
    elif battle_state=="fight":
        moves=party[first_alive()]["moves"]
        if key==pygame.K_LEFT and battle_cursor%2: battle_cursor-=1
        elif key==pygame.K_RIGHT and battle_cursor%2==0: battle_cursor+=1
        elif key==pygame.K_UP: battle_cursor=max(0,battle_cursor-2)
        elif key==pygame.K_DOWN: battle_cursor=min(3,battle_cursor+2)
        elif key in [pygame.K_RETURN,pygame.K_z] and battle_cursor<len(moves): start_battle_turn(battle_cursor)
        elif key in [pygame.K_ESCAPE,pygame.K_x]: battle_state="menu"; battle_cursor=0
    elif battle_state=="switch":
        if key==pygame.K_UP: party_cursor=max(0,party_cursor-1)
        elif key==pygame.K_DOWN: party_cursor=min(max(0,len(party)-1),party_cursor+1)
        elif key in [pygame.K_RETURN,pygame.K_z]: perform_switch(party_cursor)
        elif key in [pygame.K_ESCAPE,pygame.K_x]: battle_state="menu"

def draw_battle():
    screen.fill((220,235,205)); idx=first_alive(); own=party[idx] if idx>=0 else None; enemy=get_enemy()
    pygame.draw.ellipse(screen,GREEN,(430,110,280,90)); pygame.draw.ellipse(screen,GREEN,(55,335,300,95))
    if enemy: draw_big_pokemon(enemy["name"],565,155)
    if own: draw_big_pokemon(own["name"],205,375)
    if enemy:
        pygame.draw.rect(screen,WHITE,(35,35,350,125)); pygame.draw.rect(screen,BLACK,(35,35,350,125),3)
        label=(trainer_name+": " if trainer_battle else "")+enemy["name"]; draw_text(label+" Nv."+str(enemy["level"]),55,50); draw_text(enemy["type"],55,78,SMALL); draw_hp_bar(55,108,270,enemy["hp"],enemy["max_hp"]); draw_text("Status: "+enemy["status"],55,130,SMALL)
    if own:
        pygame.draw.rect(screen,WHITE,(390,270,340,145)); pygame.draw.rect(screen,BLACK,(390,270,340,145),3); draw_text(own["name"]+" Nv."+str(own["level"]),410,285); draw_text(own["type"],410,313,SMALL); draw_hp_bar(410,340,250,own["hp"],own["max_hp"]); draw_text(str(own["hp"])+"/"+str(own["max_hp"]),590,365,SMALL); draw_text("Status: "+own["status"],410,388,SMALL)
        ratio=own["xp"]/max(1,own["xp_to_next"]); pygame.draw.rect(screen,BLACK,(410,405,250,8)); pygame.draw.rect(screen,BLUE,(412,407,int(246*ratio),4))
    pygame.draw.rect(screen,WHITE,(0,450,WIDTH,126)); pygame.draw.rect(screen,BLACK,(0,450,WIDTH,126),4)
    if v6_battle_bag:
        names=[("Pokébola",pokeballs),("Poção",items.get("Poção",0)),("Super Poção",items.get("Super Poção",0)),("Antídoto",items.get("Antídoto",0))]
        draw_text("MOCHILA",45,462,BIG)
        for i,(n,q) in enumerate(names):
            y=505+(i%2)*30; x=50+(i//2)*330
            if v6_bag_cursor==i: draw_text(">",x-22,y)
            draw_text(n+" x"+str(q),x,y,SMALL)
    elif battle_state=="menu":
        for i,opt in enumerate(["LUTAR","POKÉMON","MOCHILA","FUGIR"]):
            x=70+(i%2)*330; y=465+(i//2)*48
            if battle_cursor==i: draw_text(">",x-25,y)
            draw_text(opt,x,y)
    elif battle_state=="fight":
        active=party[first_alive()]
        for i in range(4):
            x=60+(i%2)*330; y=465+(i//2)*45
            if i<len(active["moves"]):
                if battle_cursor==i: draw_text(">",x-25,y)
                m=active["moves"][i]; pp=active.get("move_pp",{}).get(m,MOVE_DATA.get(m,{"pp":0})["pp"]); draw_text(m+" PP "+str(pp),x,y)
            else: draw_text("---",x,y)

def draw_menu():
    screen.fill((180,205,175)); pygame.draw.rect(screen,WHITE,(130,35,508,505)); pygame.draw.rect(screen,BLACK,(130,35,508,505),4); draw_text("MENU",345,55,BIG)
    opts=["POKÉMON","POKÉDEX","MOCHILA","SALVAR","CARREGAR","VOLTAR"]
    for i,opt in enumerate(opts):
        y=125+i*55
        if menu_cursor==i: draw_text(">",205,y)
        draw_text(opt,245,y)
    draw_text("Pokébolas: "+str(pokeballs),245,455,SMALL); draw_text("Dinheiro: $"+str(money),430,455,SMALL); draw_text("Insígnias: "+str(badges)+"/10",245,485,SMALL)

def handle_menu_key(key):
    global game_mode,menu_cursor
    if key==pygame.K_UP: menu_cursor=(menu_cursor-1)%6
    elif key==pygame.K_DOWN: menu_cursor=(menu_cursor+1)%6
    elif key in [pygame.K_RETURN,pygame.K_z,pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5,pygame.K_6]:
        nums={pygame.K_1:0,pygame.K_2:1,pygame.K_3:2,pygame.K_4:3,pygame.K_5:4,pygame.K_6:5}
        if key in nums: menu_cursor=nums[key]
        modes=["party","pokedex","bag","save","load","world"]
        if menu_cursor==3: save_game()
        elif menu_cursor==4: load_game()
        else: game_mode=modes[menu_cursor]
    elif key in [pygame.K_ESCAPE,pygame.K_x]: game_mode="world"

def draw_ending():
    screen.fill((20,30,45))
    pygame.draw.rect(screen, (54, 79, 110), (90, 60, 588, 450), 4)
    pygame.draw.rect(screen, (109, 142, 190), (120, 90, 528, 120), 3)
    draw_text("BRASAR — CAMPEÃO", 220, 110, BIG, WHITE)
    draw_text("Você superou os líderes da região.", 175, 180, FONT, WHITE)
    draw_text("Você venceu a Elite 4 e a Liga.", 185, 220, FONT, WHITE)
    draw_text("Você derrotou DiguiDex, o Rei de Brasar.", 150, 260, FONT, WHITE)
    draw_text("A região reconhece o seu título!", 190, 300, FONT, WHITE)
    draw_text("BRASAR AGORA TEM UM NOVO CAMPEÃO!", 120, 355, FONT, YELLOW)
    draw_text("ESC ou ENTER para continuar explorando", 175, 440, SMALL, WHITE)


# ============================================================
# V7 — EXPLORAÇÃO, SAVE SLOTS, MENU DE CONTROLE E POKÉMON
# ============================================================

# A V7 mantém toda a V6 e adiciona:
# - saídas claras nas bordas dos mapas;
# - um único botão de interação no mundo: E;
# - menu de pausa/controle com salvar, título e sair;
# - tela inicial com 3 slots;
# - mais Pokémon de outras regiões;
# - habilidades simples;
# - visual de mapa/personagem mais próximo do estilo portátil clássico,
#   usando pixel-art original (sem copiar sprites oficiais).

V7_INTERACT_KEY = pygame.K_e
V7_PAUSE_KEY = pygame.K_ESCAPE
V7_CONFIRM_KEY = pygame.K_RETURN

SAVE_SLOTS = [Path("brasar_save_1.json"), Path("brasar_save_2.json"), Path("brasar_save_3.json")]
title_cursor = 0
slot_cursor = 0
pause_cursor = 0
control_cursor = 0
v7_pending_mode = None

PLAYER_OPTIONS = [
    {"gender": "menino", "name": "Caio", "color": BLUE},
    {"gender": "menina", "name": "Lia", "color": RED},
]
VERSION_OPTIONS = [
    {"name": "Pokémon Brasar: Chabalos", "mascot": "Chaballos", "color": ORANGE},
    {"name": "Pokémon Brasar: Horpija", "mascot": "Orpyja", "color": BLUE},
]
player_option_cursor = 0
version_option_cursor = 0
player_gender = "menino"
player_name = "Caio"
rival_name = "Lia"
game_version = "Chabalos"
version_mascot = "Chaballos"
opening_step = 0


def configure_rival():
    rival = "Lia" if player_gender == "menino" else "Caio"
    rival_species = "Flaguar" if game_version == "Chabalos" else "Suriqua"
    TRAINERS[rival] = {
        "map": "route1v6", "x": 10, "y": 6,
        "team": [rival_species, "Canarin"], "level": 5,
        "rival": True, "reward": 300,
    }
    globals()["rival_name"] = rival


def draw_selection_screen(title, subtitle, options, cursor, footer):
    screen.fill((30, 67, 61))
    pygame.draw.rect(screen, (247, 239, 204), (82, 45, 604, 485))
    pygame.draw.rect(screen, (38, 60, 52), (82, 45, 604, 485), 5)
    draw_text(title, 220, 78, BIG, (38, 60, 52))
    draw_text(subtitle, 170, 125, SMALL, (70, 85, 72))
    for index, option in enumerate(options):
        y = 205 + index * 125
        selected = cursor == index
        color = option.get("color", (50, 70, 60))
        pygame.draw.rect(screen, (232, 225, 190), (155, y - 18, 458, 92), 0 if selected else 2)
        if selected:
            pygame.draw.rect(screen, color, (155, y - 18, 458, 92), 5)
            draw_text("▶", 175, y + 12, BIG, color)
        draw_text(option["name"], 220, y, FONT, (38, 60, 52))
        detail = "Mascote: " + option["mascot"] if "mascot" in option else "Sua jornada começa aqui"
        draw_text(detail, 220, y + 35, SMALL, (80, 80, 65))
    draw_text(footer, 220, 480, SMALL, (38, 60, 52))


def draw_protagonist_select():
    draw_selection_screen("ESCOLHA SEU PROTAGONISTA", "A escolha oposta será seu rival.", [{"name": "MENINO", "color": BLUE}, {"name": "MENINA", "color": RED}], player_option_cursor, "UP/DOWN escolher   ENTER confirmar")


def draw_version_select():
    draw_selection_screen("ESCOLHA SUA VERSÃO", "Cada versão tem um mascote de Brasar.", VERSION_OPTIONS, version_option_cursor, "UP/DOWN escolher   ENTER confirmar")


def draw_opening_house():
    screen.fill((82, 111, 93))
    pygame.draw.rect(screen, (224, 190, 130), (70, 55, 628, 425))
    pygame.draw.rect(screen, (65, 49, 42), (70, 55, 628, 425), 6)
    pygame.draw.rect(screen, (176, 125, 82), (120, 150, 528, 240))
    pygame.draw.rect(screen, (106, 72, 53), (310, 300, 150, 90))
    pygame.draw.rect(screen, (54, 96, 126), (155, 185, 115, 70))
    pygame.draw.rect(screen, (54, 96, 126), (498, 185, 115, 70))
    draw_character(384, 275, PLAYER_OPTIONS[player_option_cursor]["color"])
    if opening_step == 0:
        draw_text("Sua casa em Guarany Town", 235, 90, BIG, WHITE)
        draw_text("Você acorda no quarto. A porta está logo abaixo.", 165, 440, FONT, WHITE)
        draw_text("ENTER sair de casa", 285, 505, SMALL, WHITE)
    else:
        draw_text("Guarany Town", 300, 90, BIG, WHITE)
        draw_text("Professor Yby: " + player_name + "! Espere!", 175, 440, FONT, WHITE)
        draw_text("ENTER falar com o professor", 245, 505, SMALL, WHITE)


def handle_protagonist_key(key):
    global player_option_cursor, game_mode
    if key in (pygame.K_UP, pygame.K_DOWN):
        player_option_cursor = 1 - player_option_cursor
    elif key in (pygame.K_RETURN, pygame.K_e):
        selected = PLAYER_OPTIONS[player_option_cursor]
        globals()["player_gender"] = selected["gender"]
        globals()["player_name"] = selected["name"]
        globals()["rival_name"] = "Lia" if selected["gender"] == "menino" else "Caio"
        game_mode = "version_select"


def handle_version_key(key):
    global version_option_cursor, game_mode
    if key in (pygame.K_UP, pygame.K_DOWN):
        version_option_cursor = 1 - version_option_cursor
    elif key in (pygame.K_RETURN, pygame.K_e):
        selected = VERSION_OPTIONS[version_option_cursor]
        globals()["game_version"] = selected["name"].split(": ")[-1]
        globals()["version_mascot"] = selected["mascot"]
        configure_rival()
        globals()["opening_step"] = 0
        game_mode = "opening_house"


def handle_opening_house_key(key):
    global opening_step, game_mode
    if key in (pygame.K_RETURN, pygame.K_e):
        if opening_step == 0:
            opening_step = 1
        else:
            story_flags["professor_met"] = True
            game_mode = "starter"
            show_message("Professor Yby: escolha seu parceiro e comece sua lenda!")

# Saídas ficam sempre nas bordas. O tile da saída é desenhado como caminho,
# e não como arbusto/árvore, para ficar visualmente óbvio.
EDGE_GATES = {
    ("guarany", 7, 11), ("route1v6", 7, 0),
    ("route1v6", 15, 6), ("amazon", 0, 6),
    ("amazon", 15, 6), ("route2v6", 0, 6),
    ("route2v6", 15, 6), ("akre", 0, 6),
    ("akre", 15, 6), ("route3v6", 0, 6),
    ("route3v6", 15, 6), ("cuiabee", 0, 6),
    ("cuiabee", 15, 6), ("route4v6", 0, 6),
    ("route4v6", 15, 6), ("blumenice", 0, 6),
    ("blumenice", 15, 6), ("route5v6", 0, 6),
    ("route5v6", 15, 6), ("saintpaul", 0, 6),
    ("saintpaul", 15, 6), ("route6v6", 0, 6),
    ("route6v6", 15, 6), ("ryo", 0, 6),
    ("ryo", 15, 6), ("route7v6", 0, 6),
    ("route7v6", 15, 6), ("turmalina", 0, 6),
    ("turmalina", 15, 6), ("route8v6", 0, 6),
    ("route8v6", 15, 6), ("soulvior", 0, 6),
    ("soulvior", 15, 6), ("route9v6", 0, 6),
    ("route9v6", 15, 6), ("olynda", 0, 6),
    ("olynda", 15, 6), ("route10v6", 0, 6),
    ("route10v6", 15, 6), ("fortress", 0, 6),
    ("fortress", 15, 6), ("area_zero", 0, 6),
    ("area_zero", 15, 6), ("league", 0, 6),
}

# Todas as conexões da aventura passam pela borda do mapa.
V7_TRANSITIONS = [
    ("guarany",7,11,"route1v6",7,1,"Rota 1 — a aventura começou!"),
    ("route1v6",7,0,"guarany",7,10,"Você voltou para Guarany Town."),
    ("route1v6",15,6,"amazon",1,6,"Amazon City surgiu no horizonte!"),
    ("amazon",0,6,"route1v6",14,6,"Você voltou à Rota 1."),
    ("amazon",15,6,"route2v6",1,6,"Rota 2: floresta e rios começam aqui."),
    ("route2v6",0,6,"amazon",14,6,"Você voltou a Amazon City."),
    ("route2v6",15,6,"akre",1,6,"Você chegou a Akre City."),
    ("akre",0,6,"route2v6",14,6,"Você voltou à Rota 2."),
    ("akre",15,6,"route3v6",1,6,"A Rota 3 leva ao coração de Brasar."),
    ("route3v6",0,6,"akre",14,6,"Você voltou a Akre."),
    ("route3v6",15,6,"cuiabee",1,6,"Você chegou a Cuiabee City."),
    ("cuiabee",0,6,"route3v6",14,6,"Você voltou à Rota 3."),
    ("cuiabee",15,6,"route4v6",1,6,"Rumo aos pampas gelados."),
    ("route4v6",0,6,"cuiabee",14,6,"Você voltou a Cuiabee."),
    ("route4v6",15,6,"blumenice",1,6,"Você chegou a Blumenice City."),
    ("blumenice",0,6,"route4v6",14,6,"Você voltou à rota montanhosa."),
    ("blumenice",15,6,"route5v6",1,6,"Rumo a SaintPaul."),
    ("route5v6",0,6,"blumenice",14,6,"Você voltou a Blumenice."),
    ("route5v6",15,6,"saintpaul",1,6,"Você chegou a SaintPaul City."),
    ("saintpaul",0,6,"route5v6",14,6,"Você voltou à rota."),
    ("saintpaul",15,6,"route6v6",1,6,"Rumo a Ryo City."),
    ("route6v6",0,6,"saintpaul",14,6,"Você voltou a SaintPaul."),
    ("route6v6",15,6,"ryo",1,6,"Você chegou a Ryo City."),
    ("ryo",0,6,"route6v6",14,6,"Você voltou à rota."),
    ("ryo",15,6,"route7v6",1,6,"Rumo às Minas Triangulares."),
    ("route7v6",0,6,"ryo",14,6,"Você voltou a Ryo."),
    ("route7v6",15,6,"turmalina",1,6,"Você chegou a Turmalina City."),
    ("turmalina",0,6,"route7v6",14,6,"Você voltou às montanhas."),
    ("turmalina",15,6,"route8v6",1,6,"Rumo a Soulvior."),
    ("route8v6",0,6,"turmalina",14,6,"Você voltou a Turmalina."),
    ("route8v6",15,6,"soulvior",1,6,"Você chegou a Soulvior City."),
    ("soulvior",0,6,"route8v6",14,6,"Você voltou à rota."),
    ("soulvior",15,6,"route9v6",1,6,"Rumo a Olynda."),
    ("route9v6",0,6,"soulvior",14,6,"Você voltou a Soulvior."),
    ("route9v6",15,6,"olynda",1,6,"Você chegou a Olynda City."),
    ("olynda",0,6,"route9v6",14,6,"Você voltou à rota."),
    ("olynda",15,6,"route10v6",1,6,"Rumo à Fortaleza de Gonzaga."),
    ("route10v6",0,6,"olynda",14,6,"Você voltou a Olynda."),
    ("fortress",0,6,"route10v6",14,6,"Você voltou a Olynda."),
    ("route10v6",15,6,"fortress",1,6,"Você chegou a Fortress City."),
    ("fortress",15,6,"area_zero",1,6,"Uma passagem secreta leva à Área Zero."),
    ("area_zero",0,6,"fortress",14,6,"Você saiu da Área Zero."),
    ("area_zero",15,6,"league",1,6,"Você chegou à Liga Pokémon!"),
    ("league",0,6,"area_zero",14,6,"Você voltou à Área Zero."),
]
V6_TRANSITIONS = V7_TRANSITIONS

# Pokémon adicionais de Kanto/Johto/Hoenn/Sinnoh/Unova/Kalos/Alola/Galar/Paldea.
# Eles usam os mesmos sistemas de HP, EXP, tipos, golpes, status e evolução da V6.
V7_EXTRA_SPECIES = {
    "Bulbasaur":("Grama/Veneno",45,49,49,45,["Folhagem","Toxina"]),
    "Charmander":("Fogo",39,52,43,65,["Brasa","Investida"]),
    "Squirtle":("Água",44,48,65,43,["Jato d'Água","Investida"]),
    "Pikachu":("Elétrico",35,55,40,90,["Choque","Investida"]),
    "Meowth":("Normal",40,45,35,90,["Investida","Mordida"]),
    "Psyduck":("Água",50,52,48,55,["Jato d'Água","Confusão"]),
    "Growlithe":("Fogo",55,70,45,60,["Brasa","Mordida"]),
    "Gastly":("Fantasma/Veneno",30,35,30,80,["Bola Sombria","Toxina"]),
    "Eevee":("Normal",55,55,50,55,["Investida","Ataque Rápido"]),
    "Dratini":("Dragão",41,64,45,50,["Garra Dragão","Investida"]),
    "Chikorita":("Grama",45,49,65,45,["Folhagem","Investida"]),
    "Cyndaquil":("Fogo",39,52,43,65,["Brasa","Investida"]),
    "Totodile":("Água",50,65,64,43,["Jato d'Água","Mordida"]),
    "Mareep":("Elétrico",55,40,40,35,["Choque","Investida"]),
    "Eeveeon":("Normal",90,70,55,90,["Investida","Ataque Rápido"]),
    "Treecko":("Grama",40,45,35,70,["Folhagem","Investida"]),
    "Torchic":("Fogo",45,60,40,45,["Brasa","Investida"]),
    "Mudkip":("Água",50,70,50,40,["Jato d'Água","Investida"]),
    "Ralts":("Psíquico/Fada",28,25,25,40,["Confusão","Vento Fada"]),
    "Aron":("Aço/Pedra",50,70,100,30,["Pedrada","Cabeçada"]),
    "Shinx":("Elétrico",45,65,34,45,["Choque","Mordida"]),
    "Riolu":("Lutador",40,70,40,60,["Golpe Marcial","Investida"]),
    "Gible":("Dragão/Terra",58,70,45,42,["Garra Dragão","Terremoto"]),
    "Snivy":("Grama",45,45,55,63,["Folhagem","Investida"]),
    "Tepig":("Fogo",65,63,45,45,["Brasa","Investida"]),
    "Oshawott":("Água",55,55,45,45,["Jato d'Água","Investida"]),
    "Zorua":("Sombrio",40,65,40,65,["Mordida Sombria","Investida"]),
    "Froakie":("Água",41,56,40,71,["Jato d'Água","Investida"]),
    "Fletchling":("Normal/Voador",45,50,43,62,["Asa de Vento","Investida"]),
    "Rowlet":("Grama/Voador",68,55,55,42,["Folhagem","Asa de Vento"]),
    "Litten":("Fogo",45,65,40,70,["Brasa","Mordida"]),
    "Popplio":("Água",50,54,54,40,["Jato d'Água","Vento Fada"]),
    "Grookey":("Grama",50,65,50,69,["Folhagem","Investida"]),
    "Scorbunny":("Fogo",50,71,40,69,["Brasa","Investida"]),
    "Sobble":("Água",50,40,40,70,["Jato d'Água","Investida"]),
    "Sprigatito":("Grama",40,61,54,65,["Folhagem","Mordida"]),
    "Fuecoco":("Fogo",67,45,59,36,["Brasa","Mordida"]),
    "Quaxly":("Água",55,65,45,50,["Jato d'Água","Asa de Vento"]),
}
for _n,_d in V7_EXTRA_SPECIES.items():
    if _n not in POKEMON:
        _species(_n,*_d)

# Algumas espécies evoluídas e encontros comuns usados pela expansão.
V7_MORE_SPECIES = {
    "Pidgey":("Normal/Voador",40,45,40,56,["Investida","Asa de Vento"]),
    "Ivysaur":("Grama/Veneno",60,62,63,60,["Folhagem","Toxina"]),
    "Venusaur":("Grama/Veneno",80,82,83,80,["Folhagem","Toxina"]),
    "Charmeleon":("Fogo",58,64,58,80,["Brasa","Mordida"]),
    "Charizard":("Fogo/Voador",78,84,78,100,["Brasa","Asa de Vento"]),
    "Wartortle":("Água",59,63,80,58,["Jato d'Água","Mordida"]),
    "Blastoise":("Água",79,83,100,78,["Jato d'Água","Hidro Bomba"]),
    "Bayleef":("Grama",60,62,80,60,["Folhagem","Investida"]),
    "Meganium":("Grama",80,82,100,80,["Folhagem","Dreno Vital"]),
    "Quilava":("Fogo",58,64,58,80,["Brasa","Investida"]),
    "Typhlosion":("Fogo",78,84,78,100,["Brasa","Mordida"]),
    "Croconaw":("Água",65,80,80,58,["Jato d'Água","Mordida"]),
    "Feraligatr":("Água",85,105,100,78,["Jato d'Água","Mordida"]),
    "Grovyle":("Grama",50,65,45,95,["Folhagem","Investida"]),
    "Sceptile":("Grama",70,85,65,120,["Folhagem","Dreno Vital"]),
    "Combusken":("Fogo/Lutador",60,85,60,55,["Brasa","Golpe Marcial"]),
    "Blaziken":("Fogo/Lutador",80,120,70,80,["Brasa","Golpe Marcial"]),
    "Marshtomp":("Água/Terra",70,85,70,50,["Jato d'Água","Terremoto"]),
    "Swampert":("Água/Terra",100,110,90,60,["Jato d'Água","Terremoto"]),
    "Gabite":("Dragão/Terra",68,90,65,82,["Garra Dragão","Terremoto"]),
    "Garchomp":("Dragão/Terra",108,130,95,102,["Garra Dragão","Terremoto"]),
    "Frogadier":("Água",54,63,52,97,["Jato d'Água","Investida"]),
    "Greninja":("Água/Sombrio",72,95,67,122,["Jato d'Água","Mordida Sombria"]),
    "Lucario":("Lutador/Aço",70,110,70,90,["Golpe Marcial","Cabeçada"]),
    "Raichu":("Elétrico",60,90,55,110,["Choque","Ataque Rápido"]),
}
for _n,_d in V7_MORE_SPECIES.items():
    if _n not in POKEMON:
        _species(_n,*_d)

# Habilidades simples: elas realmente participam da batalha.
ABILITY_BY_SPECIES = {
    "Bulbasaur":"Overgrow","Charmander":"Blaze","Squirtle":"Torrent",
    "Treecko":"Overgrow","Torchic":"Blaze","Mudkip":"Torrent",
    "Rowlet":"Overgrow","Litten":"Blaze","Popplio":"Torrent",
    "Grookey":"Overgrow","Scorbunny":"Blaze","Sobble":"Torrent",
    "Sprigatito":"Overgrow","Fuecoco":"Blaze","Quaxly":"Torrent",
    "Pikachu":"Static","Growlithe":"Intimidate","Shinx":"Intimidate",
    "Aron":"Sturdy","Riolu":"Inner Focus","Zorua":"Illusion",
    "Eevee":"Adaptability",
}
for _name,_ability in ABILITY_BY_SPECIES.items():
    if _name in POKEMON:
        POKEMON[_name]["ability"]=_ability

# Mistura regional + Pokémon conhecidos nas rotas.
V7_MIXED_ENCOUNTERS = {
    "route1v6":(["Grubey","Perigreen","Canarin","Macarim","Pikachu","Pidgey","Bulbasaur"],(3,5)),
    "route2v6":(["Julifly","Briganite","Chloralga","Murizika","Eevee","Charmander","Mareep"],(7,10)),
    "route3v6":(["Guarice","Brigarock","Canindarara","Muihrite","Toxua","Squirtle","Shinx"],(10,15)),
    "route4v6":(["Guarice","Caxinguelice","Briganite","Pipat","Sinistea de Brasar","Gible","Ralts"],(14,18)),
    "route5v6":(["Toxua","Melopole","Feipig","Canarin","Maugh","Riolu","Gastly"],(18,22)),
    "route6v6":(["Pepperim","Roseph","Aquack","Canangry","Dolphink","Treecko","Torchic"],(22,27)),
    "route7v6":(["Muihrite","Rockeon","Mandimole","Falinks de Brasar","Guaramite","Aron","Mudkip"],(27,32)),
    "route8v6":(["Yamask de Brasar","Foffet","Phanteon","Maugh","Mimikyu de Brasar","Zorua","Froakie"],(32,38)),
    "route9v6":(["Gigarucu","Dolphink","Sirenatee","Aquack","Sarereh","Rowlet","Litten"],(38,45)),
    "route10v6":(["Cabrooat","Dubwool de Brasar","Jaduitan","Kuckagron","Alarala","Grookey","Scorbunny"],(45,52)),
    "area_zero":(["Iron Bubble","Iron Television","Old Bundle","Kuckagron","Orpyja","Gible","Sobble"],(60,68)),
}
ROUTE_ENCOUNTERS = V7_MIXED_ENCOUNTERS

# Evoluções de alguns Pokémon conhecidos.
V7_EVOLUTIONS = {
    "Bulbasaur":("Ivysaur",16),"Ivysaur":("Venusaur",32),
    "Charmander":("Charmeleon",16),"Charmeleon":("Charizard",36),
    "Squirtle":("Wartortle",16),"Wartortle":("Blastoise",36),
    "Pikachu":("Raichu",20),"Chikorita":("Bayleef",16),"Bayleef":("Meganium",32),
    "Cyndaquil":("Quilava",14),"Quilava":("Typhlosion",36),
    "Totodile":("Croconaw",18),"Croconaw":("Feraligatr",30),
    "Treecko":("Grovyle",16),"Grovyle":("Sceptile",36),
    "Torchic":("Combusken",16),"Combusken":("Blaziken",36),
    "Mudkip":("Marshtomp",16),"Marshtomp":("Swampert",36),
    "Gible":("Gabite",24),"Gabite":("Garchomp",48),
    "Riolu":("Lucario",25),"Froakie":("Frogadier",16),"Frogadier":("Greninja",36),
}
for _base,_pair in V7_EVOLUTIONS.items():
    _next,_lv=_pair
    if _base in POKEMON and _next not in POKEMON:
        d=POKEMON[_base]
        _species(_next,d["type"],d["base_hp"]+12,d["attack"]+10,d["defense"]+8,d["speed"]+8,list(d["moves"]))
EVOLUTIONS.update(V7_EVOLUTIONS)

# ---------------- SAVE SLOTS ----------------

def _save_data():
    return {
        "version":8,
        "player_gender": player_gender, "player_name": player_name,
        "rival_name": rival_name, "game_version": game_version,
        "version_mascot": version_mascot,
        "current_map":current_map,"player_x":player_x,"player_y":player_y,
        "party":party,"pokeballs":pokeballs,"money":money,"pokedex":list(pokedex),
        "badges":badges,"trainer_defeated":list(trainer_defeated),
        "story_flags":story_flags,"items":items,"active_index":active_index,
    }

def _write_slot(slot):
    try:
        if not 0 <= slot < len(SAVE_SLOTS):
            raise ValueError("slot de save inválido")
        target = SAVE_SLOTS[slot]
        temporary = target.with_suffix(target.suffix + ".tmp")
        payload = json.dumps(_save_data(), ensure_ascii=False, indent=2)
        temporary.write_text(payload, encoding="utf-8")
        temporary.replace(target)
        show_message("Jogo salvo no Slot "+str(slot+1)+"!")
        return True
    except (OSError, TypeError, ValueError) as exc:
        show_message("Erro ao salvar: "+str(exc)[:45]); return False


def _valid_save_data(data):
    if not isinstance(data, dict):
        return False
    if not isinstance(data.get("party", []), list):
        return False
    if not isinstance(data.get("items", {}), dict):
        return False
    map_name = data.get("current_map", "guarany")
    return map_name in V6_MAPS or map_name.startswith("__interior_")


def _load_slot(slot):
    global current_map,player_x,player_y,party,pokeballs,money,pokedex,badges
    global trainer_defeated,story_flags,items,active_index,game_mode
    global player_gender,player_name,rival_name,game_version,version_mascot
    if not 0 <= slot < len(SAVE_SLOTS):
        return False
    if not SAVE_SLOTS[slot].exists():
        return False
    try:
        data=json.loads(SAVE_SLOTS[slot].read_text(encoding="utf-8"))
        if not _valid_save_data(data):
            show_message("Este save não possui um formato válido.")
            return False
        current_map=data.get("current_map","guarany")
        player_x=data.get("player_x",7); player_y=data.get("player_y",7)
        party=data.get("party",[]); pokeballs=data.get("pokeballs",5)
        money=data.get("money",300); pokedex=set(data.get("pokedex",[]))
        badges=min(10,int(data.get("badges",0)))
        trainer_defeated=set(data.get("trainer_defeated",[]))
        story_flags.update(data.get("story_flags",{}))
        items.update(data.get("items",{}))
        active_index=int(data.get("active_index",0))
        player_gender=data.get("player_gender", "menino")
        player_name=data.get("player_name", "Caio" if player_gender == "menino" else "Lia")
        rival_name=data.get("rival_name", "Lia" if player_gender == "menino" else "Caio")
        game_version=data.get("game_version", "Chabalos")
        version_mascot=data.get("version_mascot", "Chaballos" if game_version == "Chabalos" else "Orpyja")
        configure_rival()
        game_mode="world"
        return True
    except (OSError, UnicodeError, json.JSONDecodeError, TypeError, ValueError):
        return False

def _new_game():
    global current_map,player_x,player_y,party,pokeballs,money,pokedex,badges
    global trainer_defeated,story_flags,items,active_index,game_mode
    current_map="guarany"; player_x,player_y=7,7; party=[]
    pokeballs=5; money=300; pokedex=set(); badges=0
    trainer_defeated=set(); active_index=0
    story_flags.clear(); story_flags.update(V6_FLAGS)
    items.clear(); items.update({"Poção":2,"Antídoto":1,"Super Poção":0})
    story_flags["professor_met"] = False
    game_mode="protagonist_select"

def _slot_label(slot):
    if not SAVE_SLOTS[slot].exists():
        return "VAZIO"
    try:
        d=json.loads(SAVE_SLOTS[slot].read_text(encoding="utf-8"))
        p=d.get("party",[])
        lead=p[0]["name"] if p else "Sem Pokémon"
        return "Nv."+str(p[0].get("level",5))+" "+lead+"  |  "+str(d.get("badges",0))+"/10 insígnias"
    except Exception:
        return "SAVE CORROMPIDO"

def draw_title():
    screen.fill((31, 87, 64))
    pygame.draw.rect(screen,(248, 238, 200),(70, 40, 628, 500))
    pygame.draw.rect(screen,(35, 65, 50),(70, 40, 628, 500),5)
    pygame.draw.rect(screen,(220, 238, 175),(110, 80, 548, 110), 3)
    draw_text("POKÉMON BRASAR",198,95,BIG,(35,65,50))
    draw_text("REGIÃO DE BRASAR",255,126,SMALL,(82,82,60))
    draw_text("FIRE RED-STYLE REMAKE / FAN REGION BRASILEIRA",150,158,SMALL,(75,90,80))
    draw_text("Biomas: Mata Atlântica • Cerrado • Pantanal • Amazônia",125,178,SMALL,(75,90,80))

    panel_x = 160
    panel_y = 205
    pygame.draw.rect(screen,(233, 228, 210),(panel_x, panel_y, 448, 195), 3)
    draw_text("INFORMAÇÕES DA REGIÃO",225,220,FONT,(35,65,50))
    draw_text("Nome: " + BRASAR_PROFILE["region_name"],185,250,SMALL,(35,65,50))
    draw_text("Lenda: " + BRASAR_PROFILE["legend"],185,273,SMALL,(35,65,50))
    draw_text("Criador da identidade: " + BRASAR_PROFILE["founder"],185,296,SMALL,(35,65,50))
    draw_text("Cidades e líderes: " + ", ".join(BRASAR_PROFILE["bosses"][:4]),185,319,SMALL,(35,65,50))
    draw_text("+ o campeão final: " + BRASAR_PROFILE["bosses"][-1],185,342,SMALL,(35,65,50))

    opts=["SLOT 1","SLOT 2","SLOT 3"]
    for i,opt in enumerate(opts):
        y=415+i*35
        if title_cursor==i: draw_text("▶",150,y,BIG,RED)
        draw_text(opt,185,y,FONT,(35,65,50))
        draw_text(_slot_label(i),285,y+2,SMALL,(80,80,60))
    draw_text("ENTER selecionar   |   ESC sair",220,485,SMALL,(35,65,50))

def handle_title_key(key):
    global title_cursor,game_mode
    if key==pygame.K_UP: title_cursor=(title_cursor-1)%3
    elif key==pygame.K_DOWN: title_cursor=(title_cursor+1)%3
    elif key in (pygame.K_RETURN,pygame.K_e):
        if SAVE_SLOTS[title_cursor].exists():
            if _load_slot(title_cursor): show_message("Save "+str(title_cursor+1)+" carregado!"); game_mode="world"
            else: show_message("Não foi possível carregar este save.")
        else:
            _new_game()
    elif key==pygame.K_ESCAPE: game_mode="quit_confirm"

def draw_pause():
    screen.fill((30,40,35))
    pygame.draw.rect(screen,WHITE,(105,35,558,505))
    pygame.draw.rect(screen,BLACK,(105,35,558,505),4)
    draw_text("MENU DE CONTROLE",235,60,BIG)
    opts=["CONTINUAR","POKÉMON","POKÉDEX","MOCHILA","SALVAR","CONTROLES","TELA INICIAL","SAIR DO JOGO"]
    for i,opt in enumerate(opts):
        y=115+i*45
        if pause_cursor==i: draw_text("▶",145,y)
        draw_text(opt,180,y)
    draw_text("ESC abre/fecha este menu",220,500,SMALL)

def handle_pause_key(key):
    global pause_cursor,game_mode,slot_cursor
    opts=8
    if key==pygame.K_UP: pause_cursor=(pause_cursor-1)%opts
    elif key==pygame.K_DOWN: pause_cursor=(pause_cursor+1)%opts
    elif key in (pygame.K_RETURN,pygame.K_e):
        if pause_cursor==0: game_mode="world"
        elif pause_cursor==1: game_mode="party"
        elif pause_cursor==2: game_mode="pokedex"
        elif pause_cursor==3: game_mode="bag"
        elif pause_cursor==4: slot_cursor=0; game_mode="save_slots"
        elif pause_cursor==5: control_cursor=0; game_mode="controls"
        elif pause_cursor==6: game_mode="title"
        elif pause_cursor==7: game_mode="quit_confirm"
    elif key==pygame.K_ESCAPE: game_mode="world"

def draw_save_slots():
    screen.fill((45,65,55)); pygame.draw.rect(screen,WHITE,(100,55,568,455)); pygame.draw.rect(screen,BLACK,(100,55,568,455),4)
    draw_text("SALVAR JOGO",300,75,BIG)
    for i in range(3):
        y=155+i*90
        if slot_cursor==i: draw_text("▶",135,y)
        draw_text("SLOT "+str(i+1),175,y)
        draw_text(_slot_label(i),175,y+30,SMALL)
    draw_text("ENTER salvar | ESC voltar",250,470,SMALL)

def handle_save_slots(key):
    global slot_cursor,game_mode
    if key==pygame.K_UP: slot_cursor=(slot_cursor-1)%3
    elif key==pygame.K_DOWN: slot_cursor=(slot_cursor+1)%3
    elif key in (pygame.K_RETURN,pygame.K_e):
        _write_slot(slot_cursor); game_mode="pause"
    elif key==pygame.K_ESCAPE: game_mode="pause"

def draw_controls():
    screen.fill((225,225,205))
    pygame.draw.rect(screen,WHITE,(100,55,568,455)); pygame.draw.rect(screen,BLACK,(100,55,568,455),4)
    draw_text("CONTROLES",310,75,BIG)
    controls=[
        "↑ ↓ ← →   Mover",
        "E         Interagir",
        "ESC       Menu de controle",
        "ENTER     Confirmar nos menus",
        "ESC       Voltar nos menus",
        "",
        "No mundo existe apenas um botão",
        "de interação: E.",
    ]
    for i,t in enumerate(controls):
        draw_text(t,170,135+i*40,SMALL if i!=0 else FONT)
    draw_text("ENTER/ESC voltar",285,470,SMALL)

def draw_quit_confirm():
    screen.fill((35,35,40)); pygame.draw.rect(screen,WHITE,(160,165,448,240)); pygame.draw.rect(screen,BLACK,(160,165,448,240),4)
    draw_text("SAIR DO JOGO?",285,200,BIG)
    draw_text("ENTER = sim",250,275,FONT)
    draw_text("ESC = não",410,275,FONT)

# Um único botão de interação no mundo: E.
def v7_interact_world():
    interact_world()

def v7_can_walk(x,y):
    mapa=get_map()
    if (current_map,x,y) in EDGE_GATES:
        return True
    if y<0 or y>=len(mapa) or x<0 or x>=len(mapa[y]): return False
    return mapa[y][x] in ".GDTNSCAL"

can_walk=v7_can_walk

def v7_move_player(dx,dy):
    global player_x,player_y,current_map
    nx,ny=player_x+dx,player_y+dy
    if not v7_can_walk(nx,ny): return
    player_x,player_y=nx,ny
    for a,ax,ay,b,bx,by,msg in V7_TRANSITIONS:
        if current_map==a and player_x==ax and player_y==ay:
            if not can_leave_city(current_map, b):
                required_leader = BRASAR_CITY_ROUTE_GATES[current_map][1]
                show_message("Derrote " + required_leader + " antes de seguir para a próxima rota.")
                return
            if b=="area_zero" and badges<10:
                show_message("A passagem está selada. Você precisa das 10 insígnias."); return
            if b=="league" and not story_flags.get("area_zero_unlocked",False):
                show_message("A Liga só pode ser acessada depois da Área Zero."); return
            current_map,player_x,player_y=b,bx,by; show_message(msg); return
    check_trainer_encounter()
    if current_map in ROUTE_ENCOUNTERS and get_map()[player_y][player_x]=="G" and random.random()<0.13:
        start_battle()

move_player=v7_move_player

# Visual de mapa V7: as saídas não parecem arbustos; são clareiras claramente marcadas.
def draw_map_v7():
    mapa=get_map(); screen.fill(LIGHT_GREEN)
    for y,row in enumerate(mapa):
        for x,tile in enumerate(row):
            rect=pygame.Rect(x*TILE,y*TILE,TILE,TILE)
            gate=(current_map,x,y) in EDGE_GATES
            if gate:
                pygame.draw.rect(screen,PATH,rect)
                pygame.draw.rect(screen,(155,125,75),rect,2)
                if x==0: draw_text("◀",rect.x+12,rect.y+10,FONT,WHITE)
                elif x==15: draw_text("▶",rect.x+12,rect.y+10,FONT,WHITE)
                else: draw_text("▼",rect.x+12,rect.y+10,FONT,WHITE)
            elif tile=="#":
                pygame.draw.rect(screen,DARK_GREEN,rect)
                # árvore/arbusto com pixel-art simples
                pygame.draw.rect(screen,(25,75,40),(rect.x+12,rect.y+20,24,20))
                pygame.draw.rect(screen,(45,120,55),(rect.x+7,rect.y+7,34,30))
                pygame.draw.rect(screen,(70,145,65),(rect.x+14,rect.y+2,20,12))
            elif tile==".":
                pygame.draw.rect(screen,PATH,rect)
            elif tile=="G":
                pygame.draw.rect(screen,GREEN,rect)
                for ox in (10,24,36):
                    pygame.draw.rect(screen,DARK_GREEN,(rect.x+ox,rect.y+24,3,15))
                    pygame.draw.rect(screen,DARK_GREEN,(rect.x+ox-3,rect.y+20,8,4))
            elif tile=="D":
                pygame.draw.rect(screen,WATER,rect)
                pygame.draw.line(screen,(160,215,245),(rect.x+5,rect.y+16),(rect.right-5,rect.y+16),2)
                pygame.draw.line(screen,(160,215,245),(rect.x+12,rect.y+32),(rect.right-8,rect.y+32),2)
            elif tile=="T":
                pygame.draw.rect(screen,(165,125,180),rect); pygame.draw.rect(screen,PURPLE,rect,3)
            elif tile=="C": draw_house(rect)
            elif tile=="S":
                pygame.draw.rect(screen,(75,105,180),rect); pygame.draw.rect(screen,WHITE,(rect.x+10,rect.y+9,28,25),2); draw_text("P",rect.x+18,rect.y+10,SMALL,WHITE)
            elif tile=="A":
                pygame.draw.rect(screen,(220,180,95),rect); pygame.draw.rect(screen,BROWN,rect,3); draw_text("A",rect.x+18,rect.y+13,SMALL,WHITE)
            elif tile=="L":
                pygame.draw.rect(screen,(90,70,110),rect); pygame.draw.rect(screen,WHITE,rect,2)
            pygame.draw.rect(screen,(80,80,70),rect,1)
    title=CITY_NAMES.get(current_map,{"route1v6":"Rota 1 — Floresta Yby","route2v6":"Rota 2 — Rios do Norte","route3v6":"Rota 3 — Desafio das Chamas","route4v6":"Rota 4 — Pampas","route5v6":"Rota 5 — Caminho de SaintPaul","route6v6":"Rota 6 — Costa de Ryo","route7v6":"Rota 7 — Minas Triangulares","route8v6":"Rota 8 — Sombras","route9v6":"Rota 9 — Grande Amazon River","route10v6":"Rota 10 — Caminho da Fortaleza"}.get(current_map,current_map))
    pygame.draw.rect(screen,(30,50,35),(0,0,WIDTH,35))
    draw_text(title,12,8,SMALL,WHITE); draw_text("Insígnias: "+str(badges)+"/10",610,8,SMALL,WHITE)
    # personagem com contorno e sombra para aproximar a leitura visual dos RPGs portáteis clássicos
    pygame.draw.ellipse(screen,(90,90,75),(player_x*TILE+10,player_y*TILE+34,28,8))
    draw_player_character(player_x*TILE+24,player_y*TILE+27)

draw_map=draw_map_v7

# Sprites maiores: contorno escuro, formas em blocos e sombra, mantendo pixel-art original.
def draw_big_pokemon_v7(name,x,y,color=None):
    if color is None: color=pokemon_color(name)
    outline=(35,35,35)
    shadow=(55,55,45)
    p=7
    # silhuetas por famílias, para não voltar aos "rostinhos".
    if name in ("Pikachu","Shinx","Canarin","Canangry"):
        body=pygame.Rect(x-28,y-24,56,55)
        pygame.draw.ellipse(screen,outline,(x-33,y-30,66,65))
        pygame.draw.ellipse(screen,color,body)
        pygame.draw.polygon(screen,outline,[(x-24,y-30),(x-43,y-52),(x-34,y-20),(x-15,y-26)])
        pygame.draw.polygon(screen,outline,[(x+24,y-30),(x+43,y-52),(x+34,y-20),(x+15,y-26)])
        pygame.draw.rect(screen,RED,(x-21,y-1,9,9)); pygame.draw.rect(screen,RED,(x+12,y-1,9,9))
        pygame.draw.rect(screen,BLACK,(x-10,y-8,6,6)); pygame.draw.rect(screen,BLACK,(x+5,y-8,6,6))
    elif name in ("Charmander","Cyndaquil","Torchic","Litten","Scorbunny","Fuecoco","Flaguar","Flatirica","Jaguarze"):
        pygame.draw.ellipse(screen,outline,(x-39,y-34,78,68))
        pygame.draw.ellipse(screen,color,(x-33,y-28,66,56))
        pygame.draw.polygon(screen,outline,[(x+25,y+15),(x+55,y+2),(x+66,y+12),(x+45,y+27)])
        pygame.draw.polygon(screen,ORANGE,[(x+43,y+12),(x+58,y+6),(x+52,y+20)])
        pygame.draw.rect(screen,BLACK,(x-19,y-8,7,7)); pygame.draw.rect(screen,BLACK,(x+12,y-8,7,7))
        pygame.draw.rect(screen,outline,(x-30,y+22,18,12)); pygame.draw.rect(screen,outline,(x+12,y+22,18,12))
    elif name in ("Squirtle","Totodile","Mudkip","Popplio","Sobble","Suriqua","Snariver","Tsuconda"):
        pygame.draw.ellipse(screen,outline,(x-42,y-31,84,65))
        pygame.draw.ellipse(screen,color,(x-35,y-25,70,53))
        pygame.draw.arc(screen,outline,(x-20,y-15,40,35),0,3.14,3)
        pygame.draw.rect(screen,outline,(x-35,y+16,18,15)); pygame.draw.rect(screen,outline,(x+17,y+16,18,15))
    elif name in ("Bulbasaur","Chikorita","Treecko","Rowlet","Grookey","Sprigatito","Macarim","Macacique","Guarilla"):
        pygame.draw.ellipse(screen,outline,(x-40,y-30,80,63))
        pygame.draw.ellipse(screen,color,(x-33,y-24,66,51))
        pygame.draw.polygon(screen,DARK_GREEN,[(x-18,y-22),(x-6,y-52),(x+4,y-22),(x+18,y-50),(x+25,y-18)])
        pygame.draw.rect(screen,outline,(x-29,y+17,18,15)); pygame.draw.rect(screen,outline,(x+11,y+17,18,15))
    else:
        pygame.draw.ellipse(screen,outline,(x-40,y-31,80,65))
        pygame.draw.ellipse(screen,color,(x-33,y-24,66,52))
        pygame.draw.rect(screen,outline,(x-27,y+18,16,13)); pygame.draw.rect(screen,outline,(x+11,y+18,16,13))
        pygame.draw.rect(screen,BLACK,(x-17,y-7,6,6)); pygame.draw.rect(screen,BLACK,(x+11,y-7,6,6))
    pygame.draw.ellipse(screen,shadow,(x-32,y+30,x*0+64,8))

draw_big_pokemon=draw_big_pokemon_v7


# ============================================================
# V8 — INTERIORES, GINÁSIOS E SPRITES PIXEL-ART MAIS CORPORAIS
# ============================================================
# O objetivo é aproximar a leitura de um RPG Pokémon portátil:
# corpo, cabeça, patas/asas/cauda e detalhes de espécie, em vez de
# círculos com olhos. Os desenhos são originais e feitos com primitivas.

V8_INTERIORS = {}
V8_BUILDING_INFO = {}
interior_return_map = None
interior_return_pos = (0, 0)
interior_kind = None

# Um pequeno interior-base reutilizável. Cada prédio ganha identidade
# visual através de paredes, balcão e NPC/objeto principal.
def _make_interior(kind):
    m = [
        "##########",
        "#........#",
        "#........#",
        "#........#",
        "#........#",
        "#........#",
        "#........#",
        "#........#",
        "#........#",
        "####..####",
    ]
    if kind == "center":
        m[2] = "#...SS...#"
        m[3] = "#...SS...#"
    elif kind == "shop":
        m[2] = "#...KK...#"
        m[3] = "#...KK...#"
    elif kind == "gym":
        m[2] = "#..AAAA..#"
        m[3] = "#..AAAA..#"
    elif kind == "house":
        m[2] = "#...TT...#"
        m[3] = "#...TT...#"
    return m

for _kind in ("center", "shop", "gym", "house"):
    V8_INTERIORS[_kind] = _make_interior(_kind)

# Coordenadas dos prédios nas cidades V6. O jogador pode entrar ao pisar
# no prédio e apertar E. Não é mais necessário adivinhar uma coordenada.
def _find_city_buildings(city):
    mapa = V6_MAPS.get(city, [])
    result = []
    for y, row in enumerate(mapa):
        for x, tile in enumerate(row):
            if tile in "CS":
                result.append((x, y, "center" if tile == "S" else "house"))
            elif tile == "A":
                result.append((x, y, "gym"))
    return result

for _city in CITY_NAMES:
    if _city in ("area_zero", "league"):
        continue
    for _x, _y, _kind in _find_city_buildings(_city):
        V8_BUILDING_INFO[(_city, _x, _y)] = _kind

# Ginásio de Victorya: a entrada é o prédio A de Amazon City, não uma
# coordenada invisível no meio da rua. Isso corrige o problema de entrada.


def v8_enter_building():
    global current_map, player_x, player_y, interior_return_map
    global interior_return_pos, interior_kind, game_mode
    if current_map not in CITY_NAMES:
        return False
    # Loja física: a placa/entrada fica na rua na posição clássica do V7.
    # Ela agora leva a um interior em vez de abrir a loja diretamente.
    if abs(player_x - 11) <= 1 and abs(player_y - 2) <= 1:
        interior_return_map = current_map
        interior_return_pos = (player_x, player_y)
        interior_kind = "shop"
        current_map = "__interior_shop"
        player_x, player_y = 5, 8
        game_mode = "world"
        show_message("Você entrou no PokéMart.")
        return True
    key = (current_map, player_x, player_y)
    kind = V8_BUILDING_INFO.get(key)
    if kind is None:
        # A entrada fica no tile caminhável imediatamente diante do prédio.
        for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            kind = V8_BUILDING_INFO.get((current_map, player_x + dx, player_y + dy))
            if kind is not None:
                break
    if kind is None:
        return False
    interior_return_map = current_map
    interior_return_pos = (player_x, player_y)
    interior_kind = kind
    current_map = "__interior_" + kind
    player_x, player_y = 5, 8
    game_mode = "world"
    names = {"house":"Casa", "center":"Centro Pokémon", "gym":"Ginásio", "shop":"Loja"}
    show_message("Você entrou em " + names[kind] + ".")
    return True


def v8_exit_building():
    global current_map, player_x, player_y, interior_return_map, interior_return_pos, interior_kind
    if not current_map.startswith("__interior_"):
        return False
    current_map = interior_return_map or "guarany"
    player_x, player_y = interior_return_pos
    interior_return_map = None
    interior_kind = None
    show_message("Você saiu do prédio.")
    return True


def v8_get_map():
    if current_map.startswith("__interior_"):
        kind = current_map.replace("__interior_", "")
        return V8_INTERIORS.get(kind, V8_INTERIORS["house"])
    return V6_MAPS.get(current_map, V6_MAPS["guarany"])

get_map = v8_get_map


def v8_can_walk(x, y):
    mapa = get_map()
    if y < 0 or y >= len(mapa) or x < 0 or x >= len(mapa[y]):
        return False
    if current_map.startswith("__interior_"):
        return mapa[y][x] in ".SKTA"
    if (current_map, x, y) in EDGE_GATES:
        return True
    return mapa[y][x] in ".GTNL"

can_walk = v8_can_walk


def v8_interact_world():
    global game_mode
    if current_map.startswith("__interior_"):
        kind = current_map.replace("__interior_", "")
        if (player_x, player_y) in [(4, 8), (5, 8)]:
            v8_exit_building()
            return
        if kind == "center" and abs(player_x - 5) <= 1 and abs(player_y - 2) <= 1:
            heal_party()
            show_message("Centro Pokémon: sua equipe foi completamente restaurada!")
            return
        if kind == "gym":
            gym = v6_city_gym(interior_return_map)
            if gym and abs(player_x - 5) <= 1 and abs(player_y - 2) <= 1:
                if badges >= gym.get("gym_index", 1):
                    show_message("Você já conquistou este ginásio.")
                elif badges < gym.get("gym_index", 1) - 1:
                    show_message("Você ainda precisa de mais insígnias para desafiar este ginásio.")
                else:
                    start_trainer_battle(gym["leader"])
                return
        if kind == "shop" and abs(player_x - 5) <= 1 and abs(player_y - 2) <= 1:
            game_mode = "shop"
            return
        if kind == "house" and abs(player_x - 5) <= 1 and abs(player_y - 2) <= 1:
            show_message("Morador: Brasar tem muitos lugares para explorar. Boa viagem!")
            return
        return

    # Primeiro tenta entrar em prédios. Isso vem antes dos antigos eventos,
    # evitando que a antiga coordenada do ginásio inicie uma batalha na rua.
    if v8_enter_building():
        return
    # Mantém todo o restante do sistema V7/V6.
    interact_world()


# O prédio S passa a ser também a porta do Centro Pokémon e K é usado apenas
# no interior da loja; a loja física é criada em frente a um dos prédios de
# serviço quando possível. Para manter os mapas existentes, o atalho antigo
# continua disponível, mas agora com interior.


def v8_move_player(dx, dy):
    global player_x, player_y, current_map
    nx, ny = player_x + dx, player_y + dy
    if not v8_can_walk(nx, ny):
        return
    player_x, player_y = nx, ny
    if current_map.startswith("__interior_"):
        if player_y == 9 and player_x in (4, 5):
            v8_exit_building()
        return
    for a, ax, ay, b, bx, by, msg in V7_TRANSITIONS:
        if current_map == a and player_x == ax and player_y == ay:
            if not can_leave_city(current_map, b):
                required_leader = BRASAR_CITY_ROUTE_GATES[current_map][1]
                show_message("Derrote " + required_leader + " antes de seguir para a próxima rota.")
                return
            if b == "area_zero" and not regional_progress_complete():
                next_gym = next_regional_gym()
                show_message("A passagem está selada. Derrote " + next_gym["leader"] + " primeiro.")
                return
            if b == "league" and not story_flags.get("area_zero_unlocked", False):
                show_message("A Liga só pode ser acessada depois da Área Zero.")
                return
            current_map, player_x, player_y = b, bx, by
            show_message(msg)
            return
    check_trainer_encounter()
    if current_map in ROUTE_ENCOUNTERS and get_map()[player_y][player_x] == "G" and random.random() < 0.13:
        start_battle()

move_player = v8_move_player


# ---------------- DERROTA: limpar completamente a batalha de treinador ----------------
def v8_defeat_player():
    global game_mode, current_map, player_x, player_y, active_index
    global trainer_battle, trainer_name, trainer_team, trainer_index
    global trainer_enemy_hp, trainer_enemy_max_hp
    if first_alive() != -1:
        return False
    # Este era o bug da V7: trainer_battle continuava True depois da derrota.
    # Ao entrar novamente na grama, a batalha selvagem herdava o treinador.
    trainer_battle = False
    trainer_name = None
    trainer_team = []
    trainer_index = 0
    trainer_enemy_hp = 0
    trainer_enemy_max_hp = 0
    heal_party()
    active_index = 0
    current_map = "guarany"
    player_x, player_y = 7, 7
    show_message("Você desmaiou e foi levado ao Centro Pokémon de Guarany Town.")
    game_mode = "world"
    return True

defeat_player = v8_defeat_player


# ---------------- SPRITES V8 ----------------
def _pix_rect(x, y, w, h, color):
    pygame.draw.rect(screen, color, pygame.Rect(int(x), int(y), int(w), int(h)))


def _sprite_palette(name):
    c = pokemon_color(name)
    dark = tuple(max(0, v - 55) for v in c)
    light = tuple(min(255, v + 45) for v in c)
    return c, dark, light


def draw_big_pokemon_v8(name, x, y, color=None):
    c, dark, light = _sprite_palette(name) if color is None else (color, tuple(max(0,v-55) for v in color), tuple(min(255,v+45) for v in color))
    o = (30, 30, 30)
    white = (245,245,235)
    # sombra de chão
    pygame.draw.ellipse(screen, (55,55,45), (x-48,y+38,96,13))

    # Cabeças/corpos muito diferentes por espécie/família.
    if name in {"Pikachu","Raichu","Shinx","Canarin","Canangry"}:
        _pix_rect(x-24,y-20,48,48,o); _pix_rect(x-19,y-16,38,40,c)
        pygame.draw.polygon(screen,o,[(x-18,y-18),(x-37,y-48),(x-31,y-8)])
        pygame.draw.polygon(screen,o,[(x+18,y-18),(x+37,y-48),(x+31,y-8)])
        pygame.draw.polygon(screen,dark,[(x-13,y-18),(x-30,y-42),(x-25,y-9)])
        pygame.draw.polygon(screen,dark,[(x+13,y-18),(x+30,y-42),(x+25,y-9)])
        _pix_rect(x-29,y+18,16,17,o); _pix_rect(x+13,y+18,16,17,o)
        _pix_rect(x-20,y+22,12,12,c); _pix_rect(x+8,y+22,12,12,c)
        _pix_rect(x-16,y-2,6,6,o); _pix_rect(x+10,y-2,6,6,o)
        if name in {"Pikachu","Raichu"}: pygame.draw.polygon(screen,o,[(x+22,y+12),(x+48,y+2),(x+57,y+13),(x+32,y+28)])
    elif name in {"Charmander","Charmeleon","Charizard","Cyndaquil","Quilava","Typhlosion","Torchic","Combusken","Blaziken","Litten","Scorbunny","Fuecoco","Flaguar","Flatirica","Jaguarze"}:
        _pix_rect(x-28,y-15,56,50,o); _pix_rect(x-22,y-10,44,40,c)
        # pernas
        for xx in (-20,10): _pix_rect(x+xx,y+22,14,20,o); _pix_rect(x+xx+3,y+24,8,15,c)
        # focinho e cauda de fogo
        _pix_rect(x-20,y-3,40,22,light)
        if name in {"Charizard","Jaguarze","Flaguar","Flatirica"}:
            pygame.draw.polygon(screen,o,[(x+18,y+10),(x+50,y-2),(x+62,y+8),(x+38,y+20)])
            pygame.draw.polygon(screen,ORANGE,[(x+35,y+7),(x+57,y+4),(x+44,y+15)])
        if name in {"Charizard"}: pygame.draw.polygon(screen,o,[(x-23,y-8),(x-52,y-28),(x-35,y+5),(x+20,y-2)])
        _pix_rect(x-14,y-1,6,6,o); _pix_rect(x+8,y-1,6,6,o)
    elif name in {"Squirtle","Wartortle","Blastoise","Totodile","Croconaw","Feraligatr","Mudkip","Marshtomp","Swampert","Popplio","Sobble","Suriqua","Snariver","Tsuconda"}:
        # Corpo baixo + carapaça/barriga + patas.
        _pix_rect(x-32,y-18,64,48,o); _pix_rect(x-26,y-13,52,38,c)
        _pix_rect(x-23,y+18,16,17,o); _pix_rect(x+7,y+18,16,17,o)
        _pix_rect(x-18,y-4,36,25,light)
        pygame.draw.line(screen,dark,(x-16,y+8),(x+16,y+8),4)
        if name in {"Blastoise","Swampert","Feraligatr","Tsuconda"}:
            _pix_rect(x-39,y-6,12,24,o); _pix_rect(x+27,y-6,12,24,o)
        if name in {"Blastoise"}: _pix_rect(x-11,y-28,22,14,o); _pix_rect(x-7,y-26,14,10,c)
        if name in {"Tsuconda"}: pygame.draw.polygon(screen,o,[(x+23,y+10),(x+52,y+4),(x+63,y+15),(x+34,y+22)])
        _pix_rect(x-14,y-2,5,5,o); _pix_rect(x+9,y-2,5,5,o)
    elif name in {"Bulbasaur","Ivysaur","Venusaur","Chikorita","Bayleef","Meganium","Treecko","Grovyle","Sceptile","Rowlet","Grookey","Sprigatito","Macarim","Macacique","Guarilla","Chloralga","Victeed"}:
        _pix_rect(x-31,y-17,62,46,o); _pix_rect(x-25,y-12,50,36,c)
        for xx in (-21,11): _pix_rect(x+xx,y+20,14,17,o); _pix_rect(x+xx+3,y+23,8,12,c)
        if name in {"Bulbasaur","Ivysaur","Venusaur"}:
            pygame.draw.polygon(screen,o,[(x-24,y-12),(x-10,y-48),(x+1,y-12),(x+15,y-48),(x+28,y-12)])
            pygame.draw.polygon(screen,DARK_GREEN,[(x-18,y-13),(x-8,y-40),(x-2,y-13),(x+14,y-40),(x+22,y-13)])
        elif name in {"Chikorita","Bayleef","Meganium"}:
            pygame.draw.polygon(screen,o,[(x-6,y-15),(x-22,y-48),(x+2,y-24),(x+19,y-45),(x+12,y-12)])
        else:
            pygame.draw.polygon(screen,DARK_GREEN,[(x-10,y-12),(x-2,y-48),(x+7,y-12),(x+20,y-39),(x+17,y-6)])
        _pix_rect(x-15,y-1,6,6,o); _pix_rect(x+9,y-1,6,6,o)
    elif name in {"Pidgey","Fletchling","Perigreen","Canindarara","Alarala","Julifly","Murizika"}:
        # Aves/insetos alados têm pescoço, asas e pernas separados.
        _pix_rect(x-18,y-8,36,37,o); _pix_rect(x-13,y-4,26,31,c)
        pygame.draw.polygon(screen,o,[(x-12,y-5),(x-43,y-20),(x-22,y+12),(x-4,y+7)])
        pygame.draw.polygon(screen,o,[(x+12,y-5),(x+43,y-20),(x+22,y+12),(x+4,y+7)])
        _pix_rect(x-7,y-28,14,21,o); _pix_rect(x-4,y-25,8,15,light)
        _pix_rect(x+5,y-22,15,6,ORANGE)
        _pix_rect(x-10,y+25,5,13,o); _pix_rect(x+5,y+25,5,13,o)
    elif name in {"Gastly","Phantag","Ghoil","Sinistea de Brasar","Polteageist de Brasar","Mimikyu de Brasar"}:
        pygame.draw.polygon(screen,o,[(x-32,y+25),(x-40,y-5),(x-25,y-28),(x,y-38),(x+25,y-28),(x+40,y-5),(x+32,y+25),(x+15,y+36),(x,y+28),(x-15,y+36)])
        pygame.draw.polygon(screen,c,[(x-27,y+22),(x-34,y-4),(x-21,y-23),(x,y-31),(x+21,y-23),(x+34,y-4),(x+27,y+22),(x+13,y+30),(x,y+23),(x-13,y+30)])
        _pix_rect(x-16,y-7,9,8,white); _pix_rect(x+8,y-7,9,8,white)
        _pix_rect(x-12,y-5,5,6,o); _pix_rect(x+8,y-5,5,6,o)
    elif name in {"Gible","Gabite","Garchomp","Tsuconda","Toxua","Tamantox","Mandimole","Jaduitan","Brigarock","Briganite"}:
        _pix_rect(x-29,y-17,58,48,o); _pix_rect(x-23,y-12,46,38,c)
        _pix_rect(x-25,y+20,17,18,o); _pix_rect(x+8,y+20,17,18,o)
        pygame.draw.polygon(screen,o,[(x-25,y-13),(x-45,y-37),(x-31,y+2)])
        pygame.draw.polygon(screen,o,[(x+25,y-13),(x+45,y-37),(x+31,y+2)])
        if name in {"Gible","Gabite","Garchomp","Tsuconda"}:
            pygame.draw.polygon(screen,light,[(x+14,y+10),(x+46,y+1),(x+52,y+13),(x+25,y+21)])
        _pix_rect(x-13,y-2,6,6,o); _pix_rect(x+9,y-2,6,6,o)
    else:
        # Silhueta corporal de reserva: cabeça + tronco + quatro apoios,
        # com cauda/asa dependendo do tipo. Nunca mais um simples rosto.
        _pix_rect(x-28,y-18,56,46,o); _pix_rect(x-22,y-13,44,36,c)
        for xx in (-20,10):
            _pix_rect(x+xx,y+18,14,20,o); _pix_rect(x+xx+3,y+20,8,15,c)
        _pix_rect(x-13,y-2,6,6,o); _pix_rect(x+8,y-2,6,6,o)
        if "Voador" in POKEMON.get(name,{}).get("type",""):
            pygame.draw.polygon(screen,o,[(x-18,y-7),(x-48,y-25),(x-32,y+9),(x-8,y+5)])
            pygame.draw.polygon(screen,o,[(x+18,y-7),(x+48,y-25),(x+32,y+9),(x+8,y+5)])
        elif "Água" in POKEMON.get(name,{}).get("type",""):
            pygame.draw.polygon(screen,o,[(x+18,y+10),(x+48,y),(x+55,y+12),(x+28,y+22)])
        else:
            pygame.draw.polygon(screen,o,[(x+20,y+10),(x+48,y+3),(x+55,y+13),(x+28,y+21)])
    # contorno visual final, sem suavização para manter aspecto pixelado.


draw_big_pokemon = draw_big_pokemon_v8

# Save/load: versão 8 guarda também se o jogador estava dentro de um prédio.
_save_data_v7 = _save_data
def _save_data_v8():
    data = _save_data_v7()
    data["version"] = 8
    data["interior_return_map"] = interior_return_map
    data["interior_return_pos"] = list(interior_return_pos)
    data["interior_kind"] = interior_kind
    return data
_save_data = _save_data_v8

_old_load_slot_v7 = _load_slot
def _load_slot_v8(slot):
    global interior_return_map, interior_return_pos, interior_kind
    ok = _old_load_slot_v7(slot)
    if ok:
        try:
            data=json.loads(SAVE_SLOTS[slot].read_text(encoding="utf-8"))
            interior_return_map=data.get("interior_return_map")
            pos=data.get("interior_return_pos",[0,0]); interior_return_pos=(int(pos[0]),int(pos[1]))
            interior_kind=data.get("interior_kind")
        except Exception:
            interior_return_map=None; interior_kind=None
    return ok
_load_slot = _load_slot_v8

# Interação única no mundo passa a usar os interiores V8.
v7_interact_world = v8_interact_world


# Tela inicial é obrigatória na V7.
game_mode="title"

# Compatibilidade: ESC abre o menu de controle no mundo; E é o único botão
# de interação do mundo. Enter/Z deixam de interagir com NPCs/objetos no mapa.



def v8_check_trainer_encounter():
    # Líderes ficam dentro dos ginásios. Assim atravessar a cidade nunca
    # dispara acidentalmente a batalha do líder.
    if current_map.startswith("__interior_"):
        if interior_kind == "gym" and (player_x, player_y) in [(5, 2), (4, 2), (6, 2)]:
            gym = v6_city_gym(interior_return_map)
            if gym and gym["leader"] not in trainer_defeated:
                if badges < gym.get("gym_index", 1) - 1:
                    show_message("O líder ainda não aceita seu desafio.")
                else:
                    start_trainer_battle(gym["leader"])
        return
    for name, info in TRAINERS.items():
        if info["map"] == current_map and info["x"] == player_x and info["y"] == player_y and name not in trainer_defeated:
            if info.get("leader"):
                continue
            if info.get("elite") and badges < 10:
                continue
            if info.get("champion") and sum(1 for n in trainer_defeated if TRAINERS.get(n, {}).get("elite")) < 4:
                continue
            start_trainer_battle(name)
            return

check_trainer_encounter = v8_check_trainer_encounter


def draw_interior_v8():
    mapa = get_map()
    screen.fill((105, 82, 62))
    kind = current_map.replace("__interior_", "")
    for y, row in enumerate(mapa):
        for x, tile in enumerate(row):
            r = pygame.Rect(x*TILE, y*TILE, TILE, TILE)
            if tile == "#":
                pygame.draw.rect(screen, (95, 67, 48), r)
                pygame.draw.rect(screen, (55, 43, 35), r, 2)
                pygame.draw.line(screen, (125, 91, 62), (r.x+5,r.y+9), (r.right-5,r.y+9), 2)
            else:
                pygame.draw.rect(screen, (190, 160, 118), r)
                pygame.draw.rect(screen, (155, 126, 91), r, 1)
            if tile == "S":
                pygame.draw.rect(screen, (235, 220, 238), r.inflate(-6,-6))
                pygame.draw.circle(screen, (220, 80, 110), (r.centerx, r.centery), 7)
                pygame.draw.line(screen, WHITE, (r.centerx-12,r.centery), (r.centerx+12,r.centery), 3)
            elif tile == "K":
                pygame.draw.rect(screen, (80, 120, 170), r.inflate(-5,-5))
                pygame.draw.rect(screen, (220, 180, 95), (r.x+7,r.y+11,34,23))
            elif tile == "A":
                pygame.draw.rect(screen, (130, 90, 150), r.inflate(-5,-5))
                pygame.draw.rect(screen, (225, 190, 90), (r.x+9,r.y+10,30,25))
            elif tile == "T":
                pygame.draw.rect(screen, (110, 75, 45), r.inflate(-6,-6))
                pygame.draw.rect(screen, (190, 135, 70), (r.x+11,r.y+10,26,28))
    if kind == "center":
        title = "CENTRO POKÉMON"
        draw_text("ENFERMEIRA", 315, 120, SMALL, WHITE)
        pygame.draw.rect(screen, (235,235,235), (295,145,180,55))
        pygame.draw.rect(screen, (40,40,40), (295,145,180,55), 2)
        draw_text("Cure sua equipe aqui", 307, 164, SMALL)
    elif kind == "gym":
        gym = v6_city_gym(interior_return_map)
        title = "GINÁSIO — " + (gym["leader"] if gym else "BRASAR")
        if gym:
            draw_text(gym["type"], 350, 120, SMALL, WHITE)
            pygame.draw.rect(screen, (75,65,90), (290,145,220,70))
            draw_text("LÍDER", 365, 157, SMALL, WHITE)
            draw_text(gym["leader"], 315, 180, FONT, WHITE)
            # treinador do ginásio desenhado com corpo, não apenas um quadrado.
            draw_character(400, 260, RED)
    elif kind == "shop":
        title = "POKÉMART"
    else:
        title = "CASA"
        draw_character(400, 190, (180, 110, 75))
        draw_text("Morador", 365, 225, SMALL, WHITE)
    draw_text(title, 15, 10, SMALL, WHITE)
    draw_text("E = interagir / porta", 500, 10, SMALL, WHITE)
    draw_player_character(player_x*TILE+24, player_y*TILE+24)


def draw_map_v8():
    if current_map.startswith("__interior_"):
        draw_interior_v8()
    else:
        draw_map_v7()

draw_map = draw_map_v8


# ============================================================
# V9 — SPRITES PIXEL ART MAIS DETALHADOS
# Referência de estilo: RPG portátil da era GBA, sem reutilizar sprites oficiais.
# ============================================================
pygame.display.set_caption("Pokémon Brasar - V9")

player_facing = "down"
player_walk_frame = 0

# O jogador agora possui cabeça, boné, cabelo, mochila, braços, pernas e
# quatro direções distintas. Os pixels são desenhados em blocos para manter
# uma aparência nítida mesmo com a resolução maior do protótipo.
def _r(x, y, w, h, c):
    pygame.draw.rect(screen, c, (int(x), int(y), int(w), int(h)))

def _outline_rect(x, y, w, h, fill, outline=(32,32,32), border=2):
    _r(x,y,w,h,outline)
    _r(x+border,y+border,w-border*2,h-border*2,fill)

def draw_character_v9(cx, cy, color, facing=None, step=None, npc=False):
    # Sombras pequenas fazem o personagem parecer apoiado no chão.
    pygame.draw.ellipse(screen, (55,55,48), (cx-12, cy+19, 24, 7))
    if facing is None:
        facing = player_facing if color == BLUE and not npc else "down"
    if step is None:
        step = player_walk_frame if color == BLUE and not npc else 0

    skin=(240,194,150)
    hair=(74,48,32)
    cap=(205,52,48) if not npc else color
    shirt=(62,103,190) if color == BLUE else color
    pants=(48,62,92)
    outline=(30,30,34)
    light=tuple(min(255,v+35) for v in shirt)

    # Posição das pernas alterna nos frames de caminhada.
    left_leg = -5 if step % 2 == 0 else -7
    right_leg = 5 if step % 2 == 0 else 7

    if facing == "up":
        # Mochila e costas.
        _outline_rect(cx-11,cy-3,22,20,shirt,outline)
        _outline_rect(cx-14,cy+1,6,14,(110,78,55),outline)
        _outline_rect(cx+8,cy+1,6,14,(110,78,55),outline)
        _outline_rect(cx-9,cy-15,18,14,hair,outline)
        _r(cx-10,cy-18,20,5,outline); _r(cx-8,cy-17,16,3,cap)
        _outline_rect(cx+left_leg-4,cy+15,8,13,pants,outline)
        _outline_rect(cx+right_leg-4,cy+15,8,13,pants,outline)
        _r(cx+left_leg-5,cy+26,10,4,outline); _r(cx+right_leg-5,cy+26,10,4,outline)
    elif facing == "left" or facing == "right":
        sign=-1 if facing=="left" else 1
        _outline_rect(cx-8,cy-13,16,15,skin,outline)
        # Boné lateral com aba.
        _r(cx-9,cy-19,18,7,outline); _r(cx-7,cy-18,14,5,cap)
        _r(cx+sign*7,cy-16,8,4,outline); _r(cx+sign*7,cy-15,7,2,cap)
        _outline_rect(cx-10,cy+1,20,18,shirt,outline)
        _r(cx+sign*8,cy+5,6,11,outline); _r(cx+sign*8,cy+7,4,8,skin)
        _outline_rect(cx+left_leg-4,cy+17,8,12,pants,outline)
        _outline_rect(cx+right_leg-4,cy+17,8,12,pants,outline)
        _r(cx+sign*3,cy-7,3,3,hair)
        _r(cx+sign*5,cy-7,3,3,outline)
    else:
        # Frente: rosto, boné, camisa, braços e pernas separados.
        _outline_rect(cx-9,cy-14,18,16,skin,outline)
        _r(cx-11,cy-20,22,7,outline); _r(cx-9,cy-19,18,5,cap)
        _r(cx-13,cy-16,7,4,outline); _r(cx-12,cy-15,6,2,cap)
        _r(cx+6,cy-16,7,4,outline); _r(cx+6,cy-15,6,2,cap)
        _r(cx-5,cy-7,3,3,outline); _r(cx+3,cy-7,3,3,outline)
        _outline_rect(cx-11,cy+1,22,18,shirt,outline)
        _r(cx-8,cy+3,16,4,light)
        _r(cx-16,cy+4,6,13,outline); _r(cx-14,cy+6,4,9,skin)
        _r(cx+10,cy+4,6,13,outline); _r(cx+10,cy+6,4,9,skin)
        _outline_rect(cx+left_leg-4,cy+17,8,12,pants,outline)
        _outline_rect(cx+right_leg-4,cy+17,8,12,pants,outline)
        _r(cx+left_leg-5,cy+26,10,4,outline); _r(cx+right_leg-5,cy+26,10,4,outline)

# Mantém a API antiga: NPCs que chamam draw_character também recebem um corpo
# completo, em vez dos círculos e retângulos simplificados da versão anterior.
def draw_character(cx, cy, color):
    draw_character_v9(cx, cy, color, npc=(color != BLUE))


PLAYER_SPRITE_COLOR = (65, 115, 210)


def draw_player_character(cx, cy):
    draw_character_v9(cx, cy, PLAYER_SPRITE_COLOR, facing=player_facing, step=player_walk_frame, npc=False)

# Movimentação atualiza a direção e alterna os frames de caminhada.
_move_player_v8 = move_player
def move_player_v9(dx, dy):
    global player_facing, player_walk_frame
    if dx < 0: player_facing="left"
    elif dx > 0: player_facing="right"
    elif dy < 0: player_facing="up"
    elif dy > 0: player_facing="down"
    old=(player_x,player_y,current_map)
    _move_player_v8(dx,dy)
    if old != (player_x,player_y,current_map):
        player_walk_frame=(player_walk_frame+1)%2
move_player = move_player_v9

# ---------- sprites de batalha V9 ----------
# A V8 já separava várias famílias. A V9 acrescenta detalhes individuais e
# poses mais legíveis para espécies importantes, mantendo uma silhueta própria.
_draw_big_pokemon_v8 = draw_big_pokemon

def _eye(x,y,scale=1):
    _r(x,y,5*scale,5*scale,(28,28,28))
    if scale>1: _r(x+scale,y+scale,scale,scale,(245,245,240))

def draw_big_pokemon_v9(name, x, y, color=None):
    # Espécies com desenho individual mais reconhecível.
    c,dark,light=_sprite_palette(name) if color is None else (color,tuple(max(0,v-55) for v in color),tuple(min(255,v+45) for v in color))
    o=(28,28,30)
    pygame.draw.ellipse(screen,(55,55,48),(x-52,y+39,104,14))

    if name in {"Eevee","Vaporeon","Jolteon","Flareon"}:
        # Raposa: cabeça distinta, orelhas grandes, peito e cauda.
        pygame.draw.polygon(screen,o,[(x-30,y+25),(x-35,y-15),(x-27,y-35),(x-8,y-12),(x+5,y-44),(x+24,y-14),(x+33,y+20)])
        pygame.draw.polygon(screen,c,[(x-25,y+22),(x-29,y-13),(x-25,y-28),(x-8,y-7),(x+6,y-36),(x+18,y-11),(x+27,y+17)])
        pygame.draw.polygon(screen,o,[(x+25,y+10),(x+60,y-4),(x+67,y+12),(x+35,y+25)])
        pygame.draw.polygon(screen,light,[(x+31,y+11),(x+57,y+2),(x+59,y+12),(x+34,y+20)])
        _eye(x-11,y-2); _eye(x+9,y-2)
        _r(x-10,y+13,20,5,light)
        for xx in (-19,8): _outline_rect(x+xx,y+20,12,16,c,o)
    elif name in {"Riolu","Lucario","Ralts","Kirlia","Gardevoir"}:
        # Humanoide: tronco, braços, pernas e cabeça claramente separados.
        _outline_rect(x-18,y-20,36,35,c,o)
        _outline_rect(x-15,y-48,30,31,light,o)
        pygame.draw.polygon(screen,dark,[(x-13,y-43),(x-28,y-60),(x-17,y-30)])
        pygame.draw.polygon(screen,dark,[(x+13,y-43),(x+28,y-60),(x+17,y-30)])
        _eye(x-9,y-35); _eye(x+5,y-35)
        _r(x-31,y-13,13,8,o); _r(x+18,y-13,13,8,o)
        for xx in (-14,5): _outline_rect(x+xx,y+13,10,28,dark,o)
    elif name in {"Dratini","Dragonair","Dragonite","Allicuca","Dracuca","Kuckagron"}:
        # Dragões e serpentes: corpo longo, pescoço e cabeça separados.
        pygame.draw.lines(screen,o,False,[(x-54,y+25),(x-38,y-4),(x-16,y+12),(x+4,y-17),(x+25,y+3)],22)
        pygame.draw.lines(screen,c,False,[(x-52,y+24),(x-37,y-3),(x-15,y+11),(x+5,y-15),(x+24,y+3)],14)
        _outline_rect(x+14,y-32,34,31,c,o)
        pygame.draw.polygon(screen,o,[(x+38,y-30),(x+61,y-20),(x+39,y-12)])
        _eye(x+25,y-23); _r(x+30,y-10,12,4,light)
    elif name in {"Wooloo de Brasar","Dubwool de Brasar","Lamblet","Corneiro"}:
        # Ovelhas: lã irregular e quatro patas curtas.
        for ox,oy,r in [(-22,-15,22),(0,-24,25),(22,-13,22),(-8,2,25),(17,5,20)]:
            pygame.draw.circle(screen,o,(x+ox,y+oy),r)
            pygame.draw.circle(screen,light,(x+ox,y+oy),max(3,r-4))
        _outline_rect(x+22,y-19,26,24,c,o)
        _eye(x+30,y-11); _r(x+38,y+2,8,3,o)
        for xx in (-25,-4,18,36): _outline_rect(x+xx,y+18,8,20,dark,o)
    else:
        _draw_big_pokemon_v8(name,x,y,color)
        return

draw_big_pokemon = draw_big_pokemon_v9

# Interface de batalha V9: contornos mais próximos de um RPG portátil clássico,
# com plataformas em camadas e o Pokémon do jogador posicionado como aliado.
_draw_battle_v8 = draw_battle
def draw_battle_v9():
    screen.fill((215,232,198))
    # Faixas de fundo e plataformas em pixels, sem copiar assets oficiais.
    for yy in range(0,450,18):
        if yy%36==0: pygame.draw.line(screen,(205,224,187),(0,yy),(WIDTH,yy),1)
    pygame.draw.ellipse(screen,(83,130,70),(430,130,275,72))
    pygame.draw.ellipse(screen,(120,172,92),(442,120,250,58))
    pygame.draw.ellipse(screen,(83,130,70),(48,355,305,75))
    pygame.draw.ellipse(screen,(120,172,92),(62,345,278,58))
    idx=first_alive(); own=party[idx] if idx>=0 else None; enemy=get_enemy()
    if enemy: draw_big_pokemon(enemy["name"],565,154)
    if own: draw_big_pokemon(own["name"],205,370)
    if enemy:
        _outline_rect(25,28,365,132,WHITE,(35,35,35),3)
        label=(trainer_name+": " if trainer_battle else "")+enemy["name"]
        draw_text(label+"  Nv."+str(enemy["level"]),45,45)
        draw_text(enemy["type"],45,75,SMALL)
        draw_hp_bar(45,108,275,enemy["hp"],enemy["max_hp"])
        draw_text("HP",330,105,SMALL)
    if own:
        _outline_rect(375,268,355,158,WHITE,(35,35,35),3)
        draw_text(own["name"]+"  Nv."+str(own["level"]),398,286)
        draw_text(own["type"],398,315,SMALL)
        draw_hp_bar(398,343,250,own["hp"],own["max_hp"])
        draw_text(str(own["hp"])+"/"+str(own["max_hp"]),575,367,SMALL)
        draw_text("EXP",398,391,SMALL)
        ratio=own["xp"]/max(1,own["xp_to_next"])
        pygame.draw.rect(screen,(35,35,35),(440,394,230,10))
        pygame.draw.rect(screen,BLUE,(443,397,int(224*max(0,min(1,ratio))),4))
    pygame.draw.rect(screen,WHITE,(0,450,WIDTH,126)); pygame.draw.rect(screen,(35,35,35),(0,450,WIDTH,126),4)
    if v6_battle_bag:
        names=[("Pokébola",pokeballs),("Poção",items.get("Poção",0)),("Super Poção",items.get("Super Poção",0)),("Antídoto",items.get("Antídoto",0))]
        draw_text("MOCHILA",42,462,BIG)
        for i,(n,q) in enumerate(names):
            yy=505+(i%2)*30; xx=50+(i//2)*330
            if v6_bag_cursor==i: draw_text(">",xx-22,yy)
            draw_text(n+" x"+str(q),xx,yy,SMALL)
    elif battle_state=="menu":
        for i,opt in enumerate(["LUTAR","POKÉMON","MOCHILA","FUGIR"]):
            xx=70+(i%2)*330; yy=465+(i//2)*48
            if battle_cursor==i: draw_text(">",xx-25,yy)
            draw_text(opt,xx,yy)
    elif battle_state=="fight" and own:
        for i in range(4):
            xx=60+(i%2)*330; yy=465+(i//2)*45
            if i<len(own["moves"]):
                if battle_cursor==i: draw_text(">",xx-25,yy)
                m=own["moves"][i]; pp=own.get("move_pp",{}).get(m,MOVE_DATA.get(m,{"pp":0})["pp"])
                draw_text(m+" PP "+str(pp),xx,yy)
            else: draw_text("---",xx,yy)

draw_battle = draw_battle_v9

# Informação visual da versão no título, sem quebrar o sistema de saves V8.
_draw_title_v8 = draw_title
def draw_title_v9():
    _draw_title_v8()
    draw_text("VERSÃO 9 — PIXEL SPRITES", 255, 535, SMALL, WHITE)
draw_title = draw_title_v9



# ============================================================
# V10 — SPRITES INDIVIDUAIS DOS POKÉMON DE BRASAR
# Modelagem em pixel art inspirada em sprites portáteis clássicos:
# silhueta primeiro, contorno escuro, cores em blocos e sombreamento.
# Os desenhos abaixo são originais do jogo e não reutilizam sprites externos.
# ============================================================
pygame.display.set_caption("Pokémon Brasar - V10")

_V10_OUT = (30, 31, 36)

def _v10_rect(x, y, w, h, c):
    pygame.draw.rect(screen, c, (round(x), round(y), round(w), round(h)))

def _v10_poly(points, fill, outline=_V10_OUT, width=0):
    pts=[(round(px/2)*2, round(py/2)*2) for px,py in points]
    if outline:
        pygame.draw.polygon(screen, outline, pts)
        if width==0:
            # Uma segunda forma levemente reduzida não funciona bem para todos
            # os polígonos; usamos contorno de pixel depois.
            pygame.draw.polygon(screen, fill, pts)
            pygame.draw.lines(screen, outline, True, pts, 3)
        else:
            pygame.draw.polygon(screen, fill, pts)
            pygame.draw.lines(screen, outline, True, pts, width)
    else:
        pygame.draw.polygon(screen, fill, pts)

def _v10_ellipse(rect, fill, outline=_V10_OUT, width=3):
    pygame.draw.ellipse(screen, fill, rect)
    if outline:
        pygame.draw.ellipse(screen, outline, rect, width)

def _v10_eye(x, y, iris=(50,70,60), angry=False):
    _v10_rect(x-7,y-10,14,20,(242,242,235))
    _v10_rect(x-8,y-11,16,22,_V10_OUT)
    _v10_rect(x-5,y-8,10,16,(238,238,230))
    if angry:
        _v10_poly([(x-8,y-11),(x+7,y-8),(x+6,y-4),(x-8,y-7)],_V10_OUT,None)
    _v10_ellipse((x-3,y-4,7,12),iris,None)
    _v10_rect(x,y-2,3,5,(255,255,255))

def _v10_shadow(x,y,w=112):
    pygame.draw.ellipse(screen,(58,65,56),(x-w//2,y-7,w,14))

def _v10_cat(name,x,y,c,dark,light):
    """Flaguar/Flatirica/Jaguarze: felinos com cauda e patas reais."""
    scale={"Flaguar":0.82,"Flatirica":1.0,"Jaguarze":1.18}.get(name,1.0)
    s=scale
    _v10_shadow(x,y+48,int(105*s))
    # cauda curva em segmentos pixelados
    tail_dark = (45,43,48) if name=="Jaguarze" else dark
    pts=[(x+20*s,y+18*s),(x+48*s,y+7*s),(x+63*s,y-13*s),(x+58*s,y-29*s),
         (x+68*s,y-39*s),(x+77*s,y-28*s),(x+75*s,y-6*s),(x+59*s,y+22*s),
         (x+31*s,y+36*s)]
    _v10_poly(pts,c)
    _v10_poly([(x+60*s,y-30*s),(x+69*s,y-39*s),(x+77*s,y-28*s),(x+72*s,y-16*s)],tail_dark)
    # corpo quadrúpede
    _v10_ellipse((x-39*s,y-4*s,74*s,52*s),c)
    _v10_ellipse((x-30*s,y+9*s,47*s,33*s),light,None)
    # cabeça e orelhas
    _v10_poly([(x-42*s,y+12*s),(x-48*s,y-26*s),(x-32*s,y-43*s),(x-12*s,y-27*s),
               (x+9*s,y-48*s),(x+27*s,y-29*s),(x+25*s,y+6*s),(x+8*s,y+22*s),(x-25*s,y+23*s)],c)
    _v10_poly([(x-39*s,y-25*s),(x-33*s,y-39*s),(x-25*s,y-23*s)],(210,120,125))
    _v10_poly([(x+5*s,y-29*s),(x+10*s,y-43*s),(x+18*s,y-27*s)],(210,120,125))
    # focinho e olhos
    _v10_ellipse((x-32*s,y-2*s,40*s,24*s),(235,232,215))
    _v10_eye(x-19*s,y-9*s,(75,155,150),name!="Flaguar")
    _v10_eye(x+3*s,y-10*s,(75,155,150),name!="Flaguar")
    _v10_rect(x-11*s,y+2*s,10*s,5*s,(200,90,95))
    _v10_rect(x-7*s,y+9*s,14*s,3*s,_V10_OUT)
    # manchas e patas
    for ox,oy in [(-4,14),(18,21)]:
        _v10_ellipse((x+ox*s,y+oy*s,8*s,13*s),tail_dark,None)
    for ox,oy in [(-29,31),(5,33)]:
        _v10_rect(x+ox*s,y+oy*s,16*s,23*s,c)
        _v10_rect(x+(ox-2)*s,y+(oy+19)*s,20*s,8*s,tail_dark)
    if name=="Jaguarze":
        # juba escura e chama na ponta da cauda
        _v10_poly([(x-42*s,y-16*s),(x-52*s,y-28*s),(x-39*s,y-22*s),(x-45*s,y-38*s),
                   (x-28*s,y-27*s),(x-18*s,y-40*s),(x-9*s,y-24*s)],(48,49,57))
        _v10_poly([(x+66*s,y-43*s),(x+75*s,y-65*s),(x+81*s,y-45*s),(x+87*s,y-58*s),
                   (x+90*s,y-38*s),(x+76*s,y-26*s)],(245,125,40))
        _v10_poly([(x+74*s,y-54*s),(x+80*s,y-63*s),(x+83*s,y-46*s)],(255,215,65),None)

def _v10_monkey(name,x,y,c,dark,light):
    """Macarim/Macacique/Guarilla: primatas com membros, orelhas e folhas."""
    scale={"Macarim":0.78,"Macacique":1.0,"Guarilla":1.18}.get(name,1.0); s=scale
    _v10_shadow(x,y+50,int(110*s))
    # cauda
    _v10_poly([(x+19*s,y+15*s),(x+47*s,y+7*s),(x+56*s,y-13*s),(x+46*s,y-25*s),
               (x+40*s,y-13*s),(x+45*s,y-1*s),(x+23*s,y+6*s)],dark)
    # pernas
    for ox in (-20,8):
        _v10_rect(x+ox*s,y+20*s,16*s,29*s,dark)
        _v10_ellipse((x+(ox-4)*s,y+43*s,25*s,11*s),dark)
    # tronco
    _v10_ellipse((x-28*s,y-10*s,58*s,52*s),c)
    # braços longos
    _v10_poly([(x-25*s,y),(x-46*s,y+8*s),(x-51*s,y+30*s),(x-39*s,y+36*s),
               (x-30*s,y+17*s),(x-13*s,y+12*s)],c)
    _v10_poly([(x+23*s,y-2*s),(x+42*s,y+8*s),(x+50*s,y+27*s),(x+39*s,y+34*s),
               (x+25*s,y+16*s),(x+10*s,y+11*s)],c)
    # cabeça e grandes orelhas
    _v10_ellipse((x-24*s,y-49*s,48*s,45*s),light)
    _v10_ellipse((x-50*s,y-39*s,25*s,31*s),c)
    _v10_ellipse((x+25*s,y-39*s,25*s,31*s),c)
    _v10_ellipse((x-44*s,y-34*s,13*s,21*s),(170,105,85),None)
    _v10_ellipse((x+31*s,y-34*s,13*s,21*s),(170,105,85),None)
    # focinho e olhos
    _v10_ellipse((x-13*s,y-24*s,26*s,18*s),(170,115,80))
    _v10_eye(x-9*s,y-33*s,(230,85,60),name!="Macarim")
    _v10_eye(x+8*s,y-33*s,(230,85,60),name!="Macarim")
    _v10_rect(x-5*s,y-18*s,10*s,4*s,(75,55,45))
    # folhas no topo
    leaf=(42,135,70)
    _v10_poly([(x-7*s,y-49*s),(x-23*s,y-76*s),(x-5*s,y-57*s)],leaf)
    _v10_poly([(x+2*s,y-50*s),(x+25*s,y-74*s),(x+10*s,y-53*s)],leaf)
    if name=="Guarilla":
        _v10_poly([(x-38*s,y-8*s),(x-60*s,y-23*s),(x-48*s,y+4*s)],dark)
        _v10_poly([(x+37*s,y-8*s),(x+58*s,y-23*s),(x+48*s,y+5*s)],dark)

def _v10_snake(name,x,y,c,dark,light):
    """Suriqua/Snariver/Tsuconda: serpente aquática com corpo sinuoso."""
    scale={"Suriqua":0.78,"Snariver":1.0,"Tsuconda":1.22}.get(name,1.0); s=scale
    _v10_shadow(x,y+48,int(128*s))
    path=[(x-56*s,y+28*s),(x-38*s,y+2*s),(x-12*s,y+23*s),(x+8*s,y+5*s),
          (x+27*s,y+25*s),(x+47*s,y+4*s)]
    pygame.draw.lines(screen,_V10_OUT,False,path,int(23*s))
    pygame.draw.lines(screen,c,False,path,int(15*s))
    # cabeça levantada
    _v10_ellipse((x+20*s,y-48*s,47*s,39*s),c)
    _v10_poly([(x+58*s,y-38*s),(x+77*s,y-29*s),(x+61*s,y-21*s)],c)
    _v10_eye(x+45*s,y-35*s,(80,180,220),name!="Suriqua")
    _v10_rect(x+56*s,y-19*s,11*s,3*s,_V10_OUT)
    # barriga e marcas
    _v10_ellipse((x+29*s,y-21*s,27*s,15*s),light,None)
    for ox,oy in [(-33,6),(-7,20),(16,12)]:
        _v10_ellipse((x+ox*s,y+oy*s,8*s,12*s),dark,None)
    if name=="Tsuconda":
        _v10_poly([(x+25*s,y-48*s),(x+32*s,y-67*s),(x+41*s,y-48*s)],dark)
        _v10_poly([(x+51*s,y-48*s),(x+59*s,y-67*s),(x+64*s,y-43*s)],dark)
        # fumaça/névoa característica
        for ox,oy,r in [(-5,-24,8),(7,-37,7),(19,-50,6)]:
            _v10_ellipse((x+ox*s,y+oy*s,r*s,r*s),(190,220,225),None)

def _v10_bird(name,x,y,c,dark,light):
    """Perigreen/Canindarara/Alarala/Canarin: aves com bico, asas e pés."""
    scale={"Perigreen":0.8,"Canindarara":1.0,"Alarala":1.22,"Canarin":0.68}.get(name,1.0); s=scale
    _v10_shadow(x,y+50,int(100*s))
    _v10_ellipse((x-26*s,y-17*s,52*s,55*s),c)
    _v10_ellipse((x-32*s,y-50*s,43*s,45*s),light)
    # bico
    beak=(245,150,55) if name!="Canarin" else (235,205,50)
    _v10_poly([(x-35*s,y-34*s),(x-59*s,y-25*s),(x-35*s,y-16*s)],beak)
    _v10_eye(x-16*s,y-34*s,(55,55,55))
    # asa e cauda
    _v10_poly([(x-1*s,y-10*s),(x+35*s,y+2*s),(x+50*s,y+23*s),(x+16*s,y+20*s)],dark)
    _v10_poly([(x+22*s,y+9*s),(x+68*s,y+17*s),(x+35*s,y+30*s)],c)
    # pernas
    for ox in (-10,8):
        _v10_rect(x+ox*s,y+34*s,4*s,17*s,(150,95,45))
        _v10_poly([(x+(ox-4)*s,y+50*s),(x+(ox+9)*s,y+50*s),(x+(ox+2)*s,y+54*s)],(150,95,45),None)
    if name=="Alarala":
        for col,ox in [((220,55,55),-3),((60,110,210),8),((245,205,55),19)]:
            _v10_poly([(x+ox*s,y-14*s),(x+(ox+18)*s,y+5*s),(x+(ox+28)*s,y+25*s)],col)
    if name=="Canarin":
        _v10_poly([(x-3*s,y-48*s),(x+6*s,y-68*s),(x+12*s,y-47*s)],(235,205,50))

def _v10_bug(name,x,y,c,dark,light):
    """Grubey/Julifly/Murizika: insetos com segmentos e asas."""
    scale={"Grubey":0.72,"Julifly":0.92,"Murizika":1.08}.get(name,1.0); s=scale
    _v10_shadow(x,y+42,int(96*s))
    # abdômen segmentado
    for i in range(3):
        _v10_ellipse((x+(-8+i*13)*s,y+(i*2)*s,26*s,22*s), c if i<2 else dark)
    _v10_ellipse((x-34*s,y-18*s,30*s,30*s),light)
    _v10_eye(x-24*s,y-10*s,(50,50,55))
    # antenas
    pygame.draw.line(screen,_V10_OUT,(x-25*s,y-20*s),(x-38*s,y-36*s),3)
    pygame.draw.line(screen,_V10_OUT,(x-15*s,y-22*s),(x-10*s,y-40*s),3)
    # asas para formas evoluídas
    if name!="Grubey":
        _v10_ellipse((x-5*s,y-35*s,39*s,32*s),(180,220,235),_V10_OUT,2)
        _v10_ellipse((x+12*s,y-24*s,43*s,30*s),(165,205,230),_V10_OUT,2)
    # pernas
    for ox in (-22,-8,8):
        pygame.draw.line(screen,_V10_OUT,(x+ox*s,y+15*s),(x+(ox-10)*s,y+33*s),3)
    if name=="Murizika":
        _v10_poly([(x+22*s,y-2*s),(x+47*s,y-14*s),(x+38*s,y+9*s)],(130,75,175))

def _v10_plant(name,x,y,c,dark,light):
    """Chloralga/Victeed/Guaramite/Guaraviton: plantas com folhas e corpo."""
    scale={"Chloralga":0.82,"Victeed":1.04,"Guaramite":0.85,"Guaraviton":1.08}.get(name,1.0); s=scale
    _v10_shadow(x,y+48,int(105*s))
    if name in {"Guaramite","Guaraviton"}:
        berry=(175,45,40)
        for ox,oy,r in [(-17,-8,20),(17,-10,22),(5,18,24)]:
            _v10_ellipse((x+(ox-r)*s,y+(oy-r)*s,2*r*s,2*r*s),berry)
            _v10_eye(x+(ox-5)*s,y+(oy-3)*s,(65,65,65))
        for ox,oy in [(-25,-30),(8,-37),(29,-20),(-28,17),(23,27)]:
            _v10_poly([(x+ox*s,y+oy*s),(x+(ox+18)*s,y+(oy-11)*s),(x+(ox+14)*s,y+(oy+13)*s)],(48,125,65))
        return
    # corpo vegetal
    _v10_ellipse((x-25*s,y-40*s,50*s,45*s),light)
    _v10_eye(x-10*s,y-25*s,(65,65,65))
    _v10_eye(x+10*s,y-25*s,(65,65,65))
    _v10_poly([(x-12*s,y-43*s),(x-25*s,y-68*s),(x-4*s,y-50*s)],(195,105,145))
    _v10_poly([(x+1*s,y-47*s),(x+22*s,y-64*s),(x+11*s,y-43*s)],(195,105,145))
    _v10_poly([(x-19*s,y+1*s),(x-48*s,y+12*s),(x-24*s,y+22*s)],c)
    _v10_poly([(x+17*s,y+1*s),(x+48*s,y+12*s),(x+23*s,y+23*s)],c)
    _v10_poly([(x-5*s,y+2*s),(x-16*s,y+35*s),(x,y+48*s)],dark)
    _v10_poly([(x+5*s,y+2*s),(x+17*s,y+35*s),(x,y+48*s)],dark)
    if name=="Victeed":
        for ox,oy in [(-47,28),(-28,37),(22,37),(43,25)]:
            _v10_ellipse((x+ox*s,y+oy*s,30*s,12*s),(160,205,95))
        pygame.draw.line(screen,(80,120,55),(x-3*s,y+38*s),(x-43*s,y+31*s),3)
        pygame.draw.line(screen,(80,120,55),(x+4*s,y+38*s),(x+43*s,y+29*s),3)

def draw_big_pokemon_v10(name, x, y, color=None):
    c,dark,light = _sprite_palette(name) if color is None else (
        color, tuple(max(0,v-55) for v in color), tuple(min(255,v+45) for v in color)
    )
    if name in {"Macarim","Macacique","Guarilla"}:
        _v10_monkey(name,x,y,c,dark,light)
    elif name in {"Flaguar","Flatirica","Jaguarze"}:
        _v10_cat(name,x,y,c,dark,light)
    elif name in {"Suriqua","Snariver","Tsuconda"}:
        _v10_snake(name,x,y,c,dark,light)
    elif name in {"Perigreen","Canindarara","Alarala","Canarin"}:
        _v10_bird(name,x,y,c,dark,light)
    elif name in {"Grubey","Julifly","Murizika"}:
        _v10_bug(name,x,y,c,dark,light)
    elif name in {"Chloralga","Choralga","Victeed","Guaramite","Guaraviton"}:
        _v10_plant(name,x,y,c,dark,light)
    else:
        # As demais espécies continuam usando o renderizador V9 até receberem
        # uma silhueta individual específica, sem quebrar o jogo.
        draw_big_pokemon_v9(name,x,y,color)

draw_big_pokemon = draw_big_pokemon_v10

# ============================================================
# LOOP PRINCIPAL V7
# ============================================================

running = __name__ == "__main__"
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        elif event.type==pygame.KEYDOWN:
            key=event.key

            if game_mode=="title":
                handle_title_key(key)

            elif game_mode=="protagonist_select":
                handle_protagonist_key(key)

            elif game_mode=="version_select":
                handle_version_key(key)

            elif game_mode=="opening_house":
                handle_opening_house_key(key)

            elif game_mode=="starter":
                if key in [pygame.K_1,pygame.K_2,pygame.K_3]:
                    name={pygame.K_1:"Macarim",pygame.K_2:"Flaguar",pygame.K_3:"Suriqua"}[key]
                    party.append(create_pokemon(name,5))
                    pokedex.add(name)
                    story_flags["starter_received"]=True
                    game_mode="world"
                    show_message("Você escolheu "+name+"!")

            elif game_mode=="world":
                if key==pygame.K_UP: move_player(0,-1)
                elif key==pygame.K_DOWN: move_player(0,1)
                elif key==pygame.K_LEFT: move_player(-1,0)
                elif key==pygame.K_RIGHT: move_player(1,0)
                elif key==V7_INTERACT_KEY: v7_interact_world()
                elif key==V7_PAUSE_KEY: game_mode="pause"; pause_cursor=0

            elif game_mode=="pause":
                handle_pause_key(key)

            elif game_mode=="save_slots":
                handle_save_slots(key)

            elif game_mode=="controls":
                if key in [pygame.K_ESCAPE,pygame.K_RETURN,pygame.K_e]:
                    game_mode="pause"

            elif game_mode=="quit_confirm":
                if key==pygame.K_RETURN: running=False
                elif key==pygame.K_ESCAPE: game_mode="pause"

            elif game_mode=="menu":
                handle_menu_key(key)
            elif game_mode=="party":
                handle_party_key(key)
            elif game_mode=="pokedex":
                if key in [pygame.K_ESCAPE,pygame.K_x]: game_mode="pause"
            elif game_mode=="bag":
                if key==pygame.K_UP: menu_cursor=(menu_cursor-1)%4
                elif key==pygame.K_DOWN: menu_cursor=(menu_cursor+1)%4
                elif key in [pygame.K_RETURN,pygame.K_e]: use_item(["Pokébola","Poção","Super Poção","Antídoto"][menu_cursor])
                elif key in [pygame.K_ESCAPE,pygame.K_x]: game_mode="pause"
            elif game_mode=="shop":
                handle_shop_key(key)
            elif game_mode=="battle":
                handle_battle_key(key)
            elif game_mode=="ending":
                if key in [pygame.K_ESCAPE,pygame.K_RETURN,pygame.K_e]: game_mode="world"

    if game_mode=="title":
        draw_title()
    elif game_mode=="protagonist_select": draw_protagonist_select()
    elif game_mode=="version_select": draw_version_select()
    elif game_mode=="opening_house": draw_opening_house()
    elif game_mode=="world":
        draw_map()
        if message_timer>0:
            pygame.draw.rect(screen,WHITE,(35,480,WIDTH-70,70))
            pygame.draw.rect(screen,BLACK,(35,480,WIDTH-70,70),3)
            draw_text(message,55,505)
            message_timer-=1
    elif game_mode=="starter": draw_starter_screen()
    elif game_mode=="battle":
        draw_battle()
        if message_timer>0:
            pygame.draw.rect(screen,WHITE,(35,480,WIDTH-70,70))
            pygame.draw.rect(screen,BLACK,(35,480,WIDTH-70,70),3)
            draw_text(message,55,505)
            message_timer-=1
    elif game_mode=="pause": draw_pause()
    elif game_mode=="save_slots": draw_save_slots()
    elif game_mode=="controls": draw_controls()
    elif game_mode=="quit_confirm": draw_quit_confirm()
    elif game_mode=="menu": draw_menu()
    elif game_mode=="party": draw_party_screen()
    elif game_mode=="pokedex": draw_pokedex_screen()
    elif game_mode=="bag": draw_bag_screen()
    elif game_mode=="shop": draw_shop()
    elif game_mode=="ending": draw_ending()

    pygame.display.flip()

if __name__ == "__main__":
    pygame.quit()
    sys.exit()
