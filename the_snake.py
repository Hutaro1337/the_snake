import json
import os
import random
from random import randint

import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (0, 0, 0)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
STONE_COLOR = (128, 128, 128)
POISON_COLOR = (147, 112, 219)
SPEED_BOOST_COLOR = (255, 165, 0)
SLOW_DOWN_COLOR = (173, 216, 230)

MIN_SPEED = 5
MAX_SPEED = 30
DEFAULT_SPEED = 15
MAX_APPLES = 3
MAX_STONES = 5
MAX_POISONS = 2
MAX_POWERUPS = 2
SCORE_FILE = "snake_record.json"

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
clock = pygame.time.Clock()


class GameObject:
    def __init__(self, body_color=None, position=None):
        self.position = position
        self.body_color = body_color

    def draw(self):
        pass


class Apple(GameObject):
    def __init__(self):
        super().__init__(APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self):
        if self.position:
            rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Stone(GameObject):
    def __init__(self):
        super().__init__(STONE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self):
        if self.position:
            rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Poison(GameObject):
    def __init__(self):
        super().__init__(POISON_COLOR)
        self.randomize_position()

    def randomize_position(self):
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self):
        if self.position:
            rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class SpeedBoost(GameObject):
    def __init__(self):
        super().__init__(SPEED_BOOST_COLOR)
        self.randomize_position()
        self.duration = 100

    def randomize_position(self):
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self):
        if self.position:
            rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class SlowDown(GameObject):
    def __init__(self):
        super().__init__(SLOW_DOWN_COLOR)
        self.randomize_position()
        self.duration = 100

    def randomize_position(self):
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self):
        if self.position:
            rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    def __init__(self):
        super().__init__(SNAKE_COLOR)
        self.reset()
        self.direction = RIGHT
        self.next_direction = None

    def reset(self):
        start_x = SCREEN_WIDTH // 2
        start_y = SCREEN_HEIGHT // 2
        start_x = start_x // GRID_SIZE * GRID_SIZE
        start_y = start_y // GRID_SIZE * GRID_SIZE
        self.positions = [(start_x, start_y)]
        self.length = 1

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        self.last = self.positions[-1]
        head_x, head_y = self.get_head_position()
        new_x = head_x + self.direction[0] * GRID_SIZE
        new_y = head_y + self.direction[1] * GRID_SIZE

        if new_x >= SCREEN_WIDTH:
            new_x = 0
        elif new_x < 0:
            new_x = SCREEN_WIDTH - GRID_SIZE
        if new_y >= SCREEN_HEIGHT:
            new_y = 0
        elif new_y < 0:
            new_y = SCREEN_HEIGHT - GRID_SIZE

        self.positions.insert(0, (new_x, new_y))
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_head_position(self):
        return self.positions[0]

    def grow(self):
        self.length += 1

    def shrink(self):
        if self.length > 1:
            self.length -= 1
            if len(self.positions) > self.length:
                self.positions.pop()

    def check_collision(self):
        head = self.get_head_position()
        return head in self.positions[1:]


def load_record():
    if os.path.exists(SCORE_FILE):
        try:
            with open(SCORE_FILE, "r") as f:
                data = json.load(f)
                return data.get("record", 1)
        except:
            return 1
    return 1


def save_record(record):
    data = {"record": record}
    with open(SCORE_FILE, "w") as f:
        json.dump(data, f)


def update_window_title(
    snake_length, record_length, speed, speed_boost_active, slow_down_active
):
    title_parts = [
        f"Змейка | Длина: {snake_length} | Рекорд: {record_length} | Скорость: {speed}"
    ]

    if speed_boost_active:
        title_parts.append("Ускорение ▲")
    if slow_down_active:
        title_parts.append("Замедление ▼")

    title_parts.append("Управление: [↑↓←→] Движение | [1] + [2] - | [R] Сброс")

    pygame.display.set_caption(" | ".join(title_parts))


def handle_keys(snake, speed):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, speed
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False, speed
            elif event.key == pygame.K_r:
                snake.reset()
                return True, DEFAULT_SPEED
            elif event.key == pygame.K_1:
                new_speed = min(speed + 3, MAX_SPEED)
                return True, new_speed
            elif event.key == pygame.K_2:
                new_speed = max(speed - 3, MIN_SPEED)
                return True, new_speed
            elif event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT
    return True, speed


def is_position_valid(position, all_objects, snake):
    if position in snake.positions:
        return False

    for obj_list in all_objects:
        for obj in obj_list:
            if obj.position == position:
                return False

    return True


def respawn_objects(objects_list, max_count, object_class, all_objects, snake):
    while len(objects_list) < max_count:
        new_obj = object_class()
        attempts = 0
        while (
            not is_position_valid(new_obj.position, all_objects, snake)
            and attempts < 100
        ):
            new_obj.randomize_position()
            attempts += 1
        if attempts < 100:
            objects_list.append(new_obj)


def main():
    pygame.init()

    record_length = load_record()
    snake = Snake()

    apples = []
    stones = []
    poisons = []
    speed_boosts = []
    slow_downs = []

    all_objects = [apples, stones, poisons, speed_boosts, slow_downs]

    for _ in range(MAX_APPLES):
        apple = Apple()
        while not is_position_valid(apple.position, all_objects, snake):
            apple.randomize_position()
        apples.append(apple)

    for _ in range(MAX_STONES):
        stone = Stone()
        while not is_position_valid(stone.position, all_objects, snake):
            stone.randomize_position()
        stones.append(stone)

    for _ in range(MAX_POISONS):
        poison = Poison()
        while not is_position_valid(poison.position, all_objects, snake):
            poison.randomize_position()
        poisons.append(poison)

    for _ in range(MAX_POWERUPS):
        speed_boost = SpeedBoost()
        while not is_position_valid(speed_boost.position, all_objects, snake):
            speed_boost.randomize_position()
        speed_boosts.append(speed_boost)

    for _ in range(MAX_POWERUPS):
        slow_down = SlowDown()
        while not is_position_valid(slow_down.position, all_objects, snake):
            slow_down.randomize_position()
        slow_downs.append(slow_down)

    speed = DEFAULT_SPEED
    speed_boost_active = False
    slow_down_active = False
    speed_boost_timer = 0
    slow_down_timer = 0
    game_active = True

    update_window_title(
        snake.length, record_length, speed, speed_boost_active, slow_down_active
    )

    while game_active:
        clock.tick(speed)

        game_active, speed = handle_keys(snake, speed)

        snake.update_direction()
        snake.move()

        head_pos = snake.get_head_position()

        if snake.check_collision():
            snake.reset()
            speed = DEFAULT_SPEED
            speed_boost_active = False
            slow_down_active = False

        for apple in apples[:]:
            if head_pos == apple.position:
                snake.grow()
                apples.remove(apple)
                if snake.length > record_length:
                    record_length = snake.length
                    save_record(record_length)
                break

        for stone in stones[:]:
            if head_pos == stone.position:
                snake.reset()
                speed = DEFAULT_SPEED
                speed_boost_active = False
                slow_down_active = False
                break

        for poison in poisons[:]:
            if head_pos == poison.position:
                snake.shrink()
                poisons.remove(poison)
                if snake.length < 1:
                    snake.reset()
                    speed = DEFAULT_SPEED
                break

        for speed_boost in speed_boosts[:]:
            if head_pos == speed_boost.position:
                speed = min(speed + 10, MAX_SPEED)
                speed_boosts.remove(speed_boost)
                speed_boost_active = True
                speed_boost_timer = 100
                break

        for slow_down in slow_downs[:]:
            if head_pos == slow_down.position:
                speed = max(speed - 10, MIN_SPEED)
                slow_downs.remove(slow_down)
                slow_down_active = True
                slow_down_timer = 100
                break

        if speed_boost_active:
            speed_boost_timer -= 1
            if speed_boost_timer <= 0:
                speed_boost_active = False
                speed = max(speed - 5, DEFAULT_SPEED)

        if slow_down_active:
            slow_down_timer -= 1
            if slow_down_timer <= 0:
                slow_down_active = False
                speed = min(speed + 5, DEFAULT_SPEED)

        respawn_objects(apples, MAX_APPLES, Apple, all_objects, snake)
        respawn_objects(poisons, MAX_POISONS, Poison, all_objects, snake)
        respawn_objects(speed_boosts, MAX_POWERUPS, SpeedBoost, all_objects, snake)
        respawn_objects(slow_downs, MAX_POWERUPS, SlowDown, all_objects, snake)

        update_window_title(
            snake.length, record_length, speed, speed_boost_active, slow_down_active
        )

        screen.fill(BOARD_BACKGROUND_COLOR)

        for stone in stones:
            stone.draw()

        for poison in poisons:
            poison.draw()

        for speed_boost in speed_boosts:
            speed_boost.draw()

        for slow_down in slow_downs:
            slow_down.draw()

        for apple in apples:
            apple.draw()

        snake.draw()

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
