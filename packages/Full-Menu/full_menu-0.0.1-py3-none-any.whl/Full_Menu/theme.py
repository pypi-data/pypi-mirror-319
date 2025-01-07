class Theme(object):
    def __init__(self, left, right, up, down, corners: list[str, str, str, str]):
        self.left = left 
        self.right = right
        self.up = up
        self.down = down
        self.t_left_corner = corners[0]
        self.t_right_corner = corners[1]
        self.b_left_corner = corners[2]
        self.b_right_corner = corners[3]
        self._render_top = True
        self._render_bottom = True

    def set_bottom(self, value):
        self._render_bottom = value

    def render_top(self, length):
        if self._render_top:
            # Create the top string
            out = self.t_left_corner + self.up * (length - 2) + self.t_right_corner + '\n'
            return out
        return ''

    def render_middle(self, empty=False, width=0, text=''):
        if width < 2:
            raise ValueError("Width must be at least 2 to render middle.")

        if empty:
            # Create an empty middle row
            out = self.left + ' ' * (width - 2) + self.right + '\n'
            return out
        else:
            # Center the text in the middle row
            if len(str(text.text)) > width - 2:
                raise ValueError(f"Text is too long for the given width: {text}, {len(str(text.text))}")

            padding = (width - 2 - len(text)) // 2
            out = self.left + ' ' * padding + str(text) + ' ' * (width - 2 - len(text) - padding) + self.right + '\n'
            return out

    def render_bottom(self, length):
        if self._render_bottom:
            # Create the bottom string
            out = self.b_left_corner + self.down * (length - 2) + self.b_right_corner
            return out
        return ''

