import math
import random
from statistics import mode

def detect_squares(dots):
   getModeGroup = [];
   for x in range(0, 10):
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
            Ones+=1;
         else:
            centerSquareTwoX += dots[i][0]
            centerSquareTwoY += dots[i][1]
            Twos+=1;
      if Ones == 0:
         centerSquareOne = seedOne
      else:
         centerSquareOne = (centerSquareOneX/Ones, centerSquareOneY/Ones)
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
         centerSquareOne = seedOne
      else:
         centerSquareOne = (centerSquareOneX / Ones, centerSquareOneY / Ones)
      if Twos == 0:
         centerSquareTwo = seedTwo
      else:
         centerSquareTwo = (centerSquareTwoX / Twos, centerSquareTwoY / Twos)
      combined = (centerSquareOne, centerSquareTwo)
      getModeGroup.append(combined)
   rightAnswer = mode(getModeGroup)
   return rightAnswer[0], rightAnswer[1]

def getDistance(testPoint, seedPoint):
   dist = math.sqrt((testPoint[0]-seedPoint[0])**2 + (testPoint[1]-seedPoint[1])**2)
   return dist
