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

figuresDropOneWhite = [0.21869377089141895, 0.21011012151135053, 0.007074262430731407, -1.5695672888915648, 0.011130066353245075, -0.028126005266537996]
figuresDropOneBlack = [-0.2850486507865893, 0.20805706302827867, 0.0061128822391171705, -1.5749129879288757, 0.020048489207885933, -0.004185079725394194]


figuresDropTwoWhite = [0.21869377089141895, 0.21011012151135053, 0.007074262430731407, -1.5695672888915648, 0.011130066353245075, -0.028126005266537996]

figuresDropTwoBlack = [-0.2850486507865893, 0.20805706302827867, 0.0061128822391171705, -1.5749129879288757, 0.020048489207885933, -0.004185079725394194]

figuresDropThreeWhite = [0.21869377089141895, 0.21011012151135053, 0.007074262430731407, -1.5695672888915648, 0.011130066353245075, -0.028126005266537996]

figuresDropThreeBlack = [-0.2850486507865893, 0.20805706302827867, 0.0061128822391171705, -1.5749129879288757, 0.020048489207885933, -0.004185079725394194]

playerOneRfPt = [(82, 2), (573, 481)]
playerTwoRfPt = [(82, 2), (573, 481)]
playerThreeRfPt = [(82, 2), (573, 481)]

#playerOneCamChessboard = [0.09675389528274536, -1.3994048277484339, -1.4052794615374964, -1.9647515455829065, -1.5906232039081019, 3.0755436420440674]
playerOneCamChessboard = [1.8162250518798828, -1.4802187124835413, -1.3213704268084925, -1.9307964483844202, -1.6237886587726038, 2.914108991622925]
playerTwoCamChessboard = [1.8162250518798828, -1.4802187124835413, -1.3213704268084925, -1.9307964483844202, -1.6237886587726038, 2.914108991622925]
playerThreeCamChessboard = [1.8162250518798828, -1.4802187124835413, -1.3213704268084925, -1.9307964483844202, -1.6237886587726038, 2.914108991622925]


#playerOneJPose =  [0.08900909125804901, -1.6477697531329554, -1.4908612410174769, -1.5547736326800745, 1.5817259550094604, 0.1801697164773941]
#playerOneLPose =  [0.45314738468687216, -0.16881999501108105, 0.023660661182472925, -1.1208433377154408, 1.2477971095137799, -1.2876061373162973]
playerOneJPose = [1.8050403594970703, -1.6614320913897913, -1.4907053152667444, -1.5547612349139612, 1.5818578004837036, 0.180193692445755]
playerOneLPose =  [0.14346309815115846, 0.4884450656636697, 0.022482832290728713, -1.5170048279622137, 0.007462587185121416, -0.0038205321062002016]

playerTwoJPose = [1.8050403594970703, -1.6614320913897913, -1.4907053152667444, -1.5547612349139612, 1.5818578004837036, 0.180193692445755]
playerTwoLPose =  [0.14346309815115846, 0.4884450656636697, 0.022482832290728713, -1.5170048279622137, 0.007462587185121416, -0.0038205321062002016]
                  
playerThreeJPose = [3.6829328536987305, -1.6158984343158167, -1.474543873463766, -1.583454434071676, 1.533982276916504, 0.5338751673698425]
playerThreeLPose = [0.48406619046003424, -0.1704353009513687, 0.022907569496674024, -1.229713923214575, 1.216681344565119, -1.1868963956414373]

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

dropboard_squareX = 0.036
dropboard_squareY = 0.036

#robot speed
vel = 0.8
acc = 0.8
#robot sleep after move
sleep = 0.2

#inputs
InButton[0] = 2
InButton[1] = 3
InButton[2] = 4

#outputs
OutGrip = 0
led_flash = 1
OutButton[0] = 2
OutButton[1] = 3
OutButton[2] = 4
led_blue = 5
led_red = 6
#last free slot output 7