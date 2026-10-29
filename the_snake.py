from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER_SCREEN = (GRID_WIDTH // 2, GRID_HEIGHT // 2)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Обработка нажатия клавиш
def handle_keys(game_object):
    """Обработка нажатия клавиш"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


# Тут опишите все классы игры.
class GameObject():
    """Базовый класс игры Змейка для наследования"""

    def __init__(self, body_color=SNAKE_COLOR, position=CENTER_SCREEN):
        self.body_color = body_color
        self.position = position

    def draw(self):
        """Шаблон отрисовки элемента"""
        pass


class Snake(GameObject):
    """Класс змейки из игры Змейка"""

    def __init__(self, length=1, positions=CENTER_SCREEN, direction=RIGHT,
                 next_direction=RIGHT,
                 body_color=SNAKE_COLOR, position=CENTER_SCREEN):
        self.length = length
        # Надо сделать списком всех позиций, а не просто typle
        self.positions = []
        self.positions.append(positions)
        self.direction = direction
        self.next_direction = next_direction
        self.body_color = body_color
        self.position = position

    def draw(self):
        """Отрисовка змейки"""
        for position in self.positions[:]:
            rect = (pygame.Rect((position[0] * 20, position[1] * 20),
                                (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def update_direction(self):
        """Обновление направления движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def eating(self, apple):
        """Проверка съела ли змейка яблоко"""
        if abs(self.positions[0][0] - apple.position[0]) < 1:
            if abs(self.positions[0][1] - apple.position[1]) < 1:
                return True
        return False

    def get_head_position(self):
        """Получение позиции головы"""
        return self.positions[0]

    def reset(self):
        """Сброс змейки"""
        self.positions = [CENTER_SCREEN]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = RIGHT

    def move(self, flag):
        """Логика движения змейки как объекта"""
        self.positions.insert(0, ((self.positions[0][0] + self.direction[0]) % GRID_WIDTH,
                                  (self.positions[0][1] + self.direction[1]) % GRID_HEIGHT))
        if self.positions[0] in self.positions[1:]:
            self.reset()
            t = 1
            print(t)
            return -1
        if not flag:
            self.positions.pop()
        else:
            self.length += 1


class Apple(GameObject):
    """Класс яблока из игры Змейка"""

    @classmethod
    def randomize_position(cls):
        """Рандомизация позиции яблока"""
        return (randint(0, GRID_WIDTH - 1), randint(0, GRID_HEIGHT - 1))

    def __init__(self):
        self.position = Apple.randomize_position()
        self.body_color = APPLE_COLOR

    def draw(self):
        """Отрисовка яблока на поле"""
        rect = pygame.Rect((self.position[0] * 20, self.position[1] * 20),
                           (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def main():
    """Точка запуска"""
    pygame.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)   # очистка экрана

        handle_keys(snake)                    # ввод
        snake.update_direction()              # применить направление

        flag = snake.eating(apple)            # проверка яблока
        if snake.move(flag) == -1:            # движение (и проверка смерти)
            apple = Apple()                   # новое яблоко после сброса
            continue

        if flag:
            apple = Apple()                   # новое яблоко

        snake.draw()                          # отрисовка
        apple.draw()
        pygame.display.update()               # показ


if __name__ == '__main__':
    """Главная функция"""
    main()


#     Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
