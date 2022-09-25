from mercado_bitcoin.ingestors import AwsDaysummaryIngestor
from mercado_bitcoin.writers import S3Writer
import datetime
import logging

logger = logging.getLogger()
logging.basicConfig(level="INFO")

def lambda_handler(event, context):
    logger.info(f"{event}")
    logger.info(f"{context}")
    
    AwsDaysummaryIngestor(
        writer = S3Writer, 
        coins = ["BTC", "ETH", "LTC"], 
        default_start_date=datetime.date(2021, 6, 2)
    ).ingest()
