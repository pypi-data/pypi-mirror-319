from typing import List
from datetime import datetime

import pandas as pd
from hydutils.hydrology_constants import TIMESTAMP, TEMPERATURE, PRECIPITATION, EVAPOTRANSPIRATION, DISCHARGE


class Dataset:
    def __init__(
            self,
            timestamp: List[datetime],
            temperature: List[float],
            precipitation: List[float],
            evapotranspiration: List[float],
            discharge: List[float],
    ):
        if not (len(timestamp) == len(temperature) == len(precipitation) == len(evapotranspiration) == len(discharge)):
            raise ValueError("All input lists must have the same length.")

        self.__timestamp = timestamp
        self.__temperature = temperature
        self.__precipitation = precipitation
        self.__evapotranspiration = evapotranspiration
        self.__discharge = discharge

    def get_timestamp(self):
        return self.__timestamp

    def get_temperature(self):
        return self.__temperature

    def get_precipitation(self):
        return self.__precipitation

    def get_evapotranspiration(self):
        return self.__evapotranspiration

    def get_discharge(self):
        return self.__discharge

    def to_dataframe(self):
        dataset_dict = {
            TIMESTAMP: self.__timestamp,
            TEMPERATURE: self.__temperature,
            PRECIPITATION: self.__precipitation,
            EVAPOTRANSPIRATION: self.__evapotranspiration,
            DISCHARGE: self.__discharge,
        }

        df = pd.DataFrame(dataset_dict)
        df[TIMESTAMP] = pd.to_datetime(df[TIMESTAMP])
        return df
