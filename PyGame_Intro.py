import sys, pygame, time

pygame.init()

size = width, height = 1400  , 750
speed = [2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

#ball = pygame.image.load("intro_ball.gif")
ball = pygame.image.load("gerbil_tartar.gif")


ballrect = ball.get_rect()

while 1:
    x = 1
    while x==1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        ballrect = ballrect.move(speed)
        if ballrect.left < 0 or ballrect.right > width:
            speed[0] = -speed[0]
        if ballrect.top < 0 or ballrect.bottom > height:
            speed[1] = -speed[1]


            if ballrect.left == 0 and ballrect.top == 0:
                speed = speed + 0.001
                x=x1

            screen.fill(black)
            screen.blit(ball, ballrect)
            time.sleep(.005)
            pygame.display.flip()