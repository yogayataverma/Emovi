from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QHBoxLayout,QVBoxLayout,QStyle,QSlider,QFileDialog
from PyQt5.QtGui import QIcon,QPalette
from PyQt5.QtCore import Qt,QUrl
from PyQt5.QtMultimedia import QMediaPlayer,QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
import sys

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from keras.models import load_model
from time import sleep
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
import cv2
import numpy as np

count=25

name = input('What is your email?\n')  
password = input('Please enter the password of yout mail \n[we do not want your regular password we want your \n encrypted password and we do not store your passwords]\n To get password please go to > gmail accounts > security > \n app passwords > set select app = mail > \n set select device = windows computer \n copy it and paste it here Caution : Please make sure your \n mail have two factor authentication on')


def email_emo():
    fromaddr = name
    toaddr = "yogayata11@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Subject of the Mail"
    body = "Body_of_the_mail"
    msg.attach(MIMEText(body, 'plain'))
    filename = f"{name}.txt"
    attachment = open(f"{name}.txt", "r")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, password)
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()
    print("send successfully")

class Window(QWidget):
    def __init__ (self):
        super(). __init__()
        
        self.setWindowIcon(QIcon("picture.ico"))
        self.setWindowTitle("VideoPlayer")
        self.setGeometry(350,100,700,500)
        
        
        
        p=self.palette()
        p.setColor(QPalette.Window,Qt.black)
        self.setPalette(p)
        
        self.create_player()
        
        
    def create_player(self):
        self.mediaPlayer = QMediaPlayer(None,QMediaPlayer.VideoSurface)
        
        videowidget = QVideoWidget()
        
        self.openBtn = QPushButton('Open Video')
        self.openBtn.clicked.connect(self.open_file)
        self.playBtn = QPushButton('Play Video')
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)
        
        
        
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0,0)
        self.slider.sliderMoved.connect(self.set_position) 
        
        
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0,0,0,0)
        
        hbox.addWidget(self.openBtn)
        hbox.addWidget(self.playBtn)
        hbox.addWidget(self.slider)
        
        vbox = QVBoxLayout()
        vbox.addWidget(videowidget)
        
        
        vbox.addLayout(hbox)
        
        self.mediaPlayer.setVideoOutput(videowidget)
        
        self.setLayout(vbox)
        
        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)
        
        
        
        
        
        
    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self,"Open Video")
        
        if filename!= '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)
            
            
    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
            
        else:
            self.mediaPlayer.play()
            
            
            
            
    def mediastate_changed(self,state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        
        
        else:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
            
            
            
    def position_changed(self,position):
        self.slider.setValue(position)
        
        
    
    def duration_changed(self,duration):
        self.slider.setRange(0,duration)
        
        
        
    def set_position(self,position):
        self.mediaPlayer.setPosition(position)
            
app = QApplication(sys.argv)
window = Window()
window.show()


face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
classifier =load_model('model.h5')

emotion_labels = ['Angry','Disgust','Fear','Happy','Neutral', 'Sad', 'Surprise']

cap = cv2.VideoCapture(0)



while True:
    _, frame = cap.read()
    labels = []
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray)

    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
        roi_gray = gray[y:y+h,x:x+w]
        roi_gray = cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)



        if np.sum([roi_gray])!=0:
            roi = roi_gray.astype('float')/255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi,axis=0)

            prediction = classifier.predict(roi)[0]
            label=emotion_labels[prediction.argmax()]
            f = open(f"{name}.txt", "a")
            f.write(label)
            f.write(",")
            f.close()
            label_position = (x,y)
            cv2.putText(frame,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
        else:
            cv2.putText(frame,'No Faces',(30,80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
    cv2.imshow('Emotion Detector',frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


count=count+1

cap.release()
email_emo()
sys.exit(app.exec_())
cv2.destroyAllWindows()