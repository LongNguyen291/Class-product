from typing import Any
import pygame
from pygame.locals import *
from pygame import mixer


pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()
vec = pygame.math.Vector2 #2 Dimensional

clock = pygame.time.Clock()
fps = 90

#display window
window_height = 1200
window_width = 1500
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Platformer Game')

#game variables
tile_size = 75
game_over = 0


#images
sun_img = pygame.image.load('img/sun1.png')
bg_img = pygame.image.load('img/background.jpg')
dirt_img = pygame.image.load('img/dirt.jpg')
grass_img = pygame.image.load('img/grass.jpg')
restart_img = pygame.image.load('img/killerqueen.png')
win_img = pygame.image.load('img/buffedsteve.jpg')
'''
start_img = pygame.image.load('img/')
start_img = pygame.image.load('img/')
'''
#sound effects
death_fx = pygame.mixer.Sound('img/death.mp3')
death_fx.set_volume(1)
jump_fx = pygame.mixer.Sound('img/jump.mp3')
jump_fx.set_volume(1)

#grid
'''def draw_grid():
    for line in range(0,20):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (window_width, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line *tile_size, 0), (line *tile_size, window_height))'''

#button
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False
        #get mouse position:
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked condition:
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True      
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #draw button
        window.blit(self.image, self.rect)

        return action

#player
class Player():
    def __init__(self, x, y):
        self.reset(x, y)


    def update(self, game_over):
        dx = 0
        dy = 0
        walk_cd = 10

        if game_over == 0:

            #get keypresses
            key = pygame.key.get_pressed()
            if key[pygame.K_w] and self.jumped == False and self.in_air == False:
                jump_fx.play()
                self.vel_y = -28
                self.jumped = True
            if key[pygame.K_w] == False:
                self.jumped = False
            if key[pygame.K_a]:
                dx -= 8
                self.counter += 1
                self.direction = -1
            if key[pygame.K_d]:
                dx += 8
                self.counter += 1
                self.direction = 1
            if key[pygame.K_a] == False and key[pygame.K_d] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            #animation
            if self.counter > walk_cd:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]
                

            #add gravity
            self.vel_y += 1.5
            if self.vel_y > 15:
                self.vel_y = 15
            dy += self.vel_y

            if self.rect.bottom > window_height:
                self.rect.bottom = window_height
                dy=0
            if self.rect.x < 0:
                self.rect.x = 0
                dx = 0
            if self.rect.right > window_width:
                self.rect.right = window_width
                dx = 0

            #check collision
            self.in_air = True
            for tile in world.tile_list:

                #check for collision in x direction:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                
                #check for collision in y direction:
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #check if below the ground i.e. jumping
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y =0
                    #check if above the ground i.e. jumping
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y =0
                        self.in_air = False

                #check for collision with enemies:
                if pygame.sprite.spritecollide(self, hogrider_group, False):
                    game_over = -1
                    death_fx.play()
                if pygame.sprite.spritecollide(self, mamtom_group, False):
                    game_over = -1
                    death_fx.play()
                if pygame.sprite.spritecollide(self, robloxman_group, False):
                    game_over = -1
                    death_fx.play()
                if pygame.sprite.spritecollide(self, primo_group, False):
                    game_over = 1

                
            #update player coordination
            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            self.image = self.dead_image
            self.rect.y -= 5

        #draw player
        window.blit(self.image, self.rect)
        

        return game_over
    
    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range (1,5):
            img_right = pygame.image.load(f'img/steve{num}.png')
            img_right = pygame.transform.scale(img_right, (tile_size, tile_size))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_image = pygame.image.load('img/srpelosans1.png')
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True

#world
class World():
    def __init__(self, data):
        self.tile_list = []
        
        row_count = 0
        for row in data:
            col_count= 0
            for tile in row:
                #dirt block
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                #grass block
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                #hogrider
                if tile == 3:
                    hogrider = Hogrider(col_count * tile_size - 40, row_count * tile_size - 50)
                    hogrider_group.add(hogrider)
                #Mam tom
                if tile == 4:
                    mamtom = Mamtom(col_count * tile_size, row_count * tile_size+(tile_size//4))
                    mamtom_group.add(mamtom)
                #RobloxMan
                if tile == 5:
                    robloxman = Robloxman(col_count * tile_size, row_count * tile_size - 15)
                    robloxman_group.add(robloxman)
                if tile == 6:
                    primogem = Primogem(col_count * tile_size, row_count * tile_size)
                    primo_group.add(primogem)

                col_count += 1
            row_count += 1
    
    def draw(self):
        for tile in self.tile_list:
            window.blit(tile[0], tile[1])
            
    
#Hogrider
class Hogrider(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img_hogrider = pygame.image.load('img/hogrider.png')
        self.image = pygame.image.load('img/hogrider.png')
        self.image = pygame.transform.scale(img_hogrider, (tile_size*1.75, tile_size*1.75))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 1

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > tile_size * 3:
            self.move_direction *= -1
            self.move_counter *= -1
        
        window.blit(self.image, self.rect)
        '''pygame.draw.rect(window, (255, 255, 255), self.rect, 2)'''


#Robloxman

class Robloxman(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img_robloxman = pygame.image.load('img/robloxman.png')
        self.image = pygame.image.load('img/robloxman.png')
        self.image = pygame.transform.scale(img_robloxman, (tile_size*1.25, tile_size*1.25))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > tile_size * 1.5:
            self.move_direction *= -1
            self.move_counter *= -1
        
        window.blit(self.image, self.rect)
        

#Mamtom
class Mamtom(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/mamtom.jpg')
        self.image = pygame.transform.scale(img, (tile_size, tile_size * 0.75))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Primogem(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/ticket.png')
        self.image = pygame.transform.scale(img, (tile_size*1.5, tile_size * 1.5))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



world_data = [
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	2,	2,	0,	0,	0,	0,	0,	0,	0,	0,	0,	6,	0],
[0,	0,	2,	2,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	2,	2,	2,	2],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	2,	0,	0,	0,	1,	1,	1],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1],
[2,	2,	0,	0,	5,	0,	0,	0,	5,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1],
[0,	0,	0,	2,	2,	2,	2,	2,	2,	2,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1],
[0,	0,	0,	0,	1,	1,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	3,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	2,	2,	2,	2,	2,	2,	2,	2,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	1,	1,	1,	1,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	2,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	2],
[0,	0,	0,	2,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1],
[0,	0,	0,	1,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1],
[2,	2,	2,	1,	2,	2,	1,	2,	2,	2,	4,	4,	4,	4,	2,	2,	2,	2,	2,	1],
]


player = Player(tile_size, window_height - tile_size*2)

hogrider_group = pygame.sprite.Group()
robloxman_group = pygame.sprite.Group()
mamtom_group = pygame.sprite.Group()
primo_group = pygame.sprite.Group()

world = World(world_data)

#create buttons
restart_button = Button(window_width//2-400,  window_height//2-400, restart_img)

#main loop
run = True
while run:

    clock.tick(fps)
    
    #background images
    window.blit(bg_img, (0,0))
    window.blit(sun_img, (1100,50))

    world.draw()

    if game_over == 0:
        hogrider_group.update()
        robloxman_group.update()
    hogrider_group.draw(window)
    robloxman_group.draw(window)
    mamtom_group.draw(window)
    primo_group.draw(window)

    game_over = player.update(game_over)

    #if player ded:
    if game_over == -1:
        if restart_button.draw():
            player.reset(tile_size, window_height - tile_size*2)
            game_over = 0

    #if player wins
    if game_over == 1:
        window.blit(win_img, (window_width/10, window_height / 5))
    
    #quit system
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

    
            
pygame.quit()