import neat.config
import neat.genome
import neat.population

import settings
import neat
import pygame

from bird import Bird
from game import Game
from pipe import Pipes


class classproperty(property):
    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


class NeatBird(Bird):
    # static fitness threshold
    _fitness_threshold: int | None = None

    @classproperty
    def fitness_threshold(cls) -> int | None:
        return cls._fitness_threshold

    @fitness_threshold.setter
    def fitness_threshold(cls, val: int | None) -> int | None:
        cls._fitness_threshold = val

    def __init__(self, x: float, y: float, genome: neat.genome.DefaultGenome, net: neat.nn.FeedForwardNetwork):
        self._genome = genome
        self._net = net
        super().__init__(x, y)

    @Bird.check_alive
    def think(self, activation_tuple: tuple[float, float, float]) -> None:
        if NeatBird.fitness_threshold and int(NeatBird.fitness_threshold) < self._genome.fitness:
            self.kill()
            return

        self._genome.fitness += 1

        output: float = self._net.activate(activation_tuple)[0]

        if output > settings.NEAT_THRESHOLD:
            self.jump()


class NeatGame(Game):
    def __init__(self, *, headless: bool, config: neat.config.Config):
        # begin neat genome config
        self._config: neat.config.Config = config
        self._population: neat.Population = neat.Population(config)

        # start normal game operation
        super().__init__(headless=headless)

    def _gen_birds(self) -> list[Bird]:
        # set the maximum value birds can get to
        NeatBird.fitness_threshold = self._config.fitness_threshold

        return [NeatBird(
            settings.SCREEN_SIZE.x / 2 - settings.BIRD_SIZE.x / 2,
            settings.SCREEN_SIZE.y / 2,
            genome,
            net
        ) for genome, net in zip(self._genomes, self._nets)]

    def _input(self) -> None:
        if not self._headless:
            # poll for events
            for event in pygame.event.get():
                # exit game when exit is clicked
                if event.type == pygame.QUIT:
                    return self.close()

            # take user keyboard input
            keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()

            if keys[pygame.K_ESCAPE]:
                return self.close()

            # skip to next generation n
            if keys[pygame.K_n]:
                self._running = False

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
            f"Birds: {self.birds_alive}", True, (255, 255, 255)), (30, 45))
        self._screen.blit(self._font.render(
            f"Gen: {self._population.generation + 1}", True, (255, 255, 255)), (30, 80))
        self._screen.blit(self._font.render(
            f"Fit: {max(bird._genome.fitness for bird in self._birds)}", True, (255, 255, 255)), (30, 115))

    def __eval_gen(self, genomes: tuple[str, neat.genome.DefaultGenome], config: neat.config.Config) -> None:
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

    def run(self, *, generations: int) -> None:
        if generations <= 0:
            raise ValueError("Generations must be a positive number")

        self._population.run(self.__eval_gen, generations)

        print(f"Generations Completely Ran: {self._population.generation}")


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

    with NeatGame(headless=False, config=config) as game:
        game.run(generations=10)
