class display():
    def __init__(self): # Cette fonction est automatiquement éxécuter lors de la création de l'objet
        self.defuse = True # Ce module est toujours désamorçé.

        self.frame = LabelFrame(Fen, text = "Display") # On créer une sous-fenêtre
        self.frame.grid(row = 1, column = 1, sticky = "NEWS") # On l'affiche

        self.label = Label(self.frame, text = "ici on affichera le texte")
        self.label.grid(row = 1, column = 1, sticky = "NEWS")

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

        if self.time > 0:
            self.chrono_event = Fen.after(1000, self.chrono)
        else: self.Lose() # Perdu par manque de temps


    def start(self):
        self.PenalityAnimation = False
        self.DefuseAnimation = False
        self.time = 181 # En lanceant le chrono, une seconde est immédiatement supprimée
        self.chrono()


    def checkDefuse(self):
        self.time += App.config["Bonus de temps"]["Value"]

        _Stop = False
        for module in classModule:
            if classModule[module].defuse == False:
                _Stop = True

        if not(_Stop): # Si tout les modules sont désamorcé
            Fen.after_cancel(self.chrono_event) # On désactive le chrono
            self.write(random.choice(["GG", "Bravo", "Félicitation"]))

        else:
            self.DefuseAnimation = True


    def PenalityLife(self):
        App.Life -= 1
        self.PenalityAnimation = True

        if App.Life <= 0:
            self.Lose()


    def Lose(self):
        Fen.after_cancel(self.chrono_event) # On désactive le chrono
        self.write(random.choice(["Perdu", "Dommage", "Try again"]))
        # Réitialiser tout les modules

classModule["display"] = display()
