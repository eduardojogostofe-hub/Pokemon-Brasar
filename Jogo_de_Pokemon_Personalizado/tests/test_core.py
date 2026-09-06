import os
import pathlib
import tempfile
import unittest
from copy import deepcopy
from unittest.mock import patch

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

from pokemon_brasar import game


class CoreGameTests(unittest.TestCase):
    def setUp(self):
        self.original_slots = game.SAVE_SLOTS
        self.original_defeated = set(game.trainer_defeated)
        self.original_trainers = deepcopy(game.TRAINERS)
        self.original_state = {
            name: deepcopy(getattr(game, name))
            for name in (
                "party", "items", "story_flags", "pokedex", "current_map",
                "player_x", "player_y", "pokeballs", "money", "badges",
                "active_index", "game_mode", "trainer_battle", "trainer_name",
                "trainer_team", "trainer_index", "trainer_enemy_hp",
                "trainer_enemy_max_hp", "battle_enemy_obj", "battle_enemy",
                "battle_enemy_level", "battle_enemy_hp", "battle_enemy_max_hp",
                "battle_state", "battle_turn_queue", "battle_turn_index", "battle_turn_delay",
                "forced_switch",
                "interior_return_map", "interior_return_pos",
                "interior_kind",
            )
        }
        game.SAVE_SLOTS = []
        game.trainer_defeated.clear()
        game.party.clear()
        game.pokedex.clear()
        game.items.clear()
        game.items.update({"Poção": 2, "Antídoto": 1, "Super Poção": 0})

    def tearDown(self):
        game.SAVE_SLOTS = self.original_slots
        game.TRAINERS.clear()
        game.TRAINERS.update(self.original_trainers)
        game.trainer_defeated.clear()
        game.trainer_defeated.update(self.original_defeated)
        for name, value in self.original_state.items():
            setattr(game, name, value)

    def test_type_immunities(self):
        self.assertEqual(game.type_effectiveness("Normal", "Fantasma"), 0.0)
        self.assertEqual(game.type_effectiveness("Fantasma", "Normal"), 0.0)
        self.assertEqual(game.type_effectiveness("Elétrico", "Terra"), 0.0)

    def test_regional_gate(self):
        self.assertFalse(game.can_leave_city("amazon", "route2v6"))
        game.trainer_defeated.add("Victorya da Matta")
        self.assertTrue(game.can_leave_city("amazon", "route2v6"))
        self.assertTrue(game.can_leave_city("amazon", "route1v6"))

    def test_active_collision_blocks_water_walls_and_buildings(self):
        self.assertFalse(game.can_walk(7, 5))
        self.assertFalse(game.can_walk(0, 0))
        self.assertFalse(game.can_walk(3, 2))
        game.current_map = "league"
        self.assertTrue(game.can_walk(3, 2))

        game.current_map = "guarany"
        game.player_x, game.player_y = 3, 4
        game.v7_interact_world()
        self.assertEqual(game.current_map, "__interior_house")
        game.v7_interact_world()
        self.assertEqual(game.current_map, "guarany")

    def test_active_progression_and_return_transition(self):
        game.current_map = "amazon"
        game.player_x, game.player_y = 14, 6
        game.move_player(1, 0)
        self.assertEqual(game.current_map, "amazon")

        game.trainer_defeated.add("Victorya da Matta")
        game.current_map = "amazon"
        game.player_x, game.player_y = 14, 6
        game.move_player(1, 0)
        self.assertEqual((game.current_map, game.player_x, game.player_y), ("route2v6", 1, 6))

        game.current_map = "route2v6"
        game.player_x, game.player_y = 1, 6
        game.move_player(-1, 0)
        self.assertEqual((game.current_map, game.player_x, game.player_y), ("amazon", 14, 6))

    def test_every_leader_route_gate(self):
        leaders = [leader for _, leader, _ in game.BRASAR_PROGRESS_SEQUENCE]
        for city, (target, leader) in game.BRASAR_CITY_ROUTE_GATES.items():
            game.trainer_defeated.clear()
            game.current_map = city
            game.player_x, game.player_y = 14, 6
            game.move_player(1, 0)
            self.assertEqual(game.current_map, city, city)

            if target == "area_zero":
                game.trainer_defeated.update(leaders)
            else:
                game.trainer_defeated.add(leader)
            game.current_map = city
            game.player_x, game.player_y = 14, 6
            game.move_player(1, 0)
            self.assertEqual(game.current_map, target, city)

    def test_transition_happens_once_per_move(self):
        game.current_map = "route1v6"
        game.player_x, game.player_y = 14, 6
        game.move_player(1, 0)
        self.assertEqual((game.current_map, game.player_x, game.player_y), ("amazon", 1, 6))

    def test_all_referenced_moves_exist(self):
        referenced = {
            move
            for species in game.POKEMON.values()
            for move in species.get("moves", [])
        }
        for trainer in game.TRAINERS.values():
            for species_name in trainer.get("team", []):
                referenced.update(game.POKEMON[species_name].get("moves", []))
        self.assertEqual(referenced - set(game.MOVE_DATA), set())

    def test_wild_battle_starts_with_real_enemy(self):
        game.party.append(game.create_pokemon("Macarim", 5))
        game.current_map = "route1v6"
        game.start_battle()
        self.assertEqual(game.game_mode, "battle")
        self.assertIsNotNone(game.battle_enemy_obj)
        self.assertGreater(game.battle_enemy_obj["hp"], 0)

    def test_route_one_pikachu_is_balanced(self):
        game.party.append(game.create_pokemon("Flaguar", 5))
        game.current_map = "route1v6"
        game.v6_route_wild = lambda: ("Pikachu", 5)
        game.start_battle()
        self.assertEqual(game.battle_enemy_level, 5)
        target = game.party[0]
        with patch.object(game.random, "randint", return_value=1), patch.object(game.random, "random", return_value=1.0), patch.object(game.random, "uniform", return_value=1.0):
            damage = game.calculate_damage(game.battle_enemy_obj, target, "Choque")[0]
        self.assertLess(damage, target["max_hp"])
        self.assertGreater(target["max_hp"] - damage, 0)

    def test_forced_switch_requires_player_choice(self):
        game.party.extend([game.create_pokemon("Flaguar", 5), game.create_pokemon("Macarim", 4)])
        game.start_battle()
        game.active_index = 0
        game.party[0]["hp"] = 0
        game.battle_state = "turn"
        game.battle_turn_queue = [{"source": "enemy", "move_name": "Choque"}]
        game.battle_turn_index = 0
        game.run_battle_turn_step()
        self.assertEqual(game.battle_state, "switch")
        self.assertTrue(game.forced_switch)
        self.assertEqual(game.active_index, -1)
        game.perform_switch(1)
        self.assertEqual(game.active_index, 1)
        self.assertEqual(game.battle_state, "menu")
        self.assertFalse(game.forced_switch)

    def test_active_battle_turn_queue(self):
        game.party.append(game.create_pokemon("Macarim", 5))
        game.current_map = "route1v6"
        game.start_battle()
        game.battle_enemy_obj = game.create_pokemon("Grubey", 3)
        game.battle_enemy_obj["hp"] = 999
        game.battle_enemy_obj["max_hp"] = 999
        game.battle_state = "fight"
        game.battle_cursor = 0
        with patch.object(game.random, "randint", return_value=1), patch.object(game.random, "random", return_value=1.0), patch.object(game.random, "uniform", return_value=1.0):
            game.handle_battle_key(game.pygame.K_RETURN)
            self.assertEqual(game.battle_state, "turn")
            self.assertEqual(
                {action["source"] for action in game.battle_turn_queue},
                {"player", "enemy"},
            )
            game.run_battle_turn_step()
            self.assertEqual(game.battle_turn_index, 1)
            game.run_battle_turn_step()
            self.assertEqual(game.battle_state, "menu")

        game.start_battle_turn(99)
        self.assertEqual(game.battle_state, "menu")

    def test_move_priority_can_beat_speed(self):
        player = game.create_pokemon("Pikachu", 5)
        player["moves"].append("Ataque Rápido")
        player["move_pp"]["Ataque Rápido"] = game.MOVE_DATA["Ataque Rápido"]["pp"]
        player["speed"] = 1
        enemy = game.create_pokemon("Macarim", 5)
        enemy["speed"] = 100
        game.party.append(player)
        game.battle_enemy_obj = enemy
        game.battle_enemy = enemy["name"]
        game.battle_enemy_level = enemy["level"]
        game.trainer_battle = False
        game.game_mode = "battle"
        game.start_battle_turn(2)
        self.assertEqual(game.battle_turn_queue[0]["source"], "player")

    def test_status_turn_rules(self):
        pokemon = game.create_pokemon("Macarim", 5)
        pokemon["status"] = "Congelado"
        with patch.object(game.random, "random", return_value=0.99):
            self.assertFalse(game.status_can_act(pokemon))
        with patch.object(game.random, "random", return_value=0.0):
            self.assertTrue(game.status_can_act(pokemon))
        pokemon["status"] = "Envenenado"
        hp_before = pokemon["hp"]
        game.apply_end_turn_status(pokemon)
        self.assertLess(pokemon["hp"], hp_before)
        pokemon["status"] = "Paralisado"
        self.assertEqual(game.battle_speed(pokemon), pokemon["speed"] // 2)

    def test_damage_physical_special_immunity_and_pp(self):
        attacker = game.create_pokemon("Flaguar", 10)
        defender = game.create_pokemon("Macarim", 10)
        with patch.object(game.random, "randint", return_value=1), patch.object(game.random, "random", return_value=1.0), patch.object(game.random, "uniform", return_value=1.0):
            physical = game.calculate_damage(attacker, defender, "Investida")
            special = game.calculate_damage(attacker, defender, "Brasa")
        self.assertGreater(physical[0], 0)
        self.assertGreater(special[0], 0)

        defender["type"] = "Fantasma"
        attacker["move_pp"]["Investida"] = 1
        with patch.object(game.random, "randint", return_value=1), patch.object(game.random, "random", return_value=1.0), patch.object(game.random, "uniform", return_value=1.0):
            immune = game.calculate_damage(attacker, defender, "Investida")
        self.assertEqual(immune[0], 0)
        self.assertEqual(attacker["move_pp"]["Investida"], 0)
        self.assertIsNone(game.calculate_damage(attacker, defender, "Investida")[0])

        invalid = game.calculate_damage(attacker, defender, "Movimento inválido")
        self.assertIsNone(invalid[0])
        self.assertIn("Movimento inválido", invalid[3])

    def test_active_abilities_and_evolution_keep_ability(self):
        pikachu = game.create_pokemon("Pikachu", 5)
        self.assertEqual(pikachu["ability"], "Static")

        attacker = game.create_pokemon("Charmander", 5)
        defender = game.create_pokemon("Macarim", 5)
        attacker["hp"] = attacker["max_hp"] // 3
        with patch.object(game.random, "randint", return_value=1), patch.object(game.random, "random", return_value=1.0), patch.object(game.random, "uniform", return_value=1.0):
            boosted = game.calculate_damage(attacker, defender, "Brasa")
        attacker["ability"] = "None"
        attacker["move_pp"]["Brasa"] = game.MOVE_DATA["Brasa"]["pp"]
        defender["hp"] = defender["max_hp"]
        with patch.object(game.random, "randint", return_value=1), patch.object(game.random, "random", return_value=1.0), patch.object(game.random, "uniform", return_value=1.0):
            normal = game.calculate_damage(attacker, defender, "Brasa")
        self.assertGreater(boosted[0], normal[0])

        for species, move, ability_type in (("Bulbasaur", "Folhagem", "Grama"), ("Squirtle", "Jato d'Água", "Água")):
            powered = game.create_pokemon(species, 5)
            powered["hp"] = powered["max_hp"] // 3
            powered_target = game.create_pokemon("Macarim", 5)
            with patch.object(game.random, "randint", return_value=1), patch.object(game.random, "random", return_value=1.0), patch.object(game.random, "uniform", return_value=1.0):
                powered_damage = game.calculate_damage(powered, powered_target, move)[0]
            powered["ability"] = "None"
            powered["move_pp"][move] = game.MOVE_DATA[move]["pp"]
            powered_target["hp"] = powered_target["max_hp"]
            with patch.object(game.random, "randint", return_value=1), patch.object(game.random, "random", return_value=1.0), patch.object(game.random, "uniform", return_value=1.0):
                regular_damage = game.calculate_damage(powered, powered_target, move)[0]
            self.assertGreater(powered_damage, regular_damage, ability_type)

        sturdy = game.create_pokemon("Aron", 5)
        sturdy["ability"] = "Sturdy"
        sturdy["hp"] = sturdy["max_hp"]
        strong = game.create_pokemon("Flaguar", 50)
        with patch.object(game.random, "randint", return_value=1), patch.object(game.random, "random", return_value=1.0), patch.object(game.random, "uniform", return_value=1.0):
            damage = game.calculate_damage(strong, sturdy, "Brasa")[0]
        self.assertLess(damage, sturdy["hp"])

        static = game.create_pokemon("Pikachu", 5)
        static["status"] = "Normal"
        with patch.object(game.random, "randint", return_value=1), patch.object(game.random, "random", return_value=1.0), patch.object(game.random, "uniform", return_value=1.0):
            game.calculate_damage(strong, static, "Investida")
        self.assertEqual(static["status"], "Paralisado")

        intimidate = game.create_pokemon("Shinx", 5)
        normal_defender = game.create_pokemon("Macarim", 5)
        with patch.object(game.random, "randint", return_value=1), patch.object(game.random, "random", return_value=1.0), patch.object(game.random, "uniform", return_value=1.0):
            reduced = game.calculate_damage(strong, intimidate, "Investida")[0]
            regular = game.calculate_damage(strong, normal_defender, "Investida")[0]
        self.assertLess(reduced, regular)

        adaptability = game.create_pokemon("Eevee", 5)
        base_attacker = game.create_pokemon("Macarim", 5)
        with patch.object(game.random, "randint", return_value=1), patch.object(game.random, "random", return_value=1.0), patch.object(game.random, "uniform", return_value=1.0):
            adapted = game.calculate_damage(adaptability, normal_defender, "Investida")[0]
            base = game.calculate_damage(base_attacker, normal_defender, "Investida")[0]
        self.assertGreater(adapted, base)

        burned = game.create_pokemon("Flaguar", 5)
        burned["status"] = "Queimado"
        burned["move_pp"]["Investida"] = game.MOVE_DATA["Investida"]["pp"]
        normal = game.create_pokemon("Flaguar", 5)
        with patch.object(game.random, "randint", return_value=1), patch.object(game.random, "random", return_value=1.0), patch.object(game.random, "uniform", return_value=1.0):
            burned_damage = game.calculate_damage(burned, normal_defender, "Investida")[0]
            normal_damage = game.calculate_damage(normal, normal_defender, "Investida")[0]
        self.assertLess(burned_damage, normal_damage)

        evolving = game.create_pokemon("Pikachu", 20)
        evolving["level"] = 20
        game.try_evolution(evolving)
        self.assertEqual(evolving["name"], "Raichu")
        self.assertEqual(evolving["ability"], "Static")

        with tempfile.TemporaryDirectory() as temporary_dir:
            game.SAVE_SLOTS = [pathlib.Path(temporary_dir) / "evolution.json"]
            game.current_map = "guarany"
            game.party[:] = [evolving]
            self.assertTrue(game._write_slot(0))
            game.party.clear()
            self.assertTrue(game._load_slot(0))
            self.assertEqual(game.party[0]["name"], "Raichu")
            self.assertEqual(game.party[0]["ability"], "Static")

    def test_trainer_victory_and_defeat_reset(self):
        game.TRAINERS["Teste P0"] = {
            "map": "route1v6", "x": 4, "y": 4,
            "team": ["Grubey"], "level": 5, "reward": 50,
        }
        game.party.append(game.create_pokemon("Flaguar", 10))
        game.start_trainer_battle("Teste P0")
        game.trainer_current()["hp"] = 1
        game.trainer_enemy_hp = 1
        game.player_attack(0)
        self.assertIn("Teste P0", game.trainer_defeated)
        self.assertFalse(game.trainer_battle)

        game.party[0]["hp"] = 0
        game.current_map = "route1v6"
        self.assertTrue(game.defeat_player())
        self.assertEqual(game.current_map, "guarany")
        self.assertEqual(game.party[0]["hp"], game.party[0]["max_hp"])

    def test_trainer_sends_next_pokemon_on_next_turn(self):
        game.TRAINERS["Teste Duplo"] = {
            "map": "route1v6", "x": 4, "y": 4,
            "team": ["Grubey", "Canarin"], "level": 5, "reward": 50,
        }
        game.party.append(game.create_pokemon("Flaguar", 10))
        game.start_trainer_battle("Teste Duplo")
        game.trainer_current()["hp"] = 1
        game.trainer_enemy_hp = 1
        game.battle_state = "fight"
        game.battle_cursor = 0
        game.handle_battle_key(game.pygame.K_RETURN)
        game.run_battle_turn_step()
        self.assertEqual(game.trainer_index, 1)
        self.assertEqual(game.battle_state, "menu")
        self.assertEqual(game.battle_turn_queue, [])

    def test_switch_capture_and_experience(self):
        game.party.extend([game.create_pokemon("Macarim", 5), game.create_pokemon("Flaguar", 5)])
        game.start_battle()
        game.battle_switch()
        game.perform_switch(1)
        self.assertEqual(game.active_index, 1)

        game.game_mode = "battle"
        game.trainer_battle = False
        game.pokeballs = 1
        game.battle_enemy_obj = game.create_pokemon("Grubey", 3)
        game.battle_enemy_obj["hp"] = 1
        with patch.object(game.random, "random", return_value=0.0):
            game.try_capture()
        self.assertEqual(game.game_mode, "world")
        self.assertTrue(any(p["name"] == "Grubey" for p in game.party))

        target = game.create_pokemon("Macarim", 5)
        old_level = target["level"]
        game.gain_xp(target, target["xp_to_next"])
        self.assertGreater(target["level"], old_level)

    def test_battle_item_consumes_player_turn(self):
        game.party.append(game.create_pokemon("Macarim", 5))
        game.start_battle()
        game.party[0]["hp"] -= 10
        game.items["Poção"] = 1
        game.v6_battle_bag = True
        game.v6_bag_cursor = 1
        game.v6_bag_use()
        self.assertEqual(game.battle_state, "turn")
        self.assertEqual(game.battle_turn_queue, [{"source": "enemy"}])
        game.run_battle_turn_step()
        self.assertEqual(game.battle_state, "menu")

    def test_atomic_save_round_trip(self):
        with tempfile.TemporaryDirectory() as temporary_dir:
            game.SAVE_SLOTS = [pathlib.Path(temporary_dir) / "slot.json"]
            game._new_game()
            self.assertTrue(game._write_slot(0))
            self.assertTrue(game._load_slot(0))
            game.SAVE_SLOTS[0].write_text("{broken", encoding="utf-8")
            self.assertFalse(game._load_slot(0))
            self.assertFalse(game._load_slot(1))

    def test_real_save_state_round_trip(self):
        with tempfile.TemporaryDirectory() as temporary_dir:
            game.SAVE_SLOTS = [pathlib.Path(temporary_dir) / "slot.json"]
            game._new_game()
            game.party.append(game.create_pokemon("Flaguar", 7))
            game.pokeballs = 9
            game.money = 1250
            game.items["Poção"] = 4
            game.badges = 2
            game.trainer_defeated.add("Victorya da Matta")
            game.current_map = "route2v6"
            game.player_x, game.player_y = 4, 4
            expected = (game.current_map, game.player_x, game.player_y, game.money, game.pokeballs, game.badges)
            self.assertTrue(game._write_slot(0))

            game.current_map = "guarany"
            game.party.clear()
            game.money = 0
            self.assertTrue(game._load_slot(0))
            actual = (game.current_map, game.player_x, game.player_y, game.money, game.pokeballs, game.badges)
            self.assertEqual(actual, expected)
            self.assertEqual(game.party[0]["name"], "Flaguar")
            self.assertEqual(game.items["Poção"], 4)


if __name__ == "__main__":
    unittest.main()
