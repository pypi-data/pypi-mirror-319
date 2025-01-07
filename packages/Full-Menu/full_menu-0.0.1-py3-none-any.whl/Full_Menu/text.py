class Text(object):
    def __init__(self, text, colour='defualt'):
        self.text = text
        
        colours = {
            "red": "\033[31m",
            "orange": "\033[38;5;208m",
            "yellow": "\033[33m",
            "green": "\033[32m",
            "blue": "\033[34m",
            "pink": "\033[38;5;213m",
            "defualt": "\033[0m"
        }

        self.reset = colours["defualt"]

        self.colour = colours[colour]

    def __str__(self):
        return f"{self.colour}{self.text}{self.reset}"
    
    def __len__(self):
        return len(self.text)
    
    def get_text(self):
        return self.text