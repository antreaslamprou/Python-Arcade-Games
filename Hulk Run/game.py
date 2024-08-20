# Title: Hulk Run
# Author: Antreas Lamprou
# Email: alambrou1@uclan.ac.uk
# Description: This python program demonstrates the classic game where a dragon has to jump over some trees that are
# coming its way. This has been modified to a hulk jumping over buildings so he will avoid breaking them.

# import library for graphics
from tkinter import *
from random import *


# function that updates everything (dino/hulk animation, score, cactus/buildings, color of sky, clouds/airplanes and colligions)
def update_all():
    global frame_index, score
    if not paused and not beginning:
        if not dead:
            if not in_a_jump:
                canvas.itemconfig(dino_animation, image=frames[frame_index])
                frame_index += 1
                if frame_index == FRAME_COUNT:
                    frame_index = 0
            else:
                canvas.itemconfig(dino_animation, image=frames[FRAME_COUNT])

            (x, y) = canvas.coords(ground)  # this picks the coordinates of the given object
            if x >= 0:
                canvas.move(ground, -20, 0)  # move the background to the left by changing the X by -20
            else:

                canvas.move(ground, WIDTH, 0)

            update_score()
            cactus()
            color_sky()
            cloud()
            colligion()

    win.after(DELAY, update_all)


# function to make the jump
def update(index):
    global in_a_jump, jump_index
    if not paused:
        if not dead and not beginning:
            canvas.itemconfig(dino_animation, image=frames[index])

            # if in a jump, move the character by jump_offset
            if in_a_jump:
                jump_offset = jump_offsets[jump_index]
                canvas.move(dino_animation, 0, jump_offset)  # the 'canvas.move' function moves the specified object by the specified X.Y offset
                jump_index = jump_index + 1  # prepare for the next phase of the jump
                if jump_index > len(jump_offsets) - 1:  # when the jump ends, reset the jump_index and set in_a_jump back to False
                    jump_index = 0
                    in_a_jump = False

            index += 1
            if index == FRAME_COUNT:
                index = 0

    win.after(DELAY, update, index)


# function to avoid double jumping
def jump(__self__):
    global in_a_jump
    if not dead and not paused:
        if not in_a_jump:  # only process the jump event if no other jump is in progress
            in_a_jump = True


# function to make the colligion between dino/hulk & cactus/buildings
def colligion():
    (h_x,h_y) = canvas.coords(dino_animation)
    (c1_x,c1_y) = canvas.coords(cactus1)
    (c2_x,c2_y) = canvas.coords(cactus2)
    (c3_x,c3_y) = canvas.coords(cactus3)
    d1_x = abs(h_x - c1_x)
    d1_y = abs(h_y - c1_y)
    d2_x = abs(h_x - c2_x)
    d2_y = abs(h_y - c2_y)
    d3_x = abs(h_x - c3_x)
    d3_y = abs(h_y - c3_y)
    if d1_x <= 15 and d1_y <= 40 :
        lost()
        canvas.move(cactus1, 0, HEIGHT+100)
        canvas.coords(rip1, c1_x,c1_y)
    if d2_x <= 25 and d2_y <= 40 :
        lost()
        canvas.move(cactus2, 0, HEIGHT + 100)
        canvas.coords(rip2, c2_x, c2_y)
    if d3_x <= 15 and d3_y <= 40 :
        lost()
        canvas.move(cactus3, 0, HEIGHT + 100)
        canvas.coords(rip3, c3_x, c3_y)


# function for the update of score and highscore
def update_score():
    global score, highscore, speed
    score += 1
    canvas.itemconfig(s_text, text=f'{score:08}')
    if highscore <= score:
        highscore = score
    canvas.itemconfig(h_text, text=f'HI {highscore:08}')


# function for the movement of cactus/buildings
def cactus():
    canvas.move(cactus1,-speed, 0)
    canvas.move(cactus2,-speed, 0)
    canvas.move(cactus3, -speed, 0)
    (x1, y1) = canvas.coords(cactus1)
    (x2, y2) = canvas.coords(cactus2)
    (x3, y3) = canvas.coords(cactus3)
    if x1 < -20:
        canvas.move(cactus1, randint(WIDTH + 20, WIDTH + 500), 0)
    if x2 < -20:
        canvas.move(cactus2, randint(WIDTH + 20, WIDTH + 500), 0)
    if x3 < -20:
        canvas.move(cactus3, randint(WIDTH + 20, WIDTH + 500), 0)


# function for movement of clouds/airplanes
def cloud():
    canvas.move(airplane1, -speed/2, 0)
    (x1,y1) = canvas.coords(airplane1)
    (x2, y2) = canvas.coords(airplane2)
    if x1 < -50:
        canvas.move(airplane1, randint(WIDTH + 20, WIDTH + 500), 0)
    canvas.move(airplane2, speed/2, 0)
    if x2 > WIDTH + 50:
        canvas.move(airplane2, -randint(WIDTH + 20, WIDTH + 500), 0)


# fucntion to change the colour of the sky
def color_sky():
    j = int(str(score)[-2:])
    if 00 <= j <= 25:
        i = 0
    elif 26 <= j <= 50:
        i = 1
    elif 51 <= j <= 75:
        i = 2
    elif 76 <= j < 100:
        i = 3
    canvas.itemconfig(sky_box, fill= sky[i])


# function to make the losing screen
def lost():
    global dead
    dead = True
    canvas.itemconfig(dino_animation, image=dead_frame)
    canvas.move(dino_animation, -70,0)
    canvas.coords(d_box, WIDTH / 2 - 150, HEIGHT / 2 - 50, WIDTH / 2 + 150, HEIGHT / 2 + 50)
    canvas.coords(d_text, WIDTH / 2, HEIGHT / 2)


# function to do actions based on user inputs
def key_press(event):
    global paused, score, dead, beginning, in_a_jump, jump_index
    if event.char == 'q' or event.char == 'Q':
        quit()
    if event.char == 'p' or event.char == 'P':
        if paused == False:
            paused = True
            canvas.coords(box, WIDTH/2 - 150, HEIGHT/2-50, WIDTH/2 + 150, HEIGHT/2 + 50)
            canvas.coords(text, WIDTH/2, HEIGHT/2)
        else:
            paused = False
            canvas.coords(box, WIDTH+5, HEIGHT+5, WIDTH+10, HEIGHT+10)
            canvas.coords(text, WIDTH + 50, HEIGHT+ 50)
    if event.char == 'r' or event.char == 'R':
        if dead == True:
            dead = False
        if paused == True:
            paused = False
            canvas.coords(box, WIDTH + 5, HEIGHT + 5, WIDTH + 10, HEIGHT + 10)
            canvas.coords(text, WIDTH + 50, HEIGHT + 50)
        if in_a_jump == True:
            in_a_jump = False
            jump_index = 0
        score = 0
        canvas.coords(cactus1, WIDTH - 200, HEIGHT - 110)
        canvas.coords(cactus2, WIDTH, HEIGHT - 110)
        canvas.coords(cactus3, WIDTH + 200, HEIGHT - 110)
        canvas.coords(airplane1, WIDTH + 100, 250)
        canvas.coords(airplane2, -100, 100)
        canvas.coords(dino_animation, 150, HEIGHT - 120)
        canvas.coords(d_box, WIDTH + 5, HEIGHT + 5, WIDTH + 10, HEIGHT + 10)
        canvas.coords(d_text, WIDTH + 50, HEIGHT + 50)
        canvas.coords(rip1, 0, HEIGHT + 100)
        canvas.coords(rip2, 0, HEIGHT + 100)
        canvas.coords(rip3, 0, HEIGHT + 100)
        canvas.itemconfig(dino_animation, image=frames[0])
    if (event.char == 's' or event.char == 'S' ) and beginning == True:
        beginning = False
        canvas.delete(main_menu)


# use some standard variables.
WIDTH = 800
HEIGHT = 600
Title = "Hulk Run"

score = 0 # will be used to count the points
highscore = 0

DELAY = 100 # will be used to update the score based on this time (ms)
FRAME_COUNT = 8
frame_index = 0 # the index of the current frame - used to drive the animation
speed = 20
distance = 200

in_a_jump = False  # this boolean values tells us when already in a jump as to not start another one
jump_offsets = [0, -65, -40, -25, 20, 45, 65]
jump_index = 0 # the jump index is used to keep track of the phase of the jump, it completes after len(jump_offsets) steps


# speeds up based on score
if score > 100:
    speed += 5
if score > 200:
    speed += 5
if score > 300:
    speed += 5
if score > 400:
    speed += 5


#create the window
win = Tk()
win.title(Title)
win.geometry(str(WIDTH + 10)+"x"+str(HEIGHT+10))


# makes the window not resizeable
win.resizable(False, False) # [https://www.tutorialspoint.com/how-to-make-a-tkinter-window-not-resizable#:~:text=Let%20us%20suppose%20that%20we,resizable(False%2C%20False).]


# create canvas and frame
canvas = Canvas(win, width=WIDTH, height=HEIGHT)
canvas.pack()


# creates sky and list for the colors
sky = ['cyan','skyblue','blue','darkblue']
sky_box = canvas.create_rectangle(-10,-10,WIDTH+10,HEIGHT, fill=sky[0])


# add pictures to the game
background_img = PhotoImage(file='resources/background-tall.png')
background = canvas.create_image(WIDTH/2, HEIGHT/2, image= background_img)

ground_img = PhotoImage(file='resources/cityground.png')
ground = canvas.create_image(WIDTH/2, HEIGHT-45, image= ground_img)

airplane1_img = PhotoImage(file='resources/airplane1.png')
airplane2_img = PhotoImage(file='resources/airplane2.png')
airplane1 = canvas.create_image(WIDTH + 100, 250, image=airplane1_img)
airplane2 = canvas.create_image(-100, 100, image=airplane2_img)

frames = [PhotoImage(file='resources/hulk%i.png' % i) for i in range(FRAME_COUNT+1)]
dead_frame = PhotoImage(file='resources/hulk9.png')
dino_animation = canvas.create_image(150, HEIGHT-120, image=frames[0])

cac1 = PhotoImage(file='resources/building-tall.png')
cac2 = PhotoImage(file='resources/building-double.png')
cac3 = PhotoImage(file='resources/building-tall.png')
cactus1 = canvas.create_image(WIDTH - 200, HEIGHT-110, image=cac1)
cactus2 = canvas.create_image(WIDTH , HEIGHT-110, image=cac2)
cactus3 = canvas.create_image(WIDTH + 200, HEIGHT-110, image=cac3)

rip1_img = PhotoImage(file='resources/building-tall-rip.png')
rip2_img = PhotoImage(file='resources/building-double-rip.png')
rip3_img = PhotoImage(file='resources/building-tall-rip.png')
rip1 = canvas.create_image(0,HEIGHT + 100, image= rip1_img)
rip2 = canvas.create_image(0,HEIGHT + 100, image= rip2_img)
rip3 = canvas.create_image(0,HEIGHT + 100, image= rip3_img)

main_menu_img = PhotoImage(file='resources/main-menu.png')


# for pausing
paused = False
box = canvas.create_rectangle(WIDTH+5, HEIGHT+5, WIDTH+10, HEIGHT+10, fill= 'cyan', width= 5 )
text = canvas.create_text(WIDTH + 50 , HEIGHT + 50, text='PAUSED', font=('System', 20), fill='black')

# for end screen
dead = False
d_box = canvas.create_rectangle(WIDTH+5, HEIGHT+5, WIDTH+10, HEIGHT+10, fill= 'red', width= 5 )
d_text = canvas.create_text(WIDTH + 50 , HEIGHT + 50, text='GAME OVER', font=('System', 20), fill='black')


# creates the small guide on the bottom left of the screen and the score on the bottom right and the highscore on top right
canvas.create_text(200, HEIGHT - 10, text= 'CO1417  -  Dino Run  |  Q: Quit  -  P: Pause  -  R: Restart', font= ("System",15), fill= 'black')
s_text = canvas.create_text(WIDTH - 50, HEIGHT - 10, text= f'{score:08}', font= ("System",15), fill= 'black') # [https://bobbyhadz.com/blog/python-add-leading-zeros-to-number]
h_text = canvas.create_text(WIDTH - 50, 10, text= f'HI {highscore:08}', font= ("System",15), fill= 'black')


# create a main menu for the beginning
beginning = True
main_menu = canvas.create_image(WIDTH/2, HEIGHT/2, image=main_menu_img)


win.after(0, update_all) # calls function cimutaniusly


update(jump_index) # calls function


# binds functions
win.bind('<KeyPress>', key_press)

win.bind("<space>", jump)


# keeps the window up
win.mainloop()