#!/usr/bin/env python3
"""
Test script to verify the project structure and basic imports
This test doesn't require API keys
"""

import sys
import os

# Add src to path
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.insert(0, src_path)

def test_imports():
    """Test that all modules can be imported"""
    print("Testing module imports...")
    
    # Set a dummy API key for testing
    os.environ['GEMINI_API_KEY'] = 'test_key_for_import_only'
    
    try:
        from ternarius_atlas import EbookGenerator
        print("✅ Main module imported successfully")
    except Exception as e:
        print(f"❌ Failed to import main module: {e}")
        return False
    
    try:
        from ternarius_atlas.text_generator import TextGenerator
        print("✅ TextGenerator imported successfully")
    except Exception as e:
        print(f"❌ Failed to import TextGenerator: {e}")
        return False
    
    try:
        from ternarius_atlas.image_generator import ImageGenerator
        print("✅ ImageGenerator imported successfully")
    except Exception as e:
        print(f"❌ Failed to import ImageGenerator: {e}")
        return False
    
    try:
        from ternarius_atlas.page_composer import PageComposer
        print("✅ PageComposer imported successfully")
    except Exception as e:
        print(f"❌ Failed to import PageComposer: {e}")
        return False
    
    return True


def test_page_composer():
    """Test page composer without requiring API"""
    print("\nTesting page composer...")
    
    try:
        # Set a dummy API key for testing (won't be used in this test)
        os.environ['GEMINI_API_KEY'] = 'test_key_not_used'
        
        from ternarius_atlas.page_composer import PageComposer
        from ternarius_atlas.config import Config
        
        config = Config()
        composer = PageComposer(config)
        
        # Create a simple title page
        title_page = composer.create_title_page(
            title="Test E-book",
            author="Test Author"
        )
        
        print(f"✅ Title page created: {title_page.size}")
        
        # Create a simple content page
        content_page = composer.create_page(
            text="This is a test page content. " * 20,
            page_number=1,
            title="Test Chapter"
        )
        
        print(f"✅ Content page created: {content_page.size}")
        
        return True
        
    except Exception as e:
        print(f"❌ Page composer test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_image_generator():
    """Test image generator placeholder functionality"""
    print("\nTesting image generator (placeholder mode)...")
    
    try:
        os.environ['GEMINI_API_KEY'] = 'test_key_not_used'
        
        from ternarius_atlas.image_generator import ImageGenerator
        
        generator = ImageGenerator()
        
        # Generate a placeholder image
        img = generator.generate_image("Test prompt", 512, 512)
        
        if img:
            print(f"✅ Placeholder image generated: {img.size}")
            return True
        else:
            print("❌ Image generation returned None")
            return False
            
    except Exception as e:
        print(f"❌ Image generator test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 Running Ternarius Atlas Tests")
    print("=" * 60)
    
    results = []
    
    # Test imports
    results.append(("Import Test", test_imports()))
    
    # Test page composer
    results.append(("Page Composer Test", test_page_composer()))
    
    # Test image generator
    results.append(("Image Generator Test", test_image_generator()))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print("\n⚠️  Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
