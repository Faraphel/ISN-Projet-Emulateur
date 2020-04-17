class safe():
    def __init__(self): # Cette fonction est automatiquement éxécuter lors de la création de l'objet
        self.rules = {
            "Facile": {
                1: {1: 3, 2: 2, 3: 1, 4: 4}, # Nb Etape : {Si led X allumé : selectionné led Y, ...}
                2: {1: 4, 2: 3, 3: 2, 4: 1},
                3: {1: 3, 2: 1, 3: 4, 4: 2}
            }, "Normal": {
                1: {1: 2, 2: 1, 3: 3, 4: 4},
                2: {1: 1, 2: 2, 3: 4, 4: 3},
                3: {1: 4, 2: 3, 3: 2, 4: 1},
                4: {1: 2, 2: 4, 3: 1, 4: 3},
                5: {1: 3, 2: 1, 3: 4, 4: 2},
                6: {1: 3, 2: 2, 3: 1, 4: 4}
            }, "Difficile": {
                1: {1: 2, 2: 4, 3: 1, 4: 3},
                2: {1: 4, 2: 1, 3: 2, 4: 3},
                3: {1: 1, 2: 3, 3: 4, 4: 2},
                4: {1: 1, 2: 2, 3: 4, 4: 3},
                5: {1: 3, 2: 2, 3: 1, 4: 4},
                6: {1: 4, 2: 3, 3: 2, 4: 1},
                7: {1: 4, 2: 2, 3: 3, 4: 1},
                8: {1: 2, 2: 1, 3: 3, 4: 4},
                9: {1: 3, 2: 4, 3: 1, 4: 2}
            }
        }


        self.frame = LabelFrame(Fen, text = "Safe") # On créer une sous-fenêtre
        self.frame.grid(row = 1, column = 3, sticky = "NEWS") # On l'affiche

        self.label = Label(self.frame, text = "", background = "lightgray", relief = SUNKEN, width = 2, height = 1) # On créer la led
        self.label.grid(row = 1, column = 1)

        self.scale = Scale(self.frame, from_ = 1, to_ = 4, orient = HORIZONTAL) # On créer un scroller pour sélectionner une valeur entre 1 et 4
        self.scale.grid(row = 2, column = 1)

        self.Valid_but = Button(self.frame, text = "Validé", background = "lightgreen", relief = RIDGE)
        self.Valid_but.grid(row = 3, column = 1)


    def start(self):
        self.defuse = False # Le module n'est pas désamorçer.
        self.Step = 0
        self.position_curseur = 0

        self.scale.config(command = lambda event: self.zone_choice())
        self.Valid_but.config(command = lambda: self.check())
        self.scale_zone = []

        for _ in range(9):
            self.scale_zone.append(random.choice([1, 2, 3, 4])) # Valeur que le joueur doit sélectionner avec le curseur

        self.zone_choice()



    def zone_choice(self): # S'enclenche quand le joueur touche au curseur
        self.position_curseur = self.scale.get() # Valeur sélectionner avec le curseur

        if self.scale_zone[self.Step] == self.position_curseur:
            self.label.config(background = "yellow")
        else:
            self.label.config(background = "lightgray")

    def check(self):
        Difficulty = App.config["Difficulté"]["Value"]
        Step_max = len(self.rules[Difficulty])

        if self.rules[Difficulty][self.Step + 1][self.scale_zone[self.Step]] == self.position_curseur: # Si le joueur à bien placé le curseur
            self.Step += 1
            if self.Step >= Step_max: # Si à la dernière étape
                self.defuse = True
                print("DEFUSER")
            else:
                self.zone_choice()

        else: print("FAUX")
        # +pénaliter si le nombre d'erreur autorisé est atteint donc enlever une vie








        # Code qui choisi des combinaisons à rentré


classModule["safe"] = safe()
