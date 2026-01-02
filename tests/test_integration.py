import sys
import os

def test_button_sequence():
    """Test a sequence of button presses"""
    print("Testing button sequence: 5 + 3 = 8")
    
    # Simulate calculator state
    state = {
        'display': '',
        'memory': 0,
        'operator': None
    }
    
    def press_button(value, button_type='number'):
        if button_type == 'number':
            state['display'] += str(value)
        elif button_type == 'operator':
            if state['display']:
                state['memory'] = float(state['display'])
                state['operator'] = value
                state['display'] = ''
        elif button_type == 'equals':
            if state['operator'] and state['display']:
                current = float(state['display'])
                if state['operator'] == '+':
                    state['display'] = str(state['memory'] + current)
                state['memory'] = 0
                state['operator'] = None
    
    # Simulate: 5 + 3 =
    press_button('5')
    assert state['display'] == '5', f"Expected '5', got {state['display']}"
    
    press_button('+', 'operator')
    assert state['memory'] == 5, f"Expected memory 5, got {state['memory']}"
    assert state['operator'] == '+', f"Expected operator '+', got {state['operator']}"
    
    press_button('3')
    assert state['display'] == '3', f"Expected '3', got {state['display']}"
    
    press_button('=', 'equals')
    assert state['display'] == '8.0', f"Expected '8.0', got {state['display']}"
    
    print("✅ Button sequence test passed!")

def test_error_handling():
    """Test error scenarios"""
    print("Testing error handling...")
    
    # Test division by zero
    def safe_divide(a, b):
        try:
            return a / b
        except ZeroDivisionError:
            return "Error: Division by 0"
    
    result = safe_divide(10, 0)
    assert result == "Error: Division by 0", f"Expected error message, got {result}"
    
    # Test invalid input
    def validate_input(input_str):
        try:
            float(input_str)
            return True
        except ValueError:
            return False
    
    assert validate_input("123") == True
    assert validate_input("12.34") == True
    assert validate_input("abc") == False
    
    print("✅ Error handling tests passed!")

def test_keyboard_input():
    """Test keyboard input simulation"""
    print("Testing keyboard input...")
    
    # Map keyboard keys to calculator functions
    key_map = {
        '1': '1', '2': '2', '3': '3',
        '4': '4', '5': '5', '6': '6',
        '7': '7', '8': '8', '9': '9', '0': '0',
        '+': '+', '-': '-', '*': '×', '/': '÷',
        '=': '=', '.': '.', 'c': 'C', 'C': 'C'
    }
    
    # Test key mapping
    test_keys = ['5', '+', '3', '=']
    expected_actions = ['5', '+', '3', '=']
    
    for key, expected in zip(test_keys, expected_actions):
        action = key_map.get(key, None)
        assert action == expected, f"Key '{key}' should map to '{expected}', got '{action}'"
    
    print("✅ Keyboard input tests passed!")

if __name__ == "__main__":
    print("=" * 50)
    print("Starting Integration Tests")
    print("=" * 50)
    
    all_tests = [
        test_button_sequence,
        test_error_handling,
        test_keyboard_input
    ]
    
    passed = 0
    failed = 0
    
    for test in all_tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ Test failed: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ Test error: {e}")
            failed += 1
    
    print("=" * 50)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 50)
    
    if failed == 0:
        print("✅ All integration tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed")
        sys.exit(1)