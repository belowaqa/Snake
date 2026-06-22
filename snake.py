import tkinter as tk
import random

# Настройки
WIDTH = 400         # Ширина окна
HEIGHT = 400        # Высота окна
DIRECTIONS = ["Up", "Down", "Left", "Right"]  # Допустимые направления
CELL_SIZE = 10      # Размер одной клетки (и еды, и сегмента змейки)
DELAY = 100         # Задержка между кадрами (мс)


# Окно игры
root = tk.Tk()
root.title("Змейка | Счёт: 0")
root.resizable(False, False)

canvas = tk.Canvas(
    root, width=WIDTH, height=HEIGHT,
    bg="black", highlightthickness=0
)
canvas.pack()

# Создаём стартовую змейку
def create_snake():
    # Определяем допустимый диапазон координат головы змейки
    max_x = (WIDTH // CELL_SIZE) - 3
    max_y = (HEIGHT // CELL_SIZE) - 1

    # Случайные координаты головы (умножаем на CELL_SIZE для перевода в пиксели)
    x = random.randint(0, max_x) * CELL_SIZE
    y = random.randint(0, max_y) * CELL_SIZE

    # Строим змейку из 3 сегментов, направленную вправо
    return [(x, y), (x - CELL_SIZE, y), (x - 2 * CELL_SIZE, y)]

# Инициализация
snake = create_snake()
direction = "Right"
score = 0
game_over = False

# Еда
def create_food():
    while True:
        x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        if (x, y) not in snake:
            return (x, y)

food = create_food()

# Отрисовка еды
def draw_food():
    canvas.create_rectangle(
        food[0], food[1],
        food[0] + CELL_SIZE, food[1] + CELL_SIZE,
        fill="red"
    )

# Отрисовка змейки
def draw_snake():
    for segment in snake:
        canvas.create_rectangle(
            segment[0], segment[1],
            segment[0] + CELL_SIZE,
            segment[1] + CELL_SIZE,
            fill="green",
            outline="darkgreen"
        )

# Движение змейки
def move_snake():
    head_x, head_y = snake[0]

    # Определяем новое положение головы
    if direction == "Up":
        new_head = (head_x, head_y - CELL_SIZE)
    elif direction == "Down":
        new_head = (head_x, head_y + CELL_SIZE)
    elif direction == "Left":
        new_head = (head_x - CELL_SIZE, head_y)
    elif direction == "Right":
        new_head = (head_x + CELL_SIZE, head_y)

    # Добавляем голову в начало списка
    snake.insert(0, new_head)

    # Удаляем хвост, если не съедена еда
    if not check_food_collision():
        snake.pop()

# Проверка: съедена ли еда
def check_food_collision():
    global food, score
    if snake[0] == food:
        score += 1
        food = create_food()
        return True
    return False

# Проверка: столкновение со стенами
def check_wall_collision():
    head_x, head_y = snake[0]
    return (
        head_x < 0 or head_x >= WIDTH or
        head_y < 0 or head_y >= HEIGHT
    )

# Проверка: столкновение с собой
def check_self_collision():
    return snake[0] in snake[1:]

# Завершение игры
def end_game():
    global game_over
    game_over = True
    canvas.create_text(
        WIDTH // 2, HEIGHT // 2,
        text=f"Игра окончена! Счёт: {score}",
        fill="white",
        font=("Arial", 24)
    )

# Обновление заголовка окна
def update_title():
    root.title(f"Змейка | Счёт: {score}")

# Перезапуск игры
def restart_game():
    global snake, direction, food, score, game_over

    snake = create_snake()      # ← Используем случайную генерацию
    direction = "Right"
    food = create_food()
    score = 0
    game_over = False

    canvas.delete("all")
    draw_food()
    draw_snake()
    update_title()
    root.after(DELAY, game_loop)

# Обработка нажатий клавиш
def on_key_press(event):
    global direction, game_over

    key = event.keysym

    # Меняем направление, если игра не окончена и не происходит разворот на 180°
    if key in DIRECTIONS and not game_over:
        if (key == "Up" and direction != "Down" or
            key == "Down" and direction != "Up" or
            key == "Left" and direction != "Right" or
            key == "Right" and direction != "Left"):
            direction = key
    elif key == "space" and game_over:
        restart_game()

# Основной игровой цикл
def game_loop():
    global snake, food, score

    if game_over:
        return

    move_snake()

    if check_wall_collision() or check_self_collision():
        end_game()
        return

    canvas.delete("all")
    draw_food()
    draw_snake()
    update_title()
    root.after(DELAY, game_loop)

# Старт игры
root.bind("<KeyPress>", on_key_press)
draw_food()
draw_snake()
root.after(DELAY, game_loop)
root.mainloop()
