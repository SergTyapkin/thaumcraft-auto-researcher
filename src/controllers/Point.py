import logging
from dataclasses import dataclass

import keyboard
import mouse

from src.utils.utils import eventsDelay


@dataclass(frozen=True)
class P:
    x: float
    y: float

    def move(self):
        mousePos = mouse.get_position()
        if mousePos[0] != self.x or mousePos[1] != self.y:
            logging.debug(f"Move mouse to point {self}")
            mouse.move(self.x, self.y)
            eventsDelay()
        else:
            logging.debug(f"Move mouse to point {self} - mouse already in this pos")

    def click(self, button=mouse.LEFT, shift=False):
        self.move()
        if not shift:
            logging.debug(f"Click mouse on point {self}")
            mouse.click(button)
            return
        keyboard.press('shift')
        eventsDelay()
        logging.debug(f"Click on point {self} with shift")
        mouse.click(button)
        eventsDelay()
        keyboard.release('shift')

    def hold(self, button=mouse.LEFT):
        self.move()
        logging.debug(f"Hold mouse on point {self}")
        mouse.press(button)

    def release(self, button=mouse.LEFT):
        self.move()
        logging.debug(f"Release mouse on point {self}")
        mouse.release(button)
