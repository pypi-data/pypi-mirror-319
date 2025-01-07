class Function(object):
    def __init__(self, text, command):
        self.command = command
        self.text = text

    def get_text(self):
        return self.text
    
    def get_command(self):
        return self.command