class display():
    def __init__(self): # Cette fonction est automatiquement éxécuter lors de la création de l'objet
        self.defuse = True # Ce module est toujours désamorçé.

        self.frame = LabelFrame(Fen, text = "Display", width = 180, height = 180) # On créer une sous-fenêtre
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
        self.time = App.config["Temps"]["Value"] + 1 # En lanceant le chrono, une seconde est immédiatement supprimée
        self.chrono()


    def checkDefuse(self):
        self.time += App.config["Bonus de temps"]["Value"]

        _Stop = 0
        for module in classModule:
            if classModule[module].defuse == False:
                _Stop += 1

        if _Stop <= App.config["Module négli."]["Value"]: # Si tout les modules sont désamorcé
            Fen.after_cancel(self.chrono_event) # On désactive le chrono
            self.write(random.choice(["GG", "Bravo", "Félicitation"]))

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

        self.reset_all()


    def reset_all(self): # Cette fonction demande à tous les autres modules de se réinitialiser
        for module in classModule:
            classModule[module].reset()


    def reset(self): # Cette fonction est appelé a chaque fin de partie pour réinitialiser ce module
        self.label.config(foreground = "black", background = "SystemButtonFace")
        Fen.after(7500, lambda: App.MainMenu()) # On laisse le joueur devant le message de victoire / défaite pendant 7.5 secondes

classModule["display"] = display()
