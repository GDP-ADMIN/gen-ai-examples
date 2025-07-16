"""TenantContextHolder is a thread-local storage for tenant context.

Authors:
    Berty C L Tobing (berty.c.l.tobing@gdplabs.id)

References:
    NONE
"""

import contextvars

TENANT_HEADER = "Tenant"


class TenantContext:
    """TenantContext holds the tenant name for the current thread.

    Attributes:
        tenant (str | None): The tenant name.
    """

    def __init__(self, tenant: str | None = None) -> None:
        """Initialize the TenantContext with a tenant name.

        Args:
            tenant (str | None, optional): The tenant name. Defaults to None.
        """
        self.tenant = tenant


_tenant_context_var: contextvars.ContextVar[TenantContext | None] = contextvars.ContextVar(
    "tenant_context", default=None
)


class TenantContextHolder:
    """TenantContextHolder is a context holder for tenant context."""

    @classmethod
    def get_context(cls) -> TenantContext:
        """Get the tenant context for the current thread.

        Returns:
            TenantContext: The tenant context for the current thread.
        """
        context = _tenant_context_var.get()
        if context is None:
            context = TenantContext()
            _tenant_context_var.set(context)
        return context

    @classmethod
    def set_context(cls, context: TenantContext) -> None:
        """Set the tenant context for the current thread.

        Args:
            context (TenantContext): The tenant context to set.
        """
        _tenant_context_var.set(context)

    @classmethod
    def clear_context(cls) -> None:
        """Clear the tenant context for the current thread."""
        _tenant_context_var.set(None)

    @classmethod
    def get_tenant(cls) -> str | None:
        """Get the tenant name from the current thread's context.

        Returns:
            str | None: The tenant name or None if not set.
        """
        context = cls.get_context()
        return context.tenant
