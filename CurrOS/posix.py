from pathlib import Path

appdata_path = Path.home() / (
    ".config" if not str(Path.home()).startswith("/Users/") else ""
)
