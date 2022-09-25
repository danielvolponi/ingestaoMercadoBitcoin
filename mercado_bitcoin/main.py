#%%
import datetime
from schedule import repeat, every, run_pending
import time

from mercado_bitcoin.ingestors import AwsDaysummaryIngestor
from mercado_bitcoin.writers import S3Writer

if __name__ == '__main__':
    day_summary_ingestor = AwsDaysummaryIngestor(
        writer = S3Writer, 
        coins = ["BTC", "ETH", "LTC"], 
        default_start_date=datetime.date(2021, 6, 2)
        )

    @repeat(every(1).seconds)
    def job():
        day_summary_ingestor.ingest()

    while True:
        run_pending()
        time.sleep(0.5)