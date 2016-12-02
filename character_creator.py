# character_creator.py
# Thorin Schmidt
# 11/29/2016

''' GUI-based character generator'''

import tkinter as tk
import character as ch
import monster as mon

TITLE_FONT = ("Helvetica", 18, "bold")
HEADING1_FONT = ("Helvetica", 14, "bold")
SIMPLE_MESSAGE = "The user is asked which stat(str, dex, con, int, wis, cha) "+\
                "is most important, and which is least.  most important gets "+\
                "a value of 17, least gets a 9, and the rest get 12. This " +\
                "method is suitable for a 20-point character build using " +\
                "Pathfinder d20 rules.  This method has only a few choices, " +\
                "and results in moderate satisfaction for the user."
HARDCORE_MESSAGE = "Results are generated randomly using the 3d6 method, "+\
                   "in standard stat block sequence: (str, dex, con, int, "+\
                   "wis, cha). If none of the stats are over 12, then the "+\
                   "entire set is re-rolled until it does. The user has no "+\
                   "control over ability scores. This method is the "+\
                   "easiest, but usually has the least satisfaction for the "+\
                   "user."
FOUR_D_6_MESSAGE = "Keep best three, arrange to suit - 6 sets of 4d6 are "+\
                   "rolled, in each set, the top three dice are kept and "+\
                   "added together. Then these scores are assigned by the "+\
                   "user. This method usually has the highest satisfaction "+\
                   "for the player, but is also the most complicated, due "+\
                   "to the many choices required."

class RootApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        '''Custom Window class for Game

        Data Model - Character object
        referenced in frames by using:
            self.controller.player'''

        self.player = ch.Character()

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others

        container = tk.Frame(self)
        container.columnconfigure(0, weight = 1)
        container.grid(sticky = (tk.N+tk.S+tk.E+tk.W))

        self.frames = {}
        for F in (Menu, Hardcore, Simple, FourD6, Help):
            page_name = F.__name__
            frame = F(parent=container, controller=self) 
            self.frames[page_name] = frame  

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.columnconfigure(0, weight = 1)
            frame.grid(row = 0,column=0, sticky = (tk.N+tk.S+tk.E+tk.W))

        self.show_frame("Menu")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class Menu(tk.Frame):
    """ Opening Menu for Character Creator """ 
    def __init__(self, parent, controller):
        """ Initialize the frame. """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid(sticky = (tk.E+tk.W))
        self.create_widgets()

    def create_widgets(self):
        """ Create button, text, and entry widgets. """
        # create instruction label
        self.instLbl = tk.Label(self, text =
                              "Choose a Character Creation Method:")
        self.instLbl.grid(row = 0, column = 0, sticky = (tk.E+tk.W))

        # create whitespace
        self.blankLbl = tk.Label(self, text = '')
        self.blankLbl.grid(row = 1, column = 0, sticky = (tk.E+tk.W))
        
        # create hardcore button
        self.hcBttn = tk.Button(self, text = "Hardcore",
                                command = lambda: self.controller.show_frame("Hardcore"))
        self.hcBttn.grid(row = 2, column = 0, sticky = (tk.E+tk.W))

        # create simple button
        self.simpleBttn = tk.Button(self, text = "Simple",
                             command = lambda: self.controller.show_frame("Simple"))
        self.simpleBttn.grid(row = 3, column = 0, sticky = (tk.E+tk.W))

        # create 4d6 button
        self.fourD6Bttn = tk.Button(self, text = "4d6",
                             command = lambda: self.controller.show_frame("FourD6"))
        self.fourD6Bttn.grid(row = 4, column = 0, sticky = (tk.E+tk.W))

        # create Description button
        self.helpBttn = tk.Button(self, text = "Method Descriptions",
                             command = lambda: self.controller.show_frame("Help"))
        self.helpBttn.grid(row = 5, column = 0, sticky = (tk.E+tk.W))

class Hardcore(tk.Frame):

    def __init__(self, parent, controller):
        '''class constructor'''
        
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        '''method for widget placement'''
        
        label = tk.Label(self, text="Hardcore", font=TITLE_FONT)
        label.grid()
        button = tk.Button(self, text="Back to Menu",
                           command=lambda: self.controller.show_frame("Menu"))
        button.grid()


class Simple(tk.Frame):

    def __init__(self, parent, controller):
        '''class constructor'''
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        '''method for widget placement'''
        
        label = tk.Label(self, text="Simple", font=TITLE_FONT)
        label.grid(
            )
        button = tk.Button(self, text="Back to Menu",
                           command=lambda: self.controller.show_frame("Menu"))
        button.grid()

class FourD6(tk.Frame):

    def __init__(self, parent, controller):
        '''class constructor'''
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        '''method for widget placement'''
        
        label = tk.Label(self, text="4 d 6", font=TITLE_FONT)
        label.grid()
        button = tk.Button(self, text="Back to Menu",
                           command=lambda: self.controller.show_frame("Menu"))
        button.grid()

class Help(tk.Frame):
    '''Displays descriptions of the three character creation methods'''

    def __init__(self, parent, controller):
        '''class constructor'''
        
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        '''method for widget placement'''
        
        titleLbl = tk.Label(self, text="Method Descriptions", font=TITLE_FONT)
        titleLbl.grid()

        simpleLbl = tk.Label(self, text = "Simple", font=HEADING1_FONT)
        simpleLbl.grid()
        simpleTxt = tk.Text(self, height = 7, wrap = tk.WORD)
        simpleTxt.insert(0.0, SIMPLE_MESSAGE)
        simpleTxt.config(state= tk.DISABLED)
        simpleTxt.grid()
        
        hardLbl = tk.Label(self, text = "Hardcore", font=HEADING1_FONT)
        hardLbl.grid()
        hardTxt = tk.Text(self, height = 6, wrap = tk.WORD)
        hardTxt.insert(0.0, HARDCORE_MESSAGE)
        hardTxt.config(state= tk.DISABLED)
        hardTxt.grid()
        
        fourD6Lbl = tk.Label(self, text = "4d6", font=HEADING1_FONT)
        fourD6Lbl.grid()
        fourD6Txt = tk.Text(self, height = 6, wrap = tk.WORD)
        fourD6Txt.insert(0.0, FOUR_D_6_MESSAGE)
        fourD6Txt.config(state= tk.DISABLED)
        fourD6Txt.grid()

        backBttn = tk.Button(self, text="Back to Menu",
                           command=lambda: self.controller.show_frame("Menu"))
        backBttn.grid()


# main
root = RootApp()
root.title("Character Creator")
root.geometry("800x800+250+250")
root.columnconfigure(0, weight = 1)

root.mainloop()