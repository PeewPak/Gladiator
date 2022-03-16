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
round_start = pygame.USEREVENT + 3
round_end = pygame.USEREVENT + 4

winner_font = pygame.font.SysFont("comicsans", 100)

#Corners
LT, RT = [90, 85], [1040, 80]
LB, RB = [90, 500], [1040, 500]
CL, CR = [370, 120], [790,120]
Gate = [RT[0]+20, (RT[1]+RB[1])/2]


#Load files
background = pygame.image.load("Assets/background.jpg")
background = pygame.transform.scale(background, (width, height))

gladiator = pygame.image.load("Assets/Gladiator.png")
gladiator = pygame.transform.scale(gladiator, (glad_width, glad_height))

enemy_sword = pygame.image.load("Assets/enemy.png")
enemy_sword = pygame.transform.scale(enemy_sword, (glad_width, glad_height))

class enemy(object):
    def __init__(self, posx, posy, width, height, HP, damage, vel):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.HP = HP
        self.damage = damage
        self.vel = vel

    #def draw(win):
        #win.blit(enemy_sword, (enemy.posx, enemy.posy))

    def move(randx, randy):
        diffx, diffy = (enemy.posx - randx, enemy.posy - randy)
        stepx, stepy = (diffx / FPS, diffy / FPS)
        enemy.set_position(enemy.posx + stepx, enemy.posy + stepy) 

        

def draw_looser(text):
    draw_text = winner_font.render(text, 1, (0, 0, 0))
    win.blit(draw_text, (width/2 - draw_text.get_width()/2, height/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def draw_round(text):
    draw_text = winner_font.render(text, 1, (0, 0, 0))
    win.blit(draw_text, (width/2 - draw_text.get_width()/2, height/2 - draw_text.get_height()/2))
    pygame.display.update()

def draw_window(hero, hero_health_bar, health_bar, opponent):
    win.blit(background, (0,0))
    win.blit(gladiator, (hero.x, hero.y))       

    pygame.draw.rect(win, (0, 0, 0), health_bar, 2)     #Draw Health Bar
    for OneHP in hero_health_bar:                       #Draw HPs
        pygame.draw.rect(win, (255, 0, 0), OneHP)

    if len(opponent) != 0:
        for i in range(len(opponent)):
            win.blit(enemy_sword, (opponent[i].posx, opponent[i].posy))

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
    #opponent = pygame.Rect(Gate[0], Gate[1], glad_width, glad_height)
    opponent = []
    hero = pygame.Rect(LT[0]+50, (LB[1]-LT[1])/2, glad_width, glad_height)
    health_bar = pygame.Rect(hero.x , hero.y - 5, glad_width + 2, 7)
    hero_health_bar = []
    current_HP = hero_MaxHP
    round_num = 5

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
                    pygame.event.post(pygame.event.Event(round_start))

            if event.type == hero_get_hit:
                current_HP -= 1
                for OneHP in hero_health_bar:
                    if len(hero_health_bar) != current_HP:
                        hero_health_bar.remove(OneHP)
                        print("Remove HP", len(hero_health_bar))
                        health(hero, hero_health_bar, health_bar, current_HP)
                        draw_window(hero, hero_health_bar, health_bar, opponent)
                #print("Current HP: ", current_HP)

            if event.type == round_start:
                round_num += 1
                if round_num % 2 == 0:
                    for i in range(int(round_num/2)):
                        randx = random.randrange(LT[0], RT[0]-glad_width)
                        randy = random.randrange(LT[1], LB[1]-glad_height)
                        print("i= ", i)
                        if i % 2 != 0:
                            print("Tutajj też")
                            enemy_model = pygame.Rect(randx, randy, glad_width, glad_height)
                            opponent.append(enemy_model)
                            opponent [i] = enemy(enemy_model.x, enemy_model.y, glad_width, glad_height, enemy_MaxHP, enemy_damage, enemy_vel[0])
                            print("ranx ", randx) 
                        if i % 2 == 0:
                            print("Albo chociaż tu")
                            enemy_model = pygame.Rect(randx, randy, glad_width, glad_height)
                            opponent.append(enemy_model)
                            opponent [i] = enemy(enemy_model.x, enemy_model.y, glad_width, glad_height, enemy_MaxHP, enemy_damage, enemy_vel[1])
                            print("ranx ", randx)
                else:       
                    for i in range(int((round_num+1)/2)):
                        randx = random.randrange(LT[0], RT[0]-glad_width)
                        randy = random.randrange(LT[1], LB[1]-glad_height)          
                        print("i= ", i)
                        if i % 2 != 0:
                            print("działą")
                            enemy_model = pygame.Rect(randx, randy, glad_width, glad_height)
                            opponent.append(enemy_model)
                            opponent [i] = enemy(enemy_model.x, enemy_model.y, glad_width, glad_height, enemy_MaxHP, enemy_damage, enemy_vel[0])
                            print("ranx ", randx)
                        if i % 2 == 0:
                            print("Działa też")
                            enemy_model = pygame.Rect(randx, randy, glad_width, glad_height)
                            opponent.append(enemy_model)
                            opponent [i] = enemy(enemy_model.x, enemy_model.y, glad_width, glad_height, enemy_MaxHP, enemy_damage, enemy_vel[1])
                            print("ranx ", randx)

        if current_HP == 0:
            looser_text = "You lost, bitch!"
            draw_looser(looser_text)
            break                 


        character_movement(hero)
        health(hero, hero_health_bar, health_bar, current_HP)
        draw_window(hero, hero_health_bar, health_bar, opponent)


main()
        