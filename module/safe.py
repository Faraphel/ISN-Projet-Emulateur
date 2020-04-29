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


        self.frame = LabelFrame(Fen, text = "Coffre-fort", width = 180, height = 180, borderwidth = 4) # On créer une sous-fenêtre
        self.frame.grid(row = 1, column = 3, sticky = "NEWS") # On l'affiche

        self.frame.grid_propagate(0) # Force le LabelFrame à ne pas changer de taille

        self.frame.grid_columnconfigure(1, weight = 1)


        self.label = Label(self.frame, text = "", background = "lightgray", relief = SUNKEN, width = 2, height = 1) # On créer la led
        self.label.grid(row = 1, column = 1)

        ###########
        self.size_canvas = 90

        self.canvas = Canvas(self.frame, width = self.size_canvas, height = self.size_canvas)
        self.canvas.grid(row = 2, column = 1)

        self.mult_base = 6
        # Cercle sur lequel va tourner la base
        self.cache_canvas = self.canvas.create_oval(
                                (self.size_canvas / 2) - (self.size_canvas / self.mult_base), # Ax
                                (self.size_canvas / 2) - (self.size_canvas / self.mult_base), # Ay
                                (self.size_canvas / 2) + (self.size_canvas / self.mult_base), # Bx
                                (self.size_canvas / 2) + (self.size_canvas / self.mult_base), # By

                                fill = "gray12")

        # Cercle sur lequel va tourner le pic

        for index in range(4):
            self.canvas.create_arc( 2, self.size_canvas, # A(x, y)
                                    self.size_canvas, 2, # B(x, y)

                                    start = 90 * (index + 1), extent = 90, # ici en dégrée
                                    fill = "lightgray", outline = "black", width = 1)


            self.canvas.create_text((self.size_canvas / 2) + (self.size_canvas / 4.5) * round(math.cos((index) * (math.pi / 2) + math.sqrt(2)/2 + math.pi/2)) + 2,
                                    (self.size_canvas / 2) - (self.size_canvas / 4.5) * round(math.sin((index) * (math.pi / 2) + math.sqrt(2)/2 + math.pi/2)) + 2,
                                    text = str(index + 1), font = ("Arial Black", 15), angle = 225 + 90 * (index))


        ##########

        self.scale = Scale(self.frame, from_ = 0.01, to_ = 4, orient = HORIZONTAL, width = 10, showvalue = False, resolution = 0.01) # On créer un scroller pour sélectionner une valeur entre 1 et 4
        self.scale.grid(row = 3, column = 1, sticky = "S")

        self.Valid_but = Button(self.frame, text = "Valider", background = "lightgreen", relief = RIDGE, width = 10)
        self.Valid_but.grid(row = 4, column = 1)

        self.position_curseur = 0.01
        self.Event = None
        self.updateCanvas()

    def updateCanvas(self):
        angle = (self.position_curseur - 1) / (4/(2*math.pi)) + math.pi


        if self.Event != None: self.canvas.delete(self.Event)
        self.Event = self.canvas.create_polygon((self.size_canvas / 2) - (self.size_canvas / self.mult_base) * math.sin(angle),
                                                (self.size_canvas / 2) - (self.size_canvas / self.mult_base) * math.cos(angle),

                                                (self.size_canvas / 2) + (self.size_canvas / self.mult_base) * math.sin(angle),
                                                (self.size_canvas / 2) + (self.size_canvas / self.mult_base) * math.cos(angle),

                                                (self.size_canvas / 2) + (self.size_canvas / 2) * math.cos(angle),
                                                (self.size_canvas / 2) - (self.size_canvas / 2) * math.sin(angle),

                                                fill = "orange", outline = "black", width = 2)

        self.canvas.tag_raise(self.cache_canvas)


    def start(self):
        self.defuse = False # Le module n'est pas désamorçé.
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
        self.updateCanvas()
        if self.scale_zone[self.Step] == math.ceil(self.position_curseur):
            self.label.config(background = "yellow")
        else:
            self.label.config(background = "lightgray")


    def check(self):
        Difficulty = App.config["Difficulté"]["Value"]
        Step_max = len(self.rules[Difficulty])

        if self.rules[Difficulty][self.Step + 1][self.scale_zone[self.Step]] == math.ceil(self.position_curseur): # Si le joueur à bien placé le curseur
            self.Step += 1
            if self.Step >= Step_max: # Si à la dernière étape
                self.defuse = True
                classModule["display"].checkDefuse()
                self.Valid_but.config(command = lambda: "pass")
            else:
                self.zone_choice()

        else:
            classModule["display"].PenalityLife()


    def reset(self):
        self.label.config(background = "lightgray") # On éteint la LED
        self.scale.config(command = lambda x: "pass") # Désactive la mise à jour du curseur
        self.Valid_but.config(command = lambda: "pass") # Désactive le bouton


classModule["safe"] = safe()
