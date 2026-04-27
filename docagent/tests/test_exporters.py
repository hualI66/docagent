import pytest
import os
import tempfile
from docagent.exporters.markdown_exporter import export_to_markdown
from docagent.exporters.pdf_exporter import export_to_pdf

def test_export_to_markdown():
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, "test.md")
        result = export_to_markdown("# Test\nContent", output_path)
        assert result == output_path
        assert os.path.exists(output_path)

def test_export_to_pdf():
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, "test.pdf")
        result = export_to_pdf("# Test\nContent", output_path)
        assert result == output_path
        assert os.path.exists(output_path)