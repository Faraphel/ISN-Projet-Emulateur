class simon():
    def __init__(self): # Cette fonction est automatiquement éxécuter lors de la création de l'objet
        self.frame = LabelFrame(Fen, text = "Simon") # On créer une sous-fenêtre
        self.frame.grid(row = 2, column = 1, sticky = "NEWS") # On l'affiche

        self.dico_but = {} # On créer un dictionnaire qui va contenir les objets bouttons.

        self.dico_but["Up"] = Button(self.frame, text = "", background = "lightgreen", width = 2, height = 1) # On créer le boutton du haut
        self.dico_but["Up"].grid(row = 2, column = 2)

        self.dico_but["Left"] = Button(self.frame, text = "", background = "lightblue", width = 2, height = 1) # On créer le boutton à gauche
        self.dico_but["Left"].grid(row = 3, column = 1)

        self.dico_but["Right"] = Button(self.frame, text = "", background = "indianred", width = 2, height = 1) # On créer le boutton à droite
        self.dico_but["Right"].grid(row = 3, column = 3)

        self.dico_but["Down"] = Button(self.frame, text = "", background = "lightyellow", width = 2, height = 1)  # On créer le boutton en bas
        self.dico_but["Down"].grid(row = 4, column = 2)



classModule["simon"] = simon()
