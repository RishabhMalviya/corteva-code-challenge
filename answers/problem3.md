# Problem 3 - Data Analysis
1. The core code for ingestion is [here](https://github.com/RishabhMalviya/corteva-code-challenge/tree/main/src/data_analysis)
2. The script to invoke the code and run the analysis pipeline is [here](https://github.com/RishabhMalviya/corteva-code-challenge/blob/main/scripts/data_analysis.py). 

## Running Locally
To run this locally, execute the following commands from the repo root (AFTER activating your venv; run `make setup && source ./.venv/bin/activate` if you're not sure):
```bash
make clean && make run_data_pipeline && make run_data_analysis
``` 
If you have already executed the command given in `problem2.md`, just execute:
```bash
make run_data_analysis
```

## Additional Notes
The data model for the output of the data analysis pipeline is [here](https://github.com/RishabhMalviya/corteva-code-challenge/blob/main/src/data_models/yearly_aggregations.py#L11)
