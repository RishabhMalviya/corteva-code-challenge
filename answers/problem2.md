# Code for ingestion is [here](https://github.com/RishabhMalviya/corteva-code-challenge/tree/main/src/data_ingestion)
A usage example is [here](https://github.com/RishabhMalviya/corteva-code-challenge/blob/main/scripts/data_pipeline.py). To run this in your environment, run `make clean && make setup && make run_data_pipeline` from the root of this repo.

## Additional comments:
There are no duplicates because the data model specifies primary keys - https://github.com/RishabhMalviya/corteva-code-challenge/blob/main/src/data_models/weather_data.py#L14
Logging is being done here - https://github.com/RishabhMalviya/corteva-code-challenge/blob/main/src/data_ingestion/ingest_weather_data.py#L61
