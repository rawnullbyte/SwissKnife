from __future__ import annotations

import importlib
from pathlib import Path

from fastapi import APIRouter


def discover_routers() -> list[APIRouter]:
    routers: list[APIRouter] = []

    for module_dir in sorted(Path(__file__).parent.iterdir()):
        if not module_dir.is_dir():
            continue
        if module_dir.name.startswith("_"):
            continue
        if not (module_dir / "router.py").exists():
            continue

        dotted = f"modules.{module_dir.name}.router"
        mod = importlib.import_module(dotted)

        router = getattr(mod, "router", None)
        if isinstance(router, APIRouter):
            routers.append(router)

    return routers
