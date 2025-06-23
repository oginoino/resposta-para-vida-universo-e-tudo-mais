import pygame as pg
from button import Button # Assuming button.py is in the same directory

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

BG_COLOR = (40, 40, 40) # Dark gray
TITLE = "Pygame Modern Button Demo"

# --- Button Callbacks ---
def action_button_1():
    print("Action Button 1 Clicked: Performing an action!")

def action_button_2():
    print("Action Button 2 Clicked: Toggling something maybe?")

def quit_button_action():
    global running
    print("Quit button clicked. Exiting...")
    running = False

# --- Pygame Setup ---
pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption(TITLE)
clock = pg.time.Clock()

# --- Create Buttons ---
# Using freetype should be automatic if available, otherwise Button class falls back.
# For font_name, pass None to use system default, or a path to a .ttf file.
button_font_name = None # Or path to your .ttf file e.g. "arial.ttf"

button1 = Button(
    x=SCREEN_WIDTH // 2 - 125, y=150,
    width=250, height=60,
    text="Perform Action 1",
    on_click=action_button_1,
    font_name=button_font_name, font_size=28,
    text_color=(230, 230, 230),
    normal_color=(0, 122, 204),  # A modern blue
    hover_color=(0, 142, 224),
    pressed_color=(0, 102, 184),
    border_radius=8
)

button2 = Button(
    x=SCREEN_WIDTH // 2 - 125, y=250,
    width=250, height=60,
    text="Toggle Option",
    on_click=action_button_2,
    font_name=button_font_name, font_size=28,
    text_color=(230, 230, 230),
    normal_color=(96, 96, 96),   # A sleek gray
    hover_color=(128, 128, 128),
    pressed_color=(64, 64, 64),
    border_radius=8
)

quit_button = Button(
    x=SCREEN_WIDTH // 2 - 75, y=SCREEN_HEIGHT - 100,
    width=150, height=50,
    text="Quit",
    on_click=quit_button_action,
    font_name=button_font_name, font_size=24,
    text_color=(220, 220, 220),
    normal_color=(202, 81, 0),   # A modern orange/red
    hover_color=(222, 101, 20),
    pressed_color=(182, 61, 0),
    border_radius=6
)

buttons = [button1, button2, quit_button]

# --- Game Loop ---
running = True
while running:
    # Event Handling
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        for btn in buttons:
            btn.handle_event(event)

    # Update (No specific game logic updates in this demo)

    # Draw
    screen.fill(BG_COLOR)
    for btn in buttons:
        btn.draw(screen)

    pg.display.flip()

    # Cap the framerate
    clock.tick(FPS)

# --- Quit Pygame ---
pg.quit()
print("Application closed.")
