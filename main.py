import pygame
from random import randint


class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 500
        self.screen_height = 500
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.running = True
        self.snake = Snake(self.screen)
        self.fruit_exists = False
        self.fruit = None
        self.score = 0
        self.font = pygame.font.SysFont("Noto Sans", 20, True)
        self.game_end = False
        self.clock = pygame.time.Clock()

    def show_score(self):
        text_surface = self.font.render(f"Score: {self.score}", True, (230, 230, 230))
        self.screen.blit(text_surface, (10, 10))

    def check_game_end(self):
        head = self.snake.blocks[0]
        if head.x > self.screen_width - head.width or head.x <= 0:
            self.game_end = True
        if head.y > self.screen_height - head.height or head.y <= 0:
            self.game_end = True

        for i in range(1, len(self.snake.blocks)):
            cur_block = self.snake.blocks[i]
            if cur_block.x == head.x and cur_block.y == head.y:
                self.game_end = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    if event.key == pygame.K_RIGHT:
                        self.snake.move_right()
                    if event.key == pygame.K_LEFT:
                        self.snake.move_left()
                    if event.key == pygame.K_UP:
                        self.snake.move_up()
                    if event.key == pygame.K_DOWN:
                        self.snake.move_down()

            if not self.fruit_exists:
                self.fruit = Fruit()
                self.fruit_exists = True

            self.screen.fill((0, 0, 0))
            self.fruit.draw(self.screen)
            self.show_score()
            self.check_game_end()
            if self.game_end:
                self.running = False
                self.game_end_screen()
            self.snake.walk()
            self.clock.tick(self.snake.speed)
            self.check_fruit_collison()
            pygame.display.update()

    def check_fruit_collison(self):
        head = self.snake.blocks[0]
        fruit = self.fruit.rect
        if head.colliderect(fruit):
            self.fruit = None
            self.fruit_exists = False
            self.snake.append_block()
            self.score += 10

    def game_end_screen(self):
        running = True
        font = pygame.font.SysFont("Noto Sans", 30, True)
        game_over_text = font.render("GAMEOVER", True, (0, 255, 0))
        score_text = font.render(f"Score: {self.score}", True, (0, 255, 0))

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            self.screen.blit(game_over_text, (150, 150))
            self.screen.blit(score_text, (150, 180))
            pygame.display.update()


class Snake:
    def __init__(self, screen):
        self.game_screen = screen
        self.direction = "right"
        self.speed = 10
        self.blocks = [
            pygame.Rect(40, 40, 10, 10),
            pygame.Rect(30, 40, 10, 10),
            pygame.Rect(20, 40, 10, 10),
            pygame.Rect(10, 40, 10, 10),
        ]

    def draw(self):
        for block in self.blocks:
            pygame.draw.rect(self.game_screen, (74, 219, 39), block)

    def move_right(self):
        if self.direction != "left":
            self.direction = "right"

    def move_left(self):
        if self.direction != "right":
            self.direction = "left"

    def move_up(self):
        if self.direction != "down":
            self.direction = "up"

    def move_down(self):
        if self.direction != "up":
            self.direction = "down"

    def walk(self):
        new_block = None
        if self.direction == "right":
            new_block = self.blocks[0].move(self.speed, 0)
        if self.direction == "left":
            new_block = self.blocks[0].move(-self.speed, 0)
        if self.direction == "up":
            new_block = self.blocks[0].move(0, -self.speed)
        if self.direction == "down":
            new_block = self.blocks[0].move(0, self.speed)

        self.blocks.insert(0, new_block)
        self.blocks.pop()
        self.draw()

    def append_block(self):
        new_block = None
        last_block = self.blocks[-1]
        if self.direction == "right":
            new_block = last_block.move(-self.speed, 0)
        if self.direction == "left":
            new_block = last_block.move(self.speed, 0)
        if self.direction == "up":
            new_block = last_block.move(0, self.speed)
        if self.direction == "down":
            new_block = last_block.move(0, -self.speed)
        self.blocks.append(new_block)


class Fruit:
    def __init__(self):
        self.x = randint(10, 490)
        self.y = randint(10, 490)
        self.rect = None

    def draw(self, game_screen):
        self.rect = pygame.draw.circle(game_screen, (255, 0, 0), (self.x, self.y), 4)


if __name__ == "__main__":
    game = Game()
    game.run()
