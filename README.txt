NEAT-Checkerboard-STEM-Project

This program can train a neural network (using the NEAT algorithm) to play checkers by clicking 'NEAT vs NEAT'.
After training, you may play against the network by choosing one of the first two options in the menu, 'Play as BLUE' or 'Play as RED'!

Included is a pretrained network to play against, but you may customize and train your own network by editing the config file.

Currently it has a pop size of 2, and will run until the fitness threshold reaches 100,000 points.
The fitness evaluation function is not designed for small starting populations, so the training will complete relativly quickly.

Dependencies: 
NEAT; install here https://neat-python.readthedocs.io/en/latest/installation.html
GraphViz; install here https://graphviz.readthedocs.io/en/stable/manual.html#installation

GraphViz is only needed for the trainer to properly display winning genome. 
Training will save even if the graphviz error occurs, so you may still play against your network.  