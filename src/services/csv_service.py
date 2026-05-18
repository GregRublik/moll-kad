import csv
import re
from datetime import datetime
from pathlib import Path
from typing import Literal


class CsvService:
    base_dir = Path(__file__).parent.parent.parent / "results"

    @staticmethod
    def _sanitize_filename(value: str) -> str:
        # заменяем всё, что может ломать имя файла
        return re.sub(r'[\\/*?:"<>|]', "_", value)

    @staticmethod
    def _normalize(value):
        if isinstance(value, (dict, list)):
            return str(value)
        return value

    def save_results(
        self,
        num_deal: str,
        type_data: Literal["search", "info"],
        results: list[dict]
    ) -> Path:

        # папка: results/search или results/info
        dir_path = self.base_dir / type_data
        dir_path.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y.%m.%d_%H-%M-%S")
        filename = f"{timestamp}_{type_data}_{num_deal}.csv"
        filename = self._sanitize_filename(filename)

        filepath = dir_path / filename

        fieldnames = sorted({key for row in results for key in row.keys()})

        with filepath.open(mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for row in results:
                writer.writerow({
                    k: self._normalize(v)
                    for k, v in row.items()
                })

        return filepath