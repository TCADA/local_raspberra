#!/usr/bin/env python3
__author__ = "Copyright ⓒ Jun 2020 by www.chenxuanwei.com"
### 🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅 ###
### My Application:
### Version 2.0
### 20-06-2020
### 🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅 ###
from tkinter import Tk

from Socket import Socket
from canvas import Debug, XCanvas, XButton
from db     import Database

class Application(Tk):

    DESCRIPTION = "This is the ....." 
    COPYRIGHT = "Copyright ⓒ 2020 by www.chenxuanwei.com, All rights Reserved!"
    WIDTH, HEIGHT = 600, 400
    BACKGROUND = "#004D40"
    TITLE = "Welcome"
    FENS = {
        "head":         [  7,   7, 590,  40],
        "body":         [  7,  47, 590, 270],
        "comment":      [  7, 317, 590,  40],
        "copyright":    [  7, 357, 590,  40]}
    TAGLINE = "tag_line"
    TAGSWITCH = "tag_switch"


    def __init__(self):

        self.mouse = []
        super().__init__()
        self.title()
        super().geometry("%dx%d+105+105" %(self.WIDTH, self.HEIGHT))
        super().configure(bg = self.BACKGROUND)
        super().title(self.TITLE)
        super().maxsize(self.WIDTH, self.HEIGHT)
        super().minsize(self.WIDTH, self.HEIGHT)

        super().bind("<Button-1>", self.click)  ### catchup the event of mouse clicked

        self.cv    = XCanvas(root  = self) #### initital Canvas
        self.debug = Debug(root = self, cord = self.FENS["comment"]) 
        self.db    = Database()
        
        self.btnCommOn = False  ### communication status with RaspBerryPi, TRUE or FALSE
        self.btnGpioOn = True   ### SIGNAL LEVEL (On or Off) to GPIO

        self.sock = Socket(callback = self.getResult)
        self.network = self.db.loadImage(file = "network")
        self.switch  = self.db.loadImages(files = ["swOff", "swOn"])

    ### 🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢 ###
    ### Mouse Control, register and unregister
    def register(self, cord, command, tag): 
        self.mouse.append([cord, command, tag])

    def unregister(self, tag):
        for index, tuple in enumerate(self.mouse):
            if tuple[2] == tag:
                self.mouse.pop(index)
                return
        return

    def click(self, event):

        ### Debug.out("x = {}, y= {}".format(event.x, event.y))
        for (cord, command, tag) in self.mouse:
            x, y = event.x - cord[0], event.y - cord[1]
            if self.domain(x, y, cord): command(x = x, y = y, tag = tag)

    ### check if the mouse clicked in the domain.
    def domain(self, x, y, cord): return 0 <= y and y <= cord[3] and 0 <= x and x <= cord[2]

    ### 🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢 ###
    ### rewrite the mainloop()
    def mainloop(self):
        
        #### initial the Layout of Canvas
        for _, cord in self.FENS.items(): 
            self.cv.bolder(cord, fill = self.BACKGROUND, tag = "fens")

        #### initial the menu
        MENU = {
            "connect":      self.btnCommClicked,
            "GPIO On":      self.btnGpioClicked,
            "Quit":         self.btnExitClicked}

        self.menu = self.initMenu(cord = self.FENS["head"], ctrl = MENU, tag = "menu")
        self.cv.text(cord = self.FENS["copyright"], text = self.COPYRIGHT, fill = "#263238")
        self.refresh()
        self.cv.image(cord = self.FENS["body"], img = self.network, tag = "network")
        self.debug.comment(text = "press <Connect> to init the socket with Raspberry Pi")

        super().mainloop()

    #### refresh the status of menus, self.menu.
    def refresh(self):      
        self.menu[0].showText(text = "disconnect"   if self.btnCommOn else "connect")
        self.menu[1].showText(text = "Switch On"    if self.btnGpioOn else "Switch Off")
        self.menu[1].state(status = "normal"   if self.btnCommOn else "disabled")
        self.menu[2].state(status = "disabled" if self.btnCommOn else "normal")
        self.connected()
        self.switchOn()
        
    def initMenu(self, cord, ctrl, tag):

        number = len(ctrl.keys())

        width  = cord[2]  / number ### width for each button
        btn    = []

        for index, (text, command) in enumerate(ctrl.items()):
            btn.append(XButton(root = self, command = command, text = text, round = True,
                                          tag = "%s_%d" %(tag, index), font = ("Times", 12), adjust = True))
            btn[-1].initial(cord = [cord[0] + width * index, cord[1], width, cord[3] * 0.9 ])

        return btn

    def initBtn(self, text, command):
        btn = XButton(self.root, text = text, font = ("ariel", 16), command = command, width = 14, height = 2,
            activebackground = "#01579B", activeforeground = "#01579B", relief = tkinter.RAISED,
            fg = "black")

        btn.pack( padx = 2, pady = 5, side = tkinter.LEFT)
        btn["background"] = "green"
        return btn
    
    def initLabel(self, text = "This is test."):
        label = XLabel(self.root, text = text, font = ("ariel", 20),
            bg = "#004D40", fg = "black", width = 78, height = 2)

        label.pack(padx = 20, pady = 5, side = tkinter.BOTTOM)
        return label

    #### 🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅 ###
    #### btn Clicked process, 
    def btnCommClicked(self, tag):
        Debug.out("communication Button is clicked!")

        if self.btnCommOn:  ### TRUE, disconnect the socket with RaspberryPi
            self.btnCommOn = False
            self.sock.closeClient()
        else:               ### FALSE, initial the socket with Raspberry Pi
            self.sock.initClient()

        self.refresh() #### update the status of the Buttons


    def btnGpioClicked(self, tag):
        Debug.out("GPIO Button is clicked!") 
        
        if self.btnGpioOn: ### send GPIO_ON to Raspberry Pi
            self.sock.send2Server(data = "GPIO_ON")
        else:
            self.sock.send2Server(data = "GPIO_OFF")

        self.refresh() #### update the status of the Buttons

    ### Quit the application
    def btnExitClicked(self, tag):
        if self.btnCommOn:
            Debug.out("Please disconnect the socket before you quit!") 
        else:
            super().quit()
    
    #### 🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅 ###
    #### get Feedback from RaspberryPi,
    def getResult(self, cmd):
        Debug.out("🔴🔴🔴🔴: " + cmd)
        if cmd == self.sock.msgHandshake:  #### the socket with RaspberryPi is hand shaken. 
            self.btnCommOn = True
            self.debug.comment(text = "the socket with raspberryPi is Connected ...")
        elif cmd == "exit":
            self.btnCommOn = False 
            self.debug.comment(text = " the socket with raspberryPi is disConnected ...")
        elif cmd == self.sock.msgGPIO_ON:
            self.btnGpioOn = False
            self.debug.comment(text = "signal GPIO ON is sent to raspberryPi ...")
        elif cmd == self.sock.msgGPIO_OFF:
            self.btnGpioOn = True
            self.debug.comment(text = "signal GPIO OFF is sent to raspberryPi ...")

    def connected(self):
        if self.btnCommOn:
            self.cv.line(x0 = 100, y0 = 210, x1 = 250, y1 = 210, fill = "#64DD17", width = 10, tag = self.TAGLINE)
        else:
            self.cv.delete(self.TAGLINE)
    
    def switchOn(self):
        if self.btnGpioOn:
            self.cv.delete(self.TAGSWITCH)
        else:
            self.cv.image(cord = [330, 190, 0, 0], img = self.switch["swOn"], tag = self.TAGSWITCH)
            self.cv.line(x0 = 250, y0 = 210, x1 = 330, y1 = 210, fill = "#64DD17", width = 10, tag = self.TAGSWITCH)
            self.cv.line(x0 = 370, y0 = 210, x1 = 520, y1 = 210, fill = "#64DD17", width = 10, tag = self.TAGSWITCH)

#### 🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅 ###
#### main process, the entrance of the application
if __name__ == "__main__":  
    Application().mainloop()
#### 🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅 ###
