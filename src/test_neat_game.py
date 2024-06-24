import settings

from bird import Bird
from neat_game import NeatGame, NeatBird


class TestNeatGame(NeatGame):
    def __init__(self, *, headless: bool, bird: NeatBird):
        self._bird: NeatBird = bird

        # start normal game operation
        super(NeatGame, self).__init__(headless=headless)

    def _gen_birds(self) -> list[Bird]:
        self._bird.x = settings.SCREEN_SIZE.x / 2 - settings.BIRD_SIZE.x / 2
        self._bird.y = settings.SCREEN_SIZE.y / 2

        return [self._bird]

    def _display_text(self) -> None:
        self._screen.blit(self._font.render(
            f"FPS: {round(self._clock.get_fps(), 1)}", True, (255, 255, 255)), (30, 10))
        self._screen.blit(self._font.render(
            f"Fit: {self._bird._genome.fitness}", True, (255, 255, 255)), (30, 45))

    def run(self,) -> None:
        super(NeatGame, self).run()


if __name__ == "__main__":
    import pickle
    from pathlib import Path

    pickle_save_path: Path = Path(
        __file__).parent.resolve() / "neat_player.pkl"

    bird: NeatBird = pickle.load(open(pickle_save_path, 'rb'))
    bird._genome.fitness = 0

    with TestNeatGame(headless=False, bird=bird) as game:
        game.run()
