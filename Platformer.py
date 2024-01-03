#TODO:
'''
    add new levels
    add a level select/world select screen
'''

import arcade
import pathlib
import math
import shelve

from Entities.Player import Player
from Entities.Enemies.Wisp import Wisp
from Entities.Coins.GoldCoin import GoldCoin
from Entities.Coins.SilverCoin import SilverCoin
from Entities.Coins.RedCoin import RedCoin
from Entities.Spell import Spell
from Entities.Portal import Portal

from Util.Constants import Constants
from Util.Sounds import Sounds

from Views.MainMenu import MainMenu
from Views.GameOver import GameOverView
from Views.WinScreen import WinScreen
from Views.PauseScreen import PauseScreen

const = Constants()
sounds = Sounds()

#Assets Path
PATH_TO_MAIN_FOLDER = pathlib.Path(__file__).resolve().parent
PATH_TO_ASSETS = pathlib.Path(__file__).resolve().parent / "Assets"

def load_texture_pair(fileName): 
    return [
        arcade.load_texture(fileName),
        arcade.load_texture(fileName, flipped_horizontally = True)
    ]

class PreLevel(arcade.View):
       
    def __init__(self):
        super().__init__()

        save_data = shelve.open('Save_Data/Save_Data')

        self.level = save_data['current_level']
        self.world = save_data['current_world']
        self.background = arcade.load_texture(PATH_TO_ASSETS / "Images" / "PreLevel" / f"Level{self.level}.png")

        save_data.close()

        self.platformer = Platformer(world = self.world, level = self.level)

    def on_show_view(self):
        arcade.play_sound(sounds.LEVEL_START_SOUND)
        arcade.schedule(self.startGame, 1)
        arcade.set_background_color(arcade.color.AERO_BLUE)

    def on_hide_view(self):
        arcade.unschedule(self.startGame)

    def on_draw(self):
        self.clear()

        arcade.draw_lrwh_rectangle_textured(0, 0, self.window.width, self.window.height, self.background, alpha = 150)

        '''arcade.draw_text(
            f"World {self.world} Level {self.level}",
            self.window.width / 2,
            self.window.height / 2,
            arcade.color.BLACK,
            self.window.width / 30,
            font_name = "Kenney Future",
            anchor_x = "center",
            bold = True
        )'''

    def startGame(self, delta_time):
        self.window.show_view(self.platformer)
    
        
class Platformer(arcade.View):
    def __init__(self, world = 1, level = 1):
        # Call the parent class and set up the window
        super().__init__()

        self.save_data = shelve.open('Save_Data/Save_Data')

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.cast_pressed = False
        self.jump_needs_reset = False
        self.restart = False
        self.paused = False

        self.bgm = sounds.GAME_BGM
        self.player = None

        self.image = None
        self.pause_count = 0

        self.health = 0
        self.invincible_timer = 0

        self.can_cast = False
        self.cast_timer = 0

        self.tile_map = None

        self.scene = None
        self.player_sprite = None

        self.physics_engine = None
        self.camera = None

        self.gui_camera = None
        self.score = 0

        self.reset_score = True
        self.end__of_map = 0

        self.can_teleport = True
        self.teleport_timer = 30
        self.teleport_counter = 0

        self.world = world
        self.level = level

    def setup(self):
        self.camera = arcade.Camera(self.window.width, self.window.height)
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)
        self.health = 3

        self.heart = "♥"

        map_path = PATH_TO_MAIN_FOLDER / "Levels" / f"Level{self.level}.tmx"
        layer_options = {
            const.LAYER_NAME_GROUND: {
                "use_spatial_hash": True,
            },
            const.LAYER_NAME_COINS: {
                "use_spatial_hash": True,
            },
            const.LAYER_NAME_GOAL: {
                "use_spatial_hash": True
            }
        }

        self.tile_map = arcade.load_tilemap(map_path, const.TILE_SCALING, layer_options)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        if self.reset_score:
            self.score = 0
        self.reset_score = True

        self.can_cast = True
        self.cast_timer = 0

        self.player_sprite = Player()
        self.player_sprite.center_x = const.PLAYER_START_X
        self.player_sprite.center_y = const.PLAYER_START_Y
        self.scene.add_sprite(const.LAYER_NAME_PLAYER, self.player_sprite)

        self.end_of_map = self.tile_map.width * const.GRID_PIXEL_SIZE

        enemies = self.scene[const.LAYER_NAME_ENEMIES]
        newEnemies = []

        for enemy_object in enemies:
            enemy_type = enemy_object.properties['type']
            if enemy_type == "Wisp":
                enemy = Wisp()
            else:
                raise Exception(f"Unknown enemy type {enemy_type}.")
            
            enemy.center_x = enemy_object.center_x
            enemy.center_y = enemy_object.center_y
    
            if "boundary_left" in enemy_object.properties:
                enemy.boundary_left = enemy_object.properties["boundary_left"]
            if "boundary_right" in enemy_object.properties:
                enemy.boundary_right = enemy_object.properties["boundary_right"]
            if "change_x" in enemy_object.properties:
                enemy.change_x = enemy_object.properties["change_x"]

            newEnemies.append(enemy)
            
        self.scene[const.LAYER_NAME_ENEMIES].clear()

        for sprite in newEnemies:
            self.scene.add_sprite(const.LAYER_NAME_ENEMIES, sprite)

        coins = self.scene[const.LAYER_NAME_COINS]
        newCoins = []

        for coin_object in coins:
            coin_type = coin_object.properties['type']
            if coin_type == "gold":
                coin = GoldCoin()
            elif coin_type == "silver":
                coin = SilverCoin()
            elif coin_type == "red":
                coin = RedCoin()
            else:
                raise Exception(f"Unknown enemy type {coin_type}.")
            
            coin.center_x = coin_object.center_x
            coin.center_y = coin_object.center_y

            newCoins.append(coin)
            
        self.scene[const.LAYER_NAME_COINS].clear()

        for sprite in newCoins:
            self.scene.add_sprite(const.LAYER_NAME_COINS, sprite)

        portals = self.scene[const.LAYER_NAME_GOAL]
        newPortals = []

        for portal_object in portals:
            portal = Portal()
            
            portal.center_x = portal_object.center_x
            portal.center_y = portal_object.center_y

            newPortals.append(portal)
            
        self.scene[const.LAYER_NAME_GOAL].clear()

        for sprite in newPortals:
            self.scene.add_sprite(const.LAYER_NAME_GOAL, sprite)

        if const.LAYER_NAME_PORTALS in self.scene.name_mapping:
            portals = self.scene[const.LAYER_NAME_PORTALS]
            newPortals = []

            for portal_object in portals:
                if portal_object.properties['right_facing']:
                    portal = Portal(portal_type = "Green", direction = const.RIGHT_FACING, id = portal_object.properties['portal_id'], pairedID = portal_object.properties['paired_id'])
                else:
                    portal = Portal(portal_type = "Green", id = portal_object.properties['portal_id'], pairedID = portal_object.properties['paired_id'])
                
                portal.center_x = portal_object.center_x
                portal.center_y = portal_object.center_y

                newPortals.append(portal)
            
            self.scene[const.LAYER_NAME_PORTALS].clear()

            for portal in newPortals:
                for paired_portal in newPortals:
                    if portal.paired_id == paired_portal.id:
                        if paired_portal.direction == const.LEFT_FACING:
                            portal.teleport_x = paired_portal.center_x - 40
                        else:
                            portal.teleport_x = paired_portal.center_x + 40
                        portal.teleport_y = paired_portal.center_y + 50

            for sprite in newPortals:
                self.scene.add_sprite(const.LAYER_NAME_PORTALS, sprite)
            

        self.scene.add_sprite_list(const.LAYER_NAME_SPELLS)

        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        if self.has_platforms():
            self.physics_engine = arcade.PhysicsEnginePlatformer(
                player_sprite = self.player_sprite, 
                walls = self.scene[const.LAYER_NAME_GROUND],
                gravity_constant =  const.GRAVITY,
                platforms = self.scene[const.LAYER_NAME_PLATFORMS],
            )
        else:
            self.physics_engine = arcade.PhysicsEnginePlatformer(
                player_sprite = self.player_sprite, 
                walls = self.scene[const.LAYER_NAME_GROUND],
                gravity_constant =  const.GRAVITY,
            )

        self.player = self.bgm.play(volume = 0.5, loop = True)

        self.physics_engine.enable_multi_jump(2)

        '''self.image = arcade.get_image()
        self.image.save(f"Level{self.level}.png")'''

    def has_platforms(self):
        return const.LAYER_NAME_PLATFORMS in self.scene.name_mapping
    
    def has_portals(self):
        return const.LAYER_NAME_PORTALS in self.scene.name_mapping

    def on_show_view(self):
        if not self.paused:
            self.setup()
        else:
            self.paused = False
            if self.right_pressed:
                self.right_pressed = False
            elif self.left_pressed:
                self.left_pressed = False
            if self.player_sprite.ducking and self.down_pressed:
                self.player_sprite.ducking = False
                self.down_pressed = False
            
            
    def changeFullScreen(self):
        self.window.set_fullscreen(not self.window.fullscreen)
        self.camera.resize(self.window.width, self.window.height)
        self.gui_camera.resize(self.window.width, self.window.height)

    
    def on_draw(self):
        self.clear()

        self.camera.use()
        self.scene.draw()

        self.gui_camera.use()

        hearts = "".join([str(self.heart) + " "] * self.health)
        score_text = f"Score: {self.score} \t Health: "
        arcade.draw_text(score_text, self.window.height * (1/30), self.window.height * (19/20), arcade.color.WHITE, self.window.width / 80 , font_name = "Kenney Blocks")
        arcade.draw_text(f"{hearts}", (self.window.width * (len(score_text) - 2) / 80), self.window.height * (19/20), arcade.color.RED, self.window.width / 70, bold = True, font_name = "Kenney Future")

    def process_keyChange(self):
        if self.restart:
            self.restart = False
            self.bgm.stop(self.player)
            self.setup()
            return

        if self.paused:
            self.pause_count += 1
            self.image = arcade.get_image()
            arcade.play_sound(sounds.PAUSE_SOUND)
            self.window.show_view(PauseScreen(self))

        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.can_jump(y_distance = 10) and not self.jump_needs_reset:
                if self.physics_engine.jumps_since_ground == 0:
                    self.player_sprite.change_y = const.PLAYER_JUMP_SPEED
                    self.physics_engine.increment_jump_counter()
                    self.jump_needs_reset = True
                    arcade.play_sound(sounds.PLAYER_JUMP_SOUND)
                else:
                    self.player_sprite.change_y = const.PLAYER_DOUBLE_JUMP_SPEED
                    self.physics_engine.increment_jump_counter()
                    self.jump_needs_reset = True
                    arcade.play_sound(sounds.PLAYER_JUMP_SOUND)

        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = const.PLAYER_MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -const.PLAYER_MOVEMENT_SPEED
        else:
            self.player_sprite.change_x = 0

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True    
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True

        if key == arcade.key.ESCAPE:
            self.paused = True
        elif key == const.FULL_SCREEN_KEY:
            self.changeFullScreen()
        
        if key == arcade.key.R:
            self.restart = True
        
        if key == arcade.key.Q:
            self.cast_pressed = True

        self.process_keyChange()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
            self.jump_needs_reset = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

        if key == arcade.key.Q:
            self.cast_pressed = False

        self.process_keyChange()

    def center_player_camera(self, speed = 0.25):
        screen_center_x = self.camera.scale * (self.player_sprite.center_x - (self.camera.viewport_width / 2))
        screen_center_y = self.camera.scale * (self.player_sprite.center_y - (self.camera.viewport_height / 2))

        if screen_center_x < 0: screen_center_x = self.tile_map.tile_width * 2
        if screen_center_y < 0: screen_center_y = 0

        if (
            screen_center_x + self.camera.viewport_width 
            > 
            self.tile_map.width * self.tile_map.tile_width
            ): 
            screen_center_x = (self.tile_map.width * self.tile_map.tile_width) - self.camera.viewport_width
        if (
            screen_center_y + self.camera.viewport_height 
            > 
            self.tile_map.height * self.tile_map.tile_height
            ): 
            screen_center_y = (self.tile_map.height * self.tile_map.tile_height) - self.camera.viewport_height

        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered, speed)

    def on_update(self, delta_time):
            # Move the player with the physics engine
            self.physics_engine.update()
            
            if self.physics_engine.can_jump():
                self.player_sprite.jumping = False
            else:
                self.player_sprite.jumping = True

            if self.down_pressed:
                self.player_sprite.ducking = True
            else:
                self.player_sprite.ducking = False

            if self.can_cast:
                if self.cast_pressed:
                    self.player_sprite.attacking = True

                    arcade.play_sound(sounds.SPELL_SOUND)
                    spell = Spell(self.player_sprite.character_direction)

                    if self.player_sprite.character_direction == const.RIGHT_FACING:
                        spell.change_x = const.SPELL_SPEED
                    else:
                        spell.change_x = -const.SPELL_SPEED

                    spell.center_x = self.player_sprite.center_x
                    spell.center_y = self.player_sprite.center_y

                    self.scene.add_sprite(const.LAYER_NAME_SPELLS, spell)
                    self.can_cast = False
            else:
                self.cast_timer += 1
                if self.cast_timer == const.SPELL_CAST_SPEED:
                    self.can_cast = True
                    self.cast_timer = 0

            if self.player_sprite.isInvincible:
                self.invincible_timer += 1
                if self.invincible_timer == const.INVINCIBLE_TIME:
                    self.player_sprite.isInvincible = False
                    self.invincible_timer = 0

            self.scene.update_animation(
                delta_time, [
                    const.LAYER_NAME_BACKGROUND, 
                    const.LAYER_NAME_PLAYER, 
                    const.LAYER_NAME_COINS, 
                    const.LAYER_NAME_ENEMIES,
                    const.LAYER_NAME_SPELLS,
                    const.LAYER_NAME_GOAL,
                ]
            )

            if const.LAYER_NAME_PORTALS in self.scene.name_mapping:
                self.scene.update_animation(
                delta_time, [
                    const.LAYER_NAME_PORTALS, 
                ]
            )

            self.scene.update([
                const.LAYER_NAME_ENEMIES, 
                const.LAYER_NAME_SPELLS, 
                const.LAYER_NAME_COINS
            ])

            for enemy in self.scene[const.LAYER_NAME_ENEMIES]:
                if (
                    enemy.boundary_right
                    and enemy.right > enemy.boundary_right
                    and enemy.change_x > 0
                ):
                    enemy.change_x *= -1
                if (
                    enemy.boundary_left
                    and enemy.left < enemy.boundary_left
                    and enemy.change_x < 0
                ):
                    enemy.change_x *= -1

            if self.has_portals():
                for spell in self.scene[const.LAYER_NAME_SPELLS]:
                    spell_collision_list = arcade.check_for_collision_with_list(spell, self.scene[const.LAYER_NAME_PORTALS])
                    if len(spell_collision_list) > 0:
                        collided_portal = spell_collision_list[0]
                        for portal in self.scene[const.LAYER_NAME_PORTALS]:
                            if portal.id == collided_portal.paired_id:
                                if (
                                    (portal.direction == const.LEFT_FACING and spell.change_x > 0) 
                                    or (portal.direction == const.RIGHT_FACING and spell.change_x < 0)
                                ):
                                    spell.change_x *= -1
                                spell.center_x = collided_portal.teleport_x
                                spell.center_y = portal.center_y
                                break
                
            for spell in self.scene[const.LAYER_NAME_SPELLS]:
                spell_collision_list = arcade.check_for_collision_with_lists(
                    spell,
                    [
                        self.scene[const.LAYER_NAME_ENEMIES],
                        self.scene[const.LAYER_NAME_GROUND]
                    ],
                )

                if spell_collision_list:
                    spell.remove_from_sprite_lists()

                    for collision in spell_collision_list:
                        if self.scene[const.LAYER_NAME_ENEMIES] in collision.sprite_lists:
                            collision.health -= const.SPELL_DAMAGE
                            collision.isHit = True
                            if collision.health <= 0:
                                if collision.type == "Wisp":
                                    arcade.play_sound(sounds.WISP_DEATH_SOUND)
                                    self.score += (collision.max_health * 2)
                                collision.remove_from_sprite_lists()
                            else:
                                arcade.play_sound(sounds.HIT_SOUND)
                    return
                
                if spell.right < 0 or spell.left > ((self.tile_map.width * self.tile_map.tile_width) * const.TILE_SCALING):
                    spell.remove_from_sprite_lists()

            if self.has_portals():
                if not self.can_teleport:
                    self.teleport_counter += 1
                    if self.teleport_counter >= self.teleport_timer:
                        self.teleport_counter = 0
                        self.can_teleport = True
                if self.can_teleport:
                    portal_collision_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene[const.LAYER_NAME_PORTALS])
                    if len(portal_collision_list) > 0:
                        portal_collided = portal_collision_list[0]
                        self.player_sprite.center_x = portal_collided.teleport_x
                        self.player_sprite.center_y = portal_collided.teleport_y
                        arcade.play_sound(sounds.TELEPORT_SOUND)
                        self.can_teleport = False

            player_collision_list = arcade.check_for_collision_with_lists(
                self.player_sprite, 
                [
                    self.scene[const.LAYER_NAME_COINS],
                    self.scene[const.LAYER_NAME_ENEMIES],
                    self.scene[const.LAYER_NAME_GOAL],
                ]
            )

            self.level_ended = False
            for collision in player_collision_list:
                if self.scene[const.LAYER_NAME_GOAL] in collision.sprite_lists:
                    if not self.level_ended:
                        arcade.play_sound(sounds.GOAL_SOUND)
                        self.level_ended = True
                        self.bgm.stop(self.player)
                        if self.level + 1 <= const.MAX_LEVEL:
                            self.reset_score = False
                            self.save_data['current_level'] = self.level + 1
                            self.save_data.close()
                            self.window.show_view(PreLevel())
                        else:
                            if self.world + 1 <= const.MAX_WORLD:
                                self.reset_score = False
                                self.save_data['current_world'] = self.world + 1
                                self.save_data['current_level'] = 1
                                self.save_data.close()
                                self.window.show_view(PreLevel())
                            else: 
                                self.save_data['current_world'] = 1
                                self.save_data['current_level'] = 1
                                self.save_data.close()
                                new_menu = MainMenu(PreLevel())
                                win_screen = WinScreen(new_menu)
                                self.window.show_view(win_screen)
                elif self.scene[const.LAYER_NAME_ENEMIES] in collision.sprite_lists:
                    if not self.player_sprite.isInvincible:
                        if collision.type == "Wisp":
                            collision.HitPlayer = True
                        self.health -= 1
                        if self.health == 0:
                            arcade.play_sound(sounds.GAME_OVER_SOUND)
                            game_over = GameOverView(MainMenu(PreLevel()))
                            self.bgm.stop(self.player)
                            self.window.show_view(game_over)
                        else:
                            self.player_sprite.isInvincible = True
                            arcade.play_sound(sounds.HURT_SOUND)
                            self.player_sprite.change_y = const.PLAYER_JUMP_SPEED
                elif self.scene[const.LAYER_NAME_COINS] in collision.sprite_lists:
                    collision.remove_from_sprite_lists()
                    arcade.play_sound(sounds.COIN_SOUND)
                    self.score += int(collision.point_val)     

            if self.has_platforms():
                onPlat = False
                for platform in self.scene[const.LAYER_NAME_PLATFORMS]:
                    if math.dist((self.player_sprite.center_x, self.player_sprite.center_y), (platform.center_x, platform.center_y)) <= 40:
                        self.player_sprite.onMovingPlatform = True
                        onPlat = True
                if not onPlat:
                    self.player_sprite.onMovingPlatform = False
            

            if self.player_sprite.center_y < -100:
                self.player_sprite.center_x = const.PLAYER_START_X
                self.player_sprite.center_y = const.PLAYER_START_Y

            self.center_player_camera()