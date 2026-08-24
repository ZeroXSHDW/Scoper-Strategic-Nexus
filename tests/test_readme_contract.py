from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_readme_defines_the_release_operator_contract():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for heading in (
        "## Scope",
        "## Prerequisites",
        "## Installation and setup",
        "## Data and provenance",
        "## Build",
        "## Test",
        "## Publishing Checklist",
        "## Verification",
        "## Troubleshooting",
        "## Contributing",
        "## Security",
        "## License",
    ):
        assert readme.count(heading) == 1, f"README must contain one {heading} heading"

    for token in (
        "python3 -m regulatory_requirements build-all --offline",
        "python3 -m regulatory_requirements build-all --refresh",
        "python3 -m regulatory_requirements clean",
        "python -m pip install --require-hashes -r requirements-ci.txt",
        "python -m pip_audit --progress-spinner off",
        "git diff --check",
        "No credentials are required for the public-source workflow.",
    ):
        assert token in readme, f"README is missing operator contract: {token}"

    assert "/Users/" not in readme
    assert "C:\\Users\\" not in readme
