#!/usr/bin/python3.5
print("chodges7-running_tkinter")
from tkinter import *
from random import randrange
from time import sleep
from math import floor

window_width = 530
window_height = 530
canvas_width = (window_width - 70) # 460
canvas_height = (window_height - 70) # 460

class conway:
    def __init__(self, root):
        self.root = root
        self.root.title("Lab 11/12-Conway")
        self.root.geometry("{}x{}".format(window_width, window_height))

        # ----- variables -----
        vcmd = root.register(self.validate) # we have to wrap the command
        self.entry = Entry(root, validate="key", validatecommand=(vcmd, '%P'))
        self.color_dict = {0:"red",
                           1:"dark green",
                           2:"green",
                           3:"light green",}
        # print(self.get_key(self.color_dict, "red")) # returns 0
        self.entered_number = 0

        self.array = [0] * 21
        for i in range(21):
            self.array[i] = [0] * 21

        # ----- buttons and lables -----
        self.runs = Label(root, text="Runs")
        self.label = Label(root, text="Welcome to the game")
        self.run_entry = Button(root, text="RUN", command=self.simulate)
        # self.greet_button = Button(root, text="Press me", command=self.greet)
        self.close_button = Button(root, text="Close", command=root.quit)
        self.change_button = Button(root, text="Change colors",
                                    command=self.change_color)

        # ----- define canvas and binds -----
        self.canvas = Canvas(root, bg="white", bd=0,
                             width=canvas_width,
                             height=canvas_height)
        self.canvas.bind("<Button-1>", self.click)
        # self.canvas.bind("<Double-1>", self.array_print)

        # ----- make the lines in the canvas ------
        for i in range(21):
            self.canvas.create_line(22 * i, 0, 22 * i, 460)
            self.canvas.create_line(0, 22 * i, 460, 22 * i)
            for j in range(21):
                rand_color = self.color_dict[randrange(4)]
                self.id = self.canvas.create_rectangle(
                    22*j, 22*i,
                    22*(j+1), 22*(i+1),
                    fill=rand_color)
                self.array[i][j] = self.id


        # ----- Now let's configure the window -----
        self.label.pack()
        self.canvas.pack()
        self.runs.pack(side=LEFT)
        self.entry.pack(side=LEFT, expand=TRUE)
        self.run_entry.pack(side=LEFT, expand=TRUE, fill=X)
        # self.greet_button.pack(side=LEFT, expand=TRUE, fill=X)
        self.change_button.pack(side=LEFT, expand=TRUE, fill=X)
        self.close_button.pack(side=LEFT, expand=TRUE, fill=X)
        # self.root.after(2000, self.draw)

    # ----- functions -----
    # def draw(self):
    #     self.root.after(2000, self.simulate)
    #     self.root.after(0, self.draw)

    def simulate(self):
        if self.entered_number == 0:
            self.entered_number = 1
        sim_arr = self.array
        # while(self.entered_number > 0):
        #     print(self.entered_number)
        #     self.entered_number -= 1
        total_reds = 0
        for i in range(len(sim_arr)):
            for j in range(len(sim_arr[i])):
                ret = self.canvas.itemcget(sim_arr[i][j], 'fill')
                if ret == "red":
                    total_reds += 1
        # print(total_reds)

        while (self.entered_number > 0):
            for i in range(len(sim_arr)): # i == rows
                for j in range(len(sim_arr[i])): # j == cols
                    i_plu = i + 1
                    j_plu = j + 1
                    i_min = i - 1
                    j_min = j - 1

                    if i_plu > 20:
                        i_plu = 0
                    if j_plu > 20:
                        j_plu = 0
                    # technically not needed since array[-1] works in python
                    # if i_min < 0:
                    #     i_min = 20
                    # if j_min < 0:
                    #     j_min = 20

                    color_neigh = {}
                    color_neigh["red"]         = 0
                    color_neigh["green"]       = 0
                    color_neigh["dark green"]  = 0
                    color_neigh["light green"] = 0

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
                        # print("array[{}][{}]\n".format(dir[1][0], dir[1][1]))
                        x = dir[1][0]
                        y = dir[1][1]
                        ret = self.canvas.itemcget(sim_arr[x][y], 'fill')
                        color_neigh[ret] += 1

                    rng = randrange(1, 101) # generate a number between 1 and 100
                    me = self.canvas.itemcget(sim_arr[i][j], 'fill')
                    if me == "dark green": # new
                        if (rng <= 5):
                            self.canvas.itemconfigure(self.array[i][j], fill="red")
                        elif (rng > 5 and rng <= 45):
                            self.canvas.itemconfigure(self.array[i][j], fill="green")
                    elif me == "green": # normal
                        if (rng <= 5):
                            self.canvas.itemconfigure(self.array[i][j], fill="light green")
                        elif (rng > 5 and rng <= 20):
                            self.canvas.itemconfigure(self.array[i][j], fill="dark green")
                        elif (rng > 20 and rng <= 40 and color_neigh["red"] > 0):
                            self.canvas.itemconfigure(self.array[i][j], fill="red")
                    elif me == "light green": # aged
                        if (rng <= 10):
                            self.canvas.itemconfigure(self.array[i][j], fill="red")
                    elif me == "red": # defective
                        per = floor((total_reds / 441) * 100)
                        if (rng <= per):
                            self.canvas.itemconfigure(self.array[i][j], fill="dark green")
                    else:
                        print("Something went wrong")
            sleep(.005)
            self.entered_number -= 1

        self.entry.delete(0, END)


    # def greet(self):
    #     a = randrange(21)
    #     b = randrange(21)
    #     self.random_id = self.array[a][b]
    #     self.canvas.itemconfigure(self.random_id, fill="red")
    #     print("User pressed the button")

    def click(self, event):
        b = int(event.x / 22)
        a = int(event.y / 22)
        rect_id = self.array[b][a]
        for i in range(-1,2):
            y = b + i
            if (y > 20):
                y = 0

            x = a + 1
            if (x > 20):
                x = 0

            top_rect = self.array[x - 2][y]
            mid_rect = self.array[x - 1][y]
            bot_rect = self.array[  x  ][y]
            self.canvas.itemconfigure(top_rect, fill="red")
            self.canvas.itemconfigure(mid_rect, fill="red")
            self.canvas.itemconfigure(bot_rect, fill="red")
        # this is how to use positional arguments on print
        print("array[%d][%d] at X:%d Y:%d"%(a, b, event.x, event.y))

    # def array_print(self, event):
    #     cur_array = self.array
    #     for i in range(len(cur_array)):
    #         for j in range(len(cur_array[i])):
    #             print(" {} ".format(cur_array[i][j]), end="")
    #         print("")

    def change_color(self):
        cur_array = self.array
        for i in range(len(cur_array)):
            for j in range(len(cur_array)):
                rand_color = self.color_dict[randrange(4)]
                self.canvas.itemconfigure(cur_array[i][j], fill=rand_color)

    def validate(self, new_text):
        if not new_text: # the field is being cleared
            self.entered_number = 0
            return True

        try:
            self.entered_number = int(new_text)
            # print(self.entered_number)
            return True
        except ValueError:
            return False


    # https://www.geeksforgeeks.org/python-get-key-from-value-in-dictionary/
    def get_key(self, my_dict, val):
        for key, value in my_dict.items():
             if val == value:
                 return key

        return "key doesn't exist"


root = Tk() # call root
my_gui = conway(root) # set the GUI
root.mainloop() # run the main loop
print("stopping") # runs this when stopping


# itemcget
