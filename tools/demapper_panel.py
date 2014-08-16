#!/usr/bin/env python
#coding=utf-8
#################################
#   Copyright 2014.8.15
#       fly_vedio 
#   @author: 345570600@qq.com
#################################
import wx  
import scipy
import os
import sys
import lte_sat
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx


#设置系统默认编码方式，不用下面两句，中文会乱码
reload(sys)
sys.setdefaultencoding("utf-8")    

class MainFrame(wx.Frame):
    def __init__(self,parent,id):
        wx.Frame.__init__(self, None, title=u"星座图绘制", size=(1000,700))
        self.Centre()

        self.SetBackgroundColour("white")

        #创建面板
        self.createframe()

    def createframe(self):
        #星座图绘制区域
        self.figure = Figure()
        self.canvas = FigureCanvas(self, -1, self.figure)

        self.toolbar=NavigationToolbar2Wx(self.canvas)
        self.toolbar.AddLabelTool(5,'',wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, (32,32)))

        self.toolbar.Realize()

        self.button1 = wx.Button(self, -1, "PCFI星座图")
        self.button1.SetBackgroundColour('black')
        self.button1.SetForegroundColour('white')
        self.Bind(wx.EVT_BUTTON,self.draw_scatter,self.button1)

        self.button2 = wx.Button(self, -1, "PDCCH星座图")
        self.button2.SetBackgroundColour('black')
        self.button2.SetForegroundColour('white')
        self.Bind(wx.EVT_BUTTON,self.draw_scatter,self.button2)

        self.button3 = wx.Button(self, -1, "PDSCH星座图")
        self.button3.SetBackgroundColour('black')
        self.button3.SetForegroundColour('white')
        self.Bind(wx.EVT_BUTTON,self.draw_scatter,self.button3)

        self.cb_grid = wx.CheckBox(self, -1, 
            "显示网格",
            style=wx.ALIGN_RIGHT)

        #小区ID
        id_cell = wx.StaticText(self, -1, u'小区ID:')
        self.id_cell_t = wx.TextCtrl(self, -1, "0", style=wx.TE_READONLY)

        #系统带宽
        bandwidth = wx.StaticText(self, -1, u'系统带宽:')
        self.bandwidth_t = wx.TextCtrl(self, -1, "0", style=wx.TE_READONLY)

        #RNTI
        RNTI_st = wx.StaticText(self, -1, u"RNTI:")
        self.RNTI = wx.SpinCtrl(self, -1, "", (-1, -1))
        self.RNTI.SetRange(61,65523)
        self.RNTI.SetValue(100)

        #sfn
        sfn_st = wx.StaticText(self, -1, u"子帧总数:")
        self.sfn = wx.TextCtrl(self, -1, "", style=wx.TE_READONLY)

        #sfn_scope
        sfn_scope_st = wx.StaticText(self, -1, u"请输入子帧号的范围(上限：子帧总数):")
        self.LOW = wx.TextCtrl(self, -1, "0",size=(80,30))
        self.sfn_scope_zhi = wx.StaticText(self, -1, u"至")
        self.HIGH = wx.TextCtrl(self, -1, "100")
        
        #选择文件
        self.button_file = wx.Button(self, label="选择")
        self.Bind(wx.EVT_BUTTON,self.file_select,self.button_file)

        #数据源
        data_st = wx.StaticText(self, -1, u"数据源:")
        self.data_t = wx.TextCtrl(self, -1, "", style=wx.TE_READONLY)

        ########开始布局############
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(self.button1,1,wx.EXPAND)
        sizer1.Add(self.button2,1,wx.EXPAND)
        sizer1.Add(self.button3,1,wx.EXPAND)

        sizer2 = wx.FlexGridSizer(cols=4, hgap=5, vgap=5)
        sizer2.AddGrowableCol(1)
        sizer2.AddGrowableCol(3)
        sizer2.Add(RNTI_st, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        sizer2.Add(self.RNTI, 0, wx.EXPAND)

        sizer2.Add(sfn_st, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        sizer2.Add(self.sfn, 0, wx.EXPAND)

        sizer2.Add(id_cell, 0, wx.ALIGN_RIGHT)
        sizer2.Add(self.id_cell_t, 0, wx.EXPAND)
        sizer2.Add(bandwidth, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        sizer2.Add(self.bandwidth_t, 0, wx.EXPAND)

        sizer3 = wx.FlexGridSizer(cols=4, hgap=5, vgap=5)
        sizer3.AddGrowableCol(1)
        sizer3.Add(data_st, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        sizer3.Add(self.data_t, 0,wx.EXPAND)
        sizer3.Add(self.button_file, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        sizer3.Add(self.cb_grid, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)

        sizer4 = wx.FlexGridSizer(cols=4, hgap=5, vgap=5)
        # sizer4.AddGrowableCol(1)
        sizer4.Add(sfn_scope_st, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        sizer4.Add(self.LOW, 0,wx.EXPAND)
        sizer4.Add(self.sfn_scope_zhi, 0,wx.ALIGN_CENTER_VERTICAL)
        sizer4.Add(self.HIGH, 0,wx.EXPAND)

        sizer5 = wx.StaticBoxSizer(wx.StaticBox(self, wx.NewId(), u'星座图信息'), wx.VERTICAL)
        sizer5.Add(sizer2, 0, wx.EXPAND | wx.ALL, 10)
        sizer5.Add(sizer4, 0, wx.EXPAND | wx.ALL, 10)
        sizer5.Add(sizer3, 0, wx.EXPAND | wx.ALL, 10)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.sizer.Add(wx.StaticLine(self), 0,wx.EXPAND|wx.TOP|wx.BOTTOM,5)
        self.sizer.Add(sizer1, 0, wx.EXPAND)
        self.sizer.Add(wx.StaticLine(self), 0,wx.EXPAND|wx.TOP|wx.BOTTOM,5)
        self.sizer.Add(sizer5,0,wx.EXPAND)
        self.sizer.Add(self.toolbar, 0, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()

    def file_select(self,event):
        wildcard = "Source data (*.dat)|*.dat|" \
            "All files (*.*)|*.*"
        file_path = wx.FileDialog(None, "选择文件", os.getcwd(), 
                "", wildcard, wx.OPEN)
        if file_path.ShowModal() == wx.ID_OK:
            self.data_t.SetValue(file_path.GetPath())
        file_path.Destroy()
        self.process()

    def process(self):
        self.file = open(self.data_t.GetValue(),'rb')
        self.file.seek(0,2)
        end = self.file.tell()
        total_sfn = (end-8)/(8064)
        self.sfn.SetValue(str(total_sfn))
        self.file.seek(0,0)
        self.x = np.fromfile ( self.file , dtype = np.int32 , count = 2 )
        self.id_cell_t.SetValue(str(self.x[0]))
        self.bandwidth_t.SetValue(str(self.x[1]))
        self.file.close()

    def draw_scatter(self,event):
        self.figure.clear() 
        self.axes = self.figure.add_subplot(111)
        self.axes.clear()
        self.axes.grid(self.cb_grid.IsChecked())
        try:
            self.file = open(self.data_t.GetValue(),'rb')
        except:
            self.file_select(event)
            self.file = open(self.data_t.GetValue(),'rb')
        self.file.seek(8,1)
        sfn_low = int(self.LOW.GetValue())
        sfn_high = int(self.HIGH.GetValue())
        N = sfn_high - sfn_low +1
        len_sf = 1008

        self.file.seek(sfn_low*len_sf*2*4,1)
        print self.file.tell()
        y = np.fromfile ( self.file , dtype = np.float32 , count = len_sf*2*N)
        self.file.close()

        real_list = []
        imag_list = []
        for i in range(len_sf*2*N):
            if i%2==0:
                real_list.append(y[i])
            else:
                imag_list.append(y[i])

        self.dl_subframe_demapper = lte_sat.dl_subframe_demapper(int(self.RNTI.GetValue()))
        self.dl_subframe_demapper.set_cell_id(int(self.x[0]))
        self.dl_subframe_demapper.set_rb_count(int(self.x[1]))
        
        real_total_list = zip(*[iter(real_list)]*len_sf)
        imag_total_list = zip(*[iter(imag_list)]*len_sf)
        # real_list.reshape(N,len_sf)
        # imag_list.reshape(N,len_sf)
        pcfich_total_real = []
        pcfich_total_imag = []
        for i in range(N):
            """ Reconstruct the original complex array """
            wfc = np.zeros ( [ len_sf ] , dtype = np.complex )
            wfc.real = real_total_list[i]
            wfc.imag = imag_total_list[i]
            self.dl_subframe_demapper.demux(wfc, (i+sfn_low)%10)
            # self.dl_subframe_demapper.demux(wfc, 0)
            pcfich_data = self.dl_subframe_demapper.get_red(0)

            pcfich_real = []
            pcfich_imag = []
            for i in range(len(pcfich_data)):
                pcfich_real.append(pcfich_data[i].real)
                pcfich_imag.append(pcfich_data[i].imag)

                pcfich_total_real = pcfich_total_real + pcfich_real
                pcfich_total_imag = pcfich_total_imag + pcfich_imag

        self.axes.scatter( pcfich_total_real, pcfich_total_imag, facecolor='blue' )
        self.canvas.draw()

    
    def OnCloseWindow(self, event):
        self.Destroy()

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MainFrame(parent=None, id=-1)
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True

if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()

