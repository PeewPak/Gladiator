import random
import math
import time
import pygame
pygame.font.init()
from pygame import mixer
mixer.init()

#Display
pygame.display.set_caption("Gladiator")
width, height = 1200, 600
FPS = 120
win = pygame.display.set_mode((width, height))
basetime = time.time()
cooldown = time.time()

#Hero
glad_width, glad_height = 48, 100
glad_vel = 2
hero_MaxHP = 10
hero_damage = 1
attack_range = 40


               #stand  right  left   attack
hero_position = [True, False, False, 0]
          #right left
hero_count = [0, 0]

#Enemy
enemy_width, enemy_height = 48, 100

#User evnts
hero_get_hit = pygame.USEREVENT + 1
round_prepare = pygame.USEREVENT + 2
round_start = pygame.USEREVENT + 3

winner_font = pygame.font.SysFont("comicsans", 100)
smaller_font = pygame.font.SysFont("comicsans", 50) 

#Corners
LT, RT = [90, 85], [1040, 80]
LB, RB = [90, 500], [1040, 500]
CL, CR = [370, 120], [790,120]
Gate = [RT[0]+20, (RT[1]+RB[1])/2]

#Load files
background = pygame.image.load("Assets/background_copy.jpg")
background = pygame.transform.scale(background, (width, height))

gladiator = pygame.image.load("Assets/Gladiator_front.png")
gladiator = pygame.transform.scale(gladiator, (glad_width, glad_height))
gladiator_attack = [pygame.image.load("Assets/Gladiator_attackR.png"), pygame.image.load("Assets/Gladiator_attackL.png")]
gladiator_attack = [pygame.transform.scale(gladiator_attack[0], (glad_width, glad_height)), pygame.transform.scale(gladiator_attack[1], (glad_width, glad_height))]
gladiatorR = [pygame.image.load("Assets/Gladiator_R1.png"), pygame.image.load("Assets/Gladiator_R2.png"), pygame.image.load("Assets/Gladiator_R3.png"), pygame.image.load("Assets/Gladiator_R4.png"), pygame.image.load("Assets/Gladiator_R5.png")]
gladiatorR = [pygame.transform.scale(gladiatorR[0], (glad_width, glad_height)), pygame.transform.scale(gladiatorR[1], (glad_width, glad_height)), pygame.transform.scale(gladiatorR[2], (glad_width, glad_height)), pygame.transform.scale(gladiatorR[3], (glad_width, glad_height)), pygame.transform.scale(gladiatorR[4], (glad_width, glad_height))]
gladiatorL = [pygame.image.load("Assets/Gladiator_L1.png"), pygame.image.load("Assets/Gladiator_L2.png"), pygame.image.load("Assets/Gladiator_L3.png"), pygame.image.load("Assets/Gladiator_L4.png"), pygame.image.load("Assets/Gladiator_L5.png")]
gladiatorL = [pygame.transform.scale(gladiatorL[0], (glad_width, glad_height)), pygame.transform.scale(gladiatorL[1], (glad_width, glad_height)), pygame.transform.scale(gladiatorL[2], (glad_width, glad_height)), pygame.transform.scale(gladiatorL[3], (glad_width, glad_height)), pygame.transform.scale(gladiatorL[4], (glad_width, glad_height))]

lionR = [pygame.image.load("Assets/lionR1.png"), pygame.image.load("Assets/lionR2.png"), pygame.image.load("Assets/lionR3.png"), pygame.image.load("Assets/lionR4.png"), pygame.image.load("Assets/lionR5.png")]
lionR = [pygame.transform.scale(lionR[0], (enemy_width, enemy_height)), pygame.transform.scale(lionR[1], (enemy_width, enemy_height)), pygame.transform.scale(lionR[2], (enemy_width, enemy_height)), pygame.transform.scale(lionR[3], (enemy_width, enemy_height)), pygame.transform.scale(lionR[4], (enemy_width, enemy_height)),]
enemy_sword = pygame.image.load("Assets/enemy.png")
enemy_sword = pygame.transform.scale(enemy_sword, (enemy_width, enemy_height))
#enemy_dead = pygame.transform.rotate(enemy_sword, 270)

hit_sound = mixer.Sound("Assets/hit.wav")
miss_sound = mixer.Sound("Assets/miss.wav")
death_sound = mixer.Sound("Assets/Death.wav")
roblox_sound = mixer.Sound("Assets/roblox.wav")

class enemy(object):
    def __init__(self, posx, posy, width, height):

        startposx = random.randrange(LT[0], RT[0]-glad_width)
        startposy = random.randrange(LT[1], LB[1]-glad_height)
        vel = random.uniform(0.7, 1.5)
        MaxHP = 5
        damage = 1
        currentHP = MaxHP

        self.posx = posx
        self.posy = posy
        self.startposx = startposx
        self.startposy = startposy
        self.width = width
        self.height = height
        self.MaxHP = MaxHP
        self.currentHP = currentHP
        self.damage = damage
        self.vel = vel

    def move(self, opponent):


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
    
    def chase(self, hero, opponent):

        if opponent.posx > hero.x + glad_width:                     #Enemy on right side
            opponent.posx -= opponent.vel
        elif opponent.posx + enemy_width < hero.x:                  #Enemy on left side
            opponent.posx += opponent.vel
        else:
            if math.fabs(opponent.posx + enemy_width/2 - hero.x) < math.fabs(opponent.posx + enemy_width/2 - (hero.x + glad_width)):
                opponent.posx -= opponent.vel
            else:
                opponent.posx += opponent.vel


        if opponent.posy < hero.y:                                  #Enemy above
                opponent.posy += opponent.vel
        elif opponent.posy - glad_height > hero.y:                  #Enemy below
                opponent.posy -= opponent.vel
        else:
            if math.fabs(opponent.posy + enemy_height/2 - hero.y) < math.fabs(opponent.posy + enemy_height/2 - hero.y + glad_height):
                opponent.posy -= opponent.vel
            else:
                opponent.posy += opponent.vel

    def health(self):
        #Create Health Bar
        health_bar = pygame.Rect(self.posx, self.posy - 2, self.width + 2, 7)
        health_points = []

        self.healthbar = health_bar
        self.healthpoints = health_points

        #Stick Health Bar to enemy model
        health_bar.x = self.posx
        health_bar.y = self.posy

        #Fill Health Bar with HPs
        if len(health_points) == 0:
            for i in range(self.currentHP):
                OneHP = pygame.Rect(health_bar.x + (i*(enemy_width +2)/self.MaxHP) + 1, health_bar.y + 1, (self.width + 2)/self.MaxHP, 5)
                health_points.append(OneHP)

        #Stick HPs to Health Bar
        for i in range(len(health_points)):
            health_points[i].x = health_bar.x + (i*(self.width + 2)/self.MaxHP) + 1 
            health_points[i].y = health_bar.y + 1


def left_knocback(hero, opponent, hero_knockback, enemy_knockback):
    if hero.x + glad_width + hero_knockback < RT[0]:
        hero.x += hero_knockback
    else:
        hero.x = RT[0]-glad_width

    if opponent.posx - enemy_knockback > LT[0]:
        opponent.posx -= enemy_knockback
    else:
        opponent.posx = LT[0]
    
def right_knockback(hero, opponent, hero_knockback, enemy_knockback):
    if hero.x - hero_knockback > LT[0]:
        hero.x -= hero_knockback
    else:
        hero.x = LT[0]

    if opponent.posx + enemy_knockback < RT[0]:
        opponent.posx += enemy_knockback
    else:
        opponent.posx = RT[0]-opponent.width


def hero_hit(opponent, hero, swordL, swordR):
    global cooldown
    global hero_position
    hero_knockback = 0
    enemy_knockback = 50

    cooldown = time.time()
    for i in range(len(opponent)):
        if hero.y > opponent[i].posy and hero.y < opponent[i].posy + opponent[i].height or opponent[i].posy > hero.y and opponent[i].posy < hero.y + glad_height/2 :
            if opponent[i].posx + enemy_width > swordL.x and opponent[i].posx + enemy_width < hero.x + glad_width:
                    #print("Left hit")
                    #hero_position[3] = 2
                    hit_sound.play()
                    left_knocback(hero, opponent[i], hero_knockback, enemy_knockback)
                    enemy_get_hit(opponent[i], opponent)
            elif opponent[i].posx < swordR.x + attack_range and opponent[i].posx > hero.x:
                    #print("Right hit")
                    #hero_position[3] = 1
                    hit_sound.play()
                    right_knockback(hero, opponent[i], hero_knockback, enemy_knockback)
                    enemy_get_hit(opponent[i], opponent)
            #else:
                #choose = random.randrange(1,2)
                #hero_position[3] = choose
                #miss_sound.play()           

def enemy_hit(opponent, hero):
    hero_knockback = 50
    enemy_knockback = 50

    for i in range(len(opponent)):
        if opponent[i].posy >= hero.y - 5 and opponent[i].posy <= hero.y + glad_height/2:
            if opponent[i].posx <= hero.x + glad_width and opponent[i].posx >= hero.x:          #Enemy on right side
                pygame.event.post(pygame.event.Event(hero_get_hit))
                right_knockback(hero, opponent[i], hero_knockback, enemy_knockback)
            elif opponent[i].posx + enemy_width >= hero.x and opponent[i].posx + enemy_width <= hero.x + glad_width:            #Enemy on left side
                pygame.event.post(pygame.event.Event(hero_get_hit))
                left_knocback(hero, opponent[i], hero_knockback, enemy_knockback)
        
def enemy_get_hit(opponent, horde):
    global basetime

    opponent.currentHP -= hero_damage
    for OneHP in opponent.healthpoints:
        if len(opponent.healthpoints) != opponent.currentHP:
            opponent.healthpoints.remove(OneHP)
    if opponent.currentHP == 0:
        horde.remove(opponent)
        death_sound.play()
        if len(horde) == 0:
            basetime = time.time()


def check_start(preparation, opponent):
    global basetime

    if len(opponent) == 0 and preparation == False and (time.time() - basetime) > 3:
        pygame.event.post(pygame.event.Event(round_prepare))

def draw_looser(text):
    draw_text = winner_font.render(text, 1, (0, 0, 0))
    win.blit(draw_text, (width/2 - draw_text.get_width()/2, height/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def draw_round(text, number):
    prepare = smaller_font.render("Prepare!", 1, (0, 0, 0))
    draw_text = winner_font.render(text, 1, (0, 0, 0))
    draw_number = winner_font.render(number, 1, (0, 0, 0))
    win.blit(draw_text, (width/2 - draw_text.get_width()/2 - draw_number.get_width(), height/2 - draw_text.get_height()))
    win.blit(draw_number, (width/2 + draw_text.get_width()/2, height/2 - draw_text.get_height()))
    win.blit(prepare, (width/2 - prepare.get_width()/2, height/2))
    pygame.display.update()

def draw_counter():
    global basetime
    text = "Next round in"
    number = 3 - int(time.time() - basetime)
    number = str(number)
    draw_text = smaller_font.render(text, 1, (255, 0, 0))
    draw_number = smaller_font.render(number, 1, (255, 0, 0))
    win.blit(draw_text, (width/2 - draw_text.get_width()/2 - draw_number.get_width(), height - draw_text.get_height()))
    win.blit(draw_number, (width/2 + draw_text.get_width()/2, height - draw_text.get_height()))
    pygame.display.update()

def draw_hero(hero):
    global cooldown
    global hero_position
    global hero_count

    #if time.time() - cooldown > 1:    
        #hero_position[0] = True
        #hero_position[3] = 0
    #print(hero_position[3])
    if hero_position[3] != 0:                         #Draw attack
        if hero_position[3] == 1:
            win.blit(gladiator_attack[0], (hero.x, hero.y))
        #elif hero_attack == 2:
            #win.blit(gladiator_attack[1][, (hero.x, hero.y))
    elif hero_position[0] == True:
        win.blit(gladiator, (hero.x, hero.y))               #Draw standing hero
    elif hero_position[1] == True:
        win.blit(gladiatorR[hero_count[0]], (hero.x, hero.y))    #Draw right hero
        hero_count[0] += 1
        if hero_count[0] == 4:
            hero_count[0] = 0
        hero_position[1] = False
        hero_position[0] = True
    elif hero_position[2] == True:
        win.blit(gladiatorL[hero_count[1]], (hero.x, hero.y))    #Draw right hero
        hero_count[1] += 1
        if hero_count[1] == 4:
            hero_count[1] = 0
        hero_position[0] = True
        hero_position[2] = False

def draw_enemy(opponent):
    if len(opponent) != 0:     
        for i in range(len(opponent)):
            #if opponent[i].currentHP != 0:
            win.blit(enemy_sword, (opponent[i].posx, opponent[i].posy))     #Draw opponents
            pygame.draw.rect(win, (0, 0, 0), opponent[i].healthbar, 2)      #Draw enemy health bars
            for OneHP in opponent[i].healthpoints:              
                    pygame.draw.rect(win, (255, 0, 0), OneHP)                   #Draw enemy HPs
            #else:
                #win.blit(enemy_dead, (opponent[i].posx, opponent[i].posy))

def draw_window(hero, hero_health_bar, health_bar, opponent, round_num, preparation):
    win.blit(background, (0,0))                         #Draw background

    draw_enemy(opponent)
    draw_hero(hero)                                     #Draw hero
    pygame.draw.rect(win, (0, 0, 0), health_bar, 2)     #Draw Health Bar
    for OneHP in hero_health_bar:                       #Draw HPs
        pygame.draw.rect(win, (255, 0, 0), OneHP)

    if preparation == True:                             #Draw round number
        draw_round("Round", str(round_num))
        
    if len(opponent) == 0:                              #Draw time to start
        draw_counter()

    #point = pygame.draw.circle(win, (255,0,0), [150, 470], 2)
    pygame.display.update()


def character_movement(hero, swordR, swordL):
    global hero_position
    global hero_count

    #Attach swords
    swordR.x = hero.x - attack_range
    swordR.y = hero.y
    swordL.x = hero.x + glad_width
    swordL.y = hero.y 


    #Movement
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        if hero.y > CL[1] and hero.y + glad_height < 470 and hero.x - glad_vel > LT[0]:
            hero.x -= glad_vel
            hero_position[0] = False
            hero_position[2] = True
        elif hero.y + glad_height >= 470 and hero.x - glad_vel > 150:
            hero.x -= glad_vel
            hero_position[0] = False
            hero_position[2] = True
        elif hero.y < CL[1] and hero.x + glad_width <= CL[0] and hero.x - glad_vel > LT[0]:
            hero.x -= glad_vel
            hero_position[0] = False
            hero_position[2] = True
        elif hero.y < CL[1] and hero.x >= CR[0] and hero.x - glad_vel > CR[0]:
            hero.x -= glad_vel
            hero_position[0] = False
            hero_position[2] = True
    if keys[pygame.K_d]:
        if hero.y >= CL[1] and hero.x + glad_vel + glad_width < RT[0]:
            hero.x += glad_vel
            hero_position[0] = False
            hero_position[1] = True
        elif hero.y < CL[1] and hero.x + glad_vel + glad_width < CL[0]:
            hero.x += glad_vel
            hero_position[0] = False
            hero_position[1] = True
        elif hero.y < CL[1] and hero.x >= CR[0] and hero.x + glad_vel + glad_width < RT[0]:
            hero.x += glad_vel
            hero_position[0] = False
            hero_position[1] = True
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

def health(hero, hero_health_bar, health_bar, hero_current_HP, opponent):
    #Stick Health Bar to Hero
    health_bar.x = hero.x
    health_bar.y = hero.y - 5


    #Fill Health Bar with HPs
    if len(hero_health_bar) == 0:
        for i in range(hero_current_HP):
            OneHP = pygame.Rect(health_bar.x + (i*(glad_width + 2)/hero_MaxHP) + 1 , health_bar.y + 1, (glad_width + 2)/hero_MaxHP, 5)
            hero_health_bar.append(OneHP)
       
    #Stick HPs to Health Bar
    for i in range(len(hero_health_bar)):
        hero_health_bar[i].x = health_bar.x + (i*(glad_width + 2)/hero_MaxHP) + 1 
        hero_health_bar[i].y = health_bar.y + 1

    for i in range(len(opponent)):
        opponent[i].health()

def main():
    #Define objects
    global basetime
    global cooldown
    opponent = []
    hero = pygame.Rect(LT[0]+50, (LB[1]-LT[1])/2, glad_width, glad_height)
    swordR = pygame.Rect(hero.x + glad_width, hero.y, attack_range, glad_height)
    swordL = pygame.Rect(hero.x - attack_range, hero.y, attack_range, glad_height)
    health_bar = pygame.Rect(hero.x, hero.y - 10, glad_width + 2, 7)
    hero_health_bar = []
    hero_current_HP = hero_MaxHP
    preparation = False
    round_num = 0

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and preparation == False:
                    if time.time() - cooldown > 1:
                        hero_hit(opponent, hero, swordR, swordL)

            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and round_num == 0:
                    pygame.event.post(pygame.event.Event(round_prepare))
            
            
            if event.type == hero_get_hit:
                hero_current_HP -= 1
                for OneHP in hero_health_bar:
                    if len(hero_health_bar) != hero_current_HP:
                        hero_health_bar.remove(OneHP)
                        #print("Remove HP", len(hero_health_bar))
                        roblox_sound.play()
                        health(hero, hero_health_bar, health_bar, hero_current_HP, opponent)
                        draw_window(hero, hero_health_bar, health_bar, opponent, round_num, preparation)
        
            if event.type == round_prepare:
                round_num += 1
                if round_num % 2 == 0:
                    for i in range(int(round_num/2)):
                        if i % 2 != 0:
                            enemy_model = pygame.Rect(Gate[0], Gate[1], enemy_width, enemy_height)
                            opponent.append(enemy_model)
                            opponent [i] = enemy(enemy_model.x, enemy_model.y, enemy_width, enemy_height) 
                        if i % 2 == 0:
                            enemy_model = pygame.Rect(Gate[0], Gate[1], enemy_width, enemy_height)
                            opponent.append(enemy_model)
                            opponent [i] = enemy(enemy_model.x, enemy_model.y, enemy_width, enemy_height)
                else:       
                    for i in range(int((round_num+1)/2)):
                        if i % 2 != 0:
                            enemy_model = pygame.Rect(Gate[0], Gate[1], enemy_width, enemy_height)
                            opponent.append(enemy_model)
                            opponent [i] = enemy(enemy_model.x, enemy_model.y, enemy_width, enemy_height) 
                        if i % 2 == 0:
                            enemy_model = pygame.Rect(Gate[0], Gate[1], enemy_width, enemy_height)
                            opponent.append(enemy_model)
                            opponent [i] = enemy(enemy_model.x, enemy_model.y, enemy_width, enemy_height)
                preparation = True
        
            if event.type == round_start:
                for i in range(len(opponent)):
                    opponent[i].chase(hero, opponent[i])

        if hero_current_HP == 0:
            looser_text = "You lost, bitch!"
            draw_looser(looser_text)
            break                 

        if preparation == True:
            ready = 0
            for i in range(len(opponent)):
                if opponent[i].posx != opponent[i].startposx or opponent[i].posy != opponent[i].startposy:
                    opponent[i].move(opponent[i])
                elif opponent[i].posx == opponent[i].startposx and opponent[i].posy == opponent[i].startposy:
                    ready += 1

                if ready == len(opponent):
                    print("Ready")
                    preparation = False
        else:  
            pygame.event.post(pygame.event.Event(round_start))
            enemy_hit(opponent, hero)        

        check_start(preparation, opponent)
        character_movement(hero, swordR, swordL)
        health(hero, hero_health_bar, health_bar, hero_current_HP, opponent)
        draw_window(hero, hero_health_bar, health_bar, opponent, round_num, preparation)


main()
        