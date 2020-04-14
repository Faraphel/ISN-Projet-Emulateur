########### import #############
from tkinter import *
import os
import pickle
import json

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

		self.load()
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


	def save(self): # self.config -> enregistrer dans un fichier pickle
		with open(r"config.pickle", "wb") as file:
			pickle.dump(self.config, file)


	def load(self): # Lire le fichier pickle -> self.config
		try: # En supposant que le fichier pickle existe et qu'il ne soit pas corrompu
			with open(r"config.pickle","rb") as file:
				self.config = pickle.load(file)
		except: # Sinon, charge les options par défaut
			with open(r"config.json","rb") as file:
				self.config = json.load(file)


	def start(self):
		pass
		# Code pour démarrer une partie

	def settings(self, selected = 0):
		 # On créer un dictionnaire qui associe toute les options proposé à leur fonction respective.
		SettingsMenu_Keys = list(self.config.keys()) # On créer une liste qui ne contient que les clé du dictionnaire, permettant d'utiliser des index numériques.

		classModule["display"].write(SettingsMenu_Keys[selected]) # On affiche le texte sur l'écran

		if selected == 0: func_up = "pass" # Si on est à la première option, ne fait rien
		else: func_up = lambda: self.settings(selected = selected - 1) # sinon, remonte

		if selected == len(SettingsMenu_Keys) - 1: func_down = "pass" # Si on est à la dernière option, ne fait rien
		else: func_down = lambda: self.settings(selected = selected + 1) # sinon, descend

		selected_name = SettingsMenu_Keys[selected]
		func_right = lambda: self.modif_settings(selected_name = selected_name) # Renvoie la fonction associé à l'option selectionné

		func_left = lambda: self.MainMenu(selected = 1)

		classModule["simon"].bind(UpCmd = func_up, DownCmd = func_down, LeftCmd = func_left, RightCmd = func_right)


	def modif_settings(self, selected_name, selected = 0):
		 # On créer une liste qui ne contient que les clé du dictionnaire, permettant d'utiliser des index numériques.
		ModifSettingsMenu_Keys = self.config[selected_name]["Available"]

		classModule["display"].write(ModifSettingsMenu_Keys[selected]) # On affiche le texte sur l'écran

		if selected == 0: func_up = "pass" # Si on est à la première option, ne fait rien
		else: func_up = lambda: self.modif_settings(selected_name = selected_name, selected = selected - 1)

		if selected == len(ModifSettingsMenu_Keys) - 1: func_down = "pass" # Si on est à la dernière option, ne fait rien
		else: func_down = lambda: self.modif_settings(selected_name = selected_name, selected = selected + 1) # sinon, descend


		func_right = lambda: "pass"
		func_left = lambda: self.settings(selected = 0)

		classModule["simon"].bind(UpCmd = func_up, DownCmd = func_down, LeftCmd = func_left, RightCmd = func_right)

		# Faire le système pour confirmer
		# + Bonus : afficher par défaut la valeur sur laquel le jeu est paramétrer


	def leave(self):
		pass
		# Code pour quitter le jeu



App = AppClass()

mainloop() # On "active" la fênetre
