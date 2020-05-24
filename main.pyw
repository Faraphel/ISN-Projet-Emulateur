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

##### création de fichier ######
if not(os.path.exists(PATH_HISTORY)): os.makedirs(PATH_HISTORY)

if not(os.path.exists("./statistic.pickle")):
	with open("./statistic.pickle", "wb") as File:
		pickle.dump({
			"Mod. Dés. Total":	0,
			"Temps de jeu":		"00:00", # s
			"Mod. Des. / min.":	"0/min", # mod / min
			"Partie Classique": 0,
			"Partie Infini": 	0,
			"Partie total":		0,
			"Classique gagné":	"0 (0 %)",
			"Classique perdu":	"0 (0 %)"
		}, File)

######## initialisation ########
Fen = Tk()
Fen.resizable(width = False, height = False)
Fen.iconphoto(False, ImageTk.PhotoImage(file = PATH_ASSETS + "icon.ico"))
Fen.title("Emulateur - Bombe")
classModule = {} # Dictionnaire qui va contenir tout les modules afin qu'ils puissent intéragir entre eux

global DEFAULT_BG_COLOR
DEFAULT_BG_COLOR = Fen.cget("background")

for file in os.listdir(PATH_MODULE): # On cherche les modules dans leur dossier
	with open(PATH_MODULE + file, "rb") as module: # On les ouvres en lecture
		exec(module.read()) # On les executes


class AppClass(): # Classe du "moteur" du jeu
	def __init__(self): # Initialisation

		self.load_settings()
		self.MainMenu()
		self.InfinityMode = False

	def menu(self, selected_name = "", selected = 0, ListKeys = [], func_navigation = None, text = "", func_left = None, func_right = None):
		prefix = "\u2191 "
		suffix = " \u2193"

		if selected == 0:
			func_up = "pass" # Si on est à la première option, ne fait rien
			prefix = "  "
		else: func_up = lambda: func_navigation(selected_name = selected_name, selected = selected - 1)

		if selected == len(ListKeys) - 1:
			func_down = "pass" # Si on est à la dernière option, ne fait rien
			suffix = "  "
		else: func_down = lambda: func_navigation(selected_name = selected_name, selected = selected + 1)

		classModule["display"].write(prefix + str(text) + suffix)

		classModule["simon"].bind(UpCmd = func_up, DownCmd = func_down, LeftCmd = func_left, RightCmd = func_right)


	def MainMenu(self, selected = 0, selected_name = None): # Niveau 1
		MainMenu_Option = {
			"Lancer" : self.start,
			"Mode Infini": self.start_infinity_mode,
			"Option" : self.settings,
			"Historique": self.history,
			"Statistique": self.statistic,
			"Reinit. Option.": self.confirm_reinit_option,
			"Quitter" : self.leave,
		} # On créer un dictionnaire qui associe toute les options proposé à leur fonction respective.
		ListKeys = list(MainMenu_Option.keys()) # On créer une liste qui ne contient que les clé du dictionnaire, permettant d'utiliser des index numériques.

		self.menu(
				selected_name = selected_name,
				selected = selected,
				ListKeys = ListKeys,
				func_navigation = self.MainMenu,
				text = ListKeys[selected],
				func_right = MainMenu_Option[ListKeys[selected]],
				func_left = "pass"
			)


	def pre_start(self, seed = None):
		with open("./statistic.pickle", "rb") as File:
			self.StatDico = pickle.load(File)

		if seed == None: self.seed = random.randint(-10**10, 10**10) # On défini la seed afin de pouvoir la sauvegarder pour l'historique.
		else: self.seed = seed
		random.seed(self.seed)

		self.mode = "Classique"
		self.start_time = time.time()
		self.mod_des = 0

	def start(self, seed = None):
		if not(self.InfinityMode):
			self.pre_start(seed = seed)

		classModule["simon"].bind(UpCmd = "pass", DownCmd = "pass", LeftCmd = "pass", RightCmd = "pass")
		self.Life = self.config["Vie"]["Value"] # On initialise le nombre de vie comme indiqué dans les paramètres

		for module in classModule:
			classModule[module].start()


		# Initilisalisé tout les modules
		# Démmaré un chrono

	def start_infinity_mode(self, seed = None):
		self.pre_start(seed = seed)
		self.mode = "Infinity"
		self.InfinityMode = True
		self.start()


	def history(self, selected = 0, selected_name = None): # Menu des fichiers .history
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

		self.menu(
				selected_name = selected_name,
				selected = selected,
				ListKeys = ListFileHistory,
				func_navigation = self.history,
				text = selected_name_show,
				func_right = lambda: self.history_show(selected_name = selected_name),
				func_left = lambda: self.MainMenu(selected = 3)
			)


	def history_show(self, selected = 0, selected_name = None): # Menu pour afficher le contenu des fichiers .history
		with open(PATH_HISTORY + selected_name, "rb") as File:
			StatHistory = pickle.load(File)

		ListKeys = list(StatHistory.keys())

		StatName = ListKeys[selected]
		StatData = StatHistory[StatName]

		if StatName == "Paramètre": text = StatName + "\n" + "Droite pour voir"
		else: text = StatName + "\n" + str(StatData)

		if StatName == "Paramètre": 	func_right = lambda: self.history_show_settings(selected = 0, selected_name = selected_name) # Renvoie la fonction associé à l'option selectionné
		elif StatName == "Archiver": 	func_right = lambda: self.SwitchArchive(selected = selected, selected_name = selected_name)
		elif StatName == "Effacer": 	func_right = lambda: self.confirm_delete_history(selected_name = selected_name)
		elif StatName == "Seed":
			if StatHistory["Mode"] == "Classique": 	func_right = lambda: self.start(seed = StatData)
			elif StatHistory["Mode"] == "Infinity": func_right = lambda: self.start_infinity_mode(seed = StatData)

		else: func_right = "pass"

		ListFileHistory = list(reversed(os.listdir(PATH_HISTORY)))

		self.menu(
				selected_name = selected_name,
				selected = selected,
				ListKeys = ListKeys,
				func_navigation = self.history_show,
				text = text,
				func_right = func_right,
				func_left = lambda: self.history(selected = ListFileHistory.index(selected_name))
			)


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
		ListKeys = list(StatHistorySettings.keys())
		StatSettingsName = ListKeys[selected]
		StatSettingsData = StatHistorySettings[StatSettingsName]["Value"]

		self.menu(
				selected_name = selected_name,
				selected = selected,
				ListKeys = ListKeys,
				func_navigation = self.history_show_settings,
				text = StatSettingsName + "\n" + str(StatSettingsData),
				func_right = lambda: "pass",
				func_left = lambda: self.history_show(selected = list(StatHistory.keys()).index("Paramètre"), selected_name = selected_name)
			)


	def statistic(self, selected = 0, selected_name = None):
		with open("./statistic.pickle", "rb") as File:
			StatDico = pickle.load(File)

		ListKeys = list(StatDico.keys())
		StatName = ListKeys[selected]
		StatData = StatDico[StatName]

		self.menu(
				selected_name = selected_name,
				selected = selected,
				ListKeys = ListKeys,
				func_navigation = self.statistic,
				text = StatName + "\n" + str(StatData),
				func_right = lambda: "pass",
				func_left = lambda: self.MainMenu(selected = 4)
			)


	def settings(self, selected = 0, selected_name = None): # selected_name n'est pas utilisé, mais évite une erreur
		 # On créer un dictionnaire qui associe toute les options proposé à leur fonction respective.
		ListKeys = list(self.config.keys()) # On créer une liste qui ne contient que les clé du dictionnaire, permettant d'utiliser des index numériques.
		selected_name = ListKeys[selected]

		selected_value = self.config[selected_name]["Available"].index(self.config[selected_name]["Value"]) # Valeur de l'index de la valeur déjà défini dans les paramètres

		self.menu(
				selected_name = selected_name,
				selected = selected,
				ListKeys = ListKeys,
				func_navigation = self.settings,
				text = selected_name,
				func_right = lambda: self.modif_settings(selected_name = selected_name, selected = selected_value),
				func_left = lambda: self.MainMenu(selected = 2)
			)


	def modif_settings(self, selected_name, selected = 0): # selected_name -> nom de la variable que l'on change # selected -> valeur actuellement sélectionné
		 # On créer une liste qui ne contient que les clé du dictionnaire, permettant d'utiliser des index numériques.
		ListKeys = self.config[selected_name]["Available"]

		self.menu(
				selected_name = selected_name,
				selected = selected,
				ListKeys = ListKeys,
				func_navigation = self.modif_settings,
				text = str(ListKeys[selected]),
				func_right = lambda: self.save_settings(selected_name = selected_name, selected = ListKeys[selected]),
				func_left = lambda: self.settings(selected = list(self.config.keys()).index(selected_name))
			) # On renvoie le joueur sur le menu de l'option qu'il est en train d'éditer


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
		cancel = lambda: self.MainMenu(selected = 5)
		confirm = lambda: self.reinit_option(mainmenu_return = True)
		classModule["simon"].bind(UpCmd = cancel, DownCmd = cancel, LeftCmd = cancel, RightCmd = confirm)


	def reinit_option(self, mainmenu_return = False):
		with open(r"config.json","rb") as file:
			self.config = json.load(file)

		with open(r"config.pickle","wb") as file: # Recréer le .pickle
			pickle.dump(self.config, file)

		if mainmenu_return: self.MainMenu(selected = 5)


	def leave(self):
		Fen.destroy()
		exit()
		# Code pour quitter le jeu



App = AppClass()

mainloop() # On "active" la fênetre
