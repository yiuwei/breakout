import pygame
import random

pygame.init()

width = 600
height = 550

# Create paddle class
class Paddle:
    def __init__(self):
        self.width = 100
        self.height = 15
        self.x = (width - self.width) // 2
        self.y = height - 60
        self.speed = 8
        self.color = (0, 152, 255)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def position(self, position):
        if position == "left" and self.x - self.speed > 0:
            self.x -= self.speed
        if position == "right" and self.x + self.speed + self.width < width:
            self.x += self.speed
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, display):
        pygame.draw.rect(display, self.color, self.rect)

# Create ball class
class Ball:
    def __init__(self):
        self.radius = 10
        self.x = width // 2
        self.y = height // 2
        self.color = (255, 0, 0)
        self.i = random.choice([-3, 4])
        self.j = -5

    def position(self):
        self.x += self.i
        self.y += self.j
        if self.x - self.radius < 0 or self.x + self.radius > width:
            self.i = -self.i
        if self.y - self.radius < 0:
            self.j = -self.j

    def draw(self, display):
        pygame.draw.circle(display, self.color, (self.x, self.y), self.radius)

# Create brick class
class Brick:
    def __init__(self, x, y):
        self.width = 62
        self.height = 20
        self.x = x
        self.y = y
        self.color = random.choice([(0, 150, 255), (255, 0, 0), (255, 165, 0)])
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, display):
        pygame.draw.rect(display, self.color, self.rect)

def add_items(i, j):
    bricks = []
    for row in range(i):
        for col in range(j):
            brick = Brick(col * (width // j), row * 22)
            bricks.append(brick)
    return bricks

# Define main function
def main():
    display = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Breakout Game")

    font = pygame.font.SysFont('Calibri', 26, bold=1)
    background_font = pygame.font.SysFont('Calibri', 50, bold=1)

    def restart():
        paddle = Paddle()
        ball = Ball()
        bricks = add_items(6, 9)
        total_score = 0
        return paddle, ball, bricks, total_score

    paddle, ball, bricks, total_score = restart()
    clock = pygame.time.Clock()
    running = True
    game_ended = False 

    while running:
        display.fill((50, 50, 50))
        
        # Return output if the game has not ended
        if not game_ended:
            title = background_font.render("Breakout Game", True, (200, 200, 200))
            display.blit(title, (width // 2 - title.get_width() // 2, height // 2 - title.get_height() // 2))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            text = pygame.key.get_pressed()
            if text[pygame.K_LEFT]:
                paddle.position("left")
            if text[pygame.K_RIGHT]:
                paddle.position("right")

            ball.position()

            if ball.y + ball.radius > height:
                game_ended = True

            if paddle.rect.collidepoint(ball.x, ball.y + ball.radius):
                ball.j = -ball.j

            for brick in bricks[:]: 
                if brick.rect.collidepoint(ball.x, ball.y - ball.radius):
                    ball.j = -ball.j
                    bricks.remove(brick)
                    total_score += 1

            if not bricks:
                game_ended = True

        # Return output when the game has ended
        if game_ended:
            end_text = font.render("Game Over!", True, (255, 0, 255)) if ball.y + ball.radius > height else font.render("You Win!", True, (255, 255, 255))
            display.blit(end_text, (width // 2 - end_text.get_width() // 2, height // 2 - end_text.get_height() // 2))
            prompt_text = font.render("Enter R to restart and E to end", True, (1, 205, 240))
            display.blit(prompt_text, (width // 2 - prompt_text.get_width() // 2, height // 2 + 30))

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        paddle, ball, bricks, total_score = restart()
                        game_ended = False
                    elif event.key == pygame.K_e:
                        running = False
                
        paddle.draw(display)
        ball.draw(display)
        for brick in bricks:
            brick.draw(display)

        # Display total points
        text = font.render(f"Points: {total_score}", True, (225, 225, 225))
        display.blit(text, (width - text.get_width() - 10, height - 35))

        pygame.display.flip() 
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
