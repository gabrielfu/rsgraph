import re
import io
from rich.console import Console
from rich.table import Table
from perfplot._main import PerfplotData


def format_time(dt: float, precision: int=3):
    """Formats time to unit. Taken from `timeit` module."""
    units = {"nsec": 1e-9, "usec": 1e-6, "msec": 1e-3, "sec": 1.0}
    scales = [(scale, unit) for unit, scale in units.items()]
    scales.sort(reverse=True)
    for scale, unit in scales:
        if dt >= scale:
            break

    return "%.*g %s" % (precision, dt / scale, unit)


def format_perf_data(perf_data: PerfplotData):
    """Formats PerfplotData with pretty time format."""
    table = Table(show_header=True)
    table.add_column("n")
    for label in perf_data.labels:
        table.add_column(label)

    for n, t in zip(perf_data.n_range, perf_data.timings_s.T):
        lst = [str(n)] + [format_time(tt) for tt in t]
        table.add_row(*lst)

    f = io.StringIO()
    console = Console(file=f)
    console.print(table)
    return f.getvalue()


def format_snake_case(string: str):
    # return string.lower().replace("-", "_").
    string = re.sub(r'(?<=[a-z])(?=[A-Z])|[^a-zA-Z]', ' ', string.replace("'", "")).strip().replace(' ', '_')
    return ''.join(string.lower())
