"""Inicialização e loop principal do Pokémon Brasar."""

import sys

import pygame

from . import game


def run():
    running = True
    while running:
        game.clock.tick(game.FPS)

        if game.game_mode == "battle" and game.battle_state == "turn":
            if game.battle_turn_delay > 0:
                game.battle_turn_delay -= 1
            else:
                game.run_battle_turn_step()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                key = event.key

                if game.game_mode == "title":
                    game.handle_title_key(key)
                elif game.game_mode == "protagonist_select":
                    game.handle_protagonist_key(key)
                elif game.game_mode == "version_select":
                    game.handle_version_key(key)
                elif game.game_mode == "opening_house":
                    game.handle_opening_house_key(key)
                elif game.game_mode == "starter":
                    if key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                        name = {
                            pygame.K_1: "Macarim",
                            pygame.K_2: "Flaguar",
                            pygame.K_3: "Suriqua",
                        }[key]
                        game.party.append(game.create_pokemon(name, 5))
                        game.pokedex.add(name)
                        game.story_flags["starter_received"] = True
                        game.game_mode = "world"
                        game.show_message("Você escolheu " + name + "!")
                elif game.game_mode == "world":
                    if key == pygame.K_UP:
                        game.move_player(0, -1)
                    elif key == pygame.K_DOWN:
                        game.move_player(0, 1)
                    elif key == pygame.K_LEFT:
                        game.move_player(-1, 0)
                    elif key == pygame.K_RIGHT:
                        game.move_player(1, 0)
                    elif key == game.V7_INTERACT_KEY:
                        game.v7_interact_world()
                    elif key == game.V7_PAUSE_KEY:
                        game.game_mode = "pause"
                        game.pause_cursor = 0
                elif game.game_mode == "pause":
                    game.handle_pause_key(key)
                elif game.game_mode == "save_slots":
                    game.handle_save_slots(key)
                elif game.game_mode == "controls":
                    if key in [pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_e]:
                        game.game_mode = "pause"
                elif game.game_mode == "quit_confirm":
                    if key == pygame.K_RETURN:
                        running = False
                    elif key == pygame.K_ESCAPE:
                        game.game_mode = "pause"
                elif game.game_mode == "menu":
                    game.handle_menu_key(key)
                elif game.game_mode == "party":
                    game.handle_party_key(key)
                elif game.game_mode == "pokedex":
                    if key in [pygame.K_ESCAPE, pygame.K_x]:
                        game.game_mode = "pause"
                elif game.game_mode == "bag":
                    if key == pygame.K_UP:
                        game.menu_cursor = (game.menu_cursor - 1) % 4
                    elif key == pygame.K_DOWN:
                        game.menu_cursor = (game.menu_cursor + 1) % 4
                    elif key in [pygame.K_RETURN, game.V7_INTERACT_KEY]:
                        game.use_item(
                            ["Pokébola", "Poção", "Super Poção", "Antídoto"][
                                game.menu_cursor
                            ]
                        )
                    elif key in [pygame.K_ESCAPE, pygame.K_x]:
                        game.game_mode = "pause"
                elif game.game_mode == "shop":
                    game.handle_shop_key(key)
                elif game.game_mode == "battle":
                    game.handle_battle_key(key)
                elif game.game_mode == "ending":
                    if key in [pygame.K_ESCAPE, pygame.K_RETURN, game.V7_INTERACT_KEY]:
                        game.game_mode = "world"

        if game.game_mode == "title":
            game.draw_title()
        elif game.game_mode == "protagonist_select":
            game.draw_protagonist_select()
        elif game.game_mode == "version_select":
            game.draw_version_select()
        elif game.game_mode == "opening_house":
            game.draw_opening_house()
        elif game.game_mode == "world":
            game.draw_map()
            _draw_message()
        elif game.game_mode == "starter":
            game.draw_starter_screen()
        elif game.game_mode == "battle":
            game.draw_battle()
            _draw_message()
        elif game.game_mode == "pause":
            game.draw_pause()
        elif game.game_mode == "save_slots":
            game.draw_save_slots()
        elif game.game_mode == "controls":
            game.draw_controls()
        elif game.game_mode == "quit_confirm":
            game.draw_quit_confirm()
        elif game.game_mode == "menu":
            game.draw_menu()
        elif game.game_mode == "party":
            game.draw_party_screen()
        elif game.game_mode == "pokedex":
            game.draw_pokedex_screen()
        elif game.game_mode == "bag":
            game.draw_bag_screen()
        elif game.game_mode == "shop":
            game.draw_shop()
        elif game.game_mode == "ending":
            game.draw_ending()

        pygame.display.flip()

    pygame.quit()
    sys.exit()


def _draw_message():
    if game.message_timer <= 0:
        return
    pygame.draw.rect(game.screen, game.WHITE, (35, 480, game.WIDTH - 70, 70))
    pygame.draw.rect(game.screen, game.BLACK, (35, 480, game.WIDTH - 70, 70), 3)
    game.draw_text(game.message, 55, 505)
    game.message_timer -= 1


if __name__ == "__main__":
    run()
