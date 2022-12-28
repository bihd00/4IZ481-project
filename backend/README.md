# Backend

## Stack

- [Python](https://www.python.org/)
- [Google Cloud Functions](https://developers.google.com/learn/topics/functions)

## Development

- configure environment
  - add `service-account-key.json` to the root of the backend folder
  - create `.env` file at the root of the backend folder
  - add necessary variables
- install Python `3.10.9`
- in your terminal, run:
  - (optional) `python -m venv venv`
  - (optional) `source venv/Scripts/activate`
  - `pip install -r requirements.txt`
- functions are located in **cloud_functions** folder

### Testing

- since backend functions are primarily event-based (opposed to http-based), testing them locally the "google-cloud-way" is rather troublesome
- as a workaround, tests are run as any other python file 
- environment has to be set up properly
- function tests are located in the **tests** folder
- the code in tests is very comparable to the code in cloud_functions

## Deployment

- backend is deployed as separate cloud functions
- Example Google Cloud CLI deployment command for a firestore document.write trigger
```
gcloud functions deploy <function_name> \
    --entry-point=<function_name> \
    --region=<region_id> \
    --runtime=python310 \
    --trigger-event="providers/cloud.firestore/eventTypes/document.write" \
    --trigger-resource="projects/<project_id>/databases/(default)/documents/<schema>/{recordId}"
```