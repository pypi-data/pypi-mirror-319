from Full_Menu.screen import Screen
from Full_Menu.Parts import body, footer, header

class Menu(object):
    def __init__(self, head, body, footer, screen=None):
        if screen == None:
            self.screen = Screen()
        else: self.screen = screen

        self.head = head
        self.body = body
        self.footer = footer


    def show(self):
        h = self.head.show()
        b = self.body.show()
        f = self.footer.show()

        c = h + b + f
        lines = c.splitlines()
        num = len(lines)

        empty_space = self.screen.get_height() - num

        self.footer.empty_space(empty_space)

        f = self.footer.show()

        print(empty_space)

        print(h, end='')
        print(b, end='')
        print(f)
