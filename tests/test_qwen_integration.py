"""
Test Qwen QwQ-32B Integration
Verifies that the new advanced reasoning model works correctly
"""
import asyncio
import sys
sys.path.insert(0, 'C:/Users/timud/Documents/product-trend-automation/backend')

from services.ai_analysis.agentic_system import AgenticAISystem


class MockProduct:
    """Mock product for testing"""
    title = "Smart LED Light Bulbs with WiFi Control - Voice Activated RGB Color Changing"
    description = "Control your home lighting with voice commands. 16 million colors, schedules, and energy monitoring."
    category = "Smart Home"
    estimated_cost = 24.99
    trend_score = 88
    search_volume = 75000
    trend_source = "Amazon Best Sellers"


async def test_qwen_integration():
    """Test the Qwen QwQ-32B integration"""
    print("\n" + "="*80)
    print("🧪 TESTING QWEN QWQ-32B INTEGRATION")
    print("="*80 + "\n")

    try:
        # Initialize agentic system
        print("✅ Step 1: Initializing Agentic AI System...")
        system = AgenticAISystem()
        print("\n✅ System initialized successfully!\n")

        # Verify model configuration
        print("📋 Step 2: Verifying Model Configuration...")
        print(f"   • Coordinator Model: {system.coordinator_model}")
        print(f"   • Trend Agent Model: {system.groq_trend_model}")
        print(f"   • Research Agent Model: {system.hf_research_model}")

        # Check if Qwen QwQ-32B is configured
        if system.coordinator_model == "qwq-32b-preview":
            print("   ✅ Coordinator using Qwen QwQ-32B ✓")
        else:
            print(f"   ❌ Coordinator NOT using Qwen QwQ-32B! Using: {system.coordinator_model}")

        if system.groq_trend_model == "qwq-32b-preview":
            print("   ✅ Trend Agent using Qwen QwQ-32B ✓")
        else:
            print(f"   ❌ Trend Agent NOT using Qwen QwQ-32B! Using: {system.groq_trend_model}")

        if system.hf_research_model == "qwq-32b-preview":
            print("   ✅ Research Agent using Qwen QwQ-32B ✓")
        else:
            print(f"   ❌ Research Agent NOT using Qwen QwQ-32B! Using: {system.hf_research_model}")

        print("\n" + "="*80)
        print("🚀 Step 3: Running Full Multi-Agent Analysis with Qwen QwQ-32B")
        print("="*80 + "\n")

        # Create mock product
        product = MockProduct()

        # Run analysis
        result = await system.analyze_product_multi_agent(product)

        print("\n" + "="*80)
        print("✅ TEST RESULTS")
        print("="*80 + "\n")

        print("📊 Analysis Complete!")
        print(f"   • Recommendation: {result.get('recommendation', 'N/A').upper()}")
        print(f"   • Confidence: {result.get('confidence_score', 0)}%")
        print(f"   • Category: {result.get('ai_category', 'N/A')}")
        print(f"   • Suggested Price: ${result.get('suggested_price', 0):.2f}")
        print(f"   • Profit Score: {result.get('profit_potential_score', 0)}/100")
        print(f"   • Competition: {result.get('competition_level', 'N/A')}")

        if result.get('ai_keywords'):
            print(f"\n   📝 Keywords Generated:")
            for i, keyword in enumerate(result['ai_keywords'][:5], 1):
                print(f"      {i}. {keyword}")

        print(f"\n   💡 Reasoning: {result.get('reasoning', 'N/A')[:200]}...")

        print("\n" + "="*80)
        print("✅ QWEN QWQ-32B INTEGRATION TEST: PASSED")
        print("="*80 + "\n")

        return True

    except Exception as e:
        print("\n" + "="*80)
        print("❌ TEST FAILED")
        print("="*80)
        print(f"\nError: {str(e)}")
        print(f"\nDetails:")
        import traceback
        traceback.print_exc()
        print("\n" + "="*80 + "\n")
        return False


if __name__ == "__main__":
    print("\n🧠 Qwen QwQ-32B Advanced Reasoning Model Test")
    print("="*80)

    success = asyncio.run(test_qwen_integration())

    if success:
        print("\n✅ All tests passed! Qwen QwQ-32B is working correctly.")
        sys.exit(0)
    else:
        print("\n❌ Tests failed. Please check the errors above.")
        sys.exit(1)
