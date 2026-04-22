from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from app.models.intelligence import AppSettings

async def seed_app_settings(db: AsyncSession):
    # We use a list of dictionaries instead of model instances 
    # to work easily with the PostgreSQL 'insert' function.
    settings_data = [
        {"key": "fare_staleness_high_days", "value": "7", "description": "Days before fare confidence drops to medium"},
        {"key": "fare_staleness_medium_days", "value": "21", "description": "Days before fare confidence drops to low"},
        {"key": "correction_consensus_count", "value": "3", "description": "Number of matching corrections to flag a fare as stale"},
        {"key": "correction_window_days", "value": "7", "description": "Window in days to look for matching corrections"},
        {"key": "surge_multiplier_max", "value": "3.00", "description": "Maximum allowed surge multiplier"},
        {"key": "score_weight_fare", "value": "0.40", "description": "Scoring weight for fare amount"},
        {"key": "score_weight_duration", "value": "0.25", "description": "Scoring weight for journey duration"},
        {"key": "score_weight_proximity", "value": "0.15", "description": "Scoring weight for boarding proximity"},
        {"key": "score_weight_comfort", "value": "0.10", "description": "Scoring weight for comfort rating"},
        {"key": "score_weight_confidence", "value": "0.10", "description": "Scoring weight for data confidence"},
        {"key": "fuzzy_match_confirm_threshold", "value": "85", "description": "Score above which a fuzzy match is confirmed"},
        {"key": "fuzzy_match_suggest_threshold", "value": "75", "description": "Score above which a fuzzy match is suggested"},
    ]

    for data in settings_data:
        # 1. Create the insert statement
        stmt = insert(AppSettings).values(**data)
        
        # 2. Define the 'Upsert' logic
        # If the 'key' (Primary Key) conflicts, update 'value' and 'description'
        stmt = stmt.on_conflict_do_update(
            index_elements=['key'],
            set_={
                "value": stmt.excluded.value,
                "description": stmt.excluded.description
            }
        )
        
        await db.execute(stmt)

    await db.commit()
    print(f"  seeded/updated {len(settings_data)} app settings")