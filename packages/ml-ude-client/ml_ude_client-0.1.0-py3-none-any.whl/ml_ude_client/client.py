from datetime import datetime
import json
from typing import List

import botocore
import boto3
import pandas as pd

from ml_ude_client.memory import Memory

lambda_name = "mklosi-ude-lambda" # &&&

# &&& do we need all of this?
ude_service_bucket = "ai-s3-dev-sandbox"
service_ver = 1
dt_format_measurement = '%Y-%m-%d_%H-%M-%S'
dt_format_cache = '%Y-%m-%d_%H-%M-%S-%f'
pn_str = "plate_names"
sn_str = "screen_names"
out_fmts_str = "output_formats"
supported_out_formats = ["csv", "parquet"]
local_output_dir = "/tmp/sima_data"


def input_fail_fast(event):
    # Fail-fast on bad input.
    if pn_str not in event and sn_str not in event:
        raise ValueError(f"Must provide either '{pn_str}' or '{sn_str}'.")
    if pn_str in event and sn_str in event:
        raise ValueError(f"Must provide either '{pn_str}' or '{sn_str}', but not both.")
    if out_fmts_str not in event:
        raise ValueError("Must provide `output_formats` param.")
    if not set(event[out_fmts_str]).issubset(set(supported_out_formats)):
        raise ValueError(
            f"Only output format supported are '{set(supported_out_formats)}'. Given: {set(event[out_fmts_str])}"
        )


class Client:

    def __init__(self):
        # noinspection PyUnresolvedReferences
        config = botocore.config.Config(
            retries={'max_attempts': 0},
            read_timeout=900,  # Same timeout as that of the lambda, 15min (max).
            connect_timeout=60,
        )
        self.lambda_client = boto3.client('lambda', config=config)

    def get_measurements_df(
        self,
        screen_names: List[str] = None,
        plate_names: List[str] = None,
    ) -> pd.DataFrame:
        """
        &&& input is event in the lambda.
        :param output_formats:
        :type output_formats:
        :param plate_names:
        :type plate_names:
        :param screen_names:
        :type screen_names:
        :param input_:
        :type input_:
        :return:
        :rtype:
        """

        event = {"output_formats": ["parquet"]}
        if screen_names is not None:
            event = {**event, "screen_names": screen_names}
        if plate_names is not None:
            event = {**event, "plate_names": plate_names}

        input_fail_fast(event)

        ## &&&

        response = self.lambda_client.invoke(
            FunctionName=lambda_name,
            # InvocationType="Event",  # Asynchronous.
            InvocationType='RequestResponse',
            Payload=json.dumps(event),
        )
        response_dict = json.loads(response['Payload'].read().decode('utf-8'))
        parquet_s3_path = response_dict["parquet_s3_path"]

        # df = pd.read_parquet(parquet_s3_path)
        # parquet_s3_path = "testing/temp_df.parquet"
        # df.to_parquet(parquet_s3_path, engine="pyarrow")

        # parquet_s3_path = "testing/temp_df.parquet"

        df = pd.read_parquet(parquet_s3_path)
        return df

    def download_measurements_csv(
        self,
        local_csv_path: str,
        screen_names: List[str] = None,
        plate_names: List[str] = None,
    ) -> str:
        """
        &&& input is event in the lambda.
        :param local_csv_path:
        :type local_csv_path:
        :param output_formats:
        :type output_formats:
        :param plate_names:
        :type plate_names:
        :param screen_names:
        :type screen_names:
        :param input_:
        :type input_:
        :return:
        :rtype:
        """

        mem = Memory()
        dt_start = datetime.now()

        df = self.get_measurements_df(screen_names, plate_names)
        print(f"Got measurement df with shape: {df.shape}")
        df.to_csv(local_csv_path, index=False)

        mem.log_memory(print, "mem")
        print(f"Total runtime: {datetime.now() - dt_start}")

        return local_csv_path
