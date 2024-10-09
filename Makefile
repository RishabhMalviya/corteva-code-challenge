SHELL := /bin/bash

# Colors for `echo` commands
RED = \033[31m
GREEN = \033[32m
YELLOW = \033[33m
BLUE = \033[34m
RESET = \033[0m

clean:
	find . | grep -E "(__pycache__|.pytest_cache|.ipynb_checkpoints|*.egg-info)" | xargs rm -rf

setup: clean
	@if [ -d "./.venv" ]; then \
		echo  "Deleting existing venv..."; \
		rm -rf ./.venv; \
		echo "Existing venv removed"; \
	fi
	python3 -m venv .venv
	source ./.venv/bin/activate && pip install -e .[dev]
	@echo -e "\n$(RED)NOTE!!$(RESET): Activate the venv with the following command: $(GREEN)source ./.venv/bin/activate$(RESET)"

run_data_pipeline:
	if [ -f "local_db.db" ]; then \
		rm "local_db.db"; \
		echo "Existing Local DB deleted."; \
	fi
	source ./.venv/bin/activate && python ./src/scripts/run_data_pipeline.py

run_data_analysis:
	source ./.venv/bin/activate && python ./src/scripts/run_data_analysis.py

run_api:
	@echo -e "\n\nOnce you see \"$(YELLOW)Application startup complete$(RESET)\" below, navigate to $(GREEN)localhost:8501/docs$(RESET) in your browser to test the API:\n\n"
	source ./.venv/bin/activate && uvicorn --port 8501 --reload src.scripts.app:app

run: run_data_pipeline run_data_analysis run_api

all: clean setup run

test:
	if [ -f "local_db.db" ]; then \
		rm "local_db.db"; \
		echo "Existing Local DB deleted."; \
	fi
	source ./.venv/bin/activate && pytest	