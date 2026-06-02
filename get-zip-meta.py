from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

CDN_BASE = "http://cdn.bzgames.top/bz-games-market"


def resolve_zip_path() -> Path:
    if len(sys.argv) > 1 and sys.argv[1].strip():
        raw_path = sys.argv[1].strip()
    else:
        raw_path = input("请输入 zip 文件路径: ").strip()

    path = Path(raw_path).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"文件不存在: {path}")
    return path


def resolve_game_name() -> str:
    if len(sys.argv) > 2 and sys.argv[2].strip():
        return sys.argv[2].strip()
    return input("请输入游戏名称（CDN 目录名，如 2048 / Bird Fly / 大海世界）: ").strip()


def resolve_version() -> str:
    if len(sys.argv) > 3 and sys.argv[3].strip():
        return sys.argv[3].strip()
    return input("请输入版本号（如 1.0.0）: ").strip()


def resolve_zip_filename(game_name: str) -> str:
    """返回 raw zip 文件名，默认 = 游戏名 + .zip"""
    default = game_name + ".zip"
    if len(sys.argv) > 4 and sys.argv[4].strip():
        return sys.argv[4].strip()
    custom = input(f"zip 文件名（默认: {default}）: ").strip()
    return custom if custom else default


def sha256_of_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        while True:
            chunk = file.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    zip_path = resolve_zip_path()
    game_name = resolve_game_name()
    version = resolve_version()
    zip_filename = resolve_zip_filename(game_name)

    encoded_name = quote(game_name)
    encoded_zip = quote(zip_filename)

    icon_url = f"{CDN_BASE}/{encoded_name}/icon.png"
    cover_url = f"{CDN_BASE}/{encoded_name}/cover.png"
    download_url = f"{CDN_BASE}/{encoded_name}/v{version}/{encoded_zip}"

    result = {
        "fileName": zip_path.name,
        "fullPath": str(zip_path),
        "sha256": sha256_of_file(zip_path),
        "size": zip_path.stat().st_size,
    }
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")

    print(
        json.dumps(
            {
                "sha256": result["sha256"],
                "size": result["size"],
                "publishedAt": now,
                "downloadUrl": download_url,
                "iconUrl": icon_url,
                "coverUrl": cover_url,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
