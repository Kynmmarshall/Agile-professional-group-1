import pygame
import sys
import json
import os
from datetime import datetime

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 600  # Increased height for context panel
BUTTON_SIZE = 80
BUTTON_MARGIN = 10
DISPLAY_HEIGHT = 120
CONTEXT_PANEL_HEIGHT = 180
BACKGROUND_COLOR = (25, 30, 40)
DISPLAY_COLOR = (20, 25, 35)
BUTTON_COLOR = (50, 55, 75)
BUTTON_HOVER_COLOR = (70, 75, 95)
CONTEXT_COLOR = (40, 45, 65)
CONTEXT_HOVER_COLOR = (60, 65, 85)
OPERATOR_COLOR = (255, 140, 0)
OPERATOR_HOVER_COLOR = (255, 165, 50)
SPECIAL_COLOR = (100, 105, 130)
SPECIAL_HOVER_COLOR = (120, 125, 150)
TEXT_COLOR = (255, 255, 255)
ERROR_COLOR = (255, 50, 50)
SUCCESS_COLOR = (50, 255, 100)
HINT_COLOR = (255, 215, 0)

# Context modes with specific colors and features
CONTEXT_MODES = {
    "Standard": {
        "color": (70, 70, 90),
        "buttons": ["C", "Del", "/", "×", "-", "+", "=", "."],
        "description": "Basic arithmetic operations"
    },
    "Homework": {
        "color": (60, 100, 180),
        "buttons": ["C", "Del", "√", "x²", "π", "sin", "cos", "tan"],
        "description": "Math homework and studies"
    },
    "Shopping": {
        "color": (40, 160, 80),
        "buttons": ["C", "Del", "%", "Tax", "Tip", "Split", "Save", "Total"],
        "description": "Shopping and expenses"
    },
    "Budgeting": {
        "color": (180, 100, 60),
        "buttons": ["C", "Del", "%", "Avg", "Inc", "Dec", "Save", "Goal"],
        "description": "Personal budgeting"
    },
    "Cooking": {
        "color": (200, 120, 50),
        "buttons": ["C", "Del", "½", "⅓", "¼", "2×", "3×", "°C/°F"],
        "description": "Cooking and recipes"
    }
}

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Smart Context-Aware Calculator")
clock = pygame.time.Clock()

# Fonts
display_font = pygame.font.SysFont('Arial', 40)
button_font = pygame.font.SysFont('Arial', 26)
small_font = pygame.font.SysFont('Arial', 18)
context_font = pygame.font.SysFont('Arial', 16, bold=True)
hint_font = pygame.font.SysFont('Arial', 14)

# Calculator state
current_input = ""
previous_input = ""
current_operator = ""
result = None
error_message = ""
current_context = "Standard"
context_history = []  # Track user patterns
smart_suggestions = []  # Current smart suggestions
last_calculation_time = 0
calculation_pattern = []  # Track recent calculation patterns

# Context data storage
CONTEXT_FILE = "context_data.json"

def load_context_data():
    """Load context patterns and preferences"""
    if os.path.exists(CONTEXT_FILE):
        try:
            with open(CONTEXT_FILE, 'r') as f:
                return json.load(f)
        except:
            return {"patterns": {}, "mode_usage": {}, "preferences": {}}
    return {"patterns": {}, "mode_usage": {}, "preferences": {}}

def save_context_data(data):
    """Save context data"""
    with open(CONTEXT_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def detect_context_pattern():
    """Analyze current calculation to detect context"""
    global smart_suggestions, current_context
    
    # Analyze current input pattern
    if current_input and previous_input:
        # Pattern detection for different contexts
        
        # Shopping/Tipping pattern
        if "Tip" in calculation_pattern or ("+" in calculation_pattern and float(current_input) < 100):
            if current_context != "Shopping":
                current_context = "Shopping"
                smart_suggestions = ["15%", "18%", "20%", "Split Bill"]
        
        # Percentage calculations
        elif "%" in current_operator or ("/" in calculation_pattern and "100" in calculation_pattern):
            if current_context != "Budgeting":
                current_context = "Budgeting"
                smart_suggestions = ["Increase by %", "Decrease by %", "Average", "Savings"]
        
        # Fraction/decimal patterns (cooking)
        elif "." in current_input or any(x in current_input for x in ["0.25", "0.33", "0.5", "0.75"]):
            if current_context != "Cooking":
                current_context = "Cooking"
                smart_suggestions = ["Double", "Half", "Convert Units", "°C to °F"]
        
        # Complex math patterns (homework)
        elif any(op in calculation_pattern for op in ["sin", "cos", "tan", "√", "^"]):
            if current_context != "Homework":
                current_context = "Homework"
                smart_suggestions = ["π", "e", "Solve", "Graph"]
    
    # Time-based context switching
    current_hour = datetime.now().hour
    if 8 <= current_hour <= 14 and current_context == "Standard":
        current_context = "Homework"
        smart_suggestions = ["Study mode activated"]
    elif 16 <= current_hour <= 20 and current_context == "Standard":
        current_context = "Shopping"
        smart_suggestions = ["Evening shopping mode"]

def update_context_history(operation):
    """Update history of operations for pattern recognition"""
    context_history.append({
        "operation": operation,
        "time": datetime.now().isoformat(),
        "context": current_context,
        "input": current_input[:10] if current_input else ""
    })
    
    # Keep only last 20 operations
    if len(context_history) > 20:
        context_history.pop(0)
    
    # Update pattern detection
    calculation_pattern.append(operation)
    if len(calculation_pattern) > 5:
        calculation_pattern.pop(0)
    
    # Save to file
    data = load_context_data()
    if current_context not in data["mode_usage"]:
        data["mode_usage"][current_context] = 0
    data["mode_usage"][current_context] += 1
    save_context_data(data)

# Dynamic button layout based on context
def get_buttons_for_context():
    """Generate buttons based on current context"""
    base_buttons = []
    
    # Common number buttons (always present)
    numbers = [
        {"label": "7", "rect": pygame.Rect(BUTTON_MARGIN, DISPLAY_HEIGHT + CONTEXT_PANEL_HEIGHT + BUTTON_MARGIN, BUTTON_SIZE, BUTTON_SIZE), 
         "color": BUTTON_COLOR, "hover_color": BUTTON_HOVER_COLOR, "type": "number"},
        {"label": "8", "rect": pygame.Rect(BUTTON_MARGIN * 2 + BUTTON_SIZE, DISPLAY_HEIGHT + CONTEXT_PANEL_HEIGHT + BUTTON_MARGIN, BUTTON_SIZE, BUTTON_SIZE), 
         "color": BUTTON_COLOR, "hover_color": BUTTON_HOVER_COLOR, "type": "number"},
        {"label": "9", "rect": pygame.Rect(BUTTON_MARGIN * 3 + BUTTON_SIZE * 2, DISPLAY_HEIGHT + CONTEXT_PANEL_HEIGHT + BUTTON_MARGIN, BUTTON_SIZE, BUTTON_SIZE), 
         "color": BUTTON_COLOR, "hover_color": BUTTON_HOVER_COLOR, "type": "number"},
        {"label": "4", "rect": pygame.Rect(BUTTON_MARGIN, DISPLAY_HEIGHT + CONTEXT_PANEL_HEIGHT + BUTTON_MARGIN * 2 + BUTTON_SIZE, BUTTON_SIZE, BUTTON_SIZE), 
         "color": BUTTON_COLOR, "hover_color": BUTTON_HOVER_COLOR, "type": "number"},
        {"label": "5", "rect": pygame.Rect(BUTTON_MARGIN * 2 + BUTTON_SIZE, DISPLAY_HEIGHT + CONTEXT_PANEL_HEIGHT + BUTTON_MARGIN * 2 + BUTTON_SIZE, BUTTON_SIZE, BUTTON_SIZE), 
         "color": BUTTON_COLOR, "hover_color": BUTTON_HOVER_COLOR, "type": "number"},
        {"label": "6", "rect": pygame.Rect(BUTTON_MARGIN * 3 + BUTTON_SIZE * 2, DISPLAY_HEIGHT + CONTEXT_PANEL_HEIGHT + BUTTON_MARGIN * 2 + BUTTON_SIZE, BUTTON_SIZE, BUTTON_SIZE), 
         "color": BUTTON_COLOR, "hover_color": BUTTON_HOVER_COLOR, "type": "number"},
        {"label": "1", "rect": pygame.Rect(BUTTON_MARGIN, DISPLAY_HEIGHT + CONTEXT_PANEL_HEIGHT + BUTTON_MARGIN * 3 + BUTTON_SIZE * 2, BUTTON_SIZE, BUTTON_SIZE), 
         "color": BUTTON_COLOR, "hover_color": BUTTON_HOVER_COLOR, "type": "number"},
        {"label": "2", "rect": pygame.Rect(BUTTON_MARGIN * 2 + BUTTON_SIZE, DISPLAY_HEIGHT + CONTEXT_PANEL_HEIGHT + BUTTON_MARGIN * 3 + BUTTON_SIZE * 2, BUTTON_SIZE, BUTTON_SIZE), 
         "color": BUTTON_COLOR, "hover_color": BUTTON_HOVER_COLOR, "type": "number"},
        {"label": "3", "rect": pygame.Rect(BUTTON_MARGIN * 3 + BUTTON_SIZE * 2, DISPLAY_HEIGHT + CONTEXT_PANEL_HEIGHT + BUTTON_MARGIN * 3 + BUTTON_SIZE * 2, BUTTON_SIZE, BUTTON_SIZE), 
         "color": BUTTON_COLOR, "hover_color": BUTTON_HOVER_COLOR, "type": "number"},
        {"label": "0", "rect": pygame.Rect(BUTTON_MARGIN, DISPLAY_HEIGHT + CONTEXT_PANEL_HEIGHT + BUTTON_MARGIN * 4 + BUTTON_SIZE * 3, BUTTON_SIZE * 2 + BUTTON_MARGIN, BUTTON_SIZE), 
         "color": BUTTON_COLOR, "hover_color": BUTTON_HOVER_COLOR, "type": "number"},
        {"label": ".", "rect": pygame.Rect(BUTTON_MARGIN * 3 + BUTTON_SIZE * 2, DISPLAY_HEIGHT + CONTEXT_PANEL_HEIGHT + BUTTON_MARGIN * 4 + BUTTON_SIZE * 3, BUTTON_SIZE, BUTTON_SIZE), 
         "color": BUTTON_COLOR, "hover_color": BUTTON_HOVER_COLOR, "type": "decimal"},
    ]
    
    base_buttons.extend(numbers)
    
    # Context-specific special buttons (right column)
    context = CONTEXT_MODES[current_context]
    special_buttons = context["buttons"]
    
    for i, btn_label in enumerate(special_buttons[:8]):  # Max 8 special buttons
        row = i % 4
        col = i // 4
        x_pos = BUTTON_MARGIN * 5 + BUTTON_SIZE * 3 + (col * (BUTTON_SIZE + BUTTON_MARGIN))
        y_pos = DISPLAY_HEIGHT + CONTEXT_PANEL_HEIGHT + BUTTON_MARGIN + (row * (BUTTON_SIZE + BUTTON_MARGIN))
        
        base_buttons.append({
            "label": btn_label,
            "rect": pygame.Rect(x_pos, y_pos, BUTTON_SIZE, BUTTON_SIZE),
            "color": SPECIAL_COLOR,
            "hover_color": SPECIAL_HOVER_COLOR,
            "type": "context_" + current_context.lower()
        })
    
    # Always include equals button
    base_buttons.append({
        "label": "=",
        "rect": pygame.Rect(BUTTON_MARGIN * 5 + BUTTON_SIZE * 3, DISPLAY_HEIGHT + CONTEXT_PANEL_HEIGHT + BUTTON_MARGIN * 4 + BUTTON_SIZE * 3, BUTTON_SIZE, BUTTON_SIZE),
        "color": OPERATOR_COLOR,
        "hover_color": OPERATOR_HOVER_COLOR,
        "type": "equals"
    })
    
    return base_buttons

def draw_display():
    """Draw the calculator display area"""
    # Display background with context color tint
    context_color = CONTEXT_MODES[current_context]["color"]
    tinted_color = (
        int(DISPLAY_COLOR[0] * 0.7 + context_color[0] * 0.3),
        int(DISPLAY_COLOR[1] * 0.7 + context_color[1] * 0.3),
        int(DISPLAY_COLOR[2] * 0.7 + context_color[2] * 0.3)
    )
    pygame.draw.rect(screen, tinted_color, (0, 0, SCREEN_WIDTH, DISPLAY_HEIGHT))
    
    # Previous input (smaller, at top)
    if previous_input:
        prev_text = small_font.render(previous_input + (" " + current_operator if current_operator else ""), True, (180, 180, 200))
        screen.blit(prev_text, (20, 20))
    
    # Current input or result
    display_text = current_input if not error_message else error_message
    text_color = ERROR_COLOR if error_message else TEXT_COLOR
    
    if len(display_text) > 20:
        display_text = display_text[:20] + "..."
    
    text_surface = display_font.render(display_text, True, text_color)
    text_rect = text_surface.get_rect()
    text_rect.right = SCREEN_WIDTH - 20
    text_rect.centery = DISPLAY_HEIGHT // 2 + 10
    screen.blit(text_surface, text_rect)
    
    # Context indicator
    context_indicator = small_font.render(f"Mode: {current_context}", True, context_color)
    screen.blit(context_indicator, (20, DISPLAY_HEIGHT - 30))
    
    # Draw separator
    pygame.draw.line(screen, (70, 70, 90), (0, DISPLAY_HEIGHT), (SCREEN_WIDTH, DISPLAY_HEIGHT), 2)

def draw_context_panel():
    """Draw the smart context panel"""
    # Panel background
    pygame.draw.rect(screen, CONTEXT_COLOR, (0, DISPLAY_HEIGHT, SCREEN_WIDTH, CONTEXT_PANEL_HEIGHT))
    
    # Current mode highlight
    mode_color = CONTEXT_MODES[current_context]["color"]
    pygame.draw.rect(screen, mode_color, (0, DISPLAY_HEIGHT, SCREEN_WIDTH, 35))
    
    # Mode title
    title = context_font.render(f"{current_context} Mode", True, TEXT_COLOR)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, DISPLAY_HEIGHT + 8))
    
    # Mode description
    description = small_font.render(CONTEXT_MODES[current_context]["description"], True, (200, 200, 220))
    screen.blit(description, (SCREEN_WIDTH // 2 - description.get_width() // 2, DISPLAY_HEIGHT + 32))
    
    # Mode selector buttons
    mode_x = 10
    for i, (mode_name, mode_info) in enumerate(CONTEXT_MODES.items()):
        is_active = mode_name == current_context
        btn_width = 90
        btn_height = 30
        
        btn_rect = pygame.Rect(mode_x, DISPLAY_HEIGHT + 60, btn_width, btn_height)
        color = mode_info["color"] if is_active else (60, 65, 85)
        hover_color = (min(color[0] + 30, 255), min(color[1] + 30, 255), min(color[2] + 30, 255))
        
        # Check hover
        mouse_pos = pygame.mouse.get_pos()
        is_hover = btn_rect.collidepoint(mouse_pos) and not is_active
        
        # Draw button
        btn_color = hover_color if is_hover else color
        pygame.draw.rect(screen, btn_color, btn_rect, border_radius=5)
        
        # Draw border if active
        if is_active:
            pygame.draw.rect(screen, (255, 255, 200), btn_rect, 2, border_radius=5)
        
        # Draw mode name
        mode_text = small_font.render(mode_name, True, TEXT_COLOR)
        text_rect = mode_text.get_rect(center=btn_rect.center)
        screen.blit(mode_text, text_rect)
        
        mode_x += btn_width + 10
    
    # Smart suggestions area
    suggestion_y = DISPLAY_HEIGHT + 100
    suggestions_title = small_font.render("Smart Suggestions:", True, HINT_COLOR)
    screen.blit(suggestions_title, (15, suggestion_y))
    
    # Show smart suggestions based on context
    if smart_suggestions:
        suggestion_x = 15
        for suggestion in smart_suggestions[:4]:  # Show max 4 suggestions
            suggestion_bg = pygame.Rect(suggestion_x, suggestion_y + 25, 100, 25)
            pygame.draw.rect(screen, (60, 65, 90), suggestion_bg, border_radius=4)
            
            suggestion_text = hint_font.render(suggestion, True, (200, 230, 255))
            text_rect = suggestion_text.get_rect(center=suggestion_bg.center)
            screen.blit(suggestion_text, text_rect)
            
            suggestion_x += 105
    else:
        # Default hint based on context
        hints = {
            "Standard": "Enter numbers and operations",
            "Homework": "Try sin(), cos(), or √ functions",
            "Shopping": "Calculate tips, taxes, or split bills",
            "Budgeting": "Track expenses with % calculations",
            "Cooking": "Convert units or scale recipes"
        }
        hint = hints.get(current_context, "")
        hint_text = hint_font.render(hint, True, (180, 180, 220))
        screen.blit(hint_text, (15, suggestion_y + 30))
    
    # Pattern recognition indicator
    if calculation_pattern:
        pattern_text = hint_font.render(f"Pattern: {', '.join(calculation_pattern[-3:])}", True, (150, 200, 255))
        screen.blit(pattern_text, (SCREEN_WIDTH - pattern_text.get_width() - 15, suggestion_y + 30))
    
    # Draw separator
    pygame.draw.line(screen, (80, 80, 100), (0, DISPLAY_HEIGHT + CONTEXT_PANEL_HEIGHT), 
                    (SCREEN_WIDTH, DISPLAY_HEIGHT + CONTEXT_PANEL_HEIGHT), 2)

def draw_buttons():
    """Draw all calculator buttons"""
    buttons = get_buttons_for_context()
    mouse_pos = pygame.mouse.get_pos()
    
    for button in buttons:
        is_hover = button["rect"].collidepoint(mouse_pos)
        color = button["hover_color"] if is_hover else button["color"]
        
        # Context-specific buttons get special tint
        if button["type"].startswith("context_"):
            context_color = CONTEXT_MODES[current_context]["color"]
            color = (
                int(color[0] * 0.7 + context_color[0] * 0.3),
                int(color[1] * 0.7 + context_color[1] * 0.3),
                int(color[2] * 0.7 + context_color[2] * 0.3)
            )
        
        # Draw button
        pygame.draw.rect(screen, color, button["rect"], border_radius=8)
        
        # Draw label
        label_color = HINT_COLOR if button["type"].startswith("context_") else TEXT_COLOR
        text_surface = button_font.render(button["label"], True, label_color)
        text_rect = text_surface.get_rect(center=button["rect"].center)
        screen.blit(text_surface, text_rect)
        
        # Highlight smart suggestions
        if button["label"] in smart_suggestions:
            pygame.draw.rect(screen, HINT_COLOR, button["rect"], 3, border_radius=8)

def draw_title():
    """Draw project title"""
    title_font = pygame.font.SysFont('Arial', 24, bold=True)
    title = title_font.render("Smart Context-Aware Calculator", True, (220, 230, 255))
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT - 30))
    
    # Agile methodology indicator
    agile_text = small_font.render("Agile Adaptive Interface", True, (150, 200, 255))
    screen.blit(agile_text, (SCREEN_WIDTH // 2 - agile_text.get_width() // 2, SCREEN_HEIGHT - 50))

def handle_button_click(button):
    """Handle button click events with context awareness"""
    global current_input, previous_input, current_operator, result, error_message, current_context
    
    button_type = button["type"]
    button_label = button["label"]
    
    # Update context history
    update_context_history(button_label)
    
    # Clear error message
    if error_message and button_type not in ["clear", "context_switch"]:
        error_message = ""
    
    # Handle context switching
    if button_label in CONTEXT_MODES and button_label != current_context:
        current_context = button_label
        smart_suggestions.clear()
        detect_context_pattern()
        return
    
    # Handle context-specific functions
    if current_context == "Shopping" and button_type.startswith("context_shopping"):
        handle_shopping_function(button_label)
    
    elif current_context == "Homework" and button_type.startswith("context_homework"):
        handle_homework_function(button_label)
    
    elif current_context == "Budgeting" and button_type.startswith("context_budgeting"):
        handle_budgeting_function(button_label)
    
    elif current_context == "Cooking" and button_type.startswith("context_cooking"):
        handle_cooking_function(button_label)
    
    else:
        # Standard calculator functions
        handle_standard_function(button_label, button_type)
    
    # Detect patterns after each click
    detect_context_pattern()

def handle_standard_function(label, btn_type):
    """Handle standard calculator functions"""
    global current_input, previous_input, current_operator, result
    
    if btn_type == "number":
        current_input += label
    
    elif btn_type == "operator":
        if current_input:
            if previous_input and current_operator:
                calculate_result()
                if error_message:
                    return
                previous_input = str(result) if result is not None else ""
            else:
                previous_input = current_input
            
            current_operator = label
            current_input = ""
    
    elif btn_type == "decimal":
        if "." not in current_input:
            if not current_input:
                current_input = "0."
            else:
                current_input += "."
    
    elif btn_type == "equals":
        if previous_input and current_operator and current_input:
            calculate_result()
            if not error_message:
                previous_input = ""
                current_operator = ""
    
    elif label == "C":
        current_input = ""
        previous_input = ""
        current_operator = ""
        result = None
        error_message = ""
    
    elif label == "Del":
        if current_input:
            current_input = current_input[:-1]
        elif error_message:
            error_message = ""

def handle_shopping_function(label):
    """Handle shopping-specific functions"""
    global current_input, smart_suggestions
    
    if label == "Tip":
        if current_input:
            amount = float(current_input)
            tips = {
                "15%": amount * 0.15,
                "18%": amount * 0.18,
                "20%": amount * 0.20
            }
            smart_suggestions = [f"{k}: ${v:.2f}" for k, v in tips.items()]
    
    elif label == "Tax":
        if current_input:
            # Assume 8% tax rate
            amount = float(current_input)
            tax = amount * 0.08
            current_input = str(amount + tax)
            smart_suggestions = ["Tax added: 8%"]
    
    elif label == "Split":
        if current_input and previous_input:
            try:
                total = float(previous_input)
                people = float(current_input)
                per_person = total / people
                current_input = str(per_person)
                smart_suggestions = [f"Each pays: ${per_person:.2f}"]
            except:
                error_message = "Invalid split"

def handle_homework_function(label):
    """Handle homework-specific functions"""
    global current_input
    
    if label == "π":
        current_input = str(3.1415926535)
    
    elif label == "√":
        if current_input:
            try:
                num = float(current_input)
                if num >= 0:
                    current_input = str(num ** 0.5)
                else:
                    error_message = "Invalid sqrt"
            except:
                error_message = "Invalid input"
    
    elif label == "x²":
        if current_input:
            try:
                num = float(current_input)
                current_input = str(num ** 2)
            except:
                error_message = "Invalid input"

def handle_budgeting_function(label):
    """Handle budgeting-specific functions"""
    global current_input, smart_suggestions
    
    if label == "%":
        if current_input:
            current_input = str(float(current_input) / 100)
            smart_suggestions = ["Converted to decimal"]
    
    elif label == "Inc":
        if current_input and previous_input:
            try:
                base = float(previous_input)
                percentage = float(current_input)
                increased = base * (1 + percentage/100)
                current_input = str(increased)
                smart_suggestions = [f"Increased by {percentage}%"]
            except:
                error_message = "Invalid calculation"

def handle_cooking_function(label):
    """Handle cooking-specific functions"""
    global current_input
    
    if label == "½":
        if current_input:
            try:
                num = float(current_input)
                current_input = str(num / 2)
            except:
                error_message = "Invalid input"
    
    elif label == "2×":
        if current_input:
            try:
                num = float(current_input)
                current_input = str(num * 2)
            except:
                error_message = "Invalid input"
    
    elif label == "°C/°F":
        if current_input:
            try:
                temp = float(current_input)
                # Assume input is °C, convert to °F
                converted = (temp * 9/5) + 32
                current_input = f"{converted:.1f}°F"
                smart_suggestions = ["Converted °C to °F"]
            except:
                error_message = "Invalid temperature"

def calculate_result():
    """Perform calculation"""
    global current_input, result, error_message
    
    try:
        num1 = float(previous_input)
        num2 = float(current_input)
        
        if current_operator == "+":
            result = num1 + num2
        elif current_operator == "-":
            result = num1 - num2
        elif current_operator == "×":
            result = num1 * num2
        elif current_operator == "/":
            if num2 == 0:
                error_message = "Error: Division by 0"
                return
            result = num1 / num2
        
        # Format result
        if result.is_integer():
            current_input = str(int(result))
        else:
            current_input = str(round(result, 10)).rstrip('0').rstrip('.')
    
    except ValueError:
        error_message = "Error: Invalid input"
    except Exception as e:
        error_message = f"Error: {str(e)}"

# Main game loop
def main():
    running = True
    
    # Load initial context data
    load_context_data()
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Check context mode buttons
                    mode_x = 10
                    for mode_name in CONTEXT_MODES:
                        btn_rect = pygame.Rect(mode_x, DISPLAY_HEIGHT + 60, 90, 30)
                        if btn_rect.collidepoint(mouse_pos):
                            current_context = mode_name
                            smart_suggestions.clear()
                            detect_context_pattern()
                            break
                        mode_x += 100
                    
                    # Check calculator buttons
                    buttons = get_buttons_for_context()
                    for button in buttons:
                        if button["rect"].collidepoint(mouse_pos):
                            handle_button_click(button)
                            break
        
        # Draw everything
        screen.fill(BACKGROUND_COLOR)
        draw_display()
        draw_context_panel()
        draw_buttons()
        draw_title()
        
        # Update display
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()