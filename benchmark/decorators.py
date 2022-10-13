import perfplot
from typing import Dict, Callable
from formats import format_perf_data, format_snake_case


class Bench:
    name: str
    _registry: Dict

    @staticmethod
    def bench(cls):
        # add functions to registry
        cls._registry = {}
        for funcname in dir(cls):
            func = getattr(cls, funcname)
            if hasattr(func, "_bench_label"):
                cls._registry[getattr(func, "_bench_label")] = func

        return cls

    @staticmethod
    def register(label: str=None):
        def decorator(func: Callable):
            setattr(func, "_bench_label", label or func.__name__)
            return func
        return decorator

    @classmethod
    def run_benchmark(cls, min_n_pow2: int = 2, max_n_pow2: int = 10):
        """
        Run benchmark, print result and save image

        Args:
            min_n_pow2 (int): benchmarking from n = 2 ** min_n_pow2
            max_n_pow2 (int): benchmarking until n = 2 ** max_n_pow2
        """
        print(f"Benchmarking: {cls.name}")
        perf_data = perfplot.bench(
            setup=cls.setup,
            kernels=list(cls._registry.values()),
            labels=list(cls._registry.keys()),
            n_range=[2 ** k for k in range(min_n_pow2, max_n_pow2)],
            xlabel="graph size",
            equality_check=None,
        )
        print(format_perf_data(perf_data))
        perf_data.title = cls.name
        perf_data.save(
            filename=f"./images/perf_{format_snake_case(cls.name)}.png",
            logx=True,
            logy=True,
            transparent=False,
            bbox_inches="tight",
        )

    @staticmethod
    def setup(n):
        raise NotImplementedError
