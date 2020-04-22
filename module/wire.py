class wire():
    def __init__(self): # Cette fonction est automatiquement éxécuter lors de la création de l'objet
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
        self.defuse = False # Le module n'est pas désamorçer.

        for wire in self.dico_wire: # Pour chaque câbles, ...
            self.dico_wire[wire]["WIRE"].config(command = lambda led = "%s" % wire: self.cut_wire(led = led)) # ... On le rend sécable.

            self.dico_wire[wire]["LIT"] = random.choice(["Off", "On", "Blink"])
            if self.dico_wire[wire]["LIT"] == "On":
                self.dico_wire[wire]["LED"].config(background = "yellow")
            if self.dico_wire[wire]["LIT"] == "Blink":
                self.dico_wire[wire]["LED"].config(background = "green")


        self.wrong_cut = 0 # Compte le nombre de fils que le joueur n'aurait dû pas coupé avant
        self.check(penality = False) # On compte le nombre de fil à corrigé pour les pénalités plus tard

        if "simon" in classModule: classModule["simon"].def_sequence() # Puisque le module "simon" a besoin de l'état des LEDs pour fonctionner, on l'éxécute après leur définition
        if "button" in classModule: classModule["button"].def_condition() # Puisque le module "button" a besoin de l'état des LEDs pour fonctionner, on l'éxécute après leur définition


    def cut_wire(self, led): #coupe les cables
        self.dico_wire[led]["WIRE"].config(command = lambda: "pass")
        self.dico_wire[led]["WIRE"].config(text = "---------   ---------")

        self.dico_wire[led]["CUT"] = True

        self.check()


    def check(self, penality = True): # Fonction qui vérifie si les câbles ont bien été coupé selon le manuel
        Difficulty = App.config["Difficulté"]["Value"]

        self.wire_errorTotal = 0 # Compte le nombre de fils en mauvais état

        for wire in self.dico_wire:
            lit_wire = self.dico_wire[wire]["LIT"]

            if type(self.rules[Difficulty][wire][lit_wire]) == str: # Si la condition est un texte (donc du type LED StatutDeLaLED):
                condition = self.rules[Difficulty][wire][lit_wire].split(" ")
                if self.dico_wire[wire]["CUT"] != (self.dico_wire[condition[0]]["LIT"] != condition[1]): # Si la règle n'est pas respecté
                    self.wire_errorTotal += 1

            else:
                if self.dico_wire[wire]["CUT"] != self.rules[Difficulty][wire][lit_wire]: # Si la règle n'est pas respecté
                    self.wire_errorTotal += 1



        if penality: # Si on compte les pénalité, alors on fait ces calculs
            if self.wire_errorTotalBefore - self.wire_errorTotal == -1: # Si le fil à mal été coupé
                self.wrong_cut += 1
                classModule["display"].PenalityLife()


        if self.wire_errorTotal - self.wrong_cut == 0: # Si le joueur à tout désamorçer, en comptant les fils qu'ils n'auraient pas du coupé
            self.defuse = True
            classModule["display"].checkDefuse()
            for led in self.dico_wire: # On rend les câbles insécable de nouveau pour évité une nouvelle erreur
                self.dico_wire[led]["WIRE"].config(command = lambda: "pass")
            # + Rajouter le bonus de temps


        self.wire_errorTotalBefore = self.wire_errorTotal


        # Si tout les fils ont été coupé correctement, alors le module est considéré comme étant désamorçer module.defuse = True
        # Si une erreur est détecté, on vérifie si elle vient du fait que l'on a mal coupé le fil où si c'est le reste des câbles à désamorçer



classModule["wire"] = wire() # On ajoute le module à la liste des modules
