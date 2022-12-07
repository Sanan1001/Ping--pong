from pygame import *
from random import randint
mixer.init()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_y, player_x, player_speed,size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_y,size_x))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def updateR(self):
        keys_pressed = key.get_pressed()    
        if keys_pressed[K_w] and self.rect.y > 3:
            self.rect.y -= 5
        if keys_pressed[K_s] and self.rect.y < 400 :
            self.rect.y += 5

    def updateL(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_UP] and self.rect.y > 3:
            self.rect.y -= 5
        if keys_pressed[K_DOWN] and self.rect.y < 400:
            self.rect.y += 5

clock = time.Clock()

game = True
finish = False

font.init()
#print(font.get_fonts() ) 
font1 = font.SysFont(None,60)
font2 = font.Font(None, 110)
lose1 = font2.render('PLAYER 1 LOSE!', True, (180,0,0))
lose2 = font2.render('PLAYER 2 LOSE!', True, (180,0,0))

window = display.set_mode((800 , 500))
display.set_caption('Ping-pong')

player1 = Player('player.png', 200, 50, 10, 150, 60)
player2 = Player('player.png', 200, 700, 10, 150, 60)
ball = GameSprite('ping-pong-ball.png', 200, 200, 10, 50,50)

background = transform.scale(image.load("фон.jpg"), (1000 , 900))

knock = mixer.Sound('knock.ogg')
knock.set_volume(0.5)
bounce = mixer.Sound('bounce.ogg')
bounce.set_volume(0.5)
lose = mixer.Sound('wasted.ogg')
lose.set_volume(0.1)
r = mixer.Sound('r.ogg') 
r.set_volume(0.1)
mixer.music.load('overworld day.mp3')
mixer.music.set_volume(0.1)
mixer.music.play(-1)


speed_y = 3
speed_x = 3

FPS = 60

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:
        window.blit(background, (0,0))
        player1.reset()
        player2.reset()
        ball.reset()
        ball.rect.y += speed_y
        ball.rect.x += speed_x

        keys_pressed = key.get_pressed()  
        if keys_pressed[K_r]: # не нажимайте одновременно много раз 
            r.play()

        if ball.rect.y > 450 or ball.rect.y < 0:
            speed_y *= -1    
            bounce.play()

        if sprite.collide_rect(player1, ball) or sprite.collide_rect(player2, ball):
            speed_x *= -1
            speed_y *= 1  
            knock.play()

        if ball.rect.x < 0:
            finish = True
            window.blit(lose1,(100, 100))
            lose.play()

        if ball.rect.x >= 750:
            finish = True
            window.blit(lose2,(100, 100))
            lose.play()

        player1.updateR()
        player2.updateL()
        ball.update()

    display.update()
    clock.tick(FPS)