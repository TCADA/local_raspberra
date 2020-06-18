#!/usr/bin/env python3
__author__ = "Copyright ⓒ Jun 2020 by www.chenxuanwei.com"
### 🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅 ###
### My Application:
### Version 2.0
### 20-06-2020
### 🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅 ###
import tkinter
import Socket

class Debug:
    @staticmethod
    def out(str):
        print("\n" + str + "\n")

class Application():

    Description = "This is the ....." 
    copyright = "Copyright ⓒ 2020 by www.chenxuanwei.com, All rights Reserved!"

    def __init__(self, title = "Welcome"):
        self.root = tkinter.Tk()
        self.root.title(title)
        self.root.configure(bg = "#004D40")
        self.root.maxsize(500, 400)
        self.root.minsize(500, 400)
        
        self.btnCommOn = False  ### communication status with RaspBerryPi, TRUE or FALSE
        self.btnGpioOn = True   ### SIGNAL LEVEL (On or Off) to GPIO

        self.sock = Socket.Socket(callback = self.getResult)

    def mainloop(self):
        self.output  = self.initLabel()    
        self.btnComm = self.initBtn(text = "connect", command = self.btnCommClicked)
        self.btnGpio = self.initBtn(text = "GPIO On", command = self.btnGpioClicked)      
        self.btnExit = self.initBtn(text = "Quit",    command = self.btnExitClicked)    
        self.output["text"] = "press <Connect> to init the socket with Raspberry Pi"
        self.refresh()
        self.root.mainloop()

    def initBtn(self, text, command):
        btn = tkinter.Button(self.root, text = text, font = ("ariel", 16), command = command, width = 14, height = 2,
            activebackground = "#01579B", activeforeground = "#01579B", relief = tkinter.RAISED,
            fg = "black")

        btn.pack( padx = 2, pady = 5, side = tkinter.LEFT)
        btn["background"] = "green"
        return btn
    
    def initLabel(self, text = "This is test."):
        label = tkinter.Label(self.root, text = text, font = ("ariel", 20),
            bg = "#004D40", fg = "black", width = 78, height = 2)

        label.pack(padx = 20, pady = 5, side = tkinter.BOTTOM)
        return label


    def refresh(self):
    
        self.btnComm["text"]  = "disconnect"     if self.btnCommOn else "connect"
        self.btnGpio["text"]  = "Switch On"      if self.btnGpioOn else "Switch Off"
        self.btnGpio["state"] = tkinter.NORMAL   if self.btnCommOn else tkinter.DISABLED
        self.btnExit["state"] = tkinter.DISABLED if self.btnCommOn else tkinter.NORMAL

    #### 🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅 ###
    #### btn Clicked process, 
    def btnCommClicked(self):
        Debug.out("communication Button is clicked!")

        if self.btnCommOn:  ### TRUE, disconnect the socket with RaspberryPi
            self.sock.closeClient()
            pass
        else:               ### FALSE, initial the socket with Raspberry Pi
            self.sock.initClient()


        #self.btnCommOn = not self.btnCommOn

        self.refresh() #### update the status of the Buttons


    def btnGpioClicked(self):
        Debug.out("GPIO Button is clicked!") 
        
        if self.btnGpioOn: ### send GPIO_ON to Raspberry Pi
            self.sock.send2Server(data = "GPIO_ON")
        else:
            self.sock.send2Server(data = "GPIO_OFF")

        self.refresh() #### update the status of the Buttons

    ### Quit the application
    def btnExitClicked(self):
        if self.btnCommOn:
            Debug.out("Please disconnect the socket before you quit!") 
            self.output["text"] = "Please <disconnect> the socket ...!"
        else:
            self.root.quit()
    
    #### 🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅 ###
    #### get Feedback from RaspberryPi,
    def getResult(self, cmd):
        Debug.out("🔴🔴🔴🔴: " + cmd)
        if cmd == self.sock.msgHandshake:  #### the socket with RaspberryPi is hand shaken. 
            self.btnCommOn = True
            self.output["text"] = "the socket with raspberryPi is Connected ..."
        elif cmd == "exit":
            self.btnCommOn = False 
            self.output["text"] = " the socket with raspberryPi is disConnected ..."
        elif cmd == self.sock.msgGPIO_ON:
            self.btnGpioOn = False
            self.output["text"] = "signal GPIO ON is sent to raspberryPi ..."
        elif cmd == self.sock.msgGPIO_OFF:
            self.btnGpioOn = True
            self.output["text"] = "signal GPIO OFF is sent to raspberryPi ..."




#### 🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅 ###
#### main process, the entrance of the application
if __name__ == "__main__":  
    Application().mainloop()
#### 🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅 ###
