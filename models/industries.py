from .base_model import BaseModel


class Industries(BaseModel):

    table_name = "industries"

    def __init__(self, db_connection):
        super().__init__(db_connection)
        self.id = None
        self.industry = None

    def create_table(self):

        definition = """
            id SERIAL PRIMARY KEY,
            industry VARCHAR(20) NOT NULL
        """

        super().table(definition)

    def initial(self):
        industries = ['農業科技業', '觀光餐旅', '食品工業', '電子零組件業', '生技醫療業', '電腦及週邊設備業', '電機機械',
                      '其他業', '運動休閒', '化學工業', '其他電子業', '鋼鐵工業', '電器電纜', '建材營造業', '數位雲端',
                      '航運業', '居家生活', '文化創意業', '光電業', '綠能環保', '通信網路業', '半導體業', '資訊服務業',
                      '電子通路業', '塑膠工業', '紡織纖維', '金融保險業', '油電燃氣業', '水泥工業', '汽車工業', '玻璃陶瓷',
                      '造紙工業', '橡膠工業', '貿易百貨業']

        for industry in industries:

            self.set_data(industry=industry)
            self.create()
