from datetime import datetime


class Logger:

    def __init__(self):
        cur = datetime.now()
        self.filename = f"{cur.day}-{cur.month}-{cur.hour}-{cur.minute}-{cur.second}.log"

    def _get_title(self, type: str, link: str, status: int):
        cur = datetime.now()
        title = f" {cur.day}:{cur.month}:{cur.hour}:{cur.minute}:{cur.second} {type.upper()} {link.lower()} - {status} "
        title = title.center(80, "=")

        return title

    def write(self, msg, type=None, link="/", status=200):
        title = self._get_title(type, link, status)

        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(title + "\n")
            f.write("INFO: " + msg + "\n")
