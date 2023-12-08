import random
import pygame
import pygame.freetype
from my_car import MyCar
from road import Road
from traffic import TrafficCar

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((800, 800)) #полоса ко всему файлу 10:48
pygame.display.set_caption('JDM шашки')
background_color = (0, 0, 0)

my_car_sound = pygame.mixer.Sound('traffic/sounds/engine.wav')
my_car_sound.play(-1)

crash_sound = pygame.mixer.Sound('traffic/sounds/crash.wav')

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


road_image = pygame.image.load('traffic/images/racetrack.jpg')
road_image = pygame.transform.scale(road_image, (800, 800))

traffic_car_images = []
traffic_car1 = get_car_image('traffic/images/traffic_car1.png', (211, 90), 90)
traffic_car2 = get_car_image('traffic/images/traffic_car2.png', (211, 90), -90)
traffic_car3 = get_car_image('traffic/images/traffic_car3.png', (211, 90), -90)
traffic_car_images.extend((traffic_car1, traffic_car2, traffic_car3))

road = Road(road_image, (400, 400))
road_group.add(road)
road = Road(road_image, (400, 0))
road_group.add(road)


def spawn_road():
    road_bg = Road(road_image, (400, -600))
    road_group.add(road_bg)


def spawn_traffic():
    position = (random.randint(64, 460), random.randint(-96, -40))
    speed = random.randint(12, 20)
    traffic_car = TrafficCar(random.choice(traffic_car_images), position, speed)
    traffic_cars_group.add(traffic_car)


def draw_all():
    road_group.update()
    road_group.draw(screen)
    traffic_cars_group.update()
    traffic_cars_group.draw(screen)
    my_car.draw(screen)

def draw_start_menu(menu):
    """стартовое меню"""
    menu_image = pygame.transform.scale(menu, (800, 800))
    screen.blit(menu_image, (0, 0))
    pygame.display.update()



running = True
menu1 = pygame.image.load('traffic/images/menubackground.png')
menu2 = pygame.image.load('traffic/images/menuback2.png')
game_state = "choose_car"
supra_image = get_car_image('traffic/images/supra.png', (90, 211), 0)
supra = MyCar((500, 600), supra_image)
civic_image = get_car_image('traffic/images/civic.png', (90, 197), 0)
civic = MyCar((500, 600), civic_image)
r34_image = get_car_image('traffic/images/r34.png', (90, 217), 0)
r34 = MyCar((500, 600), r34_image)


    

while running:


    for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == spawn_road_time:
                        spawn_road()
                if event.type == spawn_traffic_time:
                        spawn_traffic()
    
    #todo машинки спавнятся когда сидишь в меню - исправить!
                
    if game_state == "choose_car":
        keys = pygame.key.get_pressed()
        draw_start_menu(menu1)
        if keys[pygame.K_1]:
            game_state = 'choose_track'
            my_car = supra
        if keys[pygame.K_2]:
            game_state = 'choose_track'
            my_car = civic
        if keys[pygame.K_3]:
            game_state = 'choose_track'
            my_car = r34
    if game_state == 'choose_track':
        keys2 = pygame.key.get_pressed()
        draw_start_menu(menu2)
        if keys2[pygame.K_1]:
            game_state = 'game_start'
            # my_car = supra

    if game_state == "game_start":
        
    

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
