import random
import time
import tkinter as tk
import numpy as np
from ga import *

win = tk.Tk()
win.title('Funny Hack 2')
win.geometry('800x600')
win_x = 800
win_y = 600
tile_length = 20
tile_size = min(win_y,win_x)/tile_length
gen_amt = 100
mut_amt = 0.02
pop_amt = 25
plot_size = 150
gen = 0

member_rect = []
rects = []
gen_rects = []
pts = [[0],[0]]
#rects_updated = 0
delay = 2000


def color_from_val(val):
    if val == 0:
        return 'green'
    elif val == 1:
        return 'deepskyblue'
    elif val == 2:
        return 'goldenrod'
    return 'black'

def gen_sample_member():
    for y in range(tile_length):
        row = []
        for x in range(tile_length):
            row.append(random.randint(0,1))
        member_rect.append(row)


def init_canvas():
    global rects
    rects = []
    for y in range(tile_length):
        rectrow = []
        for x in range(tile_length):
            rect = cvs.create_rectangle(x*tile_size,y*tile_size,
            x*tile_size+tile_size,y*tile_size+tile_size,
            fill='gray',width=0)
            rectrow.append(rect)
        rects.append(rectrow) 
    cvs.update()

def init_plot():
    plot.delete('all')
    plot.create_line(0,plot_size,plot_size,plot_size,fill='white',width=5)
    plot.create_line(0,plot_size,0,0,fill='white',width=10)

def update_plot():

    init_plot()
    for i in range(len(pts[0])):
        if i > 0:
            plot.create_line(np.interp(pts[0][i-1],[min(pts[0]),max(pts[0])],[0,plot_size]),
            np.interp(pts[1][i-1],[min(pts[1]),max(pts[1])],[plot_size,0]),
            np.interp(pts[0][i],[min(pts[0]),max(pts[0])],[0,plot_size]),
            np.interp(pts[1][i],[min(pts[1]),max(pts[1])],[plot_size,0]),fill='white',width=2)

        
        

def queue_update(member):
    gen_rects.append(member.map)    
    for i,rect in enumerate(gen_rects):
        cvs.after(i*100,update_canvas,rect)
        
        #time.sleep(0.1)

def live_update(member):
    global delay
    cvs.after(delay,update_canvas,member.map)
    delay += 1

def update_canvas(member):
    global gen
    gen += 1
    for y in range(tile_length):
        for x in range(tile_length):
            cvs.itemconfig(rects[x][y],fill=color_from_val(member.map[x][y]))
    pts[0].append(gen)
    pts[1].append(member.fitness)
    update_plot()
    cvs.update()


cvs = tk.Canvas(win,bg='black',width=600,height=600)
cvs.pack(side=tk.LEFT)

init_canvas()


tk.Label(win, text="World size").pack()
tile_length_str = tk.StringVar()
tile_length_input=tk.Entry(win, width=10, textvariable=tile_length_str).pack()
tile_length_str.set(str(tile_length))

tk.Label(win, text="Mutation").pack()
mut_amt_str = tk.StringVar()
mut_amt_input=tk.Entry(win, width=10, textvariable=mut_amt_str).pack()
mut_amt_str.set(str(mut_amt))

tk.Label(win, text="Population per generation").pack()
pop_amt_str = tk.StringVar()
pop_amt_input=tk.Entry(win, width=10, textvariable=pop_amt_str).pack()
pop_amt_str.set(str(pop_amt))

tk.Label(win, text="Maximum generation").pack()
gen_amt_str = tk.StringVar()
gen_amt_input=tk.Entry(win, width=10,textvariable=gen_amt_str).pack()
gen_amt_str.set(str(gen_amt))


def start():
    global pts
    global gen
    gen = 0
    pts = [[],[]]
    startbtn['state'] = tk.DISABLED
    global delay
    delay = 1
    global tile_length
    global tile_size

    global gen_rects
    gen_rects = []

    tile_length = int(tile_length_str.get())
    tile_size = min(win_y,win_x)/tile_length

    init_canvas()

    mut_amt = float(mut_amt_str.get())
    pop_amt = int(pop_amt_str.get())
    gen_amt = int(gen_amt_str.get())
    g = ga(m_size=tile_length, mutation_rate=mut_amt,
    call_back=update_canvas,pop_size=pop_amt,gen_stop=gen_amt)

    final = g.start()
    update_canvas(final)
    startbtn['state'] = tk.NORMAL



startbtn = tk.Button(win,text='Start',command=start)
startbtn.pack()



plot = tk.Canvas(win,bg='black',width=150,height=150)
plot.pack(side=tk.BOTTOM)

init_plot()

tk.Label(win, text="Best Fitness\nover Generation").pack(side=tk.BOTTOM)

#win.grid_rowconfigure(0,weight=1)
#win.grid_columnconfigure(0,weight=2)
#win.grid_columnconfigure(1,weight=1)
win.mainloop()