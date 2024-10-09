# Code Challenge Submission - Rishabh Malviya

The answers for the individual questions can be found in the [`answers`](https://github.com/RishabhMalviya/corteva-code-challenge/tree/main/answers) folder. They are just markdown files describing the answers with any additional links also in there.

## How to Run Locally
### 1. Setup
This solution makes use of `pyproject.toml` and expects the end user to have `pip` and `python` (>=3.10) installed on their system.

Run `make setup` to setup your local venv. Then run `source ./.venv/bin/activate` to activate it. All the following steps assume you have this venv activated.

#### Running Tests
You can run tests by simply running `pytest` from the repo root.

### 2. Data Ingestion Pipeline
Run `make run_data_pipeline`. This takes several minutes to complete. Patience....

### 3. Data Analysis Pipeline
Run `make run_data_analysis`. This should complete pretty quickly (1-2 minutes)

### 4. REST API
The previous two steps populate a SQLite database. You'll see a `local_db.db` file generated in the repo root; **DO NOT** delete it! That *is* the SQLite DB.

Now that you have the DB, you start the API server to interact with it. Run `make run_api` and then navigate to `localhost:8501/docs` in your browser to interact with the API and get data from the DB.

## How to Deploy (Bonus Question)
The first step to any deployment process would be to containerize this code. We could use a simple `python:3.10.12` base container, copy our code over, pip install it, and then specify the entrypoint. 

Something like this:
```Dockerfile
FROM python:3.10.12

COPY ./ /opt/build/corteva-code-challenge/
WORKDIR /opt/build/
RUN pip install ./corteva-code-challenge/

WORKDIR ~
RUN rm -rf /opt/build/

COPY ./src/scripts ./
COPY .env ./

# For Data Ingestion Pipeline
ENTRYPOINT ["python", "./src/scripts/run_data_pipeline.py"]
# For Data Analysis Pipeline
ENTRYPOINT ["python", "./src/scripts/run_data_analysis.py"]
# For REST API
ENTRYPOINT ["uvicorn", "--port", "8501", "--reload", "src.scripts.app:app"]
```

Once these containers are built, they can be uploaded into a registry (ECR in AWS).

### Data Ingestion/Analysis Pipeline
We can orchestrate these two steps in AWS through MWAA (managed Airflow). The `Operators` in Airflow would essentially spin up these containers and execute their entrypoints. The DAG would have two nodes:
```python
ingestion >> aggregation
```

### REST API
We can use the same container (with the last `ENTRYPOINT`, and appropriate port-forwarding) to deploy through a service like ECS on AWS.

That ECS deployment can then be exposed through a load balancer (ELB on AWS), and associated with a domain (using Route53) or simply through an IP address.
