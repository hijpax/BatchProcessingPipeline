# Batch Processing Pipeline with Dataflow
A pipeline to read text files from Cloud Storage to BigQuery with Dataflow.

## Setting up authentication
To run the client library, you must first set up authentication. One way to do that is to create a service account and set an environment variable, as shown in the following steps.

1. Create the service account:
   ```shell
    gcloud iam service-accounts create pipeline
    ```
2. Grant roles to the service account. Run the following command:
    ```shell
   gcloud projects add-iam-policy-binding empyrean-surge-360315 --member="serviceAccount:pipeline@empyrean-surge-360315.iam.gserviceaccount.com" --role=roles/storage.admin
   ```
3. Generate the key file:
    ```shell
    gcloud iam service-accounts keys create /home/jirene_delgadoh/keys.json --iam-account=pipeline@empyrean-surge-360315.iam.gserviceaccount.com
    ```
4. Provide authentication credentials to your application code by setting the environment variable GOOGLE_APPLICATION_CREDENTIALS.
    ```shell
    export GOOGLE_APPLICATION_CREDENTIALS="/home/jirene_delgadoh/keys.json"
    ```
1- Set environment on Shell\
2- Clone repo\
3- Create bucket\
4- Copy data to the bucket\
5- Create the BQ dataset\
bq mk ecommerce_behavor\
4- Build the Docker image\
docker build -t beam_python .\
5- Run a docker container with the new image\
docker run -it -e PROJECT=$PROJECT -v /home/jirene_delgadoh/keys.json:/keys.json -v $(pwd)/pipeline:/pipeline beam_python \
6 - Set the variables\
```shell
export GOOGLE_APPLICATION_CREDENTIALS=/keys.json \
export PROJECT=empyrean-surge-360315 \
export INPUT_BUCKET=ecomerce-behavor-bucket \
export INPUT_PATH=data \
export FILES_LIST=report_names.txt \
export BQ_DATASET=ecommerce_behavor
```
```shell
python pipeline.py \
--project=$PROJECT --region= \
--runner=DataflowRunner \
--staging_location=gs://$INPUT_BUCKET/test \
--temp_location gs://$INPUT_BUCKET/test \
--input-bucket=$INPUT_BUCKET \
--input-path=$INPUT_PATH \
--input-files-list=$FILES_LIST \
--bq-dataset=$BQ_DATASET 
```

7 - Enable access with the steps https://stackoverflow.com/questions/56302658/anonymous-caller-does-not-have-storage-objects-get

## Resources
* [Override the organization policy for a project](https://cloud.google.com/resource-manager/docs/organization-policy/using-constraints#v2-api_6)
* [Google BigQuery - Tableau](https://help.tableau.com/current/pro/desktop/en-us/examples_googlebigquery.htm)
* [Requiring permission to attach service accounts to resources - Dataflow](https://cloud.google.com/iam/docs/service-accounts-actas#dataproc-dataflow-datafusion)
* [Bigquery - Data Types](https://cloud.google.com/bigquery/docs/reference/standard-sql/data-types#data_type_properties)
* [Cloud Storage client libraries setup](https://cloud.google.com/storage/docs/reference/libraries#client-libraries-install-python)
* [Read files in Google Cloud Storage Bucket Using Python](https://github.com/vigneshSs-07/Cloud-AI-Analytics/tree/main/Cloud%20Storage#hands-on-on-read-files-in-google-cloud-storage-bucket-using-python)
* [How to Read Different Types Of files from Google Cloud Storage Bucket Using Python](https://www.youtube.com/watch?v=bHudgNDyltI&t=117s)
* [Google APIs tips](https://stackoverflow.com/questions/56302658/anonymous-caller-does-not-have-storage-objects-get)
* [Writing an ETL pipeline using Apache Beam and Cloud Dataflow (Python) - Lab](https://www.cloudskillsboost.google/course_sessions/1524821/labs/103668)
* [Basic ETL pipeline](https://github.com/GoogleCloudPlatform/training-data-analyst/blob/master/quests/dataflow_python/1_Basic_ETL/solution/my_pipeline.py)
* [Dataflow python - batch examples](https://github.com/GoogleCloudPlatform/professional-services/tree/main/examples/dataflow-python-examples/batch-examples/cookbook-examples)
* [Cloud Storage to Big Query Batch Job - Tutorial](https://www.youtube.com/watch?v=km9ZR6gVYe0)