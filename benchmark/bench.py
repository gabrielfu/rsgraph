import perfplot
from typing import Dict, Callable, Optional
from formats import format_perf_data, format_snake_case


class BenchMeta(type):
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        # add registered kernels to class kernel registry
        cls._kernel_registry = {}
        for func_name in dir(cls):
            func = getattr(cls, func_name)
            if hasattr(func, "_kernel_label"):
                cls._kernel_registry[getattr(func, "_kernel_label")] = func
        return cls


class Bench(metaclass=BenchMeta):
    name: str
    _kernel_registry: Dict

    @classmethod
    def run_benchmark(cls, min_n_pow2: int=2, max_n_pow2: int=10):
        """
        Run benchmark, print result and save image

        Args:
            min_n_pow2 (int): benchmarking from n = 2 ** min_n_pow2
            max_n_pow2 (int): benchmarking until n = 2 ** max_n_pow2
        """
        print(f"Benchmarking: {cls.name}")
        if len(cls._kernel_registry) == 0:
            raise ValueError("No kernel registered")

        labels, kernels = list(zip(*cls._kernel_registry.items()))
        perf_data = perfplot.bench(
            setup=cls.setup,
            kernels=kernels,
            labels=labels,
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
    def setup(n: int):
        raise NotImplementedError


def register_kernel(label: Optional[str]=None):
    def decorator(func: Callable):
        setattr(func, "_kernel_label", label or func.__name__)
        return func
    return decorator
