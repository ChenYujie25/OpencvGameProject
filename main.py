import math
import random

import cvzone
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8, maxHands=1)


class SnakeGame:
    def __init__(self, pathFood):
        self.gameOver = False
        self.score = 0  # Game score
        self.points = []  # points of snake
        self.lengths = []  # distance between each points
        self.currentLength = 0  # total length of the snake
        self.allowedLength = 200  # total allowed length
        self.previousHead = 0, 0  # previous head point

        self.imgFood = cv2.imread(pathFood, cv2.IMREAD_UNCHANGED)
        self.hitFood, self.widFood, _ = self.imgFood.shape
        self.foodPoint = 0, 0
        self.randomFoodLocation()

    def randomFoodLocation(self):
        self.foodPoint = random.randint(100, 1000), random.randint(100, 600)

    def update(self, imgMain, currentHead):

        if self.gameOver:
            cvzone.putTextRect(imgMain, "Game Over", [300, 400],
                               scale=7, thickness=5, offset=20)
            cvzone.putTextRect(imgMain, f'Your Score:{self.score}', [300, 550],
                               scale=7, thickness=5, offset=20)
        else:
            pvsx, pvsy = self.previousHead  # x,y number of previous head point
            crtx, crty = currentHead  # current x and y of the point

            self.points.append([crtx, crty])
            distance = math.hypot(crtx - pvsx, crty - pvsy)
            self.lengths.append(distance)
            self.currentLength += distance
            self.previousHead = crtx, crty

            # Length reduction

            if self.currentLength > self.allowedLength:
                for i, length in enumerate(self.lengths):
                    self.currentLength -= length
                    self.lengths.pop(i)
                    self.points.pop(i)
                    if self.currentLength < self.allowedLength:
                        break

            # Draw Snake

            if self.points:
                for i, point in enumerate(self.points):
                    if i != 0:
                        cv2.line(imgMain, self.points[i - 1], self.points[i], (0, 0, 255), 20)
                cv2.circle(imgMain, self.points[-1], 20, (200, 0, 200), cv2.FILLED)

            # Draw the Food
            rx, ry = self.foodPoint
            imgMain = cvzone.overlayPNG(imgMain, self.imgFood,
                                        (rx - self.widFood // 2, ry - self.hitFood // 2))

            # show Score
            cvzone.putTextRect(imgMain, f'Your Score:{self.score}', [50, 80],
                               scale=3, thickness=3, offset=10)

            # Check if snake ate the food
            rx, ry = self.foodPoint
            if rx < crtx < rx + self.widFood and ry < crty < ry + self.hitFood:
                self.randomFoodLocation()
                self.allowedLength += 50
                self.score += 1
                # print(self.score)

            # check for collision 蛇撞到身体则游戏结束
            pts = np.array(self.points[:-2], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(imgMain, [pts], False, (0, 200, 0), 3)
            minDistance = cv2.pointPolygonTest(pts, (crtx, crty), True)
            print(minDistance)
            if -0.1 <= minDistance <= 0.1:
                print("Hit!")
                # refresh the game
                self.gameOver = True
                self.points = []  # points of snake
                self.lengths = []  # distance between each points
                self.currentLength = 0  # total length of the snake
                self.allowedLength = 200  # total allowed length
                self.previousHead = 0, 0  # previous head point
                self.randomFoodLocation()
        return imgMain


game = SnakeGame("cloud.png")

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    if hands:
        # landmarkList
        lmList = hands[0]['lmList']
        pointIndex = lmList[8][0:2]  # 2维手部骨骼食指坐标列表
        img = game.update(img, pointIndex)
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('r'):
        game.gameOver = False
        game.score = 0  # Game score
