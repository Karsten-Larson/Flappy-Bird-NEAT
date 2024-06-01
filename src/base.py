
import pygame
import settings
from entity import Entity


class Base(Entity):
    _IMG: pygame.Surface = pygame.image.load(settings.ASSETS_PATH / "base.png")

    def __init__(self, x: float):
        super().__init__(x, settings.SCREEN_SIZE.y - settings.BASE_SIZE.y / 2,
                         settings.BASE_SIZE.x, settings.BASE_SIZE.y)
        self._velocity = settings.BASE_VELOCITY

    def update(self, delta: float) -> None:
        super().update(delta)

        if self._position.x + self._size.x <= 0:
            self._position.x += settings.SCREEN_SIZE.x + self._size.x

    def draw(self, display: pygame.Surface):
        display.blit(Base._IMG, self._position)
