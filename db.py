#!/usr/bin/env python3
__author__ = "Copyright ⓒ 2019 by www.chenxuanwei.com"
### 🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊 ###
### 数据库文件读写函数: File
### 🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊 ###
import csv, tkinter, os
class Database:
    ImagePath = "/Users/tony/local_raspberra"
    DataPath  = "/Users/tony/mApp/data"

    ### 🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴 ###
    ### 读取图像文件,返回图像文件句柄
    ### 🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴 ###
    def loadImage(self, file, where = None):
        global image
        filename = "%s/%s.png" %(self.ImagePath, file) if where == None else "%s/%s/%s.png" %(self.ImagePath, where, file)
        image = tkinter.PhotoImage(file =  filename)
        return image

    ### 批处理图像文件读取，返回字典： key为文件名，value为图像文件句柄。
    def loadImages(self, files, where = None):
        answer = dict()
        for file in files: answer[file] = self.loadImage(file = file, where = where)
        return answer

    ### 🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴 ###
    ### 读取csv文件,返回图像文件句柄, 其中upload（）采用yield方式返回数据
    ### 🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴 ###
    ### 读取csv文件，按照csv格式读取，也就是说每一行为一个数组，按照逗号进行分割，如果该行前三个字符为 ###表示该行为注释

    def upload(self, file, where = None):
        filename = "%s/%s.dat" %(self.DataPath, file) if where == None else "%s/%s/%s.dat" %(self.DataPath, where, file)
        if not os.path.isfile(filename): return

        with open(filename, newline = "") as f:
            reader = csv.reader(f)
            for data in reader:
                if len(data[0]) > 3 and data[0][:3] == "###":  ###注释文字
                    print("DB::upload().data = {}".format(data[0]))
                else:
                    yield data

    ### 将二维数组写入到csv文件中，第一行写注释

    def download(self, data, file, where = None, comment = []):
        filename = "%s/%s.dat" %(self.DataPath, file) if where == None else "%s/%s/%s.dat" %(self.DataPath, where, file)
        with open(filename, "w") as f:
            writer = csv.writer(f)
            if len(comment) > 1:
                comment[0] = "### " + comment[0]
                writer.writerow(comment)
            for tuple in data: writer.writerow(tuple)
        return

### 🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊 ###
if __name__ == "__main__": pass
### 🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊🍊 ###
