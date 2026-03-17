import structlog
from sqlalchemy.ext.asyncio import AsyncSession

log = structlog.get_logger()


async def notify_corridor_surge(corridor_id, reason: str, db: AsyncSession) -> None:
    log.info("corridor_surge_created", corridor_id=str(corridor_id), reason=reason)


async def notify_route_alert(route_id, alert_type: str, message: str, db: AsyncSession) -> None:
    log.info("route_alert_created", route_id=str(route_id), alert_type=alert_type, message=message)