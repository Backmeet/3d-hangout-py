import numpy as np
import pygame
import requests
from engine import Renderer3D

pygame.init()
screen = pygame.display.set_mode((900, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

player_name = input("name?: ")
url = input("Url?: ")

# Notify the server about the new player
requests.post(f"{url}/add-player/{player_name}")

def text(text, pos):
    screen.blit(font.render(text, 1, (255, 255, 255)), pos)

r = Renderer3D((900, 600))
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

camera_speed = 10
rotation_speed = 2

def send_data(name, value_name, amount):
    requests.post(f"{url}/change-value/{name}/{value_name}/{amount}")

r.render_distance = 10000

while True:
    r.Render_3D =  requests.get(f"{url}/get-scene/{player_name}").json().get("scene", [])

    send_data(player_name, "x", r.cPOS[0])
    send_data(player_name, "y", r.cPOS[1])
    send_data(player_name, "z", r.cPOS[2])
    send_data(player_name, "orientation", ','.join(map(str, r.cORENTATION)))

    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            requests.delete(f"{url}/remove-player/{player_name}")
            pygame.quit()
            quit()

    keys = pygame.key.get_pressed()
    forward = np.array([0, 0, 1])
    up = np.array([0, 1, 0])
    right = np.array([1, 0, 0])
    direction_forward = np.dot(r.cached_rotation_matrix, forward)
    direction_up = np.dot(r.cached_rotation_matrix, up)
    direction_right = np.dot(r.cached_rotation_matrix, right)

    if keys[pygame.K_w]: r.cPOS += direction_forward * camera_speed
    if keys[pygame.K_s]: r.cPOS -= direction_forward * camera_speed
    if keys[pygame.K_d]: r.cPOS += direction_right * camera_speed
    if keys[pygame.K_a]: r.cPOS -= direction_right * camera_speed
    if keys[pygame.K_SPACE]: r.cPOS += direction_up * camera_speed
    if keys[pygame.K_LSHIFT]: r.cPOS -= direction_up * camera_speed

    if keys[pygame.K_LEFT]: r.cORENTATION[1] += rotation_speed
    if keys[pygame.K_RIGHT]: r.cORENTATION[1] -= rotation_speed
    if keys[pygame.K_UP]: r.cORENTATION[0] -= rotation_speed
    if keys[pygame.K_DOWN]: r.cORENTATION[0] += rotation_speed

    r.tick()

    for line in r.to_render:
        if line[1][0] and line[1][1]:
            pygame.draw.line(screen, line[2], line[1][0], line[1][1], 1)

    text(f"Position: {r.cPOS}, Orientation: {r.cORENTATION}", (10, 10))
    text(f"FPS {clock.get_fps()}", (10, 40))

    pygame.display.flip()
    clock.tick(30)
