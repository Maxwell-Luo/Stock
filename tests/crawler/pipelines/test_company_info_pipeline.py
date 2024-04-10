import pytest
from unittest.mock import patch, MagicMock
from crawler.pipelines.company_info_pipeline import CompanyInfoPipeline
from models.company_info import CompanyInfo

@pytest.fixture
def pipeline():

    with patch('crawler.pipelines.company_info_pipeline.Pg') as mock_pg:
        mock_pg.return_value.connect.return_value = MagicMock()
        pipeline = CompanyInfoPipeline()
        pipeline.industries_dict = {'電子': 1}
        pipeline.market_types_dict = {'上市': 1}
        pipeline.countries_dict = {'TW': 1}
        return pipeline


def test_process_item(pipeline):

    item = {
        'code': '2330',
        'name': '台積電',
        'market_type': '上市',
        'industry': '電子',
    }

    with patch.object(CompanyInfo, 'create') as mock_create:
        processed_item = pipeline.process_item(item, spider=MagicMock)
        mock_create.assert_called_once()
        assert processed_item == item
