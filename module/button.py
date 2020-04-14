class button():
    def __init__(self): # Cette fonction est automatiquement éxécuter lors de la création de l'objet
        self.frame = LabelFrame(Fen, text = "Button") # On créer une sous-fenêtre
        self.frame.grid(row = 2, column = 3, sticky = "NEWS") # On l'affiche

        self.big_but = Button(self.frame, text = "", background = "lightgray", width = 8, height = 5, relief = GROOVE) # On créer le boutton du haut
        self.big_but.grid(row = 1, column = 1)


classModule["button"] = button()
