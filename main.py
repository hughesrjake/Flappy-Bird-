import pygame
import random

# initialize pygame
pygame.init()

# game constants
screenWidth, screenHeight = 900, 600
birdWidth, birdHeight = 90, 90  # correct to file size
obsWidth, obsHeight = 80, 280  # correct to file size
flyStrength = -10
appliedGravity = 0.4
fps = 60
obsGap = 150  # gap between the top and bottom obstacles
topObsOffset = 70  # lowered offset for the top obstacle

screen = pygame.display.set_mode((screenWidth, screenHeight))  # init screen
pygame.display.set_caption("Flappy Bird")

# load images
birdImage = pygame.image.load('bird.png')
obsImage = pygame.image.load('pipe.png')
obsImageFlipped = pygame.transform.flip(obsImage, False, True)  # top obstacle img

# font for scoring
font = pygame.font.SysFont(None, 40)

# user sprite
class User:
    def __init__(self):
        self.x = 50
        self.y = screenHeight / 2  # y-axis as close to middle (based on screen size)
        self.velocity = 0

    def draw(self, surface):
        surface.blit(birdImage, (self.x, self.y))  # draw bird at initialized x,y

    def update(self):
        self.velocity += appliedGravity  # update slowly makes velocity negative
        self.y += self.velocity  # y-axis updates upward or downward depending on velocity

    def fly(self):
        self.velocity = flyStrength  # reset velocity to fly upward

class Obstacle:
    def __init__(self):
        self.x = screenWidth  # initialize to the farthest right point
        self.height = random.randint(100, screenHeight - 250)  # top of the bottom obstacle
        self.passed = False  # check if the obstacle has been passed

    def draw(self, surface):
        surface.blit(obsImageFlipped, (self.x, -300 + topObsOffset))  # draw the top obstacle lower
        surface.blit(obsImage, (self.x, self.height + obsGap))  # draw the bottom obstacle

    def update(self):
        self.x -= 8  # move left

def main():
    clock = pygame.time.Clock()
    user = User()
    obstacles = []
    score = 0
    running = True
    last_obs_time = pygame.time.get_ticks()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # fly when space is pressed
                user.fly()
            if event.type == pygame.QUIT:  # quit
                running = False

        user.update()
        current_time = pygame.time.get_ticks()
        if current_time - last_obs_time > 1500:  # time between each obstacle
            obstacles.append(Obstacle())
            last_obs_time = current_time

        # create obstacles
        for obstacle in obstacles:
            obstacle.update()

        # check for collisions
        if user.y > screenHeight or user.y < 0:
            running = False  # user dies

        for obstacle in obstacles:  # collision handling
            if (user.x + birdWidth > obstacle.x and user.x < obstacle.x + obsWidth):
                # collision check for the top obstacle
                if user.y < -300 + topObsOffset + 300 and user.y + birdHeight > -300 + topObsOffset:
                    running = False  # died on top obstacle

                # collision check for the bottom obstacle
                if user.y + birdHeight > obstacle.height + obsGap:
                    running = False  # died on bottom obstacle

            # score counting
            if obstacle.x + obsWidth < user.x and not obstacle.passed:
                score += 1
                obstacle.passed = True  # successful obstacle clear

        obstacles = [obstacle for obstacle in obstacles if obstacle.x > -50]  # remove once off screen

        # draw
        screen.fill((0, 0, 0))
        user.draw(screen)

        for obstacle in obstacles:
            obstacle.draw(screen)

        # score rendering
        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(fps)

if __name__ == "__main__":
    main()