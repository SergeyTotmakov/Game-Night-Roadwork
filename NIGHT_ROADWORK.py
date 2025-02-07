import tkinter
import random
from threading import Timer

master = tkinter.Tk()
canvas = tkinter.Canvas(master, bg='black', height=750, width=750)
master.configure(bg='black')

dead_cells = []
flash_in_hand = 0
realcoords = [13,13]
ax_prev = 0
ay_prev = 0
ax = 0
ay = 0
ax_hatch = 0
ay_hatch = 0
counter = 0
holes = []
lightners_coords = []
hatches_count = 1
score = 0
ax_choice = [max(realcoords[0] - 1, 1), min(realcoords[0] + 1, 25)]
ay_choice = [max(realcoords[1] - 1, 1), min(realcoords[1] + 1, 25)]
f = open('RECORD.txt', 'r+')
best = int(f.read())
f.close()
cur_col = 'red'
hatch_limit = 2
flashed_cells = []
hatches_coords = []
hatches = []

def key_pressed(event):
    global dead_cells
    global flash_in_hand
    global score
    global realcoords
    global ax_choice
    global ay_choice
    global lightners_coords
    global hatches_count
    global flashed_cells
    global cur_col
    t = canvas.coords(circle)
    if event.keysym == 'w' or event.keysym == '2':
        if t[1] > 30:
            canvas.move(circle, 0, -30)
            canvas.move(flashlx, 0, -30)
            realcoords[1] -= 1
            ay_choice = [max(realcoords[1] - 1, 1), min(realcoords[1] + 1, 25)]
    if event.keysym == 'x' or event.keysym == '8':
        if t[1] < 720:
            canvas.move(circle, 0, 30)
            canvas.move(flashlx, 0, 30)
            realcoords[1] += 1
            ay_choice = [max(realcoords[1] - 1, 1), min(realcoords[1] + 1, 25)]
    if event.keysym == 'a' or event.keysym == '4':
        if t[0] > 30:
            canvas.move(circle, -30, 0)
            canvas.move(flashlx, -30, 0)
            realcoords[0] -= 1
            ax_choice = [max(realcoords[0] - 1, 1), min(realcoords[0] + 1, 25)]
    if event.keysym == 'd' or event.keysym == '6':
        if t[0] < 720:
            canvas.move(circle, 30, 0)
            canvas.move(flashlx, 30, 0)
            realcoords[0] += 1
            ax_choice = [max(realcoords[0] - 1, 1), min(realcoords[0] + 1, 25)]
    if event.keysym == 's' or event.keysym == '5':
        if flash_in_hand == 0 and realcoords not in lightners_coords:
            flash_in_hand = 1
            canvas.itemconfig(flashlx, fill='orange', outline='orange')
            lightners_coords.append([realcoords[0], realcoords[1]])
            if (realcoords[0] + realcoords[1]) % 2 == 1 and realcoords not in flashed_cells:
                cur_col = 'grey10'
            elif (realcoords[0] + realcoords[1]) % 2 == 0 and realcoords not in flashed_cells:
                cur_col = 'black'
            else:
                cur_col = '#440'
            canvas.create_rectangle(realcoords[0] * 30 - 30, realcoords[1] * 30 - 30, realcoords[0] * 30, realcoords[1] * 30, fill=cur_col, outline='red')
            for nk in hatches_coords:
                if nk in lightners_coords:
                    canvas.create_rectangle(nk[0] * 30 - 27, nk[1] * 30 - 18, nk[0] * 30 - 3, nk[1] * 30 - 12, fill='red', outline='red')
                    canvas.create_rectangle(nk[0] * 30 - 18, nk[1] * 30 - 27, nk[0] * 30 - 12, nk[1] * 30 - 3, fill='red', outline='red')
            canvas.tag_raise(circle)
            canvas.tag_raise(flashlx)
            kill_cell_flash()
        elif flash_in_hand == 1:
            canvas.create_rectangle(realcoords[0] * 30 - 29, realcoords[1] * 30 - 29, realcoords[0] * 30 - 1, realcoords[1] * 30 - 1, fill='#440', outline='#440')
            canvas.create_rectangle((realcoords[0] - 1) * 30 - 29, (realcoords[1]) * 30 - 29, (realcoords[0] - 1) * 30 - 1, (realcoords[1]) * 30 - 1, fill='#440', outline='#440')
            canvas.create_rectangle((realcoords[0]) * 30 - 29, (realcoords[1] - 1) * 30 - 29, (realcoords[0]) * 30 - 1, (realcoords[1] - 1) * 30 - 1, fill='#440', outline='#440')
            canvas.create_rectangle((realcoords[0]) * 30 - 29, (realcoords[1] + 1) * 30 - 29, (realcoords[0]) * 30 - 1, (realcoords[1] + 1) * 30 - 1, fill='#440', outline='#440')
            canvas.create_rectangle((realcoords[0] + 1) * 30 - 29, (realcoords[1]) * 30 - 29, (realcoords[0] + 1) * 30 - 1, (realcoords[1]) * 30 - 1, fill='#440', outline='#440')
            flashed_cells.append([realcoords[0], realcoords[1]])
            flashed_cells.append([realcoords[0] - 1, realcoords[1]])
            flashed_cells.append([realcoords[0] + 1, realcoords[1]])
            flashed_cells.append([realcoords[0], realcoords[1] - 1])
            flashed_cells.append([realcoords[0], realcoords[1] + 1])
            for nk in hatches_coords:
                if nk in flashed_cells:
                    canvas.create_rectangle(nk[0] * 30 - 27, nk[1] * 30 - 18, nk[0] * 30 - 3, nk[1] * 30 - 12, fill='red', outline='red')
                    canvas.create_rectangle(nk[0] * 30 - 18, nk[1] * 30 - 27, nk[0] * 30 - 12, nk[1] * 30 - 3, fill='red', outline='red')
            for h in holes:
                canvas.tag_raise(h)
            flash_in_hand = 0
            canvas.tag_raise(circle)
            canvas.tag_raise(flashlx)
            canvas.itemconfig(flashlx, fill='lightblue', outline='lightblue')
    if event.keysym == 'z' or event.keysym == '7':
        if realcoords in hatches_coords:
            hatches_count -= 1
            score += 1
            hatches_coords.remove(realcoords)
            label_4.configure(text=str(score))
            if (realcoords[0] + realcoords[1]) % 2 == 1 and realcoords not in flashed_cells:
                cur_col = 'grey10'
            elif (realcoords[0] + realcoords[1]) % 2 == 0 and realcoords not in flashed_cells:
                cur_col = 'black'
            else:
                cur_col = '#440'
            canvas.create_rectangle(realcoords[0] * 30 - 27, realcoords[1] * 30 - 18, realcoords[0] * 30 - 3, realcoords[1] * 30 - 12, fill=cur_col, outline=cur_col)
            canvas.create_rectangle(realcoords[0] * 30 - 18, realcoords[1] * 30 - 27, realcoords[0] * 30 - 12, realcoords[1] * 30 - 3, fill=cur_col, outline=cur_col)
            canvas.tag_raise(circle)
            canvas.tag_raise(circle)
            canvas.tag_raise(flashlx)
   
def repeat(seconds, action, *args):
    global best
    if realcoords not in dead_cells:
        Timer(seconds, repeat, [seconds, action] + list(args)).start()
        action(*args)
    else:
        Timer(seconds, repeat, [seconds, action] + list(args)).cancel()
        action(*args)
        if score > best:
            best = score
            f = open('RECORD.txt', 'w')
            f.write(str(best))
            f.close()

def death_check():
    if realcoords in dead_cells:
        canvas.destroy()
        btn_increase.destroy()
        btn_endgame.configure(state='disabled')

def kill_cell():
    global cur_col
    global dead_cells
    global ax
    global ay
    global ax_prev
    global ay_prev
    ax = random.randint(max(realcoords[0] - 3, 1), min(realcoords[0] + 3, 25))
    ay = random.randint(max(realcoords[1] - 3, 1), min(realcoords[1] + 3, 25))
    if (ax_prev + ay_prev) % 2 == 0:
        cur_col = 'black'
    else:
        cur_col = 'grey10'
    if [ax_prev, ay_prev] not in dead_cells and [ax_prev, ay_prev] not in hatches_coords:
        dead_cells.append([ax_prev, ay_prev])
        hole = canvas.create_oval(ax_prev * 30 - 27, ay_prev * 30 - 27, ax_prev * 30 - 3, ay_prev * 30 - 3, fill=cur_col, outline=cur_col)
        holes.append(hole)
    ax_prev = ax
    ay_prev = ay
    
def kill_cell_flash():
    global dead_cells
    global ax
    global ay
    global cur_col
    ax = random.choice(ax_choice)
    ay = random.choice(ay_choice)
    if (ax + ay) % 2 == 0:
        cur_col = 'black'
    else:
        cur_col = 'grey10'
    if [ax, ay] not in dead_cells:
        dead_cells.append([ax, ay])
        hole = canvas.create_oval(ax * 30 - 27, ay * 30 - 27, ax * 30 - 3, ay * 30 - 3, fill=cur_col, outline=cur_col)
        holes.append(hole)
        
def hatch_spawn():
    global ax_hatch
    global ay_hatch
    global hatches_count
    global hatches_coords
    global hatches
    if hatches_count <= hatch_limit:
        ax_hatch = random.randint(2,24)
        ay_hatch = random.randint(2,24)
        if [ax_hatch, ay_hatch] not in dead_cells and [ax_hatch, ay_hatch] not in hatches_coords:
            hatch_1 = canvas.create_rectangle(ax_hatch * 30 - 27, ay_hatch * 30 - 18, ax_hatch * 30 - 3, ay_hatch * 30 - 12, fill='red', outline='red')
            hatch_2 = canvas.create_rectangle(ax_hatch * 30 - 18, ay_hatch * 30 - 27, ax_hatch * 30 - 12, ay_hatch * 30 - 3, fill='red', outline='red')
            hatches.append(hatch_1)
            hatches.append(hatch_2)
            hatches_count += 1
            hatches_coords.append([ax_hatch, ay_hatch])
            canvas.tag_raise(circle)
            canvas.tag_raise(flashlx)

def surv_time():
    global counter
    counter += 1

def endgame():
    global realcoords
    global dead_cells
    realcoords = [1,1]
    dead_cells.append([1,1])
    btn_endgame.configure(state='disabled')
    btn_increase.destroy()
                          
def rus():
    btn_endgame.configure(text='ЗАВЕРШИТЬ ИГРУ')
    btn_increase.configure(text='УВЕЛИЧИТЬ КОЛИЧЕСТВО КРЕСТИКОВ НА ДОСКЕ')
    label_1.configure(text='Лучший счет: ')
    label_3.configure(text='Текущий счет: ')

def eng():
    btn_endgame.configure(text='END GAME')
    btn_increase.configure(text='INCREASE THE NUMBER OF CROSSES ON THE BOARD')
    label_1.configure(text='Best score: ')
    label_3.configure(text='Current score: ')

def danger():
    if [ax, ay] in flashed_cells and [ax, ay] not in dead_cells:
        canvas.create_rectangle(ax * 30 - 29, ay * 30 - 29, ax * 30 - 1, ay * 30  - 1, fill='#600', outline='#600')
        for h in holes:
            canvas.tag_raise(h)
        canvas.tag_raise(circle)
    
def increase():
    global hatch_limit
    global counter
    hatch_limit += 1
    counter = 0

def increase_enabling():
    if counter >= 20:
        btn_increase.configure(state='active')
    else:
        btn_increase.configure(state='disabled')

repeat(4, kill_cell)
repeat(4, danger)
repeat(0.01, death_check)
repeat(0.01, danger)

for b in range(25):
    for c in range(25):
        if (b + c) % 2 == 1:
            canvas.create_rectangle(b * 30, c * 30, b * 30 + 30, c * 30 + 30, fill='grey10', outline='grey10')
    
circle = canvas.create_oval((365, 365), (385, 385), fill='lightblue', outline='white')
flashlx = canvas.create_oval((370, 370), (380, 380), fill='lightblue', outline='lightblue')

master.bind("<KeyPress>", key_pressed)

btn_endgame = tkinter.Button(text='ЗАВЕРШИТЬ ИГРУ', anchor='n', fg='red', command = endgame, state = 'active')
btn_endgame.grid(row=0, columnspan=2, sticky='nsew')
btn_rus = tkinter.Button(text='ЯЗЫК: РУССКИЙ', anchor='n', command = rus, state = 'active')
btn_rus.grid(row=1, column=0, sticky='nsew')
btn_eng = tkinter.Button(text='LANGUAGE: ENGLISH', anchor='n', command = eng, state = 'active')
btn_eng.grid(row=1, column=1, sticky='nsew')
btn_increase = tkinter.Button(text='УВЕЛИЧИТЬ КОЛИЧЕСТВО КРЕСТИКОВ НА ДОСКЕ', anchor='n', bg='black', command = increase, state = 'disabled')
btn_increase.grid(row=2, columnspan=2, sticky='nsew')
label_1 = tkinter.Label(text='Лучший счет: ', bg = 'black', fg = 'white')
label_1.grid(row=3, column=0)
label_2 = tkinter.Label(text=str(best), bg = 'black', fg = 'white')
label_2.grid(row=3, column=1)
label_3 = tkinter.Label(text='Текущий счет: ', bg = 'black', fg = 'white')
label_3.grid(row=4, column=0)
label_4 = tkinter.Label(text='0', bg = 'black', fg = 'white')
label_4.grid(row=4, column=1)

repeat(1, surv_time)
repeat(1, increase_enabling)
repeat(5, hatch_spawn)

canvas.grid(row=5, columnspan=2)
master.mainloop()
