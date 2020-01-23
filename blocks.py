
# the blocks are defined here

def clamp(val, minimum=0, maximum=255):
    if val < minimum:
        return minimum
    if val > maximum:
        return maximum
    return val

def colorscale(hexstr, scalefactor):
    hexstr = hexstr.strip('#')
    if scalefactor < 0 or len(hexstr) != 6:
        return hexstr
    r, g, b = int(hexstr[:2], 16), int(hexstr[2:4], 16), int(hexstr[4:], 16)
    r = int(clamp(r * scalefactor))
    g = int(clamp(g * scalefactor))
    b = int(clamp(b * scalefactor))
    return "#%02x%02x%02x" % (r, g, b)

colors = {-1:"white"}



class Block:
    def __init__(self, name, shape=[[0,0]], color="grey", inputs=[],
    outputs=[], edges=[], fname="", id=0):
        if fname == "":
            self.fname = name
        else:
            self.fname = fname
        self.name = name
        self.shape = shape
        self.color = color
        self.position = (0,0)
        self.inputs = inputs
        self.outputs = outputs
        self.edges = edges
        self.id = id
        colors[id] = self.color



N = 0
blocks = []




#gun
outputs =  [[0,0,"right"]]
blocks.append(Block("gun", outputs=outputs, id=N))
N += 1

#eater
inputs =  [[0,0,"left"],[0,0,"right"],[0,0,"up"],[0,0,"down"]]
blocks.append(Block("eater", inputs=inputs, id=N))
N += 1


cf = 1.2
#and
inputs = [[0,0,"left"]]
outputs =  [[1,0,"right"]]
edges = [[[0,0],[1,0]]]
shape = [[0,0], [0,1], [1,0], [1,1]]
blocks.append(Block("NOT", shape=shape, inputs=inputs, outputs=outputs, edges=edges,
id=N, color=colorscale("#1f77b4", cf)))
N += 1

#or
inputs = [[0,0,"left"], [0,1,"left"]]
outputs =  [[1,1,"right"]]
edges = [[[0,0],[1,1]],[[0,1],[1,1]]]
shape = [[0,0], [0,1], [0,2], [1,0], [1,1]]
blocks.append(Block("OR", shape=shape, inputs=inputs, outputs=outputs, edges=edges,
id=N, color=colorscale("#ff7f0e", cf)))
N += 1


#and
inputs = [[0,0,"left"], [0,1,"left"]]
outputs =  [[1,1,"right"]]
edges = [[[0,0],[1,1]],[[0,1],[1,1]]]
shape = [[0,0], [0,1], [1,0], [1,1]]
blocks.append(Block("AND", shape=shape, inputs=inputs, outputs=outputs, edges=edges,
id=N, color=colorscale("#2ca02c", cf)))
N += 1
#nor
inputs = [[0,0,"left"], [0,1,"left"]]
outputs =  [[1,2,"right"]]
edges = [[[0,0],[1,2]],[[0,1],[1,2]]]
shape = [[0,0], [0,1], [1,0], [1,1], [1,2]]
blocks.append(Block("NOR", shape=shape, inputs=inputs, outputs=outputs, edges=edges,
id=N, color=colorscale("#d62728", cf)))
N += 1

#NOT A AND B
inputs = [[0,0,"left"], [0,1,"left"]]
outputs =  [[0,1,"right"]]
edges = [[[0,0],[0,1]]]
shape = [[0,0], [0,1]]
blocks.append(Block("(NOT a) \n AND b", shape=shape, inputs=inputs, outputs=outputs, edges=edges,
id=N, color=colorscale("#9467bd", cf), fname="NOTaANDb"))
N += 1

#branch
inputs = [[0,1,"left"]]
outputs =  [[1,0,"right"], [1,2,"right"]]
edges = [[[0,1],[1,0]],[[0,1], [1,2]]]
shape = [[0,0], [0,1], [1,0], [1,1], [1,2]]
blocks.append(Block("branch", shape=shape, inputs=inputs, outputs=outputs,
edges=edges, fname="branch", id=N))
N += 1

#cross
inputs = [[0,0,"left"], [0,1,"left"]]
outputs =  [[0,1,"right"], [0,2,"right"]]
edges = [[[0,0],[0,1]],[[0,1], [0,2]]]
shape = [[0,0], [0,1], [0,2]]
blocks.append(Block("cross", shape=shape, inputs=inputs, outputs=outputs,
edges=edges, fname="cross", id=N))
N += 1

#cross
inputs = [[0,0,"left"], [0,1,"down"]]
outputs =  [[1,0,"right"], [0,0,"up"]]
edges = [[[0,0],[1,0]],[[0,1], [0,0]]]
shape = [[0,0], [0,1], [1,0], [1,1]]
blocks.append(Block("cross", shape=shape, inputs=inputs, outputs=outputs,
edges=edges, fname="cross2", id=N))
N += 1

#cross
inputs = [[0,0,"left"], [1,0,"up"]]
outputs =  [[1,0,"right"], [1,1,"down"]]
edges = [[[0,0],[1,0]],[[1,0], [1,1]]]
shape = [[0,0], [0,1], [1,0], [1,1]]
blocks.append(Block("cross", shape=shape, inputs=inputs, outputs=outputs,
edges=edges, fname="cross3", id=N))
N += 1


#wire
inputs = [[0,0,"left"]]
outputs =  [[0,0,"right"]]
blocks.append(Block("wire", inputs=inputs, outputs=outputs, id=N, fname="wire1"))
N += 1
inputs = [[0,0,"right"]]
outputs =  [[0,0,"left"]]
blocks.append(Block("wire", inputs=inputs, outputs=outputs, id=N, fname="wire4"))
N += 1
inputs = [[0,0,"up"]]
outputs =  [[0,0,"down"]]
blocks.append(Block("wire", inputs=inputs, outputs=outputs, id=N, fname="wire3"))
N += 1
inputs = [[0,0,"down"]]
outputs =  [[0,0,"up"]]
blocks.append(Block("wire", inputs=inputs, outputs=outputs, id=N, fname="wire2"))
N += 1

#angle
inputs = [[0,0,"left"]]
outputs =  [[0,0,"down"]]
blocks.append(Block("angle", inputs=inputs, outputs=outputs, id=N, fname="angle1"))
N += 1

inputs = [[0,0,"up"]]
outputs =  [[0,0,"right"]]
shape = [[0,0], [0,1]]
blocks.append(Block("angle", shape=shape, inputs=inputs, outputs=outputs, id=N, fname="angle2"))
N += 1

inputs = [[0,0,"left"]]
outputs =  [[0,0,"up"]]
shape = [[0,0], [0,1]]
blocks.append(Block("angle", shape=shape, inputs=inputs, outputs=outputs, id=N, fname="angle3"))
N += 1

inputs = [[0,0,"down"]]
outputs =  [[0,0,"right"]]
blocks.append(Block("angle", inputs=inputs, outputs=outputs, id=N, fname="angle4"))
N += 1

inputs = [[0,0,"up"]]
outputs =  [[0,0,"left"]]
blocks.append(Block("angle", inputs=inputs, outputs=outputs, id=N, fname="angle5"))
N += 1

inputs = [[1,0,"right"]]
outputs =  [[1,0,"down"]]
shape = [[0,0], [1,0]]
blocks.append(Block("angle", shape=shape, inputs=inputs, outputs=outputs, id=N, fname="angle6"))
N += 1

inputs = [[1,0,"right"]]
outputs =  [[1,0,"up"]]
shape = [[0,0], [1,0], [0,1], [1,1]]
blocks.append(Block("angle", shape=shape, inputs=inputs, outputs=outputs, id=N, fname="angle7"))
N += 1

inputs = [[0,0,"down"]]
outputs =  [[0,0,"left"]]
shape = [[0,0], [1,0]]
blocks.append(Block("angle", shape=shape, inputs=inputs, outputs=outputs, id=N, fname="angle8"))
N += 1
