import urx
import time
robot = urx.Robot('192.168.0.20',use_rt=True)

state1 =False
state2= False
state3= False

def check_button():
    check1 = robot.get_digital_in(0)
    if check1 ==True:
        file = open('status.txt','r')
        data = file.read()
        file.close()
        data[0]='1'
        file = open('status.txt','w')
        file.write(data)
        file.close()
    check2 = robot.get_digital_in(1)
    if check2 == True:
        file = open('status.txt','r')
        data = file.read()
        file.close()
        data[1]='1'
        file = open('status.txt','w')
        file.write(data)
        file.close()
    check3 = robot.get_digital_in(2)
    if check3 == True:
        file = open('status.txt','r')
        data = file.read()
        file.close()
        data[2]='1'
        file = open('status.txt','w')
        file.write(data)
        file.close()
    time.sleep(0.5)
if __name__ == __main__:
    i = 0
    while True:
        check_button()
        i+=1
        if i==10:
            print('Check tick')
            i=0
