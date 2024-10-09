# How to run the API Server
Simply execute `make run_api` from the root of this repository. The navigate to `localhost:8501/docs` in your browser to play around with the APIs.

## Additional Notes
1. For `api/weather/`, you can choose not to provide the `date` query parameter. In that case, the output will be paginated.
2. For `api/weather/stats/`, you can choose not to provide the `year` query parameter. In that case, the output will be paginated.
