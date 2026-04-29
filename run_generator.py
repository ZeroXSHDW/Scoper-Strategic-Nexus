import sys
from pathlib import Path

# Add src to pythonpath
sys.path.insert(0, str(Path("src").resolve()))

from scoper.cli import main
from click.testing import CliRunner

runner = CliRunner()
result = runner.invoke(main, ["generate-pack", "--client", "Global Financial Bank", "--pack", "global-unified-pack", "--output", "output/Vendor_RFP_DORA_PRA_HKMA_Scope.pdf"])

print(result.output)
if result.exception:
    raise result.exception
