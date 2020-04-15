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

            self.dico_wire[led]["CUT"] = False


    def start(self): # Code qui choisi des led qui doivent s'allumé, etc...
        for wire in self.dico_wire: # Pour chaque câbles, ...
            self.dico_wire[wire]["WIRE"].config(command = lambda led = "%s" % wire: self.cut_wire(led = led)) # ... On le rend sécable.

            self.dico_wire[wire]["LIT"] = random.choice(["Off", "On", "Blink"])
            if self.dico_wire[wire]["LIT"] == "On":
                self.dico_wire[wire]["LED"].config(background = "yellow")
            if self.dico_wire[wire]["LIT"] == "Blink":
                self.dico_wire[wire]["LED"].config(background = "green")



    def cut_wire(self, led): #coupe les cables
        self.dico_wire[led]["WIRE"].config(command = lambda: "pass")
        self.dico_wire[led]["WIRE"].config(text = "---------   ---------")

        self.dico_wire[led]["CUT"] = True

        self.check()


    def check(self): # Fonction qui vérifie si les câbles ont bien été coupé selon le manuel
        self.rules = {
            "Facile": {
                "A": {"Off": False, "On": False, "Blink": True},
                "B": {"Off": True, "On": False, "Blink": False},
                "C": {"Off": False, "On": True, "Blink": False},
                "D": {"Off": True, "On": True, "Blink": True},
                "E": {"Off": True, "On": False, "Blink": True},
                "F": {"Off": False, "On": False, "Blink": False}
            }, "Normal": {
                "A": {"Off": "C Blink", "On": False, "Blink": True},
                "B": {"Off": False, "On": False, "Blink": "E Off"},
                "C": {"Off": True, "On": "F Off", "Blink": True},
                "D": {"Off": True, "On": False, "Blink": "A Blink"},
                "E": {"Off": False, "On": "B On", "Blink": True},
                "F": {"Off": True, "On": True, "Blink": False}
            }, "Difficile": {
                "A": {"Off": "B Blink", "On": False, "Blink": True},
                "B": {"Off": "A On", "On": True, "Blink": "D Off"},
                "C": {"Off": False, "On": "E Off", "Blink": "F Blink"},
                "D": {"Off": "C Blink", "On": False, "Blink": False},
                "E": {"Off": True, "On": "A On", "Blink": "B On"},
                "F": {"Off": "A Blink", "On": "E Off", "Blink": True}
            }
        } # Règles du manuel transcrite dans le code

        Difficulty = App.config["Difficulté"]["Value"]

        for wire in self.dico_wire:
            lit_wire = self.dico_wire[wire]["LIT"]

            if type(self.rules[Difficulty][wire][lit_wire]) == str: # Si la condition est un texte (donc du type LED StatutDeLaLED):
                condition = self.rules[Difficulty][wire][lit_wire].split(" ")
                if self.dico_wire[wire]["CUT"] == (self.dico_wire[condition[0]]["LIT"] == condition[1]): # Si la règle est aussi bien respecté que la condition
                    pass # Code éxécuté si le joueur à réussi
                else:
                    pass # Code éxécuté si le joueur à échoué

            else:
                if self.dico_wire[wire]["CUT"] == self.rules[Difficulty][wire][lit_wire]:
                    pass # Code éxécuté si le joueur à réussi
                else:
                    pass # Code éxécuté si le joueur à échoué


        # Si oui : cable désamorçer
        # Si non : Erreur


classModule["wire"] = wire() # On ajoute le module à la liste des modules
