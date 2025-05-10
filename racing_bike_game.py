import pygame
import random

# Initialize
pygame.init()
WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🏍️ Racing Bike Game")

# Load images
bike_img = pygame.image.load("bike.png")
bike_img = pygame.transform.scale(bike_img, (50, 90))  # scale to fit

car_img = pygame.image.load("car.png")
car_img = pygame.transform.scale(car_img, (50, 90))

# Game variables
clock = pygame.time.Clock()
FPS = 60
bike_x = WIDTH // 2 - 25
bike_y = HEIGHT - 120
bike_speed = 5

cars = []
score = 0
font = pygame.font.Font(None, 36)
game_over = False

def spawn_car():
    lane_x = random.choice([100, 200, 300])
    car = {"x": lane_x, "y": -100, "speed": random.randint(4, 8)}
    cars.append(car)

def draw_bike(x, y):
    screen.blit(bike_img, (x, y))

def draw_car(car):
    screen.blit(car_img, (car["x"], car["y"]))

def check_collision(bike_rect, car_rect):
    return bike_rect.colliderect(car_rect)

# Main loop
running = True
while running:
    screen.fill((50, 50, 50))  # road color

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # Input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and bike_x > 50:
            bike_x -= bike_speed
        if keys[pygame.K_RIGHT] and bike_x < WIDTH - 100:
            bike_x += bike_speed

        # Spawn cars
        if random.randint(1, 50) == 1:
            spawn_car()

        # Move and draw cars
        for car in cars[:]:
            car["y"] += car["speed"]
            draw_car(car)

            # Collision detection
            bike_rect = pygame.Rect(bike_x, bike_y, 50, 90)
            car_rect = pygame.Rect(car["x"], car["y"], 50, 90)
            if check_collision(bike_rect, car_rect):
                game_over = True

            if car["y"] > HEIGHT:
                cars.remove(car)
                score += 1

        draw_bike(bike_x, bike_y)

        # Display score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
    else:
        over_text = font.render("Game Over! Press R to Restart", True, (255, 0, 0))
        screen.blit(over_text, (WIDTH // 2 - 180, HEIGHT // 2))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            cars.clear()
            bike_x = WIDTH // 2 - 25
            score = 0
            game_over = False

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
