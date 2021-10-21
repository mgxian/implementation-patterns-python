import time

from domain.service.article import Clock


class SystemClock(Clock):
    def now(self) -> float:
        return time.time()
