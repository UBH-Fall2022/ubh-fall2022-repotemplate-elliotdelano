import random
import time
import tkinter as tk
from ga import *

win = tk.Tk()
win.title('Funny Hack 2')
win.geometry('800x600')
win_x = 1000
win_y = 600
tile_length = 40
tile_size = min(win_y,win_x)/tile_length
gen_amt = 100


member_rect = []
rects = []
gen_rects = []
#rects_updated = 0

def start_ga():
    print('hi')

def color_from_val(val):
    match val:
        case 0:
            return 'green'
        case 1:
            return 'blue'
        case _:
            return 'black'

def gen_sample_member():
    for y in range(tile_length):
        row = []
        for x in range(tile_length):
            row.append(random.randint(0,1))
        member_rect.append(row)


def init_canvas():
    for y in range(tile_length):
        rectrow = []
        for x in range(tile_length):
            rect = cvs.create_rectangle(x*tile_size,y*tile_size,
            x*tile_size+tile_size,y*tile_size+tile_size,
            fill='gray',width=0)
            rectrow.append(rect)
        rects.append(rectrow) 

def queue_update(member):
    gen_rects.append(member.map)
    if len(gen_rects) == gen_amt:
        for i,rect in enumerate(gen_rects):
            cvs.after(i*100,update_canvas,rect)
            
            #time.sleep(0.1)


def update_canvas(member):
    for y in range(tile_length):
        for x in range(tile_length):
            cvs.itemconfig(rects[x][y],fill=color_from_val(member[x][y]))
    print('hi')
        #rects[x][y].fill = color_from_val(member_rect[x][y])
    #print(rects)
    #print(member.map)
    #time.sleep(0.1)
       


cvs = tk.Canvas(win,bg='black',width=600,height=600)
cvs.grid(column=0,row=0,sticky='new')

init_canvas()
gen_sample_member()    



def start():
    g = ga(m_size=tile_length, mutation_rate=0.01,call_back=queue_update,pop_size=50,gen_stop=gen_amt)
    final = g.start()
    queue_update(final)

startbtn = tk.Button(win,text='Start',command=start)
startbtn.grid(column=4,row=0,sticky='e')

#win.grid_rowconfigure(0,weight=1)
#win.grid_columnconfigure(0,weight=2)
#win.grid_columnconfigure(1,weight=1)
win.mainloop()