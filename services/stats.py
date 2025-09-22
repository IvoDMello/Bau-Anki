from sqlalchemy import func
from models import db, Entry

def count_total():
    return db.session.scalar(db.select(func.count(Entry.id))) or 0

def count_today():
    return db.session.scalar(
        db.select(func.count(Entry.id)).where(func.date(Entry.created_at) == func.date(func.now()))
    ) or 0

def count_by_tag():
    # retorna dict {tag: count}; tags separadas por espaço
    rows = Entry.query.with_entities(Entry.tags).all()
    agg = {}
    for (tags,) in rows:
        if not tags:
            continue
        for t in tags.split():
            t = t.strip()
            if not t:
                continue
            agg[t] = agg.get(t, 0) + 1
    return agg
