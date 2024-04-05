import pytest
from scrapy.http import HtmlResponse
from unittest.mock import patch
from crawler.spiders.company_info_spider import CompanyInfoSpider

@pytest.fixture
def response():
    return HtmlResponse(url="http://example.com", body= """
       <html>
          <body>
            <table>
              <tbody>
                <tr>
                  <td bgcolor="#FAFAD2" colspan="7">
                    <b> 股票 <b> </b></b>
                  </td>
                </tr>
                <tr>
                  <td bgcolor="#FAFAD2">2330　台積電</td>
                  <td bgcolor="#FAFAD2">TW0002330008</td>
                  <td bgcolor="#FAFAD2">1994/09/05</td>
                  <td bgcolor="#FAFAD2">上市</td>
                  <td bgcolor="#FAFAD2">半導體業</td>
                  <td bgcolor="#FAFAD2">ESVUFR</td>
                  <td bgcolor="#FAFAD2"></td>
                </tr>
              </tbody>
            </table>
          </body>
        </html>
    """.encode("utf-8"), encoding="utf-8")


def test_parse(response):

    with patch.object(CompanyInfoSpider, 'start_requests', return_value=None):
        spider = CompanyInfoSpider()

    result = next(spider.parse(response))

    assert result['code'] == "2330"
    assert result['name'] == "台積電"
    assert result['market_type'] == "上市"
    assert result['industry'] == "半導體業"

