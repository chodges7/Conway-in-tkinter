#!/usr/bin/python3.5
from tkinter import *
from random import randrange
from time import sleep
from math import floor

window_width = 540
window_height = 540
canvas_width = (window_width - 80) # 460
canvas_height = (window_height - 80) # 460

# #d4d4d4 = alive
# #2b2b2b = dead

class conway:
    def __init__(self, root):
        self.root = root
        self.root.title("Lab 11/12-Conway")
        self.root.geometry("{}x{}".format(window_width, window_height))

        # ----- variables -----
        self.color_dict = {0:"#d4d4d4", 1:"#2b2b2b",}
        self.array = [0] * 21
        for i in range(21):
            self.array[i] = [0] * 21

        # ----- buttons and lables -----
        self.label = Label(root, text="Welcome to the game")
        self.close_button = Button(root, text="Close", command=root.quit)
        self.change_button = Button(root, text="Randomize",
                                    command=self.change_color)

        # ----- define canvas and binds -----
        self.canvas = Canvas(root, bg="white", bd=0,
                             width=canvas_width,
                             height=canvas_height)
        self.canvas.bind("<Button-1>", self.click)

        # ----- make the lines and boxes in the canvas ------
        for i in range(21):
            self.canvas.create_line(22 * i, 0, 22 * i, 460)
            self.canvas.create_line(0, 22 * i, 460, 22 * i)
            for j in range(21):
                rng = randrange(100)
                if (rng < 15):
                    rand_color = self.color_dict[0]
                else:
                    rand_color = self.color_dict[1]
                self.id = self.canvas.create_rectangle(
                    22*j, 22*i,
                    22*(j+1), 22*(i+1),
                    fill=rand_color)
                self.array[i][j] = self.id


        # ----- Now let's configure the window -----
        self.label.pack()
        self.canvas.pack()
        self.change_button.pack(side=LEFT, expand=TRUE, fill=X)
        self.close_button.pack(side=LEFT, expand=TRUE, fill=X)

        # ----- Lastly we start the main loop -----
        self.root.after(0, self.draw)

    # ----- functions -----
    def draw(self):
        self.root.after(100, self.simulate)
        self.root.after(100, self.draw)

    def simulate(self):
        sim_arr = self.array
        for i in range(len(sim_arr)): # i == rows
            for j in range(len(sim_arr[i])): # j == cols
                i_plu = i + 1
                j_plu = j + 1
                i_min = i - 1
                j_min = j - 1

                # this is for wraparound:
                #   if we're at array[0][21] it's actually array[0][0]
                #   python deals with array[-1][-1] so we dont' worry about that
                if i_plu > 20:
                    i_plu = 0
                if j_plu > 20:
                    j_plu = 0

                # dictionary to count neighbors
                color_neigh = {}
                color_neigh["#d4d4d4"] = 0
                color_neigh["#2b2b2b"] = 0

                # dictionary to store array addresses of neighbors
                neighbors = {} # make a dict

                neighbors[NW] = (i_min,j_min)
                neighbors[N ] = (i_min,  j  )
                neighbors[NE] = (i_min,j_plu)
                neighbors[W ] = (  i  ,j_min)
                        # me  = (  i  ,  j  )
                neighbors[E ] = (  i  ,j_plu)
                neighbors[SW] = (i_plu,j_min)
                neighbors[S ] = (i_plu,  j  )
                neighbors[SE] = (i_plu,j_plu)

                # grab the fills for each neighbor
                for dir in neighbors.items():
                    x = dir[1][0] # x coordinate
                    y = dir[1][1] # y coordinate
                    ret = self.canvas.itemcget(sim_arr[x][y], 'fill')
                    color_neigh[ret] += 1

                total = color_neigh["#d4d4d4"]
                me = self.canvas.itemcget(sim_arr[i][j], 'fill')
                if me == "#d4d4d4": # new
                    # Any live cell with fewer than two live neighbours dies
                    if (total < 2):
                        self.canvas.itemconfigure(sim_arr[i][j], fill="#2b2b2b")
                    # Any live cell with more than three live neighbours dies
                    elif (total > 3):
                        self.canvas.itemconfigure(sim_arr[i][j], fill="#2b2b2b")
                elif me == "#2b2b2b": # normal
                    # Any dead cell with exactly three live neighbours becomes a live cell
                    if (total == 3):
                        self.canvas.itemconfigure(sim_arr[i][j], fill="#d4d4d4")

    def click(self, event):
        b = int(event.x / 22)
        a = int(event.y / 22)
        rect_id = self.array[a][b]
        self.canvas.itemconfigure(rect_id, fill="#d4d4d4")
        # this is how to use positional arguments on print
        print("array[%d][%d] at X:%d Y:%d"%(a, b, event.x, event.y))

    def change_color(self):
        cur_array = self.array
        for i in range(len(cur_array)):
            for j in range(len(cur_array)):
                rand_color = self.color_dict[randrange(2)]
                self.canvas.itemconfigure(cur_array[i][j], fill=rand_color)

    # https://www.geeksforgeeks.org/python-get-key-from-value-in-dictionary/
    def get_key(self, my_dict, val):
        for key, value in my_dict.items():
             if val == value:
                 return key
        return "key doesn't exist"

 # ---------- main ----------
root = Tk() # call root
my_gui = conway(root) # set the GUI
root.mainloop() # run the main loop
# print("stopping") # runs this when stopping
