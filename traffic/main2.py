import random
import pygame
import pygame.freetype
from my_car import MyCar
from road import Road
from traffic import TrafficCar

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((500, 800))
pygame.display.set_caption('Traffic racer')
background_color = (0, 0, 0)

my_car_sound = pygame.mixer.Sound('sounds/engine.wav')
my_car_sound.play(-1)

crash_sound = pygame.mixer.Sound('sounds/crash.wav')

font = pygame.freetype.Font(None, 20)

road_group = pygame.sprite.Group()
spawn_road_time = pygame.USEREVENT
pygame.time.set_timer(spawn_road_time, 1000)

traffic_cars_group = pygame.sprite.Group()
spawn_traffic_time = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_traffic_time, 1000)


def get_car_image(filename, size, angle):
    image = pygame.image.load(filename)
    image = pygame.transform.scale(image, size)
    image = pygame.transform.rotate(image, angle)
    return image


my_car_image = get_car_image('images/mercedes.png', (100, 70), -90)
road_image = pygame.image.load('images/road.png')
road_image = pygame.transform.scale(road_image, (500, 800))

traffic_car_images = []
traffic_car1 = get_car_image('images/traffic_car1.png', (100, 70), 90)
traffic_car2 = get_car_image('images/traffic_car2.png', (100, 70), -90)
traffic_car3 = get_car_image('images/traffic_car3.png', (100, 70), -90)
traffic_car_images.extend((traffic_car1, traffic_car2, traffic_car3))

road = Road(road_image, (250, 400))
road_group.add(road)
road = Road(road_image, (250, 0))
road_group.add(road)


def spawn_road():
    road_bg = Road(road_image, (250, -600))
    road_group.add(road_bg)


def spawn_traffic():
    position = (random.randint(40, 460), random.randint(-60, -40))
    speed = random.randint(7, 20)
    traffic_car = TrafficCar(random.choice(traffic_car_images), position, speed)
    traffic_cars_group.add(traffic_car)


def draw_all():
    road_group.update()
    road_group.draw(screen)
    traffic_cars_group.update()
    traffic_cars_group.draw(screen)
    my_car.draw(screen)


my_car = MyCar((300, 600), my_car_image)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == spawn_road_time:
            spawn_road()
        if event.type == spawn_traffic_time:
            spawn_traffic()

    screen.fill(background_color)
    if my_car.game_status == 'game':
        my_car.move()
        draw_all()
        my_car.crash(crash_sound, traffic_cars_group)
    elif my_car.game_status == 'game_over':
        font.render_to(screen, (30, 300), 'Game Over', (255, 255, 255))
        my_car_sound.stop()

    pygame.display.flip()
    clock.tick(60)
