# file: src/app/core/mixins/audit_mixin.py

from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, Integer, Boolean, event


class AuditMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    created_by: Mapped[int | None] = mapped_column(Integer, nullable=True)
    updated_by: Mapped[int | None] = mapped_column(Integer, nullable=True)

    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


@event.listens_for(AuditMixin, "before_update", propagate=True)
def _set_updated_at(mapper, connection, target):
    target.updated_at = datetime.utcnow()

# end file: src/app/core/mixins/audit_mixin.py