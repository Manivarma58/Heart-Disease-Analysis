from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app import create_app
from app.services.database_service import get_db, import_heart_csv, real_dataset_path

DEFAULT_CSV = ROOT / "data" / "Heart_new2_clean.csv"


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        csv_path = DEFAULT_CSV if DEFAULT_CSV.exists() else real_dataset_path()
        import_heart_csv(get_db(), csv_path)
    print(f"Imported {csv_path}")
