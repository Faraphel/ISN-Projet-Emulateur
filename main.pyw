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


class AppClass(): # Classe du "moteur" du jeu
	def __init__(self): # Initialisation
		classModule["display"].write("lancer une partie")

	def navigation(key):
		pass
		# Navigation avec les touches du simon dans le menu principal

App = AppClass()

mainloop() # On "active" la fênetre
