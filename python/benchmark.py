import timeit
from typing import Callable
   

def benchmark(func: Callable, name: str=None):
    timer = timeit.default_timer
    stmt = func
    number = 0 # auto-determine
    setup = []
    repeat = timeit.default_repeat
    verbose = 0
    time_unit = None
    units = {"nsec": 1e-9, "usec": 1e-6, "msec": 1e-3, "sec": 1.0}
    precision = 3
    setup = "pass"

    t = timeit.Timer(stmt, setup, timer)
    if number == 0:
        # determine number so that 0.2 <= total time < 2.0
        callback = None
        if verbose:
            def callback(number, time_taken):
                msg = "{num} loop{s} -> {secs:.{prec}g} secs"
                plural = (number != 1)
                print(msg.format(num=number, s='s' if plural else '',
                                  secs=time_taken, prec=precision))
        try:
            number, _ = t.autorange(callback)
        except:
            t.print_exc()
            return 1

        if verbose:
            print()

    try:
        raw_timings = t.repeat(repeat, number)
    except:
        t.print_exc()
        return 1

    def format_time(dt):
        unit = time_unit

        if unit is not None:
            scale = units[unit]
        else:
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

    best = min(timings)
    worst = max(timings)
    if worst >= best * 4:
        import warnings
        warnings.warn_explicit("The test results are likely unreliable. "
                               "The worst time (%s) was more than four times "
                               "slower than the best time (%s)."
                               % (format_time(worst), format_time(best)),
                               UserWarning, '', 0)
    return None

