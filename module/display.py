class display():
    def __init__(self):
        self.frame = LabelFrame(Fen, text = "Display") # On créer une sous-fenêtre
        self.frame.grid(row = 1, column = 1, sticky = "NEWS") # On l'affiche

        self.label = Label(self.frame, text = "ici on affichera le texte")
        self.label.grid(row = 1, column = 1, sticky = "NEWS")


classModule["display"] = display()