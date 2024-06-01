from enum import Enum

import pygame
import random
import settings

from entity import Entity


class PipeOrientation(Enum):
    UP = 1
    DOWN = 2


class Pipe(Entity):
    _NORMAL_IMG: pygame.Surface = pygame.image.load(
        settings.ASSETS_PATH / "pipe-green.png")
    _REVERSE_IMG: pygame.Surface = pygame.transform.flip(
        _NORMAL_IMG, False, True)

    def __init__(self, x: float, y: float, orientation: PipeOrientation):
        super().__init__(x, y, settings.PIPE_SIZE.x, settings.PIPE_SIZE.y)
        self._velocity = settings.PIPE_VELOCITY.copy()
        self._orientation: PipeOrientation = orientation

    def draw(self, display: pygame.Surface):
        display.blit(
            Pipe._NORMAL_IMG if self._orientation == PipeOrientation.UP else Pipe._REVERSE_IMG,
            self._position
        )
        # pygame.draw.rect(display, (255, 0, 0), self.rect)


class Pipes(Entity):
    _pipe_offset: float = 320.0

    def __init__(self, x: float):
        start_y: float = -random.choice(settings.PIPE_HEIGHTS)

        self._top_pipe = Pipe(x, start_y, PipeOrientation.DOWN)
        self._bottom_pipe = Pipe(
            x, start_y + self._pipe_offset + settings.PIPE_GAP, PipeOrientation.UP)
        self.velocity = settings.PIPE_VELOCITY.copy()

    @property
    def velocity(self) -> pygame.Vector2:
        return self._top_pipe.velocity.copy()

    @velocity.setter
    def velocity(self, velocity: pygame.Vector2) -> None:
        self._top_pipe.velocity = velocity
        self._bottom_pipe.velocity = velocity

    @property
    def x(self) -> float:
        return self._top_pipe.x

    @x.setter
    def x(self, x: float) -> None:
        self._top_pipe.x = x
        self._bottom_pipe.x = x

    @property
    def y(self) -> float:
        return self._top_pipe.y

    @y.setter
    def y(self, y) -> None:
        self._top_pipe.y = y
        self._bottom_pipe.y = y + self._pipe_offset

    @property
    def top_pipe(self) -> Pipe:
        return self._top_pipe

    @property
    def bottom_pipe(self) -> Pipe:
        return self._bottom_pipe

    def update(self, delta: float) -> None:
        self._top_pipe.update(delta)
        self._bottom_pipe.update(delta)

    def collides(self, other: Entity) -> bool:
        return self._top_pipe.collides(other) or self._bottom_pipe.collides(other)

    def draw(self, display: pygame.Surface) -> None:
        self._top_pipe.draw(display)
        self._bottom_pipe.draw(display)

    def __getattr__(self, name: str) -> any:
        if hasattr(self._top_pipe, name):
            return getattr(self._top_pipe, name)

        raise AttributeError(
            f"{self.__class__.__name__} has no attribute {name}")
