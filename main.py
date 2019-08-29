import tkinter as t
from random import randint
import ast as a
import time

w = t.Tk()
robots = []
methods = []
boxes = []

x, y = 10, 10


def rast(x, y, x1, y1, board):
    from math import floor
    dx = abs(x - x1)
    dy = abs(y - y1)
    a = (y1 - y) / (x1 - x)
    if dy > dx:
        # x,x1,y,y1=y,y1,x,x1
        print(f"range: {y1-y}")
        a = 1 / a
        for i in range(y1 - y):
            print(f'x: {floor(i*a)+x} y: {i+y}')
            board[i + y][floor(x)] = 'draw'
            x += a
    else:
        for i in range(x1 - x):
            print(f"x: {i}")
            print(f'nfloor: {i*a}')
            print(f'floor: {floor(i*a)}')
            board[floor(y)][i + x] = "draw"
            y += a
    print(f'a: {a}')
    return board


class Board:
    def __init__(self, x=x, y=y):
        self.structure = []
        for i in range(y):
            temp = []
            for j in range(x):
                temp.append('')
            self.structure.append(temp)
            temp = []
        self.x = x
        self.y = y

    def redraw(self, ca):
        ca.delete('all')
        x, y = 0, 0
        for i in self.structure:
            for j in i:
                ca.create_rectangle(x, y, x + 30, y + 30)
                if str(j) == 'draw':
                    ca.create_rectangle(x + 2, y + 2, x + 28, y + 28, outline='black', fill='black')
                if str(j) == 'robot':
                    ca.create_rectangle(x + 3, y + 3, x + 27, y + 27, outline='red', fill='red')
                    if j.box == 1:
                        ca.create_rectangle(x + 5, y + 5, x + 25, y + 25, outline='blue', fill='blue')
                        ca.create_text(x + 13, y + 10, fill='white', font='Times 8 italic bold', text='box')
                        # ca.create_rectangle(x+24,y+24,x+26,y+26, outline='blue', fill='blue')
                        ca.create_text(x, y, fill="darkblue", font="Times 10 italic bold", text=j.name)
                    elif j.box == 2:
                        ca.create_rectangle(x + 6, y + 6, x + 24, y + 24, outline='blue', fill='blue')
                        ca.create_text(x, y, fill="darkblue", font="Times 10 italic bold", text=j.name + 'b')
                        ca.create_text(x + 13, y + 10, fill='white', font='Times 8 italic bold', text='box')
                    else:
                        ca.create_text(x + 10, y + 10, fill="darkblue", font="Times 10 italic bold", text=j.name)

                if str(j) == 'box':
                    ca.create_rectangle(x + 5, y + 5, x + 25, y + 25, outline='blue', fill='blue')
                    ca.create_text(x + 13, y + 10, fill='white', font='Times 8 italic bold', text='box')
                x += 30
            y += 30
            x = 0


class Box:
    def __init__(self, number, x, y, board):
        a = 0
        while not self.place(x, y, board):
            if self.place(x, y, board):
                pass
            elif a == 10:
                print('failed to create object')
                return
            else:
                x = randint(0, globals()['x'])
                y = randint(0, globals()['y'])
                a += 1
                continue
        self.name = f"#{number+1}"
        self.x = x
        self.y = y

    def place(self, x, y, board):
        if board.structure[y][x] == '':
            board.structure[y][x] = self
            print('Placed')
            return True
        return False

    def __str__(self):
        return 'box'


class Robot:
    def __init__(self, number, x, y, board):
        self.box = 0  # 0 - нет бокса, 1 - под боксом, 2 - держит бокс
        self.boxobject = None
        a = 0
        while not self.place(x, y, board):
            if self.place(x, y, board):
                pass
            elif a == 10:
                print('failed to create object')
                return
            else:
                x = randint(0, globals()['x'])
                y = randint(0, globals()['y'])
                a += 1
                continue
        self.name = f"#{number+1}"
        self.x = x
        self.y = y

    def place(self, x, y, board):
        if board.structure[y][x] == '':
            board.structure[y][x] = self
            print('Placed')
            return True
        return False

    def automove(self, track, b, c):
        if not track:
            return

        for i in track[::-1]:
            if self.x > i[0]:
                self.move(b, 'left', c)
            elif self.x < i[0]:
                self.move(b, 'right', c)
            elif self.y < i[1]:
                self.move(b, 'down', c)
            elif self.y > i[1]:
                self.move(b, 'up', c)

    def move(self, board, direction, c):
        if direction == 'up':
            if self.y > 0:
                if board.structure[self.y - 1][self.x] == '' or (
                        str(board.structure[self.y - 1][self.x]) == 'box' and (self.box == 0 or self.box == 1)):
                    if self.box == 1:
                        board.structure[self.y][self.x] = self.boxobject
                        self.box = 0
                        self.boxobject = None
                    else:
                        board.structure[self.y][self.x] = ''
                    if str(board.structure[self.y - 1][self.x]) == 'box':
                        self.box = 1
                        self.boxobject = board.structure[self.y - 1][self.x]
                    board.structure[self.y - 1][self.x] = self
                    self.y -= 1
        elif direction == 'left':
            if self.x > 0:
                if board.structure[self.y][self.x - 1] == '' or (
                        str(board.structure[self.y][self.x - 1]) == 'box' and (self.box == 0 or self.box == 1)):
                    if self.box == 1:
                        board.structure[self.y][self.x] = self.boxobject
                        self.box = 0
                        self.boxobject = None
                    else:
                        board.structure[self.y][self.x] = ''
                    if str(board.structure[self.y][self.x - 1]) == 'box':
                        self.box = 1
                        self.boxobject = board.structure[self.y][self.x - 1]
                    board.structure[self.y][self.x - 1] = self
                    self.x -= 1
        elif direction == 'down':
            if self.y < board.y - 1:
                if board.structure[self.y + 1][self.x] == '' or (
                        str(board.structure[self.y + 1][self.x]) == 'box' and (self.box == 0 or self.box == 1)):
                    if self.box == 1:
                        board.structure[self.y][self.x] = self.boxobject
                        self.box = 0
                        self.boxobject = None
                    else:
                        board.structure[self.y][self.x] = ''
                    if str(board.structure[self.y + 1][self.x]) == 'box':
                        self.box = 1
                        self.boxobject = board.structure[self.y + 1][self.x]
                    board.structure[self.y + 1][self.x] = self
                    self.y += 1
        elif direction == 'right':
            if self.x < board.x - 1:
                if board.structure[self.y][self.x + 1] == '' or (
                        str(board.structure[self.y][self.x + 1]) == 'box' and (self.box == 0 or self.box == 1)):
                    if self.box == 1:
                        board.structure[self.y][self.x] = self.boxobject
                        self.box = 0
                        self.boxobject = None
                        print('box set')
                    else:
                        board.structure[self.y][self.x] = ''
                    if str(board.structure[self.y][self.x + 1]) == 'box':
                        self.box = 1
                        self.boxobject = board.structure[self.y][self.x + 1]
                        print('box detected')
                    board.structure[self.y][self.x + 1] = self
                    self.x += 1
        if self.box == 2:
            print(f'box moved with {self.name}')
            self.boxobject.x = self.x
            self.boxobject.y = self.y
        board.redraw(c)

    def bind(self, w, b, c):
        w.unbind('<Up>')
        w.unbind('<Down>')
        w.unbind('<Left>')
        w.unbind('<Right>')
        w.bind('<Up>', lambda arg=1: self.move(b, 'up', c))
        w.bind('<Down>', lambda arg=1: self.move(b, 'down', c))
        w.bind('<Left>', lambda arg=1: self.move(b, 'left', c))
        w.bind('<Right>', lambda arg=1: self.move(b, 'right', c))
        w.bind('Control_R>', lambda arg=1: self.catch(b, c))
        w.bind('<Control_L>', lambda arg=1: self.catch(b, c))
        w.bind('<Button-3>', lambda arg=1: self.automove(a.find(self.x, self.y, x, y, b, c), b, c))
        print(self.name)

    def catch(self, b, c):
        if self.box == 2:
            self.box = 1
            b.redraw(c)
        elif self.box == 1:
            self.box = 2
            b.redraw(c)

    def __str__(self):
        return 'robot'


b = Board()

c = t.Canvas(w, width=x * 30, height=y * 30, bg='white')
c.place(x=0, y=0)
# robots.append(Robot(0, 5, 5, b))
print(b.structure)
# robots.append(Robot(1, 3, 3, b))
# robots.append(Robot(2, 1, 1, b))
# boxes.append(Box(2, 7, 8, b))

b.redraw(c)
for i in range(5):
    robots.append(Robot(i, randint(0, x - 1), randint(0, y - 1), b))

for i in range(3):
    boxes.append(Box(i, randint(0, x - 1), randint(0, y - 1), b))

print(robots)

for i in range(len(robots)):
    methods.append(lambda arg=i: robots[arg].bind(w, b, c))
print(len(methods))

for i in range(len(methods)):
    te = t.Button(w, text=f'#{i+1}', width=5, height=5, command=methods[i])
    te.place(x=(i % 3) * 50 + 20, y=y * 30 + 10 + (i // 3) * 100)

w.geometry(f'{x*30}x{y*40+(((len(robots)-1)//3)*100)}')
w.maxsize(width=x * 30, height=y * 40 + (((len(robots) - 1) // 3) * 100))
w.minsize(width=x * 30, height=y * 40 + (((len(robots) - 1) // 3) * 100))
print(len(robots) // 3 * 100)
b.redraw(c)

w.mainloop()
