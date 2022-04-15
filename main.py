from PyQt5 import QtWidgets , QtGui,QtCore
from PyQt5.QtCore import QThread, pyqtSignal
from appui import Ui_MainWindow
import psutil
import threading
import time
import sys
import platform,socket,re,uuid,json,logging

class MEM(QThread,Ui_MainWindow):
    """
    Runs a ram thread.
    """
    x = pyqtSignal(int)

    def run(self):
        try:
            while True:
                value = psutil.virtual_memory().percent
                self.x.emit(int(value))
                time.sleep(1)

        except:
            self.statusBar.showMessage("Error in getting Ram informations")
class PROC(QThread,Ui_MainWindow):
    """
    Runs a cpu thread.
    """
    y = pyqtSignal(int)

    def run(self):
        try:
            while True:
                value = psutil.cpu_percent()
                self.y.emit(int(value))
                time.sleep(1)
        except:
            self.statusBar.showMessage("Error in getting Cpu informations")     
class DISK(QThread,Ui_MainWindow):
    """
    Runs a disk thread.
    """
    z = pyqtSignal(int)

    def run(self):
        try:
            while True:
                obj_Disk = psutil.disk_usage('/')
                self.z.emit(int(obj_Disk.percent))
                time.sleep(1)            
        except:
            self.statusBar.showMessage("Error in getting disk informations")

#main class
class MyWindow(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.setSysinfo()
        self.StartThread()
        self.actionAbout.triggered.connect(self.about)
        self.actionExit.triggered.connect(self.exit)
        th = threading.Thread(target=self.setStatsInfo)
        th.setDaemon(True)
        th.start()
                   
    
    def setSysinfo(self):
        try:
            self.pltf.setText(self.pltf.text()+" "+platform.system())
            self.pltf_ver.setText(self.pltf_ver.text()+" "+platform.version())
            self.pltf_re.setText(self.pltf_re.text()+" "+platform.release())
            self.ram.setText(self.ram.text()+" "+str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB")
            self.host.setText(self.host.text()+" "+socket.gethostname())
            self.ip.setText(self.ip.text()+" "+socket.gethostbyname(socket.gethostname()))
            self.mac.setText(self.mac.text()+" "+':'.join(re.findall('..', '%012x' % uuid.getnode())))            
            self.cpu.setText(self.cpu.text()+" "+platform.processor())
            self.cpu_cores.setText(self.cpu_cores.text()+" "+str(psutil.cpu_count()))
        except:
            self.statusBar.showMessage("Error in getting System informations")
    def StartThread(self):
        self.ram_obj = MEM()
        self.cpu_obj = PROC() 
        self.disk_obj = DISK()

        self.ram_obj.x.connect(self.setRam)
        self.cpu_obj.y.connect(self.setCpu)
        self.disk_obj.z.connect(self.setDisk)
        self.ram_obj.start()
        self.cpu_obj.start()
        self.disk_obj.start()
    
    def setStatsInfo(self):
        try:
            while True:
                obj_Disk = psutil.disk_usage('/')
                self.ram_info.setText("\nAvailable Memory :"+str(round(psutil.virtual_memory().available/(1024.0**3),2)) + "Go"+"\n\n"+"Used Memory :"+str(round(psutil.virtual_memory().used/(1024.0**3),2)) + "Go")
                self.diskinfo.setText("\ntotal Disk  :"+ str(round(obj_Disk.total / (1024.0 ** 3),2))+"Go\n\nused Disk  :"+str(round(obj_Disk.used / (1024.0 ** 3),2)) + "Go\n\nfree Disk  :"+ str(round(obj_Disk.free / (1024.0 ** 3),2)) + "Go" )
                time.sleep(1)
        except:
            self.statusBar.showMessage("Error in getting additional information about ram and cpu")
    
    def setRam(self, value):
        self.RamProgressBar.setValue(value)
    def setCpu(self, value):
        self.CpuProgressBar.setValue(value)    
    def setDisk(self,value):
        self.DiskProgressBar.setValue(value)
    
    def about(self):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("About")
        msg.setText("SystemMonitor:\nVersion:1.0\nProgrammer:Oussama Ben Sassi")
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.exec_()                                                  

    def exit(self):
        QtWidgets.QApplication.quit() 

app = QtWidgets.QApplication(sys.argv)
win = MyWindow()
sys.exit(app.exec_())        
