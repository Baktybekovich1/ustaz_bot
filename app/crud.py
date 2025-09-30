from sqlalchemy import select, insert
from .models import Lead
from .schemas import LeadCreate
from sqlalchemy.ext.asyncio import AsyncSession

async def create_lead(db: AsyncSession, payload: LeadCreate):
    obj = Lead(**payload.dict(exclude_none=True))
    db.add(obj)
    await db.flush()
    await db.commit()
    await db.refresh(obj)
    return obj

async def stream_leads_csv(db: AsyncSession):
    q = select(Lead)
    result = await db.execute(q)
    for row in result.scalars():
        yield row
