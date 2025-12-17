import json
import pandas as pd

IN_CSV = r"Network_Data/phisingData.csv"
OUT_JSON = r"Network_Data/phisingData.json"


def csv_to_json(file_path: str):
    df = pd.read_csv(file_path)
    df.reset_index(drop=True, inplace=True)
    records = json.loads(df.T.to_json()).values()
    return list(records)


if __name__ == '__main__':
    records = csv_to_json(IN_CSV)
    with open(OUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    print(f'Wrote {len(records)} records to {OUT_JSON}')
