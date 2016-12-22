# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

PADDLE_SPEED = 8
ball_pos = [0, 0]
ball_vel = [0, 0]
score1 = 0
score2 = 0
paddle1_pos = 0
paddle2_pos = 0
paddle1_vel = 0
paddle2_vel = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists

    ball_pos = [WIDTH / 2 - 1, HEIGHT / 2 - 1]
    if direction == LEFT:
        ball_vel = [random.randrange(120, 240) / 60, -random.randrange(60, 180) / 60]
    elif direction == RIGHT:
        ball_vel = [-random.randrange(120, 240) / 60, -random.randrange(60, 180) / 60]

# define event handlers
def new_game():    
    reset_game()
    spawn_ball(random.choice([True, False]))

def reset_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    
    paddle1_pos = HEIGHT / 2 - HALF_PAD_HEIGHT
    paddle2_pos = HEIGHT / 2 - HALF_PAD_HEIGHT
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # determine whether paddle and ball collide   
    if (ball_pos[0] - BALL_RADIUS - PAD_WIDTH <= 0):
        if (ball_pos[1] >= (paddle1_pos - BALL_RADIUS) and ball_pos[1] <= (paddle1_pos + PAD_HEIGHT + BALL_RADIUS)):
            ball_vel[0] *= -1.1
            ball_vel[1] *= 1.1
        else:
            score2 += 1
            spawn_ball(LEFT)
    elif (ball_pos[0] + BALL_RADIUS + PAD_WIDTH >= WIDTH):
        if (ball_pos[1] >= (paddle2_pos - BALL_RADIUS) and ball_pos[1] <= (paddle2_pos + PAD_HEIGHT + BALL_RADIUS)):
            ball_vel[0] *= -1.1
            ball_vel[1] *= 1.1
        else:
            score1 += 1
            spawn_ball(RIGHT)
    
    if (ball_pos[1] - BALL_RADIUS <= 0) or (ball_pos[1] + BALL_RADIUS >= HEIGHT):
        ball_vel[1] *= -1
        
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS - 2, 2, "White", "Yellow")
    
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos += paddle1_vel
    paddle2_pos += paddle2_vel
    
    if paddle1_pos <= 0:
        paddle1_pos = 0
    
    if paddle1_pos >= HEIGHT - PAD_HEIGHT:
        paddle1_pos = HEIGHT - PAD_HEIGHT
    
    if paddle2_pos <= 0:
        paddle2_pos = 0
    
    if paddle2_pos >= HEIGHT - PAD_HEIGHT:
        paddle2_pos = HEIGHT - PAD_HEIGHT
        
    # draw paddles
    canvas.draw_polyline([(HALF_PAD_WIDTH, paddle1_pos), (HALF_PAD_WIDTH, paddle1_pos + PAD_HEIGHT)], PAD_WIDTH, 'Green')
    canvas.draw_polyline([(WIDTH - HALF_PAD_WIDTH, paddle2_pos), (WIDTH - HALF_PAD_WIDTH, paddle2_pos + PAD_HEIGHT)], PAD_WIDTH, 'Green')   
        
    # draw scores
    canvas.draw_text(str(score1),(250, 50), 24, "White")
    canvas.draw_text(str(score2),(337, 50), 24, "White")
        
def key_down(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = -PADDLE_SPEED
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = PADDLE_SPEED
    
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -PADDLE_SPEED
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = PADDLE_SPEED
   
def key_up(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
        
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0

def button_handler():
    new_game()
    
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)

# print labels
frame.add_label("Left paddle")
frame.add_label("W - Up")
frame.add_label("S - Down")
frame.add_label(" ")
frame.add_label("Right paddle")
frame.add_label("Up arrow - Up")
frame.add_label("Down arrow - Down")
frame.add_label(" ")

reset_button = frame.add_button('Reset Game', button_handler)

# start frame
new_game()
frame.start()
