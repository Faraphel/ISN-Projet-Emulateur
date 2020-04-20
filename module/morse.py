class morse():
    def __init__(self): # Cette fonction est automatiquement éxécuter lors de la création de l'objetself.Complete = False
        self.PATH_SYMBOL = "./assets/morse/"
        self.MorseWordTable = {
            'ABSTRAIT': 3, 'BAIGNER': 9, 'CACHOT': 10, 'DALLE': 2, 'ERREUR': 11, 'FLEUR': 6,
            'GALLAIS': 8, 'HANCHE': 4, 'IDOLE': 1, 'JAPON': 5, 'KART': 8, 'LAIT': 11, 'MACRO': 4,
            'NAVET': 10, 'OBJET': 4, 'PUIT': 10, 'QUEL': 11, 'RUELLE': 12, 'SANS': 9, 'TABLE': 8,
            'ULTRA': 3, 'VACHE': 12, 'WAGON': 5, 'XYLENE': 3, 'YAOURT': 8, 'ZAFARI': 12,
            'AMBRE': 4, 'BUCHE': 9, 'COFFRE': 7, 'DOIGT': 4, 'EFFET': 12, 'FIL': 7, 'GRENADE': 1,
            'HOTEL': 11, 'IDEAL': 10, 'JOUET': 5, 'KAYAK': 5, 'LAMPE': 2, 'MANOIR': 3, 'NEZ': 6,
            'OCEAN': 5, 'PETIT': 1, 'QUINTE': 4, 'RIRE': 1, 'SUIVRE': 7, 'TETE': 5, 'USINE': 6,
            'VIVRE': 3, 'WIKI': 10, 'XYLOPHONE': 7, 'YEUX': 6, 'ZINC': 2, 'ANIMAL': 2, 'BEBE': 1,
            'CUIVRE': 3, 'DORMIR': 2, 'EFFECTIF': 8, 'FABULEUX': 3, 'GRANDE': 12, 'HAUTEUR': 7,
            'IDEE': 7, 'JOIE': 12, 'KOALA': 6, 'LOUP': 4, 'MOUCHE': 1, 'NOUS': 9, 'ORANGE': 11,
            'POULET': 8, 'QUICHE': 6, 'RITUEL': 12, 'SAUCE': 10, 'TUILE': 9, 'UTILE': 2,
            'VICTOIRE': 11, 'WEEKEND': 9, 'XENOPHOBE': 5, 'YOGA': 2, 'ZEN': 9}

            ABCDEFGHIJKLMNOPQRSTUVWXYZ

        self.MorseLetter = {
            "A": ".-", "B":"-...", "C":"-.-.", "D":"-..", "E":".", "F":"..-.", "G":"--.",
            "H":"....", "I":"..", "J":".---", "K":"-.-", "L":"--.", "M":"--", "N":"-.",
            "O":"---", "P":".--.", "Q":"--.-", "R":".-.", "S":"...", "T":"-", "U":"..-",
            "V":"...-", "W":".--", "X":"-..-", "Y":"-.--", "Z":"--.."}

        self.frame = LabelFrame(Fen, text = "Morse") # On créer une sous-f  enêtre
        self.frame.grid(row = 2, column = 2, sticky = "NEWS") # On l'affiche

        self.frame.grid_rowconfigure(1, weight = 1) # tout les objets seront centré horizontalement
        self.frame.grid_columnconfigure(1, weight = 1) # tout les objets seront centré verticalement


        self.morse = Label(self.frame, text = "", background = "lightgray", relief = SUNKEN, width = 2, height = 1)
        self.morse.grid(row = 1, column = 1)

        self.SelectButton = Button(self.frame, text = "", relief = RIDGE, width = 16, height = 3)
        self.SelectButton.grid(row = 2, column = 1)

        self.SelectFen = Toplevel() # Créer une fenêtre secondaire.
        self.HideSymbol()

    def start(self):
        self.defuse = False
        self.SelectButton.config(command = self.ShowSymbol)
        # mot à afficher en morse

    def ShowSymbol(self):
        self.SelectFen.deiconify() # Affiche la fenêtre de sélection
        self.SelectButton.config(command = self.HideSymbol, text = "Cacher les cartes")

    def HideSymbol(self):
        self.SelectFen.withdraw() # Cache la fenêtre de sélection
        self.SelectButton.config(command = self.ShowSymbol, text = "Afficher les cartes")


classModule["morse"] = morse()

# 1 - Charger les images
# 2 - Afficher les images dans un ordre aléatoire (afin de ne pas avoir d'exploit avec leur position)
# 3 - Faire choisir un mot aléatoirement et l'afficher en morse
# 4 - Rendre la sélection des mots effectives
# 5 - Vérifier si le joueur à donné la bonne réponse
