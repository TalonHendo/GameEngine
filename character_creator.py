# character_creator.py
# Thorin Schmidt
# Additions by: Talon H.
# 11/29/2016

''' GUI-based character generator'''

import tkinter as tk
import character as ch
import monster as mon
import random as rd

TITLE_FONT = ("Helvetica", 20, "bold")
HEADING1_FONT = ("Helvetica", 16, "bold")
TABLE_FONT = ("Arial", 14, "bold")
INSTRUCTION_FONT = ("Helvetica", 14, "bold")
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
        self.columnconfigure(0, weight=1)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others

        container = tk.Frame(self)
        container.columnconfigure(0, weight=1)
        container.grid(sticky = (tk.N+tk.S+tk.E+tk.W))
        self.frames = {}
        for F in (Menu, Hardcore, Simple, FourD6, Help):
            page_name = F.__name__
            frame = F(parent=container, controller=self) 
            self.frames[page_name] = frame  

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row = 0,column=0, sticky = (tk.N+tk.S+tk.E+tk.W))

        self.show_frame("Menu")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class Display(tk.Frame):

    def __init__(self, parent, controller):
        '''class constructor'''
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.create_widgets()
        self.columnconfigure(0, weight=1)

    def create_widgets(self):
        '''method for widget placement'''
        
        self.nameLbl = tk.Label(self, text = self.controller.player.name)
        self.nameLbl.grid(row = 0, column = 0)

        #Show the image
        self.photo = tk.PhotoImage(file=self.controller.player.imageFileName)
        self.photoLbl = tk.Label(self, image = self.photo)
        self.photoLbl.grid(row=0, column=1, sticky = tk.N)


        
        self.button = tk.Button(self, text="Back to Menu",
                           command=lambda: self.controller.show_frame("Menu"))
        self.button.grid()

class Menu(tk.Frame):
    """ Opening Menu for Character Creator """ 
    def __init__(self, parent, controller):
        """ Initialize the frame. """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.columnconfigure(0, weight = 1)
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
                                command = lambda:
                                self.controller.show_frame("Hardcore"))
        self.hcBttn.grid(row = 2, column = 0, sticky = (tk.E+tk.W))

        # create simple button
        self.simpleBttn = tk.Button(self, text = "Simple",
                                    command = lambda:
                                    self.controller.show_frame("Simple"))
        self.simpleBttn.grid(row = 3, column = 0, sticky = (tk.E+tk.W))

        # create 4d6 button
        self.fourD6Bttn = tk.Button(self, text = "4d6",
                                    command = lambda:
                                    self.controller.show_frame("FourD6"))
        self.fourD6Bttn.grid(row = 4, column = 0, sticky = (tk.E+tk.W))

        # create Description button
        self.helpBttn = tk.Button(self, text = "Method Descriptions",
                                  command = lambda:
                                  self.controller.show_frame("Help"))
        self.helpBttn.grid(row = 5, column = 0, sticky = (tk.E+tk.W))

        #create Display button
        #self.displayBttn = tk.Button(self, text = "Display Character",
        #                             command = lambda:
        #                             self.controller.show_frame("Display"))
        #
        #self.displayBttn.grid(row = 6, column = 0, sticky = (tk.E+tk.W))


class Hardcore(tk.Frame):

    def __init__(self, parent, controller):
        '''class constructor'''
        
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        
        self.statBlock = [rd.randint(3,18),
                          rd.randint(3,18),
                          rd.randint(3,18),
                          rd.randint(3,18),
                          rd.randint(3,18),
                          rd.randint(3,18)]

        self.create_widgets()

    def create_widgets(self):
        '''method for widget placement'''
        
        self.label = tk.Label(self, text="Hardcore", font=TITLE_FONT)
        self.label.grid(row=0, column=0, columnspan=3)


        self.label2 = tk.Label(self, text = "none")
        self.label2.grid()
     
        self.button = tk.Button(self, text="Back to Menu",
                           command=lambda: self.controller.show_frame("Menu"))
        self.button.grid()



        
class Simple(tk.Frame):

    def __init__(self, parent, controller):
        '''class constructor'''
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.create_widgets()

    def create_widgets(self):
        '''method for widget placement'''
        
        self.label = tk.Label(self, text="Simple", font=TITLE_FONT)
        self.label.grid()
        self.button = tk.Button(self, text="Back to Menu",
                           command=lambda: self.controller.show_frame("Menu"))
        self.button.grid()

class FourD6(tk.Frame):

    def __init__(self, parent, controller):
        '''class constructor'''
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.buttonClicks = 0
        self.statBlock = []
        for i in range(6):
            self.statBlock.append(self.roll_dice())

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.create_widgets()

    def roll_dice(self):
        '''roll 4d6, keep the highest'''

        rolls = []
        for i in range(4):
            rolls.append(rd.randint(1,6))
        rolls.remove(min(rolls))
        return sum(rolls)

    def create_widgets(self):
        '''method for widget placement'''
        #row 0 - Heading
        self.label = tk.Label(self, text="4 d 6", font=TITLE_FONT)
        self.label.grid(row=0, column=0, columnspan=3)

        #row 1 - table headings
        self.attLbl = tk.Label(self, text="Attribute")
        self.abrLbl = tk.Label(self, text="Abbreviation")
        self.scoreLbl = tk.Label(self, text="Score")
        self.attLbl.grid(row=1, column=0)
        self.abrLbl.grid(row=1, column=1)
        self.scoreLbl.grid(row=1, column=2)

        #row 2 - Strength
        self.strengthLbl = tk.Label(self, text="Strength", background="red",
                                    font=TABLE_FONT, width=20)
        self.strLbl = tk.Label(self, text="(STR)", background="red",
                               font=TABLE_FONT, width=20)
        self.strStatLbl = tk.Label(self, text="", background="red",
                                   font=TABLE_FONT, width=20)
        self.strengthLbl.grid(row = 2, column=0)
        self.strLbl.grid(row = 2, column=1)
        self.strStatLbl.grid(row = 2, column=2)

        #row 3 - Dexterity
        self.dexterityLbl = tk.Label(self, text="Dexterity", background="orange",
                                    font=TABLE_FONT, width=20)
        self.dexLbl = tk.Label(self, text="(DEX)", background="orange",
                               font=TABLE_FONT, width=20)
        self.dexStatLbl = tk.Label(self, text="", background="orange",
                                   font=TABLE_FONT, width=20)
        self.dexterityLbl.grid(row = 3, column=0)
        self.dexLbl.grid(row = 3, column=1)
        self.dexStatLbl.grid(row = 3, column=2)

        #row 4 - Constitution
        self.constitutionLbl = tk.Label(self, text="Constitution",
                                        background="yellow", font=TABLE_FONT,
                                        width=20)
        self.conLbl = tk.Label(self, text="(CON)", background="yellow",
                               font=TABLE_FONT, width=20)
        self.conStatLbl = tk.Label(self, text="", background="yellow",
                                   font=TABLE_FONT, width=20)
        self.constitutionLbl.grid(row = 4, column=0)
        self.conLbl.grid(row = 4, column=1)
        self.conStatLbl.grid(row = 4, column=2)

        #row 5 - Intelligence
        self.intelligenceLbl = tk.Label(self, text="Intelligence",
                                        background="green", font=TABLE_FONT,
                                        width=20)
        self.intLbl = tk.Label(self, text="(INT)", background="green",
                               font=TABLE_FONT, width=20)
        self.intStatLbl = tk.Label(self, text="", background="green",
                                   font=TABLE_FONT, width=20)
        self.intelligenceLbl.grid(row = 5, column=0)
        self.intLbl.grid(row = 5, column=1)
        self.intStatLbl.grid(row = 5, column=2)

        #row 6 - Wisdom
        self.wisdomLbl = tk.Label(self, text="Wisdom", background="cyan",
                                    font=TABLE_FONT, width=20)
        self.wisLbl = tk.Label(self, text="(WIS)", background="cyan",
                               font=TABLE_FONT, width=20)
        self.wisStatLbl = tk.Label(self, text="", background="cyan",
                                   font=TABLE_FONT, width=20)
        self.wisdomLbl.grid(row = 6, column=0)
        self.wisLbl.grid(row = 6, column=1)
        self.wisStatLbl.grid(row = 6, column=2)

        #row 7 - Charisma
        self.charismaLbl = tk.Label(self, text="Charisma", background="magenta3",
                                    font=TABLE_FONT, width=20)
        self.chaLbl = tk.Label(self, text="(CHA)", background="magenta3",
                               font=TABLE_FONT, width=20)
        self.chaStatLbl = tk.Label(self, text="", background="magenta3",
                                   font=TABLE_FONT, width=20)
        self.charismaLbl.grid(row = 7, column=0)
        self.chaLbl.grid(row = 7, column=1)
        self.chaStatLbl.grid(row = 7, column=2)

        #row 8 - subheading "Available scores"
        self.subHeadLbl = tk.Label(self, text="Available Scores",
                                   font = HEADING1_FONT)
        self.subHeadLbl.grid(row=8, column=0, columnspan=3)

        #row 9 - Instructions
        self.instructionLbl = tk.Label(self, text="Click a button to choose "+\
                                       "your Strength score",
                                       font = INSTRUCTION_FONT)
        self.instructionLbl.grid(row=9, column=0, columnspan=3)

        #row 10 - first row of score buttons
        self.bttn1 = tk.Button(self, text = str(self.statBlock[0]),
                               font=TABLE_FONT, width=20,
                               command=lambda:
                               self.bttnClick(1, str(self.statBlock[0])))
        self.bttn1.grid(row=10, column=0)

        self.bttn2 = tk.Button(self, text = str(self.statBlock[1]),
                               font=TABLE_FONT, width=20,
                               command=lambda:
                               self.bttnClick(2, str(self.statBlock[1])))
        self.bttn2.grid(row=10, column=1)

        self.bttn3 = tk.Button(self, text = str(self.statBlock[2]),
                               font=TABLE_FONT, width=20,
                               command=lambda:
                               self.bttnClick(3, str(self.statBlock[2])))
        self.bttn3.grid(row=10, column=2)

        #row 11 - second row of score buttons
        self.bttn4 = tk.Button(self, text = str(self.statBlock[3]),
                               font=TABLE_FONT, width=20,
                               command=lambda:
                               self.bttnClick(4, str(self.statBlock[3])))
        self.bttn4.grid(row=11, column=0)

        self.bttn5 = tk.Button(self, text = str(self.statBlock[4]),
                               font=TABLE_FONT, width=20,
                               command=lambda:
                               self.bttnClick(5, str(self.statBlock[4])))
        self.bttn5.grid(row=11, column=1)
                               
        self.bttn6 = tk.Button(self, text = str(self.statBlock[5]),
                               font=TABLE_FONT, width=20,
                               command=lambda:
                               self.bttnClick(6, str(self.statBlock[5])))
        self.bttn6.grid(row=11, column=2)

        #row 12 - reset button
        self.resetBttn = tk.Button(self, text = "Reset", width=20,
                               command = self.reset)
        self.resetBttn.grid(row=12, column=1)
        
        #row 13 - Navigation Buttons
        self.rrBttn = tk.Button(self, text = "Reroll", width=20,
                               command = self.re_roll)
        self.rrBttn.grid()

        self.backbutton = tk.Button(self, text="Back to Menu", width=20,
                           command=lambda: self.controller.show_frame("Menu"))
        self.backbutton.grid(row=13, column=1)

        self.saveBttn = tk.Button(self, text="Save and\nContinue", width=20,
                                  command=self.save_character, state=tk.DISABLED)
        self.saveBttn.grid(row=13, column=2)
        
    def save_character(self):
        self.controller.player.strength = int(self.strStatLbl["text"])
        self.controller.player.dexterity = int(self. dexStatLbl["text"])
        self.controller.player.constitution = int(self.conStatLbl["text"])
        self.controller.player.intelligence = int(self.intStatLbl["text"])
        self.controller.player.wisdom = int(self.wisStatLbl["text"])
        self.controller.player.charisma = int(self.chaStatLbl["text"])
        print(self.controller.player)
        self.controller.show_frame("Menu")

    def re_roll(self):
        ''' re-roll the stat block '''
        buttonList = (self.bttn1, self.bttn2, self.bttn3,
                      self.bttn4, self.bttn5, self.bttn6)
        for i in range(len(self.statBlock)):
            self.statBlock[i] = rd.randint(3,18)
            buttonList[i].configure(text = str(self.statBlock[i]))
        self.reset()

    def reset(self):
        '''enable all buttons, set labels back to blank'''
        self.buttonClicks = 0
        self.update_instructions()
        buttonList = (self.bttn1, self.bttn2, self.bttn3,
                      self.bttn4, self.bttn5, self.bttn6)
        for i in range(len(buttonList)):
            buttonList[i].configure(state = tk.NORMAL)

        self.strStatLbl["text"] = ""
        self.dexStatLbl["text"] = ""
        self.conStatLbl["text"] = ""
        self.intStatLbl["text"] = ""
        self.wisStatLbl["text"] = ""
        self.chaStatLbl["text"] = ""
            
    def bttnClick(self, value, newText):

        self.labelList = (self.strStatLbl, self.dexStatLbl, self.conStatLbl,
                          self.intStatLbl, self.wisStatLbl, self.chaStatLbl)
        buttonList = (self.bttn1, self.bttn2, self.bttn3,
                      self.bttn4, self.bttn5, self.bttn6)

        self.labelList[self.buttonClicks].configure(text = newText)
        buttonList[value-1].configure(state = tk.DISABLED)
        self.buttonClicks += 1
        self.update_instructions()
        if self.buttonClicks > 5:
            self.saveBttn["state"] = tk.NORMAL

    def update_instructions(self):
        '''change instructions as user picks stats'''
        wordList = ("Strength", "Dexterity", "Constitution",
                    "Intelligence", "Wisdom", "Charisma")
        if self.buttonClicks < 6:
            word = wordList[self.buttonClicks]

            message = "Click a button to choose your " + word + " score."
            self.instructionLbl["text"] = message

class Help(tk.Frame):
    '''Displays descriptions of the three character creation methods'''

    def __init__(self, parent, controller):
        '''class constructor'''
        
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.columnconfigure(0, weight=1)
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
        hardTxt = tk.Text(self, height = 7, wrap = tk.WORD)
        hardTxt.insert(0.0, HARDCORE_MESSAGE)
        hardTxt.config(state= tk.DISABLED)
        hardTxt.grid()
        
        fourD6Lbl = tk.Label(self, text = "4d6", font=HEADING1_FONT)
        fourD6Lbl.grid()
        fourD6Txt = tk.Text(self, height = 7, wrap = tk.WORD)
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

root.mainloop()
