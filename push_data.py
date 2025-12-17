import os
import json
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    # python-dotenv not installed; continue without loading .env
    load_dotenv = None

mongodb_url = os.getenv('MONGODB_URL')
print(mongodb_url)


import certifi
certifi.where()

import pandas as pd 
import numpy as np
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from  networksecurity.logging.logger import logging
import sys

class NetworkDataExtract:
    def __call__(self):
        try:
            pass
        except Exception as e:
            if isinstance(e, NetworkSecurityException):
                raise
            raise NetworkSecurityException(e, sys)

    def csv_to_json_converter(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = json.loads(data.T.to_json()).values()
            records = list(records)
            return records
        except Exception as e:
            if isinstance(e, NetworkSecurityException):
                raise
            raise NetworkSecurityException(e, sys)

    def insert_data_mongodb(self, records, database, collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records
            if not mongodb_url:
                logging.error('MONGODB_URL environment variable is not set')
                raise NetworkSecurityException('MONGODB_URL not set. Set MONGODB_URL in environment or .env', sys)

            # create client (will raise on connection issues)
            self.mongo_client = pymongo.MongoClient(mongodb_url, tlsCAFile=certifi.where())
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return len(self.records)
        except Exception as e:
            if isinstance(e, NetworkSecurityException):
                raise
            raise NetworkSecurityException(e, sys)

    def save_json(self, records, out_path: str):
        try:
            with open(out_path, 'w', encoding='utf-8') as f:
                json.dump(records, f, ensure_ascii=False, indent=2)
            return out_path
        except Exception as e:
            if isinstance(e, NetworkSecurityException):
                raise
            raise NetworkSecurityException(e, sys)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Push network CSV data to MongoDB or save as JSON')
    parser.add_argument('--file', '-f', default='Network_Data/phisingData.csv', help='Path to CSV file')
    parser.add_argument('--database', '-d', default='crash_i', help='MongoDB database name')
    parser.add_argument('--collection', '-c', default='network_data', help='MongoDB collection name')
    parser.add_argument('--dry-run', action='store_true', help='Write JSON to file instead of inserting to MongoDB')
    parser.add_argument('--out', '-o', default='Network_Data/phisingData_from_push.json', help='Output JSON path for dry run')

    args = parser.parse_args()

    network_obj = NetworkDataExtract()
    records = network_obj.csv_to_json_converter(args.file)

    if args.dry_run:
        out_path = network_obj.save_json(records, args.out)
        print(f'Wrote {len(records)} records to {out_path}')
    else:
        number_of_records = network_obj.insert_data_mongodb(records, args.database, args.collection)
        print(f'Number of records inserted: {number_of_records}')



