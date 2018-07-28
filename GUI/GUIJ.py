import wx.lib.scrolledpanel as scrolled
import wx
from Sorting.InsertionSort import *
from PIL import *
from random import *
from os import *


class ImageDisplayer(wx.Panel):
    def __init__(self, parent, path=None):
        super(ImageDisplayer, self).__init__(parent, -1)
        self.control = None
        if path is not None:
            self.set_image(path)

    @staticmethod
    def static_bitmap_from_pil_image(caller, pil_image):
        wx_image = wx.EmptyImage(pil_image.size[0], pil_image.size[1])
        wx_image.SetData(pil_image.convert("RGB").tobytes())
        wx_image.SetAlpha(pil_image.convert("RGBA").tobytes()[3::4])
        bitmap = wx.BitmapFromImage(wx_image)
        static_bitmap = wx.StaticBitmap(caller, wx.ID_ANY, wx.NullBitmap)
        static_bitmap.SetBitmap(bitmap)
        return static_bitmap

    def set_image(self, img):
        # bitmap = wx.Bitmap(path)
        static_bitmap = self.static_bitmap_from_pil_image(self, img)
        if self.control is not None:
            self.control.Destroy()
        self.Refresh()
        self.control = static_bitmap # wx.StaticBitmap(self, -1, bitmap)
        self.control.SetPosition((10, 10))


class ScrolledImage(scrolled.ScrolledPanel):
    def __init__(self, parent):
        scrolled.ScrolledPanel.__init__(self, parent, -1)

        self.displayer = ImageDisplayer(self)

        sizer_v = wx.BoxSizer(wx.VERTICAL)
        sizer_h = wx.BoxSizer(wx.HORIZONTAL)
        sizer_v.Add(self.displayer, 1, wx.ALIGN_CENTER_HORIZONTAL)
        sizer_h.Add(sizer_v, 1, wx.CENTER)
        self.SetSizer(sizer_h)

        self.SetupScrolling()


class MainPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)

        self.imagePanel = ScrolledImage(self)
        self.set_image = self.imagePanel.displayer.set_image
        self.promptPanel = wx.Panel(self)
        self.buttonsPanel = wx.Panel(self)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        main_sizer.Add(self.imagePanel, 8, wx.EXPAND, border=20)
        main_sizer.Add(self.promptPanel, 1, wx.CENTER, border=20)
        main_sizer.Add(self.buttonsPanel, 1, wx.EXPAND, border=20)

        self.prompt = wx.StaticText(self.promptPanel)
        self.prompt.SetLabelText("")
        self.prompt.SetFont(wx.Font(36, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.promptPanel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.promptPanel_sizer.Add(self.prompt, 1, wx.TOP)
        self.promptPanel.SetSizer(self.promptPanel_sizer)

        self.SetSizer(main_sizer)

        self.backBtn = wx.Button(self.buttonsPanel, label='<<BACK', style=wx.BU_EXACTFIT, size=(50, 30))
        self.backBtn.Bind(wx.EVT_BUTTON, self.backBtnClicked)

        self.exitBtn = wx.Button(self.buttonsPanel, label='EXIT', style=wx.BU_EXACTFIT, size=(50, 30))
        self.exitBtn.Bind(wx.EVT_BUTTON, self.exitBtnClicked)

        self.nextBtn = wx.Button(self.buttonsPanel, label='NEXT>>', style=wx.BU_EXACTFIT, size=(50, 30))
        self.nextBtn.Bind(wx.EVT_BUTTON, self.nextBtnClicked)

        self.selection = wx.ComboBox(self.buttonsPanel, style=wx.BU_EXACTFIT|wx.CB_DROPDOWN,
                                     choices=["Insertion Sort", "Key Sort"])
        self.selection.SetValue("")

        self.buttonsPanel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.buttonsPanel_sizer.Add(self.backBtn, 1, wx.CENTER|wx.LEFT|wx.RIGHT, border=20)
        self.buttonsPanel_sizer.Add(self.exitBtn, 1, wx.CENTER|wx.LEFT|wx.RIGHT, border=20)
        self.buttonsPanel_sizer.Add(self.nextBtn, 1, wx.CENTER|wx.LEFT|wx.RIGHT, border=20)
        self.buttonsPanel_sizer.Add(self.selection, 1, wx.CENTER | wx.LEFT | wx.RIGHT, border=20)
        self.buttonsPanel.SetSizer(self.buttonsPanel_sizer)

        main_sizer.Fit(self)

        self.promptPanel.Bind(wx.EVT_KEY_DOWN, self.KeyDown)
        self.imagePanel.Bind(wx.EVT_KEY_DOWN, self.KeyDown)
        self.buttonsPanel.Bind(wx.EVT_KEY_DOWN, self.KeyDown)
        self.selection.Bind(wx.EVT_COMBOBOX, self.launch_algorithm)

        self.inS = None

    def set_text(self, text):
        self.prompt.SetLabelText(text)

    def launch_algorithm(self, event):
        self.set_text("Wait")
        if self.selection.GetSelection() == 0:
            a = [None] * 5
            for i in range(0, 5):
                a[i] = randint(0, 200)
            self.inS = InsertionSort(a)
            self.inS.register(self.show_diagram)
            self.inS.launch()

    def show_diagram(self, diagram):
        print "SHOWING DIAGRAM"
        self.set_text("Nothing")
        self.set_image(diagram)
        self.Layout()

    def backBtnClicked(self, event):
        print("Back Button")

    def nextBtnClicked(self, event):
        self.inS.resume()

    def exitBtnClicked(self, event):
        print("Exit Button")

    def KeyDown(self, event=None):
        assert isinstance(event, wx.KeyEvent)
        if event.GetKeyCode() == 13:
            self.nextBtnClicked(None)


class MainWindow(wx.Frame):
    def __init__(self, parent, id, title="My GUI"):
        wx.Frame.__init__(self, parent, wx.ID_ANY, title="Algorithm Demostration", size=(800, 600))
        self.panel = MainPanel(self)
        self.panel.buttonsPanel.SetFocus()
        self.Show(True)


if __name__ == '__main__':
    app = wx.App(False)
    app.frame = MainWindow(None, wx.ID_ANY)
    app.frame.Show()

    app.MainLoop()
