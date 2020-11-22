
#flappy duck

import pygame
import time
import random
pygame.init()
clock = pygame.time.Clock()

FPS = 60
WIDTH = 550
HEIGHT = 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy Duck')

FALL_IMAGE = pygame.image.load('SPRITE_0.png')
FALL_IMAGE = pygame.transform.scale(FALL_IMAGE, (50, 50))
JUMP_IMAGE = pygame.image.load('SPRITE_1.png')
JUMP_IMAGE = pygame.transform.scale(JUMP_IMAGE, (50, 50))
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


class Bird:
    def __init__(self, x, y):

        self.img = FALL_IMAGE
        self.jump = False
        self.jump_count = 0
        self.jump_speed = 20 * -1
        self.fall_speed = 3
        self.speed = self.fall_speed
        self.x = x
        self.y = y
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.score = 0

    def draw(self):
        WIN.blit(self.img, (self.x, self.y))

    def update(self):
        if self.speed >= 0 :
            self.img = FALL_IMAGE
        elif self.speed < 0:
            self.img = JUMP_IMAGE
        if self.jump and self.jump_count > FPS/10:
            self.jump_count = 0
            self.jump = False
            self.speed = self.jump_speed
        self.jump_count += 1
        if self.speed < self.fall_speed:
            self.speed += self.fall_speed
        if (self.y + self.speed + self.height < HEIGHT and self.y + self.speed > 0)\
            or self.jump:
            self.y += self.speed


class Wall:
    HOLE_HEIGHT = 150
    MIN_WALL_HEIGHT = 60
    SPEED = 1
    SPACING = 200
    width = 80
    def __init__(self):

        self.color = BLUE
        self.height_up = random.randrange(self.MIN_WALL_HEIGHT, HEIGHT - self.HOLE_HEIGHT, self.MIN_WALL_HEIGHT)

        self.image_up = pygame.Surface([self.width, self.height_up])
        self.image_up.fill(self.color)
        self.rect_up = self.image_up.get_rect()

        self.image_down = pygame.Surface([self.width, HEIGHT - (self.height_up + self.HOLE_HEIGHT)])
        self.image_down.fill(self.color)

        self.image_up_x = WIDTH
        self.image_down_x = WIDTH

        self.hit = False

    def draw(self):
        WIN.blit(self.image_up, (self.image_up_x , 0))
        WIN.blit(self.image_down, (self.image_down_x , self.height_up + self.HOLE_HEIGHT))

    def update(self):
        self.image_up_x -= self.SPEED
        self.image_down_x -= self.SPEED


def draw_message(text, x, y, color, font_size = 40):
    font_style = pygame.font.SysFont('FUTURAM.ttf', font_size)
    b = font_style.render(text, True, color)
    WIN.blit(b, [x, y])


def main():
    lost = False
    walls_list = []
    bird = Bird(150, 100)
    wall = Wall()
    walls_list.append(wall)
    score = 0
    while not lost:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                lost = True
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump = True
        if len(walls_list) < WIDTH/Wall.SPACING:
            if WIDTH - walls_list[len(walls_list) - 1].image_up_x > Wall.SPACING + Wall.width:
                wall = Wall()
                walls_list.append(wall)
                print(len(walls_list))
        bird.update()

        WIN.fill(BLACK)
        for wall in walls_list[:]:
            if wall.image_up_x < wall.width * -1:
                walls_list.remove(wall)
            if bird.x + bird.width > wall.image_up_x and bird.x + bird.width + bird.width/10 < wall.image_up_x + wall.width:
                if bird.y + bird.width/5 < wall.height_up or bird.y + bird.height > wall.height_up + wall.HOLE_HEIGHT:
                    wall.hit = True
                    lost = True
                    return score
            if bird.x > wall.image_up_x + wall.width and not wall.hit:
                wall.hit = True
                score += 10
            wall.update()
            wall.draw()
        draw_message('score: ' + str(score), 30, 30, YELLOW)
        bird.draw()
        pygame.display.flip()


def gameLoop():
    done = False
    score = 0
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    score = main()
        WIN.fill(BLACK)
        draw_message('Press "t" to play!', WIDTH/2 - 130 , 300, RED)
        draw_message('Your score: ' + str(score), 140, 150, YELLOW, 60)

        pygame.display.flip()


gameLoop()