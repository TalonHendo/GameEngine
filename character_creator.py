# character_creator.py
# Thorin Schmidt
# 11/29/2016

''' GUI-based character generator'''

import tkinter as tk
import character as ch
import monster as mon
import random as rd

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
        button.grid(sticky = tk.S, column = 1, row = 7)
        
        reRollButton = tk.Button(self, text = "ReRoll")
        reRollButton.grid(sticky = tk.S, column = 0, row = 7)
        saveAndContinueButton = tk.Button(self, text = "Save/Continue")
        saveAndContinueButton.grid(sticky = tk.S, column = 3, row = 7)
        strengthLabel = tk.Label(self, text = "Strength", foreground = "red")
        strengthLabel.grid(sticky = tk.N + tk.S + tk.E + tk.W, column = 0, row = 1)
        dexterityLabel = tk.Label(self, text = "Dexterity", foreground = "orange")
        dexterityLabel.grid(sticky = tk.N + tk.S + tk.E + tk.W, column = 0, row = 2)
        constitutionLabel = tk.Label(self, text = "Constitution", foreground = "yellow")
        constitutionLabel.grid(sticky = tk.N + tk.S + tk.E + tk.W, column = 0, row = 3)
        intelligenceLabel = tk.Label(self, text = "Intelligence", foreground = "green")
        intelligenceLabel.grid(sticky = tk.N + tk.S + tk.E + tk.W, column = 0, row = 4)
        wisdomLabel = tk.Label(self, text = "Wisdom", foreground = "blue")
        wisdomLabel.grid(sticky = tk.N + tk.S + tk.E + tk.W, column = 0, row = 5)
        charismaLabel = tk.Label(self, text = "Charisma", foreground = "indigo")
        charismaLabel.grid(sticky = tk.N + tk.S + tk.E + tk.W, column = 0, row = 6)
        strLabel = tk.Label(self, text = "(STR)", foreground = "red")
        strLabel.grid(sticky = tk.N + tk.S + tk.E + tk.W, column = 1, row = 1)
        dexLabel = tk.Label(self, text = "(DEX)", foreground = "orange")
        dexLabel.grid(sticky = tk.N + tk.S + tk.E + tk.W, column = 1, row = 2)
        conLabel = tk.Label(self, text = "(CON)", foreground = "yellow")
        conLabel.grid(sticky = tk.N + tk.S + tk.E + tk.W, column = 1, row = 3)
        intLabel = tk.Label(self, text = "(INT)", foreground = "green")
        intLabel.grid(sticky = tk.N + tk.S + tk.E + tk.W, column = 1, row = 4)
        wisLabel = tk.Label(self, text = "(WIS)", foreground = "blue")
        wisLabel.grid(sticky = tk.N + tk.S + tk.E + tk.W, column = 1, row = 5)
        chaLabel = tk.Label(self, text = "(CHA)", foreground = "indigo")
        chaLabel.grid(sticky = tk.N + tk.S + tk.E + tk.W, column = 1, row = 6)
        strPointsLabel = tk.Label(self, text = "#", foreground = "red")
        strPointsLabel.grid(sticky = tk.N + tk.S + tk.E + tk.W, column = 3, row = 1)
        dexPointsLabel = tk.Label(self, text = "#", foreground = "orange")
        dexPointsLabel.grid(sticky = tk.N + tk.S + tk.E + tk.W, column = 3, row = 2)
        conPointsLabel = tk.Label(self, text = "#", foreground = "yellow")
        conPointsLabel.grid(sticky = tk.N + tk.S + tk.E + tk.W, column = 3, row = 3)
        intPointsLabel = tk.Label(self, text = "#", foreground = "green")
        intPointsLabel.grid(sticky = tk.N + tk.S + tk.E + tk.W, column = 3, row = 4)
        wisPointsLabel = tk.Label(self, text = "#", foreground = "blue")
        wisPointsLabel.grid(sticky = tk.N + tk.S + tk.E + tk.W, column = 3, row = 5)
        chaPointsLabel = tk.Label(self, text = "#", foreground = "indigo")
        chaPointsLabel.grid(sticky = tk.N + tk.S + tk.E + tk.W, column = 3, row = 6)


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
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.parent = parent
        
        self.statBlock = [rd.randint(3,18),
                          rd.randint(3,18),
                          rd.randint(3,18),
                          rd.randint(3,18),
                          rd.randint(3,18),
                          rd.randint(3,18)]
        self.statIndex = 0
        
        self.create_widgets()

    def create_widgets(self):
        '''method for widget placement'''
        
        label = tk.Label(self, text="4 d 6", font=TITLE_FONT)
        label.grid(column = 1, row = 0)
        menuButton = tk.Button(self, text="Back to Menu",
                           command=lambda: self.controller.show_frame("Menu"))
        menuButton.grid(column = 1, row = 13)
        strengthLabel = tk.Label(self, text = "Strength", foreground = "red")
        strengthLabel.grid(column = 0, row = 2)
        dexterityLabel = tk.Label(self, text = "Dexterity", foreground = "orange")
        dexterityLabel.grid(column = 0, row = 3)
        constitutionLabel = tk.Label(self, text = "Constitution", foreground = "yellow")
        constitutionLabel.grid(column = 0, row = 4)
        intelligenceLabel = tk.Label(self, text = "Intelligence", foreground = "green")
        intelligenceLabel.grid(column = 0, row = 5)
        wisdomLabel = tk.Label(self, text = "Wisdom", foreground = "blue")
        wisdomLabel.grid(column = 0, row = 6)
        charismaLabel = tk.Label(self, text = "Charisma", foreground = "indigo")
        charismaLabel.grid(column = 0, row = 7)
        chaLabel = tk.Label(self, text = "CHA", foreground = "indigo")
        chaLabel.grid(column = 1, row = 7)
        wisLabel = tk.Label(self, text = "WIS", foreground = "blue")
        wisLabel.grid(column = 1, row = 6)
        intLabel = tk.Label(self, text = "INT", foreground = "green")
        intLabel.grid(row = 5, column = 1)
        conLabel = tk.Label(self, text = "CON", foreground = "yellow")
        conLabel.grid(row = 4, column = 1)
        dexLabel = tk.Label(self, text = "DEX", foreground = "orange")
        dexLabel.grid(row = 3, column = 1)
        strLabel = tk.Label(self, text = "STR", foreground = "red")
        strLabel.grid(row = 2, column = 1)
        yourScoresLabel = tk.Label(self, text = "Available Scores")
        yourScoresLabel.grid(column = 1, row = 8)
        instructionLabel = tk.Label(self, text = "Click a button to pick strength.")
        instructionLabel.grid(column = 1, row = 9)
        self.firstScoreButton = tk.Button(self, text = str(self.statBlock[0]),
                                          command = lambda: self.bttnClick(1, str(self.statBlock[0])))
        self.firstScoreButton.grid(column = 0, row = 10)
        self.secondScoreButton = tk.Button(self, text = str(self.statBlock[1]),
                                           command = lambda: self.bttnClick(2, str(self.statBlock[1])))
        self.secondScoreButton.grid(column = 1, row = 10)
        self.thirdScoreButton = tk.Button(self, text = str(self.statBlock[2]),
                                          command = lambda: self.bttnClick(3, str(self.statBlock[2])))
        self.thirdScoreButton.grid(column = 2, row = 10)
        self.fourthScoreButton = tk.Button(self, text = str(self.statBlock[3]),
                                           command = lambda: self.bttnClick(4, str(self.statBlock[3])))
        self.fourthScoreButton.grid(column = 0, row = 11)
        self.fifthScoreButton = tk.Button(self, text = str(self.statBlock[4]),
                                          command = lambda: self.bttnClick(5, str(self.statBlock[4])))
        self.fifthScoreButton.grid(column = 1, row = 11)
        self.sixthScoreButton = tk.Button(self, text = str(self.statBlock[5]),
                                          command = lambda: self.bttnClick(6, str(self.statBlock[5])))
        self.sixthScoreButton.grid(column = 2, row = 11)
        resetButton = tk.Button(self, text = "Reset", command = self.reset)
        resetButton.grid(column = 1, row = 12)
        reRollButton = tk.Button(self, text = "Re-Roll", command = self.re_roll)
        reRollButton.grid(column = 0, row = 13)
        saveButton = tk.Button(self, text = "Save", command = self.save)
        saveButton.grid(column = 2, row = 13)
        self.strValueLabel = tk.Label(self, text = "#", foreground = "red")
        self.strValueLabel.grid(column = 2, row = 2)
        self.dexValueLabel = tk.Label(self, text = "#", foreground = "orange")
        self.dexValueLabel.grid(column = 2, row = 3)
        self.conValueLabel = tk.Label(self, text = "#", foreground = "yellow")
        self.conValueLabel.grid(column = 2, row = 4)
        self.intValueLabel = tk.Label(self, text = "#", foreground = "green")
        self.intValueLabel.grid(column = 2, row = 5)
        self.wisValueLabel = tk.Label(self, text = "#", foreground = "blue")
        self.wisValueLabel.grid(column = 2, row = 6)
        self.chaValueLabel = tk.Label(self, text = "#", foreground = "indigo")
        self.chaValueLabel.grid(column = 2, row = 7)

    def re_roll(self):
        """Re-roll the stat block"""
        print("rerolling!")
        self.reset()
        buttonList= (self.firstScoreButton, self.secondScoreButton, self.thirdScoreButton,
                     self.fourthScoreButton, self.fifthScoreButton, self.sixthScoreButton)
        for i in range(len(self.statBlock)):
            self.statBlock[i] = rd.randint(3,18)
            buttonList[i].configure(text = str(self.statBlock[i]))
    def bttnClick(self, value, newText):
        if self.statIndex == 0:
            self.strValueLabel.configure(text = newText)
        elif self.statIndex == 1:
            self.dexValueLabel.configure(text = newText)
        elif self.statIndex == 2:
            self.conValueLabel.configure(text = newText)
        elif self.statIndex == 3:
            self.intValueLabel.configure(text = newText)
        elif self.statIndex == 4:
            self.wisValueLabel.configure(text = newText)
        else:
            self.chaValueLabel.configure(text = newText)
            
        if value == 1:
            self.firstScoreButton["state"] = tk.DISABLED
        elif value == 2:
            self.secondScoreButton["state"] = tk.DISABLED
        elif value == 3:
            self.thirdScoreButton["state"] = tk.DISABLED
        elif value == 4:
            self.fourthScoreButton["state"] = tk.DISABLED
        elif value == 5:
            self.fifthScoreButton["state"] = tk.DISABLED
        elif value == 6:
            self.sixthScoreButton["state"] = tk.DISABLED
        self.statIndex += 1

    def reset(self):
        self.firstScoreButton["state"] = tk.NORMAL
        self.secondScoreButton["state"] = tk.NORMAL
        self.thirdScoreButton["state"] = tk.NORMAL
        self.fourthScoreButton["state"] = tk.NORMAL
        self.fifthScoreButton["state"] = tk.NORMAL
        self.sixthScoreButton["state"] = tk.NORMAL
        self.strValueLabel.configure(text = "#")
        self.dexValueLabel.configure(text = "#")
        self.conValueLabel.configure(text = "#")
        self.intValueLabel.configure(text = "#")
        self.wisValueLabel.configure(text = "#")
        self.chaValueLabel.configure(text = "#")
        self.statIndex = 0

    def save(self):
        if self.statIndex >= 6:
            self.controller.player.strength = int(self.strValueLabel.cget("text"))
            self.controller.player.dexteriy = int(self.dexValueLabel.cget("text"))
            self.controller.player.constitution = int(self.conValueLabel.cget("text"))
            self.controller.player.intelligence = int(self.intValueLabel.cget("text"))
            self.controller.player.wisdom = int(self.wisValueLabel.cget("text"))
            self.controller.player.charisma = int(self.chaValueLabel.cget("text"))
            print(self.controller.player)
        else:
            print("NOPE!")
        

        

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
