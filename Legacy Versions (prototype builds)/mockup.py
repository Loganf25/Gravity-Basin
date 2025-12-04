import pygame
import math
import random
from typing import List, Dict


pygame.init()

#util     *** Variables ***

# Set up the display 
SCREEN_SIZE = (1024, 720)
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Gravity Basin - Solar System Simulation UI Mockup")
clock = pygame.time.Clock()

# Simulation area Constants
SIM_W = 560
SIM_H = 420
SIM_X = 40
SIM_Y = (SCREEN_SIZE[1] - SIM_H) // 2 + 20
CX = SIM_X + SIM_W // 2
CY = SIM_Y + SIM_H // 2

#Colors
COLOR_SPACE_BLACK = (10, 10, 20)
COLOR_STAR = (200, 220, 255)
COLOR_UI_BG = (22, 28, 38, 220)
COLOR_UI_ACCENT = (30, 160, 230)
COLOR_ORBIT = (70, 80, 100)
COLOR_TEXT = (230, 235, 240)
COLOR_LABEL_BG = (0, 0, 0, 120)
COLOR_SUN = (255, 200, 0)
COLOR_MERCURY = (169, 169, 169)
COLOR_VENUS = (218, 165, 32)
COLOR_EARTH = (100, 149, 237)
COLOR_MARS = (188, 39, 50)
COLOR_JUPITER = (210, 180, 140)
COLOR_SATURN = (244, 164, 96)
COLOR_URANUS = (175, 238, 238)
COLOR_NEPTUNE = (72, 61, 139)

#Fonts/Drawing setup
try:
    ui_font = pygame.font.SysFont("Segoe UI", 16)
    title_font = pygame.font.SysFont("Seogoe UI", 20, bold=True)
    small_font = pygame.font.SysFont("Segoe UI", 14)
except:
    print("Error loading fonts. Using default.")
    ui_font = pygame.font.Font(None, 16)
    title_font = pygame.font.Font(None, 24)
    small_font = pygame.font.Font(None, 14)

#           **** HELPER FUNCTIONS ****
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_ui_panel(rect, radius=8):
    s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    s.fill(COLOR_UI_BG)
    screen.blit(s, rect.topleft)

def point_circle(px, py, cx, cy, r):
    return (px - cx) ** 2 + (py - cy) ** 2 <= r * r 


#repo 
# Planets: name, color, orbit_radius, radius_pixels, angle_deg
PLANETS = [
    ("Mercury", COLOR_MERCURY, 60, 6, 260),
    ("Venus", COLOR_VENUS,  95, 9, 200),
    ("Earth", COLOR_EARTH, 130, 11, 140),
    ("Mars", COLOR_MARS,   165, 9, 80),
    ("Jupiter", COLOR_JUPITER, 220, 18, 20),
    ("Saturn",  COLOR_SATURN,  270, 16, 320),
    ("Uranus", COLOR_URANUS, 320, 12, 9),
    ("Neptune", COLOR_NEPTUNE, 370, 12, 7)   ]

# compute scale so all planets fit inside the simulation area (SIM_W x SIM_H)
max_logical_orbit = max(o for (_, _, o, _, _) in PLANETS)
margin = 24
available_radius = min(SIM_W, SIM_H) / 2 - margin
scale = available_radius / max_logical_orbit if max_logical_orbit > 0 else 1.0

planet_states: List[Dict] = []
for name, color, logical_orbit, size, angle_deg in PLANETS:
    angle = math.radians(angle_deg)
    orbit_px = max(8, int(logical_orbit * scale))  
    x = CX + int(math.cos(angle) * orbit_px)
    y = CY + int(math.sin(angle) * orbit_px)
    planet_states.append({
        "name": name,
        "color": color,
        "orbit": logical_orbit,  
        "orbit_px": orbit_px,     
        "radius": size,
        "angle": angle,
        "pos": (x, y),
        "mass": "—",
        "velocity": "—"
    })
selected = None

#Starfield
STAR_COUNT = 220
stars = [(random.randint(SIM_X, SIM_X + SIM_W), random.randint(SIM_Y, SIM_Y + SIM_H), random.choice((1,2))) 
         for _ in range(STAR_COUNT)]

#time control
time_paused = False
time_scale = 1.0
time_seconds = 0.0

#app
run = True
while run:
    dt = clock.tick(60) / 1000.0 
    for event in pygame.event.get():
        #End program check
        if event.type == pygame.QUIT:
            run = False
        #Planet click check
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            # check planet clicks
            sel = None
            for i, st in enumerate(planet_states):
                x, y = st["pos"]
                if point_circle(mx, my, x, y, st["radius"] + 6):
                    sel = i
                    break
            selected = sel

    #Fill background
    screen.fill(COLOR_SPACE_BLACK)

    # Draw simulation area background panel
    sim_rect = pygame.Rect(SIM_X - 6, SIM_Y - 6, SIM_W + 12, SIM_H + 12)
    pygame.draw.rect(screen, (14, 18, 28), sim_rect, border_radius=10)
    # Starfield
    for sx, sy, r in stars:
        pygame.draw.circle(screen, COLOR_STAR, (sx, sy), r)

    # Orbits and sun
    for st in planet_states:
        pygame.draw.circle(screen, COLOR_ORBIT, (CX, CY), st["orbit_px"], 1)
    pygame.draw.circle(screen, COLOR_SUN, (CX, CY), 28)

    # Draw planets (static positions)
    for i, st in enumerate(planet_states):
        x, y = st["pos"]
        # subtle halo behind planet for depth
        halo = pygame.Surface((st["radius"]*6, st["radius"]*6), pygame.SRCALPHA)
        pygame.draw.circle(halo, (*st["color"], 28), (halo.get_width()//2, halo.get_height()//2), int(st["radius"]*3))
        screen.blit(halo, (x - halo.get_width()//2, y - halo.get_height()//2))
        #Planet
        pygame.draw.circle(screen, st["color"], (x, y), st["radius"])
        # highlight if selected
        if selected == i:
            pygame.draw.circle(screen, COLOR_UI_ACCENT, (x, y), st["radius"] + 6, 2)

    # Settings button above right toolbar
    settings_rect = pygame.Rect(SIM_X + SIM_W + 195, SIM_Y - 30, 45, 45)
    draw_ui_panel(settings_rect)
    # Right toolbar
    toolbar_rect = pygame.Rect(SIM_X + SIM_W + 18, SIM_Y + 40, 220, 140)
    draw_ui_panel(toolbar_rect)
    draw_text("Controls", title_font, COLOR_TEXT, toolbar_rect.x + 12, toolbar_rect.y + 10)
    draw_text("[ ] Toggle Orbits", ui_font, COLOR_TEXT, toolbar_rect.x + 12, toolbar_rect.y + 44)
    draw_text("[ ] Toggle Labels", ui_font, COLOR_TEXT, toolbar_rect.x + 12, toolbar_rect.y + 66)
    draw_text("Zoom / Pan", ui_font, COLOR_TEXT, toolbar_rect.x + 12, toolbar_rect.y + 96)

    # Bottom info panel
    info_rect = pygame.Rect(SIM_X + 40, SIM_Y + SIM_H + 6, SIM_W - 80, 100)
    draw_ui_panel(info_rect)
    if selected is None:
        draw_text("No selection", title_font, COLOR_TEXT, info_rect.x + 12, info_rect.y + 8)
        draw_text("Click a planet to inspect its properties", ui_font, COLOR_TEXT, info_rect.x + 12, info_rect.y + 40)
    else:
        st = planet_states[selected]
        draw_text(st["name"], title_font, COLOR_TEXT, info_rect.x + 12, info_rect.y + 8)
        draw_text(f"Orbit radius: {st['orbit']} px", ui_font, COLOR_TEXT, info_rect.x + 12, info_rect.y + 40)
        draw_text(f"Radius: {st['radius']} px", ui_font, COLOR_TEXT, info_rect.x + 220, info_rect.y + 40)
        draw_text("Mass: " + st.get("mass", "—"), ui_font, COLOR_TEXT, info_rect.x + 12, info_rect.y + 64)

    # Title/top-left label
    draw_text("GRAVITY BASIN — Mockup", title_font, COLOR_TEXT, SIM_X + 185, SIM_Y - 36)
    time_panel_rect = pygame.Rect(SIM_X, SIM_Y - 62, SIM_W, 48)
    btn_play_rect = pygame.Rect(time_panel_rect.x + 12, time_panel_rect.y + 8, 36, 32)
    btn_minus_rect = pygame.Rect(btn_play_rect.right + 8, btn_play_rect.y, 36, 32)
    btn_plus_rect = pygame.Rect(btn_minus_rect.right + 8, btn_minus_rect.y, 36, 32)
    draw_ui_panel(time_panel_rect)
    # draw buttons
    pygame.draw.rect(screen, (40,40,48), btn_play_rect, border_radius=6)
    draw_text("⏵" if time_paused else "⏸", title_font, COLOR_TEXT, btn_play_rect.x + 8, btn_play_rect.y + 4)  # inverted icon: show play when paused
    pygame.draw.rect(screen, (40,40,48), btn_minus_rect, border_radius=6)
    draw_text("−", title_font, COLOR_TEXT, btn_minus_rect.x + 10, btn_minus_rect.y + 4)
    pygame.draw.rect(screen, (40,40,48), btn_plus_rect, border_radius=6)
    draw_text("+", title_font, COLOR_TEXT, btn_plus_rect.x + 10, btn_plus_rect.y + 4)
    # show current time scale and paused state
    ts_label = f"Scale: {time_scale}x"
    ps_label = "Paused" if time_paused else "Running"
    draw_text(ts_label, ui_font, COLOR_TEXT, time_panel_rect.right - 160, time_panel_rect.y + 12)
    draw_text(ps_label, ui_font, COLOR_TEXT, time_panel_rect.right - 76, time_panel_rect.y + 12)

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()