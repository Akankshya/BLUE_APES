import glob
import os
import serial
import sys
import subprocess
import wx
import py2exe

images =[os.path.abspath('open.png'),
            os.path.abspath('burn.png'),
            os.path.abspath('logo.bmp')]
butt=[]


#DialogBox
class SubclassDialog(wx.Dialog):
    def __init__(self):
               wx.Dialog.__init__(self, None, -1, 'Are You Sure?',size=(300, 100))
               okButton = wx.Button(self, wx.ID_OK, "OK", pos=(15, 15))
               okButton.SetDefault()
               cancelButton = wx.Button(self, wx.ID_CANCEL, "Cancel",pos=(115, 15))


class CWAIN(wx.Frame):
    
    def __init__(self,parent,id):


        wx.Frame.__init__(self,parent,id,'AVRDUDE BURNER BY CWAIN MICROSYSTEMS PVT. LTD.',size=(520,440))
        panel=wx.Panel(self,1)
        self.msg = "Either paste file path or OPEN"
        self.setImg(panel)
        self.input_stream=''
        self.Bind(wx.EVT_CLOSE,self.OnClose)
        #print self.partDict
    def OnClose(self,event):
        """dlg = wx.MessageDialog(self, "Do you really want to close this application?","Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:"""
        #subprocess.call('taskkill /f /IM avrdude.exe',shell=True)
        subprocess.call('taskkill /f /IM APES.exe', shell=True)
        subprocess.call('taskkill /f /IM pythonw.exe', shell=True)
        subprocess.call('taskkill /f /IM python.exe', shell=True)
        self.Destroy()
    def setImg(self,panel):
        #Setting up Images

        for i in range(2):
            img1 = wx.Image(images[i],wx.BITMAP_TYPE_ANY)
            w = img1.GetWidth()
            h = img1.GetHeight()
            img2 = img1.Scale(w*.25, h*.25)
            self.bttn=wx.BitmapButton(panel,-1,wx.BitmapFromImage(img2),pos=(20+100*i,10))
            butt.append(self.bttn)

        

        #Button event Handler
        butt[0].Bind(wx.EVT_BUTTON, self.OpenButton, butt[0])
        butt[1].Bind(wx.EVT_BUTTON, self.BurnButton, butt[1])
        #butt[2].Bind(wx.EVT_BUTTON, self.EraseButton, butt[2])
        

        #Setting Logo

        log=wx.Image(images[2],wx.BITMAP_TYPE_ANY)
        w=log.GetWidth()
        h=log.GetHeight()
        logo=log.Scale(log.GetWidth()*.75,log.GetWidth()*.75)
        wx.StaticBitmap(panel,-1,wx.BitmapFromImage(logo),pos=(420,160))


        self.SetBackgroundColour('WHITE')
        custom=wx.StaticText(panel,-1,"COMS: ",(10,100),(0,0),wx.ALIGN_CENTRE)
        custom.SetFont(wx.Font(17,wx.DEFAULT,wx.NORMAL,wx.NORMAL,0, "Norasi"))
        custom.SetForegroundColour('BLACK')


        #different lines

        self.ln = wx.StaticLine(panel,-1, size=(500,4), style=wx.LI_HORIZONTAL,pos=(12,130))
        self.ln = wx.StaticLine(panel,-1, size=(500,5), style=wx.LI_HORIZONTAL,pos=(12,131))
        self.ln = wx.StaticLine(panel,-1, size=(200,4), style=wx.LI_HORIZONTAL,pos=(12,195))
        self.ln = wx.StaticLine(panel,-1, size=(200,5), style=wx.LI_HORIZONTAL,pos=(12,196))
        self.ln = wx.StaticLine(panel,-1, size=(500,4), style=wx.LI_HORIZONTAL,pos=(12,260))
        self.ln = wx.StaticLine(panel,-1, size=(500,5), style=wx.LI_HORIZONTAL,pos=(12,261))


        #Dropdown Menus
        boxes4=wx.StaticText(panel,-1,"Device",(10,135))
        boxes4.SetFont(wx.Font(14,wx.DEFAULT,wx.NORMAL,wx.NORMAL,0, "Roboto"))
        mylist4=self.fileData()
        self.cbo2=wx.ComboBox(panel,-1,"",(10,160))
        self.cbo2.SetItems(mylist4)

        boxes=wx.StaticText(panel,-1,'Com Port:',(10,200))
        boxes.SetFont(wx.Font(14,wx.DEFAULT,wx.NORMAL,wx.NORMAL,0, "Roboto"))
        mylist3=self.serial_ports()
        self.cbo1=wx.ComboBox(panel,-1,"",(10,225))
        self.cbo1.SetItems(mylist3)
        
        #Select hex file

        custom2=wx.StaticText(panel,-1,"HEX: ",(10,265),(0,0),wx.ALIGN_CENTRE)
        custom2.SetFont(wx.Font(17,wx.DEFAULT,wx.NORMAL,wx.NORMAL,0, "Norasi"))
        custom2.SetForegroundColour('BLACK')

        self.label_1=wx.StaticText(panel,-1,"Add link to .hex file",(10,305))
        self.label_1.SetFont(wx.Font(14,wx.DEFAULT,wx.NORMAL,wx.NORMAL,0, "Roboto"))
        self.box=wx.TextCtrl(panel,-1,self.msg,(10,330),size=(300,30))
    

        #Checkboxes
        self.chkbox=[]
        self.chkboxState=[]
        self.txtBox=[]
        for _ in range(3):
            a=wx.CheckBox(panel,-1,"0x",(5+115*_,370),(30,20))
            b=wx.TextCtrl(panel,-1,"",(35+115*_,370),size=(80,20))
            self.chkbox.append(a)
            self.chkboxState.append(False)
            self.txtBox.append(b)
        self.txtBox[0].SetValue("Low Fuse")
        self.txtBox[1].SetValue("High Fuse")
        self.txtBox[2].SetValue("E Fuse")

        self.chkbox[0].Bind(wx.EVT_CHECKBOX, self.OnCb0, self.chkbox[0])
        self.chkbox[1].Bind(wx.EVT_CHECKBOX, self.OnCb1, self.chkbox[1])
        self.chkbox[2].Bind(wx.EVT_CHECKBOX, self.OnCb2, self.chkbox[2])
        self.Show()


        
    def selection(self,event):
        self.Close(True)

    def OpenButton(self,event):
        self.box.SetValue(self.OnOpen(event))
    
    def fileData(self):
        part=open('part_no.txt','r')
        self.partDict={}
        partList=[]
        for x in part:
            #print x
            a,b=x.split()
            partList.append(b)
            self.partDict[b]=a
        part.close()
        partList.sort()
        return tuple(partList)

    def OnCb0(self,event):
        if self.chkbox[0].Get3StateValue()==1:
            self.txtBox[0].Clear()
        else:
            self.txtBox[0].SetValue("Low Fuse")

    def OnCb1(self,event):
        if self.chkbox[1].Get3StateValue()==1:
            self.txtBox[1].Clear()
        else:
            self.txtBox[1].SetValue("High Fuse")

    def OnCb2(self,event):
        if self.chkbox[2].Get3StateValue()==1:
            self.txtBox[2].Clear()
        else:
            self.txtBox[2].SetValue('E Fuse')

    
    def OnOpen(self, event):

        openFileDialog = wx.FileDialog(self, "Open HEX file", "", "",
                                       "HEX files (*.hex)|*.hex", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            wx.MessageBox("Please select a file")
            return self.msg    # the user changed idea...

            # proceed loading the file chosen by the user
            # this can be done with e.g. wxPython input streams:
        self.input_stream = openFileDialog.GetPath()
        if self.input_stream[len(self.input_stream)-3:]=='hex':
            return self.input_stream
        else:
            wx.MessageBox("You have selected wrong or no file. Try again")
            return self.msg
    
    def BurnButton(self,event):
        #self.x=subprocess.check_output(""+self.input_stream, shell=True)
        #print(self.x)

        partName=self.cbo2.GetValue()
        if partName=='':
            wx.MessageBox("Please Select Device")
            return
        else:
            partNo=self.partDict[partName]
        comPort=self.cbo1.GetValue()
        fuseD={0:' -U l',1:' -U h',2:' -U e',3:''}
        fuse=[]
        for _ in range(2):
            fuse.append(self.getVal(_))
            if fuse[_]!='':
                fuse[_]=fuseD[_]+fuse[_]

        command = 'avrdude -p '+ partNo + ' -c avrisp -P '+ comPort + ' -b 19200 -U flash:w:'+self.box.GetValue()+':i';
        x=self.box.GetValue()
        for a in fuse:
            command+=a
        

        #PROGRESS BAR
        if partNo=='':
            wx.MessageBox("Please select Device")
            return
        elif comPort=='':
            wx.MessageBox("Specify/Select COM Port")
            return
        elif x[len(x)-3:]!='hex':
            wx.MessageBox("Please Select HEX File")
            return
        wx.MessageBox("Part no. is: "+partNo+"\nCOM Port: "+comPort)
        dialog = SubclassDialog()
        result = dialog.ShowModal()
        if result == wx.ID_OK:
            print command
            #x=subprocess.check_output(command,shell=True)
            #subprocess.call(command,shell=True)
            if subprocess.check_call(command,shell=True)==0:
                wx.MessageBox("Process successfully completed")
            else:
                wx.MessageBox("Process failed")
            #print x
        else:
            dialog.Destroy()
        
    
    def getVal(self,i):
        if self.chkbox[i].GetValue():
            low=self.txtBox[i].GetValue()
            low='fuse:w:0x'+low+':m'
        else:
            low=''

        return low
        

    def serial_ports(self):
    
        if sys.platform.startswith('win'):
            ports = ['COM' + str(i + 1) for i in range(256)]

        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this is to exclude your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')

        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')

        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

if __name__=='__main__':
    app=wx.PySimpleApp()
    frame=CWAIN(parent=None,id=-1)
    frame.Show()
    app.MainLoop()
