class morse():
    def __init__(self): # Cette fonction est automatiquement éxécuter lors de la création de l'objet
        self.frame = LabelFrame(Fen, text = "Morse") # On créer une sous-fenêtre
        self.frame.grid(row = 2, column = 2, sticky = "NEWS") # On l'affiche

        self.frame.grid_rowconfigure(1, weight = 1) # tout les objets seront centré horizontalement
        self.frame.grid_columnconfigure(1, weight = 1) # tout les objets seront centré verticalement


        self.morse = Label(self.frame, text = "", background = "lightgray", relief = SUNKEN, width = 2, height = 1)
        self.morse.grid(row = 1, column = 1)




classModule["morse"] = morse()
