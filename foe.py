import time
import math

import requests

# server url
server_url = "http://127.0.0.1:5000/"

# team definitions
teams = [{"id": 10,
          "name": "DummyTeam1",
          "password": "AdimCaferBoyumBirOn",
          "session_get": requests.Session(),
          "session_put": requests.Session(),
          "telemetry": 8020},
         {"id": 41,
          "name": "DummyTeam2",
          "password": "YouHaveNoIdeaHowHighCanIFly",
          "session_get": requests.Session(),
          "session_put": requests.Session(),
          "telemetry": 8030},
         {"id": 58,
          "name": "DummyTeam3",
          "password": "PleaseLeaveMeAlone",
          "session_get": requests.Session(),
          "session_put": requests.Session(),
          "telemetry": 8040},
         {"id": 117,
          "name": "DummyTeam4",
          "password": "MyEnemiesAreAfterMe",
          "session_get": requests.Session(),
          "session_put": requests.Session(),
          "telemetry": 8050}]

# login to judge server
for team in teams:
    team["session_put"].post(url="http://127.0.0.1:5000/api/giris",
                             headers={"Content-Type": "application/json"},
                             json={"kadi": team["name"], "sifre": team["password"]})

# do below always
while True:

    # for each team
    for team in teams:
        # get telemetry data
        telemetry_data_get = team["session_get"].get(url=f"http://127.0.0.1:{team['telemetry']}/get/all").json()

        # parse telemetry data
        telemetry_data_put = {
            "takim_numarasi": team["id"],
            "IHA_enlem": telemetry_data_get["GLOBAL_POSITION_INT"]["lat"] * 1e-7,
            "IHA_boylam": telemetry_data_get["GLOBAL_POSITION_INT"]["lon"] * 1e-7,
            "IHA_irtifa": telemetry_data_get["GLOBAL_POSITION_INT"]["relative_alt"] * 1e-3,
            "IHA_dikilme": math.degrees(telemetry_data_get["ATTITUDE"]["pitch"]),
            "IHA_yonelme": telemetry_data_get["GLOBAL_POSITION_INT"]["hdg"] * 1e-2,
            "IHA_yatis": math.degrees(telemetry_data_get["ATTITUDE"]["roll"]),
            "IHA_hiz": telemetry_data_get["VFR_HUD"]["groundspeed"],
            "IHA_batarya": telemetry_data_get["SYS_STATUS"]["battery_remaining"],
            "IHA_otonom": 0,
            "IHA_kilitlenme": 0,
            "Hedef_merkez_X": 0,
            "Hedef_merkez_Y": 0,
            "Hedef_genislik": 0,
            "Hedef_yukseklik": 0,
            "GPSSaati": {
                "saat": 0,
                "dakika": 0,
                "saniye": 0,
                "milisaniye": 0
            }
        }

        team["session_put"].post("http://127.0.0.1:5000/api/telemetri_gonder",
                                 headers={"Content-Type": "application/json"},
                                 json=telemetry_data_put)

    # cool down the process
    time.sleep(1)
