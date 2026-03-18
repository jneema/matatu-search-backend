from sqlalchemy.ext.asyncio import AsyncSession
from app.models.stage import Stage, StageType, Direction


async def seed_stages(db: AsyncSession) -> dict:
    stages_data = [
        Stage(name="Juja Stage", area="Juja", landmark="Opposite Equity Bank Juja", stage_type=StageType.FORMAL, direction=Direction.INBOUND, latitude=-1.1037, longitude=37.0144, is_active=True),
        Stage(name="Juja Stage", area="Juja", landmark="Juja outbound side", stage_type=StageType.FORMAL, direction=Direction.OUTBOUND, latitude=-1.1040, longitude=37.0148, is_active=True),
        Stage(name="Thika Road Mall Stage", area="TRM", landmark="Opposite TRM entrance", stage_type=StageType.FORMAL, direction=Direction.INBOUND, latitude=-1.2005, longitude=36.8899, is_active=True),
        Stage(name="Roysambu Stage", area="Roysambu", landmark="After Roysambu junction", stage_type=StageType.FORMAL, direction=Direction.INBOUND, latitude=-1.2195, longitude=36.8887, is_active=True),
        Stage(name="Githurai Stage", area="Githurai", landmark="Githurai 44 stage", stage_type=StageType.FORMAL, direction=Direction.INBOUND, latitude=-1.2127, longitude=36.9285, is_active=True),
        Stage(name="GPO Stage", area="CBD", landmark="Opposite GPO, Kenyatta Avenue", stage_type=StageType.FORMAL, direction=Direction.BOTH, latitude=-1.2841, longitude=36.8228, is_active=True),
        Stage(name="OTC Stage", area="CBD", landmark="Outside OTC, Accra Road", stage_type=StageType.FORMAL, direction=Direction.BOTH, latitude=-1.2855, longitude=36.8241, is_active=True),
        Stage(name="River Road Stage", area="CBD", landmark="River Road near Latema", stage_type=StageType.FORMAL, direction=Direction.BOTH, latitude=-1.2863, longitude=36.8252, is_active=True),
    ]
    for s in stages_data:
        db.add(s)
    await db.commit()

    result = {}
    for s in stages_data:
        key = f"{s.area}_{s.direction.value}"
        result[key] = s

    print(f"  seeded {len(stages_data)} stages")
    return result