import tkinter as tk
import random

# Настройки игры
WIDTH = 600
HEIGHT = 600
DIRECTIONS = ["Up", "Down", "Left", "Right"]
CELL_SIZE = 10
DELAY = 100

# Создание главного окна
root = tk.Tk()
root.title("Snake | Score:0")
root.resizable(False, False)

# Создание холста для рисования
canvas = tk.Canvas(
    root,
    width=WIDTH,
    height=HEIGHT,
    bg="black",
    highlightthickness=0,
)
canvas.pack()

# Начальное состояние игры
snake = [(100, 100), (90,100), (80,100)]
direction = "Right"
score = 0
game_over = False

# Создание еды
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
        food[0] + CELL_SIZE,
        food[1] + CELL_SIZE,
        fill="red",
    )

def draw_snake():
    for segment in snake:
        canvas.create_rectangle(
            segment[0], segment[1],
            segment[0] + CELL_SIZE,
            segment[1] + CELL_SIZE,
            fill="green",
            outline="darkgreen"
        )

def move_snake():
    head_x, head_y = snake[0]

    if direction == "Up":
        new_head = (head_x, head_y - CELL_SIZE)
    elif direction == "Down":
        new_head = (head_x, head_y + CELL_SIZE)
    elif direction == "Left":
        new_head = (head_x - CELL_SIZE, head_y)
    elif direction == "Right":
        new_head = (head_x + CELL_SIZE, head_y)

    snake.insert(0, new_head)  # Добавляем новую голову
    snake.pop()  # Удаляем хвост (если еда не съедена)


def on_key_press(event):
    global direction
    key = event.keysym
    if key in DIRECTIONS:
        if (key == "Up" and direction != "Down" or
            key == "Down" and direction != "Up" or
            key == "Left" and direction != "Right" or
            key == "Right" and direction != "Left"):
            direction = key

root.bind("<KeyPress>", on_key_press)

# Игровой цикл
def game_loop():
    global snake, food, score
    move_snake()
    canvas.delete("all")
    draw_food()
    draw_snake()
    root.after(DELAY, game_loop)

# Первоначальная отрисовка
draw_food()
draw_snake()
root.after(DELAY, game_loop)

# Запуск главного цикла
root.mainloop()