import pygame
pygame.init()
RESOLUTIONS = [(720, 480), (960, 540), (1280, 720), (1366,768), (1600, 900), (1920, 1080), (2560, 1440)]
WIDTH, HEIGHT = RESOLUTIONS[0]
PORT = 50008
characterChoice = 0
ACCELERATION = 1
STUN_DURATION = 0.25
IP_ADDRESS = '127.0.0.1'
WAIT = True
tab_Colour, tab_selectColour, tab_outerColour = (50, 50, 50), "white", "blue"


sully_info = [[6, 0.05, 51, 45, 8, 2, 9, "sprites/Sully_idle.png"],
              [21, 0.5, 56, 45, 4, 0, 9, "sprites/Sully_run-Sheet.png"],
              [9, 0.5, 54, 48, 6, 0, 5, "sprites/Sully_jump-Sheet.png"],
              [1, 0, 52, 48, 8, 3, 5, "sprites/Sully_fall-Sheet.png"],
              [1, 0, 51, 51, 9, 3, 2, "sprites/Sully_fast-fall-Sheet.png"],
              [9, 0.4, 69, 47, 21, 1, 7,"sprites/Sully-Slight-Sheet.png"],
              [13, 0.4, 58, 50, 1, 1, 5, "sprites/Sully_Nlight-Sheet.png"],
              [12, 0.35, 78, 54, 12, 0, 0, "sprites/Sully_Dlight-Sheet.png"]]























