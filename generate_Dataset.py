import random
import arcade
from arcade import check_for_collision
import pandas as pd

class Snake(arcade.Sprite):
    def __init__(self, w, h):
        super().__init__()
        self.color = arcade.color.GREEN
        self.speed = 1
        self.width = 18
        self.height = 18
        self.center_x = w // 2
        self.center_y = h // 2
        self.r = 9
        self.change_x = 0
        self.change_y = 0
        self.score = 0
        self.body = []
        self.body.insert(0, [self.center_x, self.center_y])
        
    def draw(self):
        for body in self.body:
            arcade.draw_circle_filled(body[0], body[1], self.r, self.color)
            
    def move(self, x_apple, y_apple):
        if self.center_x < x_apple:
            self.change_x = 1
        elif self.center_x > x_apple:
            self.change_x = -1
        elif self.center_x == x_apple:
            self.change_x = 0
            
        if self.center_y < y_apple:
            self.change_y = 1
        elif self.center_y > y_apple:
            self.change_y = -1
        elif self.center_y == y_apple:
            self.change_y = 0
        
        self.center_x += self.speed * self.change_x
        self.center_y += self.speed * self.change_y
        self.body.append([self.center_x, self.center_y])
        
        if len(self.body) > 1:
            del self.body[0]
        
    def eat(self, object):
        if object == "apple":
            self.score += 1
        elif object == "pear":
            self.score += 2
        elif object == "bomb":
            self.score -= 1
    
    def create_Body(self):
        self.body.append([self.body[-1][0], self.body[-1][1]])

class Apple(arcade.Sprite):
    def __init__(self, w, h):
        super().__init__("Images/apple.png")
        self.width = 30
        self.height = 30
        self.center_x = random.randint(10, w-10)
        self.center_y = random.randint(10, h-10)

class Pear(arcade.Sprite):
    def __init__(self, w, h):
        super().__init__("Images/pear.png")
        self.width = 30
        self.height = 30
        self.center_x = random.randint(10, w-10)
        self.center_y = random.randint(10, h-10)

class Bomb(arcade.Sprite):
    def __init__(self, w, h):
        super().__init__("Images/bomb.png")
        self.width = 40
        self.height = 40
        self.center_x = random.randint(10, w-10)
        self.center_y = random.randint(10, h-10)
    
class Game(arcade.Window):
    def __init__(self, w=600, h=600, title="Snake Game"):
        self.w = w
        self.h = h
        super().__init__(self.w, self.h, title)
        arcade.set_background_color(arcade.color.SAND)
        self.snake = Snake(self.w, self.h)
        self.apple = Apple(self.w, self.h)
        self.pear = Pear(self.w, self.h)
        self.bomb = Bomb(self.w, self.h)
        self.game_over = GameOver(self.w, self.h)
        self.data = []
        self.flag = 0
    
    def on_draw(self):
        arcade.start_render()
        self.snake.draw()
        self.apple.draw()
        self.pear.draw()
        self.bomb.draw()
        arcade.draw_text(text= f"Score: {self.snake.score}", start_x=0, start_y=self.h - 50, width=self.w, font_size=20, align="center", color=arcade.color.BLACK)
        
        if self.flag == 1:
            self.game_over.on_draw()
    
    def on_update(self, delta_time: float):
        self.snake.move(self.apple.center_x, self.apple.center_y)
        
        data = []
        data.append(self.snake.center_x)
        data.append(self.snake.center_y)
        data.append(self.apple.center_x)
        data.append(self.apple.center_y)
        data.append(self.snake.center_x - self.apple.center_x)
        data.append(self.snake.center_y - self.apple.center_y)
        
                # Directions
                #  7  0  1
                #   \ | /
                #    \|/
                # 6---|---->2
                #    /|\
                #   / | \
                #  5  4  3

        if self.snake.change_x == 0:
            if self.snake.change_y == 1:
                data.append(0)
            elif self.snake.change_y == 0:
                pass
            elif self.snake.change_y == -1:
                data.append(4)
        
        elif self.snake.change_x == 1:
            if self.snake.change_y == 1:
                data.append(1)
            elif self.snake.change_y == 0:
                data.append(2)
            elif self.snake.change_y == -1:
                data.append(3)
        
        elif self.snake.change_x == -1:
            if self.snake.change_y == 1:
                data.append(7)
            elif self.snake.change_y == 0:
                data.append(6)
            elif self.snake.change_y == -1:
                data.append(5)
        
        self.data.append(data)
        
        if self.snake.score >= 50:
            features_data = pd.DataFrame(self.data)
            features_data.columns = ["x_snake", "y_snake", "x_apple", "y_apple", "x_S-A_distance", "y_S-A_distance", "direction"]
            features_data.to_csv("data/features_data.csv", index=False)
            arcade.exit()
            
        if (self.snake.center_x < 0 or self.snake.center_x > self.w) or (self.snake.center_y < 0 or self.snake.center_y > self.h):
            self.flag = 1
        
        if check_for_collision(self.snake, self.apple):
            self.snake.eat("apple")
            self.snake.create_Body()
            self.apple = Apple(self.w, self.h)
            print(self.snake.score)
        
        elif check_for_collision(self.snake, self.pear):
            self.snake.eat("pear")
            self.snake.create_Body()
            self.pear = Pear(self.w, self.h)
            print(self.snake.score)
            self.snake.create_Body()
            self.snake.create_Body()
            
        elif check_for_collision(self.snake, self.bomb):
            self.snake.eat("bomb")
            if self.snake.score <= 0:
                self.flag = 1
            self.bomb = Bomb(self.w, self.h)
            del self.snake.body[-1]
            print(self.snake.score)
            
    def on_key_release(self, key, modifires):
        if key == arcade.key.ESCAPE:
            self.game_over.exit_Game()

class GameOver(arcade.View):
    def __init__(self, w, h):
        super().__init__()
        self.width = w
        self.height = h
        arcade.set_background_color(arcade.color.SAND)
        arcade.set_viewport(0, self.width-1, 0, self.height-1)
        
    def on_draw(self):
        arcade.start_render()
        arcade.draw_text('Game Over', self.width // 2.4, self.height // 2, arcade.color.BLACK, 20, 20)
        arcade.draw_text("Press 'ESC' for exit", self.width // 2.4, self.height // 2.3, arcade.color.BLACK, 12, 12)
    
    def exit_Game(self):
        arcade.start_render()
        arcade.exit()
        
game = Game(800, 600)
arcade.run()