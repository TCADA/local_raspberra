#!/usr/bin/env python3
__author__ = "Copyright ⓒ Jun 2020 by www.chenxuanwei.com"
### 🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅 ###
### Canvas re-defination:
### Version 2.0
### 20-06-2020
### 🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅 ###
import tkinter, threading, time

#### 🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅 ###
#### Re-Definate features of Debug
class Debug:
    def __init__(self, root, cord):
        self.root = root
        self.cord = cord

    @staticmethod
    def out(str):   print("\n" + str + "\n")
    def comment(self, text):
        self.root.cv.text(cord = self.cord, text = text)

#### 🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅 ###
#### Re-Definate tkinter.Canvas
class XCanvas(tkinter.Canvas):
    def __init__(self, root):
        self.root = root
        super().__init__(self.root, width = self.root.WIDTH, height = self.root.HEIGHT, bg = self.root.BACKGROUND)
        super().pack(padx = 0, pady = 0)

    def text(self, cord, text, fill = "black", font = ("Times", 14), tag = "text", anchor = "center"): ### 放置文本
        self.delete(tag)

        x = cord[0] + cord[2] / 2 if anchor == "center" else cord[0] + 12
        y = cord[1] + cord[3] / 2 if anchor == "center" else cord[1] + 2
        return super().create_text(x, y, text = text, fill = fill, font = font, tag = tag, anchor = anchor)

    def rectangle(self, cord, outline = "darkgrey", fill = "blue", width = 2, tag = "rectangle"): ### 画长方形,起点坐标和长度,宽度
        return super().create_rectangle(cord[0], cord[1], cord[0] + cord[2] - width * 2, cord[1] + cord[3] - width * 2,
                outline = outline, fill = fill, width = width, tag = tag)

    def bolder(self, cord, outline = "darkgrey", inline = "grey", fill = "darkblue", width = 2, tag = "bolder"):

        self.rectangle(cord,  outline = outline, fill = fill, width = width, tag = tag)
        cord1 = [cord[0] + width, cord[1] + width, cord[2] - width * 2, cord[3] - width * 2]
        self.rectangle(cord1, outline = inline,  fill = fill, width = width, tag = tag)
        return tag

    def circle(self, cord, outline = "darkgrey", fill = "red", width = 2, tag = "circle"): ### 画圆形, 中心坐标和半径
        return super().create_oval(cord[0], cord[1], cord[2], cord[3],
            outline = outline, fill= fill, width = width, tag = tag)

    def arc(self, cord, start, duration, outline = "darkgrey", fill = "green", width = 2, tag = "arc"): ###画散形
        return super().create_arc(cord, start = start, extent = duration,
            outline = outline, fill = fill, width = width, tag = tag)

    def polygon(self, points, outline = "darkgrey", fill = "yellow", width = 2, tag = "polygon"): ## 画多边形
        return super().create_polygon(points, outline = outline, fill = fill, width =width, tag = tag)

    def line(self, x0, y0, x1, y1, fill = "red", width = 2, tag = "line"):
        return super().create_line(x0, y0, x1, y1, fill = fill, width = width, tag = tag)

    def image(self, cord, img, tag):
        return super().create_image(cord[0], cord[1], image = img, anchor = "nw", tag = tag)

#### 🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅 ###
#### Self-Definate Button
class XButton:
    def __init__(self, root, tag, command = None,
        text = "", image = None, round = False, font = ("Times", 20), width = 2,
        outline = "#434343", inline   = "#606043", active  = "#707043", inactive = "#343434", enabled = True, adjust = False):

        self.root     = root
        self.command  = command
        self.round    = round
        self.tag      = tag
        self.font     = font
        self.width    = width
        self.txtColor = "#000000"
        self.outline  = outline     ### 外框颜色
        self.inline   = inline      ### 背景颜色
        self.selectedOutline = self.outline ### 被选择后的外框颜色
        self.selectedWidth   = self.width   ### 被选择后的外框宽度
        self.active   = active      ### 按钮激活时的颜色
        self.inactive = inactive    ### 按钮未激活时的颜色
        self.enabled  = enabled
        self.cord     = None
        self.selected = False       ### 该按钮是否被选择
        self.adjust   = adjust      ### True表示需要调整框的大小进行自适应。

        self.text     = text
        self.image    = image
        self.cord     = None

    def setFill(self, color):
        self.active = color
        self.place(enabled = self.enabled)

    def initial(self, cord):
        if self.adjust:
            blankX = cord[2] / 10
            blankY = cord[3] / 10
            self.cord = [cord[0] + blankX, cord[1] + blankY, cord[2] - blankX * 2, cord[3] - blankY * 2]
        else:
            self.cord = cord
        self.root.register(cord = self.cord, command = self.click, tag = self.tag)
        self.place(enabled = self.enabled)

    ### button 资源释放
    def release(self):

        self.root.cv.delete(self.tag)            ### 删除按钮图片.
        self.root.unregister(tag = self.tag)  ###  需要释放mouse的注册函数

    ### 🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢 ###
    ### 显示文字或者图片图片，注意这两个动作是互斥的； 也就是说按钮只可能是图片或者文字，
    ### 不能同时显示text和image
    ### 其中图片大小需要与按钮的宽度和高度进行人工匹配和确认
    ### 🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢 ###
    ### 显示图片， 同时清除文字　
    def showImage(self, image):
        self.image = image
        self.text  = ""
        self.place(enabled = self.enabled)

    ### 显示文字，同时清除图片
    def showText(self, text, font = None, fill = None):
        self.image = None
        self.text  = text
        if font != None:    self.font = font
        if fill != None:    self.txtColor = fill
        #self.app.cv.delete(self.tag)
        self.place(enabled = self.enabled)

    ### 清空按钮，包括图片或者文字都被清除
    def clear(self):
        self.image = None
        self.text  = ""
        if self.cord != None:   self.place(enabled = self.enabled)


    ### 🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢 ###
    ### enable and disable the button
    ### 🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢 ###
    def state(self, status = "normal"):
        assert(status in ["normal", "disabled"])
        self.enabled = (status == "normal")
        self.place(enabled = self.enabled)

    ### 🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢 ###
    ### 按钮被点击时的回调函数, 点击按钮会有flash，通过动画实现。
    ### 🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢 ###
    def click(self, x, y, tag):
        if self.enabled:    threading.Thread(target = self.animate, args = (x, y, tag,)).start()

    def animate(self, x, y, tag):

        self.place(enabled = False)
        time.sleep(0.2)
        self.place(enabled = True)
        if self.command != None: self.command(tag = tag)

    ### 🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢 ###
    ### 按钮显示
    ### 🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢 ###
    def place(self, enabled):

        fill = self.active if enabled else self.inactive

        outline = self.selectedOutline if self.selected else self.outline
        width   = self.selectedWidth   if self.selected else self.width

        if self.round:  ###画圆角按钮
            cord1 = [self.cord[0], self.cord[1], self.cord[0] + self.cord[3], self.cord[1] + self.cord[3]]
            self.root.cv.circle(cord = cord1, outline = outline, fill = fill, width = width, tag = self.tag)

            cord1 = [self.cord[0] + self.cord[2], self.cord[1], self.cord[0] + self.cord[2] - self.cord[3], self.cord[1] + self.cord[3]]
            self.root.cv.circle(cord = cord1, outline = outline, fill = fill, width = width, tag = self.tag)

            cord1 = [self.cord[0] + self.cord[3] / 2, self.cord[1], self.cord[2] - self.cord[3], self.cord[3] + 4]
            self.root.cv.rectangle(cord = cord1, outline = outline, fill = fill, width = width, tag = self.tag)

            cord1 = [self.cord[0] + self.cord[3] / 2, self.cord[1] + 2, self.cord[2] - self.cord[3], self.cord[3]]
            self.root.cv.rectangle(cord = cord1, outline = fill, fill = fill, width = width, tag = self.tag)

        else:           ### 画直角按钮
            self.root.cv.bolder(cord = self.cord, outline = outline, inline = self.inline, fill = fill, width = width, tag = self.tag)

        ### 显示文字和图片
        if self.text != "":     self.root.cv.text(cord = self.cord, text = self.text, fill = self.txtColor, font = self.font, tag = self.tag + "_text")
        if self.image != None:  self.root.cv.image(cord = [self.cord[0] + 2, self.cord[1] + 2, 0, 0], img = self.image, tag = self.tag)

#### 🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅 ###
#### main process, the entrance of the application
if __name__ == "__main__":  pass
#### 🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅 ###
