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
        wx.Frame.__init__(self, None, title=u"星座图绘制")

        self.panel = wx.Panel(self, -1, style = wx.RAISED_BORDER|wx.TAB_TRAVERSAL)
        self.panel.SetBackgroundColour("white")

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
        self.Bind(wx.EVT_BUTTON,self.draw_pcfich, self.button1)

        self.button2 = wx.Button(self, -1, "PDCCH星座图")
        self.button2.SetBackgroundColour('black')
        self.button2.SetForegroundColour('white')
        self.Bind(wx.EVT_BUTTON, self.draw_pdcch, self.button2)

        self.button3 = wx.Button(self, -1, "PDSCH星座图")
        self.button3.SetBackgroundColour('black')
        self.button3.SetForegroundColour('white')
        self.Bind(wx.EVT_BUTTON,self.draw_pdsch, self.button3)

        #RNTI
        RNTI_st = wx.StaticText(self.panel, -1, u"RNTI:")
        self.RNTI = wx.SpinCtrl(self.panel, -1, "", (-1, -1))
        self.RNTI.SetRange(61,65523)
        self.RNTI.SetValue(100)

        #sfn
        sfn_st = wx.StaticText(self.panel, -1, u"子帧总数:")
        self.sfn = wx.TextCtrl(self.panel, -1, "", style=wx.TE_READONLY)

        #小区ID
        id_cell = wx.StaticText(self.panel, -1, u'小区ID:')
        self.id_cell_t = wx.TextCtrl(self.panel, -1, "0", style=wx.TE_READONLY)

        #系统带宽
        bandwidth = wx.StaticText(self.panel, -1, u'系统带宽:')
        self.bandwidth_t = wx.TextCtrl(self.panel, -1, "0", style=wx.TE_READONLY)

        #sfn_number
        sfn_start_st = wx.StaticText(self.panel, -1, u"起始帧号:")
        self.sfn_start = wx.TextCtrl(self.panel, -1, "0",size=(80,30))
        sfn_total_st = wx.StaticText(self.panel, -1, u"子帧总数:")
        self.sfn_total = wx.TextCtrl(self.panel, -1, "100")

        #刷新处理按钮
        self.refresh = wx.Button(self.panel, label="刷新")
        self.Bind(wx.EVT_BUTTON,self.process,self.refresh)
        self.refresh.SetBackgroundColour('black')
        self.refresh.SetForegroundColour('white')
        
        #选择文件
        self.button_file = wx.Button(self.panel, label="选择")
        self.Bind(wx.EVT_BUTTON,self.file_select,self.button_file)
        self.button_file.SetBackgroundColour('black')
        self.button_file.SetForegroundColour('white')

        #数据源
        data_st = wx.StaticText(self.panel, -1, u"数据源:")
        self.data_t = wx.TextCtrl(self.panel, -1, "", style=wx.TE_READONLY)

        # self.cb_grid = wx.CheckBox(self.panel, -1, "显示网格", style=wx.ALIGN_RIGHT)

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

        sizer4 = wx.FlexGridSizer(cols=7, hgap=5, vgap=5)
        sizer4.AddGrowableCol(5)
        sizer4.Add(sfn_start_st, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        sizer4.Add(self.sfn_start, 0,wx.EXPAND)
        sizer4.Add((20,20))
        sizer4.Add(sfn_total_st, 0,wx.ALIGN_CENTER_VERTICAL)
        sizer4.Add(self.sfn_total, 0,wx.EXPAND)
        sizer4.Add((20,20),wx.EXPAND)
        sizer4.Add(self.refresh, 0,wx.ALIGN_RIGHT)

        sizer5 = wx.StaticBoxSizer(wx.StaticBox(self, wx.NewId(), u'星座图信息'), wx.VERTICAL)
        sizer5.Add(sizer2, 0, wx.EXPAND | wx.ALL, 10)
        sizer5.Add(sizer4, 0, wx.EXPAND | wx.ALL, 10)
        sizer5.Add(sizer3, 0, wx.EXPAND | wx.ALL, 10)

        self.panel.SetSizer(sizer5)
        sizer5.Fit(self)
        sizer5.SetSizeHints(self)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.sizer.Add(wx.StaticLine(self), 0,wx.EXPAND|wx.TOP|wx.BOTTOM,5)
        self.sizer.Add(sizer1, 0, wx.EXPAND)
        self.sizer.Add(wx.StaticLine(self), 0,wx.EXPAND|wx.TOP|wx.BOTTOM,5)
        self.sizer.Add(self.panel,0,wx.EXPAND)
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
            self.process(wx.EVT_BUTTON)
        file_path.Destroy()

    def process(self,event):
        self.fData = open(self.data_t.GetValue(),'rb')
        self.fData.seek(0,2)
        end = self.fData.tell()
        total_sfn = (end-8)/(8064)
        self.sfn.SetValue(str(total_sfn))
        self.fData.seek(0,0)
        x = np.fromfile ( self.fData , dtype = np.int32 , count = 2 )
        self.cell_id = x[0];
        self.prb_count = x[1];
        self.id_cell_t.SetValue(str(x[0]))
        self.bandwidth_t.SetValue(str(x[1]))

        len_sf = self.prb_count*12*14;
        sfn_start = int(self.sfn_start.GetValue())
        N = int(self.sfn_total.GetValue())

        self.dl_subframe_demapper = lte_sat.dl_subframe_demapper(int(self.RNTI.GetValue()))
        self.dl_subframe_demapper.set_cell_id(int(self.cell_id))
        self.dl_subframe_demapper.set_rb_count(int(self.prb_count))

        """ Reconstruct the original complex array """
        self.fData = open(self.data_t.GetValue(),'rb')
        self.fData.seek(sfn_start*len_sf*2*4+8)
        print self.fData.tell()
        y = np.fromfile ( self.fData , dtype = np.complex64 , count = len_sf*N)

        wfc = np.zeros ( [ N*len_sf ] , dtype = np.complex )
        for i in range(len(y)):
            wfc[i] = y[i]

        self.dl_subframe_demapper.demux(wfc, (sfn_start%10))
        self.fData.close();

    def draw_pcfich(self, event):
        self.draw_scatter(0)

    def draw_pdcch(self, event):
        self.draw_scatter(1)

    def draw_pdsch(self, event):
        self.draw_scatter(2)

    def draw_scatter(self, drawtype):
        self.figure.clear() 
        self.axes = self.figure.add_subplot(111)
        self.axes.clear()

        pcfich_data = self.dl_subframe_demapper.get_red(drawtype)

        pcfich_real = []
        pcfich_imag = []
        for i in range(len(pcfich_data)):
            pcfich_real.append(pcfich_data[i].real)
            pcfich_imag.append(pcfich_data[i].imag)

        self.axes.scatter( pcfich_real, pcfich_imag, facecolor='blue' )
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

