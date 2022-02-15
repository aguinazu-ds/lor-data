from ratelimit import limits, RateLimitException, sleep_and_retry
import time

@sleep_and_retry
@limits(calls=1, period=1.25)
@limits(calls=30, period=60)
def test():
    print(time.strftime("%H:%M:%S"))

for i in range(1000):
    print(i)
    test()