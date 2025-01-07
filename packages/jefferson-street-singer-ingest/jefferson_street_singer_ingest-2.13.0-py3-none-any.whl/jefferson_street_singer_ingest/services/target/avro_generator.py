import logging
import fastavro

from fastavro import writer


def build_avro_schema(column_names, name: str) -> None:
    # TODO check for jefferson_street_ingest_datetime and jefferson_street_stream_name

    """Method to zip field names into Avro schema format."""
    logging.debug(f"Table name is set to {name}")
    avro_dict = {
        "namespace": "jeffersons_street_technologies",
        "type": "record",
        "name": "source",
        "fields": [
            {"name": column_name, "type": "string", "default": ""}
            for column_name in column_names
        ],
    }
    return fastavro.parse_schema(avro_dict)


def build_avro_file(file_name, avro_schemas, processed_responses):
    if avro_schemas:
        with open(f"/mnt/ephemeral/{file_name}.avro", "a+b") as out:
            writer(out, avro_schemas, processed_responses)
