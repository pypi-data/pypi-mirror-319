from Full_Menu.text import Text
from Full_Menu.theme import Theme

class Header(object):
    def __init__(self, text: Text, theme: Theme, width, height):
        self.text = text
        self.theme = theme

        self.content = self.preload(width, height)

    def preload(self, width, height):
        if height < 5:
            print("ERROR: HEIGHT TOO SMALL")
            raise Exception
        self.theme.render_bottom(False)
        content = ''
        content += self.theme.render_top(width)
        content += self.theme.render_middle(True, width)
        content += self.theme.render_middle(False, width, self.text)
        content += self.theme.render_middle(True, width)
        content += self.theme.render_bottom(width)

        return content
    
    def show(self):
        return self.content