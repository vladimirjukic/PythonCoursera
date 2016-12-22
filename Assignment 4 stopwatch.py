# template for "Stopwatch: The Game"
import simplegui

# define global variables
timer_counter = 0
timer_stops_total = 0
timer_stops_success = 0
timer_stop = True

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    tenth_sec = (t) % 10
    sec = int(t / 10) % 10
    minutes = int(t / 600) % 600
    ten_min = int(t / 100) % 6
    formated_text = str(minutes) + ":" + str(ten_min) + str(sec) + "." + str(tenth_sec)
    return formated_text
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_handler():
    global timer_stop
    timer_stop = False
    timer.start()

def stop_handler():
    global timer_stops_total, timer_stops_success, timer_stop

    if timer_stop == False:
        if timer_counter % 10 == 0 and timer_counter != 0:
            timer_stops_success += 1
            timer_stops_total += 1
        elif timer_counter != 0:
            timer_stops_total += 1
    
    timer_stop = True
    timer.stop()
        
def reset_handler():
    global timer_counter, timer_stops_total, timer_stops_success, timer_stop
    timer_counter = 0
    timer_stop = True
    timer_stops_total = 0
    timer_stops_success = 0
    timer.stop()

# define event handler for timer with 0.1 sec interval
def timer_handler():
    global timer_counter
    timer_counter = timer_counter + 1
    
# define draw handler
def draw(canvas):
    timer_text = format(timer_counter)
    canvas.draw_text(timer_text,[55,120],70,"White")
    canvas.draw_text(str(timer_stops_success)+'/'+str(timer_stops_total),[220,30],20,"White")
    
# create frame
frame = simplegui.create_frame("Stopwatch: The Game", 300, 200)
frame.set_draw_handler(draw)

# register event handlers
start_button = frame.add_button('Start', start_handler)
stop_button = frame.add_button('Stop', stop_handler)
reset_button = frame.add_button('Reset', reset_handler)
timer = simplegui.create_timer(100, timer_handler)

# start frame
frame.start()

# Please remember to review the grading rubric
