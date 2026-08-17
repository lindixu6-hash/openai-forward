from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "recovery-ci.yml"


def main() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")

    required = (
        "permissions:\n  contents: read",
        'python-version:\n          - "3.9"\n          - "3.10"',
        'python -m pip install ".[test]" build',
        "python -m pytest tests -q",
        "python -m pip check",
        "python -m compileall -q openai_forward",
        "python -m build",
    )
    missing = [item for item in required if item not in workflow]
    if missing:
        raise SystemExit(f"Recovery workflow is missing required contracts: {missing}")

    forbidden = (
        "secrets.",
        "docker/login-action",
        "gh-action-pypi-publish",
        "permissions: write-all",
        "contents: write",
    )
    present = [item for item in forbidden if item in workflow]
    if present:
        raise SystemExit(f"Recovery workflow contains release or secret access: {present}")

    print("Public recovery contract verified")


if __name__ == "__main__":
    main()
