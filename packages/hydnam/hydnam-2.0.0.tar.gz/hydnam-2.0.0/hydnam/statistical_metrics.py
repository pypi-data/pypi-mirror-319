class StatisticalMetrics:
    def __init__(
            self,
            mse: float = -9999,
            rmse: float = -9999,
            nse: float = -9999,
            r2: float = -9999,
            pbias: float = -9999,
            fbias: float = -9999,
    ):
        self.__mse = mse
        self.__rmse = rmse
        self.__nse = nse
        self.__r2 = r2
        self.__pbias = pbias
        self.__fbias = fbias

    def get_mse(self) -> float:
        return self.__mse

    def get_rmse(self) -> float:
        return self.__rmse

    def get_nse(self) -> float:
        return self.__nse

    def get_r2(self) -> float:
        return self.__r2

    def get_pbias(self) -> float:
        return self.__pbias

    def get_fbias(self) -> float:
        return self.__fbias
