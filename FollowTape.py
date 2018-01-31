import time
from di_sensors.light_color_sensor import LightColorSensor
import gopigo3 # import the GoPiGo3 drivers
import easygopigo3 as easy

print("Example Program")
gpg = easy.EasyGoPiGo3()
GPG2 = gopigo3.GoPiGo3()
lcs = LightColorSensor(led_state = True)


#below vars are used for Turn() normal 
rightTurns = 0
leftTurns = 0
distance = 0

#true is left, false is right
anger = True

#below vars are used for 
lastTurned = 0
#0 = neutral, 1 = left, 2 = right.


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

def Move():

    my_distance_sensor = gpg.init_distance_sensor()
    time.sleep(0.02)
    print("Distance Sensor Reading (mm): " + str(my_distance_sensor.read_mm()))
    
    print("Move the motors forward freely for 1 second.")

    #sense objects
    if my_distance_sensor.read_mm() < 20:
        Spin()
        time.sleep(0.1)
    else:
        gpg.forward()
        time.sleep(0.2)

    global rightTurns
    global leftTurns
    
    rightTurns = 0
    leftTurns = 0

def TurnRight():
    print("Turn right")
    TurnDegrees(5, 100)
    time.sleep(0.01)

def TurnLeft():
    print("Turn leftTurnDegrees(94, 100)")
    TurnDegrees(-5, 100)
    time.sleep(0.01)

def TurnSlightlyRight():
    print("Turn SLIGHTLY right")
    TurnDegrees(2, 100)
    time.sleep(0.01)

def TurnSlightlyLeft():
    print("Turn SLIGHTLY leftTurnDegrees(94, 100)")
    TurnDegrees(-2, 100)
    time.sleep(0.01)

def Spin():
    print("Spin")
    TurnDegrees(-180, 100)
    time.sleep(4)

def Turn(red, green, blue, clear):

    global rightTurns
    global leftTurns
    global distance

    global anger
    global lastTurned

    isBlack = 0

    leftCounter = 0
    rightCounter = 0

    #first, check where you turned last.
    if lastTurned == 1:

        while isBlack == 0 and leftCounter < 10:
            
            print("CHECKING optimized LEFT")
            TurnSlightlyLeft()
            
            if isOnBlack(red, green, blue, clear) == 1:
                isBlack = 1

            leftCounter = leftCounter + 1

        if isBlack == 0 and leftCounter == 10:
            for x in range(10):
                TurnSlightlyRight()

            lastTurned = 0


                
    if lastTurned == 2:

        while isBlack == 0 and rightCounter < 10:
            
            print("CHECKING optimized RIGHT")
            TurnSlightlyRight()
            
            if isOnBlack(red, green, blue, clear) == 1:
                isBlack = 1

            rightCounter = rightCounter + 1
                
        if isBlack == 0 and rightCounter == 10:
            for y in range(10):
                TurnSlightlyLeft()
                
            lastTurned = 0
                
    
    count = 1
    x = 0
    direction = True
    
    while isBlack == 0:

        if direction == True:
            
            while x < count and isBlack == 0:
                TurnRight()
                x = x + 1
                print("Normal right")
            isBlack = isOnBlack(red, green, blue, clear)

            if isBlack == 1:
                lastTurned = 2
            
            count = count + 1
            x = 0
            direction = False

        if direction == False:
            
            while x < count and isBlack == 0:
                TurnLeft()
                x = x + 1
                print("Normal left")
            isBlack = isOnBlack(red, green, blue, clear)
            count = count + 1
            x = 0
            direction = True

            if isBlack == 1 and lastTurned != 2:
                lastTurned = 1


        TurnDegrees(-3.5, 100)
        time.sleep(0.1)
        gpg.forward()
        time.sleep(0.02)

        

    if isBlack < 1:
        
        gpg.forward()
        time.sleep(0.5)

        SpinAndCheck(red, green, blue, clear)



def SpinAndCheck(red, green, blue, clear):

    checkCounter = 0

    while checkCounter < 72:
        
        TurnRight()

        if isOnBlack(red, green, blue, clear) > 0:
            checkCounter = 72

        checkCounter = checkCounter + 1


    if isOnBlack(red, green, blue, clear) == 0:
        TurnDegrees(90, 100)
        time.sleep(1)
        gpg.forward()
        time.sleep(1)
        SpinAndCheck(red, green, blue, clear)
        


def FindRed(red, green, blue, clear):

    my_distance_sensor = gpg.init_distance_sensor()
    time.sleep(0.02)
    #print("Distance Sensor Reading (mm): " + str(my_distance_sensor.read_mm()))

    distanceToTravel = my_distance_sensor.read_mm()

    while distanceToTravel > 200:

        print("checking for RED")

        if distanceToTravel > 500:
            gpg.forward()
            time.sleep(1)
    
        elif distanceToTravel >= 200 and distanceToTravel <= 500:
            gpg.forward()
            time.sleep(0.2)

        my_distance_sensor = gpg.init_distance_sensor()
        time.sleep(0.02)
        distanceToTravel = my_distance_sensor.read_mm()


    if isOnRed(red, green, blue, clear) > 0:
        gpg.forward()
        time.sleep(0.4)
        TurnDegrees(90, 100)
        time.sleep(1)
    else:
        SpinAndCheck(red, green, blue, clear)

        
    

def drive(red, green, blue, clear):

    if isOnGreen(red, green, blue, clear) > 0:
        FindRed(red, green, blue, clear)

    if isOnBlack(red, green, blue, clear) > 0:
        Move()
    else:
        Turn(red, green, blue, clear)
        
    
    

def isOnBlack(red, green, blue, clear):
    
    red, green, blue, clear = lcs.get_raw_colors()
    time.sleep(0.01)
    
    if red > 0.002 and red < 0.1:
        if green > 0.002 and green < 0.1:
            if blue > 0.001 and blue < 0.07:
                if clear > 0.001 and clear < 0.2:
                    return 1

    return 0



def isOnGreen(red, green, blue, clear):

    red, green, blue, clear = lcs.get_raw_colors()
    time.sleep(0.01)
    
    if red > 0.003 and red < 0.06:
        if green > 0.06 and green < 0.08:
            if blue > 0.03 and blue < 0.06:
                if clear > 0.1 and clear < 0.2:
                    return 1

    return 0


def isOnRed(red, green, blue, clear):

    red, green, blue, clear = lcs.get_raw_colors()
    time.sleep(0.01)
    
    if red > 0.10 and red < 0.30:
        if green > 0.03 and green < 0.07:
            if blue > 0.03 and blue < 0.06:
                if clear > 0.2 and clear < 0.4:
                    return 1

    return 0



                    
while True:

    red, green, blue, clear = lcs.get_raw_colors()
    time.sleep(0.01)

    my_distance_sensor = gpg.init_distance_sensor()
    time.sleep(0.02)
    print("Distance Sensor Reading (mm): " + str(my_distance_sensor.read_mm()))


    drive(red, green, blue, clear)

    print("Red: {:5.3f} Green: {:5.3f} Blue: {:5.3f} Clear: {:5.3f}".format(red, green, blue, clear))

    gpg.stop()
    print("Done!")
























