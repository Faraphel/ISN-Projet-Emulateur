class display():
    def __init__(self): # Cette fonction est automatiquement éxécuter lors de la création de l'objet
        self.defuse = True # Ce module est toujours désamorçé.
        self.InitInfinity = False # Vaut False si la partie en mode infinity est à sa première partie, si tous les modules sont alors désamoçé une fois, elle vaut True.
        # Permet de ne lancer le chrono qu'une seule fois.

        self.frame = LabelFrame(Fen, text = "Ecran d'affichage", width = 180, height = 180, borderwidth = 4) # On créer une sous-fenêtre
        self.frame.grid(row = 1, column = 1) # On l'affiche

        self.frame.grid_propagate(0) # Force le LabelFrame à ne pas changer de taille
        self.frame.grid_rowconfigure(1, weight = 1) # Centre verticalement
        self.frame.grid_columnconfigure(1, weight = 1) # Centre horizontalement


        self.label = Label(self.frame, text = "chargement du chrono", font = ("TkDefaultFont", 15))
        self.label.grid(row = 1, column = 1)

    def write(self, text):
        self.label.config(text = text)


    def chrono(self):
        self.time -= 1
        self.minute = self.time // 60
        self.second = self.time % 60

        if self.PenalityAnimation: # Si le joueur vient de se trompé
            self.PenalityAnimation = False
            self.write("/!\\ Erreur /!\\\nVie restante : %i" % App.Life)

        elif self.DefuseAnimation: # Si le joueur vient de désamorçé tout le module
            self.DefuseAnimation = False
            self.write("Module désamorcé !")

        else:
            self.write("%02i:%02i" % (self.minute, self.second))

        if self.time <= 45: # Clignotement du chrono
            if self.time % 2 == 0: self.label.config(foreground = "indianred", background = "gold")
            else: self.label.config(foreground = "gold", background = "indianred")

        else:
            self.label.config(foreground = "black", background = "SystemButtonFace")

        if self.time >= 0: # Vérification que le joueur n'ai pas dépassé le temps imparti
            self.chrono_event = Fen.after(1000, self.chrono)

        else:
            self.Lose() # Perdu par manque de temps



    def start(self):
        self.PenalityAnimation = False
        self.DefuseAnimation = False

        if self.InitInfinity == False: # Si le jeu n'a pas encore été lancé
            self.time = App.config["Temps"]["Value"] + 1 # En lanceant le chrono, une seconde est immédiatement supprimée
            self.chrono()


    def checkDefuse(self):
        self.time += App.config["Bonus de temps"]["Value"]
        App.mod_des += 1

        _Stop = 0
        for module in classModule:
            if classModule[module].defuse == False:
                _Stop += 1

        if _Stop <= App.config["Module négli."]["Value"]: # Si tout les modules sont désamorcé
            self.write(random.choice(["GG", "Bravo", "Félicitation"]))
            self.Win = "Gagné"
            self.reset_all()

        else:
            self.DefuseAnimation = True


    def PenalityLife(self):
        App.Life -= 1
        self.PenalityAnimation = True
        self.time -= App.config["Malus de temps"]["Value"]

        if App.Life <= 0:
            self.Lose()


    def Lose(self):
        Fen.after_cancel(self.chrono_event) # On désactive le chrono
        self.write(random.choice(["Perdu", "Dommage", "Try again"]))

        self.InitInfinity = False
        App.InfinityMode = False
        self.Win = "Perdu"
        self.reset_all()


    def reset_all(self): # Cette fonction demande à tous les autres modules de se réinitialiser
        for module in classModule:
            classModule[module].reset()


    def reset(self): # Cette fonction est appelé a chaque fin de partie pour réinitialiser ce module
        if App.InfinityMode == False: # Si l'on n'est pas en mode infini
            Fen.after_cancel(self.chrono_event) # On désactive le chrono
            self.label.config(foreground = "black", background = "SystemButtonFace")

            duration = time.time() - App.start_time
            duration_min, duration_sec = duration // 60, duration % 60

            ############################## HISTORIQUE ##############################
            with open(PATH_HISTORY + time.strftime("%d%m%Y %H%M%S") + ".history", "wb") as File:

                pickle.dump({
                "Seed": App.seed,
                "Mode": App.mode,
                "Partie": self.Win,
                "Durée": "%02i:%02i" % (duration_min, duration_sec),
                "Mod. Des.": App.mod_des,
                "Mod. Des. / min.": round(App.mod_des / (duration / 60), 1),
                "Paramètre": App.config,
                "Archiver": "Non",
                "Effacer": ""
                }, File)



            ListFileHistory = os.listdir(PATH_HISTORY)
            Max_file_save = App.config["Max. Score sauv."]["Value"]

            if len(ListFileHistory) > Max_file_save:
                for file in ListFileHistory:

                    with open(PATH_HISTORY + file, "rb") as File: StatHistory = pickle.load(File)
                    if StatHistory["Archiver"] == "Non":
                        os.remove(PATH_HISTORY + file)
                        break

            ############################## STATISTIQUE ##############################
            App.StatDico["Mod. Dés. Total"] += App.mod_des
            total_min, total_sec = App.StatDico["Temps de jeu"].split(":")
            App.StatDico["Temps de jeu"] = "%02i:%02i" % (int(total_min) + duration_min, int(total_sec) + duration_sec)
            total_min, total_sec = App.StatDico["Temps de jeu"].split(":") # On actualise ces variables car nécéssaire pour d'autre stat


            total_Mod_Des_min = int(App.StatDico["Mod. Des. / min."].split("/")[0])
            App.StatDico["Mod. Des. / min."] = "%i/min" % round(App.StatDico["Mod. Dés. Total"] / (int(total_min) + (int(total_sec) / 60)), 1)


            App.StatDico["Partie total"] += 1

            if App.mode == "Classique":
                App.StatDico["Partie Classique"] += 1
                casual_win = int(App.StatDico["Classique gagné"].split(" ")[0])
                casual_lose = int(App.StatDico["Classique perdu"].split(" ")[0])

                if self.Win == "Gagné": casual_win += 1
                else: casual_lose += 1

                App.StatDico["Classique gagné"] = "%i (%i %%)" % (casual_win, int((casual_win / App.StatDico["Partie total"]) * 100))
                App.StatDico["Classique perdu"] = "%i (%i %%)" % (casual_lose, int((casual_lose / App.StatDico["Partie total"]) * 100))

            elif App.mode == "Infinity":
                App.StatDico["Partie Infini"] += 1


            with open("./statistic.pickle", "wb") as File:
                pickle.dump(App.StatDico, File)


            Fen.after(7500, lambda: App.MainMenu()) # On laisse le joueur devant le message de victoire / défaite pendant 7.5 secondes


        else: # Si l'on est en mode infini
            self.InitInfinity = True # On a déjà fini le jeu une fois
            Fen.after(1000, App.start) # On relance le jeu


classModule["display"] = display()
