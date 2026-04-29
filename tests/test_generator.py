import pytest
from pathlib import Path
from scoper.generator import ScopingPackGenerator

@pytest.fixture
def real_data_dir():
    return Path(__file__).parent.parent / "src" / "scoper" / "data"

def test_generator_initialization(real_data_dir):
    generator = ScopingPackGenerator(real_data_dir)
    assert generator is not None

def test_generator_pdf_export_fallback(real_data_dir, tmp_path):
    generator = ScopingPackGenerator(real_data_dir)
    output_path = tmp_path / "output.pdf"
    
    # Generate HTML only to avoid Playwright test hangs or use fallback
    html_content = generator.generate("Test Client", "Global", [], output_path, pack_id="global-unified-pack")
    
    # It should fallback to HTML or create the PDF
    assert (tmp_path / "output.html").exists() or output_path.exists()
