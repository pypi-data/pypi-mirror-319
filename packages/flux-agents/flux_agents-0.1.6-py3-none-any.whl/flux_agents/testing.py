"""
Test runner for flux_agents package.
"""

from deployment.config import initialize_environment
initialize_environment()

import asyncio
import logging
import os
import sys
import traceback

# Add the package root to Python path
package_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, package_root)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import test functions using absolute imports
from flux_agents.tests.embeddings import (
    test_embeddings,
    test_embeddings_store,
    test_file_operations
)
from flux_agents.tests.llm import test_llm
from flux_agents.tests.agents import (
    test_base_agent,
    test_agent_serialization,
    test_react_agent,
    test_planning_agent,
    test_hierarchical_agent
)


async def run_async_tests():
    """Run all async tests."""
    await test_file_operations()
    await test_hierarchical_agent()


def run_sync_tests():
    """Run all synchronous tests."""
    # Embedding tests
    print("\n1. Testing Embeddings")
    print("-" * 50)
    test_embeddings()
    test_embeddings_store()

    # LLM tests
    print("\n2. Testing LLM")
    print("-" * 50)
    test_llm()

    # Agent tests
    print("\n3. Testing Agents")
    print("-" * 50)
    test_base_agent()
    test_agent_serialization()
    test_react_agent()
    test_planning_agent()


def run_tests():
    """Run all tests."""
    print("\n=== Running All Tests ===")
    print("=" * 50)
    
    try:
        # Run sync tests
        run_sync_tests()
        
        # Run async tests
        asyncio.run(run_async_tests())
        
        print("\n=== All Tests Complete ===")
        return True
    except:
        error = traceback.format_exc()
        print(f"\n❌ Tests failed: {error}")
        return False


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
