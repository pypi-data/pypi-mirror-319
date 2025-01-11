# Flux Agents

A modern, async-first framework for building AI agents with integrated LLM capabilities and vector operations. Flux provides a clean, type-safe API for building complex AI agents with built-in support for async operations, vector embeddings, and comprehensive monitoring.

## Key Features

- 🚀 **Async-First**: Built on asyncio for high-performance, non-blocking operations
- 🤖 **Multiple Agent Types**: ReAct, Planning, and Hierarchical agents for different use cases
- 🔍 **Vector Operations**: Integrated embedding generation and similarity search
- 📊 **Monitoring**: Built-in logging with LangFuse integration
- 🔄 **Flexible LLM Support**: Easy integration with various LLM providers

## Installation

```bash
# Basic installation
pip install flux-agents

# With local embedding support
pip install flux-agents[torch]

# With development tools
pip install flux-agents[dev]
```

## Quick Start

Here's a simple example showing how to create and use a ReAct agent:

```python
from flux_agents import (
    LLM, ReActAgent, Message, AgentConfig,
    EmbeddingModel, Tool, Logging
)
import asyncio

# Initialize LLM
llm = LLM(
    inference_fn="<llm_inference_fn>",  # Your LLM inference function
    model_name="<model_name>",          # e.g., "gemini-pro"
    max_tokens=2000
)

# Initialize embedding model
embeddings = EmbeddingModel(
    model_fn="<embedding_fn>",          # Your embedding function
    dimension=384
)

# Define a tool
def search_tool(query: str) -> str:
    """Search for information."""
    return "<search_results>"

tool = Tool(
    function=search_tool,
    name="search",
    description="Search for information"
)

# Create agent
agent = ReActAgent(
    name="Assistant",
    llm=llm,
    embedding_function=embeddings,
    config=AgentConfig(
        logging=Logging.ENABLED,
        search_context=True
    )
)

# Add tool
await agent.add_tool(tool)

# Synchronous usage
response = agent.sync_call(
    "What is the capital of France?",
    metadata={"context": "geography"}
)
print(f"Response: {response.content}")

# Asynchronous usage
async def process_queries():
    queries = [
        Message("What is Python?"),
        Message("Explain asyncio")
    ]
    
    # Process concurrently
    responses = await asyncio.gather(*[
        agent(query) for query in queries
    ])
    
    for query, response in zip(queries, responses):
        print(f"Q: {query.content}")
        print(f"A: {response.content}\n")

# Run async
if __name__ == "__main__":
    asyncio.run(process_queries())
```

## Advanced Usage

Here's how to create a hierarchical agent for complex tasks:

```python
from flux_agents import HierarchicalAgent, HierarchicalConfig

agent = HierarchicalAgent(
    name="Project Manager",
    llm=llm,
    embedding_function=embeddings,
    config=HierarchicalConfig(
        worker_count=3,
        worker_type="mixed",
        logging=Logging.LANGFUSE
    )
)

async def complex_task():
    response = await agent(
        Message(
            content="Analyze and summarize these documents",
            files=[doc1, doc2],
            metadata={"priority": "high"}
        )
    )
    return response

result = asyncio.run(complex_task())
```

## Documentation

For detailed documentation, visit our [Documentation](https://tiger1def.github.io/Flux/).

## Contributing

Contributions are welcome! Please see our [Contributing Guide](CONTRIBUTING.md).

## License

Copyright 2024 Flux AI

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.