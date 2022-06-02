import cv2
import numpy as np
import pygame
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time

from circleBase import Item

pygame.init()

# create window
width, height = 1280, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("my game")

# Camera

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.7)

# initialize fps clock
fps = 60
clock = pygame.time.Clock()

# main
firstItem = Item(window)

start = True
while start:
    # get events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()

    # apply logic

    # Opencv

    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)
    if hands:
        # landmarkList
        lmList_1 = hands[0]['lmList']

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imgRGB = np.rot90(imgRGB)
    frame = pygame.surfarray.make_surface(imgRGB).convert()
    frame = pygame.transform.flip(frame, True, False)
    window.blit(frame, (0, 0))
    # block logic
    firstItem.draw_item()
    firstItem.update()

    # update display

    pygame.display.update()
    # set fps
    clock.tick(fps)
