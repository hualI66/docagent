from pathlib import Path

def export_to_markdown(content: str, output_path: str) -> str:
    """导出文档为Markdown文件"""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')
    return str(path)