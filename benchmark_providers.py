"""
Benchmark script to test all AI providers and measure performance.

This script runs healing tests with each provider and collects metrics:
- Response time
- Healing success rate
- Locator quality
"""

import time
import json
import os
from datetime import datetime
from playwright.sync_api import sync_playwright
from ai_playwright import AIPage
from ai_playwright.core.healer import HealerAgent


class ProviderBenchmark:
    """Benchmark runner for AI providers"""
    
    def __init__(self):
        self.results = []
        
    def test_provider(self, provider_name, model=None):
        """Test a specific provider and collect metrics"""
        print(f"\n{'='*60}")
        print(f"Testing Provider: {provider_name.upper()}")
        if model:
            print(f"Model: {model}")
        print(f"{'='*60}")
        
        try:
            start_time = time.time()
            
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context()
                page = context.new_page()
                
                # Configure AI page with specific provider
                ai_page = AIPage(page)
                ai_page.healer = HealerAgent(provider=provider_name, model=model)
                ai_page.original_page.set_default_timeout(30000)
                
                # Navigate to test page
                ai_page.goto("https://example.com")
                
                # Attempt action that will trigger healing
                healing_start = time.time()
                try:
                    ai_page.get_by_role("link", name="More information").click()
                    healing_time = time.time() - healing_start
                    success = True
                    error = None
                except Exception as e:
                    healing_time = time.time() - healing_start
                    success = False
                    error = str(e)
                
                total_time = time.time() - start_time
                
                # Verify navigation
                if success:
                    final_url = ai_page.url
                    success = "iana" in final_url.lower()
                
                browser.close()
            
            # Record results
            result = {
                "provider": provider_name,
                "model": model or "default",
                "timestamp": datetime.now().isoformat(),
                "success": success,
                "total_time": round(total_time, 2),
                "healing_time": round(healing_time, 2),
                "error": error
            }
            
            self.results.append(result)
            
            # Print result
            status = "✅ PASSED" if success else "❌ FAILED"
            print(f"Status: {status}")
            print(f"Total Time: {total_time:.2f}s")
            print(f"Healing Time: {healing_time:.2f}s")
            if error:
                print(f"Error: {error[:100]}...")
            
            return result
            
        except Exception as e:
            print(f"❌ FAILED: {str(e)[:100]}")
            result = {
                "provider": provider_name,
                "model": model or "default",
                "timestamp": datetime.now().isoformat(),
                "success": False,
                "total_time": 0,
                "healing_time": 0,
                "error": str(e)
            }
            self.results.append(result)
            return result
    
    def run_all_benchmarks(self):
        """Run benchmarks for all configured providers"""
        print("\n" + "="*60)
        print("AI PROVIDER BENCHMARK SUITE")
        print("="*60)
        
        # Test Gemini (default)
        if os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"):
            self.test_provider("gemini")
        else:
            print("\n⚠️  Skipping Gemini - No API key found")
        
        # Test OpenAI
        if os.getenv("OPENAI_API_KEY"):
            self.test_provider("openai", "gpt-4o-mini")
            # Optionally test other models
            # self.test_provider("openai", "gpt-4o")
        else:
            print("\n⚠️  Skipping OpenAI - No API key found")
        
        # Test Anthropic
        if os.getenv("ANTHROPIC_API_KEY"):
            self.test_provider("anthropic", "claude-3-5-sonnet-20241022")
        else:
            print("\n⚠️  Skipping Anthropic - No API key found")
        
        # Test Azure OpenAI
        if os.getenv("AZURE_OPENAI_API_KEY") and os.getenv("AZURE_OPENAI_ENDPOINT"):
            self.test_provider("azure")
        else:
            print("\n⚠️  Skipping Azure OpenAI - No credentials found")
        
        # Test Ollama (if running locally)
        try:
            import requests
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            if response.status_code == 200:
                self.test_provider("ollama", "llama3")
            else:
                print("\n⚠️  Skipping Ollama - Server not responding")
        except:
            print("\n⚠️  Skipping Ollama - Server not running")
    
    def generate_report(self):
        """Generate benchmark report"""
        print("\n" + "="*60)
        print("BENCHMARK RESULTS SUMMARY")
        print("="*60)
        
        # Summary table
        print(f"\n{'Provider':<15} {'Model':<30} {'Status':<10} {'Time (s)':<12} {'Healing (s)'}")
        print("-" * 80)
        
        for result in self.results:
            status = "✅ PASS" if result["success"] else "❌ FAIL"
            print(f"{result['provider']:<15} {result['model']:<30} {status:<10} "
                  f"{result['total_time']:<12.2f} {result['healing_time']:.2f}")
        
        # Statistics
        successful = [r for r in self.results if r["success"]]
        if successful:
            avg_time = sum(r["total_time"] for r in successful) / len(successful)
            avg_healing = sum(r["healing_time"] for r in successful) / len(successful)
            fastest = min(successful, key=lambda x: x["total_time"])
            
            print(f"\n{'='*60}")
            print("STATISTICS")
            print(f"{'='*60}")
            print(f"Total Tests: {len(self.results)}")
            print(f"Passed: {len(successful)}")
            print(f"Failed: {len(self.results) - len(successful)}")
            print(f"Success Rate: {len(successful)/len(self.results)*100:.1f}%")
            print(f"\nAverage Total Time: {avg_time:.2f}s")
            print(f"Average Healing Time: {avg_healing:.2f}s")
            print(f"\nFastest Provider: {fastest['provider']} ({fastest['model']}) - {fastest['total_time']:.2f}s")
        
        # Save detailed results
        output_file = "benchmark_results.json"
        with open(output_file, 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "results": self.results,
                "summary": {
                    "total_tests": len(self.results),
                    "passed": len(successful),
                    "failed": len(self.results) - len(successful),
                    "success_rate": len(successful)/len(self.results)*100 if self.results else 0
                }
            }, f, indent=2)
        
        print(f"\n📊 Detailed results saved to: {output_file}")
        
        return self.results


if __name__ == "__main__":
    benchmark = ProviderBenchmark()
    benchmark.run_all_benchmarks()
    benchmark.generate_report()
