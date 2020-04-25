class morse():
    def __init__(self): # Cette fonction est automatiquement éxécuter lors de la création de l'objet
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
            'VICTOIRE': 11, 'WEEKEND': 9, 'XENOPHOBE': 5, 'YOGA': 2, 'ZEN': 9
            }

        self.MorseLetter = {
            "A": ".-", "B":"-...", "C":"-.-.", "D":"-..", "E":".", "F":"..-.", "G":"--.",
            "H":"....", "I":"..", "J":".---", "K":"-.-", "L":"--.", "M":"--", "N":"-.",
            "O":"---", "P":".--.", "Q":"--.-", "R":".-.", "S":"...", "T":"-", "U":"..-",
            "V":"...-", "W":".--", "X":"-..-", "Y":"-.--", "Z":"--.."
            }

        self.frame = LabelFrame(Fen, text = "Morse", width = 180, height = 180, borderwidth = 4) # On créer une sous-fenêtre
        self.frame.grid(row = 2, column = 2, sticky = "NEWS") # On l'affiche

        self.frame.grid_propagate(0) # Force le LabelFrame à ne pas changer de taille

        self.frame.grid_rowconfigure(1, weight = 1) # tout les objets seront centré horizontalement
        self.frame.grid_columnconfigure(1, weight = 1) # tout les objets seront centré verticalement

        self.morse = Label(self.frame, text = "", background = "lightgray", relief = SUNKEN, width = 2, height = 1)
        self.morse.grid(row = 1, column = 1)

        self.SelectButton = Button(self.frame, text = "", relief = RIDGE, width = 16, height = 3)
        self.SelectButton.grid(row = 2, column = 1, sticky = "WE")

        self.SelectFen = Toplevel() # Créer une fenêtre secondaire.
        self.SelectFen.resizable(width = False, height = False)
        self.SelectFen.iconbitmap(PATH_ASSETS + "icon.ico") # Change l'icone
        self.SelectFen.title("Emulateur - Morse") # Change le titre
        self.SelectFen.protocol('WM_DELETE_WINDOW', lambda: "pass") # Rend la fenêtre non fermable
        self.HideSymbol()

        self.ready = Label(self.SelectFen, text = "Lancer une partie pour\nafficher les symboles")
        self.ready.grid(row = 1, column = 1)


    def start(self):
        self.defuse = False
        self.SelectButton.config(command = self.ShowSymbol)
        # mot à afficher en morse

        ######
        self.ready.grid_forget()
        Img_random = list(range(1, 13)) # On créer une liste allant de 1 à 12
        random.shuffle(Img_random) # On la mélange
        self.dico_PNG = {} # On créer un dico pour garder en mémoire toute les images
        self.dico_But = {}
        for index, Num_img in enumerate(Img_random): # On les affiches toutes dans des bouttons
            self.dico_PNG[Num_img] = ImageTk.PhotoImage(Image.open(PATH_ASSETS + "morse/" + str(Num_img) + ".png"))
            self.dico_But[Num_img] = Button(self.SelectFen, image = self.dico_PNG[Num_img], width = 200, height = 200, command = lambda x = Num_img: self.check(x))
            self.dico_But[Num_img].grid(row = index // 3, column = index % 3)

        self.SelectFen.update()
        ######

        ######
        self.word = random.choice(list(self.MorseWordTable.keys())) # On prend un mot au pif dans la liste

        List_letter = []
        for Letter in self.word:
            List_letter.append(self.MorseLetter[Letter])

        self.word_morse = " ".join(List_letter)
        ######

        self.LedMorse()

        self.True_symbol = self.MorseWordTable[self.word]


    def LedMorse(self, index = 0): # Responsable de l'affichage du mot en morse avec la LED

        if index < len(self.word_morse):

            if self.word_morse[index] == ".":
                self.morse.config(background = "yellow")
                Fen.after(250, lambda: self.morse.config(background = "lightgray"))
                self.Led_event = Fen.after(750, lambda: self.LedMorse(index + 1)) # 500 ms d'attente entre les signaux, plus les 250ms ou elle reste allumé afin de séparer les points et les virgules entre eux

            elif self.word_morse[index] == "-":
                self.morse.config(background = "yellow")
                Fen.after(1000, lambda: self.morse.config(background = "lightgray"))
                self.Led_event = Fen.after(1500, lambda: self.LedMorse(index + 1))

            elif self.word_morse[index] == " ":
                self.Led_event = Fen.after(2000, lambda: self.LedMorse(index + 1))

        else:
            self.Led_event = Fen.after(4000, lambda: self.LedMorse(index = 0))



    def ShowSymbol(self): # Affiche la fenêtre de sélection
        self.SelectFen.deiconify() # Affiche la fenêtre de sélection
        self.SelectButton.config(command = self.HideSymbol, text = "Cacher les cartes")

    def HideSymbol(self): # Affiche la fenêtre de sélection
        self.SelectFen.withdraw() # Cache la fenêtre de sélection
        self.SelectButton.config(command = self.ShowSymbol, text = "Afficher les cartes")


    def check(self, symbol_press):
        if symbol_press == self.True_symbol:
            self.defuse = True
            classModule["display"].checkDefuse()
            for index in self.dico_But:
                self.dico_But[index].config(command = lambda: "pass")

        else:
            classModule["display"].PenalityLife()


    def reset(self):
        self.morse.config(background = "lightgray")
        for Num_img in self.dico_But:
            self.dico_But[Num_img].destroy()

        self.ready.grid(row = 1, column = 1)
        Fen.after_cancel(self.Led_event)


classModule["morse"] = morse()
