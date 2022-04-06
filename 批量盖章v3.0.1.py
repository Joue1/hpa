# -*- coding: utf-8 -*-
from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QFileDialog
from PyQt5 import  QtWidgets
import os
from skimage import io
import numpy as np
from PIL import Image
from PySide2.QtGui import  QIcon

class Stats:

    def __init__(self):
        # 从文件中加载UI定义
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load('QTUI/main.ui')
        self.ui.lineEditFujia.setText(" 拷贝")

        self.ui.ButtonImageIn.clicked.connect(self.opendir)
        self.ui.ButtonImageOut.clicked.connect(self.savepath)
        self.ui.ButtonZhangIn.clicked.connect(self.openzhang)
        self.ui.ButtonClear.clicked.connect(self.clear)
        self.ui.ButtonRun.clicked.connect(self.run)
        self.ui.ButtonCheck.clicked.connect(self.check)

        self.ui.action_help.triggered.connect(self.helpInfo)
        self.ui.actionOpen.triggered.connect(self.delcopy)
        self.ui.action_banben.triggered.connect(self.editionInfo)

        self.ui.comboBoxImageIn.addItems(['PNG', 'JPG'])
        self.ui.comboBoxImageOut.addItems(['jpg', 'png'])

        self.ui.radioButton.setChecked(True)  #设置默认选中radioButton
    def delcopy(self):
        try:
            tifpaths = []
            ImageIn = self.ui.lineEditImageIn.text()

            def gettif(path):
                # 获取待盖章图片信息
                for rt, dirs, files in os.walk(path):
                    for each_file in files:
                        tifdict = {'name': each_file}
                        tifdict.update({'file_path': rt + '\\' + each_file})
                        tifpaths.append(tifdict)
                return tifdict

            gettif(ImageIn)
            for x in range(len(tifpaths)):
                if "拷贝" in tifpaths[x]["name"]:
                    os.remove(tifpaths[x]["file_path"])
            self.printf("删除完成")
        except:
            self.printf("无可删除文件")
    def helpInfo(self):
        self.printf("使用说明：\n"
                    "1.‘检查’按钮用来检查每一种图片的第一张的分辨率是否与章相同，不同则缩放调整章的分辨率大小\n    以便于进行正片叠底盖章;\n"
                    "2.使用‘输出到原路径‘并且删除‘附加’会覆盖掉原文件\n"
                    "3.待盖章的五种图片每一种图片分辨率必须固定,否则会跳过处理\n"
                    "4.未能处理成功的图片会在最后一起输出\n"
                    "5.‘检查’按钮的合格检测阈值设置为3，请自行判断调整后的章是否能用于盖章处理\n"
                    " ")
    def printf(self,string):
        #打印输出到textBrowser的函数
        #self.ui.textBrowser.insertPlainText(string)
        self.ui.textBrowser.append(string)  # 在指定的区域显示提示信息
        self.cursor=self.ui.textBrowser.textCursor()
        self.ui.textBrowser.moveCursor(self.cursor.End) #光标移到最后，这样就会自动显示出来
        self.ui.textBrowser.update()
        QtWidgets.QApplication.processEvents()   #使用qt实时输出，而不是全部处理完成之后一起输出
    def sumint(self):
        #一个测试的求和函数
        num1 = 1
        num2 = 3
        sum = num1 + num2
        self.printf(str(sum))
    def run(self):
        #盖章的主体函数

        self.printf("开始处理...")
        ImageIn = self.ui.lineEditImageIn.text()   #从lineEditImageIn中获取待盖章的路径
        ImageOut = self.ui.lineEditImageOut.text()    #从lineEditImageIn中获取保存的路径
        Fujia = self.ui.lineEditFujia.text()        #从lineEditImageIn中获取添加的附加字符串
        ZhangIn = self.ui.lineEditZhangIn.text()    #从lineEditImageIn中获取章的路径
        CBoxImageIn = self.ui.comboBoxImageIn.currentText()     #从comboBoxImageIn中获取待盖章图片的格式
        CBoxImageOut = self.ui.comboBoxImageOut.currentText()   #从comboBoxImageIn中获取保存图片的格式
        typeGet = self.ui.buttonGroup.checkedButton().text()

        tifpaths = []
        zhangdict = {}
        zhangpaths = []
        ZongdiInfo,ZongdizongtuInfo,QuanjiZongInfo,QuanjiHengInfo,JiezhidianInfo = [],[],[],[],[]
        tifdict = {}
        if os.path.exists(ImageIn) and os.path.exists(ZhangIn):
            def gettif(path):
                global tifdict
                #获取待盖章图片信息
                self.printf("获取待盖章图片信息")
                for rt, dirs, files in os.walk(path):
                    for each_file in files:
                        if each_file.rpartition('.')[2].upper() == CBoxImageIn:
                            tifdict = {'name': each_file}
                            img = Image.open(rt + '\\' + each_file)
                            imgSize = img.size
                            imgSizeW = str(imgSize[0])
                            imgSizeH = str(imgSize[1])
                            imgSizeStr = str(imgSize).replace("(", "").replace(")", "").replace(" ", "")
                            tifdict.update({"size": imgSizeStr})
                            tifdict.update({"imgSizeW":int(imgSizeW)})
                            tifdict.update({"imgSizeH": int(imgSizeH)})
                            tifdict.update({'file_path': rt + '\\' + each_file})
                            tifdict.update({"path": rt})
                            if "宗地图" in tifdict["name"]:
                                ZongdiInfo.append(tifdict)
                            if "界址点" in tifdict["name"]:
                                JiezhidianInfo.append(tifdict)
                            if "农房平面总图" in tifdict["name"]:
                                ZongdizongtuInfo.append(tifdict)
                            if "不动产权籍" in tifdict["name"] and tifdict["imgSizeW"] < 3000:
                                QuanjiZongInfo.append(tifdict)
                            if "不动产权籍" in tifdict["name"] and tifdict["imgSizeW"] > 3000:
                                QuanjiHengInfo.append(tifdict)
                            else:
                                pass
                            #self.printf(tifdict)
                            tifpaths.append(tifdict)

                return tifdict
            gettif(ImageIn)

            self.ui.lineEditZongdi.setText(ZongdiInfo[0]["size"])
            self.ui.lineEditZongdizongtu.setText(ZongdizongtuInfo[0]["size"])
            self.ui.lineEditQuanjiZong.setText(QuanjiZongInfo[0]["size"])
            self.ui.lineEditQuanjiHeng.setText(QuanjiHengInfo[0]["size"])
            self.ui.lineEditJiezhidian.setText(JiezhidianInfo[0]["size"])

            #从各个图片的分辨率文本编辑框获取到分辨率字符串
            Zongdi = self.ui.lineEditZongdi.text()
            Zongdizongtu = self.ui.lineEditZongdizongtu.text()
            QuanjiZong = self.ui.lineEditQuanjiZong.text()
            QuanjiHeng = self.ui.lineEditQuanjiHeng.text()
            Jiezhidian = self.ui.lineEditJiezhidian.text()

            #self.printf(tifpaths)
            def getzhang(path):
                global zhangdict
                for rt, dirs, files in os.walk(path):

                    for each_file in files:
                        if each_file.rpartition('.')[2].upper() == "JPG":
                            zhangpaths.append(rt + '\\' + each_file)
                # return zhangdict
            getzhang(ZhangIn)

            #self.printf(zhangpaths)
            # 输出方式：输出到原路径
            if typeGet == "输出到原路径":
                self.printf("开始输出到原路径")
                file_weichuli = []
                for x in range(len(tifpaths)):
                    SavePath = tifpaths[x]["path"]
                    file_name = tifpaths[x]["file_path"]
                    try:
                        def photoAndphoto(SaveFilePath,ZhangNum):
                            img1_1 = io.imread(file_name)
                            img1_1 = img1_1 / 255.0
                            img1_2 = io.imread(zhangpaths[ZhangNum])
                            img1_2 = img1_2 / 255.0
                            img = img1_1 * img1_2
                            # 保存图片
                            new_img = (img * 255.0).astype(np.uint8)
                            io.imsave(SaveFilePath, new_img)
                            self.printf(str(tifpaths[x]["name"]) + " " + "盖章完成")
                        if __name__ == "__main__":
                            if tifpaths[x]['size'] == Zongdi and "宗地图" in zhangpaths[3]:
                                ZhangNum = 3
                                ExtImageIn = "." + CBoxImageIn
                                save_file_name = str(tifpaths[x]["name"]).upper().replace(ExtImageIn,
                                                                                          Fujia + "." + CBoxImageOut)
                                SaveFilePath = SavePath + "\\" + save_file_name
                                photoAndphoto(SaveFilePath,ZhangNum)
                            elif tifpaths[x]['size'] == Zongdizongtu and "平面总图" in zhangpaths[2]:
                                ZhangNum = 2
                                ExtImageIn = "." + CBoxImageIn
                                save_file_name = str(tifpaths[x]["name"]).upper().replace(ExtImageIn,
                                                                                          Fujia + "." + CBoxImageOut)
                                SaveFilePath = SavePath + "\\" + save_file_name
                                photoAndphoto(SaveFilePath, ZhangNum)
                            elif tifpaths[x]['size'] == QuanjiZong and "权籍调查表" in zhangpaths[1]:
                                ZhangNum = 1
                                ExtImageIn = "." + CBoxImageIn
                                save_file_name = str(tifpaths[x]["name"]).upper().replace(ExtImageIn,
                                                                                          Fujia + "." + CBoxImageOut)
                                SaveFilePath = SavePath + "\\" + save_file_name
                                photoAndphoto(SaveFilePath, ZhangNum)
                            elif tifpaths[x]['size'] == QuanjiHeng and "权籍调查表" in zhangpaths[0]:
                                ZhangNum = 0
                                ExtImageIn = "." + CBoxImageIn
                                save_file_name = str(tifpaths[x]["name"]).upper().replace(ExtImageIn,
                                                                                          Fujia + "." + CBoxImageOut)
                                SaveFilePath = SavePath + "\\" + save_file_name
                                photoAndphoto(SaveFilePath, ZhangNum)
                            elif tifpaths[x]['size'] == Jiezhidian and "界址点" in zhangpaths[4]:
                                ZhangNum = 4
                                ExtImageIn = "." + CBoxImageIn
                                save_file_name = str(tifpaths[x]["name"]).upper().replace(ExtImageIn,
                                                                                          Fujia + "." + CBoxImageOut)
                                SaveFilePath = SavePath + "\\" + save_file_name
                                photoAndphoto(SaveFilePath, ZhangNum)
                            else:
                                file_weichuli.append(tifpaths[x]["name"])
                                pass
                                # self.printf("----------")
                                # file_weichuli.append(tifpaths[x]["name"])
                                # self.printf(str(tifpaths[x]["name"]) + " " + "未处理")
                    except:
                        file_weichuli.append(tifpaths[x]["name"])
                if len(file_weichuli) > 0:
                    self.printf("----------")
                    for file_wei in file_weichuli:
                        self.printf(file_wei + " " + "未处理")
                    self.printf("----------")
                    self.printf("可盖章的已全部完成")
                    self.printf("----------")
                    self.printf(" ")
                else:
                    self.printf(" ")
                    self.printf("已全部完成")
                    self.printf("----------")
                    self.printf(" ")

            # 输出方式：输出到新路径
            if typeGet == "输出到新路径":
                self.printf("待更新'输出到新路径'功能")
                # ZongdiNewPaths, ZongdizongtuNewPaths, jiezhidianNewPaths, quanjiNewPaths = [], [], [], []
                #
                # def getNewpath(path):
                #     # 得到一个新路径的字典列表
                #     for rt, dirs, files in os.walk(path):
                #         folderName = str(rt).split("\\")
                #         if folderName[-1] == "宗地图":
                #             zongdidict = {'name': folderName[-1]}
                #             Newfolderpath = str(rt).replace(ImageIn, ImageOut)
                #             zongdidict.update({"folderpath": Newfolderpath})
                #             ZongdiNewPaths.append(zongdidict)
                #         if folderName[-1] == "总图":
                #             zongdizongtudict = {'name': folderName[-1]}
                #             Newfolderpath = str(rt).replace(ImageIn, ImageOut)
                #             zongdizongtudict.update({"folderpath": Newfolderpath})
                #             ZongdizongtuNewPaths.append(zongdizongtudict)
                #         if folderName[-1] == "界址点":
                #             jiezhidiandict = {'name': folderName[-1]}
                #             Newfolderpath = str(rt).replace(ImageIn, ImageOut)
                #             jiezhidiandict.update({"folderpath": Newfolderpath})
                #             jiezhidianNewPaths.append(jiezhidiandict)
                #         if folderName[-1] == "权籍":
                #             quanjidict = {'name': folderName[-1]}
                #             Newfolderpath = str(rt).replace(ImageIn, ImageOut)
                #             quanjidict.update({"folderpath": Newfolderpath})
                #             quanjiNewPaths.append(quanjidict)
                # getNewpath(ImageIn)
                # os.makedirs(ZongdiNewPaths[0]["folderpath"])
                # os.makedirs(ZongdizongtuNewPaths[0]["folderpath"])
                # os.makedirs(jiezhidianNewPaths[0]["folderpath"])
                # os.makedirs(quanjiNewPaths[0]["folderpath"])
                # for x in range(len(tifpaths)):
                #     SavePath = tifpaths[x]["path"]
                #     file_name = tifpaths[x]["file_path"]
                #     def photoAndphoto(SaveFilePath,ZhangNum):
                #         img1_1 = io.imread(file_name)
                #         img1_1 = img1_1 / 255.0
                #         img1_2 = io.imread(zhangpaths[ZhangNum])
                #         img1_2 = img1_2 / 255.0
                #
                #         img = img1_1 * img1_2
                #         # 保存图片
                #         new_img = (img * 255.0).astype(np.uint8)
                #         io.imsave(SaveFilePath, new_img)
                #         self.printf(str(tifpaths[x]["name"]) + " " + "盖章完成")
                #     if __name__ == "__main__":
                #         if tifpaths[x]['size'] == zongdi and "宗地图" in zhangpaths[3]:
                #                 print(zongdi)
                #                 ZhangNum = 3
                #                 In_extension2 = "." + CBoxImageOut
                #                 save_file_name = str(tifpaths[x]["name"]).upper().replace(In_extension2, Fujia + "." + CBoxImageOut)
                #                 SaveFilePath = ZongdiNewPaths[0]["folderpath"] + "\\" + save_file_name
                #                 photoAndphoto(SaveFilePath,ZhangNum)
        else:
            pass
            self.printf("请输入正确的路径")
            self.printf(" ")

    def check(self):
        self.printf("开始检查...")
        ImageIn = self.ui.lineEditImageIn.text()
        ZhangIn = self.ui.lineEditZhangIn.text()
        CBoxImageIn = self.ui.comboBoxImageIn.currentText()     #从comboBoxImageIn中获取待盖章图片的格式
        CBoxImageOut = self.ui.comboBoxImageOut.currentText()   #从comboBoxImageIn中获取保存图片的格式
        zhangpaths = []

        tifpaths = []
        zongdiList,zongdizongtuList,quanjiHengList,quanjiZongList,JZDList = [],[],[],[],[]
        # zongdizongtuList = []
        # quanjiHengList = []
        # quanjiZongList = []
        # JZDList = []
        zongdiZhang,zongdizongtuZhang,quanjiHengZhang,quanjiZongZhang,JZDZhang = [],[],[],[],[]
        # zongdizongtuZhang = []
        # quanjiHengZhang = []
        # quanjiZongZhang = []
        # JZDZhang = []
        Zhangdict = {}
        tifdict = {}
        if os.path.exists(ImageIn) and os.path.exists(ZhangIn):
            def getZhangInfo(path):
                global Zhangdict
                for rt, dirs, files in os.walk(path):
                    # print(rt)
                    for each_file in files:
                        if each_file.rpartition('.')[2].upper() == "JPG":
                            Zhangdict = {'name': each_file}
                            img = Image.open(rt + '\\' + each_file)
                            imgSize = img.size
                            imgSizeW = str(imgSize[0])
                            imgSizeH = str(imgSize[1])
                            imgSizeStr = str(imgSize).replace("(", "").replace(")", "").replace(" ", "")
                            Zhangdict.update({"size": imgSizeStr})
                            Zhangdict.update({"imgSizeW": int(imgSizeW)})
                            Zhangdict.update({"imgSizeH": int(imgSizeH)})
                            # print(imgSize[0])
                            Zhangdict.update({'file_path': rt + '\\' + each_file})
                            Zhangdict.update({"path": rt})
                            if "宗地图" in Zhangdict["name"]:
                                zongdiZhang.append(Zhangdict)
                            if "界址点" in Zhangdict["name"]:
                                JZDZhang.append(Zhangdict)
                            if "农房平面总图" in Zhangdict["name"]:
                                zongdizongtuZhang.append(Zhangdict)
                            if "不动产权籍" in Zhangdict["name"] and Zhangdict["imgSizeW"] < 3000:
                                quanjiZongZhang.append(Zhangdict)
                            if "不动产权籍" in Zhangdict["name"] and Zhangdict["imgSizeW"] > 3000:
                                quanjiHengZhang.append(Zhangdict)
                            else:
                                pass
                            zhangpaths.append(Zhangdict)
                return Zhangdict
            getZhangInfo(ZhangIn)

            def gettif(path):
                global tifdict
                for rt, dirs, files in os.walk(path):
                    # print(rt)
                    for each_file in files:
                        if each_file.rpartition('.')[2].upper() == CBoxImageIn:
                            tifdict = {'name': each_file}
                            img = Image.open(rt + '\\' + each_file)
                            imgSize = img.size
                            imgSizeW = str(imgSize[0])
                            imgSizeH = str(imgSize[1])
                            imgSizeStr = str(imgSize).replace("(", "").replace(")", "").replace(" ", "")
                            tifdict.update({"size": imgSizeStr})
                            tifdict.update({"imgSizeW": int(imgSizeW)})
                            tifdict.update({"imgSizeH": int(imgSizeH)})
                            # print(imgSize[0])
                            tifdict.update({'file_path': rt + '\\' + each_file})
                            tifdict.update({"path": rt})
                            if "宗地图" in tifdict["name"]:
                                zongdiList.append(tifdict)
                            if "界址点成果" in tifdict["name"]:
                                JZDList.append(tifdict)
                            if "农房平面总图" in tifdict["name"]:
                                zongdizongtuList.append(tifdict)
                            if "不动产权籍" in tifdict["name"] and tifdict["imgSizeW"] < 3000:
                                quanjiZongList.append(tifdict)
                            if "不动产权籍" in tifdict["name"] and tifdict["imgSizeW"] > 3000:
                                quanjiHengList.append(tifdict)
                            else:
                                pass
                            tifpaths.append(tifdict)
                return tifdict

            gettif(ImageIn)

            # 根据读取到的图片分辨率调整章的分辨率
            def ResizeImage(filein, fileout, fileList):
                """
                改变图片大小
                :param filein: 输入图片
                :param fileout: 输出图片
                :param width: 输出图片宽度
                :param height: 输出图片宽度
                :param type: 输出图片类型（png, gif, jpeg...）
                :return:
                """
                # img = Image.open(zongdiZhang[0]["file_path"])
                img = Image.open(filein)
                width = fileList[0]['imgSizeW']
                height = fileList[0]['imgSizeH']
                type = img.format
                out = img.resize((width, height), Image.ANTIALIAS)
                # 第二个参数：
                # Image.NEAREST ：低质量
                # Image.BILINEAR：双线性
                # Image.BICUBIC ：三次样条插值
                # Image.ANTIALIAS：高质量
                out.save(fileout, type)  #

            if __name__ == "__main__":
                self.printf("开始检查是否需要调整章的分辨率")
                self.printf("")
                if zongdiZhang[0]["imgSizeW"] != zongdiList[0]["imgSizeW"] or zongdiZhang[0]["imgSizeH"] != \
                        zongdiList[0]["imgSizeH"]:
                    filein = zongdiZhang[0]["file_path"]
                    fileout = zongdiZhang[0]['file_path']
                    fileList = zongdiList
                    ResizeImage(filein, fileout, fileList)
                if zongdizongtuZhang[0]["imgSizeW"] != zongdizongtuList[0]["imgSizeW"] or zongdizongtuZhang[0][
                    "imgSizeH"] != zongdizongtuList[0]["imgSizeH"]:
                    filein = zongdizongtuZhang[0]["file_path"]
                    fileout = zongdizongtuZhang[0]['file_path']
                    fileList = zongdizongtuList
                    ResizeImage(filein, fileout, fileList)
                if JZDZhang[0]["imgSizeW"] != JZDList[0]["imgSizeW"] or JZDZhang[0]["imgSizeH"] != JZDList[0][
                    "imgSizeH"]:
                    filein = JZDZhang[0]["file_path"]
                    fileout = JZDZhang[0]['file_path']
                    fileList = JZDList
                    ResizeImage(filein, fileout, fileList)
                if quanjiHengZhang[0]["imgSizeW"] != quanjiHengList[0]["imgSizeW"] or quanjiHengZhang[0]["imgSizeH"] != \
                        quanjiHengList[0]["imgSizeH"]:
                    filein = quanjiHengZhang[0]["file_path"]
                    fileout = quanjiHengZhang[0]['file_path']
                    fileList = quanjiHengList
                    ResizeImage(filein, fileout, fileList)
                if quanjiZongZhang[0]["imgSizeW"] != quanjiZongList[0]["imgSizeW"] or quanjiZongZhang[0]["imgSizeH"] != \
                        quanjiZongList[0]["imgSizeH"]:
                    filein = quanjiZongZhang[0]["file_path"]
                    fileout = quanjiZongZhang[0]['file_path']
                    fileList = quanjiZongList
                    ResizeImage(filein, fileout, fileList)
                else:
                    pass
            Zhangdictafter = {}
            zhangpathsafter,zongdiZhangafter,JZDZhangafter,zongdizongtuZhangafter,quanjiZongZhangafter,quanjiHengZhangafter = [],[],[],[],[],[]
            # zongdiZhangafter = []
            # JZDZhangafter = []
            # zongdizongtuZhangafter = []
            # quanjiZongZhangafter = []
            # quanjiHengZhangafter = []

            def getZhangInfoafter(path):
                global Zhangdictafter
                for rt, dirs, files in os.walk(path):
                    # print(rt)
                    for each_file in files:
                        if each_file.rpartition('.')[2].upper() == "JPG":
                            Zhangdictafter = {'name': each_file}
                            img = Image.open(rt + '\\' + each_file)
                            imgSize = img.size
                            imgSizeW = str(imgSize[0])
                            imgSizeH = str(imgSize[1])
                            imgSizeStr = str(imgSize).replace("(", "").replace(")", "").replace(" ", "")
                            Zhangdictafter.update({"size": imgSizeStr})
                            Zhangdictafter.update({"imgSizeW": int(imgSizeW)})
                            Zhangdictafter.update({"imgSizeH": int(imgSizeH)})
                            # print(imgSize[0])
                            Zhangdictafter.update({'file_path': rt + '\\' + each_file})
                            Zhangdictafter.update({"path": rt})

                            if "宗地图" in Zhangdictafter["name"]:
                                zongdiZhangafter.append(Zhangdictafter)
                            if "界址点" in Zhangdictafter["name"]:
                                JZDZhangafter.append(Zhangdictafter)
                            if "农房平面总图" in Zhangdictafter["name"]:
                                zongdizongtuZhangafter.append(Zhangdictafter)
                            if "不动产权籍" in Zhangdictafter["name"] and Zhangdictafter["imgSizeW"] < 3000:
                                quanjiZongZhangafter.append(Zhangdictafter)
                            if "不动产权籍" in Zhangdictafter["name"] and Zhangdictafter["imgSizeW"] > 3000:
                                quanjiHengZhangafter.append(Zhangdictafter)
                            else:
                                pass
                            zhangpathsafter.append(Zhangdictafter)
                return Zhangdictafter

            getZhangInfoafter(ZhangIn)

            zongdiZhangMark = False
            zongdizongtuMark = False
            JZDZhangMark = False
            quanjiHengZhangMark = False
            quanjiZongZhangMark = False
            if abs(zongdiZhangafter[0]["imgSizeW"] - zongdiZhang[0]["imgSizeW"]) < 3 and abs(
                    zongdiZhangafter[0]["imgSizeH"] - zongdiZhang[0]["imgSizeH"]) < 3:
                zongdiZhangMark = True
            self.printf("宗地图章分辨率调整值为：" + str(zongdiZhangafter[0]["imgSizeW"] - zongdiZhang[0]["imgSizeW"]) + "," + str(
                zongdiZhangafter[0]["imgSizeH"] - zongdiZhang[0]["imgSizeH"]))
            if abs(zongdizongtuZhangafter[0]["imgSizeW"] - zongdizongtuZhang[0]["imgSizeW"]) < 3 and abs(
                    zongdizongtuZhangafter[0]["imgSizeH"] - zongdizongtuZhang[0]["imgSizeH"]) < 3:
                zongdizongtuMark = True
            self.printf("农房平面总图章分辨率调整值为：" + str(
                zongdizongtuZhangafter[0]["imgSizeW"] - zongdizongtuZhang[0]["imgSizeW"]) + "," + str(
                zongdizongtuZhangafter[0]["imgSizeH"] - zongdizongtuZhang[0]["imgSizeH"]))
            if abs(JZDZhangafter[0]["imgSizeW"] - JZDZhang[0]["imgSizeW"]) < 3 and abs(
                    JZDZhangafter[0]["imgSizeH"] - JZDZhang[0]["imgSizeH"]) < 3:
                JZDZhangMark = True
            self.printf("界址点章分辨率调整值为：" + str(JZDZhangafter[0]["imgSizeW"] - JZDZhang[0]["imgSizeW"]) + "," + str(
                JZDZhangafter[0]["imgSizeH"] - JZDZhang[0]["imgSizeH"]))
            if abs(quanjiHengZhangafter[0]["imgSizeW"] - quanjiHengZhang[0]["imgSizeW"]) < 3 and abs(
                    quanjiHengZhangafter[0]["imgSizeH"] - quanjiHengZhang[0]["imgSizeH"]) < 3:
                quanjiHengZhangMark = True
            self.printf("不动产权籍调查表章-房屋章分辨率调整值为：" + str(
                quanjiHengZhangafter[0]["imgSizeW"] - quanjiHengZhang[0]["imgSizeW"]) + "," + str(
                quanjiHengZhangafter[0]["imgSizeH"] - quanjiHengZhang[0]["imgSizeH"]))
            if abs(quanjiZongZhangafter[0]["imgSizeW"] - quanjiZongZhang[0]["imgSizeW"]) < 3 and abs(
                    quanjiZongZhangafter[0]["imgSizeH"] - quanjiZongZhang[0]["imgSizeH"]) < 3:
                quanjiZongZhangMark = True
            self.printf("不动产权籍调查表章分辨率调整值为：" + str(
                quanjiZongZhangafter[0]["imgSizeW"] - quanjiZongZhang[0]["imgSizeW"]) + "," + str(
                quanjiZongZhangafter[0]["imgSizeH"] - quanjiZongZhang[0]["imgSizeH"]))

            if zongdiZhangMark and zongdizongtuMark and JZDZhangMark and quanjiHengZhangMark and quanjiZongZhangMark:
                self.printf("-------------")
                self.printf("检查通过，可开始进行盖章。")
                self.printf("-------------")
            else:
                self.printf("-------------")
                self.printf("不可进行盖章!请检查路径下的章是否有较大形变")
        else:
            self.printf("请输入正确的路径")
    def opendir(self):
        #选择打开路径
        filePath = QFileDialog.getExistingDirectory(self.ui, "选择打开路径")
        self.ui.lineEditImageIn.setText(filePath)
    def savepath(self):
        #打开保存路径
        SaveFilePath = QFileDialog.getExistingDirectory(self.ui, "选择存储路径")
        self.ui.lineEditImageOut.setText(SaveFilePath)
    def openzhang(self):
        #打开章的路径
        ZhangFilePath = QFileDialog.getExistingDirectory(self.ui, "选择存储路径")
        self.ui.lineEditZhangIn.setText(ZhangFilePath)
    def clear(self):
        #清空输入框数据
        self.ui.lineEditImageIn.clear()
        self.ui.lineEditImageOut.clear()
        self.ui.lineEditZhangIn.clear()
    def editionInfo(self):
        QMessageBox.about(self.ui,
                          '版本v3.0.1',
'''
1.改进算法;\n2.使用pyside2编写界面，优化打开速度\n3.使用try,跳过异常处理，并将未能盖章的图片放在最后输出到下方textBrowser
'''
                          )

app = QApplication([])
app.setWindowIcon(QIcon('QTUI/mylogo.png'))
stats = Stats()
stats.ui.show()
app.exec_()
