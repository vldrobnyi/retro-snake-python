import pygame, sys, random
from pygame.math import Vector2

pygame.init()

TITLE_FONT = pygame.font.Font(None, 60)
SCORE_FONT = pygame.font.Font(None, 40)
GAME_OVER_FONT = pygame.font.Font(None, 80)

GREEN = (173, 204, 96)
DARK_GREEN = (43, 51, 24)

CELL_SIZE = 30
NUMBERS_OF_CELLS = 25

OFFSET = 75

class Food:
    def __init__(self, snake_body):
        self.position = self.generate_random_position(snake_body)

    def draw(self):
        food_rect = pygame.Rect(int(OFFSET + self.position.x * CELL_SIZE), int(OFFSET + self.position.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
        screen.blit(food_surface, food_rect)

    def generate_random_cell(self):
        x = random.randint(0, NUMBERS_OF_CELLS - 1)
        y = random.randint(0, NUMBERS_OF_CELLS - 1)
        return Vector2(x, y)

    def generate_random_position(self, snake_body):        
        position = self.generate_random_cell()
        while position in snake_body:
            position = self.generate_random_cell()

        return position

class Snake:
    def __init__(self):
        self.body = [Vector2(6, 10), Vector2(5, 10), Vector2(4, 10)]
        self.direction = Vector2(1, 0)
        self.add_block = False        
    
    def draw(self):
        for index, block in enumerate(self.body):
            x_pos = int(OFFSET + block.x * CELL_SIZE)
            y_pos = int(OFFSET + block.y * CELL_SIZE)
            block_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)

            if index == 0:
                head_image = pygame.image.load("assets/images/head.png")
                if self.direction == Vector2(1, 0):  
                    head_image = pygame.transform.rotate(head_image, 270)
                elif self.direction == Vector2(-1, 0):  
                    head_image = pygame.transform.rotate(head_image, 90)
                elif self.direction == Vector2(0, -1): 
                    head_image = pygame.transform.rotate(head_image, 0)
                elif self.direction == Vector2(0, 1):  
                    head_image = pygame.transform.rotate(head_image, 180)

                screen.blit(head_image, (x_pos, y_pos))
            elif index == len(self.body) - 1:
                tail_image = pygame.image.load("assets/images/tail.png")
                direction_to_tail = self.body[index - 1] - self.body[index]
                
                if direction_to_tail == Vector2(1, 0):
                    tail_image = pygame.transform.rotate(tail_image, 90)
                elif direction_to_tail == Vector2(-1, 0):
                    tail_image = pygame.transform.rotate(tail_image, 270)
                elif direction_to_tail == Vector2(0, 1):
                    tail_image = pygame.transform.rotate(tail_image, 0)
                elif direction_to_tail == Vector2(0, -1):
                    tail_image = pygame.transform.rotate(tail_image, 180)

                screen.blit(tail_image, (x_pos, y_pos))
            else:
                body_image = pygame.image.load("assets/images/body.png")
                screen.blit(body_image,  (x_pos, y_pos))
    
    def update(self):
        self.body.insert(0, self.body[0] + self.direction)
        if self.add_block:
            self.add_block = False
        else:
            self.body = self.body[:-1]
    
    def reset(self):
        self.body = [Vector2(6, 10), Vector2(5, 10), Vector2(4, 10)]
        self.direction = Vector2(1, 0)
        self.add_block = False

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.state = "start"
        self.score = 0
        self.eat_sound = pygame.mixer.Sound("assets/sounds/eat.mp3")
        self.game_over_sound = pygame.mixer.Sound("assets/sounds/game_over.mp3")

    def draw(self):
        if self.state == "running":
            self.snake.draw()
            self.food.draw()
        elif self.state == "start":
            self.draw_start_screen()
        elif self.state == "paused":
            self.draw_pause_screen()
        elif self.state == "stopped":
            self.draw_game_over()

    def update(self):
        if self.state == "running":
            self.snake.update()
            self.check_collision_with_food()
            self.check_collision_with_walls()
            self.check_collision_with_tail()

    def check_collision_with_food(self):
        if self.food.position == self.snake.body[0]:
            self.food.position = self.food.generate_random_position(self.snake.body)
            self.snake.add_block = True
            self.score += 1
            self.eat_sound.play()
    
    def check_collision_with_walls(self):
        if self.snake.body[0].x == NUMBERS_OF_CELLS or self.snake.body[0].x == -1 or self.snake.body[0].y == NUMBERS_OF_CELLS or self.snake.body[0].y == -1:
            self.game_over()            

    def check_collision_with_tail(self):
        if self.snake.body[0] in self.snake.body[1:]:
            self.game_over()
        
    def game_over(self):
        self.game_over_sound.play()
        self.state = "stopped"

    def draw_start_screen(self):
        instructions = SCORE_FONT.render("Press Enter to Start", True, DARK_GREEN)
        instructions_rect = instructions.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(instructions, instructions_rect)

    def draw_game_over(self):
        game_over_surface = GAME_OVER_FONT.render("Game Over", True, DARK_GREEN)
        retry_surface = SCORE_FONT.render("Press R to Restart", True, DARK_GREEN)
        
        game_over_rect = game_over_surface.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 50))
        retry_rect = retry_surface.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 + 30))
        
        screen.blit(game_over_surface, game_over_rect)
        screen.blit(retry_surface, retry_rect)

    def draw_pause_screen(self):
        pause_surface = GAME_OVER_FONT.render("Paused", True, DARK_GREEN)
        resume_surface = SCORE_FONT.render("Press ESC to Resume", True, DARK_GREEN)
        
        pause_rect = pause_surface.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 50))
        resume_rect = resume_surface.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 + 30))
        
        screen.blit(pause_surface, pause_rect)
        screen.blit(resume_surface, resume_rect)

    def reset(self):
        self.snake.reset()
        self.food.position = self.food.generate_random_position(self.snake.body)
        self.state = "running"
        self.score = 0

    def toggle_pause(self):
        if self.state == "running":
            self.state = "paused"
        elif self.state == "paused":
            self.state = "running"


screen = pygame.display.set_mode((2 * OFFSET + CELL_SIZE * NUMBERS_OF_CELLS, 2 * OFFSET + CELL_SIZE * NUMBERS_OF_CELLS))

pygame.display.set_caption("Retro Snake")

clock = pygame.time.Clock()

game = Game()
food_surface = pygame.image.load("assets/images/food.png")

SNAKE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE, 100)

while True:    
    for event in pygame.event.get():
        if event.type == SNAKE_UPDATE and game.state == "running":
            game.update()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if game.state == "stopped" and event.key == pygame.K_r:
                game.reset()
            elif game.state == "start" and event.key == pygame.K_RETURN:
                game.state = "running"
            elif event.key == pygame.K_ESCAPE:
                game.toggle_pause()
            elif game.state == "running":
                if event.key == pygame.K_UP and game.snake.direction != Vector2(0, 1):
                    game.snake.direction = Vector2(0, -1)
                if event.key == pygame.K_DOWN and game.snake.direction != Vector2(0, -1):
                    game.snake.direction = Vector2(0, 1)
                if event.key == pygame.K_LEFT and game.snake.direction != Vector2(1, 0):
                    game.snake.direction = Vector2(-1, 0)
                if event.key == pygame.K_RIGHT and game.snake.direction != Vector2(-1, 0):
                    game.snake.direction = Vector2(1, 0)

    screen.fill(GREEN)
    pygame.draw.rect(screen, DARK_GREEN, (OFFSET - 5, OFFSET - 5, CELL_SIZE * NUMBERS_OF_CELLS + 10, CELL_SIZE * NUMBERS_OF_CELLS + 10), 5)

    game.draw()
    title_surface = TITLE_FONT.render("Retro Snake", True, DARK_GREEN)
    score_surface = SCORE_FONT.render("Score: " + str(game.score), True, DARK_GREEN)
    screen.blit(title_surface, (OFFSET - 5, 20))
    screen.blit(score_surface, (screen.get_width() - OFFSET - score_surface.get_width(), 20))
    pygame.display.update()

    clock.tick(60)