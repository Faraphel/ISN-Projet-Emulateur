class button():
    def __init__(self): # Cette fonction est automatiquement éxécuter lors de la création de l'objet
        self.rules = {
            "Facile": {
                "Else": "None"
            }, "Normal": {
                "F Blink": "3 any",
                "F Off": "7 any",
                "F On": "0 any"
            }, "Difficile": {
                "D Blink": "3 any",
                "A Off": "7 any",
                "B On": "0 any",
                "F Blink": "5 sec",
                "B Blink": "5 sec",
                "C On": "3 sec",
                "Else": "None"
            }
        }

        self.frame = LabelFrame(Fen, text = "Button") # On créer une sous-fenêtre
        self.frame.grid(row = 2, column = 3, sticky = "NEWS") # On l'affiche

        self.big_but = Button(self.frame, text = "", background = "lightgray", width = 8, height = 5, relief = GROOVE) # On créer le boutton du haut
        self.big_but.grid(row = 1, column = 1)



    def start(self):
        self.defuse = False
        self.big_but.config(command = self.check)


    def def_condition(self):
        Difficulty = App.config["Difficulté"]["Value"]
        Condition = list(self.rules[Difficulty].keys())

        for index in range(len(Condition)):
            Condition_split = Condition[index].split(" ")

            if Condition_split[0] != "Else": State_led = classModule["wire"].dico_wire[Condition_split[0]]["LIT"] # Si la condition n'est pas else, on récupère l'état de la LED
            else: State_led = Condition_split[-1] # Sinon, on fait en sorte que la condition fonctionne obligatoirement.

            if State_led == Condition_split[-1]:
                self.rules_chrono = self.rules[Difficulty][Condition[index]]
                break


    def check(self):
        second = classModule["display"].second
        minute = classModule["display"].minute

        rules_chrono_split = self.rules_chrono.split(" ")

        _Stop = False

        if rules_chrono_split[0] != "None":
            if rules_chrono_split[1] == "any":
                if not(rules_chrono_split[0] in str(minute) + str(second)):
                    _Stop = True

            if rules_chrono_split[1] == "sec":
                if not(rules_chrono_split[0] in str(second)[-1]):
                    _Stop = True


        if not(_Stop):
            self.defuse = True
            classModule["display"].checkDefuse()

        else:
            classModule["display"].PenalityLife()


classModule["button"] = button()

# 2 - Le bouton doit être relié à la fonction "check"
# 3 - On vérifie que la condition est respecté
