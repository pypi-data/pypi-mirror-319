import os
import numpy as np
from typing import Union, List
import aiohttp
import asyncio
from concurrent.futures import ThreadPoolExecutor


async def pulse_embeddings(text: Union[str, list[str]]):
    """
    Generate embeddings for a given text using Pulse API.
    
    :param text: Text to embed
    :type text: Union[str, list[str]]
    :return: Embedding vector or list of embedding vectors
    :rtype: Union[List[float], List[List[float]]]
    """
    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Apikey {os.getenv("PULSE_API_KEY")}'
        }
        
        if not isinstance(text, list):
            text = [text]
            
        payload = {"text": text}
        url = f"{os.getenv('INFERENCE_URL')}/pulse/v4/pf/lp/llm/get_embeddings"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('embeddings', [])
                else:
                    raise RuntimeError(f"API request failed with status {response.status}")
            
    except Exception as e:
        raise RuntimeError(f"Failed to fetch embeddings using Pulse: {str(e)}")



