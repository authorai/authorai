import openai
import os
# Pre-installed packages
import re

openai.api_key = os.getenv("OPENAI_KEY")
openai_model = 'text-davinci-003'

def openai_completion(prompt, temperature=0.9, tokens=70, model=openai_model):
    """AuthorAI wrapper for OpenAI Completion API.

    Args:
        prompt: Zero/few-shot learning prompt for generating a completion.
        temperature: Model takes more risks with higher values (0.9), model is deterministic at 0.
        tokens: Similar count as words in prompt plus completion. Counts towards OpenAI API cost.
        model: Model version of OpenAI GPT to run.

    Returns:
        The as-is completion response as JSON.
    """
    response = openai.Completion.create(
        model=model, prompt=prompt, temperature=temperature, max_tokens=tokens)
    return response

def strip_filename(filename: str) -> str:
    """Strip a filename of any characters which are not alphabets while preserving whitespace.

    Args:
        filename: File name to strip.
    Returns:
        filename_stripped: Stipped file name. Maybe same as input.
    """
    filename_stripped = re.sub(r'[^a-zA-Z\s]', '', filename)
    return filename_stripped

