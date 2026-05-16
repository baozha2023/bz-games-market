from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def resolve_zip_path() -> Path:
    if len(sys.argv) > 1 and sys.argv[1].strip():
        raw_path = sys.argv[1].strip()
    else:
        raw_path = input("请输入 zip 文件路径: ").strip()

    path = Path(raw_path).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"文件不存在: {path}")
    return path


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
    result = {
        "fileName": zip_path.name,
        "fullPath": str(zip_path),
        "sha256": sha256_of_file(zip_path),
        "size": zip_path.stat().st_size,
    }
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")

    print("\n结果：")
    print(json.dumps(result, ensure_ascii=False, indent=2))

    print("\n当前时间（ISO 8601）：")
    print(f"  {now}")

    print("\n可直接粘贴到 market.json 的字段：")
    print(
        json.dumps(
            {
                "sha256": result["sha256"],
                "size": result["size"],
                "publishedAt": now,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
