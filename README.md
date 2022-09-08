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