from typing import Any
import ast

def evaluate_parameter(value: str) -> Any:
    value = value.strip()
  
    if value.lower() == 'true':
        value = True
    elif value.lower() == 'false':
        value = False
    
    elif value.lower() == 'none':
        value = None
    
    elif value[0] == '[' or value[0] == '{':
        value = ast.literal_eval(value)
        
    else:
        try:
            if '*' in value:
                value = eval(value.replace(' ', ''))
            elif '.' in value:
                value = float(value)
            else:
                value = int(value)
        except ValueError:
            value = value.strip("'")
            pass
        
    return value