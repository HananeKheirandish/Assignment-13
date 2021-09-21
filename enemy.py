import random
import arcade

class Enemy(arcade.Sprite):
    def __init__(self, w, h):
        super().__init__()

        self.texture = arcade.load_texture(':resources:images/animated_characters/zombie/zombie_idle.png')
        
        self.width = 70
        self.height = 125
        self.speed = 2
        self.center_x = random.randint(0, w)
        self.center_y = h 
        self.change_x = random.choice([-1, 1]) * self.speed