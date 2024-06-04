import pygame
import math

import settings
from entity import Entity


class Bird(Entity):
    _BIRD_IMGS = [pygame.image.load(settings.ASSETS_PATH / filename) for filename in [
        'yellowbird-downflap.png', 'yellowbird-midflap.png', 'yellowbird-upflap.png']]
    _bird_counter: int = 0

    def __init__(self, x: float, y: float):
        super().__init__(x, y, settings.BIRD_SIZE.x, settings.BIRD_SIZE.y)
        self._rotation: float = 0.0
        self._velocity = settings.JUMP_VELOCITY.copy()

        # counter for frame animations
        self._frame_counter: float = 0.0
        self._jump_counter: float = 0.0

        # control bird's life
        self._alive: bool = True

        # index of bird
        self._index: int = Bird._bird_counter
        Bird._bird_counter += 1

    @property
    def rotation(self) -> float:
        return self._rotation

    @property
    def index(self) -> int:
        return self._index

    @property
    def is_alive(self) -> bool:
        return self._alive

    def kill(self) -> None:
        self._alive = False

    # Decorator method
    def check_alive(func):
        def wrapper(*args, **kwargs):
            if args[0]._alive:
                return func(*args, **kwargs)

        return wrapper

    def _gravity(self, delta: float) -> None:
        resulting_velocity: pygame.Vector2 = self._velocity + settings.GRAVITY * delta

        if resulting_velocity.y > settings.TERMINAL_VELOCITY.y:
            self._velocity = settings.TERMINAL_VELOCITY
            return

        self._velocity = resulting_velocity

    @check_alive
    def update(self, delta: float) -> None:
        """Updates the birds position and rotation based on velocity"""
        super().update(delta)

        # Applies gravity to the bird
        self._gravity(delta)

        # sets the rotation of the bird to a proportion of its y velcity clamped to a [-90, 90] range
        self._rotation = max(-90.0, min(-self._velocity.y / 3, 35.0))
        self._frame_counter += 5 * delta
        self._jump_counter += delta

    @check_alive
    def jump(self) -> None:
        if self._jump_counter < settings.JUMP_DELAY:
            return

        self._velocity = settings.JUMP_VELOCITY.copy()
        self._jump_counter = 0.0

    @check_alive
    def draw(self, display: pygame.Surface) -> None:
        # gets the correct bird flapping and rotates it according to its given rotation
        rotated_img: pygame.image = pygame.transform.rotate(Bird._BIRD_IMGS[math.floor(
            self._frame_counter % len(Bird._BIRD_IMGS))], self._rotation)

        # draw the bird image to the screen
        display.blit(rotated_img, self._position)
