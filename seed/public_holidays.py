from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.fare import PublicHoliday


async def seed_public_holidays(db: AsyncSession):
    holidays = [
        PublicHoliday(name="New Year's Day", holiday_date=date(2025, 1, 1), is_recurring=True),
        PublicHoliday(name="Labour Day", holiday_date=date(2025, 5, 1), is_recurring=True),
        PublicHoliday(name="Madaraka Day", holiday_date=date(2025, 6, 1), is_recurring=True),
        PublicHoliday(name="Huduma Day", holiday_date=date(2025, 10, 10), is_recurring=True),
        PublicHoliday(name="Mashujaa Day", holiday_date=date(2025, 10, 20), is_recurring=True),
        PublicHoliday(name="Jamhuri Day", holiday_date=date(2025, 12, 12), is_recurring=True),
        PublicHoliday(name="Christmas Day", holiday_date=date(2025, 12, 25), is_recurring=True),
        PublicHoliday(name="Boxing Day", holiday_date=date(2025, 12, 26), is_recurring=True),
        PublicHoliday(name="Good Friday", holiday_date=date(2025, 4, 18), is_recurring=False, year=2025),
        PublicHoliday(name="Easter Monday", holiday_date=date(2025, 4, 21), is_recurring=False, year=2025),
    ]
    for h in holidays:
        db.add(h)
    await db.commit()
    print(f"  seeded {len(holidays)} public holidays")