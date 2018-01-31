import time    # import the time library for the sleep function
import gopigo3 # import the GoPiGo3 drivers
import easygopigo3 as easy
from di_sensors.light_color_sensor import LightColorSensor
import gopigo3 # import the GoPiGo3 drivers

gpg = easy.EasyGoPiGo3()
GPG2 = gopigo3.GoPiGo3()
lcs = LightColorSensor(led_state = True)
counter = 0

def TurnDegrees(degrees, speed):
    # get the starting position of each motor
    StartPositionLeft      = GPG2.get_motor_encoder(GPG2.MOTOR_LEFT)
    StartPositionRight     = GPG2.get_motor_encoder(GPG2.MOTOR_RIGHT)
    
    # the distance in mm that each wheel needs to travel
    WheelTravelDistance    = ((GPG2.WHEEL_BASE_CIRCUMFERENCE * degrees) / 360)
    
    # the number of degrees each wheel needs to turn
    WheelTurnDegrees       = ((WheelTravelDistance / GPG2.WHEEL_CIRCUMFERENCE) * 360)
    
    # Limit the speed
    GPG2.set_motor_limits(GPG2.MOTOR_LEFT + GPG2.MOTOR_RIGHT, dps = speed)
    
    # Set each motor target
    GPG2.set_motor_position(GPG2.MOTOR_LEFT, (StartPositionLeft + WheelTurnDegrees))
    GPG2.set_motor_position(GPG2.MOTOR_RIGHT, (StartPositionRight - WheelTurnDegrees))

    # See motor degrees
    #GPG2.offset_motor_encoder(GPG2.MOTOR_LEFT, GPG2.get_motor_encoder(GPG.MOTOR_LEFT))
    #GPG2.offset_motor_encoder(GPG2.MOTOR_RIGHT, GPG2.get_motor_encoder(GPG.MOTOR_RIGHT))


def TurnRight():
    print("Turn right")
    TurnDegrees(90, 100)
    time.sleep(2)

def TurnRight45Degrees():
    print("Turn right 45 degrees")
    TurnDegrees(45, 100)
    time.sleep(1.5)

def TurnLeft():
    print("Turn leftTurnDegrees(90, 100)")
    TurnDegrees(-90, 100)
    time.sleep(2)

def TurnLeft45Degrees():
    print("Turn leftTurnDegrees(-45, 100)")
    TurnDegrees(-45, 100)
    time.sleep(1.5)

def GoForwardOne():
    gpg.forward()
    time.sleep(1.5)

def GoForwardTwo():
    gpg.forward()
    time.sleep(2)

def GoForwardThree():
    gpg.forward()
    time.sleep(3)

def GoForwardFive():
    gpg.forward()
    time.sleep(5)

def obstacleAhead():
    my_distance_sensor = gpg.init_distance_sensor()
    time.sleep(0.02)

    print("Distance Sensor Reading (mm): " + str(my_distance_sensor.read_mm()))
    
    if my_distance_sensor.read_mm() < 300:
        return False
    else:
        return True

def Move():
    
    my_distance_sensor = gpg.init_distance_sensor()
    time.sleep(0.02)
    print("Distance Sensor Reading (mm): " + str(my_distance_sensor.read_mm()))

    if my_distance_sensor.read_mm() < 300:
        MoveToTheRightOfTheObstacle()
        time.sleep(1)
    else:
        print("going forward - no object ahead")
        GoForwardOne()

def MoveToTheRightOfTheObstacle():

    print("object ahead!!!! going around")
    global counter
    
    TurnRight()
    GoForwardFive()
    TurnLeft()
    
    counter = counter + 3

    my_distance_sensor = gpg.init_distance_sensor()
    time.sleep(0.02)

    if my_distance_sensor.read_mm() < 300:
        print("obstacle still ahead, will turn right again")
        MoveToTheRightOfTheObstacle()

    print("Now we are right enough, so we will move forward..")
    MoveAheadOfObstacle()
    
    
def MoveAheadOfObstacle():

    global counter
    
    TurnLeft45Degrees()
    
    my_distance_sensor = gpg.init_distance_sensor()
    time.sleep(0.02)
    print("Distance Sensor Reading (mm): " + str(my_distance_sensor.read_mm()))
    my_distance_sensor = my_distance_sensor.read_mm()

    #if theres no obstacle ahead
    if my_distance_sensor > 300:
        print("no obstacle ahead, goign forward two more times")
        TurnRight45Degrees()
        GoForwardFive()
        counter = counter + 1
        

        #first, turn left, 
        TurnLeft()
        
        while counter > 0:
            #then, go left x number of times (where x = number of times we went right)
            print("now going left to be back on track")
            GoForwardOne()
            counter = counter - 1
        #then, move back rightso its in orignal position.
        TurnRight()
        
    else:
        print("onstacle still ahead, will keep going forward!")
        TurnRight45Degrees()
        GoForwardOne()

        MoveAheadOfObstacle()
    
    
try:
    while True:
        Move()

except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    GPG2.reset_all()     

    












        
    
