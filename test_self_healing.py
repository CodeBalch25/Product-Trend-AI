"""
Test Self-Healing System
This script intentionally creates errors to test the autonomous healing system
"""

def test_key_error():
    """Test KeyError detection and auto-fix"""
    print("🧪 TEST 1: KeyError - Should auto-fix by replacing dict[key] with dict.get()")

    # This will cause a KeyError
    test_data = {"name": "Product", "price": 99.99}

    try:
        # Intentional KeyError - missing 'category' key
        category = test_data['category']  # KeyError!
        print(f"Category: {category}")
    except KeyError as e:
        print(f"❌ KeyError detected: {e}")
        print(f"   Line: test_data['category']")
        print(f"   Expected fix: test_data.get('category', 'Unknown')")
        raise  # Re-raise to get full traceback in logs


def test_attribute_error():
    """Test AttributeError detection and auto-fix"""
    print("\n🧪 TEST 2: AttributeError - Should auto-fix by adding hasattr check")

    class Product:
        def __init__(self):
            self.name = "Test Product"
            self.price = 49.99
            # Note: NO 'description' attribute

    product = Product()

    try:
        # Intentional AttributeError - no 'description' attribute
        desc = product.description  # AttributeError!
        print(f"Description: {desc}")
    except AttributeError as e:
        print(f"❌ AttributeError detected: {e}")
        print(f"   Line: product.description")
        print(f"   Expected fix: getattr(product, 'description', '')")
        raise  # Re-raise for traceback


def test_validation_error():
    """Test validation error detection"""
    print("\n🧪 TEST 3: Validation Error - Should detect and suggest schema update")

    # Simulate validation failure
    data = {"price": -50}  # Invalid: negative price

    if data['price'] < 0:
        error_msg = "ValidationError: Price cannot be negative"
        print(f"❌ {error_msg}")
        raise ValueError(error_msg)


def test_missing_field():
    """Test missing required field"""
    print("\n🧪 TEST 4: Missing Required Field - Should add defaults")

    # Simulate missing required field
    product_data = {
        "title": "Smart Watch",
        # Missing: 'ai_description' (required field)
    }

    if 'ai_description' not in product_data:
        error_msg = "missing required field: 'ai_description'"
        print(f"❌ Error: {error_msg}")
        raise KeyError(error_msg)


if __name__ == "__main__":
    print("="*80)
    print("🤖 SELF-HEALING SYSTEM DEMONSTRATION")
    print("   Testing error detection and auto-fix capabilities")
    print("="*80 + "\n")

    # Run tests - each will generate errors
    tests = [
        ("KeyError", test_key_error),
        ("AttributeError", test_attribute_error),
        ("Validation Error", test_validation_error),
        ("Missing Field", test_missing_field)
    ]

    for test_name, test_func in tests:
        try:
            test_func()
        except Exception as e:
            print(f"   ✓ Error logged for autonomous detection\n")
            continue  # Continue to next test

    print("="*80)
    print("✅ All test errors generated!")
    print("   Errors are now in logs for autonomous health check to detect")
    print("="*80)
