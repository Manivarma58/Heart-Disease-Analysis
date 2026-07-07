from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app import create_app
from app.services.database_service import get_db, import_heart_csv

DEFAULT_CSV = ROOT / "data" / "Heart_new2.csv"


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        import_heart_csv(get_db(), DEFAULT_CSV)
    print(f"Imported {DEFAULT_CSV}")
