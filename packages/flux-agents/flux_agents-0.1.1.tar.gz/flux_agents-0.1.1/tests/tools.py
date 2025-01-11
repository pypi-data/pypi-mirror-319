from tools.models import Tool

async def test_tool_serialization():
    """Test tool serialization with various parameter types"""
    from typing import List, Dict, Any, Optional
    from pathlib import Path
    import shutil
    
    # Function can now be defined anywhere!
    def test_function(
        str_param: str,
        int_param: int,
        list_param: List[str],
        dict_param: Dict[str, Any],
        optional_param: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        return [{"result": "test"}]
    
    try:
        # Create tool
        tool = Tool.from_function(test_function)
        
        # Serialize
        test_path = Path("test_tool")
        await tool.serialize(test_path)
        
        # Deserialize
        loaded_tool = await Tool.deserialize(test_path)
        
        # Verify types are preserved
        assert loaded_tool.parameters[0].type == str
        assert loaded_tool.parameters[1].type == int
        assert loaded_tool.parameters[2].type.__origin__ == list
        assert loaded_tool.parameters[2].type.__args__[0] == str
        assert loaded_tool.return_type.__origin__ == list
        
        # Test function call
        result = await loaded_tool(
            str_param = "test",
            int_param = 1,
            list_param = ["test"],
            dict_param = {"test": "value"}
        )
        assert result == [{"result": "test"}]
        
    finally:
        # Cleanup
        if test_path.exists():
            shutil.rmtree(test_path) 