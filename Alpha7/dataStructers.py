camId = 0
import cv2
picStruct = {'r':cv2.imread('images/Chess_tile_rd.png'),
             'n':cv2.imread('images/Chess_tile_nd.png'),
             'b':cv2.imread('images/Chess_tile_bd.png'),
             'q':cv2.imread('images/Chess_tile_qd.png'),
             'k':cv2.imread('images/Chess_tile_kd.png'),
             'p':cv2.imread('images/Chess_tile_pd.png'),
             'R':cv2.imread('images/Chess_tile_rl.png'),
             'N':cv2.imread('images/Chess_tile_nl.png'),
             'B':cv2.imread('images/Chess_tile_bl.png'),
             'Q':cv2.imread('images/Chess_tile_ql.png'),
             'K':cv2.imread('images/Chess_tile_kl.png'),
             'P':cv2.imread('images/Chess_tile_pl.png')}


figureGripStruc = {'r':0.000,'n':0.000,'b':0.0,'k':0.00,'q':0.00,'p':0.000,
                   'R':0.000,'N':0.000,'B':0.0,'K':0.00,'Q':0.00,'P':0.000}

figuresDropWhitePos = {'R1':[0,0],'R2':[0,1],'N1':[0,2],'N2':[0,3],'B1':[0,4],'B2':[0,5],'Q':[0,6],'K':[0,7],
                  'P1':[1,0],'P2':[1,1],'P3':[1,2],'P4':[1,3],'P5':[1,4],'P6':[1,5],'P7':[1,6],'P8':[1,7]}

figuresDropBlackPos = {'r1':[0,0],'r2':[0,1],'n1':[0,2],'n2':[0,3],'b1':[0,4],'b2':[0,5],'q':[0,6],'k':[0,7],
                  'p1':[1,0],'p2':[1,1],'p3':[1,2],'p4':[1,3],'p5':[1,4],'p6':[1,5],'p7':[1,6],'p8':[1,7]}

figuresDropOneWhite = [0.2226199581395955, -0.2413106464984133, 0.004521873290439654, -1.1888566259114783, 1.2751558363875575, -1.222291475265545]
figuresDropOneBlack = [0.22065935104114362, 0.21853450219708218, 0.004531925825264141, -1.3145427260911073, 1.110702464946953, -1.0609430788347265]


figuresDropTwoWhite = [0.21570294174424737, 0.25229467385743654, 0.0051567756953772165, -1.5915426557799432, -0.03288984140886565, 0.0644958368540305]
figuresDropTwoBlack = [-0.2126302764856404, 0.1843793650950863, 0.0050080230611023735, -1.574513054059778, 0.008565226444295988, 0.010052695806055573]

figuresDropThreeWhite = [-0.2794468516590527, 0.1782911946406694, 0.005890793975399156, -1.2329441713536013, -1.2727155867261877, 1.246349485850643]
figuresDropThreeBlack = [-0.18612024209753247, -0.2904139672663766, 0.00769960642904137, -1.2765658152562271, -1.243957148124726, 1.165370924323247]

playerOneRfPt = [(82, 1), (560, 477)]
playerTwoRfPt = [(82, 1), (560, 477)]
playerThreeRfPt = [(82, 1), (560, 477)]

#playerOneCamChessboard = [0.09675389528274536, -1.3994048277484339, -1.4052794615374964, -1.9647515455829065, -1.5906232039081019, 3.0755436420440674]
playerOneCamChessboard = [0.0441933274269104, -1.6745670477496546, -1.1097753683673304, -1.9756305853473108, -1.582313362752096, 3.1235830783843994]
playerTwoCamChessboard = [1.7478584051132202, -1.4301851431476038, -1.3925460020648401, -1.8423822561847132, -1.5990880171405237, 2.996983528137207]
playerThreeCamChessboard = [3.4338903427124023, -1.3611272017108362, -1.4523032347308558, -1.8463237921344202, -1.5878532568561, 2.871652603149414]


#playerOneJPose =  [0.08900909125804901, -1.6477697531329554, -1.4908612410174769, -1.5547736326800745, 1.5817259550094604, 0.1801697164773941]
#playerOneLPose =  [0.45314738468687216, -0.16881999501108105, 0.023660661182472925, -1.1208433377154408, 1.2477971095137799, -1.2876061373162973]
playerOneJPose = [0.22582100331783295, -1.7258575598346155, -1.5538619200335901, -1.4542248884784144, 1.5804448127746582, 0.16899892687797546]
playerOneLPose =  [0.4891971091235066, -0.16777891314492066, 0.025072763639819376, -1.1911526236342678, 1.1942552950730323, -1.1983250575131115]

playerTwoJPose = [1.8050403594970703, -1.6614320913897913, -1.4907053152667444, -1.5547612349139612, 1.5818578004837036, 0.180193692445755]
playerTwoLPose =  [0.1355215899676299, 0.4896355868741783, 0.02524315708291347, -1.532280749390148, -0.02360076535176015, 0.05529700196208077]
                  
playerThreeJPose = [3.5324156284332275, -1.6254108587848108, -1.3376057783709925, -1.739281956349508, 1.5746710300445557, 0.44801902770996094]
playerThreeLPose = [-0.4816452635124217, 0.10479411991828315, 0.02542935149605384, -1.2123312453334991, -1.2129096652058202, 1.245559528683865]

playerOneJleftLimit =2.721442937850952
playerOneJrightLimit =1.3371856212615967

playerTwoJleftLimit =2.721442937850952
playerTwoJrightLimit =1.3371856212615967

playerThreeJleftLimit =2.721442937850952
playerThreeJrightLimit =1.3371856212615967




boardStructure = ['a1','b1','c1','d1','e1','f1','g1','h1',
                  'a2','b2','c2','d2','e2','f2','g2','h2',
                  'a3','b3','c3','d3','e3','f3','g3','h3',
                  'a4','b4','c4','d4','e4','f4','g4','h4',
                  'a5','b5','c5','d5','e5','f5','g5','h5',
                  'a6','b6','c6','d6','e6','f6','g6','h6',
                  'a7','b7','c7','d7','e7','f7','g7','h7',
                  'a8','b8','c8','d8','e8','f8','g8','h8']





picStruct = {'r':cv2.resize(cv2.imread('images/Chess_tile_rd.png'),(50,50)),
             'n':cv2.resize(cv2.imread('images/Chess_tile_nd.png'),(50,50)),
             'b':cv2.resize(cv2.imread('images/Chess_tile_bd.png'),(50,50)),
             'q':cv2.resize(cv2.imread('images/Chess_tile_qd.png'),(50,50)),
             'k':cv2.resize(cv2.imread('images/Chess_tile_kd.png'),(50,50)),
             'p':cv2.resize(cv2.imread('images/Chess_tile_pd.png'),(50,50)),
             'R':cv2.resize(cv2.imread('images/Chess_tile_rl.png'),(50,50)),
             'N':cv2.resize(cv2.imread('images/Chess_tile_nl.png'),(50,50)),
             'B':cv2.resize(cv2.imread('images/Chess_tile_bl.png'),(50,50)),
             'Q':cv2.resize(cv2.imread('images/Chess_tile_ql.png'),(50,50)),
             'K':cv2.resize(cv2.imread('images/Chess_tile_kl.png'),(50,50)),
             'P':cv2.resize(cv2.imread('images/Chess_tile_pl.png'),(50,50))}
chessboard_squareX = 0.04
chessboard_squareY = 0.04

dropboard_squareX = 0.034
dropboard_squareY = 0.034

#robot speed
vel = 0.8
acc = 0.8
#robot sleep after move
sleep = 0.2

#inputs
InButtonOne = 2
InButtonTwo = 3
InButtonThree = 4

#outputs
OutGrip = 0
led_flash = 1
OutButtonOne = 2
OutButtonTwo = 3
OutButtonThree = 4
led_blue = 5
led_red = 6
#last free slot output 7