import boto3
import datetime
import json
import os
from tempfile import NamedTemporaryFile
from typing import List


class DataTypeNotSuppoetedForIngestionException(Exception):
    def __init__(self, data):
        self.data = data
        self.message = f"Data Type {type(data)} is not supported for ingestion"
        super().__init__(self.message)


class DataWriter():
    def __init__(self, coin: str, api: str) -> None:
        self.coin = coin
        self.api = api
        self.filename = f"{self.api}/{self.coin}/{datetime.datetime.now()}.json"
    
    def _write_row(self, row: str) -> None:
        os.makedirs(os.path.dirname(self.filename), exist_ok = True)
        # insere os dados no modo append
        with open(self.filename, "a") as f:
            f.write(row)
    
    def _write_to_file(self, data: [List, dict]):
        # isinstance verifica a classe do tipo data
        if isinstance(data, dict):
            self._write_row(json.dumps(data) + "\n")
        elif isinstance(data, List):
            for element in data:
                self.write(element)
        else:
            raise DataTypeNotSuppoetedForIngestionException(data)
    
    def write(self, data: [List, dict]):
        self._write_to_file(data=data)
        


class S3Writer(DataWriter):
    def __init__(self, coin: str, api: str):
        super().__init__(coin, api)
        self.temp_file = NamedTemporaryFile()
        self.client = boto3.client("s3")
        self.key = f"mercado_bitcoin/{self.api}/coin={self.coin}/extracted_at={datetime.datetime.now().date()}/{self.api}_{self.coin}_{datetime.datetime.now()}.json"
        
    
    def _write_row(self, row: str) -> None:
        with open(self.temp_file.name, "a") as f:
            f.write(row)

    def write(self, data: [List, dict]):
        # escrever para o S3
        self._write_to_file(data=data)
        self._write_file_to_s3()

    
    def _write_file_to_s3(self):
        self.client.put_object(
            Body=self.temp_file,
            Bucket="volponi-how-lambda-btc",
            Key=self.key
        )