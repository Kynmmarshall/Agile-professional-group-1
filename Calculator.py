import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 610
BUTTON_SIZE = 80
BUTTON_MARGIN = 10
DISPLAY_HEIGHT = 120
BACKGROUND_COLOR = (30, 30, 40)
DISPLAY_COLOR = (20, 20, 30)
BUTTON_COLOR = (50, 50, 70)
BUTTON_HOVER_COLOR = (70, 70, 90)
OPERATOR_COLOR = (255, 140, 0)
OPERATOR_HOVER_COLOR = (255, 165, 50)
SPECIAL_COLOR = (100, 100, 120)
SPECIAL_HOVER_COLOR = (120, 120, 140)
TEXT_COLOR = (255, 255, 255)
ERROR_COLOR = (255, 50, 50)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Basic Calculator")
clock = pygame.time.Clock()

# Fonts
display_font = pygame.font.SysFont('Arial', 40)
button_font = pygame.font.SysFont('Arial', 28)
small_font = pygame.font.SysFont('Arial', 20)

# Calculator state
current_input = ""
previous_input = ""
current_operator = ""
result = None
error_message = ""

# Button layout following Agile project specifications
buttons = [
    # Row 1: Special buttons
    {"label": "C", "rect": pygame.Rect(BUTTON_MARGIN, DISPLAY_HEIGHT + BUTTON_MARGIN, BUTTON_SIZE * 2 + BUTTON_MARGIN, BUTTON_SIZE), 
     "color": SPECIAL_COLOR, "hover_color": SPECIAL_HOVER_COLOR, "type": "clear"},
    {"label": "Del", "rect": pygame.Rect(BUTTON_MARGIN * 3 + BUTTON_SIZE * 2, DISPLAY_HEIGHT + BUTTON_MARGIN, BUTTON_SIZE, BUTTON_SIZE), 
     "color": SPECIAL_COLOR, "hover_color": SPECIAL_HOVER_COLOR, "type": "backspace"},
    {"label": "/", "rect": pygame.Rect(BUTTON_MARGIN * 5 + BUTTON_SIZE * 3, DISPLAY_HEIGHT + BUTTON_MARGIN, BUTTON_SIZE, BUTTON_SIZE), 
     "color": OPERATOR_COLOR, "hover_color": OPERATOR_HOVER_COLOR, "type": "operator"},
    
    # Row 2: 7, 8, 9, ×
    {"label": "7", "rect": pygame.Rect(BUTTON_MARGIN, DISPLAY_HEIGHT + BUTTON_MARGIN * 2 + BUTTON_SIZE, BUTTON_SIZE, BUTTON_SIZE), 
     "color": BUTTON_COLOR, "hover_color": BUTTON_HOVER_COLOR, "type": "number"},
    {"label": "8", "rect": pygame.Rect(BUTTON_MARGIN * 2 + BUTTON_SIZE, DISPLAY_HEIGHT + BUTTON_MARGIN * 2 + BUTTON_SIZE, BUTTON_SIZE, BUTTON_SIZE), 
     "color": BUTTON_COLOR, "hover_color": BUTTON_HOVER_COLOR, "type": "number"},
    {"label": "9", "rect": pygame.Rect(BUTTON_MARGIN * 3 + BUTTON_SIZE * 2, DISPLAY_HEIGHT + BUTTON_MARGIN * 2 + BUTTON_SIZE, BUTTON_SIZE, BUTTON_SIZE), 
     "color": BUTTON_COLOR, "hover_color": BUTTON_HOVER_COLOR, "type": "number"},
    {"label": "x", "rect": pygame.Rect(BUTTON_MARGIN * 5 + BUTTON_SIZE * 3, DISPLAY_HEIGHT + BUTTON_MARGIN * 2 + BUTTON_SIZE, BUTTON_SIZE, BUTTON_SIZE), 
     "color": OPERATOR_COLOR, "hover_color": OPERATOR_HOVER_COLOR, "type": "operator"},
    
    # Row 3: 4, 5, 6, -
    {"label": "4", "rect": pygame.Rect(BUTTON_MARGIN, DISPLAY_HEIGHT + BUTTON_MARGIN * 3 + BUTTON_SIZE * 2, BUTTON_SIZE, BUTTON_SIZE), 
     "color": BUTTON_COLOR, "hover_color": BUTTON_HOVER_COLOR, "type": "number"},
    {"label": "5", "rect": pygame.Rect(BUTTON_MARGIN * 2 + BUTTON_SIZE, DISPLAY_HEIGHT + BUTTON_MARGIN * 3 + BUTTON_SIZE * 2, BUTTON_SIZE, BUTTON_SIZE), 
     "color": BUTTON_COLOR, "hover_color": BUTTON_HOVER_COLOR, "type": "number"},
    {"label": "6", "rect": pygame.Rect(BUTTON_MARGIN * 3 + BUTTON_SIZE * 2, DISPLAY_HEIGHT + BUTTON_MARGIN * 3 + BUTTON_SIZE * 2, BUTTON_SIZE, BUTTON_SIZE), 
     "color": BUTTON_COLOR, "hover_color": BUTTON_HOVER_COLOR, "type": "number"},
    {"label": "-", "rect": pygame.Rect(BUTTON_MARGIN * 5 + BUTTON_SIZE * 3, DISPLAY_HEIGHT + BUTTON_MARGIN * 3 + BUTTON_SIZE * 2, BUTTON_SIZE, BUTTON_SIZE), 
     "color": OPERATOR_COLOR, "hover_color": OPERATOR_HOVER_COLOR, "type": "operator"},
    
    # Row 4: 1, 2, 3, +
    {"label": "1", "rect": pygame.Rect(BUTTON_MARGIN, DISPLAY_HEIGHT + BUTTON_MARGIN * 4 + BUTTON_SIZE * 3, BUTTON_SIZE, BUTTON_SIZE), 
     "color": BUTTON_COLOR, "hover_color": BUTTON_HOVER_COLOR, "type": "number"},
    {"label": "2", "rect": pygame.Rect(BUTTON_MARGIN * 2 + BUTTON_SIZE, DISPLAY_HEIGHT + BUTTON_MARGIN * 4 + BUTTON_SIZE * 3, BUTTON_SIZE, BUTTON_SIZE), 
     "color": BUTTON_COLOR, "hover_color": BUTTON_HOVER_COLOR, "type": "number"},
    {"label": "3", "rect": pygame.Rect(BUTTON_MARGIN * 3 + BUTTON_SIZE * 2, DISPLAY_HEIGHT + BUTTON_MARGIN * 4 + BUTTON_SIZE * 3, BUTTON_SIZE, BUTTON_SIZE), 
     "color": BUTTON_COLOR, "hover_color": BUTTON_HOVER_COLOR, "type": "number"},
    {"label": "+", "rect": pygame.Rect(BUTTON_MARGIN * 5 + BUTTON_SIZE * 3, DISPLAY_HEIGHT + BUTTON_MARGIN * 4 + BUTTON_SIZE * 3, BUTTON_SIZE, BUTTON_SIZE), 
     "color": OPERATOR_COLOR, "hover_color": OPERATOR_HOVER_COLOR, "type": "operator"},
    
    # Row 5: 0, ., =
    {"label": "0", "rect": pygame.Rect(BUTTON_MARGIN, DISPLAY_HEIGHT + BUTTON_MARGIN * 5 + BUTTON_SIZE * 4, BUTTON_SIZE * 2 + BUTTON_MARGIN, BUTTON_SIZE), 
     "color": BUTTON_COLOR, "hover_color": BUTTON_HOVER_COLOR, "type": "number"},
    {"label": ".", "rect": pygame.Rect(BUTTON_MARGIN * 3 + BUTTON_SIZE * 2, DISPLAY_HEIGHT + BUTTON_MARGIN * 5 + BUTTON_SIZE * 4, BUTTON_SIZE, BUTTON_SIZE), 
     "color": BUTTON_COLOR, "hover_color": BUTTON_HOVER_COLOR, "type": "decimal"},
    {"label": "=", "rect": pygame.Rect(BUTTON_MARGIN * 5 + BUTTON_SIZE * 3, DISPLAY_HEIGHT + BUTTON_MARGIN * 5 + BUTTON_SIZE * 4, BUTTON_SIZE, BUTTON_SIZE), 
     "color": OPERATOR_COLOR, "hover_color": OPERATOR_HOVER_COLOR, "type": "equals"},
]

def draw_display():
    """Draw the calculator display area"""
    # Display background
    pygame.draw.rect(screen, DISPLAY_COLOR, (0, 0, SCREEN_WIDTH, DISPLAY_HEIGHT))
    
    # Previous input (smaller, at top)
    if previous_input:
        prev_text = small_font.render(previous_input + (" " + current_operator if current_operator else ""), True, (150, 150, 150))
        screen.blit(prev_text, (20, 20))
    
    # Current input or result (larger, centered vertically)
    display_text = current_input if not error_message else error_message
    text_color = ERROR_COLOR if error_message else TEXT_COLOR
    
    # Render text with word wrapping if too long
    if len(display_text) > 20:
        display_text = display_text[:20] + "..."
    
    text_surface = display_font.render(display_text, True, text_color)
    
    # Right-align text
    text_rect = text_surface.get_rect()
    text_rect.right = SCREEN_WIDTH - 20
    text_rect.centery = DISPLAY_HEIGHT // 2 + 10
    screen.blit(text_surface, text_rect)
    
    # Draw separator line
    pygame.draw.line(screen, (60, 60, 80), (0, DISPLAY_HEIGHT), (SCREEN_WIDTH, DISPLAY_HEIGHT), 2)

def draw_buttons():
    """Draw all calculator buttons"""
    mouse_pos = pygame.mouse.get_pos()
    
    for button in buttons:
        # Check if mouse is hovering over button
        is_hover = button["rect"].collidepoint(mouse_pos)
        color = button["hover_color"] if is_hover else button["color"]
        
        # Draw button
        pygame.draw.rect(screen, color, button["rect"], border_radius=10)
        
        # Draw button label
        text_surface = button_font.render(button["label"], True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=button["rect"].center)
        screen.blit(text_surface, text_rect)

def draw_title():
    """Draw project title"""
    title_font = pygame.font.SysFont('Arial', 24, bold=True)
    title = title_font.render("Basic Calculator", True, (220, 220, 255))
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT - 30))

def handle_button_click(button):
    """Handle button click events"""
    global current_input, previous_input, current_operator, result, error_message
    
    button_type = button["type"]
    button_label = button["label"]
    
    # Clear error message when new input starts
    if error_message and button_type != "clear":
        error_message = ""
    
    if button_type == "number":
        current_input += button_label
    
    elif button_type == "operator":
        if current_input:
            if previous_input and current_operator:
                # Calculate previous operation first
                calculate_result()
                if error_message:
                    return
                previous_input = str(result) if result is not None else ""
            else:
                previous_input = current_input
            
            current_operator = button_label
            current_input = ""
    
    elif button_type == "decimal":
        if "." not in current_input:
            if not current_input:
                current_input = "0."
            else:
                current_input += "."
    
    elif button_type == "equals":
        if previous_input and current_operator and current_input:
            calculate_result()
            if not error_message:
                previous_input = ""
                current_operator = ""
    
    elif button_type == "clear":
        current_input = ""
        previous_input = ""
        current_operator = ""
        result = None
        error_message = ""
    
    elif button_type == "backspace":
        if current_input:
            current_input = current_input[:-1]
        elif error_message:
            error_message = ""

def calculate_result():
    """Perform the calculation based on current inputs"""
    global current_input, result, error_message
    
    try:
        num1 = float(previous_input)
        num2 = float(current_input)
        
        if current_operator == "+":
            result = num1 + num2
        elif current_operator == "-":
            result = num1 - num2
        elif current_operator == "x":
            result = num1 * num2
        elif current_operator == "/":
            if num2 == 0:
                error_message = "Error: Division by 0"
                return
            result = num1 / num2
        
        # Format result (remove trailing .0 if integer)
        if result.is_integer():
            current_input = str(int(result))
        else:
            current_input = str(round(result, 10)).rstrip('0').rstrip('.')
    
    except ValueError:
        error_message = "Error: Invalid input"
    except Exception as e:
        error_message = f"Error: {str(e)}"

def handle_keyboard_input(event):
    """Handle keyboard input events"""
    global current_input, previous_input, current_operator, error_message
    
    # Clear error message on new input
    if error_message and event.unicode not in ['c', 'C']:
        error_message = ""
    
    # Numbers
    if event.unicode in "0123456789":
        current_input += event.unicode
    
    # Decimal point
    elif event.unicode == ".":
        if "." not in current_input:
            if not current_input:
                current_input = "0."
            else:
                current_input += "."
    
    # Operators
    elif event.unicode == "+":
        if current_input:
            previous_input = current_input
            current_operator = "+"
            current_input = ""
    
    elif event.unicode == "-":
        if current_input:
            previous_input = current_input
            current_operator = "-"
            current_input = ""
    
    elif event.unicode == "*":
        if current_input:
            previous_input = current_input
            current_operator = "×"
            current_input = ""
    
    elif event.unicode == "/":
        if current_input:
            previous_input = current_input
            current_operator = "÷"
            current_input = ""
    
    # Equals or Enter
    elif event.unicode == "=" or event.key == pygame.K_RETURN:
        if previous_input and current_operator and current_input:
            calculate_result()
            if not error_message:
                previous_input = ""
                current_operator = ""
    
    # Clear (C or Delete)
    elif event.unicode.lower() == "c" or event.key == pygame.K_DELETE:
        current_input = ""
        previous_input = ""
        current_operator = ""
        error_message = ""
    
    # Backspace
    elif event.key == pygame.K_BACKSPACE:
        if current_input:
            current_input = current_input[:-1]
        elif error_message:
            error_message = ""

# Main game loop
def main():
    running = True
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Mouse click events
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    for button in buttons:
                        if button["rect"].collidepoint(mouse_pos):
                            handle_button_click(button)
                            break
            
            # Keyboard events
            elif event.type == pygame.KEYDOWN:
                handle_keyboard_input(event)
        
        # Draw everything
        screen.fill(BACKGROUND_COLOR)
        draw_display()
        draw_buttons()
        draw_title()
        
        # Update display
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()