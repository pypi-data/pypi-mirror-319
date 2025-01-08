import numpy as np
import pandas as pd


class ModelOutput:
    def __init__(
            self,
            timestamp: np.ndarray,
            q_obs: np.ndarray,
            q_sim: np.ndarray,
            u_soil: np.ndarray,
            s_snow: np.ndarray,
            q_snow: np.ndarray,
            q_inter: np.ndarray,
            e_eal: np.ndarray,
            q_of: np.ndarray,
            q_g: np.ndarray,
            q_bf: np.ndarray,
            l_soil: np.ndarray,
    ):
        self.__Timestamp = timestamp
        self.__Q_obs = q_obs
        self.__Q_sim = q_sim
        self.__U_soil = u_soil
        self.__S_snow = s_snow
        self.__Q_snow = q_snow
        self.__Q_inter = q_inter
        self.__E_eal = e_eal
        self.__Q_of = q_of
        self.__Q_g = q_g
        self.__Q_bf = q_bf
        self.__L_soil = l_soil

    def get_timestamp(self) -> np.ndarray:
        return self.__Timestamp

    def get_q_obs(self) -> np.ndarray:
        return self.__Q_obs

    def get_q_sim(self) -> np.ndarray:
        return self.__Q_sim

    def get_u_soil(self) -> np.ndarray:
        return self.__U_soil

    def get_s_snow(self) -> np.ndarray:
        return self.__S_snow

    def get_q_snow(self) -> np.ndarray:
        return self.__Q_snow

    def get_q_inter(self) -> np.ndarray:
        return self.__Q_inter

    def get_e_eal(self) -> np.ndarray:
        return self.__E_eal

    def get_q_of(self) -> np.ndarray:
        return self.__Q_of

    def get_q_g(self) -> np.ndarray:
        return self.__Q_g

    def get_q_bf(self) -> np.ndarray:
        return self.__Q_bf

    def get_l_soil(self) -> np.ndarray:
        return self.__L_soil

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(
            {
                "Timestamp": self.__Timestamp,
                "Q_obs": self.__Q_obs,
                "Q_sim": self.__Q_sim,
                "U_soil": self.__U_soil,
                "S_snow": self.__S_snow,
                "Q_snow": self.__Q_snow,
                "Q_inter": self.__Q_inter,
                "E_eal": self.__E_eal,
                "Q_of": self.__Q_of,
                "Q_g": self.__Q_g,
                "Q_bf": self.__Q_bf,
                "L_soil": self.__L_soil
            }
        )
