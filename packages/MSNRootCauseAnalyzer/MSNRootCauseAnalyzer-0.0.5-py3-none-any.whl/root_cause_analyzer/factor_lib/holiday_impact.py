import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from holidays import country_holidays


class HolidayImpactAnalyzer:
    def __init__(self, metric=""):
        self.metric = metric
