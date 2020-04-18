class display():
    def __init__(self): # Cette fonction est automatiquement éxécuter lors de la création de l'objet
        self.defuse = True # Ce module est toujours désamorçé.

        self.frame = LabelFrame(Fen, text = "Display") # On créer une sous-fenêtre
        self.frame.grid(row = 1, column = 1, sticky = "NEWS") # On l'affiche

        self.label = Label(self.frame, text = "ici on affichera le texte")
        self.label.grid(row = 1, column = 1, sticky = "NEWS")

    def write(self, text):
        self.label.config(text = text)


    def chrono(self, time):
        minute = time // 60
        seconde = time % 60

        self.write("%02i:%02i" % (minute, seconde))

        self.chrono_event = Fen.after(1000, lambda: self.chrono(time - 1))


    def start(self):
        self.chrono(time = 180)
        # rien de spécial
        # peut être chrono


classModule["display"] = display()
