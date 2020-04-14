class wire():
    def __init__(self): # Cette fonction est automatiquement éxécuter lors de la création de l'objet
        self.frame = LabelFrame(Fen, text = "Wire") # On créer une sous-fenêtre
        self.frame.grid(row = 1, column = 2, sticky = "NEWS") # On l'affiche

        self.dico_wire = {} # On créer un dictionnaire vide qui va contenir tout les éléments

        for index, led in enumerate("ABCDEF"): # Il y a 6 câbles différents nommé par ces lettres
            self.dico_wire[led] = {} # On les tries par leur lettre associé

            self.dico_wire[led]["ID"] = Label(self.frame, text = led) # Affichage de la lettre du fil
            self.dico_wire[led]["ID"].grid(row = index, column = 0)

            self.dico_wire[led]["LED"] = Label(self.frame, text = "", background = "lightgray", relief = SUNKEN, width = 2, height = 1) # Affichage de la led
            self.dico_wire[led]["LED"].grid(row = index, column = 1)

            self.dico_wire[led]["WIRE"] = Button(self.frame, text = "---------------------", relief = FLAT) # Affichage du fil coupable
            self.dico_wire[led]["WIRE"].grid(row = index, column = 2)


    def start(self):
        print("les fils sont oppérationnels")
        # Code qui choisi des led qui doivent s'allumé, etc...


classModule["wire"] = wire() # On ajoute le module à la liste des modules
