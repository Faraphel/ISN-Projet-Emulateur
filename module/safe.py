class safe():
    def __init__(self): # Cette fonction est automatiquement éxécuter lors de la création de l'objet
        self.frame = LabelFrame(Fen, text = "Safe") # On créer une sous-fenêtre
        self.frame.grid(row = 1, column = 3, sticky = "NEWS") # On l'affiche

        self.label = Label(self.frame, text = "", background = "lightgray", relief = SUNKEN, width = 2, height = 1) # On créer la led
        self.label.grid(row = 1, column = 1)

        self.scale = Scale(self.frame, from_ = 1, to_ = 4, orient = HORIZONTAL) # On créer un scroller pour sélectionner une valeur entre 1 et 4
        self.scale.grid(row = 2, column = 1)


    def start(self):
        pass
        # Code qui choisi des combinaisons à rentré


classModule["safe"] = safe()
