import sys
import Adafruit_DHT
import time
from PyQt5.QtWidgets import QWidget,QDialog,QApplication,QMessageBox,QInputDialog,QLineEdit
from PyQt5.QtCore import QTimer,QTime,QThread,QEventLoop
from Project1 import Ui_Form

##class timerThread(QThread):
##    def collectData(self):
##        dataObject=AppWindow()
##        dataObject.getTempHum()
##
##    def __init__(self, *args, **kwargs):
##        QThread.__init__(self, *args, **kwargs)
##        self.dataCollectionTimer = QTimer()
##        self.dataCollectionTimer.moveToThread(self)
##        self.dataCollectionTimer.timeout.connect(self.collectData)
##        self.dataCollectionTimer.start(1000)

class AppWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        global threshold,deg,fah
        deg = 0
        fah = 0
        threshold = 35
        self.show()
##        self.initTimer()
        self.check()
        self.threshold = QLineEdit()
        self.ui.get_hum.clicked.connect(self.getHum)
        self.ui.get_temp.clicked.connect(self.getTemp)
        self.ui.TempAndHumidity.clicked.connect(self.getTempHum)
        self.ui.threshold_button.clicked.connect(self.setThreshold)
        self.ui.degree_button.clicked.connect(self.degTemp)
        self.ui.fahrenheit_button.clicked.connect(self.fahTemp)
        self.ui.refresh.clicked.connect(self.startTimer)
        self.ui.exit.clicked.connect(self.close)

    def startTimer(self):
        self.timer=QTimer()
        self.timer.timeout.connect(self.getTempHum)
        self.timer.start(1000)
##    def start_timer(self):
##        self.timer = timerThread()
##        self.timer.start()
        
  
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
        global threshold,deg,fah
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
            if deg == 1:
                temp = '{0:.2f}'.format(temperature)
                self.ui.temp.display(temp)
                deg = 0
            elif fah == 1:
                temperature = temperature*1.8 + 32
                temp = '{0:.2f}'.format(temperature)
                self.ui.temp.display(temp)
                fah = 0 
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
            if threshold is None:
                pass
            elif temperature > threshold:
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
            
    def degTemp(self):
        global deg
        deg = 1
        self.getTemp()
        
    def fahTemp(self):
        global fah
        fah = 1
        self.getTemp()
            
    def close(self):
        sys.exit(app.exec_())

app = QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())
