import neat.config
import neat.genome
import neat.population

import settings
import neat
import pygame

from bird import Bird
from game import Game
from pipe import Pipes


class NeatBird(Bird):

    def __init__(self, x: float, y: float, genome: neat.genome.DefaultGenome, net: neat.nn.FeedForwardNetwork):
        self._genome = genome
        self._net = net
        super().__init__(x, y)

    def think(self, activation_tuple: tuple[float, float, float]):
        if not self.check_alive():
            return

        self._genome.fitness += 1

        output: float = self._net.activate(activation_tuple)[0]

        if output > settings.NEAT_THRESHOLD:
            self.jump()


class NeatGame(Game):
    _generation: int = 0

    def __init__(self, *, headless: bool):
        # start normal game operation
        super().__init__(headless=headless)

    def _gen_birds(self) -> list[Bird]:
        return [NeatBird(
            settings.SCREEN_SIZE.x / 2 - settings.BIRD_SIZE.x / 2,
            settings.SCREEN_SIZE.y / 2,
            genome,
            net
        ) for genome, net in zip(self._genomes, self._nets)]

    def _input(self) -> None:
        # poll for events
        for event in pygame.event.get():
            # exit game when exit is clicked
            if event.type == pygame.QUIT:
                self.close()

        # take user keyboard input
        keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            self.close()

        # skip to next generation n
        if keys[pygame.K_n]:
            self._running = False

        if keys[pygame.K_SPACE]:
            for bird in self._birds:
                # Allows the bird to jump up
                bird.jump()

        # find nearest pipe to the birds
        nearest_pipe: Pipes = min(self._pipes,
                                  key=lambda pipe: abs(pipe.x - self._birds[0].x))

        # Create the input based on nearest pipe information
        horizontal_difference: float = abs(nearest_pipe.x - self._birds[0].x)
        for bird in self._birds:
            bottom_pipe_difference: float = nearest_pipe.bottom_pipe.y - bird.y
            top_pipe_difference: float = nearest_pipe.top_pipe.y + \
                nearest_pipe.top_pipe.height - bird.y

            # Allows the bird to jump up
            bird.think(
                (horizontal_difference, bottom_pipe_difference, top_pipe_difference)
            )

    def _display_text(self) -> None:
        self._screen.blit(self._font.render(
            f"FPS: {round(self._clock.get_fps(), 1)}", True, (255, 255, 255)), (30, 10))
        self._screen.blit(self._font.render(
            f"Birds: {self._birds_alive}", True, (255, 255, 255)), (30, 45))
        self._screen.blit(self._font.render(
            f"Gen: {self._generation}", True, (255, 255, 255)), (30, 80))
        self._screen.blit(self._font.render(
            f"Fit: {max(bird._genome.fitness for bird in self._birds)}", True, (255, 255, 255)), (30, 115))

    def run(self, genomes: tuple[str, neat.genome.DefaultGenome], config: neat.config.Config) -> None:
        NeatGame._generation += 1
        self._genomes: list[neat.genome.DefaultGenome] = []
        self._nets: list[neat.nn.FeedForwardNetwork] = []

        # split genomes into their respective lists
        for genome_id, genome in genomes:
            genome.fitness = 0
            self._genomes.append(genome)

            net: neat.nn.FeedForwardNetwork = neat.nn.FeedForwardNetwork.create(
                genome, config)
            self._nets.append(net)

        super().run()


if __name__ == "__main__":
    from pathlib import Path

    config_path: Path = Path(
        "/home/karsten/Coding/Python/Flappy Bird/src/neat-config.txt")

    config: neat.config.Config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    population: neat.Population = neat.Population(config)

    with NeatGame(headless=False) as game:
        population.run(game.run, 10)
