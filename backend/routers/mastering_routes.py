from fastapi import APIRouter

# This module materializes the dynamic route source that used to live in
# backend/routers/mastering.py. It imports the _ROUTE_SOURCE string from
# that module and exec()s it into a router using the dependencies provided
# by the caller of create_router().
#
# NOTE: this is a transitional helper to restore runtime behavior after
# the __init__ refactor. It preserves the original route source without
# duplicating it here. The long-term goal is to convert the route source
# into normal Python code (no exec) and move the handlers here explicitly.

from . import mastering as _mastering_src


def create_router(**dependencies):
    """Create an APIRouter by executing the original _ROUTE_SOURCE.

    The caller must pass the same dependency names that the original
    namespace expected (e.g. get_current_user, read_and_validate, jobs, etc.).
    """
    router = APIRouter()
    namespace = dict(dependencies)
    namespace["router"] = router

    _route_source = getattr(_mastering_src, "_ROUTE_SOURCE", None)
    if _route_source is None:
        raise ImportError("_ROUTE_SOURCE not found in backend.routers.mastering")

    # Execute the source in the provided namespace so the route handlers
    # are registered on `router` and can reference the provided dependencies.
    exec(compile(_route_source, _mastering_src.__file__, "exec"), namespace, namespace)

    return router
