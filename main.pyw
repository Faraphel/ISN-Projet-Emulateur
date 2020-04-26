########### import #############
from tkinter import *
import os
import pickle
import json
import random
import math
import time
from PIL import Image, ImageTk

########## constante ###########
PATH_MODULE = "./module/"
PATH_ASSETS = "./assets/"
PATH_HISTORY = "./history/"

if not(os.path.exists(PATH_HISTORY)): os.makedirs(PATH_HISTORY)
######## initialisation ########
Fen = Tk()
Fen.resizable(width = False, height = False)
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
		self.InfinityMode = False

	def MainMenu(self, selected = 0): # Niveau 1

		MainMenu_Option = {
			"Lancer" : self.start,
			"Option" : self.settings,
			"Mode Infini": self.start_infinity_mode,
			"Historique": self.history,
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
		if not(self.InfinityMode):
			self.seed = random.randint(-10**10, 10**10) # On défini la seed afin de pouvoir la sauvegarder pour l'historique.
			self.mode = "Classique"
			self.start_time = time.time()
			self.mod_des = 0

		classModule["simon"].bind(UpCmd = "pass", DownCmd = "pass", LeftCmd = "pass", RightCmd = "pass")
		self.Life = self.config["Vie"]["Value"] # On initialise le nombre de vie comme indiqué dans les paramètres

		for module in classModule:
			classModule[module].start()


		# Initilisalisé tout les modules
		# Démmaré un chrono

	def start_infinity_mode(self):
		self.seed = random.randint(-10**10, 10**10)
		self.mode = "Infinity"
		self.start_time = time.time()
		self.mod_des = 0

		self.InfinityMode = True
		self.start()


	def history(self, selected = 0): # Menu des fichiers .history
		ListFileHistory = list(reversed(os.listdir(PATH_HISTORY)))
		if len(ListFileHistory) == 0:
			self.MainMenu(selected = 3)
			return 0

		selected_name = ListFileHistory[selected]

		selected_name_show = selected_name.replace(" ", "\n").replace(".history", "") # On l'affiche sur deux lignes et on retire l'extension
		selected_name_show = [c for c in selected_name_show] # On converti le texte en liste de caractère
		selected_name_show.insert(2, "/") # séparation jour / mois
		selected_name_show.insert(5, "/") # séparation mois / année
		selected_name_show.insert(13, ":") # séparation heure / minute
		selected_name_show.insert(16, ":") # séparation minute / seconde
		selected_name_show = "".join(selected_name_show)

		prefix = "< "
		suffix = " >"

		if selected == 0:
			func_up = "pass" # Si on est à la première option, ne fait rien
			prefix = "  "

		else: func_up = lambda: self.history(selected = selected - 1) # sinon, remonte

		if selected == len(ListFileHistory) - 1:
			func_down = "pass" # Si on est à la dernière option, ne fait rien
			suffix = "  "

		else: func_down = lambda: self.history(selected = selected + 1) # sinon, descend

		classModule["display"].write(prefix + selected_name_show + suffix) # On affiche le texte sur l'écran

		func_right = lambda: self.history_show(selected_name = selected_name) # Renvoie la fonction associé à l'option selectionné
		func_left = lambda: self.MainMenu(selected = 3)

		classModule["simon"].bind(UpCmd = func_up, DownCmd = func_down, LeftCmd = func_left, RightCmd = func_right)


	def history_show(self, selected = 0, selected_name = None): # Menu pour afficher le contenu des fichiers .history
		with open(PATH_HISTORY + selected_name, "rb") as File:
			StatHistory = pickle.load(File)

		StatHistoryKeys = list(StatHistory.keys())

		StatName = StatHistoryKeys[selected]
		StatData = StatHistory[StatName]

		prefix = "< "
		suffix = " >"

		if selected == 0:
			func_up = "pass" # Si on est à la première option, ne fait rien
			prefix = "  "

		else: func_up = lambda: self.history_show(selected = selected - 1, selected_name = selected_name) # sinon, remonte

		if selected == len(StatHistory) - 1:
			func_down = "pass" # Si on est à la dernière option, ne fait rien
			suffix = "  "


		else: func_down = lambda: self.history_show(selected = selected + 1, selected_name = selected_name) # sinon, descend

		if StatName == "Paramètre": classModule["display"].write(prefix + StatName + "\n" + "Droite pour voir" + suffix)
		else: classModule["display"].write(prefix + StatName + "\n" + str(StatData) + suffix) # On affiche le texte sur l'écran

		if StatName == "Paramètre": func_right = lambda: self.history_show_settings(selected = 0, selected_name = selected_name) # func_right = lambda: self.modif_settings(selected_name = selected_name) # Renvoie la fonction associé à l'option selectionné
		elif StatName == "Archiver": func_right = lambda: self.SwitchArchive(selected = selected, selected_name = selected_name)
		elif StatName == "Effacer": func_right = lambda: self.confirm_delete_history(selected_name = selected_name)
		else: func_right = "pass"

		ListFileHistory = list(reversed(os.listdir(PATH_HISTORY)))
		func_left = lambda: self.history(selected = ListFileHistory.index(selected_name))

		classModule["simon"].bind(UpCmd = func_up, DownCmd = func_down, LeftCmd = func_left, RightCmd = func_right)


	def confirm_delete_history(self, selected_name):
		classModule["display"].write("Êtes-vous sur de\nvouloir effacer ?")

		with open(PATH_HISTORY + selected_name, "rb") as File:
			StatHistory = pickle.load(File)

		cancel = lambda: self.history_show(selected = list(StatHistory.keys()).index("Effacer"))
		confirm = lambda: self.delete_history(selected_name = selected_name)
		classModule["simon"].bind(UpCmd = cancel, DownCmd = cancel, LeftCmd = cancel, RightCmd = confirm)


	def delete_history(self, selected_name):
		os.remove(PATH_HISTORY + selected_name)
		self.history()


	def SwitchArchive(self, selected, selected_name):
		with open(PATH_HISTORY + selected_name, "rb") as File:
			StatHistory = pickle.load(File)

		if StatHistory["Archiver"] == "Oui": StatHistory["Archiver"] = "Non"
		else: StatHistory["Archiver"] = "Oui"

		with open(PATH_HISTORY + selected_name, "wb") as File:
			pickle.dump(StatHistory, File)

		self.history_show(selected = selected, selected_name = selected_name)


	def history_show_settings(self, selected = 0, selected_name = None): # Afficher les paramètres lors d'une partie stocké dans l'historique
		with open(PATH_HISTORY + selected_name, "rb") as File:
			StatHistory = pickle.load(File)

		StatHistorySettings = StatHistory["Paramètre"]
		StatHistorySettingsKeys = list(StatHistorySettings.keys())
		StatSettingsName = StatHistorySettingsKeys[selected]
		StatSettingsData = StatHistorySettings[StatSettingsName]["Value"]

		prefix = "< "
		suffix = " >"

		if selected == 0:
			func_up = "pass" # Si on est à la première option, ne fait rien
			prefix = "  "

		else: func_up = lambda: self.history_show_settings(selected = selected - 1, selected_name = selected_name) # sinon, remonte

		if selected == len(StatHistorySettings) - 1: # Pour éviter que _Protected s'affiche
			func_down = "pass" # Si on est à la dernière option, ne fait rien
			suffix = "  "

		else: func_down = lambda: self.history_show_settings(selected = selected + 1, selected_name = selected_name) # sinon, descend

		classModule["display"].write(prefix + StatSettingsName + "\n" + str(StatSettingsData) + suffix) # On affiche le texte sur l'écran

		func_right = lambda: "pass"
		func_left = lambda: self.history_show(selected = list(StatHistory.keys()).index("Paramètre"), selected_name = selected_name)

		classModule["simon"].bind(UpCmd = func_up, DownCmd = func_down, LeftCmd = func_left, RightCmd = func_right)




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
		cancel = lambda: self.MainMenu(selected = 4)
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
