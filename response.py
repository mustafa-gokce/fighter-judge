import datetime


class Response:
    """
        Server response
    """

    def __init__(self):
        """
            Initialize response
        """

        # this will hold the telemetry related data
        self.args = dict()

    def get_delay(self):
        """
            Calculate delay between received GPS time and Server time
        """

        # get server time
        server_time = datetime.datetime.now()
        server_time_hour = server_time.hour
        server_time_minute = server_time.minute
        server_time_second = server_time.second
        server_time_millisecond = round(server_time.microsecond / 1000)

        # get team time
        team_hour = int(self.args["GPSSaati"]["saat"])
        team_minute = int(self.args["GPSSaati"]["dakika"])
        team_second = int(self.args["GPSSaati"]["saniye"])
        team_millisecond = int(self.args["GPSSaati"]["milisaniye"])
        team_time = datetime.datetime(year=server_time.year,
                                      month=server_time.month,
                                      day=server_time.day,
                                      hour=team_hour,
                                      minute=team_minute,
                                      second=team_second,
                                      microsecond=team_millisecond * 1000)

        # calculate team delay in millisecond
        team_delay_millisecond = (server_time - team_time).total_seconds() * 1000

        # return to team delay
        return team_delay_millisecond

    def set_args(self, args):
        """
            Set response arguments
        """

        # set response arguments
        self.args = args

    def get_data(self):
        """
            Get response data, more foe data can be added
        """

        # get server time
        server_time = datetime.datetime.now()

        # build telemetry data
        telemetry_data = {
            "sistemSaati": {
                "saat": server_time.hour,
                "dakika": server_time.minute,
                "saniye": server_time.second,
                "milisaniye": int(server_time.microsecond / 1000)
            },
            "konumBilgileri": [
                {
                    "takim_numarasi": self.args["takim_numarasi"],
                    "iha_enlem": self.args["IHA_enlem"],
                    "iha_boylam": self.args["IHA_boylam"],
                    "iha_irtifa": self.args["IHA_irtifa"],
                    "iha_dikilme": self.args["IHA_dikilme"],
                    "iha_yonelme": self.args["IHA_yonelme"],
                    "iha_yatis": self.args["IHA_yatis"],
                    "zaman_farki": self.get_delay()
                },
                {
                    "takim_numarasi": 55,
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

        # return to telemetry data
        return telemetry_data
