import pygame
from pygame.locals import *
import random

pygame.init()

SCREEN_WIDTH  = 800 + 21*3
SCREEN_HEIGHT = 870 + 21*3
GRID_COLOR = (220,220,220)

gamescreen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

score = 0
positions = [0]
offset = 2
# used to capture the position of the player

font = pygame.font.Font('NITEMARE.ttf', 50)
text = font.render(str(score), True, (0,0,0))
textRect = text.get_rect(
        center= ((SCREEN_WIDTH/2), (898))
    )

clock = pygame.time.Clock()


def grid():
    for line in range(21):
        pygame.draw.line(gamescreen, GRID_COLOR, (0 ,1 +((800/20 + 3)*line)), ((800+21*3), (800/20 + 3)*line + 1), width=3)
        pygame.draw.line(gamescreen, GRID_COLOR, (1 +((800/20 + 3)*line), 0), ((800/20 +3)*line + 1, (800+21*3)), width=3)

class Player(pygame.sprite.Sprite):
        
    def __init__(self) :
        super(Player, self).__init__()
        self.surf = pygame.Surface((40,40))
        self.surf.fill((119,198,110))
        self.topleftx = random.randint(0,19)*43 + 3
        self.toplefty = random.randint(0,19)*43 + 3
    
        self.rect = self.surf.get_rect(
            topleft = [self.topleftx, self.toplefty]
        )

    tolog = True
     
    def update(self, pressed_keys) :
        if pressed_keys[K_UP]:
            self.rect.move_ip(0,-43)
            self.toplefty -= 43
            self.log_pos()
        elif pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 43)
            self.toplefty += 43
            self.log_pos()
        elif pressed_keys[K_RIGHT]:
            self.rect.move_ip(43, 0)
            self.topleftx += 43
            self.log_pos()
        elif pressed_keys[K_LEFT]:
            self.rect.move_ip(-43,0)
            self.topleftx -= 43
            self.log_pos()


        if self.topleftx < 0:
            self.topleftx = SCREEN_WIDTH - 43
        if self.topleftx > SCREEN_WIDTH - 43:
            self.topleftx = 3 
        if self.toplefty < 0:
            self.toplefty = 3
            self.toplefty = (800+21*3)-43
        if self.toplefty > (800+21*3)-43:
            self.toplefty = 3
            #pygame.quit()

        self.rect = self.surf.get_rect(
            topleft = [self.topleftx, self.toplefty]   
        )
        self.log_pos()
        pygame.time.wait(95)
    def log_pos(self):
        if self.tolog:
            if self.rect != positions[-1]:
                positions.append(self.rect)

class Body(pygame.sprite.Sprite):
    def __init__(self):
        super(Body, self).__init__()
        self.initialized = False
        self.surf = pygame.surface.Surface((40,40))
        self.surf.fill((119,198,110))
        self.offset = offset
        


    def follow(self):
        self.rect = positions[- self.offset]

class Food(pygame.sprite.Sprite):
    def __init__(self):
        super(Food, self).__init__()
        self.surf = pygame.Surface((40,40))
        self.rect = self.surf.get_rect(
            topleft = (random.randint(0,19)*43 + 3, random.randint(0,19)*43 + 3)
        )
    
    def move(self):
        self.surf = pygame.Surface((40,40))
        self.rect = self.surf.get_rect(
            topleft = (random.randint(0,19)*43 + 3, random.randint(0,19)*43 + 3)
        )



def main_menu():
    # Define a Play and quit Button button
    big_play_text = font.render("PLAY", True, (200,175,20))
    big_play_textRect = big_play_text.get_rect(
        center = (SCREEN_WIDTH/2 , SCREEN_HEIGHT/4)
    )

    big_quit_text = font.render("QUIT", True, (200,175,20))
    big_quit_textRect = big_play_text.get_rect(
        center = (SCREEN_WIDTH/2 , 3*SCREEN_HEIGHT/4)
    )

    play_status = True
    play_text = font.render("PLAY", True, (255,255,255))
    play_textRect = play_text.get_rect(
        center = (SCREEN_WIDTH/2 , SCREEN_HEIGHT/4)
    )

    quit_status = False
    quit_text = font.render("QUIT", True, (255,255,255))
    quit_textRect = quit_text.get_rect(
        center = (SCREEN_WIDTH/2 , 3*SCREEN_HEIGHT/4)
    )

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        
        gamescreen.fill((0,0,0))
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_UP] or pressed_keys[K_DOWN]:
            if play_status == True:
                play_status = False
                gamescreen.blit(play_text, play_textRect)
                pygame.time.wait(200)
            else:
                play_status = True
                pygame.time.wait(200)

            if quit_status == False:
                quit_status = True
                gamescreen.blit(quit_text, quit_textRect)
                pygame.time.wait(200)
            else:
                quit_status = False
                pygame.time.wait(200)
            

        if quit_status == True and (pressed_keys[K_RETURN] or pressed_keys[K_KP_ENTER]):
            running= False
            
            
        if play_status == True and (pressed_keys[K_RETURN] or pressed_keys[K_KP_ENTER]):
            gameplay()

        if play_status == True:
            gamescreen.blit(big_play_text, big_play_textRect)
            gamescreen.blit(quit_text, quit_textRect)

        else:
            gamescreen.blit(play_text, play_textRect)
            gamescreen.blit(big_quit_text, big_quit_textRect)

        
        pygame.display.update()
        clock.tick(40)

def gameplay():
    
    global offset
    global text

    game_score = 0
    game_offset = offset
    player = Player()
    food = Food()

    
    all_sprites  = pygame.sprite.Group()
    foods        = pygame.sprite.Group()
    body_sprites = pygame.sprite.Group()

    foods.add(food)
    all_sprites.add(food,player)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
     
        gamescreen.fill((128,128,128))
        if pygame.sprite.spritecollideany(player, body_sprites):
            running = False
        if pygame.sprite.spritecollideany(player, foods):
            body = Body()
            body.offset = game_offset
            game_offset += 1
            all_sprites.add(body)
            body_sprites.add(body)
            food.move()
            game_score += 1
            print(game_score)

        text = font.render(str(game_score), True, (0,0,0), (128,128,128))
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)

        for body in body_sprites:
            body.follow() 
        
        grid()
        for sprite in all_sprites:
            gamescreen.blit(sprite.surf, sprite.rect)

        gamescreen.blit(text, textRect)
        
        pygame.display.flip()

        clock.tick(120)

def gameloop():
    main_menu()


gameloop()

pygame.quit()