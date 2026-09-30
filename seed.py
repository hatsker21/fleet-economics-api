from src.database import SessionLocal
from src.models.location import Location

def seed_locations():
    db = SessionLocal()
    
    # Перевіряємо, чи таблиця вже не має цих міст, щоб не дублювати
    if db.query(Location).count() == 0:
        loc1 = Location(name="Київ", slug="kyiv")
        loc2 = Location(name="Черкаси", slug="cherkasy")
        
        db.add_all([loc1, loc2])
        db.commit()
        print("✅ Міста 'Київ' та 'Черкаси' успішно додано!")
    else:
        print("⚠️ Міста вже існують у базі.")
        
    db.close()

if __name__ == "__main__":
    seed_locations()