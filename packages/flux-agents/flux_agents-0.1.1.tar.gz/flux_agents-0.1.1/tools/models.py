"""
Tool models for agent function wrapping and parameter handling.

This module provides models for wrapping functions as tools that can be used by agents,
with support for both synchronous and asynchronous execution.
"""

from typing import List, Any, Optional, Type, Callable, Dict, get_type_hints, Union, Set
from pydantic import BaseModel, Field, PrivateAttr
from functools import partial, cached_property
import inspect
import asyncio
import json
import aiofiles
from pathlib import Path
import typing
import ast
import textwrap
from enum import Enum

from agents.agent.models import AgentState, AgentConfig
from llm import LLM, BaseEmbeddingFunction


class StaticParameter(BaseModel):
    """
    Model representing a static parameter for a tool function.
    
    :ivar name: Name of the parameter
    :type name: str
    :ivar type: Type of the parameter
    :type type: Type
    :ivar value: Value of the parameter
    :type value: Any
    :ivar description: Description of the parameter
    :type description: Optional[str]
    """
    name: str
    type: Any
    value: Any
    description: Optional[str] = None   
    
    class Config:
        arbitrary_types_allowed = True
        extra = "forbid"
        

class InternalParameterType(Enum):
    """Valid types for internal parameters that can be passed from agent state"""
    AGENT_STATE = AgentState
    AGENT_CONFIG = AgentConfig
    LLM = LLM
    EMBEDDING = BaseEmbeddingFunction


class InternalParameter(BaseModel):
    """
    Model representing an internal parameter from a parent agent
    
    :ivar name: Name of the parameter
    :type name: str
    :ivar type: Type of the parameter (must be AgentState or AgentConfig)
    :type type: InternalParameterType
    :ivar description: Description of the parameter
    :type description: Optional[str]
    """
    name: str
    type: InternalParameterType
    description: Optional[str] = None

    @classmethod
    def validate_type(cls, param_name: str, param_type: Any) -> Optional['InternalParameter']:
        """
        Validate if a parameter should be an internal parameter based on name and type.
        Returns InternalParameter if valid, None otherwise.
        """
        # Use direct type comparison instead of string matching
        if param_type in (AgentState, AgentConfig, BaseEmbeddingFunction, LLM):
            if param_type is AgentState:
                internal_type = InternalParameterType.AGENT_STATE
            elif param_type is AgentConfig:
                internal_type = InternalParameterType.AGENT_CONFIG
            elif param_type is BaseEmbeddingFunction:
                internal_type = InternalParameterType.EMBEDDING
            elif param_type is LLM:
                internal_type = InternalParameterType.LLM
            return cls(name = param_name, type = internal_type)
        return None

    def validate_value(self, value: Any) -> bool:
        """Validate that a value matches the internal parameter type"""
        return isinstance(value, self.type.value)

    class Config:
        arbitrary_types_allowed = True
        
        
class ToolParameter(BaseModel):
    """
    Model representing a parameter for a tool function.
    
    :ivar name: Name of the parameter
    :type name: str
    :ivar type: Type of the parameter
    :type type: Type
    :ivar required: Whether the parameter is required
    :type required: bool
    :ivar default: Default value for the parameter
    :type default: Any
    :ivar description: Description of the parameter
    :type description: Optional[str]
    """
    name: str
    type: Any
    required: bool = True
    default: Any = None
    description: Optional[str] = None


    @cached_property
    def get_types(self) -> List[Type]:
        return list(self._extract_types(self.type, set()))

    def _extract_types(self, param_type: Any, seen: Set[Type]) -> Set[Type]:
        """
        Recursively extract types from Union and pipe types.
        
        :param param_type: The parameter type to extract from
        :param seen: A set to track already processed types
        :return: Set of unique types
        :rtype: Set[Type]
        """
        if param_type in seen:
            return seen 
        
        # Handle Union types
        if hasattr(param_type, '__origin__') and param_type.__origin__ is Union:
            for arg in param_type.__args__:
                self._extract_types(arg, seen)  # Extract types from Union arguments

        # Handle pipe types (Python 3.10+)
        elif hasattr(param_type, '__origin__') and param_type.__origin__ is type(Union):
            for arg in param_type.__args__:
                self._extract_types(arg, seen)  # Extract types from pipe arguments

        # Handle generic types (like List, Dict, etc.)
        elif hasattr(param_type, '__origin__'):
            if param_type.__origin__ in {list, dict, set, tuple}:
                if param_type.__origin__ not in seen:
                    seen.add(param_type.__origin__)  # Add the base type
                if hasattr(param_type, '__args__'):
                    for arg in param_type.__args__:
                        self._extract_types(arg, seen)  # Extract types from generic arguments

        else:
            seen.add(param_type)  # Add non-generic types directly

        return seen


    def text(self) -> str:
        param_str = f" - {self.name} ({', '.join(t.__name__ for t in self.get_types)})"
 
        # Add optional/default indicators
        if not self.required:
            param_str += "(optional) "
        if self.default is not None:
            param_str += f"(default={self.default})"
        
        # Add parameter description on next line if available
        if self.description:
            param_str += f" → {self.description}"
        
        return param_str
    
    class Config:
        arbitrary_types_allowed = True
        extra = "forbid"


class Tool(BaseModel):
    """
    Model for wrapping functions as agent tools, allowing them to be called like functions while
    maintaining static parameters, validation, and metadata.
    
    Handles both synchronous and asynchronous function execution with parameter validation.
    
    :ivar name: Name of the tool
    :type name: str
    :ivar description: Description of what the tool does
    :type description: Optional[str]
    :ivar parameters: List of tool parameters
    :type parameters: List[ToolParameter]
    :ivar static_parameters: Static parameters to always pass to function
    :type static_parameters: List[StaticParameter]
    :ivar function: The wrapped function
    :type function: Callable
    :ivar return_type: Expected return type
    :type return_type: Optional[Type]
    :ivar _is_async: Whether the function is async
    :type _is_async: bool
    :ivar return_names: List of return variable names
    :type return_names: List[str]
    :ivar return_types: List of return variable types
    :type return_types: List[Any]
    :ivar internal_parameters: List of internal parameters
    :type internal_parameters: List[InternalParameter]
    """
    name: str = Field(default = None)
    description: Optional[str] = Field(default = None)
    parameters: List[ToolParameter] = Field(default_factory = list)
    static_parameters: List[StaticParameter] = Field(default_factory = list)
    function: Callable = Field(default = None)
    return_type: Any = Field(default = None)
    return_names: List[str] = Field(default_factory = list)
    return_types: List[Any] = Field(default_factory = list)
    internal_parameters: List[InternalParameter] = Field(default_factory=list)
    
    _is_async: bool = PrivateAttr(default = False)
    _has_internal_params: bool = PrivateAttr(default = False)
    
    class Config:
        arbitrary_types_allowed = True
        extra = "forbid"
        
        
    def __init__(self, **data):
        """
        Initialize tool and detect if function is async.
        
        :param data: Tool configuration data
        """
        super().__init__(**data)
        self._is_async = inspect.iscoroutinefunction(self.function)
        
        # Extract parameters from function if not provided
        if not self.parameters and self.function:
            # Get function signature and type hints
            signature = inspect.signature(self.function)
            type_hints = get_type_hints(self.function)
            
            # Get docstring and parse it for parameter descriptions
            doc = inspect.getdoc(self.function) or ""
            param_docs = {}
            
            if doc:
                lines = doc.split('\n')
                current_param = None
                for line in lines:
                    line = line.strip()
                    if line.startswith(':param '):
                        current_param = line[7:].split(':')[0].strip()
                        param_docs[current_param] = line.split(':', 2)[2].strip()
                    elif line.startswith('Args:'):
                        continue
                    elif current_param and line and line[0] == ' ':
                        param_docs[current_param] += ' ' + line.strip()
            
            # Create parameters list
            for param_name, param in signature.parameters.items():
                param_type = type_hints.get(param_name, Any)
                
                # Fast path - only check internal params if type matches
                if param_type in (AgentState, AgentConfig):
                    internal_param = InternalParameter.validate_type(param_name, param_type)
                    if internal_param:
                        self.internal_parameters.append(internal_param)
                        continue
                
                # Regular parameter handling
                required = param.default == param.empty
                default = None if param.default == param.empty else param.default
                
                self.parameters.append(
                    ToolParameter(
                        name = param_name,
                        type = param_type,
                        required = required,
                        default = default,
                        description = param_docs.get(param_name)
                    )
                )
            
            # Cache internal param check
            self._has_internal_params = bool(self.internal_parameters)

        # Convert static_params dict to StaticParameter list
        if "static_params" in data:
            static_params = data.pop("static_params")
            for name, value in static_params.items():
                # Find matching parameter to get type and description
                param_info = next(
                    (p for p in self.parameters if p.name == name),
                    None
                )
                if param_info:
                    self.static_parameters.append(
                        StaticParameter(
                            name=name,
                            type=param_info.type,
                            value=value,
                            description=param_info.description
                        )
                    )
                    # Remove from regular parameters
                    self.parameters = [p for p in self.parameters if p.name != name]

        # Extract return information if not already provided
        if not (self.return_names and self.return_types) and self.function:
            # Get return type hints
            type_hints = get_type_hints(self.function)
            return_hint = type_hints.get('return')
            
            # Extract return names
            self.return_names = self._extract_return_names(
                self.function, 
                self.name or self.function.__name__
            )
            
            # Process return types
            if return_hint:
                if hasattr(return_hint, '__origin__') and return_hint.__origin__ is tuple:
                    # Handle Tuple[type1, type2, ...]
                    self.return_types = list(return_hint.__args__)
                    # Ensure we have enough return names
                    while len(self.return_names) < len(self.return_types):
                        self.return_names.append(
                            f"{self.name}_result_{len(self.return_names)+1}"
                        )
                elif hasattr(return_hint, '__origin__') and return_hint.__origin__ is dict:
                    # Handle Dict returns
                    key_type, value_type = return_hint.__args__
                    self.return_types = [value_type] * len(self.return_names)
                else:
                    # Handle single return type
                    self.return_types = [return_hint]
                    if not self.return_names:
                        self.return_names = [f"{self.name}_result"]
                        
            # Set return_type for backwards compatibility
            if not self.return_type:
                self.return_type = return_hint


    @cached_property
    def __len__(self) -> int:
        return len(self.parameters)
    
    
    def __repr__(self):
        """
        Get string representation of tool.
        
        :return: String representation
        :rtype: str
        """
        return f"Tool(name={self.name}, description={self.description}, parameters={self.parameters}, static_parameters={self.static_parameters}, function={self.function}, return_type={self.return_type})"


    async def __call__(self, *args, **kwargs) -> Any:
        """
        Async call implementation for the tool.
        
        Handles both async and sync functions by running sync functions in executor.
        
        :param args: Positional arguments for the function
        :param kwargs: Keyword arguments for the function
        :return: Function result
        :rtype: Any
        """
        # Fast path if no internal parameters
        if self._has_internal_params:
            # Validate internal parameters are present and have correct type
            for internal_param in self.internal_parameters:
                if internal_param.name not in kwargs:
                    raise ValueError(
                        f"Missing required internal parameter: {internal_param.name}"
                    )
                if not internal_param.validate_value(kwargs[internal_param.name]):
                    raise TypeError(
                        f"Invalid type for internal parameter {internal_param.name}. "
                        f"Expected {internal_param.type.value.__name__}, "
                        f"got {type(kwargs[internal_param.name]).__name__}"
                    )

        # Rest of call implementation
        all_kwargs = {
            **{p.name: p.value for p in self.static_parameters},
            **kwargs
        }
        
        func = self.function
        if inspect.iscoroutinefunction(func):
            return await func(*args, **all_kwargs)
        else:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(
                None, 
                partial(func, *args, **all_kwargs)
            )


    def __sync_call__(self, *args, **kwargs) -> Any:
        """
        Synchronous call implementation for the tool.
        
        Handles both async and sync functions by running async functions in new event loop.
        
        :param args: Positional arguments for the function
        :param kwargs: Keyword arguments for the function
        :return: Function result
        :rtype: Any
        """
        all_kwargs = {**self.static_params, **kwargs}
        func = self.function
        
        if inspect.iscoroutinefunction(func):
            # For async functions, run them in a new event loop
            loop = asyncio.new_event_loop()
            try:
                return loop.run_until_complete(func(*args, **all_kwargs))
            finally:
                loop.close()
        else:
            return func(*args, **all_kwargs)


    def __get__(self, obj, objtype = None):
        """
        Descriptor protocol implementation.
        
        Returns appropriate call method based on whether function is async.
        
        :param obj: Instance that the descriptor is accessed from
        :param objtype: Type of the instance
        :return: Call method
        :rtype: Callable
        """
        if obj is None:
            return self
        return self.__call__ if self._is_async else self.__sync_call__


    def set_static(self, param_name: str, value: Any) -> None:
        """
        Convert a parameter to static with a fixed value.
        
        :param param_name: Name of parameter to make static
        :type param_name: str
        :param value: Value to assign to the parameter
        :type value: Any
        """
        param = next((p for p in self.parameters if p.name == param_name), None)
        if not param:
            raise ValueError(f"Parameter {param_name} not found")
            
        # Create static parameter
        static_param = StaticParameter(
            name=param_name,
            type=param.type,
            value=value,
            description=param.description
        )
        
        # Remove from regular parameters and add to static
        self.parameters = [p for p in self.parameters if p.name != param_name]
        self.static_parameters.append(static_param)


    def set_dynamic(
        self, 
        param_name: str, 
        default: Optional[Any] = None
    ) -> None:
        """
        Convert a static parameter to dynamic.
        
        :param param_name: Name of parameter to make dynamic
        :type param_name: str
        :param default: Optional default value for the parameter
        :type default: Optional[Any]
        """
        # Find parameter in static parameters
        static_param = next(
            (p for p in self.static_parameters if p.name == param_name), 
            None
        )
        if not static_param:
            raise ValueError(f"Static parameter {param_name} not found")
            
        # Create dynamic parameter
        dynamic_param = ToolParameter(
            name = param_name,
            type = static_param.type,
            required = default is None,
            default = default,
            description = static_param.description
        )
        
        # Remove from static parameters and add to regular
        self.static_parameters = [
            p for p in self.static_parameters if p.name != param_name
        ]
        self.parameters.append(dynamic_param)


    def text(self) -> str:
        """Generate human-readable tool description with clear usage examples"""
        param_docs = []
        for p in self.parameters:
            required = "required" if p.required else "optional"
            default = f", default={p.default}" if p.default is not None else ""
            desc = f" → {p.description}" if p.description else ""
            param_docs.append(f"  - {p.name}: {p.type.__name__} ({required}{default}){desc}")

        # Note: Intentionally not including internal parameters in text output

        # Format return information
        return_info = []
        if self.return_names and self.return_types:
            for name, type_ in zip(self.return_names, self.return_types):
                type_name = getattr(type_, '__name__', str(type_))
                if type_name:
                    return_info.append(f"  - {name}: {type_name}")
                else:
                    return_info.append(f"  - {name}")
        elif self.return_type:  # Fallback for legacy return_type
            type_name = getattr(self.return_type, '__name__', str(self.return_type))
            return_info.append(f"  - result: {type_name}")
        else:
            return_info.append("  - result")

        # Add usage hints based on function name/purpose
        usage_hint = ""
        if "select" in self.name.lower():
            usage_hint = "Use this tool first to get the columns you need from the data."
        elif "row" in self.name.lower() or "info" in self.name.lower():
            usage_hint = "Use this tool after selecting columns to get information from specific rows."

        tool_text = f"""{self.name}
  {f"Purpose: {self.description}" if self.description else ""}{f"\n  Usage: {usage_hint}" if usage_hint else ""}
  Input:
{"\n".join(param_docs)}
  Output:
{"\n".join(return_info)}"""
        
        return tool_text


    @staticmethod
    def _extract_return_names(func: Callable, tool_name: str) -> List[str]:
        """
        Extract return variable names from function source code using AST analysis.
        """
        try:
            # Get source and handle indentation properly
            source = inspect.getsource(func)
            
            # Handle indentation by finding the first non-empty line's indentation
            lines = source.splitlines()
            first_line = next(line for line in lines if line.strip())
            indent = len(first_line) - len(first_line.lstrip())
            
            # Remove that exact indentation from all lines
            dedented_lines = []
            for line in lines:
                if line[:indent].isspace() and len(line) >= indent:
                    dedented_lines.append(line[indent:])
                else:
                    dedented_lines.append(line)
            
            dedented_source = '\n'.join(dedented_lines)
            
            # Parse the dedented source
            tree = ast.parse(dedented_source)
            
            assignments = {}
            return_names = []

            class FunctionAnalyzer(ast.NodeVisitor):
                def visit_FunctionDef(self, node):
                    # Get all assignments in the function
                    for n in ast.walk(node):
                        if isinstance(n, ast.Assign):
                            for target in n.targets:
                                if isinstance(target, ast.Name):
                                    # Track what the variable is assigned from
                                    if isinstance(n.value, ast.Call):
                                        if isinstance(n.value.func, ast.Name):
                                            assignments[target.id] = {
                                                'type': 'call',
                                                'func': n.value.func.id
                                            }
                                        elif isinstance(n.value.func, ast.Attribute):
                                            assignments[target.id] = {
                                                'type': 'method',
                                                'name': n.value.func.attr
                                            }
                                    else:
                                        assignments[target.id] = {
                                            'type': 'value',
                                            'value': n.value
                                        }

                    # Find the return statement
                    returns = [n for n in ast.walk(node) if isinstance(n, ast.Return)]
                    
                    if returns:
                        ret = returns[0]  # Get the first return statement
                        
                        if isinstance(ret.value, ast.Tuple):
                            # Handle tuple returns
                            for elt in ret.value.elts:
                                if isinstance(elt, ast.Name):
                                    var_name = elt.id
                                    return_names.append(var_name)
                                elif isinstance(elt, ast.Call):
                                    if isinstance(elt.func, ast.Name):
                                        name = f"{elt.func.id}_result"
                                    elif isinstance(elt.func, ast.Attribute):
                                        name = f"{elt.func.attr}_result"
                                    else:
                                        name = f"{tool_name}_result_{len(return_names)+1}"
                                    return_names.append(name)
                                else:
                                    name = f"{tool_name}_value_{len(return_names)+1}"
                                    return_names.append(name)
                        elif isinstance(ret.value, ast.Name):
                            var_name = ret.value.id
                            return_names.append(var_name)
                        elif isinstance(ret.value, ast.Call):
                            if isinstance(ret.value.func, ast.Name):
                                name = f"{ret.value.func.id}_result"
                            elif isinstance(ret.value.func, ast.Attribute):
                                name = f"{ret.value.func.attr}_result"
                            else:
                                name = f"{tool_name}_result"
                            return_names.append(name)

            # Run the analyzer
            FunctionAnalyzer().visit(tree)
            
            return return_names if return_names else [f"{tool_name}_result"]
            
        except Exception as e:
            return [f"{tool_name}_result"]


    @classmethod
    def from_function(
        cls,
        func: Callable,
        name: Optional[str] = None,
        static_parameters: Optional[Dict[str, Any]] = None
    ) -> "Tool":
        """
        Create a Tool instance from a function.
        
        :param func: Function to wrap as a tool
        :type func: Callable
        :param name: Optional name for the tool
        :type name: Optional[str] 
        :param static_parameters: Parameters to set as static with their values
        :type static_parameters: Optional[Dict[str, Any]]
        :return: Created tool instance
        :rtype: Tool
        """
        # Get function signature and type hints
        signature = inspect.signature(func)
        type_hints = get_type_hints(func)
        
        # Get docstring and parse it
        doc = inspect.getdoc(func) or ""
        description = doc.split('\n\n')[0]
        
        # Parse docstring for parameter descriptions
        param_docs = {}
        if doc:
            lines = doc.split('\n')
            current_param = None
            for line in lines:
                line = line.strip()
                if line.startswith(':param '):
                    current_param = line[7:].split(':')[0].strip()
                    param_docs[current_param] = line.split(':', 2)[2].strip()
                elif line.startswith('Args:'):
                    continue
                elif current_param and line and line[0] == ' ':
                    param_docs[current_param] += ' ' + line.strip()
        
        # Create parameters list
        tool_parameters = []
        tool_static = []
        tool_internal = []
        static_parameters = static_parameters or {}
        
        for param_name, param in signature.parameters.items():
            param_type = type_hints.get(param_name, Any)
            
            # Fast path - only check internal params for matching types
            if param_type in (AgentState, AgentConfig):
                internal_param = InternalParameter.validate_type(param_name, param_type)
                if internal_param:
                    tool_internal.append(internal_param)
                    continue
            
            # Rest of parameter handling
            if param_name in static_parameters:
                static_param = StaticParameter(
                    name = param_name,
                    type = type_hints.get(param_name, Any),
                    value = static_parameters[param_name],
                    description = param_docs.get(param_name)
                )
                tool_static.append(static_param)
                continue
                
            required = param.default == param.empty
            default = None if param.default == param.empty else param.default
            
            tool_parameters.append(
                ToolParameter(
                    name = param_name,
                    type = param_type,
                    required = required,
                    default = default,
                    description = param_docs.get(param_name)
                )
            )

        # Extract return information
        return_hint = get_type_hints(func).get('return')
        tool_name = name or func.__name__
        return_names = cls._extract_return_names(func, tool_name)
        return_types = []

        if return_hint:
            if hasattr(return_hint, '__origin__') and return_hint.__origin__ is tuple:
                # Handle Tuple[type1, type2, ...]
                return_types = list(return_hint.__args__)
                # Ensure we have enough return names
                while len(return_names) < len(return_types):
                    return_names.append(f"{tool_name}_result_{len(return_names)+1}")
            elif hasattr(return_hint, '__origin__') and return_hint.__origin__ is dict:
                # Handle Dict returns
                key_type, value_type = return_hint.__args__
                return_types = [value_type] * len(return_names)
            else:
                # Handle single return type
                return_types = [return_hint]
                if not return_names:
                    return_names = [f"{tool_name}_result"]

        tool = cls(
            name = name or func.__name__,
            description = description,
            parameters = tool_parameters,
            static_parameters = tool_static,
            internal_parameters = tool_internal,
            function = func,
            return_type = return_hint,
            return_names = return_names,
            return_types = return_types
        )
                
        return tool


    async def serialize(self, path: Union[str, Path]) -> None:
        """
        Serialize the tool to disk using dill for function serialization.
        
        :param path: Directory path to save serialized data
        :type path: Union[str, Path]
        """
        import dill
        
        path = Path(path)
        path.mkdir(parents = True, exist_ok = True)
        
        # Helper function to serialize types
        def serialize_type(t: Any) -> Dict[str, Any]:
            try:
                return dill.dumps(t).hex()  # Convert to hex string for JSON
            except:
                return str(t)  # Fallback for types that can't be pickled
        
        # Prepare serializable data
        data = {
            "name": self.name,
            "description": self.description,
            "parameters": [{
                **p.model_dump(),
                'type': serialize_type(p.type)
            } for p in self.parameters],
            "static_parameters": [{
                **p.model_dump(),
                'type': serialize_type(p.type)
            } for p in self.static_parameters],
            "function": dill.dumps(self.function).hex(),  # Serialize entire function
            "return_type": serialize_type(self.return_type) if self.return_type else None,
            "_is_async": self._is_async,
            "internal_parameters": [{
                "name": p.name,
                "type": p.type.name,  # Store enum name
                "description": p.description
            } for p in self.internal_parameters],
        }
        
        # Save as JSON
        async with aiofiles.open(path / "tool.json", "w") as f:
            await f.write(json.dumps(data, indent = 2))


    @classmethod
    async def deserialize(cls, path: Union[str, Path]) -> 'Tool':
        """
        Deserialize a tool from disk using dill for function deserialization.
        
        :param path: Directory path containing serialized data
        :type path: Union[str, Path]
        :return: Deserialized Tool instance
        :rtype: Tool
        """
        import dill
        
        path = Path(path)
        
        # Helper function to deserialize types
        def deserialize_type(type_data: str) -> Type:
            try:
                return dill.loads(bytes.fromhex(type_data))
            except:
                # Fallback for string-serialized types
                if hasattr(typing, type_data):
                    return getattr(typing, type_data)
                elif type_data in globals():
                    return globals()[type_data]
                return Any
        
        # Load JSON data
        async with aiofiles.open(path / "tool.json", "r") as f:
            data = json.loads(await f.read())
        
        # Reconstruct function using dill
        function = dill.loads(bytes.fromhex(data["function"]))
        
        # Reconstruct parameters with proper type handling
        parameters = []
        for p in data["parameters"]:
            param_type = deserialize_type(p.pop('type'))
            parameters.append(ToolParameter(**p, type = param_type))
            
        static_parameters = []
        for p in data["static_parameters"]:
            param_type = deserialize_type(p.pop('type'))
            static_parameters.append(StaticParameter(**p, type = param_type))
        
        # Reconstruct internal parameters
        internal_parameters = []
        for p in data.get("internal_parameters", []):
            internal_parameters.append(
                InternalParameter(
                    name=p["name"],
                    type=InternalParameterType[p["type"]],  # Convert name back to enum
                    description=p["description"]
                )
            )
        
        # Create tool instance
        tool = cls(
            name = data["name"],
            description = data["description"],
            parameters = parameters,
            static_parameters = static_parameters,
            internal_parameters = internal_parameters,
            function = function
        )
        
        # Restore additional attributes
        tool._is_async = data["_is_async"]
        if data["return_type"]:
            tool.return_type = deserialize_type(data["return_type"])
        
        return tool


    def execute(self, **kwargs):
        """
        Execute the tool with the provided parameters, filtering out any extraneous ones.
        
        :param kwargs: Parameters to pass to the tool function
        :return: Result of the tool function execution
        """
        # Filter parameters to only include those expected by the tool
        valid_params = {k: v for k, v in kwargs.items() if k in self.expected_param_names()}
        return self.function(**valid_params)


    def expected_param_names(self):
        """
        Get the names of the parameters expected by the tool.
        
        :return: Set of expected parameter names
        """
        return {param.name for param in self.parameters}