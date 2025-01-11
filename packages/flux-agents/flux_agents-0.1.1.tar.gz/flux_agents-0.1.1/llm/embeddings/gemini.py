"""
Gemini embedding model implementation.

This module provides functions for generating embeddings using Google's Gemini API,
with thread-safe initialization and caching of the client.
"""

from typing import List
import os
import threading
import asyncio
import aiohttp


_genai_lock = threading.Lock()
_genai = None


def _initialize_genai():
    """Initialize the Google Generative AI client."""
    global _genai
    if _genai is None:
        with _genai_lock:
            if _genai is None:
                import google.generativeai as genai
                api_key = os.getenv("GEMINI_API_KEY")
                if not api_key:
                    raise ValueError("GEMINI_API_KEY environment variable not set")
                genai.configure(api_key=api_key)
                _genai = genai
    return _genai


_genai = _initialize_genai()


async def gemini_generate_embedding(
    text: str,
    model_name: str = 'models/embedding-001',
    task_type: str = 'retrieval_document',
    batch_size: int = 20
) -> List[float]:
    """Optimized embedding generation with connection reuse and retries"""
    
    # Use shared connection pool
    if not hasattr(gemini_generate_embedding, '_connector'):
        gemini_generate_embedding._connector = aiohttp.TCPConnector(
            limit = 100,
            ttl_dns_cache = 300,
            use_dns_cache = True
        )

    async def _batch_embed(texts: List[str]) -> List[List[float]]:
        
        async with aiohttp.ClientSession(
            connector = gemini_generate_embedding._connector,
            timeout = aiohttp.ClientTimeout(total = 30)
        ) as session:
            loop = asyncio.get_event_loop()
            tasks = []
            
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                
                def embed_batch(b):
                    try:
                        result = _genai.embed_content(
                            model = model_name,
                            content = b,
                            task_type = task_type
                        )
                        return result
                    except Exception as e:
                        print(f"Error in embed_content: {str(e)}")
                        raise
                
                task = loop.run_in_executor(None, embed_batch, batch)
                tasks.append(task)
            
            try:
                responses = await asyncio.gather(*tasks)
              
                embeddings = []
                for i, response in enumerate(responses):
        
                    # The response format is {'embedding': [[...values...]]}
                    if isinstance(response, dict) and 'embedding' in response:
                        batch_embeddings = response['embedding']
                        embeddings.extend(batch_embeddings)
                    else:
                        print(f"Unexpected response format: {response}")
                        raise ValueError(f"Unexpected response format: {response}")
                
                return embeddings
                
            except Exception as e:
                print(f"Error processing responses: {str(e)}")
                raise

    try:
        if isinstance(text, str):
            embeddings = await _batch_embed([text])
            if not embeddings:
                print("No embeddings generated for single text input")
                raise ValueError("Failed to generate embeddings")
            return embeddings[0]  # Return the first embedding for single text
        else:
            embeddings = await _batch_embed(text)
            if not embeddings:
                print("No embeddings generated for batch text input")
                raise ValueError("Failed to generate embeddings")
            return embeddings
           
    except Exception as e:
        print(f"Error in gemini_generate_embedding: {str(e)}")
        raise


