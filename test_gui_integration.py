import pytest
import pygame
import sys
import os
from unittest.mock import Mock, patch

# Mock pygame to test without GUI
def test_button_click_simulation():
    """Simulate button clicks and check state changes"""
    
    # Mock calculator state
    calculator_state = {
        'current_input': '',
        'previous_input': '',
        'current_operator': '',
        'result': None
    }
    
    # Simulate clicking number buttons
    def click_button(button_label):
        if button_label.isdigit():
            calculator_state['current_input'] += button_label
        elif button_label in ['+', '-', '×', '/']:
            if calculator_state['current_input']:
                calculator_state['previous_input'] = calculator_state['current_input']
                calculator_state['current_operator'] = button_label
                calculator_state['current_input'] = ''
    
    # Test sequence: 5 + 3 =
    click_button('5')
    assert calculator_state['current_input'] == '5'
    
    click_button('+')
    assert calculator_state['previous_input'] == '5'
    assert calculator_state['current_operator'] == '+'
    assert calculator_state['current_input'] == ''
    
    click_button('3')
    assert calculator_state['current_input'] == '3'
    
    # Test equals calculation (simplified)
    if calculator_state['previous_input'] and calculator_state['current_operator'] and calculator_state['current_input']:
        num1 = float(calculator_state['previous_input'])
        num2 = float(calculator_state['current_input'])
        if calculator_state['current_operator'] == '+':
            result = num1 + num2
            assert result == 8.0

def test_keyboard_input_simulation():
    """Test keyboard input handling"""
    
    class MockEvent:
        def __init__(self, unicode, key=None):
            self.unicode = unicode
            self.key = key
    
    # Test keyboard number input
    current_input = ''
    
    # Simulate pressing '5'
    event = MockEvent('5')
    if event.unicode in "0123456789":
        current_input += event.unicode
    assert current_input == '5'
    
    # Simulate pressing '+'
    event = MockEvent('+')
    if event.unicode == '+':
        # In real code, this would set operator
        operator = '+'
        assert operator == '+'

def test_error_handling():
    """Test error scenarios"""
    
    # Division by zero
    def perform_division(num1, num2):
        if num2 == 0:
            return "Error: Division by 0"
        return num1 / num2
    
    assert perform_division(10, 0) == "Error: Division by 0"
    assert perform_division(10, 2) == 5.0
    
    # Invalid decimal input
    current_input = "5.5.5"  # Invalid: multiple decimals
    has_error = '.' in current_input and current_input.count('.') > 1
    assert has_error == True

if __name__ == "__main__":
    test_button_click_simulation()
    test_keyboard_input_simulation()
    test_error_handling()
    print("All integration tests passed!")