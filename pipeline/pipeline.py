# Copyright 2018 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Dataflow pipeline that reads 1-n files, transforms their content, and writes
it to BigQuery tables using schema information stored in DataStore.

To run this script, you will need Python packages listed in requirements.txt.

You can easily install them with virtualenv and pip by running these commands:

    virtualenv env
    source ./env/bin/activate
    pip install -r requirements.txt

To get documentation on the script options run:
    python dataflow_python_examples/data_ingestion_configurable.py --help
"""

import argparse
import json
import logging
import os
import re
from collections import OrderedDict

import apache_beam as beam
from apache_beam.io.gcp.internal.clients.bigquery import (TableFieldSchema,
                                                          TableSchema)
from google.api_core.exceptions import InvalidArgument
from google.auth.exceptions import GoogleAuthError
from google.cloud import datastore

# TODO cambiar metodo para usarlo en cualquier schema


def parse_method(string_input, schema_json):
    """This method translates a single line of comma separated values to a
    dictionary which can be loaded into BigQuery.

    Args:
        string_input: A comma separated list of values in the form of
            state_abbreviation,gender,year,name,count_of_babies,dataset_created_date
            Example string_input: KS,F,1923,Dorothy,654,11/28/2016

    Returns:
        A dict mapping BigQuery column names as keys to the corresponding value
        parsed from string_input. In this example, the data is not transformed, and
        remains in the same format as the CSV.
        example output:
        {
            'state': 'KS',
            'gender': 'F',
            'year': '1923',
            'name': 'Dorothy',
            'number': '654',
            'created_date': '11/28/2016'
        }
     """
    # Strip out carriage return, newline and quote characters.
    values = re.split(",", re.sub('\r\n', '', re.sub('"', '',
                                                     string_input)))

    field_names = tuple(field['name'] for field in schema_json['fields'])

    row = dict(
        zip(field_names,
            values))
    return row


class InjectTimestamp(beam.DoFn):

    def process(self, element):
        import time
        element['_RAWTIMESTAMP'] = int(time.mktime(time.gmtime()))
        return [element]

# TODO Definir método para obtener esquema


def run(argv=None):
    """The main function which creates the pipeline and runs it"""

    parser = argparse.ArgumentParser()
    parser.add_argument('--input-bucket',
                        dest='input_bucket',
                        required=True,
                        default='data-daimlr',
                        help='GS bucket_name where the input files are present')

    parser.add_argument(
        '--input-path',
        dest='input_path',
        required=False,
        help='GS folder name, if the input files are inside a bucket folder')

    # File name with the list of directories of data (one for each table)
    parser.add_argument(
        '--input-files-list',
        dest='input_files_list',
        required=True,
        help='File name of the files list')

    # parser.add_argument(
    #     '--input-files',
    #     dest='input_files',
    #     required=True,
    #     help='Comma delimited names of all input files to be imported')

    parser.add_argument('--bq-dataset',
                        dest='bq_dataset',
                        required=True,
                        default='rawdata',
                        help='Output BQ dataset to write the results to')

    # Parse arguments from the command line
    known_args, pipeline_args = parser.parse_known_args(argv)

    # Initiate the pipeline using the pipeline arguments
    logging.info('START - Pipeline')
    p = beam.Pipeline(argv=pipeline_args)

    # Define the origin path
    base_path = os.path.join(
        known_args.input_bucket,
        known_args.input_path if known_args.input_path else ""
    )

    # Get the list of files
    input_files = open(os.path.join(base_path, known_args.input_files_list), 'r').readlines()

    # Cada nombre de archivo en realidad es una carpeta
    for input_file in input_files:
        logging.info('START - Preparing file %s' % input_file)

        # Get the data file path
        data_path = os.path.join(
            base_path,
            input_file,
            'data.csv'
        )

        # Get the schema file path
        schema_path = os.path.join(
            base_path,
            input_file,
            'schema.json'
        )

        table_name = os.path.splitext(input_file)[0].split('_')[0]

        # TODO Change to use the JSON file instead the Datastore record
        logging.info('Getting the schema from file')

        # Read the schema from a json file
        schema_json = json.load(open(schema_path))

        logging.info('GS path being read from: %s' % data_path)

        (p
         # Read the file. This is the source of the pipeline. All further
         # processing starts with lines read from the file. We use the input
         # argument from the command line. We also skip the first line which is a
         # header row.
         | 'Read from a File' >> beam.io.ReadFromText(data_path,
                                                      skip_header_lines=1)

         # This stage of the pipeline translates from a CSV file single row
         # input as a string, to a dictionary object consumable by BigQuery.
         # It refers to a function we have written. This function will
         # be run in parallel on different workers using input from the
         # previous stage of the pipeline.
         | 'String To BigQuery Row' >>
         beam.Map(lambda s: parse_method(s)) |

         # This stage of the pipeline translates from a CSV file single row
         # input as a string, to a dictionary object consumable by BigQuery.
         # It refers to a function we have written. This function will
         # be run in parallel on different workers using input from the
         # previous stage of the pipeline.
         'Inject Timestamp - ' + input_file >> beam.ParDo(InjectTimestamp()) |
         'Write to BigQuery - ' + input_file >> beam.io.Write(
                    beam.io.BigQuerySink(
                        # The table name passed in from the command line
                        known_args.bq_dataset + '.' + table_name,
                        # Schema of the table
                        schema=schema_json,
                        # Creates the table in BigQuery if it does not exist
                        create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                        # Data will be appended to the table
                        write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND)))

        logging.info('END - Preparing file %s' % input_file)

    p.run().wait_until_finish()
    logging.info('END - Pipeline')


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()