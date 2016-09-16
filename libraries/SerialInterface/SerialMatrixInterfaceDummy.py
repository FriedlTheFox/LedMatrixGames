'''
Created on 28.08.2016

@author: Max
'''
import wx


class InputApp():
    def __init__(self, parent):
        self.parent = parent
        frame = wx.Frame(None)
        self.panel = wx.Panel(frame)
        self.panel.Bind(wx.EVT_KEY_DOWN, self.parent.KeyHandler)

 #==================================================================================================
 #        topSz = wx.BoxSizer(wx.HORIZONTAL)
 #        upBtn = wx.Button(self.panel)
 #        topSz.Add(upBtn, wx.ALIGN_CENTER)
 # 
 #        midSz = wx.BoxSizer(wx.HORIZONTAL)
 #        lfBtn = wx.Button(self.panel)
 #        rtBtn = wx.Button(self.panel)
 #        midSz.Add(lfBtn)
 #        midSz.Add(rtBtn)
 # 
 #        lowSz = wx.BoxSizer(wx.HORIZONTAL)
 #        dnBtn = wx.Button(self.panel)
 #        lowSz.Add(dnBtn)
 # 
 #        sizer = wx.BoxSizer(wx.VERTICAL)
 #        sizer.Add(topSz)
 #        sizer.Add(midSz)
 #        sizer.Add(lowSz)
 #        self.panel.SetSizerAndFit(sizer)
 #==================================================================================================
        frame.Show()


class SerialMatrixInterface():
    def __init__(self, port, parent, *args, **kwargs):
        frame = wx.Frame(None)
        frame.SetClientSize((320, 320))
        frame.Bind(wx.EVT_CLOSE, self.OnClose)
        self.w = 8
        self.h = 8
        self.parent = parent

        self.__matrix = []

        for x in range(self.w):
            self.__matrix.append([])
            for y in range(self.h):
                self.__matrix[x].append([0, 0, 0])

        self.panel = wx.Panel(frame)
        self.panel.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.timer = wx.Timer(self.panel)

        self.panel.Bind(wx.EVT_SIZE, self.OnSize)
        self.panel.Bind(wx.EVT_PAINT, self.OnPaint)
        self.panel.Bind(wx.EVT_TIMER, self.OnRefresh, self.timer)

        self.timer.Start(10)
        frame.Show()

    def OnClose(self, evt):
        self.timer.Stop()
        evt.Skip()

    def OnRefresh(self, evt):
        self.panel.Refresh()
        evt.Skip()

    def OnSize(self, evt):
        self.panel.Refresh()

    def OnPaint(self, evt):
        w, h = self.panel.GetClientSize()
        dc = wx.AutoBufferedPaintDC(self.panel)
        dc.Clear()
        dc.SetBrush(wx.BLACK_BRUSH)
        dc.DrawRectangle(0, 0, w, h)
        dc.SetPen(wx.Pen(wx.Colour(50, 50, 50)))
        for x, col in enumerate(self.__matrix):
            for y, row in enumerate(col):
                dc.SetBrush(wx.Brush(wx.Colour(row[0], row[1], row[2])))
                dc.DrawCircle(x * 40 + 20, y * 40 + 20, 18)

    def setPixel(self, x, y, r, g, b):
        self.__matrix[x][y] = [r, g, b]