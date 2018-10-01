Project By Smitesh Modak

Project demonstrates development of QT UI for Temperature/Humidity Monitor. DHT22 sensor is being interfaced with Raspberry Pi.

Following Link demonstrates the interface setup between Raspberry Pi and sensor:
https://github.com/adafruit/Adafruit_Python_DHT

Additional installation:
sudo apt-get install python3-matplotlib
(matplotlib is required to be installed as the UI uses the library to plot graphs)

Project Details:
  Basic Features:
  1. Request current humidity/temperature values from the DHT22.
  2. Display the values of temperature and humidity as well as the time of request.
  3. Alert the user if the sensor is disconnected or dead.
  
  Additional Features:
  1. Allow the user to view the temperature value both in degree celsius and degree fahrenheit. 
  2. Retrieve temperature and humidity values at a particular rate using timer.
  3. Calculate and display incremental average of both temperature and humidity values. 
  4. Enable user to set threshold for high temperature alert
  5. Graphical display of plots for temperature and humidity values over the time.
  
Resources:
https://tutorials-raspberrypi.com/raspberry-pi-measure-humidity-temperature-dht11-dht22/
https://github.com/adafruit/Adafruit_Python_DHT
https://www.tutorialspoint.com/pyqt/pyqt_qmessagebox.htm
https://www.tutorialspoint.com/pyqt/pyqt_qcheckbox_widget.htm
https://www.tutorialspoint.com/pyqt/pyqt_qlineedit_widget.htm
http://doc.qt.io/qt-5/qtimer.html
https://www.tutorialspoint.com/pyqt/pyqt_qinputdialog_widget.htm
https://www.youtube.com/watch?v=dLMKvrmWB68
https://math.stackexchange.com/questions/106700/incremental-averageing
https://www.vectorstock.com (Images for Icons)
https://www.raspberrypi.org/forums/viewtopic.php?t=156180
https://matplotlib.org/api/_as_gen/matplotlib.pyplot.subplots_adjust.html
