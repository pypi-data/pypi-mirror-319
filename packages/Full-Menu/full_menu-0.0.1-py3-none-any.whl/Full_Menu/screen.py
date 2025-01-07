import os
import subprocess
import platform

class Screen(object):
    def __init__(self):
        self.resize()

    def fill(self, character: str):
        """
        Test function to fill the screen
        """
        for y in range(self.height):
            for x in range(self.width):
                print(character, end='')
            print(' ')

    def clear(self):
        """
        Clears The screen
        """
        if platform.system() == "Windows":
            subprocess.check_call('cls', shell=True)
        else:
            print(subprocess.check_output('clear').decode())

    def resize(self):
        size = os.get_terminal_size()
        self.width =  size.columns
        self.length = size.lines

    def get_width(self):
        return self.width

    def get_height(self):
        return self.length


