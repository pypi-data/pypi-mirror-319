import warnings
from abc import ABC, abstractmethod
from numbers import Integral, Real

import numpy as np
import scipy.sparse as sp

class BaseMetricConfig:
    """
    base class for metric config
    """
    def __init__(self):
        self.Metrics_Breakdown = {}
        self.Metric_Query = {}
        self.Metric_Expression = {}
        self.Titan_Query_Dimension_Template = {}
        self.Titan_Query_Dimension_Value_Template = {}

class BaseMetricNode:
    """
    base class for metric config tree
    """
    def __init__(self):
        self.metric_name = ""
        self.value = None
        self.formula = []
        self.op_type = None
        self.coefficient = []  # the length should be the same as the formula