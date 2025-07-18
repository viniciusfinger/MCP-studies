from mcp.server.fastmcp import Context


def get_thread_id(context: Context) -> str:
    """
    Get the thread ID from the context.
    """
    return context.request_context.request.headers.get("X-Thread-Id") or context.request_context.request.headers.get("x-thread-id")