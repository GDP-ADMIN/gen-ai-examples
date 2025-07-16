"""Tenant context middleware for FastAPI.

This middleware sets the tenant context for each request based on the tenant identifier provided in the request headers.

Authors:
    Berty C L Tobing (berty.c.l.tobing@gdplabs.id)

References:
    NONE
"""

from starlette.types import ASGIApp, Receive, Scope, Send

from claudia_gpt.multi_tenant.context.tenant_context_holder import TENANT_HEADER, TenantContext, TenantContextHolder


class TenantContextMiddleware:
    """ASGI middleware to set tenant context from header.

    Attributes:
        app (ASGIApp): The ASGI application to wrap with this middleware.
    """

    def __init__(self, app: ASGIApp) -> None:
        """Initialize the middleware with the ASGI application.

        Args:
            app (ASGIApp): The ASGI application to wrap with this middleware.
        """
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """Process an ASGI request, setting tenant context from headers.

        Args:
            scope (Scope): The ASGI connection scope.
            receive (Receive): The ASGI receive function.
            send (Send): The ASGI send function.

        Returns:
            None
        """
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        headers = {k.decode("latin1").lower(): v.decode("latin1") for k, v in scope.get("headers", [])}
        tenant_id = headers.get(TENANT_HEADER.lower())

        try:
            TenantContextHolder.set_context(TenantContext(tenant=tenant_id))
            await self.app(scope, receive, send)
        finally:
            TenantContextHolder.clear_context()
