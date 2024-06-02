import pygame
from pathlib import Path

# path to all game image folder
ASSETS_PATH: Path = Path(__file__).parent.parent / "sprites"
FRAME_RATE: float = 60.0

# screen size
SCREEN_SIZE: pygame.Vector2 = pygame.Vector2(500, 500)

# bird size
BIRD_SIZE: pygame.Vector2 = pygame.Vector2(35, 35)

# bird movement
TERMINAL_VELOCITY: pygame.Vector2 = pygame.Vector2(0, 2_000)
GRAVITY: pygame.Vector2 = pygame.Vector2(0, 250)
JUMP_VELOCITY: pygame.Vector2 = pygame.Vector2(0, -150)
JUMP_DELAY: float = 0.25

# pipe size
PIPE_SIZE: pygame.Vector2 = pygame.Vector2(52, 320)
PIPE_GAP: float = 90.0
PIPE_HEIGHTS: list[float] = list(range(0, 275, 25))

# pipe movement
PIPE_INITIAL_X: float = SCREEN_SIZE.x
PIPE_VELOCITY: pygame.Vector2 = pygame.Vector2(-100, 0)

# base size
BASE_SIZE: pygame.Vector2 = pygame.Vector2(336, 112)

# base movement
# BASE_VELOCITY: pygame.Vector2 = pygame.Vector2(-150, 0)
BASE_VELOCITY: pygame.Vector2 = PIPE_VELOCITY.copy()

# neat controls
NEAT_THRESHOLD: float = 0.5
