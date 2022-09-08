# Batch Processing Pipeline with Dataflow
A pipeline to read text files from Cloud Storage to BigQuery with Dataflow.

1- Set environment on Shell\
2- Clone repo\
3- Create bucket\
4- Copy data to the bucket\
5- Create the BQ dataset\
bq mk ecommerce_behavor\
4- Build the Docker image\
docker build -t beam_python .\
5- Run a docker container with the new image\
docker run -it -e PROJECT=$PROJECT -v $(pwd)/pipeline:/pipeline beam_python\
6 - Set the variables\
export PROJECT=empyrean-surge-360315\
export INPUT_BUCKET=ecomerce-behavor-bucket\
export INPUT_PATH=data\
export FILES_LIST=report_names.txt\
export BQ_DATASET=ecommerce_behavor\
python pipeline.py \
--project=$PROJECT --region= \
--runner=DataflowRunner \
--staging_location=gs://$PROJECT/test \
--temp_location gs://$PROJECT/test \
--save_main_session \
--input-bucket=$INPUT_BUCKET \
--input-path=$INPUT_PATH \
--input-files-list=$FILES_LIST \
--bq-dataset=$BQ_DATASET \
--requirements_file=requirements.txt
7 - Enable access with the steps https://stackoverflow.com/questions/56302658/anonymous-caller-does-not-have-storage-objects-get