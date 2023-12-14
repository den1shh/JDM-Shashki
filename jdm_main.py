import random
import pygame
import yaml
import pandas as pd
from modules.jdm_world import World
from modules.jdm_objects import Item, MyCar

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
            print('Game over')
            sound.play()
            world.game_status = False

def get_coin(my_car, world):
    for coin in world.coins:
        if coin.rect.colliderect(my_car.rect):
            world.point += 1
            coin.kill()

def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((800, 800))
    background_color = (0, 0, 0)
    pygame.display.set_caption('Traffic racer')
    sound = pygame.mixer.Sound('sounds/engine.wav')
    sound.play(-1)
    font = pygame.freetype.Font(None, 20)

    spawn_road_time = pygame.USEREVENT
    pygame.time.set_timer(spawn_road_time, 800)
    spawn_traffic_time = pygame.USEREVENT + 1
    pygame.time.set_timer(spawn_traffic_time, 1000)
    spawn_coin_time = pygame.USEREVENT + 2
    pygame.time.set_timer(spawn_coin_time, 1000)

    cars = load_cars()
    my_car = MyCar((300, 600), cars['supra']['image'])

    road_image = pygame.image.load('img/racetrack.jpg')
    road_image = pygame.transform.scale(road_image, (800, 800))
    
    coin_image = pygame.image.load('img/coin.png')
    coin_image = pygame.transform.scale(coin_image, (80, 80))
    
    
    world = World(my_car = my_car, roads = [Item(road_image, (400, 400), 15), Item(road_image, (400, -400), 15), Item(road_image, (400, -1200), 15)])
    
    while world.alive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                world.alive = False
            if event.type == spawn_road_time:
                world.spawn_road(road_image)
            if event.type == spawn_traffic_time:
                world.spawn_traffic(cars)
            if event.type == spawn_coin_time:
                world.spawn_coin(coin_image)

        screen.fill(background_color)
        if world.game_status:
            my_car.move()
            world.draw_all(screen, my_car)
            world.acceleration(pygame.time.get_ticks()/1000)
            font.render_to(screen, (800, 30), str(world.time), (255, 255, 255))
            crash(my_car, world.traffic_cars, world)
            get_coin(my_car, world)
        else:
            font.render_to(screen, (30, 300), 'Game Over', (255, 255, 255))
            font.render_to(screen, (30, 330), 'Your time: ' + str(world.time), (255, 255, 255))
            font.render_to(screen, (30, 360), 'Your score: ' + str(world.point), (255, 255, 255))
            sound.stop()
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()

