import time
import requests
from datetime import datetime

# cooldown should be between 500 and 1000 ms to get point.
COOLDOWN = 0.5

# get current time as dict
def get_time() -> dict:
    c_time = datetime.now()

    return {"saat": c_time.hour,
           "dakika": c_time.minute,
           "saniye": c_time.second,
           "milisaniye": round(c_time.microsecond / 1000)}



# server url
server_url = "http://127.0.0.1:5000/"

# create sessions
session = requests.Session()

# login to the judge server
login_response = session.post(server_url + "api/giris",
                              headers={"Content-Type": "application/json"},
                              json={"kadi": "TestUcusu", "sifre": "ZurnaGonnaGetYouDown"})

# get login data
login_data = login_response.json()

print("Login response: ", login_data)

# do some requests
for _ in range(10):

    # get server time
    time_response = session.get(server_url + "api/sunucusaati")

    # parse server time
    time_data = time_response.json()

    print("Time response: ", time_data)

    # current time
    c_time = get_time()

    # generate dummy telemetry data
    dummy_telemetry = {
        "takim_numarasi": 26,
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
            "saat": c_time["saat"],
            "dakika": c_time["dakika"],
            "saniye": c_time["saniye"],
            "milisaniye": c_time["milisaniye"]
        }
    }

    # send telemetry data to judge server
    telemetry_response = session.post(server_url + "api/telemetri_gonder",
                                      headers={"Content-Type": "application/json"},
                                      json=dummy_telemetry)

    # get telemetry data
    telemetry_data = telemetry_response.json()

    print("Telemetry response: ", telemetry_data)

    # cooldown
    time.sleep(COOLDOWN)

    # current time
    c_time = get_time()

    dummy_telemetry = {
        "takim_numarasi": 26,
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
            "saat": c_time["saat"],
            "dakika": c_time["dakika"],
            "saniye": c_time["saniye"],
            "milisaniye": c_time["milisaniye"]
        }
    }

    # send telemetry data to judge server
    telemetry_response = session.post(server_url + "api/telemetri_gonder",
                                      headers={"Content-Type": "application/json"},
                                      json=dummy_telemetry)

    # get telemetry data
    telemetry_data = telemetry_response.json()

    print("Telemetry response: ", telemetry_data)

    # cooldown
    time.sleep(COOLDOWN)

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

    print("Target response: ", target_data)

    # get score table
    score_response = session.get(server_url + "api/puan_tablosu")

    # score table as json
    scores = score_response.json()

    print("Score response: ", scores)

    # get delay table
    delay_response = session.get(server_url + "api/gecikme_tablosu")

    # delay table as json
    delays = delay_response.json()

    print("Delay response: ", delays)

# send logout request to judge server
logout_response = session.get(server_url + "api/cikis")

# get logout data
logout_data = logout_response.json()

print("Logout response: ", logout_data)


