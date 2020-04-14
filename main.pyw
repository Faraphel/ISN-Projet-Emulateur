########### import #############
from tkinter import *
import os

########## constante ###########
PATH_MODULE = "module/"

######## initialisation ########
Fen = Tk()
classModule = {} # Dictionnaire qui va contenir tout les modules afin qu'ils puissent intéragir entre eux

for file in os.listdir(PATH_MODULE): # On cherche les modules dans leur dossier
	with open(PATH_MODULE + file, "rb") as module: # On les ouvres en lecture
		exec(module.read()) # On les executes



mainloop() # On "active" la fênetre
