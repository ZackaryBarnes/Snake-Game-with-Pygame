import pygame
import sys
import random

#class for snake
class Snake(object):
    def __init__(self):
        self.length = 1
        self.positions = [((game_area_width / 2), (game_area_height / 2))]
        self.direction = neutral
        self.color = (255, 255, 255)
        self.score = 10

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        headX, headY = self.positions[0]
        x, y = self.direction
        new = (((headX + (x*gridsize)) % game_area_width), (headY + (y*gridsize)) % game_area_height)
        if headX == (game_area_width - gridsize) and self.direction == (right):
            self.reset()
        elif headX == (0) and self.direction == (left):
            self.reset()
        elif headY == (game_area_height - gridsize) and self.direction == (down):
            self.reset()
        elif headY == (0) and self.direction == (up):
            self.reset()
        elif new in self.positions:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()       
                updateScore(1, False)     
            
    def reset(self):
        self.length = 1
        self.positions = [((game_area_width / 2), (game_area_height / 2))]
        self.direction = neutral
        updateScore(0, True)
        
         
    def draw(self, game_surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (gridsize -1, gridsize -1))
            pygame.draw.rect(game_surface, self.color, r)
            
    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(up)
                elif event.key == pygame.K_DOWN:
                    self.turn(down)
                elif event.key == pygame.K_LEFT:
                    self.turn(left)
                elif event.key == pygame.K_RIGHT:
                    self.turn(right)

#class for food
class Food(object):
    def __init__(self):
        self.position = (0, 0)
        self.color = (255, 0, 0)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, grid_width-1) * gridsize, random.randint(0, grid_height-1) * gridsize)

    def draw(self, game_surface):
        r = pygame.Rect((self.position[0], self.position[1]), (gridsize-1, gridsize-1))
        pygame.draw.rect(game_surface, self.color, r)

#global functions
def redrawWindow(game_surface, menu_surface):
    game_surface.fill((0,0,0))
    pygame.draw.rect(game_surface, (96,96,96), menu_surface)
    pygame.display.update()

def updateScore(newScore, reset):
    global score
    score += newScore
    if reset:
        score = 0

#global variables
score = 10

screen_width = 650
screen_height = 650

game_area_width = 480
game_area_height = 480

menu_area_width = 170
menu_area_height = 480

gridsize = 20
grid_width = game_area_width / gridsize
grid_height = game_area_height / gridsize

up    = (0, -1)
down  = (0, 1)
left  = (-1, 0)
right = (1, 0)
neutral = (0, 0)
screen_region = (0,0,300,300)

#main game function
def main():
    pygame.init()
    
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((650, 480), 0, 32)
    
    game_surface = pygame.Surface(screen.get_size())
    game_surface = game_surface.convert()

    menu_surface = pygame.Rect(game_area_width, 0, menu_area_width, menu_area_height)

    redrawWindow(game_surface, menu_surface)

    snake = Snake()
    food = Food()

#main game loop
    while True:
        clock.tick(10)
        snake.handle_keys()
        redrawWindow(game_surface, menu_surface)
        snake.move()
        if snake.get_head_position() == food.position:
            snake.length += 1
            food.randomize_position()
            updateScore(100, False)
        snake.draw(game_surface)
        food.draw(game_surface) 
        screen.blit(game_surface, (0,0)) 

        myfont = pygame.font.SysFont("monospace", 20)
        text = myfont.render("Score: {0}".format(score), True, (255,255,255))
        screen.blit(text, (490, 10))

        pygame.display.update()

#calling the main game loop
main()