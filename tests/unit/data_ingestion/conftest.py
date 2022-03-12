from copy import deepcopy

import pytest

from tests.resources.csv_content import CSV_CONTENT


@pytest.fixture()
def read_csv_from_s3(mocker):

    csv_content = deepcopy(CSV_CONTENT)
    mocker.patch(
        "src.data_ingestion.handler.read_csv_from_s3", return_value=csv_content
    )
