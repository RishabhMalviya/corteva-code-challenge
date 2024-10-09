# Problem 2 - Ingestion
1. The core code for ingestion is [here](https://github.com/RishabhMalviya/corteva-code-challenge/tree/main/src/data_ingestion)

2. The script to invoke the code and run the ingestion pipeline is [here](https://github.com/RishabhMalviya/corteva-code-challenge/blob/main/scripts/data_pipeline.py).

## Running Locally
To run this locally, execute the following commands from the repo root (AFTER activating your venv; run `make setup && source ./.venv/bin/activate` if you're not sure): 
  ```bash
  make clean && make run_data_pipeline
  ```

## Additional comments:
1. There are no duplicates because the data model specifies primary keys - https://github.com/RishabhMalviya/corteva-code-challenge/blob/main/src/data_models/weather_data.py#L14
2. Logging is being done here - https://github.com/RishabhMalviya/corteva-code-challenge/blob/main/src/data_ingestion/ingest_weather_data.py#L61
