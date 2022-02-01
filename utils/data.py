from datetime import datetime


class Response:

    def __init__(self):
        self.args = dict()

    """
        * Calculate delay between received GPS time and Server time
    """
    def get_delay(self):
        current = datetime.now()
        c_hour = current.hour
        c_min = current.minute
        c_sec = current.second
        c_mili = round(current.microsecond / 1000)

        t_hour = int(self.args['GPSSaati']['saat'])
        t_min = int(self.args['GPSSaati']['dakika'])
        t_sec = int(self.args['GPSSaati']['saniye'])
        t_mili = int(self.args['GPSSaati']['milisaniye'])

        delay_mili = (c_sec * 1000 + c_mili) - (t_sec * 1000 + t_mili)

        return delay_mili

    def setArgs(self, args):
        self.args = args

    """
        * Get response data, more teams info can be added
        * First one is our team
    """
    def getData(self):
        current = datetime.now()
        data = {
            "sistemSaati": {
                "saat": current.hour,
                "dakika": current.minute,
                "saniye": current.second,
                "milisaniye": round(current.microsecond / 1000)
            },
            "konumBilgileri": [
                {
                    "takim_numarasi": self.args['takim_numarasi'],
                    "iha_enlem": self.args['IHA_enlem'],
                    "iha_boylam": self.args['IHA_boylam'],
                    "iha_irtifa": self.args['IHA_irtifa'],
                    "iha_dikilme": self.args['IHA_dikilme'],
                    "iha_yonelme": self.args['IHA_yonelme'],
                    "iha_yatis": self.args['IHA_yatis'],
                    "zaman_farki": self.get_delay()
                },
                {
                    "takim_numarasi": 2,
                    "iha_enlem": 0,
                    "iha_boylam": 0,
                    "iha_irtifa": 0,
                    "iha_dikilme": 0,
                    "iha_yonelme": 0,
                    "iha_yatis": 0,
                    "zaman_farki": 0
                },
            ]
        }

        return data
