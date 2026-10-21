import os
import time
from openai import OpenAI
from anthropic import Anthropic
from typing import Optional, Dict, Any, Iterator
from dotenv import load_dotenv

from config import OPENAI_MODEL, COHERE_MODEL,ANTHROPIC_MODEL, openai_client, cohere_client


load_dotenv()

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

def ask_openai(prompt: str, model: str = OPENAI_MODEL) -> Dict[str, Any]:
    """
    Ask OpenAI a question and return response with usage data.
    
    Args:
        prompt: Question or instruction
        model: Model to use
    
    Returns:
        Dictionary with response text and usage information
    """
    response = openai_client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Extract usage data directly from API response
    usage = response.usage
    
    return {
        "response": response.choices[0].message.content,
        "usage": {
            "prompt_tokens": usage.prompt_tokens,
            "completion_tokens": usage.completion_tokens,
            "total_tokens": usage.total_tokens
        }
    }

def ask_anthropic(prompt: str, model: str = ANTHROPIC_MODEL) -> Dict[str, Any]:
    """
    Ask Anthropic Claude a question and return response with usage data.
    
    Args:
        prompt: Question or instruction
        model: Model to use
    
    Returns:
        Dictionary with response text and usage information
    """
    response = anthropic_client.messages.create(
        model=model,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Extract usage data directly from API response
    usage = response.usage
    
    return {
        "response": response.content[0].text,
        "usage": {
            "input_tokens": usage.input_tokens,
            "output_tokens": usage.output_tokens
        }
    }


def ask_cohere(prompt: str, model: str = COHERE_MODEL) -> Dict[str, Any]:
    """
    Ask cohere a question and return response with usage data.
    
    Args:
        prompt: Question or instruction
        model: Model to use
    
    Returns:
        Dictionary with response text and usage information
    """
    response = cohere_client.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Extract usage data directly from API response
    usage = response.usage
    token_usage = extract_cohere_token_usage(usage)
    return {
        "response": response.message.content[1].text,
        "usage": {
            "input_tokens": token_usage["input_tokens"],
            "output_tokens": token_usage["input_tokens"]
        }
    }



def extract_cohere_token_usage(usage: Any) -> Dict[str, int]:
    """Extract Cohere token counts across SDK response shapes."""
    billed_units = getattr(usage, "billed_units", None)
    tokens = getattr(usage, "tokens", None)

    input_tokens = 0
    output_tokens = 0

    if billed_units is not None:
        input_tokens = getattr(billed_units, "input_tokens", 0) or 0
        output_tokens = getattr(billed_units, "output_tokens", 0) or 0

    if not input_tokens and tokens is not None:
        input_tokens = getattr(tokens, "input_tokens", 0) or 0

    if not output_tokens and tokens is not None:
        output_tokens = getattr(tokens, "output_tokens", 0) or 0

    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
    }



def compare_providers(prompt: str) -> Dict[str, Any]:
    """
    Ask the same question to both providers and compare responses + token usage.
    
    Args:
        prompt: Question to ask
    
    Returns:
        Dictionary with both responses and usage data
    """
    print(f"Question: {prompt}\n")
    
    # Ask OpenAI
    print("Asking OpenAI...")
    openai_result = ask_openai(prompt)
    print(f"OpenAI Response: {openai_result['response']}")
    print(f"OpenAI Usage: {openai_result['usage']}\n")
    
    # Ask Anthropic
    #print("Asking Anthropic...")
    #anthropic_result = ask_anthropic(prompt)
    #print(f"Anthropic Response: {anthropic_result['response']}")
    #print(f"Anthropic Usage: {anthropic_result['usage']}\n")

    # Ask cohere
    print("Asking Cohere...")
    cohere_result = ask_cohere(prompt)
    print(f"Cohere Response: {cohere_result['response']}")
    print(f"Cohere Usage: {cohere_result['usage']}\n")
    
    return {
        "openai": openai_result,
        "cohere": cohere_result
        # "anthropic": anthropic_result
    }

# Test with a simple prompt
#results = compare_providers("Explain machine learning in one sentence")
#print("✅ Comparison complete!")

#print("✅ Provider functions ready! (now with direct API usage tracking)")
