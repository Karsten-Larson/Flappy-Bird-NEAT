from tqdm import tqdm

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

        self._genome.fitness += max(1, 1 * self._genome.fitness / 10_000)

        output: float = self._net.activate(activation_tuple)[0]

        if output > settings.NEAT_THRESHOLD:
            self.jump()


class NeatGame(Game):
    def __init__(self, *, headless: bool, config: neat.config.Config):
        # begin neat genome config
        self._config: neat.config.Config = config
        self._population: neat.Population = neat.Population(config)

        self._progress_bar: tqdm | None = None

        # start normal game operation
        super().__init__(headless=headless)

    def _gen_birds(self) -> list[Bird]:
        # set the maximum value birds can get to
        NeatBird.fitness_threshold = self._config.fitness_threshold * 2

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

        # ground height
        ground_height: float = self._bases[0].y

        # find nearest pipe to the birds
        nearest_pipe: Pipes = min((pipe for pipe in self._pipes if pipe.x + pipe.width > self._birds[0].x),
                                  key=lambda pipe: abs(pipe.x - self._birds[0].x))

        # Create the input based on nearest pipe information
        horizontal_difference: float = abs(nearest_pipe.x - self._birds[0].x)
        for bird in self._birds:
            bottom_pipe_difference: float = nearest_pipe.bottom_pipe.y - bird.y
            top_pipe_difference: float = nearest_pipe.top_pipe.y + \
                nearest_pipe.top_pipe.height - bird.y
            ground_difference: float = ground_height - bird.y

            # Allows the bird to jump up
            bird.think(
                (
                    horizontal_difference, top_pipe_difference, bottom_pipe_difference, ground_difference, bird.velocity.y, nearest_pipe.velocity.x
                )
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
            genome.fitness = 0.0
            self._genomes.append(genome)

            net: neat.nn.FeedForwardNetwork = neat.nn.FeedForwardNetwork.create(
                genome, config)
            self._nets.append(net)

        super().run()
        self._progress_bar.update(1)

    def run(self, *, generations: int):
        if generations <= 0:
            raise ValueError("Generations must be a positive number")

        self._progress_bar: tqdm = tqdm(total=generations)

        best_genome = self._population.run(self.__eval_gen, generations)

        self._progress_bar.close()

        print(f"Generations Completely Ran: {self._population.generation}")

        return best_genome


if __name__ == "__main__":
    import pickle
    from pathlib import Path

    config_path: Path = Path(
        "/home/karsten/Coding/Python/Flappy Bird/src/neat-config.cfg")

    config: neat.config.Config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    with NeatGame(headless=True, config=config) as game:
        best_genome = game.run(generations=50)
        best_net: neat.nn.FeedForwardNetwork = neat.nn.FeedForwardNetwork.create(
            best_genome, config)

        pickle_save_path: Path = Path(
            __file__).parent.resolve() / "neat_player.pkl"

        pickle.dump(NeatBird(0, 0, genome=best_genome, net=best_net),
                    open(pickle_save_path, 'wb'), pickle.HIGHEST_PROTOCOL)
