from mcp.server.fastmcp import Context


def get_thread_id(ctx: Context) -> str:
    """
    Get the thread ID from the context.
    """
    return ctx.request_context.request.headers.get("X-Thread-Id") or ctx.request_context.request.headers.get("x-thread-id")