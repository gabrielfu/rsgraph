import timeit
from typing import Callable
   

def benchmark(func: Callable, name: str=None):
    timer = timeit.default_timer
    repeat = timeit.default_repeat
    units = {"nsec": 1e-9, "usec": 1e-6, "msec": 1e-3, "sec": 1.0}
    precision = 3

    t = timeit.Timer(stmt=func, timer=timer)
    number, _ = t.autorange()
    raw_timings = t.repeat(repeat, number)

    def format_time(dt):
        scales = [(scale, unit) for unit, scale in units.items()]
        scales.sort(reverse=True)
        for scale, unit in scales:
            if dt >= scale:
                break
        return "%.*g %s" % (precision, dt / scale, unit)

    timings = [dt / number for dt in raw_timings]
    best = min(timings)
    print("%s: %d loop%s, best of %d: %s per loop"
          % (name, number, 's' if number != 1 else '',
             repeat, format_time(best)))
