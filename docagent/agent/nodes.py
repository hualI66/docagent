from typing import Optional
import anthropic
from .prompts import (
    ROUTE_PROMPT,
    API_DOC_PROMPT,
    README_PROMPT,
    MANUAL_PROMPT
)
from .state import AgentState
from docagent.config import Config

# Create Anthropic client
client = anthropic.Anthropic(
    api_key=Config.OPENAI_API_KEY,
    base_url="https://api.minimaxi.com/anthropic"
)

def route_node(state: AgentState) -> AgentState:
    """根据内容类型判断文档类型"""
    content = state["content"]

    try:
        prompt = ROUTE_PROMPT.invoke({"content": content[:2000]})
        response = client.messages.create(
            model="MiniMax-M2.7",
            max_tokens=100,
            messages=[{"role": "user", "content": prompt.to_string()}]
        )
        # Extract text from response, handling ThinkingBlock
        content_type = None
        for block in response.content:
            if block.type == 'text':
                content_type = block.text.strip().lower()
                break
        # If no text block but has thinking block, extract answer from thinking
        if not content_type:
            for block in response.content:
                if block.type == 'thinking':
                    thinking = block.thinking
                    for word in ['code', 'markdown', 'pdf', 'web', 'text']:
                        if word in thinking.lower():
                            content_type = word
                            break
                    break
        if not content_type:
            raise RuntimeError("No text block in response")
    except Exception as e:
        raise RuntimeError(f"Failed to route content: {str(e)}")

    # 映射到文档类型
    doc_type_map = {
        "code": "api_doc",
        "markdown": "readme",
        "pdf": "manual",
        "web": "manual",
        "text": "manual"
    }

    document_type = doc_type_map.get(content_type, "manual")

    return {
        "content": content,
        "content_type": content_type,
        "document_type": document_type
    }

def generate_node(state: AgentState) -> AgentState:
    """根据文档类型生成对应文档"""
    content = state["content"]
    document_type = state.get("document_type")

    if not document_type:
        raise ValueError("document_type is required in state")

    # 选择对应的Prompt
    prompt_map = {
        "api_doc": API_DOC_PROMPT,
        "readme": README_PROMPT,
        "manual": MANUAL_PROMPT
    }

    prompt_template = prompt_map.get(document_type, MANUAL_PROMPT)

    try:
        prompt = prompt_template.invoke({"content": content[:4000]})
        response = client.messages.create(
            model="MiniMax-M2.7",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt.to_string()}]
        )
        # Extract text from response, handling ThinkingBlock
        generated_document = None
        thinking_content = None

        for block in response.content:
            if block.type == 'text' and block.text:
                generated_document = block.text
            elif block.type == 'thinking':
                thinking_content = block.thinking

        # If no text block but has thinking block, use thinking content
        if not generated_document and thinking_content:
            generated_document = thinking_content

        if not generated_document:
            raise RuntimeError("No content in response")
    except Exception as e:
        raise RuntimeError(f"Failed to generate document: {str(e)}")

    return {
        "generated_document": generated_document
    }
