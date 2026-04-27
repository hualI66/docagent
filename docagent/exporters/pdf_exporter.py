from pathlib import Path
import re
import markdown
from fpdf import FPDF

def export_to_pdf(markdown_content: str, output_path: str) -> str:
    """将Markdown转换为PDF，支持中文和分层结构"""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    # 使用fpdf2生成PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # 添加微软雅黑字体
    font_path = 'C:\\Windows\\Fonts\\msyh.ttc'
    pdf.add_font('msyh', '', font_path, uni=True)
    pdf.add_font('msyhbd', '', font_path, uni=True)
    pdf.add_font('msyhbi', '', font_path, uni=True)
    pdf.set_font('msyh', '', 11)

    # Emoji映射表
    emoji_map = {
        '📖': '[文档]', '🎯': '[目标]', '📋': '[列表]', '❓': '[问题]',
        '📱': '[手机]', '✅': '[完成]', '❌': '[失败]', '⚠️': '[警告]',
        '💡': '[提示]', '🔧': '[工具]', '📌': '[标注]', '⭐': '[星标]',
        '🚀': '[启动]', '⚡': '[快速]', '🎨': '[设计]', '📦': '[包]',
        '🔗': '[链接]', '📊': '[图表]', '📈': '[增长]', '📉': '[下降]',
        '🛠️': '[工具]', '✅': '[是]', '❌': '[否]', '🔵': '[蓝]',
        '🔴': '[红]', '🟢': '[绿]', '⚪': '[白]', '⚫': '[黑]',
    }

    def replace_emoji(text):
        for emo, replacement in emoji_map.items():
            text = text.replace(emo, replacement)
        # 移除其他无法显示的特殊字符
        text = re.sub(r'[\U00010000-\U0010ffff]', '', text)
        return text

    def safe_multi_cell(pdf, text, height=6):
        """安全的多行cell，防止宽度不足错误"""
        try:
            pdf.multi_cell(0, height, text)
        except Exception:
            # 如果出错，尝试换行后重试
            pdf.ln()
            try:
                pdf.multi_cell(0, height, text)
            except Exception:
                pass  # 跳过有问题的行

    # 解析Markdown行
    lines = markdown_content.split('\n')
    in_code_block = False

    for line in lines:
        original_line = line
        line = replace_emoji(line)

        # 代码块
        if line.strip().startswith('```'):
            if in_code_block:
                in_code_block = False
                pdf.ln(2)
                pdf.set_font('msyh', '', 11)
            else:
                in_code_block = True
                pdf.ln(3)
                pdf.set_font('Courier', '', 9)
            continue

        if in_code_block:
            pdf.set_font('Courier', '', 9)
            # 确保有足够宽度
            if pdf.w - pdf.l_margin - pdf.r_margin - pdf.get_x() < 10:
                pdf.ln()
            safe_multi_cell(pdf, line, 5)
            continue

        # 空行
        if not line.strip():
            pdf.ln(2)
            continue

        # 确保有足够宽度
        if pdf.w - pdf.l_margin - pdf.r_margin - pdf.get_x() < 10:
            pdf.ln()

        # 标题处理
        if line.strip().startswith('# '):
            pdf.ln(4)
            pdf.set_font('msyhbd', '', 18)
            pdf.set_text_color(30, 60, 120)  # 深蓝色
            safe_multi_cell(pdf, line.strip()[2:], 10)
            pdf.ln(3)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font('msyh', '', 11)
        elif line.strip().startswith('## '):
            pdf.ln(4)
            pdf.set_font('msyhbd', '', 15)
            pdf.set_text_color(50, 80, 150)  # 蓝色
            safe_multi_cell(pdf, line.strip()[3:], 8)
            pdf.ln(2)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font('msyh', '', 11)
        elif line.strip().startswith('### '):
            pdf.ln(3)
            pdf.set_font('msyhbd', '', 13)
            pdf.set_text_color(70, 100, 180)
            safe_multi_cell(pdf, line.strip()[4:], 7)
            pdf.ln(1)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font('msyh', '', 11)
        # 列表项
        elif line.strip().startswith('- ') or line.strip().startswith('* '):
            pdf.set_font('msyh', '', 11)
            safe_multi_cell(pdf, '    • ' + line.strip()[2:], 6)
        elif re.match(r'^\d+\.\s', line.strip()):
            match = re.match(r'^(\d+)\.\s(.*)', line.strip())
            if match:
                pdf.set_font('msyh', '', 11)
                safe_multi_cell(pdf, '    ' + match.group(1) + '. ' + match.group(2), 6)
        # 引用块
        elif line.strip().startswith('>'):
            pdf.set_font('msyhbi', '', 10)
            pdf.set_text_color(80, 80, 80)
            safe_multi_cell(pdf, '  ' + line.strip()[1:], 5)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font('msyh', '', 11)
        # 分割线
        elif line.strip().startswith('---'):
            pdf.ln(2)
            pdf.set_draw_color(200, 200, 200)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(2)
        # 普通段落
        else:
            pdf.set_font('msyh', '', 11)
            safe_multi_cell(pdf, line, 6)
            pdf.ln(1)

    pdf.output(str(path))
    return str(path)
