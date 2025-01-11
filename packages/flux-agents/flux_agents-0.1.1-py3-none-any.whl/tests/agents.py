"""
Test suite for agent functionality.

This module provides tests for various agent configurations and logging modes,
including Langfuse integration, basic logging, and default operation without logging.
"""
import asyncio
import polars as pl
from typing import Tuple
from datetime import datetime
import polars as pl

from agents import (
    Agent,
    AgentConfig,
    File,
    Logging,
    Message,
    Metadata
)

from agents.agent.react.models import ReActAgent, ReActConfig
from agents.agent.planning.models import PlanningAgent, PlanningConfig
from agents.agent.hierarchical.models import HierarchicalAgent, HierarchicalConfig

from llm import (
    BaseEmbeddingFunction,
    gemini_generate_embedding,
    LLM,
    gemini_llm_async_inference,
    pulse_llm_async_inference
)
from tools.models import Tool


def test_base_agent():
    """
    Test basic agent functionality with different logging configurations.
    
    Tests three configurations:
    1. Agent with Langfuse logging
    2. Agent with basic logging enabled
    3. Agent with logging disabled, using context
    
    Each configuration tests message sending and response handling.
    """
    
    print(f'Testing langfuse langchain agent')
    config = AgentConfig(
        task_prompt = "You must respond like a pirate",
        logging = Logging.LANGFUSE
    )
    
    from llm.embeddings.gemini import _initialize_genai
    _initialize_genai()
    
    llm = LLM(
        gemini_llm_async_inference, 
        input_tokens = 2000, 
        max_tokens = 2000,
        system_prompt = "You must respond like a pirate"
    )
    
    # Create embedding function
    embedding_function = BaseEmbeddingFunction(
        gemini_generate_embedding,
        dimension = 768
    )
    
    agent = Agent(
        name = "Test Agent",
        llm = llm,
        config = config,
        embedding_function = embedding_function
    )
    
    # Verify embedding function propagation
    assert agent.state.embedding_function == embedding_function
    assert agent.state.file_store.embedding_function == embedding_function
    assert agent.state.metadata_store.embedding_function == embedding_function
    
    async def test_agent():
        # Create test data
        test_df = pl.DataFrame({
            "id": range(5),
            "value": ["a", "b", "c", "d", "e"],
            "number": [1.0, 2.0, 3.0, 4.0, 5.0]
        })
        
        # Create metadata object
        metadata = Metadata(
            name="test_data",
            description="Sample test data",
            data=test_df
        )
        
        # Create a test file
        test_file = File.create(
            data="Test file content",
            path="test.txt"
        )
        
        # Create message with direct objects
        message = Message(
            content="Hello, world!",
            metadata=[metadata],  # Direct metadata object
            files=[test_file]    # Direct file object
        )
        
        # Send to agent
        response = await agent(message)
        print(f'Response: {response}')
        
        # Verify ingestion
        stored_metadata = await agent.state.metadata_store.get(metadata.id)
        assert stored_metadata is not None
        assert stored_metadata.name == metadata.name
        
        stored_file = await agent.state.file_store.get_file(test_file.id)
        assert stored_file is not None
        assert stored_file.path == test_file.path
        
        print(f"Response: {response.content}")
        if agent.config.logging != Logging.DISABLED:
            log_text = agent.text()
            print(log_text)

    asyncio.run(test_agent())
    
    print(f'Testing logging agent')
    config = AgentConfig(
        task_prompt = "You must respond like a pirate",
        logging = Logging.ENABLED
    )
    
    agent = Agent(
        name = "Test Agent",
        llm = llm,
        config = config
    )
    
    message = Message(content = "Hello, world!")
    
    async def test_agent():
        """
        Test helper function for running agent tests.
        
        Sends a test message to the agent and prints the log output.
        """
        response = await agent(message)
        output = agent.text()
        print(f'AGENT OUTPUT: {output}')
     
    asyncio.run(test_agent())
    
    
    print(f'Testing default agent')
    config = AgentConfig(
        task_prompt = "You must respond like a pirate",
        logging = Logging.DISABLED
    )
    
    agent = Agent(
        name = "Test Agent",
        llm = llm,
        config = config
    )
    
    message = Message(content = "Hello, world!")
    
    async def test_agent():
        """
        Test helper function for running agent tests.
        
        Sends a test message to the agent and prints the response.
        """
        response = await agent(message)
        print(response)
     
    asyncio.run(test_agent())
    
    
    print("\n=== Testing Base Agent ===")
    
    # Initialize agent
    print("\nInitializing agent...")
    agent = Agent(name="test_agent")
    print(f"✓ Created agent: {agent.name}")
    
    async def test_agent():
        print("\nTesting message processing:")
        message = Message(content="What is two plus two?")
        message_2 = Message(content = 'Why is the specific math problem I asked you about important?')
        message_3 = Message(content = 'Why does that matter?')
        
        try:
            response = await agent(message)
            print(f"✓ Processed message")
            print(f"  Response: {response.content}")
            
            response_2 = await agent(message_2)
            print(f"✓ Processed message 2")
            print(f"  Response: {response_2.content}")
            
            response_3 = await agent(message_3)
            print(f"✓ Processed message 3")
            print(f"  Response: {response_3.content}")
            
        except Exception as e:
            print(f"\nError in agent processing: {str(e)}")
            print(f"Agent state: {agent.agent_status}")
            raise
    
    asyncio.run(test_agent())
    print("\n=== Base Agent Tests Complete ===")


def test_agent_serialization():
    """
    Test agent serialization and deserialization.
    
    Tests:
    1. Message store serialization
    2. File store serialization
    3. Metadata store serialization
    4. Core agent data serialization
    5. Complete state restoration
    """
    import asyncio
    from pathlib import Path
    import shutil
    import polars as pl
    
    from agents import Agent
    from agents.storage.message import Message, Sender
    from agents.storage.metadata import Metadata

    async def _run_test():
        # Create test agent
        agent = Agent(name="TestAgent", type="test")
        
        # Add some test data
        test_message = Message(
            content="Hello, this is a test message",
            sender=Sender.USER
        )
        await agent.state.ingest_message_data(test_message)
        
        # Create a test file
        test_file = await agent.state.create_file(
            "test.txt",
            content="Test file content"
        )
        
        # Add some test metadata
        test_metadata = Metadata(
            name="test_meta",
            description="Test metadata",
            data=pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        )
        await agent.state.add_metadata(test_metadata)
        
        orig_metadata_len = len(agent.state.metadata_store.data)
        
        # Serialize agent
        test_path = Path("test_serialization")
        await agent.serialize(test_path)
    
        # Deserialize to new agent
        loaded_agent = await Agent.deserialize(test_path)
        
        # Verify data
        assert loaded_agent.name == agent.name
        assert loaded_agent.type == agent.type
        
        loaded_metadata_len = len(loaded_agent.state.metadata_store.data)
        
        assert loaded_metadata_len == orig_metadata_len, f"Metadata store length mismatch: {loaded_metadata_len} != {orig_metadata_len}"
        
        # Clean up
        shutil.rmtree(test_path)

    # Run async test in sync context
    asyncio.run(_run_test())


def test_react_agent():
    from agents.state.models import AgentState
    from typing import List
    
    data_frame = pl.DataFrame({
        "tenant_id": [1, 2, 3],
        "user_info": ["Caucasian male 56 years old", "African American female 34 years old", "Caucasian female 23 years old"],
        "tenant_names": ["John", "Jane", "Alice"],
        "user_names": ["Fargas3231", "Mallum5", "CKDKS"]
    })
    
    def select_columns(
        dataframe: pl.DataFrame,
        column_names: List[str]
    ) -> pl.DataFrame:
        """Select and return specific columns from the dataframe.
Returns a new dataframe containing only the requested columns."""
        filtered_df = dataframe.select(column_names)
        return filtered_df
    
    def index_row_info(
        data_frame: pl.DataFrame,
        select_column: str,
        index_value: str
    ) -> str:
        "Indexes a dataframe by the index_value for the select_column"
        row = data_frame.filter(pl.col(select_column) == index_value)
        headers = row.columns
        for row in row.iter_rows():
            formatted_info = " | ".join([f"{key}: {value}" for key, value in zip(headers, row)])
        
        return formatted_info
    
    # Create the tool first
    async def setup_test():
        
        # Create tool with static parameter
        select_tool = Tool(
            function = select_columns,
            name = "select_columns",
        )
      
        index_tool = Tool(
            function = index_row_info,
            name = "index_row_info",
        )
        
        # Create agent
        llm = LLM(
            gemini_llm_async_inference, 
            #pulse_llm_async_inference, 
            model_name = "gemini-1.5-flash", 
            #model_name = "Mixtral-8x22B-Instruct-v0.1",
            input_tokens = 2_000, 
            max_tokens = 2_000,
        )
        
        agent = ReActAgent(
            name = "Test Agent",
            llm = llm,
            config = ReActConfig(
                logging = Logging.LANGFUSE
            )
        )
        
        # Add tool to agent
        await agent.add_tool(select_tool)
        await agent.add_tool(index_tool)
        '''
        # Test the agent - this should fail
        message = Message(
            content = "Please tell me about the complexities of langgraph",
            metadata = [data_frame]
        )
        
        response = await agent(message)
        print(f"Response: {response.content}")
        
        await agent.reset()
        '''
        message = Message(
            content = "Find me the user info for Fargas3231",
            metadata = [data_frame]
        )
        start = datetime.now()
        response = await agent(message)
        end = datetime.now()
        print(f"Response: {response.content}")
        print(f"Time: {end - start}")
    
    response = asyncio.run(setup_test())


def test_planning_agent():
    from typing import List
        
    data_frame = pl.DataFrame({
        "tenant_id": [1, 2, 3],
        "user_info": ["Caucasian male 56 years old", "African American female 34 years old", "Caucasian female 23 years old"],
        "tenant_names": ["John", "Jane", "Alice"],
        "user_names": ["Fargas3231", "Mallum5", "CKDKS"]
    })
    
    def select_columns(
        dataframe: pl.DataFrame,
        column_names: List[str]
    ) -> pl.DataFrame:
        """Select and return specific columns from the dataframe.
Returns a new dataframe containing only the requested columns."""
        filtered_df = dataframe.select(column_names)
        return filtered_df
    
    def index_row_info(
        data_frame: pl.DataFrame,
        select_column: str,
        index_value: str
    ) -> str:
        "Indexes a dataframe by the index_value for the select_column"
        row = data_frame.filter(pl.col(select_column) == index_value)
        headers = row.columns
        for row in row.iter_rows():
            formatted_info = " | ".join([f"{key}: {value}" for key, value in zip(headers, row)])
        
        return formatted_info
    
    # Create the tool first
    async def setup_test():
        
        # Create tool with static parameter
        select_tool = Tool.from_function(select_columns)
        index_tool = Tool(
            function = index_row_info,
            name = "index_row_info",
        )
        
        # Create agent
        llm = LLM(
            #gemini_llm_async_inference, 
            pulse_llm_async_inference, 
            #model_name = "gemini-1.5-flash", 
            model_name = "Mixtral-8x22B-Instruct-v0.1",
            input_tokens = 2_000, 
            max_tokens = 2_000,
        )
        
        agent = PlanningAgent(
            name = "Test Agent",
            llm = llm,
            config = PlanningConfig(
                logging = Logging.LANGFUSE
            )
        )
        
        # Add tool to agent
        await agent.add_tool(select_tool)
        await agent.add_tool(index_tool)  
        
        message = Message(
            content = "Find me the user info for Fargas3231",
            metadata = [data_frame]
        )
        
        start = datetime.now()
        response = await agent(message)
        end = datetime.now()
        print(f"Response: {response.content}")
        print(f"Time: {end - start}")
          
        await agent.reset()
        
        # Test the agent - this should fail
        '''
        message = Message(
            content = "Please tell me about the complexities of langgraph",
            metadata = [data_frame]
        )
        
        response = await agent(message)
        print(f"Response: {response.content}")
        '''
    response = asyncio.run(setup_test())


async def test_hierarchical_agent():
    from typing import List
     
    data_frame = pl.DataFrame({
        "tenant_id": [1, 2, 3],
        "user_info": ["Caucasian male 56 years old", "African American female 34 years old", "Caucasian female 23 years old"],
        "tenant_names": ["John", "Jane", "Alice"],
        "user_names": ["Fargas3231", "Mallum5", "CKDKS"]
    })
    
    def select_columns(
        dataframe: pl.DataFrame,
        column_names: List[str]
    ) -> pl.DataFrame:
        """Select and return specific columns from the dataframe.
Returns a new dataframe containing only the requested columns."""
        filtered_df = dataframe.select(column_names)
        return filtered_df
    
    def index_row_info(
        data_frame: pl.DataFrame,
        select_column: str,
        index_value: str
    ) -> str:
        "Indexes a dataframe by the index_value for the select_column"
        row = data_frame.filter(pl.col(select_column) == index_value)
        headers = row.columns
        for row in row.iter_rows():
            formatted_info = " | ".join([f"{key}: {value}" for key, value in zip(headers, row)])
        
        return formatted_info

    # Create tool with static parameter
    select_tool = Tool.from_function(select_columns)
    index_tool = Tool(
        function = index_row_info,
        name = "index_row_info",
    )
    
    
    # Create agent
    llm = LLM(
        #gemini_llm_async_inference, 
        pulse_llm_async_inference, 
        #model_name = "gemini-1.5-pro", 
        model_name = "Mixtral-8x22B-Instruct-v0.1",
        input_tokens = 2_000, 
        max_tokens = 2_000,
    )
    
    agent = HierarchicalAgent(
        name = "Test Agent",
        llm = llm,
        config = HierarchicalConfig(
            logging = Logging.LANGFUSE,
            search_context = False
        )
    )
    
    # Add tool to agent
    await agent.add_tool(select_tool)
    await agent.add_tool(index_tool)  
    
    message = Message(
        content = "Find me the user info for Fargas3231",
        metadata = [data_frame]
    )
    
    start = datetime.now()
    response = await agent(message)
    end = datetime.now()
    print(f"Response: {response.content}")
    print(f"Time: {end - start}")
        
    await agent.reset()
