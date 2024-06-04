import abc
import pygame

import settings

from entity import Entity
from bird import Bird
from pipe import Pipes
from base import Base


class Game(abc.ABC):
    # background image
    _BACKGROUND_IMG: pygame.image = pygame.transform.scale(pygame.image.load(
        settings.ASSETS_PATH / "background-day.png"), settings.SCREEN_SIZE)

    def __init__(self, *, headless: bool):
        # Logic for the game loop
        self._running: bool = True
        self._dt: float = 1 / settings.FRAME_RATE
        self._headless: bool = headless

    def __gen_game_objects(self) -> None:
        # Create game objects
        self._birds: list[Bird] = self._gen_birds()

        self._pipes: list[Pipes] = [
            Pipes(settings.PIPE_INITIAL_X), Pipes(settings.PIPE_INITIAL_X * 2)]
        self._bases: list[Base] = [Base(x) for x in range(-10, 336 * 4, 336)]

    @property
    def birds_alive(self) -> int:
        return sum(1 for bird in self._birds if bird.is_alive)

    @abc.abstractmethod
    def _gen_birds(self) -> list[Bird]:
        pass

    @abc.abstractmethod
    def _input(self) -> None:
        pass

    def __init_graphics(self) -> None:
        pygame.init()
        pygame.display.set_caption("Flappy Bird")

        self._screen: pygame.Surface = pygame.display.set_mode(
            settings.SCREEN_SIZE)
        self._clock: pygame.time.Clock = pygame.time.Clock()
        self._font = pygame.font.Font("freesansbold.ttf", 32)

        self._dt = 0

    @abc.abstractmethod
    def _display_text(self) -> None:
        pass

    def __get_entities(self) -> list[Entity]:
        return [*self._pipes, *self._bases, *self._birds]

    def run(self) -> None:
        # Create all the objects required for the game
        self.__gen_game_objects()
        self._running = True

        while self._running:
            if not self._headless:
                # fill the screen with a color to wipe away anything from last frame
                pygame.Surface.blit(
                    self._screen, Game._BACKGROUND_IMG, (0, 0))

            # Checks to see if the birds still exist
            if self.birds_alive == 0:
                self._running = False

            # Update all entity positions and draw them
            for entity in self.__get_entities():
                entity.update(self._dt)

                if not self._headless:
                    entity.draw(self._screen)

            # Loop pipes back to the beginning
            for pipe in self._pipes:
                if pipe.x + pipe.width <= 0:
                    self._pipes.remove(pipe)
                    self._pipes.append(
                        Pipes(settings.PIPE_INITIAL_X * (len(self._pipes) + 1)))

            for object in [*self._bases, *self._pipes]:
                for bird in self._birds:
                    if bird.is_alive and object.collides(bird):
                        bird.kill()

            # Draw things to the screen
            if not self._headless:
                self._display_text()

                # flip() the display to put your work on screen
                pygame.display.flip()

                # limits FPS to 60, dt is delta time in seconds since last frame, used for framerate
                self._dt = self._clock.tick(settings.FRAME_RATE) / 1000

            # Control all user input functionality
            self._input()

    def __enter__(self) -> None:
        # Start the graphics if necessary
        if not self._headless:
            self.__init_graphics()

        return self

    def start(self) -> None:
        # Start the graphics if necessary
        if not self._headless:
            self.__init_graphics()

        self.run()

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()

    def close(self) -> None:
        self._running = False

        if not self._headless:
            pygame.quit()
