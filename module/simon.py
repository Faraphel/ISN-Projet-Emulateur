class simon():
    def __init__(self): # Cette fonction est automatiquement éxécuter lors de la création de l'objet
        self.rules = {
            "Facile": {
                "A On": {"Up": "Left", "Left": "Down", "Right": "Up", "Down": "Right"},
                "Else": {"Up": "Down", "Left": "Up", "Right": "Right", "Down": "Left"}
            }, "Normal": {
                "A On": {"Up": "Down", "Left": "Left", "Right": "Up", "Down": "Right"},
                "E Blink": {"Up": "Down", "Left": "Left", "Right": "Right", "Down": "Up"},
                "C Off": {"Up": "Left", "Left": "Right", "Right": "Up", "Down": "Down"},
                "Else": {"Up": "Right", "Left": "Down", "Right": "Left", "Down": "Up"}
            }, "Difficile": {
                "F On": {"Up": "Left", "Left": "Right", "Right": "Down", "Down": "Up"},
                "A Off": {"Up": "Up", "Left": "Down", "Right": "Right", "Down": "Left"},
                "B Blink": {"Up": "Down", "Left": "Left", "Right": "Right", "Down": "Up"},
                "A Blink": {"Up": "Down", "Left": "Right", "Right": "Left", "Down": "Up"},
                "C On": {"Up": "Up", "Left": "Left", "Right": "Right", "Down": "Down"},
                "Else": {"Up": "Left", "Left": "Down", "Right": "Right", "Down": "Up"}
            }
        }

        self.frame = LabelFrame(Fen, text = "Simon") # On créer une sous-fenêtre
        self.frame.grid(row = 2, column = 1, sticky = "NEWS") # On l'affiche

        self.dico_but = {} # On créer un dictionnaire qui va contenir les objets bouttons.

        self.dico_but["Up"] = Button(self.frame, text = "", background = "lightgreen", width = 2, height = 1) # On créer le boutton du haut
        self.dico_but["Up"].grid(row = 2, column = 2)

        self.dico_but["Left"] = Button(self.frame, text = "", background = "lightblue", width = 2, height = 1) # On créer le boutton à gauche
        self.dico_but["Left"].grid(row = 3, column = 1)

        self.dico_but["Right"] = Button(self.frame, text = "", background = "indianred", width = 2, height = 1) # On créer le boutton à droite
        self.dico_but["Right"].grid(row = 3, column = 3)

        self.dico_but["Down"] = Button(self.frame, text = "", background = "lightyellow", width = 2, height = 1)  # On créer le boutton
        self.dico_but["Down"].grid(row = 4, column = 2)


    def bind(self, UpCmd, DownCmd, LeftCmd, RightCmd): # Bind les touches à leur fonction associé dans les arguments
        self.dico_but["Up"].config(command = UpCmd)
        self.dico_but["Left"].config(command = LeftCmd)
        self.dico_but["Right"].config(command = RightCmd)
        self.dico_but["Down"].config(command = DownCmd)


    def start(self):
        self.Sequence = []
        for _ in range(5):
            self.Sequence.append(random.choice(["Up", "Left", "Right", "Down"]))

        print(self.Sequence)

        self.Step = 4
        self.sequence_choice()


    def reset_all(self):
            self.dico_but["Up"].config(background = "lightgreen")
            self.dico_but["Left"].config(background = "lightblue")
            self.dico_but["Right"].config(background = "indianred")
            self.dico_but["Down"].config(background = "lightyellow")


    def sequence_choice(self, frame = 0):
        if frame <= self.Step:
            self.Sequence_step = self.Sequence[frame]
            if self.Sequence_step == "Up":
                self.dico_but[self.Sequence_step].config(background = "green")
            elif self.Sequence_step == "Left":
                self.dico_but[self.Sequence_step].config(background = "blue")
            elif self.Sequence_step == "Right":
                self.dico_but[self.Sequence_step].config(background = "red")
            elif self.Sequence_step == "Down":
                self.dico_but[self.Sequence_step].config(background = "yellow")

        else:
            frame = 0

        Fen.after(1000, lambda: self.reset_all())
        Fen.after(1500, lambda: self.sequence_choice(frame + 1))


        # frame désigne le bouton qui doit s'allumer pendant la séquence, à quel étape on en est

        # Code qui choisi des combinaisons à rentré et des led qui s'allument



classModule["simon"] = simon()
