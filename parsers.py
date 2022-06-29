import flask_restful.reqparse

# judge server login request parser
login_parser = flask_restful.reqparse.RequestParser()
login_parser.add_argument("kadi", type=str, required=True)
login_parser.add_argument("sifre", type=str, required=True)

# judge server telemetry send request parser
telemetry_parser = flask_restful.reqparse.RequestParser()
telemetry_parser.add_argument("takim_numarasi", type=int, required=True)
telemetry_parser.add_argument("IHA_enlem", type=float, required=True)
telemetry_parser.add_argument("IHA_boylam", type=float, required=True)
telemetry_parser.add_argument("IHA_irtifa", type=float, required=True)
telemetry_parser.add_argument("IHA_dikilme", type=float, required=True)
telemetry_parser.add_argument("IHA_yonelme", type=float, required=True)
telemetry_parser.add_argument("IHA_yatis", type=float, required=True)
telemetry_parser.add_argument("IHA_hiz", type=float, required=True)
telemetry_parser.add_argument("IHA_batarya", type=float, required=True)
telemetry_parser.add_argument("IHA_otonom", type=int, required=True)
telemetry_parser.add_argument("IHA_kilitlenme", type=int, required=True)
telemetry_parser.add_argument("Hedef_merkez_X", type=int, required=True)
telemetry_parser.add_argument("Hedef_merkez_Y", type=int, required=True)
telemetry_parser.add_argument("Hedef_genislik", type=int, required=True)
telemetry_parser.add_argument("Hedef_yukseklik", type=int, required=True)
telemetry_parser.add_argument("GPSSaati", type=dict, required=True)

# judge server target lock request parser
lock_on_parser = flask_restful.reqparse.RequestParser()
lock_on_parser.add_argument("kilitlenmeBaslangicZamani", type=dict, required=True)
lock_on_parser.add_argument("kilitlenmeBitisZamani", type=dict, required=True)
lock_on_parser.add_argument("otonom_kilitlenme", type=int, required=True)
