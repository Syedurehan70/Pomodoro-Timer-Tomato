from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None


# ---------------------------- TIMER RESET ------------------------------- # 
def reset_time():
    global reps

    # after resetting everything start button will be available to use again
    start_button.config(state="normal")
    reset_button.config(state="disabled")

    # cancels the timer we sets up earlier, timer will stop
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    timer_label.config(text="Timer")
    check_label.config(text="")
    reps = 0


# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global reps
    global timer_label

    # in this way start button will not work after first press, prevents the abnormal looping of count down
    start_button.config(state="disabled")
    reset_button.config(state="normal")
    reps += 1
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    # func call, multiplying to make it a min interval
    if reps % 2 == 0:  # if reps are 2,4,6
        timer_label.config(text="BREAK", fg=PINK)

        # will make the window pop on top of all tabs when it's break time
        window.attributes('-topmost', 1)
        count_down(short_break_sec)
    elif reps % 8 == 0:
        timer_label.config(text="BREAK", fg=RED)
        window.attributes('-topmost', 1)
        count_down(long_break_sec)
    elif reps % 9 == 0:
        window.destroy()
    else:
        timer_label.config(text="WORK", fg=GREEN)
        count_down(work_sec)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count):

    # returns the remaining minutes, math.floor returns the largest int from the num if 4.8 than 4 returns
    count_min = math.floor(count / 60)

    # returns the remaining secs
    count_sec = count % 60

    # Dynamic typing, we're using int to display the string
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    # it's going to make update inside the canvas, and 1st arguments specifies the part needs to be modifies
    canvas.itemconfig(timer_text, text=f"{count_min}.{count_sec}")
    if count > 0:
        global timer

        # so 1 sec delay cuz of after attribute, count_down func will be recalled with modified value of count
        timer = window.after(1000, count_down, count - 1)
    else:  # when it's equals  to zero
        start_timer()
        marks = ""
        work_sessions = math.floor(reps/2)
        for _ in range(work_sessions):
            marks += "✅"
        check_label.config(text=marks)


# ---------------------------- UI SETUP ------------------------------- #
# Window
window = Tk()
window.title("Pomodoro Timer")
window.config(padx=100, pady=50, bg=YELLOW)

# Label
timer_label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 30, "bold"))
timer_label.grid(row=0, column=1)

# we want it to start empty
check_label = Label(fg=RED, bg=YELLOW)
check_label.grid(row=3, column=1)

# Buttons, normal will make start button work in beginning
start_button = Button(text="Start", command=start_timer, highlightthickness=0, state="normal")
start_button.grid(row=2, column=0)

# reset button is disabled in the beginning
reset_button = Button(text= "Reset", highlightthickness=0, command=reset_time, state="disabled")
reset_button.grid(row=2, column=2)

# Canvas

# putting picture on screen, canvas is part only where pic is displayed it's not the whole screen
canvas = Canvas(width=200, height=223, bg=YELLOW, highlightthickness=0)

# below command reads the picture file
tomato_img = PhotoImage(file="tomato.png")

# below command defines the coordinates of image on screen
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(103, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(row=1, column=1)

window.mainloop()
