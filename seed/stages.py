from sqlalchemy.ext.asyncio import AsyncSession
from app.models.stage import Stage, StageType, Direction


async def seed_stages(db: AsyncSession) -> dict:
    stages_data = [

        Stage(
            name="OTC Terminal",
            area="CBD",
            landmark="Accra Rd",
            stage_type=StageType.FORMAL,
            direction=Direction.INBOUND,
            latitude=-1.2855,
            longitude=36.8241
        ),
        Stage(
            name="OTC Stage",
            area="CBD",
            landmark="Departure Point",
            stage_type=StageType.FORMAL,
            direction=Direction.OUTBOUND,
            latitude=-1.2856,
            longitude=36.8242
        ),

        Stage(
            name="GPO Drop-off",
            area="CBD",
            landmark="Kenyatta Ave",
            stage_type=StageType.FORMAL,
            direction=Direction.INBOUND,
            latitude=-1.2841,
            longitude=36.8228
        ),
        Stage(
            name="GPO Pick-up",
            area="CBD",
            landmark="Opposite GPO",
            stage_type=StageType.FORMAL,
            direction=Direction.OUTBOUND,
            latitude=-1.2842,
            longitude=36.8229
        ),

        Stage(
            name="River Road",
            area="CBD",
            landmark="Tea Room",
            stage_type=StageType.FORMAL,
            direction=Direction.INBOUND,
            latitude=-1.2863,
            longitude=36.8252
        ),
        Stage(
            name="River Road",
            area="CBD",
            landmark="Latema Rd",
            stage_type=StageType.FORMAL,
            direction=Direction.OUTBOUND,
            latitude=-1.2864,
            longitude=36.8253
        ),

        Stage(
            name="Juja Main Stage",
            area="Juja",
            landmark="Equity",
            stage_type=StageType.FORMAL,
            direction=Direction.INBOUND,
            latitude=-1.1037,
            longitude=37.0144
        ),
        Stage(
            name="Juja Main Stage",
            area="Juja",
            landmark="Flyover",
            stage_type=StageType.FORMAL,
            direction=Direction.OUTBOUND,
            latitude=-1.1040,
            longitude=37.0148
        ),

        Stage(
            name="Kenyatta University",
            area="KU",
            landmark="Main Gate",
            stage_type=StageType.FORMAL,
            direction=Direction.INBOUND,
            latitude=-1.1820,
            longitude=36.9320
        ),
        Stage(
            name="Kenyatta University",
            area="KU",
            landmark="Exit Gate",
            stage_type=StageType.FORMAL,
            direction=Direction.OUTBOUND,
            latitude=-1.1821,
            longitude=36.9321
        ),

        Stage(
            name="Githurai 45",
            area="Githurai",
            landmark="Inbound Bridge",
            stage_type=StageType.FORMAL,
            direction=Direction.INBOUND,
            latitude=-1.2127,
            longitude=36.9285
        ),
        Stage(
            name="Githurai 45",
            area="Githurai",
            landmark="Outbound Bridge",
            stage_type=StageType.FORMAL,
            direction=Direction.OUTBOUND,
            latitude=-1.2128,
            longitude=36.9286
        ),

        Stage(
            name="Roysambu (TRM)",
            area="Roysambu",
            landmark="TRM",
            stage_type=StageType.FORMAL,
            direction=Direction.INBOUND,
            latitude=-1.2195,
            longitude=36.8887
        ),
        Stage(
            name="Roysambu (TRM)",
            area="Roysambu",
            landmark="Shell",
            stage_type=StageType.FORMAL,
            direction=Direction.OUTBOUND,
            latitude=-1.2196,
            longitude=36.8888
        ),

        Stage(
            name="Garden City",
            area="Ruaraka",
            landmark="Mall",
            stage_type=StageType.FORMAL,
            direction=Direction.INBOUND,
            latitude=-1.2320,
            longitude=36.8780
        ),
        Stage(
            name="Garden City",
            area="Ruaraka",
            landmark="Exit",
            stage_type=StageType.FORMAL,
            direction=Direction.OUTBOUND,
            latitude=-1.2321,
            longitude=36.8781
        ),

        Stage(
            name="Muthaiga",
            area="Muthaiga",
            landmark="Station",
            stage_type=StageType.FORMAL,
            direction=Direction.INBOUND,
            latitude=-1.2580,
            longitude=36.8350
        ),
        Stage(
            name="Muthaiga",
            area="Muthaiga",
            landmark="Opposite",
            stage_type=StageType.FORMAL,
            direction=Direction.OUTBOUND,
            latitude=-1.2581,
            longitude=36.8351
        ),

        Stage(
            name="Pangani",
            area="Pangani",
            landmark="Interchange",
            stage_type=StageType.FORMAL,
            direction=Direction.INBOUND,
            latitude=-1.2700,
            longitude=36.8300
        ),
        Stage(
            name="Pangani",
            area="Pangani",
            landmark="Tunnel",
            stage_type=StageType.FORMAL,
            direction=Direction.OUTBOUND,
            latitude=-1.2701,
            longitude=36.8301
        ),
    ]

    for s in stages_data:
        db.add(s)

    await db.commit()

    return {
        f"{s.name}_{s.direction.value.lower()}": s
        for s in stages_data
    }