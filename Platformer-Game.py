import time
import arcade

from player import Player
from ground import Box, Ground
from enemy import Enemy

class Game(arcade.Window):
    def __init__(self):
        self.w = 800
        self.h = 700

        super().__init__(self.w, self.h, 'Platformer')

        self.background_image = arcade.load_texture('background.jpg')
        
        self.gravity = 0.2
        self.start_time = time.time()
        self.end_game = 0

        self.key = arcade.Sprite(':resources:images/items/keyRed.png')
        self.key.center_x = 140
        self.key.center_y = 570
        self.key.width = 50
        self.key.height = 50

        self.lock = arcade.Sprite(':resources:images/tiles/lockYellow.png')
        self.lock.center_x = 750
        self.lock.center_y = 105
        self.lock.width = 60
        self.lock.height = 60


        self.me = Player(self.h)
        self.ground_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        
        for i in range(0, 1000, 120):
            ground = Ground(i, 10)
            self.ground_list.append(ground)

        for i in range(400, 700, 120):
            box = Box(i, 230)
            self.ground_list.append(box)

        for i in range(150, 400, 120):
            box = Box(i, 470)
            self.ground_list.append(box)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.me, self.ground_list, gravity_constant= self.gravity)
        self.enemy_physics_engin = []

    def on_draw(self):
        arcade.start_render()
    
        if self.me.life == 0:
            arcade.draw_text('GAME OVER', 170, self.h//2, arcade.color.YELLOW_ROSE, 60)
        else:
            arcade.draw_lrwh_rectangle_textured(0, 0, self.w, self.h, self.background_image)

            self.me.draw()

            for ground in self.ground_list:
                ground.draw()

            if self.end_game == 1:
                arcade.draw_text('YOU WIN', 200, self.h//2, arcade.color.HOT_PINK, 70)
            else:
                for enemy in self.enemy_list:
                    enemy.draw()

            try:
                self.key.draw()
            except:
                pass

            self.lock.draw()

    def on_update(self, delta_time: float):
        self.end_time = time.time()
        if self.end_time - self.start_time > 3:
            new_enemy = Enemy(self.w, self.h)
            self.enemy_list.append(new_enemy)
            self.enemy_physics_engin.append(arcade.PhysicsEnginePlatformer(new_enemy, self.ground_list, gravity_constant= self.gravity))
            self.start_time = time.time()

        self.physics_engine.update()
        for item in self.enemy_physics_engin:
            item.update()

        self.me.update_animation()

        try:
            if arcade.check_for_collision(self.me, self.key):
                self.me.pocked.append(self.key)
                del self.key
        except:
            pass

        if arcade.check_for_collision(self.me, self.lock) and len(self.me.pocked) == 1:
            self.lock.texture = arcade.load_texture(':resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png')
            self.lock.width = 60
            self.lock.height = 120
            self.lock.center_y = 135
            self.end_game = 1
    
        for enemy in self.enemy_list:
            if arcade.check_for_collision(self.me, enemy) and self.end_game == 0:
                self.me.life = 0

    def on_key_press(self, key, modifiers):
        if key == arcade.key.RIGHT:
            self.me.change_x = 1 * self.me.speed
        elif key == arcade.key.LEFT:
            self.me.change_x = -1 * self.me.speed
        elif key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.me.change_y = 10

    def on_key_release(self, key, modifiers):
        self.me.change_x = 0
    
game = Game()
arcade.run()
