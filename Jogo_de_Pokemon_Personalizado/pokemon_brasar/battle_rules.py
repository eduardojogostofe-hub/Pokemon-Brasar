"""Regras determinísticas e orientadas a dados para batalhas de Pokémon Brasar."""

import random


def pokemon_types(type_text):
    return [part.strip() for part in type_text.split("/")]


def type_effectiveness(move_type, defender_type, effectiveness):
    multiplier = 1.0
    for defender in pokemon_types(defender_type):
        multiplier *= effectiveness.get((move_type, defender), 1.0)
    return multiplier


def calculate_damage(attacker, defender, move_name, move_data, effectiveness):
    move = move_data.get(move_name)
    if move is None:
        return None, 1.0, False, "Movimento inválido: " + move_name
    move_pp = attacker.setdefault("move_pp", {})
    current_pp = move_pp.get(move_name, move.get("pp", 0))
    if current_pp <= 0:
        return None, 1.0, False, "Sem PP!"
    move_pp[move_name] = current_pp - 1
    if random.randint(1, 100) > move["accuracy"]:
        return 0, 1.0, False, " Errou o golpe!"

    is_special = move.get("category") == "Especial"
    attack_stat = attacker.get("sp_attack", attacker["attack"]) if is_special else attacker["attack"]
    defense_stat = defender.get("sp_defense", defender["defense"]) if is_special else defender["defense"]
    if not is_special and attacker.get("status") == "Queimado":
        attack_stat *= 0.5
    power = move["power"]
    base = (((2 * attacker["level"] / 5 + 2) * power * attack_stat / max(1, defense_stat)) / 20) + 2
    has_stab = move["type"] in pokemon_types(attacker["type"])
    stab = 2.0 if has_stab and attacker.get("ability") == "Adaptability" else 1.5 if has_stab else 1.0
    multiplier = type_effectiveness(move["type"], defender["type"], effectiveness)
    critical = random.random() < 0.0625
    if critical:
        base *= 1.5
    variance = random.uniform(0.85, 1.0)
    ability_multiplier = 1.0
    ability = attacker.get("ability", "None")
    if ability in {"Blaze", "Overgrow", "Torrent"} and attacker["hp"] * 3 <= attacker["max_hp"]:
        ability_type = {"Blaze": "Fogo", "Overgrow": "Grama", "Torrent": "Água"}[ability]
        if move["type"] == ability_type:
            ability_multiplier = 1.35
    if move.get("category") == "Físico" and defender.get("ability") == "Intimidate":
        ability_multiplier *= 0.9
    damage = 0 if multiplier == 0 else max(1, int(base * stab * multiplier * variance * ability_multiplier))
    if defender.get("ability") == "Sturdy" and defender["hp"] == defender["max_hp"] and damage >= defender["hp"]:
        damage = max(0, defender["hp"] - 1)

    text = ""
    if critical:
        text += " Acerto crítico!"
    if multiplier == 2.0:
        text += " É super efetivo!"
    elif 0 < multiplier < 1.0:
        text += " Não é muito efetivo..."
    elif multiplier == 0:
        text += " Não teve efeito!"
    if multiplier != 0 and move.get("effect") and random.randint(1, 100) <= move.get("chance", 0) and defender["status"] == "Normal":
        defender["status"] = move["effect"]
        if move["effect"] == "Adormecido":
            defender["sleep_turns"] = random.randint(1, 3)
        text += " " + defender["name"] + " ficou " + move["effect"].lower() + "!"
    if move.get("category") == "Físico" and defender.get("ability") == "Static" and defender["status"] == "Normal" and random.randint(1, 100) <= 20:
        defender["status"] = "Paralisado"
        text += " " + defender["name"] + " foi paralisado por Static!"
    return damage, multiplier, critical, text
