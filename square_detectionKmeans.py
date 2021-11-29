import math
import random
from statistics import mode


def detect_squares(dots):
    getModeGroup = []
    for x in range(0, 100):
        seedOne = (random.randrange(1, 485, 1), random.randrange(1, 719, 1))
        seedTwo = (random.randrange(1, 485, 1), random.randrange(1, 719, 1))
        centerSquareOneX = 0
        centerSquareOneY = 0
        centerSquareTwoX = 0
        centerSquareTwoY = 0
        Ones = 0;
        Twos = 0;
        for i in range(0, len(dots)):
            disOne = getDistance(dots[i], seedOne)
            disTwo = getDistance(dots[i], seedTwo)
            if disOne < disTwo:
                centerSquareOneX += dots[i][0]
                centerSquareOneY += dots[i][1]
                Ones += 1;
            else:
                centerSquareTwoX += dots[i][0]
                centerSquareTwoY += dots[i][1]
                Twos += 1;
        if Ones == 0:
            centerSquareOne = seedOne
        else:
            centerSquareOne = (centerSquareOneX / Ones, centerSquareOneY / Ones)
        if Twos == 0:
            centerSquareTwo = seedTwo
        else:
            centerSquareTwo = (centerSquareTwoX / Twos, centerSquareTwoY / Twos)
        centerSquareOneX = 0
        centerSquareOneY = 0
        centerSquareTwoX = 0
        centerSquareTwoY = 0
        Ones = 0;
        Twos = 0;
        for i in range(0, len(dots)):
            disOne = getDistance(dots[i], centerSquareOne)
            disTwo = getDistance(dots[i], centerSquareTwo)
            if disOne < disTwo:
                centerSquareOneX += dots[i][0]
                centerSquareOneY += dots[i][1]
                Ones += 1;
            else:
                centerSquareTwoX += dots[i][0]
                centerSquareTwoY += dots[i][1]
                Twos += 1;
        if Ones == 0:
            centerSquareOne = centerSquareOne
        else:
            centerSquareOne = (centerSquareOneX / Ones, centerSquareOneY / Ones)
        if Twos == 0:
            centerSquareTwo = centerSquareTwo
        else:
            centerSquareTwo = (centerSquareTwoX / Twos, centerSquareTwoY / Twos)
        centerSquareOneX = 0
        centerSquareOneY = 0
        centerSquareTwoX = 0
        centerSquareTwoY = 0
        Ones = 0;
        Twos = 0;
        OnesList = []
        TwosList = []
        for i in range(0, len(dots)):
            disOne = getDistance(dots[i], centerSquareOne)
            disTwo = getDistance(dots[i], centerSquareTwo)
            if disOne < disTwo:
                centerSquareOneX += dots[i][0]
                centerSquareOneY += dots[i][1]
                Ones += 1;
                OnesList.append(dots[i])
            else:
                centerSquareTwoX += dots[i][0]
                centerSquareTwoY += dots[i][1]
                Twos += 1;
                TwosList.append(dots[i])
        if Ones == 0:
            centerSquareOne = centerSquareOne
        else:
            centerSquareOne = (centerSquareOneX / Ones, centerSquareOneY / Ones)
        if Twos == 0:
            centerSquareTwo = centerSquareTwo
        else:
            centerSquareTwo = (centerSquareTwoX / Twos, centerSquareTwoY / Twos)
        if reasonableDotDist(OnesList, TwosList, centerSquareOne, centerSquareTwo):
            if (getDistance(centerSquareOne, centerSquareTwo) > 100):
                combined = (centerSquareOne, centerSquareTwo)
                getModeGroup.append(combined)
    rightAnswer = mode(getModeGroup)
    return rightAnswer[0], rightAnswer[1]


def getDistance(testPoint, seedPoint):
    dist = math.sqrt((testPoint[0] - seedPoint[0]) ** 2 + (testPoint[1] - seedPoint[1]) ** 2)
    return dist


def reasonableDotDist(OnesList, TwosList, centerSquareOne, centerSquareTwo):
    isReasonable = True
    for i in range(0, len(OnesList)):
        if (abs(OnesList[i][0] - centerSquareOne[0]) > 50) and (abs(OnesList[i][1] - centerSquareOne[1]) > 50):
            isReasonable = False
    for i in range(0, len(TwosList)):
        if (abs(TwosList[i][0] - centerSquareTwo[0]) > 50) and (abs(TwosList[i][1] - centerSquareTwo[1]) > 50):
            isReasonable = False
    return isReasonable
