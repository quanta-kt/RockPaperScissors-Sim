import enum
import itertools
import math
import pygame
import random
import sys


WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 500, 500
ENTITY_SIZE = 25

COLOR_BACKGROUND = 0xFFFFFF

ENTITY_COUNT = 3 * 10


class EntityType(enum.Enum):
    rock = 0b11_01
    paper = 0b01_10
    scissors = 0b10_11

    def beats(self, other: "EntityType") -> "EntityType":
        return self if (self.value >> 2) == other.value & 0b0011 else other

    @property
    def image_path(self) -> str:
        return f"resources/{self.name}_25x25.png"


class Entity:

    SPEED = 5

    def __init__(self, type: EntityType, x: float, y: float) -> None:
        self.type = type
        self.position = pygame.Rect(x, y, ENTITY_SIZE, ENTITY_SIZE)

        self._current_dest = (self.position.left, self.position.right)

    def move(self):

        deltaX = self._current_dest[0] - self.position.left
        deltaY = self._current_dest[1] - self.position.top

        if abs(deltaX + deltaY) < Entity.SPEED:
            x = self.position.left + random.randint(-50, 50)
            y = self.position.top + random.randint(-50, 50)

            self._current_dest = (
                min(
                    max(0, x),
                    WINDOW_WIDTH - ENTITY_SIZE,
                ),
                min(
                    max(0, y),
                    WINDOW_HEIGHT - ENTITY_SIZE,
                ),
            )

        angle = math.atan2(deltaY, deltaX)
        self.position.move_ip(
            math.cos(angle) * Entity.SPEED, math.sin(angle) * Entity.SPEED
        )


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()

    images = {
        EntityType.rock: pygame.image.load(EntityType.rock.image_path),
        EntityType.paper: pygame.image.load(EntityType.paper.image_path),
        EntityType.scissors: pygame.image.load(EntityType.scissors.image_path),
    }

    type_cycle = itertools.cycle(
        (EntityType.rock, EntityType.paper, EntityType.scissors)
    )
    entities = [
        Entity(
            type=next(type_cycle),
            x=float(random.randint(0, WINDOW_WIDTH - ENTITY_SIZE)),
            y=float(random.randint(0, WINDOW_WIDTH - ENTITY_SIZE)),
        )
        for _ in range(ENTITY_COUNT)
    ]

    positions = [entity.position for entity in entities]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(COLOR_BACKGROUND)

        for entity in entities:
            screen.blit(images[entity.type], entity.position)
            entity.move()

            for inx in entity.position.collidelistall(positions):
                other = entities[inx]
                entity.type = other.type = entity.type.beats(other.type)

        pygame.display.update()
        clock.tick(10)
