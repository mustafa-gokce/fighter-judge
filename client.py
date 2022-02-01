import requests
import time

BASE_URL = "http://127.0.0.1:5000/"

session = requests.Session()

for _ in range(10):
    ret = session.post(BASE_URL + "api/giris",
                       json={"kadi": "estu", "sifre": "1234"},
                       headers={"Content-Type": "application/json"})

    ret = session.get(BASE_URL + "api/sunucusaati")
    server_time = ret.json()

    data = {
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
            "saat": server_time['saat'],
            "dakika": server_time['dakika'],
            "saniye": server_time['saniye'],
            "milisaniye": server_time['milisaniye']
        }
    }

    ret = session.post(BASE_URL + "api/telemetri_gonder",
                       json=data,
                       headers={"Content-Type": "application/json"})
    print(ret.json())

    data2 = {
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
    ret = session.post(BASE_URL + "api/kilitlenme_bilgisi",
                       json=data2,
                       headers={"Content-Type": "application/json"})

    ret = session.get(BASE_URL + "api/cikis")

    time.sleep(1)
