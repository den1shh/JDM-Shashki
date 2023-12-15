import random
import pygame, sys
import yaml
import pandas as pd
from pygame.locals import *
from pygame import mixer
from modules.jdm_world import World
from modules.jdm_objects import Item, MyCar
from modules.jdm_button import Button
from pygame import mixer

def load_cars():
    with open("configs/cars.yaml", "r") as file:
        confs = yaml.safe_load(file)
        cars = dict()
        for conf in confs:
            cars[conf['type']] = conf
        for car in cars.values():
            car['image'] = pygame.image.load('img/' + car['image'])
            car['image'] = pygame.transform.scale(car['image'], (car['width'], car['length']))
        return cars        
    
def crash(my_car, traffic_cars, world):
    sound = pygame.mixer.Sound('sounds/crash.wav')
    for car in traffic_cars:
        if car.rect.colliderect(my_car.rect):
            sound.play()
            world.game_status = False

def paused(world):
    '''поведение игры при паузе'''
    pause = True
    while pause:
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        CONTINUE_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("img/continue.png"), (500, 67)), pos=(400, 350), 
            text_input=" ", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        QUIT_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("img/quit.png"), (172, 44)), pos=(676, 764), 
            text_input=" ", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON.update(SCREEN)
        CONTINUE_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if CONTINUE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pause = False
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        world.time_sync(pygame.time.get_ticks())        
        
        pygame.display.update()

def game_finish_screen(time, score, screen):
        '''экран конца игры'''
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        font = pygame.font.Font(None, 50)
        timetxt = font.render(str(time/1000), True, (0, 0, 0), (255, 255, 255))
        scoretxt = font.render(str(score), True, (0, 0, 0), (255, 255, 255))
        timeRect = timetxt.get_rect()
        timeRect.center = (234, 296)
        scoreRect = scoretxt.get_rect()
        scoreRect.center = (551, 296)
        
        SCREEN.blit(BG3, (0, 0))
        screen.blit(timetxt, timeRect)
        screen.blit(scoretxt, scoreRect)
        RESTART_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("img/restart.png"), (468, 70)), pos=(400, 700), 
            text_input=" ", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        RESTART_BUTTON.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if RESTART_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main_menu()

def get_coin(my_car, world):
    for coin in world.coins:
        if coin.rect.colliderect(my_car.rect):
            world.point += 1
            coin.kill()

def play(choosed_car, choosed_track):
    '''основное состояние игры - гонка'''
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((800, 800))
    background_color = (0, 0, 0)
    pygame.display.set_caption('JDM shashki')
    sound = pygame.mixer.Sound('sounds/engine.wav')
    
    sound.play(-1)
    font = pygame.freetype.Font(None, 20)

    spawn_road_time = pygame.USEREVENT
    pygame.time.set_timer(spawn_road_time, 444)
    spawn_traffic_time = pygame.USEREVENT + 1
    pygame.time.set_timer(spawn_traffic_time, 1000)
    spawn_coin_time = pygame.USEREVENT + 2
    pygame.time.set_timer(spawn_coin_time, 1000)
    update_road_time = pygame.USEREVENT + 3
    pygame.time.set_timer(update_road_time, 5000)

    cars = load_cars()
    my_car = MyCar((300, 600), cars[str(choosed_car)]['image'])

    road_image = pygame.transform.scale(pygame.image.load('img/' + str(choosed_track) + '.jpg')
, (800, 800))
    
    coin_image = pygame.transform.scale(pygame.image.load('img/coin.png')
, (80, 80))
    
    
    world = World(roads = [Item(road_image, (400, 400), 15), Item(road_image, (400, -400), 15), Item(road_image, (400, -1200), 15)], time = pygame.time.get_ticks(), choosed_track = choosed_track)
    
    while world.alive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sound.stop()
                world.alive = False
            if event.type == spawn_road_time:
                world.spawn_road(road_image)
            if event.type == spawn_traffic_time:
                world.spawn_traffic(cars)
            if event.type == spawn_coin_time:
                world.spawn_coin(coin_image)
            if event.type == update_road_time:
                world.update_road(spawn_road_time)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sound.set_volume(0)
                    paused(world)
                else:
                    sound.set_volume(1)

        screen.fill(background_color)
        if world.game_status:
            my_car.move()
            world.draw_all(screen, my_car)
            world.acceleration(pygame.time.get_ticks())
            font.render_to(screen, (800, 30), str(world.time), (255, 255, 255))
            crash(my_car, world.traffic_cars, world)
            get_coin(my_car, world)
        else:
            game_finish_screen(world.game_time, world.point, screen)
            
            # font.render_to(screen, (30, 300), 'Game Over', (255, 255, 255))
            # font.render_to(screen, (30, 330), 'Your time: ' + str(world.time), (255, 255, 255))
            # font.render_to(screen, (30, 360), 'Your score: ' + str(world.point), (255, 255, 255))
            sound.stop()
        
        pygame.display.flip()
        clock.tick(60)


def get_font(size): # Returns Press-Start-2P in the desired size
    '''для шрифта'''
    return pygame.font.Font("img/font.ttf", size)


def options():
    '''вызов меню настроек. в работе'''
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")
        QUIT_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("img/quit.png"), (172, 44)), pos=(676, 764), 
                            text_input=" ", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        
        QUIT_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if QUIT_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def track_menu(choosed_car):
    '''вызывает меню выбора трассы'''
    while True:
        SCREEN.blit(BG2, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()


        TRACK1_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("img/racetrack.jpg"), (300, 300)), pos=(217, 400), 
                            text_input=" ", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        TRACK2_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("img/racetrack2.jpg"), (300, 300)), pos=(583, 400), 
                            text_input=" ", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        PREVIOUS_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("img/previous.png"), (518, 50)), pos=(297, 760), 
                            text_input=" ", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        QUIT_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("img/quit.png"), (172, 44)), pos=(676, 764), 
                            text_input=" ", font=get_font(75), base_color="#d7fcd4", hovering_color="White")


        for button in [TRACK1_BUTTON, TRACK2_BUTTON, PREVIOUS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if TRACK1_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play(choosed_car, 'racetrack')
                if TRACK2_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play(choosed_car, 'racetrack2')
                if PREVIOUS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main_menu()             
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def main_menu():
    '''вызывает начальное меню'''
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render(" ", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))
        SUPRA_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("img/tsboku.png"), (236, 118)), pos=(145, 675), 
                            text_input=" ", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        CIVIC_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("img/csboku.png"), (236, 126)), pos=(400, 675), 
                            text_input=" ", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        R34_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("img/rsboku.png"), (236, 122)), pos=(659, 675), 
                            text_input=" ", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        OPTIONS_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("img/options.png"), (267, 50)), pos=(400, 760), 
                            text_input=" ", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("img/quit.png"), (172, 44)), pos=(676, 764), 
                            text_input=" ", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [SUPRA_BUTTON, CIVIC_BUTTON, R34_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if SUPRA_BUTTON.checkForInput(MENU_MOUSE_POS):
                    track_menu('supra')
                if CIVIC_BUTTON.checkForInput(MENU_MOUSE_POS):
                    track_menu('civic')
                if R34_BUTTON.checkForInput(MENU_MOUSE_POS):
                    track_menu('r34')
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
pygame.init()



SCREEN = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Menu")



BG = pygame.transform.scale(pygame.image.load("img/backformenu.png"), (800, 800))
BG2 = pygame.transform.scale(pygame.image.load("img/backformenu2.png"), (800, 800))
BG3 = pygame.transform.scale(pygame.image.load("img/backformenu3.png"), (800, 800))
mixer.init()
mixer.music.load('sounds/DVRST - Close Eyes.mp3')
mixer.music.play(-1)

if __name__ == "__main__":
    main_menu()

