from recipe.utils.anthropic_llm import AnthropicService
from recipe.utils.ollama_llm import OllamaService

from django.conf import settings

OLLAMA_LLM = settings.OLLAMA_LLM
ANTHROPIC_LLM = settings.ANTHROPIC_LLM

def choose_llm():
    llm = AnthropicService()
    if OLLAMA_LLM:
        llm = OllamaService()
    if ANTHROPIC_LLM:
        llm = AnthropicService()
    return llm

llm_service = choose_llm()