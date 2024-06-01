from typing import List
import pygame

import settings

from bird import Bird
from game import Game


class UserGame(Game):

    def __init__(self):
        super().__init__(headless=False)

    def _gen_birds(self) -> List[Bird]:
        return [Bird(
            settings.SCREEN_SIZE.x / 2 - settings.BIRD_SIZE.x / 2,
            settings.SCREEN_SIZE.y / 4 + settings.SCREEN_SIZE.y / 2 / 100 * offset
        ) for offset in range(100)]

    def _input(self) -> None:
        # poll for events
        for event in pygame.event.get():
            # exit game when exit is clicked
            if event.type == pygame.QUIT:
                self._running = False

        # take user keyboard input
        keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self._running = False

        if keys[pygame.K_SPACE]:
            for bird in self._birds:
                # Allows the bird to jump up
                bird.jump()

    def _display_text(self) -> None:
        self._screen.blit(self._font.render(
            f"FPS: {round(self._clock.get_fps(), 1)}", True, (255, 255, 255)), (30, 10))
        self._screen.blit(self._font.render(
            f"Birds: {self._birds_alive}", True, (255, 255, 255)), (30, 45))


if __name__ == "__main__":
    with UserGame() as game:
        game.run()
