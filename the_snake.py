"""Snake game implementation using PyGame."""

from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (0, 0, 0)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 15  # Уменьшил для более комфортной игры

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Base class for all game objects."""

    def __init__(self, body_color=None, position=None):
        """Initialize game object with color and position.

        Args:
            body_color (tuple): RGB color tuple.
            position (tuple): (x, y) coordinates.
        """
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Draw the game object on the screen."""
        pass


class Apple(GameObject):
    """Apple object that snake can eat."""

    def __init__(self):
        """Initialize apple with random position."""
        super().__init__(APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Set apple to a random position on the grid."""
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self):
        """Draw apple on the screen."""
        if self.position:
            rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Snake object controlled by player."""

    def __init__(self):
        """Initialize snake at center of screen."""
        super().__init__(SNAKE_COLOR)
        self.reset()
        self.direction = RIGHT
        self.next_direction = None

    def reset(self):
        """Reset snake to starting position and size."""
        # Начинаем змейку в центре экрана
        start_x = SCREEN_WIDTH // 2
        start_y = SCREEN_HEIGHT // 2
        # Выравниваем по сетке
        start_x = start_x // GRID_SIZE * GRID_SIZE
        start_y = start_y // GRID_SIZE * GRID_SIZE
        self.positions = [(start_x, start_y)]
        self.length = 1

    def update_direction(self):
        """Update snake direction from queued input."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Move snake in current direction."""
        # Сохраняем последнюю позицию для затирания
        self.last = self.positions[-1]

        # Получаем текущую позицию головы
        head_x, head_y = self.get_head_position()

        # Вычисляем новую позицию головы
        new_x = head_x + self.direction[0] * GRID_SIZE
        new_y = head_y + self.direction[1] * GRID_SIZE

        # Обрабатываем выход за границы экрана (телепортация)
        if new_x >= SCREEN_WIDTH:
            new_x = 0
        elif new_x < 0:
            new_x = SCREEN_WIDTH - GRID_SIZE
        if new_y >= SCREEN_HEIGHT:
            new_y = 0
        elif new_y < 0:
            new_y = SCREEN_HEIGHT - GRID_SIZE

        # Добавляем новую позицию головы в начало списка
        self.positions.insert(0, (new_x, new_y))

        # Удаляем последнюю позицию, если змейка не выросла
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Draw snake on the screen."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_head_position(self):
        """Get position of snake's head.

        Returns:
            tuple: (x, y) coordinates of head.
        """
        return self.positions[0]

    def grow(self):
        """Increase snake length."""
        self.length += 1

    def check_collision(self):
        """Check if snake collides with itself.

        Returns:
            bool: True if collision detected, False otherwise.
        """
        # Проверяем столкновение змейки со своим телом
        head = self.get_head_position()
        return head in self.positions[1:]


def handle_keys(snake):
    """Handle keyboard input for snake control.

    Args:
        snake (Snake): Snake object to control.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Main game loop."""
    pygame.init()

    # Создаем объекты игры
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        # Обработка управления
        handle_keys(snake)

        # Обновление направления змейки
        snake.update_direction()

        # Движение змейки
        snake.move()

        # Проверка столкновения с самой собой
        if snake.check_collision():
            snake.reset()
            apple.randomize_position()

        # Проверка съедания яблока
        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.randomize_position()

            # Проверяем, чтобы яблоко не появилось на змейке
            while apple.position in snake.positions:
                apple.randomize_position()

        # Отрисовка
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()