import pygame
import sys
import json
import math
import os
from datetime import datetime

# Initialize pygame
pygame.init()

# Constants - Increased width for input panel
SCREEN_WIDTH = 950  # Increased from 700
SCREEN_HEIGHT = 620
BUTTON_SIZE = 70
BUTTON_MARGIN = 10
DISPLAY_HEIGHT = 120
CONTEXT_PANEL_HEIGHT = 175
INPUT_PANEL_WIDTH = 250  # Width of right-side input panel
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
INPUT_BOX_COLOR = (35, 40, 55)
INPUT_BOX_ACTIVE_COLOR = (60, 65, 85)
INPUT_BOX_BORDER_COLOR = (80, 85, 105)
INPUT_LABEL_COLOR = (180, 185, 200)
ERROR_COLOR = (255, 50, 50)
SUCCESS_COLOR = (50, 255, 100)
HINT_COLOR = (255, 215, 0)

# Context modes with specific colors and features
CONTEXT_MODES = {
    "Standard": {
        "color": (70, 70, 90),
        "buttons": ["C", "Del", "/", "×", "-", "+", "=", "."],
        "description": "Basic arithmetic operations",
        "input_fields": []  # No input fields for standard mode
    },
    "Homework": {
        "color": (60, 100, 180),
        "buttons": ["C", "Del", "√", "x²", "π", "sin", "cos", "tan"],
        "description": "Math homework and studies",
        "input_fields": ["Angle (deg):", "Value:"]
    },
    "Shopping": {
        "color": (40, 160, 80),
        "buttons": ["C", "Del", "%", "Tax", "Tip", "Split", "Save", "Total"],
        "description": "Shopping and expenses",
        "input_fields": ["Amount ($):", "People:", "Tip %:", "Tax %:"]
    },
    "Budgeting": {
        "color": (180, 100, 60),
        "buttons": ["C", "Del", "%", "Avg", "Inc", "Dec", "Save", "Goal"],
        "description": "Personal budgeting",
        "input_fields": ["Base Amount:", "Percentage:", "Target Goal:", "Current:"]
    },
    "Cooking": {
        "color": (200, 120, 50),
        "buttons": ["C", "Del", "½", "⅓", "¼", "2×", "3×", "°C/°F"],
        "description": "Cooking and recipes",
        "input_fields": ["Amount:", "Servings:", "Temperature:", "Scale Factor:"]
    }
}

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Smart Context-Aware Calculator with Input Panel")
clock = pygame.time.Clock()

# Fonts
display_font = pygame.font.SysFont('Arial', 40)
button_font = pygame.font.SysFont('Arial', 26)
small_font = pygame.font.SysFont('Arial', 18)
context_font = pygame.font.SysFont('Arial', 16, bold=True)
hint_font = pygame.font.SysFont('Arial', 14)
input_font = pygame.font.SysFont('Arial', 20)

# Calculator state
current_input = ""
previous_input = ""
current_operator = ""
result = None
error_message = ""
current_context = "Standard"
context_history = []
smart_suggestions = []
last_calculation_time = 0
calculation_pattern = []

# Input panel state
input_fields = {}
active_input_field = None
input_field_values = {}

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

def initialize_input_fields():
    """Initialize input fields for current context"""
    global input_fields, input_field_values, active_input_field
    
    input_fields = {}
    input_field_values = {}
    active_input_field = None
    
    context_info = CONTEXT_MODES[current_context]
    field_labels = context_info["input_fields"]
    
    # Calculate positions for input fields
    start_x = SCREEN_WIDTH - INPUT_PANEL_WIDTH + 20
    start_y = DISPLAY_HEIGHT + 30
    field_height = 40
    field_spacing = 60
    
    for i, label in enumerate(field_labels):
        field_id = f"field_{i}"
        input_fields[field_id] = {
            "label": label,
            "rect": pygame.Rect(start_x, start_y + i * field_spacing, INPUT_PANEL_WIDTH - 40, field_height),
            "value": "",
            "active": False
        }
        input_field_values[field_id] = ""

def detect_context_pattern():
    """Analyze current calculation to detect context"""
    global smart_suggestions, current_context
    
    # Analyze current input pattern
    if current_input and previous_input:
        # Shopping/Tipping pattern
        if "Tip" in calculation_pattern or ("+" in calculation_pattern and current_input.replace('.', '').isdigit() and float(current_input) < 100):
            if current_context != "Shopping":
                current_context = "Shopping"
                initialize_input_fields()
                smart_suggestions = ["15%", "18%", "20%", "Split Bill"]
        
        # Percentage calculations
        elif "%" in current_operator or ("/" in calculation_pattern and "100" in calculation_pattern):
            if current_context != "Budgeting":
                current_context = "Budgeting"
                initialize_input_fields()
                smart_suggestions = ["Increase by %", "Decrease by %", "Average", "Savings"]
        
        # Fraction/decimal patterns (cooking)
        elif "." in current_input or any(x in current_input for x in ["0.25", "0.33", "0.5", "0.75"]):
            if current_context != "Cooking":
                current_context = "Cooking"
                initialize_input_fields()
                smart_suggestions = ["Double", "Half", "Convert Units", "°C to °F"]
        
        # Complex math patterns (homework)
        elif any(op in calculation_pattern for op in ["sin", "cos", "tan", "√", "^"]):
            if current_context != "Homework":
                current_context = "Homework"
                initialize_input_fields()
                smart_suggestions = ["π", "e", "Solve", "Graph"]

def update_context_history(operation):
    """Update history of operations for pattern recognition"""
    context_history.append({
        "operation": operation,
        "time": datetime.now().isoformat(),
        "context": current_context,
        "input": current_input[:10] if current_input else ""
    })
    
    if len(context_history) > 20:
        context_history.pop(0)
    
    calculation_pattern.append(operation)
    if len(calculation_pattern) > 5:
        calculation_pattern.pop(0)
    
    data = load_context_data()
    if current_context not in data["mode_usage"]:
        data["mode_usage"][current_context] = 0
    data["mode_usage"][current_context] += 1
    save_context_data(data)

def get_input_value(field_id):
    """Get value from input field or main display"""
    if input_field_values.get(field_id):
        try:
            return float(input_field_values[field_id])
        except:
            return None
    return None

def set_input_value(field_id, value):
    """Set value to input field"""
    if field_id in input_fields:
        input_field_values[field_id] = str(value)

# Dynamic button layout based on context (fits in left panel)
def get_buttons_for_context():
    """Generate buttons based on current context with dynamic positioning"""
    base_buttons = []
    
    # Calculate grid dimensions (only in left panel)
    button_area_width = SCREEN_WIDTH - INPUT_PANEL_WIDTH
    button_area_y = DISPLAY_HEIGHT + CONTEXT_PANEL_HEIGHT
    
    num_cols = 3
    special_cols = 2
    total_cols = num_cols + special_cols
    
    button_width = (button_area_width - (total_cols + 1) * BUTTON_MARGIN) // total_cols
    button_height = BUTTON_SIZE
    
    # Common number buttons
    numbers = [
        {"label": "7", "x": 0, "y": 0},
        {"label": "8", "x": 1, "y": 0},
        {"label": "9", "x": 2, "y": 0},
        {"label": "4", "x": 0, "y": 1},
        {"label": "5", "x": 1, "y": 1},
        {"label": "6", "x": 2, "y": 1},
        {"label": "1", "x": 0, "y": 2},
        {"label": "2", "x": 1, "y": 2},
        {"label": "3", "x": 2, "y": 2},
        {"label": "0", "x": 0, "y": 3, "colspan": 2},
        {"label": ".", "x": 2, "y": 3},
    ]
    
    for num in numbers:
        colspan = num.get("colspan", 1)
        x_pos = BUTTON_MARGIN + num["x"] * (button_width + BUTTON_MARGIN)
        y_pos = button_area_y + BUTTON_MARGIN + num["y"] * (button_height + BUTTON_MARGIN)
        width = button_width * colspan + BUTTON_MARGIN * (colspan - 1)
        
        btn_type = "number"
        if num["label"] == ".":
            btn_type = "decimal"
        
        base_buttons.append({
            "label": num["label"],
            "rect": pygame.Rect(x_pos, y_pos, width, button_height),
            "color": BUTTON_COLOR,
            "hover_color": BUTTON_HOVER_COLOR,
            "type": btn_type
        })
    
    # Context-specific special buttons
    context = CONTEXT_MODES[current_context]
    special_buttons = context["buttons"]
    
    for i, btn_label in enumerate(special_buttons[:8]):
        col = i // 4
        row = i % 4
        
        x_pos = BUTTON_MARGIN * 4 + button_width * 3 + col * (button_width + BUTTON_MARGIN)
        y_pos = button_area_y + BUTTON_MARGIN + row * (button_height + BUTTON_MARGIN)
        
        btn_type = f"context_{current_context.lower()}"
        
        if current_context == "Standard" and btn_label in ["+", "-", "×", "/"]:
            btn_type = "operator"
        elif current_context == "Standard" and btn_label == "=":
            btn_type = "equals"
        elif current_context == "Standard" and btn_label in ["C", "Del"]:
            btn_type = btn_label.lower()
        
        base_buttons.append({
            "label": btn_label,
            "rect": pygame.Rect(x_pos, y_pos, button_width, button_height),
            "color": SPECIAL_COLOR if btn_type.startswith("context_") else OPERATOR_COLOR,
            "hover_color": SPECIAL_HOVER_COLOR if btn_type.startswith("context_") else OPERATOR_HOVER_COLOR,
            "type": btn_type
        })
    
    if current_context != "Standard" or "=" not in [b["label"] for b in base_buttons]:
        equals_x = BUTTON_MARGIN * 4 + button_width * 3 + (button_width + BUTTON_MARGIN)
        equals_y = button_area_y + BUTTON_MARGIN + 3 * (button_height + BUTTON_MARGIN)
        
        base_buttons.append({
            "label": "=",
            "rect": pygame.Rect(equals_x, equals_y, button_width, button_height),
            "color": OPERATOR_COLOR,
            "hover_color": OPERATOR_HOVER_COLOR,
            "type": "equals"
        })
    
    return base_buttons

def draw_display():
    """Draw the calculator display area"""
    context_color = CONTEXT_MODES[current_context]["color"]
    tinted_color = (
        int(DISPLAY_COLOR[0] * 0.7 + context_color[0] * 0.3),
        int(DISPLAY_COLOR[1] * 0.7 + context_color[1] * 0.3),
        int(DISPLAY_COLOR[2] * 0.7 + context_color[2] * 0.3)
    )
    pygame.draw.rect(screen, tinted_color, (0, 0, SCREEN_WIDTH - INPUT_PANEL_WIDTH, DISPLAY_HEIGHT))
    
    if previous_input:
        prev_text = small_font.render(previous_input + (" " + current_operator if current_operator else ""), True, (180, 180, 200))
        screen.blit(prev_text, (20, 20))
    
    display_text = current_input if not error_message else error_message
    text_color = ERROR_COLOR if error_message else TEXT_COLOR
    
    if len(display_text) > 40:
        display_text = display_text[:50] + "..."
    
    text_surface = display_font.render(display_text, True, text_color)
    text_rect = text_surface.get_rect()
    text_rect.right = SCREEN_WIDTH - INPUT_PANEL_WIDTH - 20
    text_rect.centery = DISPLAY_HEIGHT // 2 + 10
    screen.blit(text_surface, text_rect)
    
    context_indicator = small_font.render(f"Mode: {current_context}", True, context_color)
    screen.blit(context_indicator, (20, DISPLAY_HEIGHT - 30))
    
    pygame.draw.line(screen, (70, 70, 90), (0, DISPLAY_HEIGHT), (SCREEN_WIDTH - INPUT_PANEL_WIDTH, DISPLAY_HEIGHT), 2)

def draw_context_panel():
    """Draw the smart context panel"""
    pygame.draw.rect(screen, CONTEXT_COLOR, (0, DISPLAY_HEIGHT, SCREEN_WIDTH - INPUT_PANEL_WIDTH, CONTEXT_PANEL_HEIGHT))
    
    mode_color = CONTEXT_MODES[current_context]["color"]
    pygame.draw.rect(screen, mode_color, (0, DISPLAY_HEIGHT, SCREEN_WIDTH - INPUT_PANEL_WIDTH, 35))
    
    title = context_font.render(f"{current_context} Mode", True, TEXT_COLOR)
    screen.blit(title, ((SCREEN_WIDTH - INPUT_PANEL_WIDTH) // 2 - title.get_width() // 2, DISPLAY_HEIGHT + 8))
    
    description = small_font.render(CONTEXT_MODES[current_context]["description"], True, (200, 200, 220))
    screen.blit(description, ((SCREEN_WIDTH - INPUT_PANEL_WIDTH) // 2 - description.get_width() // 2, DISPLAY_HEIGHT + 32))
    
    btn_width = 90
    btn_height = 30
    spacing = 10
    total_width = len(CONTEXT_MODES) * btn_width + (len(CONTEXT_MODES) - 1) * spacing
    mode_x = (SCREEN_WIDTH - INPUT_PANEL_WIDTH - total_width) // 2
    
    for i, (mode_name, mode_info) in enumerate(CONTEXT_MODES.items()):
        is_active = mode_name == current_context
        
        btn_rect = pygame.Rect(mode_x, DISPLAY_HEIGHT + 60, btn_width, btn_height)
        color = mode_info["color"] if is_active else (60, 65, 85)
        hover_color = (min(color[0] + 30, 255), min(color[1] + 30, 255), min(color[2] + 30, 255))
        
        mouse_pos = pygame.mouse.get_pos()
        is_hover = btn_rect.collidepoint(mouse_pos) and not is_active
        
        btn_color = hover_color if is_hover else color
        pygame.draw.rect(screen, btn_color, btn_rect, border_radius=5)
        
        if is_active:
            pygame.draw.rect(screen, (255, 255, 200), btn_rect, 2, border_radius=5)
        
        mode_text = small_font.render(mode_name, True, TEXT_COLOR)
        text_rect = mode_text.get_rect(center=btn_rect.center)
        screen.blit(mode_text, text_rect)
        
        mode_x += btn_width + spacing
    
    suggestion_y = DISPLAY_HEIGHT + 100
    suggestions_title = small_font.render("Smart Suggestions:", True, HINT_COLOR)
    screen.blit(suggestions_title, (15, suggestion_y))
    
    if smart_suggestions:
        suggestion_x = 15
        for suggestion in smart_suggestions[:4]:
            suggestion_bg = pygame.Rect(suggestion_x, suggestion_y + 25, 100, 25)
            pygame.draw.rect(screen, (60, 65, 90), suggestion_bg, border_radius=4)
            
            suggestion_text = hint_font.render(suggestion, True, (200, 230, 255))
            text_rect = suggestion_text.get_rect(center=suggestion_bg.center)
            screen.blit(suggestion_text, text_rect)
            
            suggestion_x += 105
    else:
        hints = {
            "Standard": "Enter numbers and operations",
            "Homework": "Try sin(), cos(), or √ functions",
            "Shopping": "Use input boxes for total, people, tip %",
            "Budgeting": "Use input boxes for base, percentage, goal",
            "Cooking": "Use input boxes for amount, servings, temperature"
        }
        hint = hints.get(current_context, "")
        hint_text = hint_font.render(hint, True, (180, 180, 220))
        screen.blit(hint_text, (15, suggestion_y + 30))
    
    if calculation_pattern:
        pattern_text = hint_font.render(f"Pattern: {', '.join(calculation_pattern[-3:])}", True, (150, 200, 255))
        screen.blit(pattern_text, (SCREEN_WIDTH - INPUT_PANEL_WIDTH - pattern_text.get_width() - 15, suggestion_y + 30))
    
    pygame.draw.line(screen, (80, 80, 100), (0, DISPLAY_HEIGHT + CONTEXT_PANEL_HEIGHT), 
                    (SCREEN_WIDTH - INPUT_PANEL_WIDTH, DISPLAY_HEIGHT + CONTEXT_PANEL_HEIGHT), 2)

def draw_input_panel():
    """Draw the right-side input panel with fields for context-specific values"""
    # Input panel background
    pygame.draw.rect(screen, (30, 35, 50), (SCREEN_WIDTH - INPUT_PANEL_WIDTH, 0, INPUT_PANEL_WIDTH, SCREEN_HEIGHT))
    
    # Panel title
    title = context_font.render(f"{current_context} Inputs", True, HINT_COLOR)
    screen.blit(title, (SCREEN_WIDTH - INPUT_PANEL_WIDTH + 20, 10))
    
    # Draw input fields
    for field_id, field in input_fields.items():
        # Draw label
        label = small_font.render(field["label"], True, INPUT_LABEL_COLOR)
        screen.blit(label, (field["rect"].x, field["rect"].y - 22))
        
        # Draw input box
        is_active = (field_id == active_input_field)
        box_color = INPUT_BOX_ACTIVE_COLOR if is_active else INPUT_BOX_COLOR
        pygame.draw.rect(screen, box_color, field["rect"], border_radius=5)
        pygame.draw.rect(screen, INPUT_BOX_BORDER_COLOR, field["rect"], 2, border_radius=5)
        
        # Draw value
        value = input_field_values.get(field_id, "")
        if not value and not is_active:
            value = "Enter value..."
            color = (100, 100, 120)
        else:
            color = TEXT_COLOR
        
        value_surface = input_font.render(value, True, color)
        value_rect = value_surface.get_rect(midleft=(field["rect"].x + 10, field["rect"].centery))
        
        # Handle overflow
        if value_surface.get_width() > field["rect"].width - 20:
            # Scroll text
            text_width = value_surface.get_width()
            if is_active:
                offset = max(0, text_width - field["rect"].width + 20)
                value_rect.x -= offset
        
        screen.blit(value_surface, value_rect)
    
    # Draw usage instructions
    instructions = [
        "Instructions:",
        "1. Click a field to activate",
        "2. Type values directly",
        "3. Use buttons with inputs",
        "4. Press Enter to apply"
    ]
    
    y_pos = DISPLAY_HEIGHT + CONTEXT_PANEL_HEIGHT + 50
    for instruction in instructions:
        inst_text = hint_font.render(instruction, True, (150, 170, 200))
        screen.blit(inst_text, (SCREEN_WIDTH - INPUT_PANEL_WIDTH + 20, y_pos))
        y_pos += 22
    
    # Draw separator
    pygame.draw.line(screen, (60, 65, 85), (SCREEN_WIDTH - INPUT_PANEL_WIDTH, 0), 
                    (SCREEN_WIDTH - INPUT_PANEL_WIDTH, SCREEN_HEIGHT), 2)

def draw_buttons():
    """Draw all calculator buttons"""
    buttons = get_buttons_for_context()
    mouse_pos = pygame.mouse.get_pos()
    
    for button in buttons:
        is_hover = button["rect"].collidepoint(mouse_pos)
        color = button["hover_color"] if is_hover else button["color"]
        
        if button["type"].startswith("context_"):
            context_color = CONTEXT_MODES[current_context]["color"]
            color = (
                int(color[0] * 0.7 + context_color[0] * 0.3),
                int(color[1] * 0.7 + context_color[1] * 0.3),
                int(color[2] * 0.7 + context_color[2] * 0.3)
            )
        
        pygame.draw.rect(screen, color, button["rect"], border_radius=8)
        
        label_color = HINT_COLOR if button["type"].startswith("context_") else TEXT_COLOR
        text_surface = button_font.render(button["label"], True, label_color)
        text_rect = text_surface.get_rect(center=button["rect"].center)
        screen.blit(text_surface, text_rect)
        
        if button["label"] in smart_suggestions:
            pygame.draw.rect(screen, HINT_COLOR, button["rect"], 3, border_radius=8)

def handle_button_click(button):
    """Handle button click events for calculator buttons"""
    global current_input, previous_input, current_operator, result, error_message
    
    button_type = button["type"]
    button_label = button["label"]
    
    update_context_history(button_label)
    
    if error_message and button_type not in ["clear", "context_switch"]:
        error_message = ""
    
    if button_type == "clear" or button_label == "C":
        current_input = ""
        previous_input = ""
        current_operator = ""
        result = None
        error_message = ""
        smart_suggestions.clear()
        # Also clear input fields
        for field_id in input_field_values:
            input_field_values[field_id] = ""
    
    elif button_type == "del" or button_label == "Del":
        if current_input:
            current_input = current_input[:-1]
        elif error_message:
            error_message = ""
    
    elif button_type == "number":
        current_input += button_label
    
    elif button_type == "decimal":
        if "." not in current_input:
            if not current_input:
                current_input = "0."
            else:
                current_input += "."
    
    elif button_type == "operator":
        if current_input:
            if previous_input and current_operator:
                calculate_result()
                if error_message:
                    return
                previous_input = str(result) if result is not None else ""
            else:
                previous_input = current_input
            
            current_operator = button_label
            current_input = ""
    
    elif button_type == "equals":
        if previous_input and current_operator and current_input:
            calculate_result()
            if not error_message:
                previous_input = ""
                current_operator = ""
    
    elif current_context == "Shopping" and button_type.startswith("context_shopping"):
        handle_shopping_function(button_label)
    
    elif current_context == "Homework" and button_type.startswith("context_homework"):
        handle_homework_function(button_label)
    
    elif current_context == "Budgeting" and button_type.startswith("context_budgeting"):
        handle_budgeting_function(button_label)
    
    elif current_context == "Cooking" and button_type.startswith("context_cooking"):
        handle_cooking_function(button_label)
    
    detect_context_pattern()

def handle_shopping_function(label):
    """Handle shopping-specific functions using input fields"""
    global current_input, smart_suggestions, error_message, previous_input
    
    try:
        if label == "Tip":
            # Get amount from field_0 or current input
            amount = get_input_value("field_0")
            if amount is None:
                if current_input:
                    amount = float(current_input)
                else:
                    error_message = "Enter amount in Amount field or display"
                    return
            
            # Get tip percentage from field_2 or use default
            tip_percent = get_input_value("field_2")
            if tip_percent is None:
                tip_percent = 15  # Default 15%
            
            tip_amount = amount * (tip_percent / 100)
            total = amount + tip_amount
            
            current_input = str(round(total, 2))
            smart_suggestions = [f"Tip: ${tip_amount:.2f}", f"Total: ${total:.2f}"]
            set_input_value("field_0", str(amount))
            if tip_percent != 15:
                set_input_value("field_2", str(tip_percent))
        
        elif label == "Tax":
            amount = get_input_value("field_0")
            if amount is None:
                if current_input:
                    amount = float(current_input)
                else:
                    error_message = "Enter amount in Amount field or display"
                    return
            
            tax_percent = get_input_value("field_3")
            if tax_percent is None:
                tax_percent = 8  # Default 8%
            
            tax = amount * (tax_percent / 100)
            total = amount + tax
            
            current_input = str(round(total, 2))
            smart_suggestions = [f"Tax: ${tax:.2f}", f"Total: ${total:.2f}"]
            set_input_value("field_0", str(amount))
        
        elif label == "Split":
            total = get_input_value("field_0")
            people = get_input_value("field_1")
            
            if total is None or people is None:
                error_message = "Enter Total and People in input fields"
                return
            
            if people == 0:
                error_message = "Cannot split by 0 people"
                return
            
            per_person = total / people
            current_input = str(round(per_person, 2))
            smart_suggestions = [f"Each pays: ${per_person:.2f}"]
            set_input_value("field_0", str(total))
            set_input_value("field_1", str(int(people)))
        
        elif label == "Total":
            # For shopping, calculate price * quantity
            if previous_input and current_input:
                try:
                    price = float(previous_input)
                    quantity = float(current_input)
                    total = price * quantity
                    current_input = str(round(total, 2))
                    smart_suggestions = [f"Total: ${total:.2f}"]
                except:
                    error_message = "Invalid values"
            else:
                error_message = "Enter price and quantity"
        
        elif label == "Save":
            original = get_input_value("field_0")
            discount = current_input
            
            if original is None:
                error_message = "Enter original price in Amount field"
                return
            
            if not discount:
                error_message = "Enter discount percentage"
                return
            
            try:
                discount_pct = float(discount)
                if discount_pct < 0 or discount_pct > 100:
                    error_message = "Discount must be 0-100%"
                    return
                
                saved = original * (discount_pct / 100)
                final_price = original - saved
                current_input = str(round(final_price, 2))
                smart_suggestions = [f"Saved: ${saved:.2f}", f"Final: ${final_price:.2f}"]
                set_input_value("field_0", str(original))
            except:
                error_message = "Invalid discount"
    
    except ValueError:
        error_message = "Invalid number format"
    except Exception as e:
        error_message = f"Error: {str(e)[:30]}"

def handle_homework_function(label):
    """Handle homework-specific functions"""
    global current_input, error_message, smart_suggestions
    
    if label == "π":
        current_input = str(math.pi)
        smart_suggestions = ["e", "√", "x²", "sin()"]
        set_input_value("field_1", str(math.pi))
    
    elif label == "√":
        value = get_input_value("field_1")
        if value is None:
            if current_input:
                value = float(current_input)
            else:
                error_message = "Enter value in Value field or display"
                return
        
        if value >= 0:
            result = math.sqrt(value)
            current_input = str(round(result, 10)).rstrip('0').rstrip('.')
            set_input_value("field_1", str(result))
        else:
            error_message = "Error: Negative sqrt"
    
    elif label == "x²":
        value = get_input_value("field_1")
        if value is None:
            if current_input:
                value = float(current_input)
            else:
                error_message = "Enter value in Value field or display"
                return
        
        result = value ** 2
        current_input = str(round(result, 10)).rstrip('0').rstrip('.')
        set_input_value("field_1", str(result))
    
    elif label in ["sin", "cos", "tan"]:
        angle = get_input_value("field_0")
        if angle is None:
            if current_input:
                angle = float(current_input)
            else:
                error_message = "Enter angle in Angle field or display"
                return
        
        radians = math.radians(angle)
        
        if label == "sin":
            result = math.sin(radians)
        elif label == "cos":
            result = math.cos(radians)
        elif label == "tan":
            if abs(math.cos(radians)) < 1e-10:
                error_message = "Error: Undefined tan"
                return
            result = math.tan(radians)
        
        current_input = str(round(result, 10)).rstrip('0').rstrip('.')
        smart_suggestions = ["sin", "cos", "tan", "π", "√"]
        set_input_value("field_0", str(angle))
        set_input_value("field_1", str(result))
    
    elif label == "e":
        current_input = str(math.e)
        smart_suggestions = ["π", "ln", "log", "√"]
        set_input_value("field_1", str(math.e))

def handle_budgeting_function(label):
    """Handle budgeting-specific functions using input fields"""
    global current_input, smart_suggestions, error_message, previous_input
    
    try:
        if label == "%":
            value = get_input_value("field_1")
            if value is None:
                if current_input:
                    value = float(current_input)
                else:
                    error_message = "Enter value in Percentage field or display"
                    return
            
            current_input = str(value / 100)
            smart_suggestions = ["Converted to decimal"]
            set_input_value("field_1", str(value))
        
        elif label == "Inc":
            base = get_input_value("field_0")
            percentage = get_input_value("field_1")
            
            if base is None or percentage is None:
                error_message = "Enter Base Amount and Percentage in input fields"
                return
            
            increased = base * (1 + percentage/100)
            current_input = str(round(increased, 2))
            smart_suggestions = [f"Increased by {percentage}% to {increased:.2f}"]
            set_input_value("field_0", str(base))
            set_input_value("field_1", str(percentage))
        
        elif label == "Dec":
            base = get_input_value("field_0")
            percentage = get_input_value("field_1")
            
            if base is None or percentage is None:
                error_message = "Enter Base Amount and Percentage in input fields"
                return
            
            decreased = base * (1 - percentage/100)
            current_input = str(round(decreased, 2))
            smart_suggestions = [f"Decreased by {percentage}% to {decreased:.2f}"]
            set_input_value("field_0", str(base))
            set_input_value("field_1", str(percentage))
        
        elif label == "Avg":
            # For avg, we might use two inputs or previous and current
            if previous_input and current_input:
                num1 = float(previous_input)
                num2 = float(current_input)
                average = (num1 + num2) / 2
                current_input = str(round(average, 2))
                smart_suggestions = ["Average calculated"]
            else:
                error_message = "Enter two numbers for average"
        
        elif label == "Save":
            income = get_input_value("field_0")
            if income is None:
                if current_input:
                    income = float(current_input)
                else:
                    error_message = "Enter income in Base Amount field or display"
                    return
            
            save_10 = income * 0.10
            save_20 = income * 0.20
            save_30 = income * 0.30
            
            smart_suggestions = [
                f"Save 10%: ${save_10:.2f}",
                f"Save 20%: ${save_20:.2f}",
                f"Save 30%: ${save_30:.2f}"
            ]
            set_input_value("field_0", str(income))
        
        elif label == "Goal":
            target = get_input_value("field_2")
            current_saved = get_input_value("field_3")
            
            if target is None or current_saved is None:
                error_message = "Enter Target Goal and Current in input fields"
                return
            
            if target <= 0:
                error_message = "Goal must be positive"
                return
            
            progress = (current_saved / target) * 100
            current_input = f"{progress:.1f}%"
            smart_suggestions = [f"Progress: {progress:.1f}% of ${target:.2f}"]
            set_input_value("field_2", str(target))
            set_input_value("field_3", str(current_saved))
    
    except ValueError:
        error_message = "Invalid number format"
    except Exception as e:
        error_message = f"Error: {str(e)[:30]}"

def handle_cooking_function(label):
    """Handle cooking-specific functions using input fields"""
    global current_input, error_message, smart_suggestions, previous_input
    
    try:
        amount = get_input_value("field_0")
        servings = get_input_value("field_1")
        temperature = get_input_value("field_2")
        scale = get_input_value("field_3")
        
        if label == "½":
            if amount is None:
                if current_input:
                    amount = float(current_input)
                else:
                    error_message = "Enter amount in Amount field or display"
                    return
            
            current_input = str(round(amount / 2, 3)).rstrip('0').rstrip('.')
            smart_suggestions = ["2×", "⅓", "¼"]
            set_input_value("field_0", current_input)
            set_input_value("field_3", "0.5")
        
        elif label == "⅓":
            if amount is None:
                if current_input:
                    amount = float(current_input)
                else:
                    error_message = "Enter amount in Amount field or display"
                    return
            
            current_input = str(round(amount / 3, 3)).rstrip('0').rstrip('.')
            smart_suggestions = ["½", "¼", "2×"]
            set_input_value("field_0", current_input)
            set_input_value("field_3", "0.333")
        
        elif label == "¼":
            if amount is None:
                if current_input:
                    amount = float(current_input)
                else:
                    error_message = "Enter amount in Amount field or display"
                    return
            
            current_input = str(round(amount / 4, 3)).rstrip('0').rstrip('.')
            smart_suggestions = ["½", "⅓", "2×"]
            set_input_value("field_0", current_input)
            set_input_value("field_3", "0.25")
        
        elif label == "2×":
            if amount is None:
                if current_input:
                    amount = float(current_input)
                else:
                    error_message = "Enter amount in Amount field or display"
                    return
            
            current_input = str(round(amount * 2, 3)).rstrip('0').rstrip('.')
            smart_suggestions = ["½", "⅓", "3×"]
            set_input_value("field_0", current_input)
            set_input_value("field_3", "2")
        
        elif label == "3×":
            if amount is None:
                if current_input:
                    amount = float(current_input)
                else:
                    error_message = "Enter amount in Amount field or display"
                    return
            
            current_input = str(round(amount * 3, 3)).rstrip('0').rstrip('.')
            smart_suggestions = ["½", "⅓", "2×"]
            set_input_value("field_0", current_input)
            set_input_value("field_3", "3")
        
        elif label == "°C/°F":
            if temperature is None:
                if current_input:
                    temp = float(current_input)
                else:
                    error_message = "Enter temperature in Temperature field or display"
                    return
            else:
                temp = temperature
            
            # Check if input might already be °F (high temp)
            if temp > 100:  # Likely °F
                converted = (temp - 32) * 5/9
                current_input = f"{converted:.1f}°C"
                smart_suggestions = ["Converted °F to °C"]
                set_input_value("field_2", current_input)
            else:  # Likely °C
                converted = (temp * 9/5) + 32
                current_input = f"{converted:.1f}°F"
                smart_suggestions = ["Converted °C to °F"]
                set_input_value("field_2", current_input)
    
    except ValueError:
        error_message = "Invalid number format"
    except ZeroDivisionError:
        error_message = "Cannot divide by zero"
    except Exception as e:
        error_message = f"Error: {str(e)[:30]}"

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
        
        if result.is_integer():
            current_input = str(int(result))
        else:
            current_input = str(round(result, 10)).rstrip('0').rstrip('.')
    
    except ValueError:
        error_message = "Error: Invalid input"
    except Exception as e:
        error_message = f"Error: {str(e)}"

def handle_input_field_click(mouse_pos):
    """Handle clicks on input fields"""
    global active_input_field
    
    for field_id, field in input_fields.items():
        if field["rect"].collidepoint(mouse_pos):
            active_input_field = field_id
            return True
    
    active_input_field = None
    return False

def handle_keypress_in_input(event):
    """Handle keyboard input for active input field"""
    global active_input_field, input_field_values
    
    if active_input_field is None:
        return False
    
    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
        # Apply the value from input field to calculator
        value = input_field_values.get(active_input_field, "")
        if value:
            try:
                # Set the current input to the field value
                current_value = float(value)
                # You might want to do something with this value
                # For now, just clear the active field
                active_input_field = None
                return True
            except:
                pass
        active_input_field = None
        return True
    
    elif event.key == pygame.K_BACKSPACE:
        current_value = input_field_values.get(active_input_field, "")
        input_field_values[active_input_field] = current_value[:-1]
        return True
    
    elif event.key == pygame.K_ESCAPE:
        active_input_field = None
        return True
    
    elif event.unicode.isdigit() or event.unicode == '.':
        current_value = input_field_values.get(active_input_field, "")
        # Allow only one decimal point
        if event.unicode == '.' and '.' in current_value:
            return True
        input_field_values[active_input_field] = current_value + event.unicode
        return True
    
    elif event.unicode == '-':
        current_value = input_field_values.get(active_input_field, "")
        # Allow minus only at the beginning
        if not current_value.startswith('-'):
            input_field_values[active_input_field] = '-' + current_value
        return True
    
    return False

# Main game loop
def main():
    global current_context, smart_suggestions, calculation_pattern, current_input
    global previous_input, current_operator, result, error_message, active_input_field
    
    running = True
    
    # Load initial context data
    load_context_data()
    initialize_input_fields()
    
    print(f"\nCalculator started with screen size: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
    print("Features:")
    print("  - Left panel: Calculator buttons")
    print("  - Right panel: Context-specific input fields")
    print("  - Click input fields to enter values")
    print("  - Press Enter to apply input field values")
    print("  - Close window to exit")
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                # Handle input field typing first
                if handle_keypress_in_input(event):
                    continue
                
                # Keyboard support for calculator
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_BACKSPACE:
                    if current_input:
                        current_input = current_input[:-1]
                    elif error_message:
                        error_message = ""
                elif event.key == pygame.K_c:
                    current_input = ""
                    previous_input = ""
                    current_operator = ""
                    result = None
                    error_message = ""
                    smart_suggestions.clear()
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    if previous_input and current_operator and current_input:
                        calculate_result()
                        if not error_message:
                            previous_input = ""
                            current_operator = ""
                elif pygame.K_0 <= event.key <= pygame.K_9:
                    current_input += chr(event.key)
                elif event.key == pygame.K_PERIOD or event.key == pygame.K_KP_PERIOD:
                    if "." not in current_input:
                        current_input += "."
                elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                    button = {"label": "+", "type": "operator"}
                    handle_button_click(button)
                elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    button = {"label": "-", "type": "operator"}
                    handle_button_click(button)
                elif event.key == pygame.K_ASTERISK or event.key == pygame.K_KP_MULTIPLY:
                    button = {"label": "×", "type": "operator"}
                    handle_button_click(button)
                elif event.key == pygame.K_SLASH or event.key == pygame.K_KP_DIVIDE:
                    button = {"label": "/", "type": "operator"}
                    handle_button_click(button)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # First check input fields
                    if handle_input_field_click(mouse_pos):
                        continue
                    
                    # Check context mode buttons
                    mode_button_width = min(100, ((SCREEN_WIDTH - INPUT_PANEL_WIDTH) - 20) // len(CONTEXT_MODES) - 10)
                    mode_button_height = 35
                    mode_x = ((SCREEN_WIDTH - INPUT_PANEL_WIDTH) - (len(CONTEXT_MODES) * (mode_button_width + 10))) // 2
                    
                    context_switched = False
                    for i, mode_name in enumerate(CONTEXT_MODES.keys()):
                        btn_rect = pygame.Rect(mode_x, DISPLAY_HEIGHT + 60, mode_button_width, mode_button_height)
                        if btn_rect.collidepoint(mouse_pos):
                            print(f"Clicked context mode: {mode_name}")
                            current_context = mode_name
                            initialize_input_fields()
                            smart_suggestions.clear()
                            calculation_pattern.clear()
                            
                            current_input = ""
                            previous_input = ""
                            current_operator = ""
                            result = None
                            error_message = ""
                            
                            if current_context == "Shopping":
                                smart_suggestions = ["Tip 15%", "Add Tax", "Split Bill", "Total"]
                            elif current_context == "Homework":
                                smart_suggestions = ["π", "√", "sin()", "cos()", "tan()"]
                            elif current_context == "Budgeting":
                                smart_suggestions = ["% Increase", "% Decrease", "Average", "Save"]
                            elif current_context == "Cooking":
                                smart_suggestions = ["½ Recipe", "2× Recipe", "Convert Units", "°C to °F"]
                            else:
                                smart_suggestions = []
                            
                            context_switched = True
                            break
                        mode_x += mode_button_width + 10
                    
                    if not context_switched:
                        buttons = get_buttons_for_context()
                        for button in buttons:
                            if button["rect"].collidepoint(mouse_pos):
                                handle_button_click(button)
                                break
        
        # Draw everything
        screen.fill(BACKGROUND_COLOR)
        draw_display()
        draw_context_panel()
        draw_input_panel()
        draw_buttons()
        
        # Update display
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()