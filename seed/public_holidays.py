from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from app.models.fare import PublicHoliday
import datetime


async def seed_public_holidays(db: AsyncSession):
    current_year = 2026

    holidays_data = [
           # Static Dates (Recurring)
            {"name": "New Year's Day", "holiday_date": datetime.date(
                current_year, 1, 1), "is_recurring": True, "year": None},
            {"name": "Labour Day", "holiday_date": datetime.date(
                current_year, 5, 1), "is_recurring": True, "year": None},
            {"name": "Madaraka Day", "holiday_date": datetime.date(
                current_year, 6, 1), "is_recurring": True, "year": None},
            {"name": "Huduma Day", "holiday_date": datetime.date(
                current_year, 10, 10), "is_recurring": True, "year": None},
            {"name": "Mashujaa Day", "holiday_date": datetime.date(
                current_year, 10, 20), "is_recurring": True, "year": None},
            {"name": "Jamhuri Day", "holiday_date": datetime.date(
                current_year, 12, 12), "is_recurring": True, "year": None},
            {"name": "Christmas Day", "holiday_date": datetime.date(
                current_year, 12, 25), "is_recurring": True, "year": None},
            {"name": "Boxing Day", "holiday_date": datetime.date(
                current_year, 12, 26), "is_recurring": True, "year": None},

            # Movable Dates for 2026
            {"name": "Good Friday", "holiday_date": datetime.date(
                2026, 4, 3), "is_recurring": False, "year": 2026},
            {"name": "Easter Monday", "holiday_date": datetime.date(
                2026, 4, 6), "is_recurring": False, "year": 2026},
            {"name": "Idd-ul-Fitr", "holiday_date": datetime.date(
                2026, 3, 20), "is_recurring": False, "year": 2026},  # Approx
           ]

    for data in holidays_data:
            stmt = insert(PublicHoliday).values(**data)

            # We conflict on the date (or whatever your unique constraint is)
            # If the date exists, update the name and recurring status
            stmt = stmt.on_conflict_do_update(
                index_elements=['holiday_date'],
                set_={
                    "name": stmt.excluded.name,
                    "is_recurring": stmt.excluded.is_recurring,
                    "year": stmt.excluded.year
                }
            )
            await db.execute(stmt)

    await db.commit()
    print(f"  seeded/updated {len(holidays_data)} public holidays")
