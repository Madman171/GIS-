# Copyright (c) 2026 ?????
# GIS???????????? - ????
# ?????????????????????

import zipfile
from pathlib import Path
from typing import Iterable


ROOT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT_DIR / "release" / "deployment"
OUTPUT_PATH = OUTPUT_DIR / "gis-knowledge-platform-deploy-V1.0.zip"
PACKAGE_ROOT = "gis-knowledge-platform"

INCLUDE_PATTERNS = [
    ".dockerignore",
    "README.md",
    "backend/*.py",
    "backend/requirements*.txt",
    "backend/.env.example",
    "backend/media/**/*",
    "frontend/package.json",
    "frontend/package-lock.json",
    "frontend/index.html",
    "frontend/vite.config.js",
    "frontend/.env.example",
    "frontend/public/**/*",
    "frontend/src/**/*",
    "data/*.cypher",
    "data/README.md",
    "deploy/*",
]

EXCLUDED_FILES = {
    "backend/.env",
    "deploy/.env",
}


def collect_files() -> Iterable[Path]:
    files = set()
    for pattern in INCLUDE_PATTERNS:
        for path in ROOT_DIR.glob(pattern):
            if not path.is_file():
                continue
            relative = path.relative_to(ROOT_DIR).as_posix()
            if relative in EXCLUDED_FILES:
                continue
            if "__pycache__" in path.parts:
                continue
            files.add(path)
    return sorted(files, key=lambda path: path.as_posix().lower())


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    files = list(collect_files())
    if not files:
        raise RuntimeError("No deployment files found")

    with zipfile.ZipFile(
        OUTPUT_PATH,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as archive:
        for path in files:
            relative = path.relative_to(ROOT_DIR)
            archive.write(
                path,
                arcname=(
                    Path(PACKAGE_ROOT) / relative
                ).as_posix(),
            )

    print(
        "Generated deployment package: {0}".format(OUTPUT_PATH)
    )
    print("Files: {0}".format(len(files)))
    print("Bytes: {0}".format(OUTPUT_PATH.stat().st_size))


if __name__ == "__main__":
    main()

