import random
import pygame
pygame.font.init()
from pygame import mixer
mixer.init()

#Display
pygame.display.set_caption("Gladiator")
width, height = 1200, 600
FPS = 120
win = pygame.display.set_mode((width, height))

#Variales
glad_width, glad_height = 50, 70
glad_vel = 2
hero_MaxHP = 10
enemy_MaxHP = 10
enemy_damage = 1
enemy_vel = [glad_vel/2, glad_vel]

#User evnts
hero_get_hit = pygame.USEREVENT + 1
enemy_get_hit = pygame.USEREVENT + 2
round_prepare = pygame.USEREVENT + 3
round_end = pygame.USEREVENT + 4

winner_font = pygame.font.SysFont("comicsans", 100)

#Corners
LT, RT = [90, 85], [1040, 80]
LB, RB = [90, 500], [1040, 500]
CL, CR = [370, 120], [790,120]
Gate = [RT[0]+20, (RT[1]+RB[1])/2]

#Random Coordinates
randx = random.randrange(LT[0], RT[0]-glad_width)
randy = random.randrange(LT[1], LB[1]-glad_height)

#Load files
background = pygame.image.load("Assets/background.jpg")
background = pygame.transform.scale(background, (width, height))

gladiator = pygame.image.load("Assets/Gladiator.png")
gladiator = pygame.transform.scale(gladiator, (glad_width, glad_height))

enemy_sword = pygame.image.load("Assets/enemy.png")
enemy_sword = pygame.transform.scale(enemy_sword, (glad_width, glad_height))

class enemy(object):
    def __init__(self, posx, posy, width, height, HP, damage, vel):

        startposx = random.randrange(LT[0], RT[0]-glad_width)
        startposy = random.randrange(LT[1], LB[1]-glad_height)

        self.posx = posx
        self.posy = posy
        self.startposx = startposx
        self.startposy = startposy
        self.width = width
        self.height = height
        self.HP = HP
        self.damage = damage
        self.vel = vel

    #def draw(win):
        #win.blit(enemy_sword, (Gate[0], Gate[1]-(glad_height)/2))

    def move(self, opponent, preparation):

        print("Possition X: ", opponent.posx, "    Starting point: ", opponent.startposx)    
        print("Possition Y: ", opponent.posy, "    Starting point: ", opponent.startposy) 
        
        #if opponent.posx != opponent.startposx and opponent.posy != opponent.startposy:
        if opponent.posx > opponent.startposx:
            if opponent.posx - opponent.vel > opponent.startposx:
                    opponent.posx -= opponent.vel
            elif opponent.posx - opponent.vel <= opponent.startposx:
                    opponent.posx = opponent.startposx
        elif opponent.posx < opponent.startposx:
            if opponent.posx + opponent.vel < opponent.startposx:
                    opponent.posx += opponent.vel
            elif opponent.posx + opponent.vel >= opponent.startposx:
                    opponent.posx = opponent.startposx

            

        if opponent.posy < opponent.startposy:
            if opponent.posy + opponent.vel < opponent.startposy:
                    opponent.posy += opponent.vel
            elif opponent.posy + opponent.vel >= opponent.startposy:
                    opponent.posy = opponent.startposy
        elif opponent.posy > opponent.startposy:
            if opponent.posy - opponent.vel > opponent.startposy:
                    opponent.posy -= opponent.vel
            elif opponent.posy - opponent.vel <= opponent.startposy:
                    opponent.posy = opponent.startposy

        #print("Preparation =  ", preparation)
    
    def chase(self, hero, opponent):
        diffx, diffy = (self.posx - hero.x, self.posy - hero.y)
        stepx, stepy = (diffx / FPS, diffy / FPS)
        opponent.set_position(self.posx + stepx, self.posy + stepy)

        
def draw_looser(text):
    draw_text = winner_font.render(text, 1, (0, 0, 0))
    win.blit(draw_text, (width/2 - draw_text.get_width()/2, height/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def draw_round(text, number):
    draw_text = winner_font.render(text, 1, (0, 0, 0))
    draw_number = winner_font.render(number, 1, (0, 0, 0))
    win.blit(draw_text, (width/2 - draw_text.get_width()/2 - draw_number.get_width(), height/2 - draw_text.get_height()/2))
    win.blit(draw_number, (width/2 + draw_text.get_width()/2, height/2 - draw_text.get_height()/2))
    pygame.display.update()

def draw_window(hero, hero_health_bar, health_bar, opponent, round_num, preparation):
    win.blit(background, (0,0))
    if len(opponent) != 0:
        for i in range(len(opponent)):
            win.blit(enemy_sword, (opponent[i].posx, opponent[i].posy))
    win.blit(gladiator, (hero.x, hero.y))  

    pygame.draw.rect(win, (0, 0, 0), health_bar, 2)     #Draw Health Bar
    for OneHP in hero_health_bar:                       #Draw HPs
        pygame.draw.rect(win, (255, 0, 0), OneHP)

    if preparation == True:
        draw_round("Round", str(round_num))

    #point = pygame.draw.circle(win, (255,0,0), [150, 470], 2)
    pygame.display.update()


def character_movement(hero):
    #Movement
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        if hero.y > CL[1] and hero.y + glad_height < 470 and hero.x - glad_vel > LT[0]:
            hero.x -= glad_vel
        elif hero.y + glad_height >= 470 and hero.x - glad_vel > 150:
            hero.x -= glad_vel
        elif hero.y < CL[1] and hero.x + glad_width <= CL[0] and hero.x - glad_vel > LT[0]:
            hero.x -= glad_vel
        elif hero.y < CL[1] and hero.x >= CR[0] and hero.x - glad_vel > CR[0]:
            hero.x -= glad_vel
    if keys[pygame.K_d]:
        if hero.y >= CL[1] and hero.x + glad_vel + glad_width < RT[0]:
            hero.x += glad_vel
        elif hero.y < CL[1] and hero.x + glad_vel + glad_width < CL[0]:
            hero.x += glad_vel
        elif hero.y < CL[1] and hero.x >= CR[0] and hero.x + glad_vel + glad_width < RT[0]:
            hero.x += glad_vel
    if keys[pygame.K_w]:
        if hero.x >= LT[0] and hero.x + glad_width <= CL[0] and hero.y - glad_vel > LT[1]:
            hero.y -= glad_vel
        elif hero.x <= RT[0] and hero.x >= CR[0] and hero.y - glad_vel > RT[1]:
            hero.y -= glad_vel
        elif hero.x + glad_width >= CL[0] and hero.x <= CR[0] and hero.y - glad_vel > CL[1]:
            hero.y -= glad_vel
    if keys[pygame.K_s]:
        if hero.x > 150 and hero.y + glad_vel + glad_height < LB[1]:
            hero.y += glad_vel
        elif hero.x < 150 and hero.y + glad_vel + glad_height < 470:
            hero.y += glad_vel



def health(hero, hero_health_bar, health_bar, current_HP):
    #Stick Health Bar to Hero
    health_bar.x = hero.x
    health_bar.y = hero.y - 5

    #print("Hero_health_bar: ", len(hero_health_bar))

    #Fill Health Bar with HPs
    if len(hero_health_bar) == 0:
        for i in range(current_HP):
            OneHP = pygame.Rect(health_bar.x + (i*5) + 1, health_bar.y + 1, 5, 5)
            hero_health_bar.append(OneHP)
       
    #Stick HPs to Health Bar
    for i in range(len(hero_health_bar)):
        hero_health_bar[i].x = health_bar.x + (i*5) + 1 
        hero_health_bar[i].y = health_bar.y + 1

def main():
    #Define objects
    opponent = []
    hero = pygame.Rect(LT[0]+50, (LB[1]-LT[1])/2, glad_width, glad_height)
    health_bar = pygame.Rect(hero.x , hero.y - 5, glad_width + 2, 7)
    hero_health_bar = []
    current_HP = hero_MaxHP
    preparation = False
    round_num = 7

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.event.post(pygame.event.Event(hero_get_hit))

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pygame.event.post(pygame.event.Event(round_prepare))

            if event.type == hero_get_hit:
                current_HP -= 1
                for OneHP in hero_health_bar:
                    if len(hero_health_bar) != current_HP:
                        hero_health_bar.remove(OneHP)
                        print("Remove HP", len(hero_health_bar))
                        health(hero, hero_health_bar, health_bar, current_HP)
                        draw_window(hero, hero_health_bar, health_bar, opponent)
                #print("Current HP: ", current_HP)
        
            if event.type == round_prepare:
                round_num += 1
                if round_num % 2 == 0:
                    for i in range(int(round_num/2)):
                        print("i= ", i)
                        if i % 2 != 0:
                            enemy_model = pygame.Rect(Gate[0], Gate[1], glad_width, glad_height)
                            opponent.append(enemy_model)
                            opponent [i] = enemy(enemy_model.x, enemy_model.y, glad_width, glad_height, enemy_MaxHP, enemy_damage, enemy_vel[0]) 
                        if i % 2 == 0:
                            enemy_model = pygame.Rect(Gate[0], Gate[1], glad_width, glad_height)
                            opponent.append(enemy_model)
                            opponent [i] = enemy(enemy_model.x, enemy_model.y, glad_width, glad_height, enemy_MaxHP, enemy_damage, enemy_vel[1])
                else:       
                    for i in range(int((round_num+1)/2)):
                        print("I= ", i)
                        if i % 2 != 0:
                            enemy_model = pygame.Rect(Gate[0], Gate[1], glad_width, glad_height)
                            opponent.append(enemy_model)
                            opponent [i] = enemy(enemy_model.x, enemy_model.y, glad_width, glad_height, enemy_MaxHP, enemy_damage, enemy_vel[0]) 
                        if i % 2 == 0:
                            enemy_model = pygame.Rect(Gate[0], Gate[1], glad_width, glad_height)
                            opponent.append(enemy_model)
                            opponent [i] = enemy(enemy_model.x, enemy_model.y, glad_width, glad_height, enemy_MaxHP, enemy_damage, enemy_vel[1])
                print("Set preparation to True")
                preparation = True
        
        if current_HP == 0:
            looser_text = "You lost, bitch!"
            draw_looser(looser_text)
            break                 

        if preparation == True:
            ready = 0
            for i in range(len(opponent)):
                if opponent[i].posx != opponent[i].startposx or opponent[i].posy != opponent[i].startposy:
                    opponent[i].move(opponent[i], preparation)
                elif opponent[i].posx == opponent[i].startposx and opponent[i].posy == opponent[i].startposy:
                    ready += 1
                    print("Ready: ", ready)

                if ready == len(opponent):
                    print("Ready")
                    preparation = False

        character_movement(hero)
        health(hero, hero_health_bar, health_bar, current_HP)
        draw_window(hero, hero_health_bar, health_bar, opponent, round_num, preparation)


main()
        