import sys
import Adafruit_DHT
import time
from PyQt5.QtWidgets import QWidget,QDialog,QApplication,QMessageBox,QInputDialog,QLineEdit
from PyQt5.QtCore import QTimer,QTime
from Project1 import Ui_Form


class AppWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.show()
##        self.initTimer()
        self.check()
        
        global threshold
        self.threshold = QLineEdit()
        self.ui.get_hum.clicked.connect(self.getHum)
        self.ui.get_temp.clicked.connect(self.getTemp)
        self.ui.refresh.clicked.connect(self.getTempHum)
        self.ui.threshold_button.clicked.connect(self.setThreshold)
        self.ui.exit.clicked.connect(self.close)

    def initTimer(self):
        self.timer=QTimer()
        self.timer.timeout.connect(self.check)
        self.timer.start(1000)
        
    def check(self):
        hum, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)

        if hum is None or temperature is None:
            alert=QMessageBox()
            alert.setIcon(QMessageBox.Critical)
            alert.setText("Sensor not detected!!!!!")
            alert.exec_()
            self.ui.temp.display("")
            self.ui.hum.display("")
        else:
            pass
##            alert=QMessageBox()
##            alert.autoclose = True
##            alert.timeout = 2
##            alert.setText("Sensor detected!!!!!")
##            alert.exec_()            
        
    def getTemp(self):
        self.check()
        hum, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)
        time=QTime.currentTime().toString()
        self.ui.temp_TOR.display(time)
        
        if hum is None or temperature is None:
            alert=QtGui.QMessageBox()
            alert.setText("Sensor not detected!!!!!")
            alert.exec_()
            self.ui.temp.display("")
        else:
            temp = '{0:.2f}'.format(temperature)
            self.ui.temp.display(temp)
            
    def getHum(self):
        self.check()
        hum, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)
        time=QTime.currentTime().toString()
        self.ui.hum_TOR.display(time)
        
        if hum is None or temperature is None:
            alert=QtGui.QMessageBox()
            alert.setText("Sensor not detected!!!!!")
            alert.exec_()
            self.ui.hum.display("")
        else:
            hum = '{0:.2f}'.format(hum)
            self.ui.hum.display(hum)
        
    def getTempHum(self):
        global threshold
        self.check()
        hum, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)
        time=QTime.currentTime().toString()
        self.ui.temp_TOR.display(time)
        self.ui.hum_TOR.display(time)
        
        if hum is None or temperature is None:
            alert=QtGui.QMessageBox()
            alert.setText("Sensor not detected!!!!!")
            alert.exec_()
            self.ui.temp.display("")
            self.ui.hum.display("")
        else:
            hum = '{0:.2f}'.format(hum)
            self.ui.hum.display(hum)
            temp = '{0:.2f}'.format(temperature)
            self.ui.temp.display(temp)
            #Set an alert for high temperautre
            if temperature > threshold:
                alert=QtGui.QMessageBox()
                alert.setText("High Temperature!!!!!")
                alert.exec_()
            else:
                pass

##        newtime = time.strftime('%m-%d-%y  %H:%M:%S')
        #self.ui.timeDisplay.setText(newtime)
    def setThreshold(self):
        global threshold
        threshold, ok = QInputDialog.getInt(self, 'integer Input Dialog', 'Enter Threshold:')
        if ok:
            self.threshold.setText(str(threshold))
            
    def close(self):
        sys.exit(app.exec_())

app = QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())
