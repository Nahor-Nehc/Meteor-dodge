import pygame
import random
import sys
import os
import PySimpleGUI as sg 

pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 600, 650
SPACESHIPSIZE = (68, 76)

HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Grenade+1.mp3"))
HEART_SOUND = pygame.mixer.Sound(os.path.join("Assets", "heart.mp3"))
MUSIC = pygame.mixer.Sound(os.path.join("Assets", "music.mp3"))
MUSIC.play(-1)

FPS = 60
PADDING = 20
DURATION = 500
VEL = 5
MICROVEL = 2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 140, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (200, 200, 200)

SPACESHIP = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))
SPACESHIP = pygame.transform.scale(SPACESHIP, (SPACESHIPSIZE))

ASTEROID = pygame.image.load(os.path.join("Assets", "asteroid.png"))
HEART = pygame.image.load(os.path.join("Assets", "heart.png"))
SIZE = 100

PBWIDTH, PBHEIGHT = 300, 70
PBX, PBY = (WIDTH - PBWIDTH)/2, 400
RBWIDTH, RBHEIGHT = 300, 70
RBX, RBY = (WIDTH - RBWIDTH)/2, 400
HWIDTH, HHEIGHT = 70, 300
HX, HY = PADDING, PADDING
HPWIDTH, HPHEIGHT = HWIDTH/3, 40
LEADERBOARDY = 100
LEADERBOARDX = 50

FONT = pygame.font.SysFont("calibri.ttf", 30)
BIGFONT = pygame.font.SysFont("calibri.ttf", 80)
ARROWFONT = pygame.font.SysFont("segoeuisymbol", 30)

SETSTATEGAME = pygame.USEREVENT + 1
HIT = pygame.USEREVENT + 2
RESTART = pygame.USEREVENT + 3
HEARTHIT = pygame.USEREVENT + 4

CONTROLS = [["G", "toggle hitboxes", FONT], ["⟷", "arrows for normal movement", ARROWFONT], ["WASD", "Fine controls", FONT], ["SPACE", "Pause game", FONT]]

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge")

MAXHEALTH = 5

def drawWindow(state, lastStarTime, stars, ship, lastAsteroidTime, asteroids, pressPlayTime, SHIP, health, score, hpplus, fireParticles, showHitBox, showControls, countTime, fileR):

  if state == "pause":
    text = BIGFONT.render("Game Paused", 1, WHITE)
    WIN.blit(text, ((WIDTH - text.get_width())/2, HEIGHT*1/4))

  elif state == "fail":

    #buttons

    text = FONT.render("Game Over", 1, WHITE)
    WIN.blit(text, ((WIDTH - text.get_width())/2, PADDING*6))
    restartText = FONT.render("Restart?", 1, BLACK)
    pygame.draw.rect(WIN, GREY, pygame.rect.Rect(RBX, RBY, RBWIDTH, RBHEIGHT))
    WIN.blit(restartText, ((WIDTH - restartText.get_width())/2, RBY + PADDING*3/2))

    #---------------

  elif state == "menu":

    #background

    pygame.draw.rect(WIN, BLACK, pygame.Rect(0, 0, WIDTH, HEIGHT))

    if countTime >= lastStarTime + DURATION/2:
      x = random.randint(1, WIDTH)
      y = -10
      size = random.randint(2, 5)
      speed = random.randint(2, 10)
      stars.append([x, y, size, speed])
      lastStarTime = countTime

    for star in stars:
      star[1] += star[3]
      pygame.draw.circle(WIN, GREY, (star[0], star[1]), star[2])

    #---------------

    #ship

    WIN.blit(SPACESHIP, (ship[0], ship[1]))

    #---------------

    #buttons

    playText = FONT.render("Play", 1, BLACK)
    pygame.draw.rect(WIN, GREY, pygame.rect.Rect(PBX, PBY, PBWIDTH, PBHEIGHT))
    WIN.blit(playText, ((WIDTH - playText.get_width())/2, PBY + PADDING*3/2))

    #---------------

    #leaderboard

    filething = sorted(fileR,key=lambda l:int(l[1]), reverse=True)
    if len(filething) >= 10:
      max = 10
    else:
      max = len(filething)
    for scoring in range(0, max):
      leaderboard = FONT.render(str(scoring+1) +  "   " + filething[scoring][0] + "   " + filething[scoring][1], 1, WHITE)
      WIN.blit(leaderboard, (LEADERBOARDX, LEADERBOARDY + leaderboard.get_height()*scoring))

    #---------------

  elif state == "countdown":

    #background

    pygame.draw.rect(WIN, BLACK, pygame.Rect(0, 0, WIDTH, HEIGHT))

    if countTime >= lastStarTime + DURATION/2:
      x = random.randint(1, WIDTH)
      y = -10
      size = random.randint(2, 5)
      speed = random.randint(2, 10)
      stars.append([x, y, size, speed])
      lastStarTime = countTime

    for star in stars:
      if star[1] <= HEIGHT:
        star[1] += star[3]
        pygame.draw.circle(WIN, GREY, (star[0], star[1]), star[2])
      else:
        stars.remove(star)

    #---------------

    #countdown

    number = 3 - int((pressPlayTime - pygame.time.get_ticks())/ -1000)

    numberText = BIGFONT.render(str(number), 1, WHITE)
    WIN.blit(numberText, ((WIDTH - numberText.get_width())/2, PADDING * 6))
    if number == 0:
      pygame.event.post(pygame.event.Event(SETSTATEGAME))

    #---------------

    #ship

    WIN.blit(SPACESHIP, (ship[0], ship[1]))

    #---------------

    #ship fire particles

    if random.randint(1, 5) == 1:
      x = random.randint(ship[0] + 5, ship[0] + SPACESHIPSIZE[0] - 5)
      y = ship[1] + SPACESHIPSIZE[1] - 5
      size = 4
      speed = 3
      timeAlive = 0
      col = RED
      fireParticles.append([x, y, size, speed, timeAlive, col])

    for part in fireParticles:
      part[1] += part[3]
      part[4] += 1
      if part[4] >= 30 and random.randint(1, 5) == 1:
        fireParticles.remove(part)
      elif part[4] >= 20:
        part[5] = YELLOW
      elif part[4] >= 10:
        part[5] = ORANGE
      pygame.draw.rect(WIN, part[5], pygame.Rect(part[0], part[1], part[2], part[2]))

    #---------------

    #controls
    
    for control in CONTROLS:
      width = ARROWFONT.render("W", 1, WHITE).get_width()
      height = ARROWFONT.render("W", 1, WHITE).get_height()
      cText = control[2].render(control[0], 1, WHITE)
      if control == CONTROLS[1]:
        WIN.blit(cText, (PADDING, HEIGHT - PADDING*(len(CONTROLS)-1) - PADDING - height * CONTROLS.index(control)))
        explainText = FONT.render(control[1], 1, WHITE)
      else:
        WIN.blit(cText, (PADDING, HEIGHT - PADDING*(len(CONTROLS)-1) - height * CONTROLS.index(control)))
        explainText = FONT.render(control[1], 1, WHITE)
      WIN.blit(explainText, (PADDING + width + PADDING*2, HEIGHT - PADDING*(len(CONTROLS)-1) - height * CONTROLS.index(control)))

    #---------------

  elif state == "game":

    #background

    pygame.draw.rect(WIN, BLACK, pygame.Rect(0, 0, WIDTH, HEIGHT))

    if countTime >= lastStarTime + DURATION/2:
      x = random.randint(1, WIDTH)
      y = -10
      size = random.randint(2, 5)
      speed = random.randint(2, 10)
      stars.append([x, y, size, speed])
      lastStarTime = countTime

    for star in stars:
      if star[1] <= HEIGHT:
        star[1] += star[3]
        pygame.draw.circle(WIN, GREY, (star[0], star[1]), star[2])
      else:
        stars.remove(star)

    #---------------

    #ship

    WIN.blit(SPACESHIP, (ship[0], ship[1]))
    if showHitBox == True:
      pygame.draw.rect(WIN, WHITE, pygame.Rect(SHIP.x, SHIP.y, SPACESHIPSIZE[0], SPACESHIPSIZE[1]), 2)

    #---------------

    #ship fire particles

    if random.randint(1, 5) == 1:
      x = random.randint(ship[0] + 5, ship[0] + SPACESHIPSIZE[0] - 5)
      y = ship[1] + SPACESHIPSIZE[1] - 5
      size = 4
      speed = random.randint(int((countTime/20000)+2), int((countTime/20000)+4)) - 1
      timeAlive = 0
      col = RED
      fireParticles.append([x, y, size, speed, timeAlive, col])

    for part in fireParticles:
      part[1] += part[3]
      part[4] += 1
      if part[4] >= 30 and random.randint(1, 5) == 1:
        fireParticles.remove(part)
      elif part[4] >= 20:
        part[5] = YELLOW
      elif part[4] >= 10:
        part[5] = ORANGE
      pygame.draw.rect(WIN, part[5], pygame.Rect(part[0], part[1], part[2], part[2]))

    #---------------

    #health

    pygame.draw.rect(WIN, RED, pygame.Rect(HX, HY, HPWIDTH, HPHEIGHT*MAXHEALTH))
    pygame.draw.rect(WIN, GREEN, pygame.Rect(HX, HY, HPWIDTH, HPHEIGHT*health))

    for i in range(1, MAXHEALTH + 1):
      pygame.draw.rect(WIN, BLACK, pygame.Rect(HX, HY, HPWIDTH, HPHEIGHT * i), 2)

    #---------------

    #score

    text = BIGFONT.render(str(score), 1, WHITE)
    WIN.blit(text, (WIDTH - PADDING - text.get_width(), PADDING))

    #---------------

    #+hp

    if random.randint(1, 1000) == 1:
      x = random.randint(1, WIDTH)
      y = -50
      size = SIZE
      speed = 1
      hpplus.append([x, y, 32, 2])

    for hp in hpplus:
      hp[1] += hp[3]
      HEARTim = pygame.transform.scale(HEART, (hp[2], hp[2]))
      WIN.blit(HEARTim, (hp[0], hp[1]))
      if SHIP.colliderect(pygame.Rect(hp[0], hp[1], hp[2], hp[2])):
        pygame.event.post(pygame.event.Event(HEARTHIT))
        hpplus.remove(hp)
      elif hp[1] >= HEIGHT:
        hpplus.remove(hp)
      if showHitBox == True:
        pygame.draw.rect(WIN, WHITE, pygame.Rect(hp[0], hp[1], hp[2], hp[2]), 2)

    #---------------

    #asteroid

    if countTime >= lastAsteroidTime - (countTime/1000) + DURATION*2:
      balancer = random.randint(1, 10)
      if balancer == 1:
        x = ship[0]
      elif balancer%2 == 0:
        x = random.randint(1, WIDTH)
      else:
        x = random.randint(ship[0] - 200, ship[0] + 200)

      y = -50
      size = random.randint(30, 70)
      speed = random.randint(int((countTime/20000)+2), int((countTime/20000)+4))
      asteroids.append([x, y, size, speed])
      lastAsteroidTime = countTime

    for asteroid in asteroids:
      asteroid[1] += asteroid[3]
      ASTEROIDim = pygame.transform.scale(ASTEROID, (asteroid[2], asteroid[2]))
      WIN.blit(ASTEROIDim, (asteroid[0], asteroid[1]))
      if SHIP.colliderect(pygame.Rect(asteroid[0], asteroid[1], asteroid[2], asteroid[2])):
        pygame.event.post(pygame.event.Event(HIT))
        asteroids.remove(asteroid)
      elif asteroid[1] >= HEIGHT or asteroid[0] <= 0-asteroid[2] or asteroid[0] >= WIDTH:
        asteroids.remove(asteroid)
        score += 1
      if showHitBox == True:
        pygame.draw.rect(WIN, WHITE, pygame.Rect(asteroid[0], asteroid[1], asteroid[2], asteroid[2]), 2)

    #---------------

    #controls

    if showControls == True:
    
      for control in CONTROLS:
        width = ARROWFONT.render("W", 1, WHITE).get_width()
        height = ARROWFONT.render("W", 1, WHITE).get_height()
        cText = control[2].render(control[0], 1, WHITE)
        if control == CONTROLS[1]:
          WIN.blit(cText, (PADDING, HEIGHT - PADDING*(len(CONTROLS)-1) - PADDING - height * CONTROLS.index(control)))
          explainText = FONT.render(control[1], 1, WHITE)
        else:
          WIN.blit(cText, (PADDING, HEIGHT - PADDING*(len(CONTROLS)-1) - height * CONTROLS.index(control)))
          explainText = FONT.render(control[1], 1, WHITE)
        WIN.blit(explainText, (PADDING + width + PADDING*2, HEIGHT - PADDING*(len(CONTROLS)-1) - height * CONTROLS.index(control)))
    else:
      cText = FONT.render("C to show controls", 1, WHITE)
      WIN.blit(cText, (PADDING, HEIGHT - PADDING - cText.get_height()))
      pygame.draw.rect(WIN, WHITE, pygame.Rect(PADDING - 1, HEIGHT - PADDING - 1 - cText.get_height(), cText.get_width(), cText.get_height()), 1)

    #---------------


  pygame.display.flip()
  return lastStarTime, stars, lastAsteroidTime, asteroids, score, hpplus, fireParticles

def shipMove(keys_pressed, ship, SHIP):
  if keys_pressed[pygame.K_LEFT] and ship[0] - VEL > 0: #left
    ship[0] -= VEL
    SHIP.x -= VEL
  elif keys_pressed[pygame.K_a] and ship[0] - MICROVEL > 0: #left
    ship[0] -= MICROVEL
    SHIP.x -= MICROVEL
  if keys_pressed[pygame.K_RIGHT] and ship[0] + SPACESHIPSIZE[0] + VEL < WIDTH: # right
    ship[0] += VEL
    SHIP.x += VEL
  elif keys_pressed[pygame.K_d] and ship[0] + SPACESHIPSIZE[0] + MICROVEL < WIDTH: #right
    ship[0] += MICROVEL
    SHIP.x += MICROVEL
  if keys_pressed[pygame.K_UP] and ship[1] - VEL > 0: #up
    ship[1] -= VEL
    SHIP.y -= VEL
  elif keys_pressed[pygame.K_w] and ship[1] - VEL > 0: #up
    ship[1] -= MICROVEL
    SHIP.y -= MICROVEL
  if keys_pressed[pygame.K_DOWN] and ship[1] + SPACESHIPSIZE[1] + VEL < HEIGHT: # down
    ship[1] += VEL
    SHIP.y += VEL
  elif keys_pressed[pygame.K_s] and ship[1] + SPACESHIPSIZE[1] + MICROVEL < HEIGHT: #down
    ship[1] += MICROVEL
    SHIP.y += MICROVEL
  
  return ship, SHIP

def game():

  file = open("leaderboard.txt", "r")
  fileR = [x.split(", ") for x in file.read().split("\n")[:-1]]
  file.close()

  state = "menu"
  stars = []
  lastStarTime = 0

  score = 0

  asteroids = []
  lastAsteroidTime = 0
  
  ship = [WIDTH/2 - SPACESHIP.get_width()/2, HEIGHT*3/4]
  SHIP = pygame.Rect(ship[0], ship[1], SPACESHIPSIZE[0], SPACESHIPSIZE[1])

  health = MAXHEALTH
  hpplus = []

  fireParticles = []
  pressPlayTime = 0
  refresh = None
  showHitBox = False
  showControls = False
  pause = False
  startPause = 0
  endPause = 0
  timeChange = []
  countTime = 0

  timeChange.append(pygame.time.get_ticks())

  clock = pygame.time.Clock()
  run = True
  while run:
    clock.tick(FPS)
    mouse = pygame.mouse.get_pos()

    if refresh != None:
      refresh += 1

    if refresh == 3:
      state = "fail"
      layout = [[sg.Text('Enter name')], [sg.InputText()], [sg.Submit(), sg.Cancel()]]
      window = sg.Window('Window Title', layout)
      _, values = window.read()
      window.close()
      if values[0] != '':
        fileR.append([values[0], str(score)])
        file = open("leaderboard.txt", "w")
        for i in fileR:
          word = ", ".join(i) + "\n"
          file.write(word)
        file.close()

    while pause == True:
      for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and (state == "game" or state == "pause"):
          if event.key == pygame.K_SPACE:
            pause = False
            state = "game"
            endPause = pygame.time.get_ticks()
            timeChange.append(endPause - startPause)

    if pause == False:
      countTime = pygame.time.get_ticks()
      for ammendment in timeChange:
        countTime -= ammendment

    for event in pygame.event.get():

      if event.type == pygame.QUIT:#quit event
        run = False
        pygame.quit()
        sys.exit()

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_g:
          showHitBox = not showHitBox
        if event.key == pygame.K_c:
          showControls = not showControls
        if event.key == pygame.K_SPACE and state == "game":
          pause = True
          state = "pause"
          startPause = pygame.time.get_ticks()


      if event.type == pygame.MOUSEBUTTONDOWN:
        if state == "menu":
          if (PBX <= mouse[0] <= PBX + PBWIDTH) and (PBY <= mouse[1] <= PBY + PBHEIGHT):
            state = "countdown"
            pressPlayTime = pygame.time.get_ticks()
        elif state == "fail":
          if (RBX <= mouse[0] <= RBX + RBWIDTH) and (RBY <= mouse[1] <= RBY + RBHEIGHT):
            pygame.time.delay(DURATION)
            run = False
          

      if event.type == SETSTATEGAME:
        state = "game"

      if event.type == HIT:
        health -= 1
        HIT_SOUND.play()
        if health == 0:
          refresh = 0


      if event.type == RESTART:
        run = False

      if event.type == HEARTHIT:
        HEART_SOUND.play()
        if health != MAXHEALTH:
          health += 1
          score += 10
        else:
          score += 25

    keys_pressed = pygame.key.get_pressed()
    if state == "game":
      ship, SHIP = shipMove(keys_pressed, ship, SHIP)

    lastStarTime, stars, lastAsteroidTime, asteroids, score, hpplus, fireParticles = drawWindow(state, lastStarTime, stars, ship, lastAsteroidTime, asteroids, pressPlayTime, SHIP, health, score, hpplus, fireParticles, showHitBox, showControls, countTime, fileR)

while True:
  game()