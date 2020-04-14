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

		self.MainMenu()


	def MainMenu(self, selected = 0): # Niveau 1
		MainMenu_Option = {
			"Lancer" : self.start,
			"Option" : self.settings,
			"Quitter" : self.leave,
		} # On créer un dictionnaire qui associe toute les options proposé à leur fonction respective.
		MainMenu_Keys = list(MainMenu_Option.keys()) # On créer une liste qui ne contient que les clé du dictionnaire, permettant d'utiliser des index numériques.

		classModule["display"].write(MainMenu_Keys[selected]) # On affiche le texte sur l'écran

		if selected == 0: func_up = "pass" # Si on est à la première option, ne fait rien
		else: func_up = lambda: self.MainMenu(selected = selected - 1) # sinon, remonte

		if selected == len(MainMenu_Keys) - 1: func_down = "pass" # Si on est à la dernière option, ne fait rien
		else: func_down = lambda: self.MainMenu(selected = selected + 1) # sinon, descend

		func_right = MainMenu_Option[MainMenu_Keys[selected]] # Renvoie la fonction associé à l'option selectionné

		classModule["simon"].bind(UpCmd = func_up, DownCmd = func_down, LeftCmd = "pass", RightCmd = func_right)



	def start(self):
		pass
		# Code pour démarrer une partie

	def settings(self):
		classModule["display"].write("settings")

	def leave(self):
		pass
		# Code pour quitter le jeu



App = AppClass()

mainloop() # On "active" la fênetre
