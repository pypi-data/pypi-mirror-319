from Full_Menu.text import Text
from Full_Menu.theme import Theme

class Footer(object):
    def __init__(self, text: Text, theme: Theme, width, height):
        self.text = text
        self.theme = theme

        self.width = width
        self.height = height

        self.content = self.preload()

    def preload(self, empty=0):
        if self.height < 5:
            print("ERROR: HEIGHT TOO SMALL")
            raise Exception

        width = self.width
        self.theme.render_bottom(False)
        content = ''
        content += self.theme.render_top(width)
        content += self.theme.render_middle(True, width)
        content += self.theme.render_middle(False, width, self.text)
        content += self.theme.render_middle(True, width)
        for i in range(empty):
            content += self.theme.render_middle(True, width)
        content += self.theme.render_bottom(width)

        print("----->  " + content)

        return content
    
    def show(self):
        return self.content

    def empty_space(self, empty):
        if empty >= 1:
            self.content = self.preload(empty - 1)
        