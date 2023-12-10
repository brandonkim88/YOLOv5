import cv2
import threading
import sys
import detect
from pathlib import Path
import time

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow


running = False
form_class = uic.loadUiType("Main.ui")[0]
fps_str = "0"      

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory

class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        opt = detect.parse_opt()
        detect.check_requirements(ROOT / 'requirements.txt', exclude=('tensorboard', 'thop'))
        threadDetect = threading.Thread(target=detect.run)
        threadDetect.start()

        self.btn_start.clicked.connect(self.start)
        self.btn_stop.clicked.connect(self.stop)

        app.aboutToQuit.connect(self.onExit)
        self.show()

    def stop(self):
        global running
        running = False
        print("stoped..")


    def start(self):
        global running
        running = True
        th = threading.Thread(target=self.run)
        th.start()
        print("started..")

    def onExit(self):
        print("exit")
        self.stop()


    def run(self):
        #global running
        #cap = cv2.VideoCapture(0)
        #width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        #height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        #self.label_Cam.resize(int(width), int(height))

        a =1;
        while running:
            #ret, img = cap.read()
            img = detect.imgShare

            #save_file = "runs/img/img1_grAA"+ str(a) +"y.PNG"
            #cv2.imwrite(save_file, img)
            
            if img != None:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
                h,w,c = img.shape
                qImg = QtGui.QImage(img.data, w, h, w*c, QtGui.QImage.Format_RGB888)
                pixmap = QtGui.QPixmap.fromImage(qImg)
                self.label_Cam.setPixmap(pixmap)
                
            time.sleep(0.02)
            #a=a+1;
            #else:
            #    QtWidgets.QMessageBox.about(win, "Error", "Cannot read frame.")
            #    print("cannot read frame.")
            #    break

        #cap.release()
        print("Thread end.")

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()

#sys.exit(app.exec_())




