import pygame as pg

class Button:
    """
    A simple clickable button with different states for modern UX.
    """
    def __init__(self, x, y, width, height, text='Button',
                 on_click=None,
                 font_name=None, font_size=30,
                 text_color=(255, 255, 255),
                 normal_color=(100, 100, 100),
                 hover_color=(150, 150, 150),
                 pressed_color=(50, 50, 50),
                 border_radius=5):
        pg.font.init() # Initialize font module if not already done

        self.rect = pg.Rect(x, y, width, height)
        self.text = text
        self.on_click = on_click
        self.font_size = font_size
        self.text_color = text_color
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.pressed_color = pressed_color
        self.border_radius = border_radius

        self.is_hovered = False
        self.is_pressed = False

        # Initialize font
        # Prefer freetype for better rendering if available
        if pg.freetype.get_init():
            self.font = pg.freetype.Font(font_name, self.font_size)
            self.use_freetype = True
        else:
            self.font = pg.font.Font(font_name, self.font_size)
            self.use_freetype = False

        # Fallback to SysFont if specified font_name fails (e.g. None or not found)
        # This needs to be handled carefully as pg.font.Font(None) is valid for default.
        # pg.freetype.Font(None) is not, it needs a path or SysFont.
        if font_name is None: # Using system default
            if self.use_freetype:
                try:
                    self.font = pg.freetype.SysFont(pg.freetype.get_default_font(), self.font_size)
                except Exception as e: # Fallback if even SysFont fails for freetype
                    print(f"Freetype SysFont Error: {e}. Falling back to pg.font.SysFont")
                    pg.font.init() # Ensure pg.font is initialized
                    self.font = pg.font.SysFont(pg.font.get_default_font(), self.font_size)
                    self.use_freetype = False # Can't use freetype if SysFont failed
            else: # pg.font.Font(None, size) is okay
                self.font = pg.font.Font(None, self.font_size)
        else: # Specific font file requested
            try:
                if self.use_freetype:
                    self.font = pg.freetype.Font(font_name, self.font_size)
                else:
                    self.font = pg.font.Font(font_name, self.font_size)
            except pg.error as e:
                print(f"Error loading font '{font_name}': {e}. Using system default font.")
                if self.use_freetype:
                    try:
                        self.font = pg.freetype.SysFont(pg.freetype.get_default_font(), self.font_size)
                    except Exception as e_sys: # Fallback if SysFont fails for freetype
                        print(f"Freetype SysFont Error: {e_sys}. Falling back to pg.font.SysFont")
                        pg.font.init()
                        self.font = pg.font.SysFont(pg.font.get_default_font(), self.font_size)
                        self.use_freetype = False
                else:
                    self.font = pg.font.Font(None, self.font_size) # pg.font's default


    def handle_event(self, event):
        """Handles a single Pygame event to update button state."""
        action_triggered = False
        if event.type == pg.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered:
                self.is_pressed = True
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1 and self.is_pressed: # Was pressed
                self.is_pressed = False
                if self.is_hovered and self.on_click: # Still hovered on release
                    self.on_click()
                    action_triggered = True
        return action_triggered


    def draw(self, surface):
        """Draws the button on the given surface with refined appearance."""
        current_color = self.normal_color
        shadow_offset = 3 # How far the shadow is offset
        current_rect = self.rect
        text_offset_y = 0

        if self.is_pressed:
            current_color = self.pressed_color
            # Simulate button press by slightly moving the button down and to the right
            # This gives a tactile feedback. We'll draw the main rect slightly offset.
            # No shadow needed as it's "pressed in".
            current_rect = self.rect.move(shadow_offset // 2, shadow_offset // 2)
            text_offset_y = shadow_offset // 2

        elif self.is_hovered:
            current_color = self.hover_color
            # Optional: slightly raise the button or make shadow more prominent on hover
            # For now, just color change is fine, shadow is constant unless pressed

        # Draw shadow (a darker version of the button color, or a fixed shadow color)
        # This is drawn only if not pressed
        if not self.is_pressed:
            shadow_color = (max(0, c - 30) for c in self.normal_color[:3]) # Darken normal color
            shadow_rect = self.rect.move(shadow_offset, shadow_offset)
            pg.draw.rect(surface, tuple(shadow_color), shadow_rect, border_radius=self.border_radius)

        # Draw the main button rectangle
        pg.draw.rect(surface, current_color, current_rect, border_radius=self.border_radius)

        # Draw button border (optional, for more definition)
        # border_color = (max(0, c - 50) for c in current_color[:3])
        # pg.draw.rect(surface, tuple(border_color), current_rect, width=2, border_radius=self.border_radius)


        # Render text
        text_render_color = self.text_color
        if self.use_freetype:
            # Freetype's render method can take a background color for antialiasing,
            # but for transparent text, this is fine.
            # For more control, render to a separate surface then blit.
            text_surf, text_render_rect = self.font.render(self.text, text_render_color)
        else:
            text_surf = self.font.render(self.text, True, text_render_color) # True for antialiasing

        text_rect = text_surf.get_rect(center=current_rect.center)
        text_rect.y += text_offset_y # Apply offset if pressed

        surface.blit(text_surf, text_rect)

if __name__ == '__main__':
    pg.init()
    if not pg.freetype.get_init(): # Ensure freetype is initialized if we want to use it
        pg.freetype.init()

    screen_width, screen_height = 800, 600
    screen = pg.display.set_mode((screen_width, screen_height))
    pg.display.set_caption("Button Refinement Test")
    clock = pg.time.Clock()

    def my_button_action():
        print("Button clicked!")

    # Test with default font (None)
    button1 = Button(50, 50, 220, 60, "Click Me (Default Font)",
                     on_click=my_button_action, font_size=22,
                     normal_color=(0, 122, 204), hover_color=(0,142,224), pressed_color=(0,102,184))

    # Test with a specific (likely available) system font for pg.font if freetype fails for it
    # For freetype, it will attempt SysFont. This is tricky because font names differ.
    # 'arial' is common, but not guaranteed. None is safer for cross-platform if no .ttf is bundled.
    test_font_name = None # Keep it simple, rely on system default
    # try:
    #     # This is just to see if a common font name works for basic pg.font.Font
    #     pg.font.Font("arial", 20)
    #     test_font_name = "arial"
    # except pg.error:
    #     test_font_name = None # Fallback to system default if arial not found

    button2 = Button(50, 150, 280, 70, "Another Button (Styled)",
                     on_click=lambda: print("Styled button pressed!"),
                     font_name=test_font_name, font_size=26,
                     text_color=(240,240,240),
                     normal_color=(217, 83, 79), # Bootstrap 'danger' red
                     hover_color=(200, 70, 65),
                     pressed_color=(180, 60, 55),
                     border_radius=10)

    button3 = Button(50, 250, 200, 50, "Small & Rounded",
                     on_click=lambda: print("Small button!"),
                     font_size=18,
                     normal_color=(92, 184, 92), # Bootstrap 'success' green
                     hover_color=(80, 170, 80),
                     pressed_color=(70, 150, 70),
                     border_radius=25) # Very rounded

    all_buttons = [button1, button2, button3]
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            for btn in all_buttons:
                btn.handle_event(event)

        screen.fill((30, 30, 30))
        for btn in all_buttons:
            btn.draw(screen)

        pg.display.flip()
        clock.tick(60)

    pg.quit()
