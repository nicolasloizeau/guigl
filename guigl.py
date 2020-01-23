from tkinter import *
from itertools import product
import copy
from blocks import*

# tkinter frames
master = Tk()
master.title("Guigl")
leftframe = Frame(master)
leftframe.pack(side=LEFT)
rightframe = Frame(master)
rightframe.pack(side=RIGHT)
topframe = Frame(rightframe)
topframe.pack(side=TOP)



def draw_block(canvas, block):
    """draw a block on a canvas"""
    for i,j in block.shape:
        canvas.create_rectangle(i*cell_size, j*cell_size,(i+1)*cell_size, (j+1)*cell_size, fill=colors[block.id], tags=(i,j))


def draw_edges(canvas, block, transfo):
    """draw the block edges on a canvas"""
    i = block.position[0]
    j = block.position[1]
    for edge in block.edges:
        i2,j2 = i+edge[0][0], j+edge[0][1]
        i3,j3 = i+edge[1][0], j+edge[1][1]
        i2,j2 = transfo(i2+0.5,j2+0.5)
        i3,j3 = transfo(i3+0.5,j3+0.5)
        canvas.create_line(i2, j2, i3, j3, width=2)


def draw_output(canvas, i, j, side, transfo):
    i2,j2 = transfo(i+0.5,j+0.5)
    if side == "up":
        i3,j3 = transfo(i+0.5,j)
    if side == "down":
        i3,j3 = transfo(i+0.5,j+1)
    if side == "right":
        i3,j3 = transfo(i+1,j+0.5)
    if side == "left":
        i3,j3 = transfo(i,j+0.5)
    canvas.create_line(i2, j2, i3, j3, arrow=LAST, width=2)

def draw_input(canvas, i, j, side, transfo):
    i2,j2 = transfo(i+0.5,j+0.5)
    if side == "up":
        i3,j3 = transfo(i+0.5,j)
    if side == "down":
        i3,j3 = transfo(i+0.5,j+1)
    if side == "right":
        i3,j3 = transfo(i+1,j+0.5)
    if side == "left":
        i3,j3 = transfo(i,j+0.5)
    canvas.create_line(i3, j3, i2, j2, arrow=LAST, width=2)


def draw_arrows(canvas, block, transfo):
    i = block.position[0]
    j = block.position[1]
    for input_ in block.inputs:
        draw_input(canvas, input_[0]+i, input_[1]+j, input_[2], transfo)
    for output in block.outputs:
        draw_output(canvas, output[0]+i, output[1]+j, output[2], transfo)



active_block = IntVar()

# delete button
Radiobutton(leftframe, text="delete", variable=active_block, value=-1,
width=7, height=5, indicatoron=0).grid(row=0, column=0)

cell_size = 30

def transfo(i,j):
    return i*cell_size, j*cell_size

canvas_size = cell_size*3

# make the blocks bar
ncol2 = 0
ncol1 = 0
ncol0 = 1
for id, block in enumerate(blocks):
    if block.name == "angle":
        col = 1
        line = ncol1
        ncol1 += 1
    elif block.name in ["wire", "cross", "branch"]:
        col = 2
        line = ncol2
        ncol2 += 1
    else:
        col = 0
        line = ncol0
        ncol0 += 1
    Radiobutton(leftframe, text=block.name, variable=active_block, value=block.id,
    width=7, height=5, indicatoron=0).grid(row=line, column=col*2)
    canvas = Canvas(leftframe, width=canvas_size, height=canvas_size)
    canvas.grid(row=line, column=col*2+1)
    draw_block(canvas, block)
    draw_edges(canvas, block, transfo)
    draw_arrows(canvas, block, transfo)
    canvas.create_oval(0, 0, 0.3*cell_size, 0.3*cell_size, fill="white")




class working_grid:
    def __init__(self, window):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        self.N = 1000
        self.color_grid = [[-1 for i in range(self.N)] for j in range(self.N)]
        self.canvas_w = int(screen_width*0.8)
        self.canvas_h = int(screen_height*0.8)
        self.canvas = Canvas(rightframe, width=self.canvas_w, height=self.canvas_h)
        self.cell_size = 50
        self.blocks = []
        self.occupied = []
        self.pos = [0,0]

        Button(topframe, text="+", command=self.zoomin).grid(row=1, column=1)
        Button(topframe, text="-", command=self.zoomout).grid(row=1, column=2)
        Button(topframe, text=u"\u25B2", command=self.down).grid(row=0, column=4)
        Button(topframe, text=u"\u25BC", command=self.up).grid(row=2, column=4)
        Button(topframe, text=u"\u25B6", command=self.left).grid(row=1, column=5)
        Button(topframe, text=u"\u25C0", command=self.right).grid(row=1, column=3)
        Button(topframe, text="clear all", command=self.clear).grid(row=1, column=8)


    def imax(self):
        return self.canvas_w/self.cell_size
    def jmax(self):
        return self.canvas_h/self.cell_size

    def create_grid(self):
        if self.cell_size > 20:
            for i in range(0,self.canvas_h,int(self.cell_size)):
                self.canvas.create_line(0, i, self.canvas_w, i, fill="black")
            for i in range(0,self.canvas_w,int(self.cell_size)):
                self.canvas.create_line(i, 0, i, self.canvas_h, fill="black")

    def update(self):
        self.canvas.pack()
        self.canvas.delete("all")
        self.create_grid()
        self.fill_cells()
        if self.cell_size > 20:
            self.draw_arrows()
            self.draw_edges()
        self.save()


    def allowed(self, block):
        i, j = block.position
        for k, l in block.shape:
            if (i+k, j+l) in self.occupied:
                return False
        return True


    def add_block(self, id, i, j):
        block = copy.deepcopy(blocks[id])
        block.position = (i,j)
        if not self.allowed(block):
            return 1
        self.blocks.append(block)
        for k, l in block.shape:
            self.color_grid[i+k][j+l] = block.id
            self.occupied.append((i+k, j+l))
        self.update()

    def get_block(self, i,j):
        for block in self.blocks:
            i2, j2 = block.position
            for cell in block.shape:
                if cell == [i-i2,j-j2]:
                    return block
        return -1

    def remove_block(self, i, j):
        shape = []
        block = self.get_block(i,j)
        if block != -1:
            i2, j2 = block.position
            for k, l in block.shape:
                self.color_grid[i2+k][j2+l] = -1
                self.occupied.remove((i2+k, j2+l))
            self.blocks.remove(block)
            self.update()

    def clear(self):
        self.color_grid = [[-1 for i in range(self.N)] for j in range(self.N)]
        self.blocks = []
        self.occupied = []
        self.update()

    def fill_cells(self):
        rangei = range(int(self.pos[0]), int(self.pos[0])+int(self.imax()))
        rangej = range(int(self.pos[1]), int(self.pos[1])+int(self.jmax()))
        for i, j in product(rangei, rangej):
            if (i,j) in self.occupied or self.cell_size > 10:
                color = colors[self.color_grid[i][j]]
                i2 = i-int(self.pos[0])
                j2 = j-int(self.pos[1])
                cell_size = int(self.cell_size)
                rectangle = self.canvas.create_rectangle(i2*cell_size, j2*cell_size,
                (i2+1)*cell_size, (j2+1)*cell_size, fill=color, tags=(i,j))
                self.canvas.tag_bind(rectangle, '<ButtonPress-1>', self.click)


    def grid2rep(self, i, j):
        i2 = (i-int(self.pos[0]))*self.cell_size
        j2 = (j-int(self.pos[1]))*self.cell_size
        return i2, j2
    def rep2grid(self, i, j):
        return j, i


    def click(self, event):
        tags = self.canvas.gettags(event.widget.find_withtag('current'))
        i, j = int(tags[0]), int(tags[1])
        if active_block.get() == -1:
            self.remove_block(i, j)
        else:
            self.add_block(active_block.get(), i, j)

    def zoomout(self):
        if self.cell_size > 4:
            self.cell_size = self.cell_size/2
            self.pos[0] -= self.imax()/4
            self.pos[1] -= self.jmax()/4
            self.update()

    def zoomin(self):
        if self.cell_size < 500:
            self.cell_size = self.cell_size*2
            self.pos[0] += self.imax()/2
            self.pos[1] += self.jmax()/2
            self.update()

    def up(self):
        self.pos[1] += 50./self.cell_size
        self.update()
    def down(self):
        self.pos[1] -= 50./self.cell_size
        self.update()
    def right(self):
        self.pos[0] -= 50./self.cell_size
        self.update()
    def left(self):
        self.pos[0] += 50./self.cell_size
        self.update()

    def draw_edges(self):
        for block in self.blocks:
            draw_edges(self.canvas, block, self.grid2rep)
    def draw_arrows(self):
        for block in self.blocks:
            draw_arrows(self.canvas, block, self.grid2rep)

    def save(self):
        lines = ""
        for block in self.blocks:
            lines += "{} {} {}\n".format(block.fname, *block.position)
        file = open("blocks.txt","w")
        file.write(lines)
        file.close()

grid = working_grid(master)

grid.update()
mainloop()
