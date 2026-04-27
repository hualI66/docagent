from typing import TypedDict, Optional

class AgentState(TypedDict):
    content: str                    # 提取的内容
    content_type: str               # 内容类型: code, markdown, pdf, web, text
    document_type: Optional[str]    # 文档类型: api_doc, readme, manual
    generated_document: Optional[str] # 生成的文档
    error: Optional[str]            # 错误信息