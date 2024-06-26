import pygame
from constants import Consts
import threading
import sys

from map import Map
from state import State

class Display:

    display_thread: threading.Thread

    def __init__(self, map_object: Map):
        w, h = map_object.w, map_object.h
        self.map_array = map_object.map
        self.w = w
        self.h = h
        self.points = map_object.points
        self.marks = []

        pygame.init()
        sw, sh = Consts.SCREEN_WIDTH, Consts.SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((sw, sh))
        self.screen.fill(Consts.BACKGROUND)

        if w / h > sw / sh:
            rect_width = sw - 2 * Consts.SCREEN_MARGIN_SIZE
            cell_size = int(rect_width / w)
            rect_height = cell_size * h
        else:
            rect_height = sh - 2 * Consts.SCREEN_MARGIN_SIZE
            cell_size = int(rect_height / h)
            rect_width = cell_size * w
        self.cell_size = cell_size
        self.rect_width = rect_width
        self.rect_height = rect_height

        self.display_thread = None

        self.item_image = pygame.image.load(Consts.ITEM_IMAGE)
        self.item_image = pygame.transform.scale(self.item_image, (cell_size, cell_size))
        self.robot_image = pygame.image.load(Consts.ROBOT_IMAGE)
        self.robot_image = pygame.transform.scale(self.robot_image, (cell_size, cell_size))
        self.x_image = pygame.image.load(Consts.X_IMAGE)
        self.x_image = pygame.transform.scale(self.x_image, (cell_size, cell_size))
        self.mark_image = pygame.image.load(Consts.MARK_IMAGE)
        self.mark_image = pygame.transform.scale(self.mark_image, (cell_size, cell_size))

        self.draw_cells()
        pygame.display.update()

    def update(self, state: State, save=False):

        self.draw_cells()
        robot_y, robot_x = state.robot
        self.draw_in_position(robot_y, robot_x, self.robot_image)
        for item in state.items:
            self.draw_in_position(item[0], item[1], self.item_image)
        for mark in self.marks:
            self.draw_in_position(mark[0], mark[1], self.mark_image)
        pygame.display.update()

    def draw_cells(self):

        sw, sh = Consts.SCREEN_WIDTH, Consts.SCREEN_HEIGHT
        w, h = self.w, self.h
        rect_width, rect_height = self.rect_width, self.rect_height
        cell_size = self.cell_size

        init_y = (sh - rect_height) / 2
        init_x = (sw - rect_width) / 2
        for j in range(h):
            for i in range(w):
                x = init_x + i * cell_size
                y = init_y + j * cell_size
                if self.map_array[j][i] == 'x':
                    color = Consts.BLOCK_COLOR
                    self.draw_in_position(j, i, self.x_image)
                else:
                    color = Display.darker(Consts.CELL_COLOR, int(self.map_array[j][i]))

                pygame.draw.rect(self.screen, color, (x, y, cell_size, cell_size), 0)
                pygame.draw.rect(self.screen, (0, 0, 0), (x, y, cell_size, cell_size), 1)

        for p in self.points:
            self.draw_in_position(p[0], p[1], self.x_image)

    def draw_in_position(self, y: int, x: int, image):

        init_y = (Consts.SCREEN_HEIGHT - self.rect_height) / 2
        init_x = (Consts.SCREEN_WIDTH - self.rect_width) / 2
        pos_x = init_x + x * self.cell_size
        pos_y = init_y + y * self.cell_size
        self.screen.blit(image, (pos_x, pos_y))

    def begin_display(self):

        def infinite_loop():

            while True:
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        sys.exit(0)

                pygame.display.update()
                pygame.time.wait(int(1000/Consts.FPS))

        self.display_thread = threading.Thread(name='Display', target=infinite_loop)
        self.display_thread.setDaemon(False)
        self.display_thread.start()

    @staticmethod
    def darker(color: tuple[int, int, int], radius: int):

        r = color[0] - (radius - 1) * 30
        g = color[1] - (radius - 1) * 30
        b = color[2] - (radius - 1) * 30
        r = 0 if r < 0 else r
        g = 0 if g < 0 else g
        b = 0 if b < 0 else b
        return r, g, b
