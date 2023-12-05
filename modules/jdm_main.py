import pygame as pg
import pygame_widgets
from solar_world import World
from solar_vis import calculate_scale_factor, Drawer, Menu
from solar_model import recalculate_space_objects_positions
from solar_input import read_space_objects_data_from_yaml, write_space_objects_data_to_yaml
from solar_stats import check_system, calculate_speed, calculate_distance, show_graph
import time
import numpy as np

def execution(menu: Menu, world: World) -> None:
    """Функция исполнения -- выполняется циклически, вызывая обработку координат машин,
    а также обновляя их положение на экране.
    Цикличность выполнения зависит от значения переменной perform_execution в объекте типа World.
    При perform_execution == True функция запрашивает вызов самой себя по таймеру через от 1 мс до 100 мс.
    """
    if world.perform_execution:
        recalculate_space_objects_positions(world.car_objects, delta)



def handle_events(events, world: World) -> None:
    """
    Обрабатывает действия пользователя и вызывает реакцию интерфейса и всей программы на них
    """
    for event in events:
        if event.type == pg.QUIT:
            world.alive = False
    pygame_widgets.update(events)


def main():
    """Главная функция главного модуля.
    Создаёт объекты графического дизайна библиотеки tkinter: окно, холст, фрейм с кнопками, кнопки.
    """

    pg.init()

    width = 900
    height = 750
    screen = pg.display.set_mode((width, height))
    world = World()

    drawer = Drawer(screen, menu)
    world.perform_execution = True

    while world.alive:
        check_game_state() #TODO функция, отвечающая за состояние игры из меню
        handle_events(pg.event.get(), world)
        time.sleep(1.0 / 60)



if __name__ == "__main__":
    main()
