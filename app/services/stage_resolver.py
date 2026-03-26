from rapidfuzz import fuzz
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, func
from app.models.stage import Stage, Direction
from app.models.sacco import SaccoAlias
from app.schemas.stage import StageRead, StageResolveResult


CONFIRM_THRESHOLD = 85
SUGGEST_THRESHOLD = 75


async def get_setting(db: AsyncSession, key: str, default: str) -> str:
    from app.models.intelligence import AppSettings
    result = await db.execute(select(AppSettings).where(AppSettings.key == key))
    setting = result.scalar_one_or_none()
    return setting.value if setting else default


async def resolve_stage(
    query: str,
    db: AsyncSession,
    direction_filter: Direction | None = None,
) -> StageResolveResult | None:
    query_lower = query.lower().strip()

    # 1. Build the query for an exact name match
    stmt = select(Stage).where(
        Stage.is_active == True,
        func.lower(Stage.name) == query_lower,
    )

    # 2. Apply direction filter if provided
    if direction_filter and direction_filter != Direction.BOTH:
        stmt = stmt.where(
            or_(
                Stage.direction == direction_filter,
                Stage.direction == Direction.BOTH
            )
        )

    # 3. Use .first() instead of .scalar_one_or_none()
    # This prevents the 500 crash even if data is slightly messy
    result = await db.execute(stmt)
    exact = result.scalars().first()

    if exact:
        return StageResolveResult(
            stage=StageRead.model_validate(exact),
            match_confidence="exact",
            score=100.0,
        )

    result = await db.execute(select(Stage).where(Stage.is_active == True))
    all_stages = result.scalars().all()
    print(f"Fuzzy matching '{query}' against {len(all_stages)} stages", {result})
    best_stage = None
    best_score = 0.0

    for stage in all_stages:
        name_score = fuzz.token_sort_ratio(query_lower, stage.name.lower())
        area_score = fuzz.token_sort_ratio(query_lower, stage.area.lower())
        score = max(name_score, area_score)
        if score > best_score:
            best_score = score
            best_stage = stage

    if best_stage is None:
        return None

    confirm_threshold = int(await get_setting(db, "fuzzy_match_confirm_threshold", "85"))
    suggest_threshold = int(await get_setting(db, "fuzzy_match_suggest_threshold", "75"))

    if best_score < suggest_threshold:
        return None

    if direction_filter and direction_filter != Direction.BOTH:
        if best_stage.direction not in (direction_filter, Direction.BOTH):
            return None

    confidence = "confirmed" if best_score >= confirm_threshold else "fuzzy"

    return StageResolveResult(
        stage=StageRead.model_validate(best_stage),
        match_confidence=confidence,
        score=best_score,
    )
