import wx
import random
import wx.lib.imagebrowser    as  ib
import emailclassification as sf
from emailpercentage import run_local
print dir(wx.lib)
class TestPanel(wx.Panel):

    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        b = wx.Button(self, -1, "Select New Test Data For Check", (50, 150))
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)
        self.tc = wx.TextCtrl(self, 1, """
                """, style=wx.TE_READONLY | wx.TE_MULTILINE,size=(430, 450),pos =(350,-1))

        self.tcs = wx.TextCtrl(self, 1, """
                        """, style=wx.TE_READONLY | wx.TE_MULTILINE, size=(200, 150),pos =(50,250))

    def OnButton(self, evt):
        self.tc.Clear()
        wildcard =  "All files (*.*)|*.*"
        # get current working directory
        dir = os.getcwd()

        # set the initial directory for the demo bitmaps
        initial_dir = os.path.join(dir, 'bitmaps')

        # open the image browser dialog
        dlg = ib.wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
            )

        dlg.Centre()

        if dlg.ShowModal() == wx.ID_OK:
            # show the selected file

            file = dlg.GetPaths()
            with open(file[0],'r') as e:
                f = e.read()

            self.tc.WriteText(f)

            #self.log.WriteText("You Selected File: " + f)
            os.chdir(os.path.dirname(os.path.abspath(__file__)))
            print os.path.abspath(__file__)
            spam_dir = ec.init_lists('enron2/ham/')
            ham_dir = ec.init_lists('enron2/spam/')
            total_emails = [(email, 'spam') for email in spam_dir]
            total_emails += [(email, 'ham') for email in ham_dir]
            random.shuffle(total_emails)
            #print ('Corpus size = ' + str(len(total_emails)) + ' emails')
            self.tcs.WriteText('Corpus size = ' + str(len(total_emails)) + ' emails\n')
            all_features = [(sf.get_features(email, ''), label) for (email, label) in total_emails]
            strain_set, test_set, classifier = ec.train(all_features, 1.0)

            # classify your new email
            self.tcs.WriteText(run_local(classifier, "",f ))
        else:
            self.log.WriteText("You pressed Cancel\n")

        dlg.Destroy()



# ---------------------------------------------------------------------------

class MyFrame(wx.Frame):
    def __init__(
            self, parent, ID, title="EMAIL_CLASSIFICATION_SYSTEM", pos=wx.DefaultPosition,
            size=(800,500), style=wx.DEFAULT_FRAME_STYLE
    ):
        wx.Frame.__init__(self, parent, ID, title, pos, size, style)
        self.panel =  TestPanel(self, -1)

        button = wx.Button(self.panel, 1003, "Run Test and Train The Data Test ")
        button.SetPosition((50, 100))
        self.Bind(wx.EVT_BUTTON, self.OnCloseMe, button)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def OnCloseMe(self, event):
        spam_dir = ec.init_lists('enron1/spam/')
        ham_dir = ec.init_lists('enron1/ham/')
        total_emails = [(email, 'spam') for email in spam_dir]
        total_emails += [(email, 'ham') for email in ham_dir]

        random.shuffle(total_emails)
        self.panel.tcs.WriteText('Corpus size = ' + str(len(total_emails)) + ' emails\n')

        all_features = [(ec.get_features(email, ''), label) for (email, label) in total_emails]
        train_set, test_set, classifier = ec.train(all_features, 0.8)

        self.panel.tcs.WriteText(sf.evaluate(train_set, test_set, classifier)+"\n")
        self.Close(True)

    def OnCloseWindow(self, event):
        self.Destroy()


# ---------------------------------------------------------------------------
'''
class iTestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        b = wx.Button(self, -1, "Create and Show a Frame", (50, 50))
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)

    def OnButton(self, evt):
        win = MyFrame(self, -1, "This is a wx.Frame", size=(350, 200),
                      style=wx.DEFAULT_FRAME_STYLE)
        win.Show(True)
'''

# ---------------------------------------------------------------------------
class MyApp(wx.App):
    def OnInit(self):
        frame_1 = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(frame_1)
        frame_1.Show()
        return True


def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win



if __name__ == '__main__':
    import sys, os

    app = MyApp(0)
    app.MainLoop()
