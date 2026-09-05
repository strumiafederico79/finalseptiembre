from __future__ import annotations

from fastapi import APIRouter

# Delegate router creation to the mastering_routes shim which keeps the
# original route source for now. This removes exec() from this module and
# centralizes the transitional logic in backend/routers/mastering_routes.py.

from .mastering_routes import create_router as _create_router_impl


def create_router(**dependencies):
    """Return an APIRouter built by the mastering_routes implementation.

    Kept as a thin wrapper so callers (importing create_mastering_router)
    continue to work as before.
    """
    return _create_router_impl(**dependencies)
