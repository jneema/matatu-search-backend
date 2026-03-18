from sqlalchemy.ext.asyncio import AsyncSession
from app.models.intelligence import AppSettings


async def seed_app_settings(db: AsyncSession):
    settings = [
        AppSettings(key="fare_staleness_high_days", value="7", description="Days before fare confidence drops to medium"),
        AppSettings(key="fare_staleness_medium_days", value="21", description="Days before fare confidence drops to low"),
        AppSettings(key="correction_consensus_count", value="3", description="Number of matching corrections to flag a fare as stale"),
        AppSettings(key="correction_window_days", value="7", description="Window in days to look for matching corrections"),
        AppSettings(key="surge_multiplier_max", value="3.00", description="Maximum allowed surge multiplier"),
        AppSettings(key="score_weight_fare", value="0.40", description="Scoring weight for fare amount"),
        AppSettings(key="score_weight_duration", value="0.25", description="Scoring weight for journey duration"),
        AppSettings(key="score_weight_proximity", value="0.15", description="Scoring weight for boarding proximity"),
        AppSettings(key="score_weight_comfort", value="0.10", description="Scoring weight for comfort rating"),
        AppSettings(key="score_weight_confidence", value="0.10", description="Scoring weight for data confidence"),
        AppSettings(key="fuzzy_match_confirm_threshold", value="85", description="Score above which a fuzzy match is confirmed"),
        AppSettings(key="fuzzy_match_suggest_threshold", value="75", description="Score above which a fuzzy match is suggested"),
    ]
    for s in settings:
        db.add(s)
    await db.commit()
    print(f"  seeded {len(settings)} app settings")