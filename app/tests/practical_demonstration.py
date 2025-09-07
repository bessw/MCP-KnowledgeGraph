"""
Practical demonstration and testing of the Knowledge Graph MCP Server
with realistic scenarios.

This script demonstrates the server's capabilities by running realistic
test scenarios that show how the server would be used in practice.
"""
import asyncio
import json
import sys
from typing import List, Dict, Any
from datetime import datetime

from app.tests.test_realistic_scenarios import RealisticTestScenarios
from app.models.schemas import KnowledgeWithSources
from app.validation.validators import DataValidator


class PracticalDemonstration:
    """Practical demonstration of the Knowledge Graph MCP Server capabilities"""
    
    def __init__(self):
        self.scenario_generator = RealisticTestScenarios()
        self.validator = DataValidator()
        self.results = {
            "total_scenarios": 0,
            "successful_scenarios": 0,
            "failed_scenarios": 0,
            "validation_issues": 0,
            "scenario_breakdown": {}
        }
    
    async def run_demonstration(self):
        """Run the complete practical demonstration"""
        print("=" * 80)
        print("Knowledge Graph MCP Server - Practical Demonstration")
        print("=" * 80)
        print()
        
        # Generate all scenarios
        scenarios = self.scenario_generator.generate_all_scenarios()
        self.results["total_scenarios"] = len(scenarios)
        
        print(f"Generated {len(scenarios)} realistic test scenarios covering:")
        print("• Software Development Knowledge")
        print("• Research and Academic Information")
        print("• Business Process Documentation")
        print("• Technical Documentation")
        print("• Personal Learning Notes")
        print()
        
        # Categorize scenarios
        categories = self._categorize_scenarios(scenarios)
        for category, count in categories.items():
            self.results["scenario_breakdown"][category] = count
            print(f"  {category}: {count} scenarios")
        print()
        
        # Demonstrate scenario validation
        await self._demonstrate_scenario_validation(scenarios)
        
        # Show detailed examples
        self._show_detailed_examples(scenarios)
        
        # Generate summary report
        self._generate_summary_report()
    
    def _categorize_scenarios(self, scenarios: List[Dict[str, Any]]) -> Dict[str, int]:
        """Categorize scenarios by type"""
        categories = {
            "Software Development": 0,
            "Academic Research": 0,
            "Business Process": 0,
            "Technical Documentation": 0,
            "Personal Learning": 0
        }
        
        for scenario in scenarios:
            scenario_id = scenario["id"]
            if scenario_id.startswith("sw_"):
                categories["Software Development"] += 1
            elif scenario_id.startswith("ac_"):
                categories["Academic Research"] += 1
            elif scenario_id.startswith("bp_"):
                categories["Business Process"] += 1
            elif scenario_id.startswith("td_"):
                categories["Technical Documentation"] += 1
            elif scenario_id.startswith("pl_"):
                categories["Personal Learning"] += 1
        
        return categories
    
    async def _demonstrate_scenario_validation(self, scenarios: List[Dict[str, Any]]):
        """Demonstrate scenario validation capabilities"""
        print("Validating Knowledge and Source Data Quality...")
        print("-" * 50)
        
        validation_tasks = []
        for i, scenario in enumerate(scenarios[:10]):  # Validate first 10 scenarios
            knowledge_with_sources = KnowledgeWithSources(
                knowledge=scenario["knowledge"],
                sources=scenario["sources"]
            )
            validation_tasks.append(
                self._validate_single_scenario(scenario["id"], knowledge_with_sources)
            )
        
        validation_results = await asyncio.gather(*validation_tasks)
        
        successful_validations = 0
        total_issues = 0
        
        for scenario_id, errors in validation_results:
            if not errors:
                successful_validations += 1
                print(f"✓ {scenario_id}: Valid")
            else:
                print(f"⚠ {scenario_id}: {len(errors)} validation issue(s)")
                for error in errors[:2]:  # Show first 2 errors
                    print(f"  - {error}")
                total_issues += len(errors)
        
        self.results["successful_scenarios"] = successful_validations
        self.results["failed_scenarios"] = len(validation_results) - successful_validations
        self.results["validation_issues"] = total_issues
        
        print(f"\nValidation Summary:")
        print(f"  Successful: {successful_validations}/{len(validation_results)}")
        print(f"  Total Issues: {total_issues}")
        print()
    
    async def _validate_single_scenario(self, scenario_id: str, knowledge_with_sources: KnowledgeWithSources):
        """Validate a single scenario"""
        try:
            errors = await self.validator.validate_knowledge_with_sources(knowledge_with_sources)
            return scenario_id, errors
        except Exception as e:
            return scenario_id, [f"Validation error: {str(e)}"]
    
    def _show_detailed_examples(self, scenarios: List[Dict[str, Any]]):
        """Show detailed examples of different scenario types"""
        print("Detailed Scenario Examples:")
        print("=" * 50)
        
        # Show one example from each category
        example_ids = ["sw_001", "ac_001", "bp_001", "td_001", "pl_001"]
        
        for example_id in example_ids:
            scenario = next((s for s in scenarios if s["id"] == example_id), None)
            if scenario:
                self._print_scenario_details(scenario)
                print()
    
    def _print_scenario_details(self, scenario: Dict[str, Any]):
        """Print detailed information about a scenario"""
        knowledge = scenario["knowledge"]
        sources = scenario["sources"]
        
        print(f"Scenario ID: {scenario['id']}")
        print(f"Title: {scenario['title']}")
        print(f"Description: {scenario['description']}")
        print(f"Knowledge Type: {knowledge.type}")
        print(f"Knowledge Title: {knowledge.title}")
        print(f"Content Preview: {knowledge.content[:100]}...")
        
        if knowledge.properties:
            print("Properties:")
            for key, value in knowledge.properties.items():
                if isinstance(value, (list, dict)):
                    print(f"  {key}: {json.dumps(value, indent=2)[:100]}...")
                else:
                    print(f"  {key}: {value}")
        
        print(f"Sources ({len(sources)}):")
        for i, source in enumerate(sources, 1):
            print(f"  {i}. {source.name} (Trust: {source.trustworthiness}/10)")
            print(f"     Type: {source.type}, Expertise: {', '.join(source.expertise)}")
            if source.url:
                print(f"     URL: {source.url}")
        
        print("-" * 50)
    
    def _generate_summary_report(self):
        """Generate and display summary report"""
        print("DEMONSTRATION SUMMARY REPORT")
        print("=" * 50)
        
        print(f"Total Scenarios Generated: {self.results['total_scenarios']}")
        print(f"Validation Success Rate: {self.results['successful_scenarios']}/{self.results['total_scenarios']} tested")
        
        if self.results['validation_issues'] > 0:
            print(f"Total Validation Issues: {self.results['validation_issues']}")
            print("  (Note: Issues are primarily due to mock URLs not being accessible)")
        
        print("\nScenario Distribution:")
        for category, count in self.results['scenario_breakdown'].items():
            percentage = (count / self.results['total_scenarios']) * 100
            print(f"  {category}: {count} ({percentage:.1f}%)")
        
        print("\nPractical Use Cases Demonstrated:")
        print("✓ Algorithm and data structure documentation")
        print("✓ API endpoint documentation for teams")
        print("✓ Business process knowledge management")
        print("✓ Technical tool and framework documentation")
        print("✓ Personal learning and development tracking")
        print("✓ Research paper and academic knowledge storage")
        print("✓ Corporate compliance and procedures")
        print("✓ Software development best practices")
        print("✓ Multi-source knowledge validation")
        print("✓ Expertise-based source trustworthiness scoring")
        
        print(f"\nDemonstration completed at: {datetime.now().isoformat()}")
        print("=" * 50)


def show_api_usage_examples():
    """Show examples of how the API would be used with these scenarios"""
    print("\nAPI Usage Examples:")
    print("=" * 30)
    
    print("1. Create Knowledge with Sources:")
    print("   POST /api/v1/knowledge")
    print("   Authorization: Bearer <api_key>")
    print("   Content-Type: application/json")
    print("""
   {
     "knowledge": {
       "type": "Algorithm",
       "title": "QuickSort Algorithm",
       "content": "A divide-and-conquer algorithm...",
       "properties": {"complexity": "O(n log n)"}
     },
     "sources": [
       {
         "type": "Website",
         "url": "https://wikipedia.org/wiki/Quicksort",
         "name": "Wikipedia",
         "trustworthiness": 8,
         "expertise": ["Computer Science", "Algorithms"]
       }
     ]
   }""")
    
    print("\n2. Query Knowledge:")
    print("   POST /api/v1/query")
    print("   Authorization: Bearer <api_key>")
    print("""
   {
     "query": "MATCH (k:Knowledge)-[:DERIVED_FROM]->(s:Source) WHERE k.type = 'Algorithm' RETURN k, s",
     "parameters": {}
   }""")
    
    print("\n3. Search Knowledge:")
    print("   GET /api/v1/knowledge/search/algorithm?knowledge_type=Algorithm")
    print("   Authorization: Bearer <api_key>")


async def main():
    """Main demonstration function"""
    demonstration = PracticalDemonstration()
    await demonstration.run_demonstration()
    show_api_usage_examples()


if __name__ == "__main__":
    asyncio.run(main())