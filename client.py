import time
import requests

# server url
server_url = "http://0.0.0.0:5000/"

# create session
session = requests.Session()

# do some requests
for _ in range(10):
    # login to the judge server
    login_response = session.post(server_url + "api/giris",
                                  headers={"Content-Type": "application/json"},
                                  json={"kadi": "TestUcusu", "sifre": "ZurnaGonnaGetYouDown"})

    # get login data
    login_data = login_response.json()

    # get server time
    time_response = session.get(server_url + "api/sunucusaati")

    # parse server time
    time_data = time_response.json()

    # generate dummy telemetry data
    dummy_telemetry = {
        "takim_numarasi": 1,
        "IHA_enlem": 433.5,
        "IHA_boylam": 222.3,
        "IHA_irtifa": 222.3,
        "IHA_dikilme": 5,
        "IHA_yonelme": 256,
        "IHA_yatis": 0,
        "IHA_hiz": 223,
        "IHA_batarya": 20,
        "IHA_otonom": 0,
        "IHA_kilitlenme": 1,
        "Hedef_merkez_X": 315,
        "Hedef_merkez_Y": 220,
        "Hedef_genislik": 12,
        "Hedef_yukseklik": 46,
        "GPSSaati": {
            "saat": time_data["saat"],
            "dakika": time_data["dakika"],
            "saniye": time_data["saniye"],
            "milisaniye": time_data["milisaniye"]
        }
    }

    # send telemetry data to judge server
    telemetry_response = session.post(server_url + "api/telemetri_gonder",
                                      headers={"Content-Type": "application/json"},
                                      json=dummy_telemetry)

    # get telemetry data
    telemetry_data = telemetry_response.json()

    # generate dummy target lock data
    dummy_lock = {
        "kilitlenmeBaslangicZamani": {
            "saat": 19,
            "dakika": 1,
            "saniye": 23,
            "milisaniye": 507
        },
        "kilitlenmeBitisZamani": {
            "saat": 19,
            "dakika": 1,
            "saniye": 45,
            "milisaniye": 236
        },
        "otonom_kilitlenme": 0
    }

    # send target lock data to judge server
    target_response = session.post(server_url + "api/kilitlenme_bilgisi",
                                   headers={"Content-Type": "application/json"},
                                   json=dummy_lock)

    # get target data
    target_data = telemetry_response.json()

    # send logout request to judge server
    logout_response = session.get(server_url + "api/cikis")

    # get logout data
    logout_data = telemetry_response.json()

    # print the responses
    print("Login response: ", login_data)
    print("Time response: ", time_data)
    print("Telemetry response: ", telemetry_data)
    print("Target response: ", target_data)
    print("Logout response: ", logout_data)

    # cool down the requests
    time.sleep(1)
