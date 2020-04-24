########### import #############
from tkinter import *
import os
import pickle
import json
import random
from PIL import Image, ImageTk

########## constante ###########
PATH_MODULE = "./module/"
PATH_ASSETS = "./assets/"

######## initialisation ########
Fen = Tk()
Fen.iconbitmap(PATH_ASSETS + "icon.ico")
Fen.title("Emulateur - Bombe")
classModule = {} # Dictionnaire qui va contenir tout les modules afin qu'ils puissent intéragir entre eux

for file in os.listdir(PATH_MODULE): # On cherche les modules dans leur dossier
	with open(PATH_MODULE + file, "rb") as module: # On les ouvres en lecture
		exec(module.read()) # On les executes


class AppClass(): # Classe du "moteur" du jeu
	def __init__(self): # Initialisation

		self.load_settings()
		self.MainMenu()


	def MainMenu(self, selected = 0): # Niveau 1

		MainMenu_Option = {
			"Lancer" : self.start,
			"Option" : self.settings,
			"Reinit. Option.": self.confirm_reinit_option,
			"Quitter" : self.leave,
		} # On créer un dictionnaire qui associe toute les options proposé à leur fonction respective.
		MainMenu_Keys = list(MainMenu_Option.keys()) # On créer une liste qui ne contient que les clé du dictionnaire, permettant d'utiliser des index numériques.

		prefix = "< "
		suffix = " >"

		if selected == 0:
			func_up = "pass" # Si on est à la première option, ne fait rien
			prefix = "  "

		else: func_up = lambda: self.MainMenu(selected = selected - 1) # sinon, remonte

		if selected == len(MainMenu_Keys) - 1:
			func_down = "pass" # Si on est à la dernière option, ne fait rien
			suffix = "  "

		else: func_down = lambda: self.MainMenu(selected = selected + 1) # sinon, descend

		func_right = MainMenu_Option[MainMenu_Keys[selected]] # Renvoie la fonction associé à l'option selectionné

		classModule["display"].write(prefix + MainMenu_Keys[selected] + suffix) # On affiche le texte sur l'écran


		classModule["simon"].bind(UpCmd = func_up, DownCmd = func_down, LeftCmd = "pass", RightCmd = func_right)



	def start(self):
		classModule["simon"].bind(UpCmd = "pass", DownCmd = "pass", LeftCmd = "pass", RightCmd = "pass")

		self.Life = self.config["Vie"]["Value"] # On initialise le nombre de vie comme indiqué dans les paramètres

		for module in classModule:
			classModule[module].start()


		# Initilisalisé tout les modules
		# Démmaré un chrono

	def settings(self, selected = 0):
		 # On créer un dictionnaire qui associe toute les options proposé à leur fonction respective.
		SettingsMenu_Keys = list(self.config.keys()) # On créer une liste qui ne contient que les clé du dictionnaire, permettant d'utiliser des index numériques.
		selected_name = SettingsMenu_Keys[selected]

		prefix = "< "
		suffix = " >"

		if selected == 0:
			func_up = "pass" # Si on est à la première option, ne fait rien
			prefix = "  "

		else: func_up = lambda: self.settings(selected = selected - 1) # sinon, remonte

		if selected == len(SettingsMenu_Keys) - 1:
			func_down = "pass" # Si on est à la dernière option, ne fait rien
			suffix = "  "

		else: func_down = lambda: self.settings(selected = selected + 1) # sinon, descend

		classModule["display"].write(prefix + selected_name + suffix) # On affiche le texte sur l'écran

		selected_value = self.config[selected_name]["Available"].index(self.config[selected_name]["Value"]) # Valeur de l'index de la valeur déjà défini dans les paramètres
		func_right = lambda: self.modif_settings(selected_name = selected_name, selected = selected_value) # Renvoie la fonction associé à l'option selectionné
		func_left = lambda: self.MainMenu(selected = 1)

		classModule["simon"].bind(UpCmd = func_up, DownCmd = func_down, LeftCmd = func_left, RightCmd = func_right)


	def modif_settings(self, selected_name, selected = 0): # selected_name -> nom de la variable que l'on change # selected -> valeur actuellement sélectionné
		 # On créer une liste qui ne contient que les clé du dictionnaire, permettant d'utiliser des index numériques.
		ModifSettingsMenu_Keys = self.config[selected_name]["Available"]

		prefix = "< "
		suffix = " >"

		if selected == 0:
			func_up = "pass" # Si on est à la première option, ne fait rien
			prefix = "  "

		else: func_up = lambda: self.modif_settings(selected_name = selected_name, selected = selected - 1)

		if selected == len(ModifSettingsMenu_Keys) - 1:
			func_down = "pass" # Si on est à la dernière option, ne fait rien
			suffix = "  "

		else: func_down = lambda: self.modif_settings(selected_name = selected_name, selected = selected + 1) # sinon, descend

		classModule["display"].write(prefix + str(ModifSettingsMenu_Keys[selected]) + suffix) # On affiche le texte sur l'écran


		func_right = lambda: self.save_settings(selected_name = selected_name, selected = ModifSettingsMenu_Keys[selected])
		func_left = lambda: self.settings(selected = list(self.config.keys()).index(selected_name)) # On renvoie le joueur sur le menu de l'option qu'il est en train d'éditer

		classModule["simon"].bind(UpCmd = func_up, DownCmd = func_down, LeftCmd = func_left, RightCmd = func_right)

		# + Bonus : afficher par défaut la valeur sur laquel le jeu est paramétrer

	def save_settings(self, selected_name, selected):
		self.config[selected_name]["Value"] = selected

		with open(r"config.pickle", "wb") as file:
			pickle.dump(self.config, file)

		self.settings(selected = list(self.config.keys()).index(selected_name)) # On renvoie le joueur sur le menu de l'option qu'il est en train d'éditer


	def load_settings(self): # Lire le fichier pickle -> self.config
		try: # En supposant que le fichier pickle existe et qu'il ne soit pas corrompu
			with open(r"config.pickle","rb") as file:
				self.config = pickle.load(file)
		except: # Sinon, charge les options par défaut
			self.reinit_option()


	def confirm_reinit_option(self):
		classModule["display"].write("Êtes-vous sur de\nvouloir réinitialiser ?")
		cancel = lambda: self.MainMenu(selected = 2)
		confirm = lambda: self.reinit_option(mainmenu_return = True)
		classModule["simon"].bind(UpCmd = cancel, DownCmd = cancel, LeftCmd = cancel, RightCmd = confirm)


	def reinit_option(self, mainmenu_return = False):
		with open(r"config.json","rb") as file:
			self.config = json.load(file)

		with open(r"config.pickle","wb") as file: # Recréer le .pickle
			pickle.dump(self.config, file)

		if mainmenu_return: self.MainMenu(selected = 2)


	def leave(self):
		Fen.destroy()
		exit()
		# Code pour quitter le jeu



App = AppClass()

mainloop() # On "active" la fênetre
