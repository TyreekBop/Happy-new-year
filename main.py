import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Happy New Year Fireworks")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
    (255, 0, 255), (0, 255, 255), (255, 128, 0), (128, 0, 255)
]

# Clock
clock = pygame.time.Clock()

# Firework class
class Firework:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT
        self.target_y = random.randint(150, 300)
        self.color = random.choice(COLORS)
        self.speed = 5
        self.exploded = False
        self.particles = []

    def move(self):
        if self.y > self.target_y:
            self.y -= self.speed
        else:
            self.exploded = True
            self.create_particles()

    def create_particles(self):
        text = "HAPPY NEW YEAR"
        angle_step = (2 * math.pi) / len(text)
        for i, char in enumerate(text):
            angle = i * angle_step
            speed = random.uniform(2, 4)
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            self.particles.append([self.x, self.y, dx, dy, self.color, char])

    def draw(self):
        if not self.exploded:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 5)

    def update_particles(self):
        for particle in self.particles:
            particle[0] += particle[2]
            particle[1] += particle[3]

    def draw_particles(self):
        font = pygame.font.Font(None, 36)
        for particle in self.particles:
            char_surface = font.render(particle[5], True, particle[4])
            screen.blit(char_surface, (particle[0], particle[1]))

# Main loop
fireworks = [Firework()]
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for firework in fireworks[:]:
        if not firework.exploded:
            firework.move()
        else:
            firework.update_particles()

        firework.draw()
        firework.draw_particles()

        # Remove particles if they are out of bounds
        firework.particles = [p for p in firework.particles if 0 <= p[0] <= WIDTH and 0 <= p[1] <= HEIGHT]
        if firework.exploded and not firework.particles:
            fireworks.remove(firework)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
