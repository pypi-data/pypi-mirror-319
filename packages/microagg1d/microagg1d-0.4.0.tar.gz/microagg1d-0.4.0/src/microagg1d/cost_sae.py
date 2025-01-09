import numpy as np
from numba import float64, int64, njit
from numba.experimental import jitclass

from microagg1d.common import calc_cumsum


@njit
def calc_sorted_median(arr, lb=0, ub=-1):
    """Returns the median from a sorted array"""
    if ub == -1:
        ub = len(arr)
    half = (ub - lb - 1) // 2 + lb
    if (ub - lb) % 2 == 0:
        return (arr[half] + arr[half + 1]) / 2
    else:
        return arr[half]


@njit
def calc_sae_from_cumsum(cumsum, i, j):
    center = (j - i) // 2
    return cumsum[j] - cumsum[j - center] - (cumsum[i + center] - cumsum[i])


@jitclass(
    [
        ("cumsum", float64[:]),
        ("k", int64),
        ("F_vals", float64[:]),
        ("SMALL_VAL", float64),
        ("LARGE_VAL", float64),
    ]
)
class AdaptedSAECostCalculator:
    """The standard calculator the microaggregation-adapted SSE cost"""

    def __init__(self, arr, k, F_vals):
        self.cumsum = calc_cumsum(arr)
        self.k = k
        self.F_vals = F_vals  # F_vals[i] is min_l w_li
        n = len(arr) - 1
        # the largest cluster cost is 2 * n * the maximum difference
        self.SMALL_VAL = (arr[-1] - arr[0]) * n
        self.LARGE_VAL = self.SMALL_VAL * (1 + n)

    def calc(self, i, j):
        """This function computes the w_{ij} values introduced"""
        if j <= i:
            return np.inf

        if not (j - i >= self.k):
            return self.LARGE_VAL + self.SMALL_VAL * i
        if not (j - i <= 2 * self.k - 1):
            return self.LARGE_VAL - self.SMALL_VAL * i
        return calc_sae_from_cumsum(self.cumsum, i, j) + self.F_vals[i]


@jitclass([("cumsum", float64[:])])
class SAECostCalculator:
    """The standard calculator the microaggregation-adapted SSE cost"""

    def __init__(self, arr):
        self.cumsum = calc_cumsum(arr)

    def calc(self, i, j):
        """This function computes the w_{ij} values introduced"""
        if j <= i:
            return np.inf
        return calc_sae_from_cumsum(self.cumsum, i, j)
