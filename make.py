# -*- coding: utf-8 -*-


# Golly script for the pattern generation

import golly as g
import numpy as np
import pickle


def paste(g, fichier, x, y):
	g.addlayer()
	g.open(fichier)
	g.select([-1000, -1000, 2000, 2000])
	g.copy()
	g.dellayer()
	g.paste(x-1000,y-1000,'or')


def transfo(i,j):
    return i*60-j*60, i*60+j*60


def load():
    file = open("blocks.txt","r")
    lines = file.read()
    file.close()
    lines = lines.split("\n")
    blocks = [line.split() for line in lines][:-1]
    blocks = [[line[0], int(line[1]), int(line[2])] for line in blocks]
    return blocks


def make(blocks):
    g.new("circuit")
    for block in blocks:
        fname = "blocks/{}.mc".format(block[0])
        paste(g, fname, *transfo(block[1], block[2]))
    g.fit()
    g.save("circuit.mc", "mc")

blocks = load()
make(blocks)
