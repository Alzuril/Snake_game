from tkinter import *
import random

GAME_WIDTH = 700
GAME_HIGHT = 700
SPEED = 150
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = 'green'
FOOD_COLOR = 'red'
BG_COLOR = 'black'



class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = field.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)


class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH/SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HIGHT/SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        field.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")


def nextTurn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    if direction == "down":
        y += SPACE_SIZE
    if direction == "left":
        x -= SPACE_SIZE
    if direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))
    square = field.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        score_lbl.config(text="Score:{}".format(score))

        field.delete('food')
        food = Food()
    else:
        del snake.coordinates[-1]
        field.delete(snake.squares[-1])
        del snake.squares[-1]

    if checkCollision(snake):
        gameOver()
    else:
        window.after(SPEED, nextTurn, snake, food)

def changeDiraction(new_diraction):
    global direction

    if new_diraction == 'left':
        if direction != 'right':
            direction = new_diraction
    elif new_diraction == 'right':
        if direction != 'left':
            direction = new_diraction
    elif new_diraction == 'up':
        if direction != 'down':
            direction = new_diraction
    elif new_diraction == 'down':
        if direction != 'up':
            direction = new_diraction

def checkCollision(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HIGHT:
        return True
    
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    
    return False

def gameOver():
    field.delete(ALL)
    field.create_text(field.winfo_width()/2, field.winfo_height()/2, font=("consolas", 70), text="GAME OVER", fill='red', tag='gameover')

#create game window

window = Tk()
window.title("Snake game")
window.resizable(False, False)

score = 0
direction = 'down'

score_lbl = Label(window, text="Score:{}".format(score), font=("consolas", 40))
score_lbl.pack()

field = Canvas(window, bg=BG_COLOR, height=GAME_HIGHT, width=GAME_WIDTH)
field.pack()

window.bind('<Left>', lambda x: changeDiraction('left'))
window.bind('<Right>', lambda x: changeDiraction('right'))
window.bind('<Up>', lambda x: changeDiraction('up'))
window.bind('<Down>', lambda x: changeDiraction('down'))

snake = Snake()
food = Food()

nextTurn(snake, food)


window.mainloop()
