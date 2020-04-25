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

        self.reset_color()

        self.frame = LabelFrame(Fen, text = "Simon", width = 180, height = 180, borderwidth = 4) # On créer une sous-fenêtre
        self.frame.grid(row = 2, column = 1, sticky = "NEWS") # On l'affiche

        self.frame.grid_propagate(0) # Force le LabelFrame à ne pas changer de taille

        self.frame.grid_columnconfigure(0, weight = 1)
        self.frame.grid_columnconfigure(4, weight = 1)

        self.frame.grid_rowconfigure(0, weight = 1)
        self.frame.grid_rowconfigure(4, weight = 1)

        self.dico_but = {} # On créer un dictionnaire qui va contenir les objets bouttons.

        self.dico_but["Up"] = Button(self.frame, text = "", background = self.green_off_color, width = 4, height = 2) # On créer le boutton du haut
        self.dico_but["Up"].grid(row = 1, column = 2)

        self.dico_but["Left"] = Button(self.frame, text = "", background = self.blue_off_color, width = 4, height = 2) # On créer le boutton à gauche
        self.dico_but["Left"].grid(row = 2, column = 1)

        self.dico_but["Right"] = Button(self.frame, text = "", background = self.red_off_color, width = 4, height = 2) # On créer le boutton à droite
        self.dico_but["Right"].grid(row = 2, column = 3)

        self.dico_but["Down"] = Button(self.frame, text = "", background = self.yellow_off_color, width = 4, height = 2)  # On créer le boutton
        self.dico_but["Down"].grid(row = 3, column = 2)


    def bind(self, UpCmd, DownCmd, LeftCmd, RightCmd): # Bind les touches à leur fonction associé dans les arguments
        self.dico_but["Up"].config(command = UpCmd)
        self.dico_but["Left"].config(command = LeftCmd)
        self.dico_but["Right"].config(command = RightCmd)
        self.dico_but["Down"].config(command = DownCmd)


    def reset_color(self):
        self.red_off_color = "indianred" # Couleur défini, peut être modifier par le mode daltonien
        self.red_lit_color = "red"
        self.blue_off_color = "lightblue"
        self.blue_lit_color = "blue"
        self.green_off_color = "lightgreen"
        self.green_lit_color = "green"
        self.yellow_off_color = "lightyellow"
        self.yellow_lit_color = "yellow"

    def start(self):
        if App.config["Mode daltonien"]["Value"] == "Protanopie":
            self.red_off_color = "gray"
            self.red_lit_color = "black"

        elif App.config["Mode daltonien"]["Value"] == "Deutéranopie":
            self.red_off_color = "gray"
            self.red_lit_color = "black"

        elif App.config["Mode daltonien"]["Value"] == "Tritanopie":
            self.blue_off_color = "gray"
            self.blue_lit_color = "black"


        self.defuse = False # Le module n'est pas désamorçer.
        self.Sequence = []
        self.MaxStep = 6
        for _ in range(self.MaxStep):
            self.Sequence.append(random.choice(["Up", "Left", "Right", "Down"]))

        self.Step = 0
        self.sequence_choice()

        self.bind(
        UpCmd = lambda: self.check(Button = "Up"),
        LeftCmd = lambda: self.check(Button = "Left"),
        RightCmd = lambda: self.check(Button = "Right"),
        DownCmd = lambda: self.check(Button = "Down"))

        self.Sequence_Button = [] # Séquence de bouton sur lesquels le joueur vient de cliqué


    def def_sequence(self):
        Difficulty = App.config["Difficulté"]["Value"] # Difficulté du jeu
        nomber_condition = len(self.rules[Difficulty])

        for index in range(nomber_condition): # boucle pour tester toute les conditions
            Condition = list(self.rules[Difficulty].keys())[index] # Condition pour utiliser le réarangement des touches
            Condition_split = Condition.split(" ")

            if Condition_split[0] != "Else": State_led = classModule["wire"].dico_wire[Condition_split[0]]["LIT"]
            else: State_led = Condition_split[-1]

            if (State_led == Condition_split[-1]): # regarder si le condition est bonne avec les LED
                self.rules_sequence = self.rules[Difficulty][Condition] # difinition de la bonne séquence
                break # On arrête la boucle car on a trouvé ce que l'on cherchait


    def reset_all(self):
            self.dico_but["Up"].config(background = self.green_off_color)
            self.dico_but["Left"].config(background = self.blue_off_color)
            self.dico_but["Right"].config(background = self.red_off_color)
            self.dico_but["Down"].config(background = self.yellow_off_color)


    def sequence_choice(self, frame = 0):
        if frame <= self.Step:
            self.Sequence_step = self.Sequence[frame]
            if self.Sequence_step == "Up": self.dico_but[self.Sequence_step].config(background = self.green_lit_color)
            elif self.Sequence_step == "Left": self.dico_but[self.Sequence_step].config(background = self.blue_lit_color)
            elif self.Sequence_step == "Right": self.dico_but[self.Sequence_step].config(background = self.red_lit_color)
            elif self.Sequence_step == "Down": self.dico_but[self.Sequence_step].config(background = self.yellow_lit_color)

        else:
            frame = -1

        Fen.after(1000, lambda: self.reset_all())
        self.Event_sequence = Fen.after(1500, lambda: self.sequence_choice(frame + 1))


    def check(self, Button):
        self.Sequence_Button.append(Button)
        Sequence_part = self.Sequence[:(self.Step + 1)]

        if len(self.Sequence_Button) >= len(Sequence_part): # Si le joueur a fait autant d'input qu'il y a de LED qui s'allument dans la séquence

            _Stop = False
            for index in range(len(Sequence_part)):
                if self.rules_sequence[Sequence_part[index]] != self.Sequence_Button[index]:
                    _Stop = True

            if not(_Stop):
                self.Step += 1

            else:
                classModule["display"].PenalityLife()

            self.Sequence_Button = []


        if self.Step >= self.MaxStep - 1: # Si le joueur a atteint la dernière étape
            self.defuse = True # la bombe est désamorçé.
            classModule["display"].checkDefuse()
            self.bind(LeftCmd = lambda: "pass", RightCmd = lambda: "pass", UpCmd = lambda: "pass", DownCmd = lambda: "pass")

    def reset(self):
        Fen.after_cancel(self.Event_sequence)
        self.bind(LeftCmd = lambda: "pass", RightCmd = lambda: "pass", UpCmd = lambda: "pass", DownCmd = lambda: "pass")


classModule["simon"] = simon()
