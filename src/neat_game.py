from typing import List
import neat.config
import pygame
import neat

import settings

from bird import Bird
from game import Game


class BirdWrapper(Bird):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self._fitness: float = 0.0
        self._ge = None
        self._net = None

    def update(self, delta: float) -> None:
        super().update(delta)

        if self.is_alive():
            self._fitness += delta

    @property
    def fitness(self) -> float:
        return self._fitness


class NeatGame(Game):
    def __init__(self, *, headless: bool = False, config: neat.config.Config):
        # Save config and create perform normal game start operations
        self._config: neat.config.Config = config
        super().__init__(headless=headless)

        # Create core evolution algorithm class
        self._population: neat.Population = neat.Population(config)

        # Add reporter for fancy statistical result
        self._population.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        self._population.add_reporter(stats)

        # Run the AI
        # self._population.run(self._eval_genomes(), 50)

    def _gen_birds(self) -> List[Bird]:
        return [BirdWrapper(settings.SCREEN_SIZE.x / 2, settings.SCREEN_SIZE.y / 2)]

    # def _eval_genomes(self, genomes, config):

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
            f"Birds: {len(self._birds)}", True, (255, 255, 255)), (30, 45))


if __name__ == "__main__":
    from pathlib import Path
    config_path: Path = Path("src/neat-config.txt")

    # config_path: str = "src/neat-config.txt"

    config: neat.config.Config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    game: NeatGame = NeatGame(headless=False, config=config)
    game.start()
