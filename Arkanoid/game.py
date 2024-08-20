# Title = "Arkanoid - First Capstone Project"
# Author: Antreas Lamprou
# Email: alambrou1@uclan.ac.uk
# Description: This python program demonstrates the classic Arkanoid game where a ball bounces to the sides and on
# the craft giving points when the bricks brake. Once all the bricks break, the user wins while if the ball touches
# the ground, the user loses. The game has 2 Modes : Easy and Hard.


# import library for graphics
from tkinter import *


# class that gives brick properties and creates them when called
class Bricks:
    def __init__(self, x1, y1, x2, y2, color, outline):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
        self.outline = outline
        self.object = canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=outline)


# class that creates the ball and adds speed properties
class Ball:

    # will be used to change ball's speed and position
    def __init__(self, x, y, speed_x, speed_y, radius, color):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.radius = radius
        self.color = color

    # changes ball position based on where it hits
    def move(self):
        self.x = self.x + self.speed_x
        if self.x >= WIDTH - self.radius:
            self.speed_x = -abs(self.speed_x)
        if self.x <= self.radius:
            self.speed_x = abs(self.speed_x)
        self.y = self.y + self.speed_y
        if self.y <= self.radius:
            self.speed_y = abs(self.speed_y)


# creates the craft as a class
class Craft:

    def __init__(self, x, y, x_size, y_size, color):
        self.x = x
        self.y = y
        self.x_size = x_size
        self.y_size = y_size
        self.color = color
        self.object = canvas.create_rectangle(x-r_width, y-r_height, x+r_width, y+r_height ,fill=color)

    def draw(self):
        canvas.coords(self.object, self.x-self.x_size, self.y-self.y_size, self.x+self.x_size, self.y+self.y_size)

    def move(self, mouse_x):
        self.x = mouse_x
        if mouse_x <= 60:
            self.x = 60
        if mouse_x >= WIDTH - 60:
            self.x = WIDTH - 60


# creates score as a class
class Score:
    def __init__(self, text, font, fill):
        self.text = text
        self.font = font
        self.fill = fill
        self.text_id = canvas.create_text(50, HEIGHT - 20, text= self.text, font= self.font, fill= self.fill)

    # updates the score
    def update(self, score):
        canvas.itemconfig(self.text_id, text='Score: ' + str(score), font=('System', 12), fill='black')


# draw and move the craft
def draw_and_move_craft(event):
    rec.move(event.x)
    rec.draw()


# creates a function to change the ball speed and position based on the colligion with the craft
def colligion_ball_craft():
    global b, rec, DEFAULT_BALL_RADIUS, r_height, r_width, HEIGHT
    if  HEIGHT - 35 >= b.y + DEFAULT_BALL_RADIUS >= HEIGHT - r_height - 35:
        if rec.x - r_width <= b.x <= rec.x + r_width:
            b.speed_x = (b.x - rec.x) * 10 / r_width  # adjust speed (x-axis) based on the the point of CONTACT between Ball and Craft
            b.speed_y = -abs(b.speed_y)  # reverse the ball to go up


# creates a function to change the ball speed and position based on the colligion with the bricks
def colligion_ball_bricks():
    global b, DEFAULT_BALL_RADIUS, score, bricks, side_x, side_y
    for brick in bricks:
        if b.y - DEFAULT_BALL_RADIUS <= brick.y2:
            if brick.x1 <= b.x + DEFAULT_BALL_RADIUS <= brick.x2 or brick.x1 <= b.x - DEFAULT_BALL_RADIUS <= brick.x2:
                bricks.remove(brick)
                canvas.delete(brick.object)
                b.speed_y = abs(b.speed_y)
                score += 10
                if brick.y1 <= b.y - DEFAULT_BALL_RADIUS < brick.y2:
                    if b.speed_x > 0:
                        b.speed_x = -b.speed_x
                    else:
                        b.speed_x = abs(b.speed_x)


# after the user loses the end screen appears
def end():
    canvas.delete(ball_id)
    canvas.create_rectangle(250, HEIGHT/2 - 100, WIDTH-250, HEIGHT / 2 + 100, fill='cyan', width=10)
    canvas.create_text(WIDTH/2, HEIGHT/2-25, text='GAME OVER', font=('System', 30), fill='red')
    canvas.create_text(WIDTH/2, HEIGHT/2+20, text='SCORE: ' + str(score), font=('System', 20), fill='red')


# after the user wins the win screen appears
def won():
    canvas.delete(ball_id)
    canvas.create_rectangle(250, HEIGHT / 2 - 100, WIDTH - 250, HEIGHT / 2 + 100, fill='cyan', width=10)
    canvas.create_text(WIDTH/2, HEIGHT/2-25, text='YOU WON', font=('System', 30), fill='green')
    canvas.create_text(WIDTH/2, HEIGHT/2+25, text='SCORE: ' + str(score), font=('System', 20), fill='green')


# creates a function for the animation of the ball, the ball's colligions and update the score
def animation():
    global b, bricks, DEFAULT_BALL_RADIUS, HEIGHT
    b.move()
    canvas.coords(ball_id, b.x-b.radius, b.y-b.radius, b.x+b.radius, b.y+b.radius)
    colligion_ball_craft()
    colligion_ball_bricks()
    s1.update(score)
    if b.y + DEFAULT_BALL_RADIUS == HEIGHT:
        end()
    if len(bricks) == 0:
        won()
    canvas.after(DELAY, animation)


# creates the 5 ball shadow illusion
def shadow():
    global WIDTH, HEIGHT, DEFAULT_BALL_RADIUS, b
    balls.append(canvas.create_oval(b.x -DEFAULT_BALL_RADIUS, b.y -DEFAULT_BALL_RADIUS, b.x + DEFAULT_BALL_RADIUS, b.y + DEFAULT_BALL_RADIUS, fill='dark red'))
    if len(balls) > MAX_BALLS:
        canvas.delete(balls.pop(0))
    canvas.tag_raise('ball')
    canvas.after(DELAY, shadow)


# creates the game mode based on input
def key_press(event):
    global game_mode
    if event.char == 'x' or event.char == 'X':
        quit()
    if event.char == '1' and game_mode == 0:
        game_mode = 1
        canvas.delete(text1,text2,text3,text4,main_menu,box)
        animation()
        shadow()
    if event.char == '2' and game_mode == 0:
        game_mode = 2
        canvas.delete(text1,text2,text3,text4,main_menu,box)
        animation()
        animation()
        animation()
        shadow()


# use some standard variables.
WIDTH = 800
HEIGHT = 600
Title = "Arkanoid - First Capstone Project"
color = ["purple" , "blue" , "skyblue", "yellow", "orange"] # brick color
side_x = 53 # brick width side size
side_y = 20 # brick height side size
game_mode = 0 # default value before choosing game mode

# for the ball
DELAY = 20  # delay between animations, in milliseconds
DEFAULT_SPEED = 5
DEFAULT_BALL_RADIUS = 10


# for moving rectangle's position and size
x = WIDTH/2
y = HEIGHT - 50
r_height = 5
r_width = 50


#create the window
win = Tk()
win.title(Title)
win.geometry(str(WIDTH + 10)+"x"+str(HEIGHT+10))


# makes the window not resizeable
win.resizable(False, False) # [https://www.tutorialspoint.com/how-to-make-a-tkinter-window-not-resizable#:~:text=Let%20us%20suppose%20that%20we,resizable(False%2C%20False).]


# will be used for the shadow of ball
balls = []
MAX_BALLS = 5


# create canvas and frame
canvas = Canvas(win, width=WIDTH, height=HEIGHT)
canvas.pack()


# create custom background
b = 100
for i in range (0,HEIGHT,b):
    for j in range (0,WIDTH,b):
        canvas.create_rectangle(j, i,j+b, i+b, fill= 'pink', outline='white')
canvas.create_rectangle(2,0, WIDTH, HEIGHT)


# creates the bricks and save them in an array
bricks = []
for i in range(0,5):
    for j in range (0,15):
        bricks.append(Bricks(j * side_x + 5, i*30, j * side_x + side_x - 1, i*30 + 3 + side_y, color[i], color[i]))


# creates the first craft at the central position
rec = Craft(WIDTH / 2, HEIGHT - r_height - 35, r_width, r_height, 'black')


# creates the score
score = 0
s1 = Score('Score: ', ('System', 12), 'black')


# creates the ball
b = Ball(WIDTH / 2, HEIGHT / 2, 0, DEFAULT_SPEED, DEFAULT_BALL_RADIUS, 'red')
ball_id = canvas.create_oval(b.x - b.radius, b.y - b.radius, b.x + b.radius, b.y + b.radius, fill='red', outline='black', tags='ball')


# creates main menu
main_menu= canvas.create_rectangle(5,145,WIDTH-3,HEIGHT-3,fill= 'pink', outline='pink')
box = canvas.create_rectangle(213,25,587,119, fill='pink', outline = 'black', width= 2)
text1= canvas.create_text(WIDTH/2, 71, text= "ARKANOID", font= ('System', 80), fill= 'black')
text2= canvas.create_text(WIDTH/2, 250, text="Easy Mode - Press: 1",font= ('System', 40), fill= 'green')
text3= canvas.create_text(WIDTH/2, 340, text="Hard Mode - Press: 2",font= ('System', 40), fill= 'red')
text4= canvas.create_text(WIDTH/2, 510, text="To exit press: x",font= ('System', 30), fill= 'black')


# binds functions
win.bind('<KeyPress>', key_press)

win.bind('<Motion>', draw_and_move_craft)


# keeps the window up
win.mainloop()