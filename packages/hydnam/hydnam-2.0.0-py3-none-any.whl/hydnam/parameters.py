class Parameters:
    bounds = (
        (0.01, 50),  # umax
        (0.01, 1000),  # lmax
        (0.01, 1),  # cqof
        (200, 1000),  # ckif
        (10, 50),  # ck12
        (0, 1),  # tof
        (0, 1),  # tif
        (0, 1),  # tg
        (500, 5000),  # ckbf
        (0, 4),  # csnow
        (-2, 4),  # snowtemp
        (0, 1),  # qofmin
        (0, 1),  # beta
        (10, 100),  # pmm
        (0, 1)  # carea
    )

    def __init__(
            self,
            umax: float = 0.01,
            lmax: float = 0.01,
            cqof: float = 0.01,
            ckif: float = 200.0,
            ck12: float = 10.0,
            tof: float = 0.0,
            tif: float = 0.0,
            tg: float = 0.0,
            ckbf: float = 500.0,
            csnow: float = 0.0,
            snowtemp: float = 0.0,
            qofmin: float = 0.4,
            beta: float = 0.1,
            pmm: float = 10.0,
            carea: float = 0.0,
    ):
        self.__umax = umax
        self.__lmax = lmax
        self.__cqof = cqof
        self.__ckif = ckif
        self.__ck12 = ck12
        self.__tof = tof
        self.__tif = tif
        self.__tg = tg
        self.__ckbf = ckbf
        self.__csnow = csnow
        self.__snowtemp = snowtemp

        self.__qofmin = qofmin
        self.__beta = beta
        self.__pmm = pmm
        self.__carea = carea

    def get_umax(self) -> float:
        return self.__umax

    def get_lmax(self) -> float:
        return self.__lmax

    def get_cqof(self) -> float:
        return self.__cqof

    def get_ckif(self) -> float:
        return self.__ckif

    def get_ck12(self) -> float:
        return self.__ck12

    def get_tof(self) -> float:
        return self.__tof

    def get_tif(self) -> float:
        return self.__tif

    def get_tg(self) -> float:
        return self.__tg

    def get_ckbf(self) -> float:
        return self.__ckbf

    def get_csnow(self) -> float:
        return self.__csnow

    def get_snowtemp(self) -> float:
        return self.__snowtemp

    def get_qofmin(self) -> float:
        return self.__qofmin

    def get_beta(self) -> float:
        return self.__beta

    def get_pmm(self) -> float:
        return self.__pmm

    def get_carea(self) -> float:
        return self.__carea

    def to_array(self) -> list:
        return [
            self.__umax,
            self.__lmax,
            self.__cqof,
            self.__ckif,
            self.__ck12,
            self.__tof,
            self.__tif,
            self.__tg,
            self.__ckbf,
            self.__csnow,
            self.__snowtemp,
            self.__qofmin,
            self.__beta,
            self.__pmm,
            self.__carea,
        ]
