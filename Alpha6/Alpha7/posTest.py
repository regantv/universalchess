import urx
robot = urx.Robot('192.168.0.20',use_rt=True)
def ReturnCoords(square):
        tick = 0
        res=[0,0]
        for x in range(8):
            for y in range(8):
                if tick ==square:
                    res[1]=x
                    res[0]=y
                
                tick+=1    
        
        return(res)
 
res = ReturnCoords(63)
pose = [0.13958703016456953, 0.49020401760824445, 0.02551327579093221, -1.5599393702678608, 0.003813643784290574, -0.015171484424153947]
robot.movel(pose,vel =0.4,acc=0.4)
a= input('press enter to continue')
deltaX = 0.04
deltaY = 0.04

pose[0]=pose[0] - deltaX*res[0]
pose[1]=pose[1] - deltaY*res[1]
robot.movel(pose,vel =0.4,acc=0.4)
