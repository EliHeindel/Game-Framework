import arcade
import json

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 5
ENEMY_SPEED = 2
BULLET_SPEED = 10
PLAYER_SIZE = 50
ENEMY_SIZE = 30
BULLET_SIZE = 5

# Colors
WHITE = arcade.color.WHITE
BLACK = arcade.color.BLACK
RED = arcade.color.RED

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        arcade.draw_rectangle_filled(self.x, self.y, PLAYER_SIZE, PLAYER_SIZE, WHITE)

    def move_left(self):
        if self.x > 0:
            self.x -= PLAYER_SPEED

    def move_right(self):
        if self.x < SCREEN_WIDTH:
            self.x += PLAYER_SPEED

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        arcade.draw_rectangle_filled(self.x, self.y, ENEMY_SIZE, ENEMY_SIZE, RED)

    def move_down(self):
        self.y -= ENEMY_SPEED

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, BULLET_SIZE, WHITE)

    def move_up(self):
        self.y += BULLET_SPEED

class SpaceInvadersGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Space Invaders")
        arcade.set_background_color(BLACK)

        self.player = Player(SCREEN_WIDTH // 2, 50)
        self.enemies = []
        for i in range(5):
            self.enemies.append(Enemy(100 * i + 50, SCREEN_HEIGHT - 100))
        self.bullets = []

    def on_draw(self):
        arcade.start_render()
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        for bullet in self.bullets:
            bullet.draw()

    def update(self, delta_time):
        for bullet in self.bullets:
            bullet.move_up()

        for enemy in self.enemies:
            if enemy.y < 0:
                self.enemies.remove(enemy)

        for bullet in self.bullets:
            for enemy in self.enemies:
                if (bullet.x - enemy.x) ** 2 + (bullet.y - enemy.y) ** 2 < (ENEMY_SIZE / 2) ** 2:
                    self.enemies.remove(enemy)
                    self.bullets.remove(bullet)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player.move_left()
        elif key == arcade.key.RIGHT:
            self.player.move_right()
        elif key == arcade.key.SPACE:
            self.bullets.append(Bullet(self.player.x, self.player.y + PLAYER_SIZE // 2))

    def save_game_state(self, filename):
        game_state = {
            'player': {'x': self.player.x, 'y': self.player.y},
            'enemies': [{'x': enemy.x, 'y': enemy.y} for enemy in self.enemies],
            'bullets': [{'x': bullet.x, 'y': bullet.y} for bullet in self.bullets]
        }
        with open(filename, 'w') as f:
            json.dump(game_state, f)

    def load_game_state(self, filename):
        with open(filename, 'r') as f:
            game_state = json.load(f)
            self.player.x = game_state['player']['x']
            self.player.y = game_state['player']['y']
            self.enemies = [Enemy(enemy['x'], enemy['y']) for enemy in game_state['enemies']]
            self.bullets = [Bullet(bullet['x'], bullet['y']) for bullet in game_state['bullets']]

def main():
    game = SpaceInvadersGame()
    arcade.run()

if __name__ == "__main__":
    main()
