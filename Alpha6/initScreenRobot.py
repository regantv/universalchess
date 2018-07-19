import os, sys, urx
from win32api import GetSystemMetrics
from PyQt5.QtWidgets import QWidget, QSlider, QAction, QApplication, QLabel, QInputDialog, QCheckBox, QDialog, QComboBox, QLineEdit, QListWidget
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.Qt import QTextEdit, QVBoxLayout, QPushButton, QHBoxLayout, pyqtSlot
from PyQt5.QtCore import Qt
from urx.ursecmon import TimeoutException
import cv2


class InitScreenRobot(QDialog):
    def __init__(self,robot):
        super().__init__()
        
#         try:
#             while True:
#                 done = self.connect2Robot()
#                 if type(done)!='None':
#                     break
#         except TimeoutException:
#             pass        
    
        self.robot = robot    
        print("robot", self.robot)    
        self.initUI()
        
    
    
    def connect2Robot(self):
        self.robot = urx.Robot("192.168.0.20", use_rt=True)
        return(self.robot)
    
#Check height and width system metric, form always stay on center    
    def settingScreen(self, width, height):
        self.setFixedSize(width, height)
        self.move(GetSystemMetrics(0)/2-width/2, GetSystemMetrics(1)/2-height/2)
    
    def click_and_crop(self,event, x, y, flags, param,):
        
        temp =self.image.copy()
    
    #refPt=[(69, 118), (309, 342)]
        if event == cv2.EVENT_LBUTTONDOWN:
            self.refPt = [(x, y)]
            self.cropping = True

            
 
    # check to see if the left mouse button was released
        elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
            self.refPt.append((x, y))
            self.cropping = False
 
        # draw a rectangle around the region of interest
            cv2.rectangle(self.image, self.refPt[0], self.refPt[1], (0, 255, 0), 2)
            cv2.imshow("image", self.image)
            roi = temp[self.refPt[0][1]:self.refPt[1][1], self.refPt[0][0]:self.refPt[1][0]]
            cv2.imshow("Selected Roi", roi)
            cv2.waitKey(0)
            #print(self.refPt)
            self.status =True
    
    def Roi(self,param):
        
        self.status =False
        self.refPt =[]
        self.cropping = True
        cam =cv2.VideoCapture(self.camId)
        while True:
            ret, self.image = cam.read()
            img = self.image.copy()
            w,h,z = img.shape
            cv2.line(img,(0,int(w/2)),(h,int(w/2)),(255,0,0),2)
            cv2.line(img,(int(h/2),0),(int(h/2),w),(255,0,0),2)
            cv2.imshow('Correct camera pose',img)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("c"):
                #self.pl
                break
        #self.image = cv2.resize(self.image,(450,450))
        clone = self.image.copy()

        cv2.namedWindow("image")
        cv2.setMouseCallback("image", self.click_and_crop)
        
        cv2.imshow('image',self.image)
        cv2.waitKey(0)
        
        
        if len(self.refPt)==2:
            #print('refPt',self.refPt)
            refPt = self.refPt
            roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
            w,h,z = roi.shape
            cv2.line(roi,(0,int(w/2)),(w,int(w/2)),(255,0,0),5)
            cv2.line(roi,(int(h/2),0),(int(h/2),h),(255,0,0),5)
            roi = cv2.resize(roi,(264,264))
            cv2.imwrite('images/tmpRoi'+ str(self.roiPlayer) +'.png',roi)
            if param ==1:
                self.roi.setPixmap(QPixmap("images/tmpRoi"+ str(self.roiPlayer) +".png"))
            
                if self.roiPlayer == 1:
                    self.playerOneRfPt = self.refPt
                    self.playerOneChessboard = self.robot.getj()
                elif self.roiPlayer == 2:
                    self.playerTwoRfPt = self.refPt
                    self.playerTwoChessboard = self.robot.getj()
                elif self.roiPlayer == 3:
                    self.playerThreeRfPt = self.refPt
                    self.playerThreeChessboard = self.robot.getj()
                
                self.coordinates = self.robot.getl()
                self.eventText.append("Player " + str(self.roiPlayer) + "\n")
                self.eventText.append("Set X: "+ str(self.coordinates[0]) + " \nSet Y: " + str(self.coordinates[1]) + " \nSet Z: " + str(self.coordinates[2])+"\n")
                self.eventText.append('images/tmpRoi'+ str(self.roiPlayer) +'.png saved\n')
            
                self.doneBtn.setEnabled(True)
                self.backBtn.setEnabled(True)
            elif param ==2:
                if self.roiPlayer ==1:
                    cv2.imwrite('images/cb1'+ str(self.roiPlayer) +'.bmp',roi)
                if self.roiPlayer ==2:
                    cv2.imwrite('images/cb2'+ str(self.roiPlayer) +'.bmp',roi)
                if self.roiPlayer ==3:
                    cv2.imwrite('images/cb3'+ str(self.roiPlayer) +'.bmp',roi)
#Action for back button, just checking stage    
    def BackStage(self):
        if self.stage == 1:
            width=224
            height=256
            
            self.settingScreen(width, height)
            
            self.backBtn.hide()
            self.doneBtn.hide()
            self.eventText.hide()
            self.eventPicture.hide()
            
            self.labelHint.show()
            self.startBtn.show()
            self.countPlayer.show()
            
        else: 
            self.stage-=2
            self.doneBtn.setText("Next")
            self.NextStage()
            
    #Step for setting robot        
    def NextStage(self):
        self.stage+=1
        if self.stage==1:
            self.eventText.append("Board 1, Step 1: Set the robot to allow the camera to cover the entire chessboard\n")
            self.eventPicture.hide()
            self.instructionPicture.hide()
            self.roi.clear()
            self.roi.show()
            self.roiPlayer = 1
            self.doneBtn.setEnabled(False)
            self.backBtn.setEnabled(False)
            self.Roi(1)
            
        if self.stage==2:
            #self.eventText.clear()
            self.eventText.append("Board 1, Step 2: Install the robot in the indicated position, which is marked in the picture on the right\n")
            self.eventPicture.show()
            self.instructionPicture.show()
            self.roi.hide()
            self.eventPicture.move(256+26*10,16+26)
            
        elif self.stage==3:
            #self.eventText.clear()
            self.coordinates = self.robot.getl()
            self.eventText.append("Set X: "+ str(self.coordinates[0]) + " \nSet Y: " + str(self.coordinates[1]) + " \nSet Z: " + str(self.coordinates[2])+"\n")
            self.eventText.append("Board 1, Step 3: Install the robot in the indicated position, which is marked in the picture on the right\n") 
            self.eventPicture.show()
            self.eventPicture.move(256+26*2,16+26*8)
            
            self.playerOneJPose = self.robot.getj()
            self.playerOneLPose = self.robot.getl()
            
        # elif self.stage==4:
        #     #self.eventText.clear()
        #     self.coordinates = self.robot.getl()
        #     self.eventText.append("Set X: "+ str(self.coordinates[0]) + " \nSet Y: " + str(self.coordinates[1]) + " \nSet Z: " + str(self.coordinates[2])+"\n")
        #     self.eventText.append("Board 1, Step 4: Install the robot in the indicated position, which is marked in the picture on the right\n")  
        #     self.eventPicture.show()
        #     self.eventPicture.move(256+26*11,16+26*8)
            
        #     self.playerOneJleftLimit = self.robot.getj()
            
        # elif self.stage==5:
        #     #self.eventText.clear()
        #     self.coordinates = self.robot.getl()
        #     self.eventText.append("Set X: "+ str(self.coordinates[0]) + " \nSet Y: " + str(self.coordinates[1]) + " \nSet Z: " + str(self.coordinates[2])+"\n")
        #     self.eventText.append("Board 1, Step 5: Install the robot in the indicated position, which is marked in the picture on the right\n")  
        #     self.eventPicture.show()
        #     self.eventPicture.move(256,16+26*8)
            
        #     self.playerOneJrightLimit = self.robot.getj()
        elif self.stage==4:
            #self.eventText.clear()
            self.coordinates = self.robot.getl()
            self.eventText.append("Set X: " + str(self.coordinates[0]) + " \nSet Y: " + str(self.coordinates[1]) + " \nSet Z: " + str(self.coordinates[2])+"\n")
            self.eventText.append("Board 1, Step 4: Install the robot in the indicated position, which is marked in the picture on the right\n")  
            self.eventPicture.show()
            self.instructionPicture.show()
            self.roi.hide()
            self.eventPicture.move(256+26*13,16+26*8)
            
            self.playerOneDropBlack = self.robot.getl()
        elif self.stage==5:
            self.playerOneDropWhite = self.robot.getl()
            
            if self.cntPlayer == 1:
                #self.eventText.clear()   
                self.coordinates = self.robot.getl()
                self.eventText.append("Set X: "+ str(self.coordinates[0]) + " \nSet Y: " + str(self.coordinates[1]) + " \nSet Z: " + str(self.coordinates[2])+"\n")
                self.eventText.setText("Good work, press to done")
                self.eventPicture.hide() 
                self.doneBtn.setText("DONE")
            else:
                #self.eventText.clear()
                self.coordinates = self.robot.getl()
                self.roiPlayer = 2
                self.eventText.append("Set X: "+ str(self.coordinates[0]) + " \nSet Y: " + str(self.coordinates[1]) + " \nSet Z: " + str(self.coordinates[2])+"\n")
                self.eventText.append("Board 2, Step 5: Set the robot to allow the camera to cover the entire chessboard\n")  
                self.eventPicture.hide()
                self.instructionPicture.hide()
                self.roi.clear()
                self.roi.show()
                self.doneBtn.setEnabled(False)
                self.backBtn.setEnabled(False)
                self.Roi(1)
        elif self.stage==6:
            if self.cntPlayer == 1:
                self.WriteDataStructers()
                self.close()
            else:
                self.eventText.append("Player " + str(self.roiPlayer) + "\n")
                self.eventText.append("Set X: "+ str(self.coordinates[0]) + " \nSet Y: " + str(self.coordinates[1]) + " \nSet Z: " + str(self.coordinates[2])+"\n")
                self.eventText.append("Board 2, Step 6: Install the robot in the indicated position, which is marked in the picture on the right\n")  
                self.eventPicture.show()
                self.instructionPicture.show()
                self.roi.hide()
                self.eventPicture.move(256+26*10,16+26)
        elif self.stage==7:
                #self.eventText.clear()
                self.coordinates = self.robot.getl()
                self.eventText.append("Set X: "+ str(self.coordinates[0]) + " \nSet Y: " + str(self.coordinates[1]) + " \nSet Z: " + str(self.coordinates[2])+"\n")
                self.eventText.append("Board 2, Step 7: Install the robot in the indicated position, which is marked in the picture on the right\n")  
                self.eventPicture.show()
                
                self.playerTwoJPose = self.robot.getj()
                self.playerTwoLPose = self.robot.getl()
                
                self.eventPicture.move(256+26*2,16+26*8)
        # elif self.stage==8:
        #     #self.eventText.clear()
        #     self.coordinates = self.robot.getl()
        #     self.eventText.append("Set X: "+ str(self.coordinates[0]) + " \nSet Y: " + str(self.coordinates[1]) + " \nSet Z: " + str(self.coordinates[2])+"\n")
        #     self.eventText.append("Board 2, Step 8: Install the robot in the indicated position, which is marked in the picture on the right\n")  
        #     self.eventPicture.show()
            
        #     self.playerTwoJleftLimit = self.robot.getj()
            
        #     self.eventPicture.move(256+26*11,16+26*8)
        # elif self.stage==9:
        #     #self.eventText.clear()
        #     self.coordinates = self.robot.getl()
        #     self.eventText.append("Set X: "+ str(self.coordinates[0]) + " \nSet Y: " + str(self.coordinates[1]) + " \nSet Z: " + str(self.coordinates[2])+"\n")
        #     self.eventText.append("Board 2, Step 11: Install the robot in the indicated position, which is marked in the picture on the right\n")  
        #     self.eventPicture.show()
            
        #     self.playerTwoJrightLimit = self.robot.getj()
            
        #     self.eventPicture.move(256,16+26*8)
        elif self.stage==8:
            #self.eventText.clear()
            self.coordinates = self.robot.getl()
            self.eventText.append("Set X: "+ str(self.coordinates[0]) + " \nSet Y: " + str(self.coordinates[1]) + " \nSet Z: " + str(self.coordinates[2])+"\n")
            self.eventText.append("Board 2, Step 8: Install the robot in the indicated position, which is marked in the picture on the right\n")  
            self.eventPicture.show()
            self.instructionPicture.show()
            self.roi.hide()
            
            self.playerTwoDropBlack = self.robot.getl()
            
            self.eventPicture.move(256+26*13,16+26*8)
        elif self.stage==9:
            self.playerTwoDropWhite = self.robot.getl() 
            
            if self.cntPlayer == 2:
                #self.eventText.clear() 
                 
                self.coordinates = self.robot.getl()
                self.eventText.append("Set X: "+ str(self.coordinates[0]) + " \nSet Y: " + str(self.coordinates[1]) + " \nSet Z: " + str(self.coordinates[2])+"\n")
                self.eventText.setText("Good work, press to done")
                self.eventPicture.hide() 
                self.doneBtn.setText("DONE")
            else:
                #self.eventText.clear()
                self.coordinates = self.robot.getl()
                self.roiPlayer = 3
                self.eventText.append("Set X: "+ str(self.coordinates[0]) + " \nSet Y: " + str(self.coordinates[1]) + " \nSet Z: " + str(self.coordinates[2])+"\n")
                self.eventText.append("Board 3, Step 9: Set the robot to allow the camera to cover the entire chessboard\n")  
                self.eventPicture.hide()
                self.instructionPicture.hide()
                self.roi.clear()
                self.roi.show()
                self.doneBtn.setEnabled(False)
                self.backBtn.setEnabled(False)
                self.Roi(1)
        elif self.stage==10:
            if self.cntPlayer == 2:
                self.WriteDataStructers()
                self.close()
            else:
                self.coordinates = self.robot.getl()
                self.eventText.append("Set X: "+ str(self.coordinates[0]) + " \nSet Y: " + str(self.coordinates[1]) + " \nSet Z: " + str(self.coordinates[2])+"\n")
                self.eventText.append("Board 3, Step 10: Install the robot in the indicated position, which is marked in the picture on the right\n")  
                self.eventPicture.show()
                self.instructionPicture.show()
                self.roi.hide()
                self.eventPicture.move(256+26*10,16+26)
        elif self.stage==11:
            
                #self.eventText.clear()
                self.coordinates = self.robot.getl()
                self.eventText.append("Set X: "+ str(self.coordinates[0]) + " \nSet Y: " + str(self.coordinates[1]) + " \nSet Z: " + str(self.coordinates[2])+"\n")
                self.eventText.append("Board 3, Step 11: Install the robot in the indicated position, which is marked in the picture on the right\n")  
                self.eventPicture.show()
                
                self.playerThreeJPose = self.robot.getj()
                self.playerThreeLPose = self.robot.getl()
                
                self.eventPicture.move(256+26*2,16+26*8)
        # elif self.stage==12:
        #     #self.eventText.clear()
        #     self.coordinates = self.robot.getl()
        #     self.eventText.append("Set X: "+ str(self.coordinates[0]) + " \nSet Y: " + str(self.coordinates[1]) + " \nSet Z: " + str(self.coordinates[2])+"\n")
        #     self.eventText.append("Board 3, Step 16: Install the robot in the indicated position, which is marked in the picture on the right\n")  
        #     self.eventPicture.show()
            
        #     self.playerThreeJleftLimit = self.robot.getj()
            
        #     self.eventPicture.move(256+26*11,16+26*8)
        # elif self.stage==13:
        #     #self.eventText.clear()
        #     self.coordinates = self.robot.getl()
        #     self.eventText.append("Set X: "+ str(self.coordinates[0]) + " \nSet Y: " + str(self.coordinates[1]) + " \nSet Z: " + str(self.coordinates[2])+"\n")
        #     self.eventText.append("Board 3, Step 17: Install the robot in the indicated position, which is marked in the picture on the right\n")  
        #     self.eventPicture.show()
            
        #     self.playerThreeJrightLimit = self.robot.getj()
            
        #     self.eventPicture.move(256,16+26*8)
        elif self.stage==12:
            #self.eventText.clear()
            self.coordinates = self.robot.getl()
            self.eventText.append("Set X: "+ str(self.coordinates[0]) + " \nSet Y: " + str(self.coordinates[1]) + " \nSet Z: " + str(self.coordinates[2])+"\n")
            self.eventText.append("Board 3, Step 12: Install the robot in the indicated position, which is marked in the picture on the right\n")  
            self.eventPicture.show()
            
            self.playerThreeDropBlack = self.robot.getl()
            
            self.eventPicture.move(256+26*13,16+26*8)
        elif self.stage==13:
            #self.eventText.clear()   
            self.coordinates = self.robot.getl()
            self.eventText.append("Set X: "+ str(self.coordinates[0]) + " \nSet Y: " + str(self.coordinates[1]) + " \nSet Z: " + str(self.coordinates[2])+"\n")
            self.eventText.setText("Good work, press to done")
            self.eventPicture.hide()
            
            self.playerThreeDropWhite = self.robot.getl()
             
            self.doneBtn.setText("DONE")
        elif self.stage==14:
            
            self.WriteDataStructers()
            self.close() 
    
    #Writing in dataStructers.py    
    def WriteDataStructers(self):
        #Basic info Structers files
        self.file = open("dataStructers.py", "a")
        
        if self.cntPlayer == 1:
            self.file.write("playerOneRfPt = " + str(self.playerOneRfPt) + "\n")
            self.file.write("playerTwoRfPt = " + str(self.playerOneRfPt) + "\n")
            self.file.write("playerThreeRfPt = " + str(self.playerOneRfPt) + "\n")
        if self.cntPlayer == 2:
            self.file.write("playerOneRfPt = " + str(self.playerOneRfPt) + "\n")
            self.file.write("playerTwoRfPt = " + str(self.playerTwoRfPt) + "\n")
            self.file.write("playerThreeRfPt = " + str(self.playerTwoRfPt) + "\n")
        if self.cntPlayer == 3:
            self.file.write("playerOneRfPt = " + str(self.playerOneRfPt) + "\n")
            self.file.write("playerTwoRfPt = " + str(self.playerTwoRfPt) + "\n")
            self.file.write("playerThreeRfPt = " + str(self.playerThreeRfPt) + "\n")
        
        self.file.write("\n")
        
        if self.cntPlayer == 1:
            self.file.write("playerOneCamChessboard = " + str(self.playerOneChessboard) + "\n")
            self.file.write("playerTwoCamChessboard = " + str(self.playerOneChessboard) + "\n")
            self.file.write("playerThreeCamChessboard = " + str(self.playerOneChessboard) + "\n")
        if self.cntPlayer == 2:
            self.file.write("playerOneCamChessboard = " + str(self.playerOneChessboard) + "\n")
            self.file.write("playerTwoCamChessboard = " + str(self.playerTwoChessboard) + "\n")
            self.file.write("playerThreeCamChessboard = " + str(self.playerTwoChessboard) + "\n")
        if self.roiPlayer == 3:
            self.file.write("playerOneCamChessboard = " + str(self.playerOneChessboard) + "\n")
            self.file.write("playerTwoCamChessboard = " + str(self.playerTwoChessboard) + "\n")
            self.file.write("playerThreeCamChessboard = " + str(self.playerThreeChessboard) + "\n")
        self.file.write("\n")
        
        if self.cntPlayer == 1:
            self.file.write("figuresDropOneWhite = " + str(self.playerOneDropWhite) + "\n")
            self.file.write("figuresDropOneBlack = " + str(self.playerOneDropBlack) + "\n")
            self.file.write("playerOneJPose = " + str(self.playerOneJPose) + "\n")
            self.file.write("playerOneLPose = " + str(self.playerOneLPose) + "\n")
            #self.file.write("playerOneJleftLimit = " + str(self.playerOneJleftLimit[0]) + "\n")
            #self.file.write("playerOneJrightLimit = " + str(self.playerOneJrightLimit[0]) + "\n\n")
            
            self.file.write("figuresDropTwoWhite = " + str(self.playerOneDropWhite) + "\n")
            self.file.write("figuresDropTwoBlack = " + str(self.playerOneDropBlack) + "\n")
            self.file.write("playerTwoJPose = " + str(self.playerOneJPose) + "\n")
            self.file.write("playerTwoLPose = " + str(self.playerOneLPose) + "\n")
            #self.file.write("playerTwoJleftLimit = " + str(self.playerOneJleftLimit[0]) + "\n")
            #self.file.write("playerTwoJrightLimit = " + str(self.playerOneJrightLimit[0]) + "\n\n")
            
            self.file.write("figuresDropThreeWhite = " + str(self.playerOneDropWhite) + "\n")
            self.file.write("figuresDropThreeBlack = " + str(self.playerOneDropBlack) + "\n")
            self.file.write("playerThreeJPose = " + str(self.playerOneJPose) + "\n")
            self.file.write("playerThreeLPose = " + str(self.playerOneLPose) + "\n")
            #self.file.write("playerThreeJleftLimit = " + str(self.playerOneJleftLimit[0]) + "\n")
            #self.file.write("playerThreeJrightLimit = " + str(self.playerOneJrightLimit[0]) + "\n\n")
        
        #Write if count players more than 1
        elif self.cntPlayer == 2:
            self.file.write("figuresDropOneWhite = " + str(self.playerOneDropWhite) + "\n")
            self.file.write("figuresDropOneBlack = " + str(self.playerOneDropBlack) + "\n")
            self.file.write("playerOneJPose = " + str(self.playerOneJPose) + "\n")
            self.file.write("playerOneLPose = " + str(self.playerOneLPose) + "\n")
            #self.file.write("playerOneJleftLimit = " + str(self.playerOneJleftLimit[0]) + "\n")
            #self.file.write("playerOneJrightLimit = " + str(self.playerOneJrightLimit[0]) + "\n\n")
            
            self.file.write("figuresDropTwoWhite = " + str(self.playerTwoDropWhite) + "\n")
            self.file.write("figuresDropTwoBlack = " + str(self.playerTwoDropBlack) + "\n")
            self.file.write("playerTwoJPose = " + str(self.playerTwoJPose) + "\n")
            self.file.write("playerTwoLPose = " + str(self.playerTwoLPose) + "\n")
            #self.file.write("playerTwoJleftLimit = " + str(self.playerTwoJleftLimit[0]) + "\n")
            #self.file.write("playerTwoJrightLimit = " + str(self.playerTwoJrightLimit[0]) + "\n\n")
            
            self.file.write("figuresDropThreeWhite = " + str(self.playerTwoDropWhite) + "\n")
            self.file.write("figuresDropThreeBlack = " + str(self.playerTwoDropBlack) + "\n")
            self.file.write("playerThreeJPose = " + str(self.playerTwoJPose) + "\n")
            self.file.write("playerThreeLPose = " + str(self.playerTwoLPose) + "\n")
            #self.file.write("playerThreeJleftLimit = " + str(self.playerTwoJleftLimit[0]) + "\n")
            #self.file.write("playerThreeJrightLimit = " + str(self.playerTwoJrightLimit[0]) + "\n\n")
            
        #Write if count players = 3
        if self.cntPlayer == 3:
            self.file.write("figuresDropOneWhite = " + str(self.playerOneDropWhite) + "\n")
            self.file.write("figuresDropOneBlack = " + str(self.playerOneDropBlack) + "\n")
            self.file.write("playerOneJPose = " + str(self.playerOneJPose) + "\n")
            self.file.write("playerOneLPose = " + str(self.playerOneLPose) + "\n")
            #self.file.write("playerOneJleftLimit = " + str(self.playerOneJleftLimit[0]) + "\n")
            #self.file.write("playerOneJrightLimit = " + str(self.playerOneJrightLimit[0]) + "\n\n")
            
            self.file.write("figuresDropTwoWhite = " + str(self.playerTwoDropWhite) + "\n")
            self.file.write("figuresDropTwoBlack = " + str(self.playerTwoDropBlack) + "\n")
            self.file.write("playerTwoJPose = " + str(self.playerTwoJPose) + "\n")
            self.file.write("playerTwoLPose = " + str(self.playerTwoLPose) + "\n")
            #self.file.write("playerTwoJleftLimit = " + str(self.playerTwoJleftLimit[0]) + "\n")
            #self.file.write("playerTwoJrightLimit = " + str(self.playerTwoJrightLimit[0]) + "\n\n")
            
            self.file.write("figuresDropThreeWhite = " + str(self.playerThreeDropWhite) + "\n")
            self.file.write("figuresDropThreeBlack = " + str(self.playerThreeDropBlack) + "\n")
            self.file.write("playerThreeJPose = " + str(self.playerThreeJPose) + "\n")
            self.file.write("playerThreeLPose = " + str(self.playerThreeLPose) + "\n")
            #self.file.write("playerThreeJleftLimit = " + str(self.playerThreeJleftLimit[0]) + "\n")
            #self.file.write("playerThreeJrightLimit = " + str(self.playerThreeJrightLimit[0]) + "\n\n")
            
        
        self.file.close()

        self.close()
        
    def FirstStage(self):
        width=640
        height=360
        self.stage=1
        self.cntPlayer = self.countPlayer.currentIndex()+1
        #self.coordinates=[3,2,3]
        
        self.roi = QLabel(self)
        self.roi.resize(264,264)
        self.roi.move(256,16)
        self.roi.clear()
        self.roi.show()
        self.roiPlayer=1
            
        self.settingScreen(width, height)
        
        self.labelHint.hide()
        self.startBtn.hide()
        self.countPlayer.hide()
        
        self.backBtn = QPushButton('Back', self)
        self.backBtn.resize(192,48)
        self.backBtn.move(16,height-16-self.backBtn.height())
        self.backBtn.show()
        self.backBtn.clicked.connect(self.BackStage)
        
        self.doneBtn = QPushButton('Next', self)
        self.doneBtn.resize(192,48)
        self.doneBtn.move(width-16-self.doneBtn.width(),height-16-self.doneBtn.height())
        #self.doneBtn.setEnabled(False)
        
        self.doneBtn.show()
        if self.doneBtn.text() == str("Next"):
            self.doneBtn.clicked.connect(self.NextStage)
        else:
            self.doneBtn.clicked.connect(self.WriteDataStructers)
        
        self.eventText = QTextEdit(self)
        self.eventText.resize(224,264)
        self.eventText.move(16,16)
        self.eventText.append("Board 1, Step 1: Set the robot to allow the camera to cover the entire chessboard\n")
        self.eventText.setReadOnly(True)
        self.eventText.show()
        
        self.instructionPicture = QLabel(self)
        self.instructionPicture.setPixmap(QPixmap("images/instruction.png"))
        self.instructionPicture.resize(364, 260)
        self.instructionPicture.move(256, 16)
        #self.instructionPicture.show()
        
        self.eventPicture = QLabel(self)
        self.eventPicture.setPixmap(QPixmap("images/instruction_square.png"))
        self.eventPicture.resize(26,26)
        self.eventPicture.move(256+26*10,16+26)
        #self.eventPicture.show()
        
        self.doneBtn.setEnabled(False)
        self.backBtn.setEnabled(False)
        
        
    #def createButton(self, object, name, resizeX, resizeY, moveX, moveY, connect):
    #    self.object = QPushButton(name, self)
    #    self.object.resize(resizeX, resizeY)
    #    self.object.move(moveX, moveY)
    #    self.object.clicked.connect(connect)
    
    def CorrectROIOnly(self):
        
        
        if self._someCounter ==0:
            self.cntPlayer =int(self.countPlayer.currentIndex()+1)
            self.startBtn.hide()
            self.countPlayer.show()
            self.cameraBox.hide()
            self.otherBtn.hide()
            self.otherBtn2.hide()
            self.labelHint.show()
            self.labelHint2.hide()
            self.closeBtn.hide()
            self.correctCams.setText("setPose")
            self.countPlayer.setDisabled(True)
            self._someCounter =1
            self.errorHint.move(16,100)
            self.errorHint.setText("Set camera point 1")
            self.Hint = QLabel('press C on picture',self)
            self.Hint.move(36,118)
            self.Hint.show()
            self.errorHint.show()
            file = open("dataStructers.py", "r")
            fileData= file.read()
            #print(fileData)
            if self.cntPlayer ==1:
            
                self.p1 = fileData[0:fileData.find('playerOneRfPt')]
                self.p2 = fileData[fileData.find('playerTwoRfPt '):fileData.find('playerOneCamChessboard')]
                self.p3 = fileData[fileData.find("playerTwoCamChessboard"):len(fileData)]
                self._someCounter =3
            elif self.cntPlayer ==2:
                self.p1 = fileData[0:fileData.find('playerOneRfPt')]
                self.p2 = fileData[fileData.find('playerThreeRfPt '):fileData.find('playerOneCamChessboard')]
                self.p3 = fileData[fileData.find("playerThreeCamChessboard"):len(fileData)]
                self._someCounter =2
            elif self.cntPlayer ==3:
                self.p1 = fileData[0:fileData.find('playerOneRfPt')]
                self.p2 = fileData[fileData.find("figuresDropOneWhite"):len(fileData)]
                self.p3 = ''
                self._someCounter =1
            file.close()
            self.roiPlayer=1
            self.Roi(2)
            #print('roi corrections for player 1 done')
            #print(self.refPt)
            
            self.playerOneRfPt = self.refPt
            self.playerOneChessboard = self.robot.getj()
               
                    
                
            
        elif self._someCounter ==1:
            self.roiPlayer =2
            self.errorHint.setText("Set camera point 2")
            self.Roi(2)
            self.playerTwoRfPt = self.refPt
            self.playerTwoChessboard = self.robot.getj()
            if self.cntPlayer ==2:
                
                self._someCounter =3
            
        elif self._someCounter ==2:
            self.roiPlayer =3
            self.errorHint.setText("Set camera point 3")
            self.Roi(2)
            self.playerThreeRfPt = self.refPt
            self.playerThreeChessboard = self.robot.getj()
            
            self._someCounter =3
            
        
        elif self._someCounter ==3:
            
            self.Hint.hide()
            self.closeBtn.show()
            self.correctCams.hide()
            self.startBtn.show()
            file = open("dataStructers.py", "w")
            
            
            file.write('camId = '+str(self.camId)+"/n")
            if self.cntPlayer ==1:
                file.write(self.p1)
                file.write("playerOneRfPt = "+ str(self.playerOneRfPt)+ "/n")
                file.write(self.p2)
                file.write("playerOneCamChessboard = "+ str(self.playerOneChessboard)+ "/n")
                file.write(self.p3)
                
            elif self.cntPlayer ==2:
                file.write(self.p1)
                file.write("playerOneRfPt = "+ str(self.playerOneRfPt)+ "/n")
                file.write("playerTwoRfPt = "+ str(self.playertwoRfPt)+ "/n")
                file.write(self.p2)
                file.write("playerOneCamChessboard = "+ str(self.playerOneChessboard)+ "/n")
                file.write("playerTwoCamChessboard = "+ str(self.playerTwoChessboard)+ "/n")
                file.write(self.p3)
            elif self.cntPlayer ==3:
                file.write(self.p1)
                file.write("playerOneRfPt = "+ str(self.playerOneRfPt)+ "/n")
                file.write("playerTwoRfPt = "+ str(self.playertwoRfPt)+ "/n")
                file.write("playerThreeRfPt = "+ str(self.playerthreeRfPt)+ "/n")
                file.write(self.p2)
                file.write("playerOneCamChessboard = "+ str(self.playerOneChessboard)+ "/n")
                file.write("playerTwoCamChessboard = "+ str(self.playerTwoChessboard)+ "/n")
                file.write("playerThreeCamChessboard = "+ str(self.playerThreeChessboard)+ "/n")
                file.write(self.p3)
            file.close()    
            
            
            
        
        
    
    
    def initUI(self):    
        width=224
        height=256
        self.stage=0
        self.settingScreen(width, height)
        self.setWindowTitle('Setting Robot')
        
        self.labelHint = QLabel('Select count Players', self)
        self.labelHint.move(16,16)
        self.labelHint.hide()
        self.labelHint2 =  QLabel('Select camera id and chek it', self)
        self.labelHint2.move(16,16)
        self.errorHint =QLabel('No such camera source',self)
        self.errorHint.move(18,150)
        self.errorHint.hide()
                
        self.startBtn = QPushButton('Correct poses', self)
        self.startBtn.resize(192,32)
        self.startBtn.move(16,192)
        self.startBtn.hide()
        
        self.otherBtn = QPushButton('Camera Ok',self)
        self.otherBtn.resize(192,32)
        self.otherBtn.move(16,192)
        self.otherBtn.clicked.connect(self.CheckDone)
        #self.otherBtn.hide()
        
        self.otherBtn2 = QPushButton('Check Camera',self)
        self.otherBtn2.resize(192,32)
        self.otherBtn2.move(16,92)
        self.otherBtn2.clicked.connect(self.CheckCam)
        
        self.closeBtn = QPushButton('Done',self)
        self.closeBtn.resize(192,32)
        self.closeBtn.move(16,92)
        self.closeBtn.clicked.connect(self.close)
        self.closeBtn.hide()
        
        self.correctCams = QPushButton('Correct ROI`s Only',self)
        self.correctCams.resize(192,32)
        self.correctCams.move(16,140)
        self.correctCams.clicked.connect(self.CorrectROIOnly)
        self._someCounter = 0
        self.correctCams.hide()
        
        
        self.countPlayer = QComboBox(self)
        self.countPlayer.addItem("1 Player")
        self.countPlayer.addItem("2 Players")
        self.countPlayer.addItem("3 Players")
        self.countPlayer.resize(192,32)
        self.countPlayer.move(16,32)
        self.countPlayer.hide()
        
        self.cameraBox = QComboBox(self)
        self.cameraBox.addItem("0")
        self.cameraBox.addItem("1")
        self.cameraBox.addItem("2")
        self.cameraBox.resize(192,32)
        self.cameraBox.move(16,32)
        
        self.startBtn.clicked.connect(self.FirstStage)
        self.startBtn.clicked.connect(self.Roi)
        
        self.show()
     
    def CheckCam(self):
         
        self.camId = int(self.cameraBox.currentText()) 
          
        cam= cv2.VideoCapture(self.camId) 
        ret,frame = cam.read()
        
        if ret:
            cv2.imshow('Cam source test',frame)
            cv2.waitKey(0)
            self.errorHint.hide()
        else:
            self.errorHint.show()
        cam.release()
    
    
        
        
    def CheckDone(self):
        self.camId = int(self.cameraBox.currentText()) 
        self.startBtn.show()
        self.countPlayer.show()
        self.cameraBox.hide()
        self.otherBtn.hide()
        self.otherBtn2.hide()
        self.labelHint.show()
        self.labelHint2.hide()
        self.closeBtn.show()
        self.correctCams.show()
       
if __name__ == '__main__':

    app = QApplication(sys.argv)
    robot =[]
    robot = urx.Robot("192.168.0.20", use_rt=True)
    ex = InitScreenRobot(robot)
    
    sys.exit(app.exec_())
    #playerOneRfPt