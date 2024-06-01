from __future__ import annotations

from abc import ABC, abstractmethod

import pygame


class Entity(ABC):

    def __init__(self, x: float, y: float, width: float, height: float):
        self._position: pygame.Vector2 = pygame.Vector2(x, y)
        self._size: pygame.Vector2 = pygame.Vector2(width, height)

        # movement
        self._velocity: pygame.Vector2 = pygame.Vector2(0.0, 0.0)

    @property
    def x(self) -> float:
        return self._position.x

    @x.setter
    def x(self, x: float) -> None:
        assert isinstance(x, float)
        self._position = pygame.Vector2(x, self._position.y)

    @property
    def y(self) -> float:
        return self._position.y

    @y.setter
    def y(self, y: float) -> None:
        assert isinstance(y, float)
        self._position = pygame.Vector2(self._position.x, y)

    @property
    def position(self) -> pygame.Vector2:
        return self._position.copy()

    @position.setter
    def position(self, position: pygame.Vector2) -> None:
        assert isinstance(position, pygame.Vector2)
        self._position = position

    @property
    def width(self) -> float:
        return self._size.x

    @property
    def height(self) -> float:
        return self._size.y

    @property
    def size(self) -> pygame.Vector2:
        return self._size.copy()

    @property
    def velocity(self) -> pygame.Vector2:
        return self._velocity

    @velocity.setter
    def velocity(self, velocity: pygame.Vector2) -> None:
        assert isinstance(velocity, pygame.Vector2)
        self._velocity = velocity

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self._position, self._size)

    def collides(self, other: Entity) -> bool:
        assert isinstance(other, Entity), "other must be of type object Entity"
        return self.rect.colliderect(other.rect)

    def update(self, delta: float) -> None:
        self._position += self._velocity * delta

    @abstractmethod
    def draw(self, display: pygame.Surface) -> None:
        pass
