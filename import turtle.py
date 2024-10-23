import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Massive Color Battle to Uniform Color')

# Colors
WHITE = (255, 255, 255)

# Dot class to handle movement, collision, and color blending
class Dot:
    def __init__(self, x, y, color, radius=2):  # Smaller radius for more dots
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.dx = random.choice([-1, 1]) * random.uniform(1, 2)
        self.dy = random.choice([-1, 1]) * random.uniform(1, 2)

    def move(self):
        self.x += self.dx
        self.y += self.dy
        if self.x - self.radius < 0 or self.x + self.radius > WIDTH:
            self.dx = -self.dx
        if self.y - self.radius < 0 or self.y + self.radius > HEIGHT:
            self.dy = -self.dy

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

    def collide(self, other_dot):
        dist = math.hypot(self.x - other_dot.x, self.y - other_dot.y)
        return dist <= self.radius + other_dot.radius

    def gradually_blend_colors(self, other_dot, blend_factor=0.03):  # Slower blending factor
        r = int(self.color[0] * (1 - blend_factor) + other_dot.color[0] * blend_factor)
        g = int(self.color[1] * (1 - blend_factor) + other_dot.color[1] * blend_factor)
        b = int(self.color[2] * (1 - blend_factor) + other_dot.color[2] * blend_factor)
        return (r, g, b)

# Function to check for collisions and blend colors gradually
def handle_collisions(dots):
    for i in range(len(dots)):
        for j in range(i + 1, len(dots)):
            if dots[i].collide(dots[j]):
                # Gradually blend the colors of the colliding dots
                new_color = dots[i].gradually_blend_colors(dots[j])
                dots[i].color = new_color
                dots[j].color = new_color

# Create initial dots with random positions and colors
def create_dots(num_dots):
    dots = []
    for _ in range(num_dots):
        x = random.randint(50, WIDTH - 50)
        y = random.randint(50, HEIGHT - 50)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        dot = Dot(x, y, color)
        dots.append(dot)
    return dots

# Main loop
def main():
    clock = pygame.time.Clock()
    running = True
    dots = create_dots(5000)  # 5000 small dots for intense battle
    blend_complete = False
    uniform_color = (0, 0, 0)  # Placeholder for the final uniform color

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not blend_complete:
            # Move and draw the dots during the "battle" phase
            for dot in dots:
                dot.move()
                dot.draw(screen)

            # Handle collisions and gradually blend colors
            handle_collisions(dots)

            # Check if all dots have blended into a similar color (within a tolerance)
            first_dot_color = dots[0].color
            all_blended = all(
                math.isclose(dot.color[0], first_dot_color[0], abs_tol=2) and
                math.isclose(dot.color[1], first_dot_color[1], abs_tol=2) and
                math.isclose(dot.color[2], first_dot_color[2], abs_tol=2)
                for dot in dots
            )

            # If all colors are close enough to be considered blended
            if all_blended:
                blend_complete = True
                uniform_color = first_dot_color
        else:
            # Once the colors are blended, fill the entire screen with the final uniform color
            screen.fill(uniform_color)

        pygame.display.flip()
        clock.tick(60)  # Limit FPS

    pygame.quit()

if __name__ == "__main__":
    main()

