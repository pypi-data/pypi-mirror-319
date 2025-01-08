import contextlib
import io
import uuid
from datetime import datetime
from typing import Optional, Literal

import numpy as np
from PIL import Image
from hydutils.df_helper import validate_columns_for_nulls, validate_interval, filter_timeseries
from hydutils.hydrology_constants import PRECIPITATION, EVAPOTRANSPIRATION, TEMPERATURE, DISCHARGE, TIMESTAMP
from hydutils.statistical_metrics import mse, rmse, nse, r2, pbias, fbias
from matplotlib import pyplot as plt
from scipy.optimize import minimize

from hydnam.dataset import Dataset
from hydnam.model_output import ModelOutput
from hydnam.parameters import Parameters
from hydnam.statistical_metrics import StatisticalMetrics


class HydNAM:
    def __init__(
            self,
            dataset: Dataset,
            parameters: Parameters,
            interval: float,
            area: float,
            start: Optional[datetime] = None,
            end: Optional[datetime] = None,
            spin_off: float = 0.0,
            name: Optional[str] = None,
    ):
        self.__dataset = dataset
        self.__parameters = parameters
        self.__area = area
        self.__interval = interval
        self.__start = start if start is not None else dataset.get_timestamp()[0]
        self.__end = end if end is not None else dataset.get_timestamp()[-1]
        self.__spin_off = spin_off
        self.__name = name if name is not None else uuid.uuid4().hex

        self.__flow_rate = self.__area / (3.6 * self.__interval)

        self.__statistical_metrics = StatisticalMetrics()
        self.__model_output = ModelOutput(
            *[np.array([-9999] * len(dataset.get_timestamp())) for _ in range(12)]
        )

        self.__model_is_broken = False

        self.__nam()

    def get_dataset(self):
        return self.__dataset

    def get_parameters(self):
        return self.__parameters

    def get_area(self):
        return self.__area

    def get_interval(self):
        return self.__interval

    def get_start(self):
        return self.__start

    def get_end(self):
        return self.__end

    def get_spin_off(self):
        return self.__spin_off

    def get_name(self):
        return self.__name

    def get_flow_rate(self):
        return self.__flow_rate

    def get_statistical_metrics(self):
        return self.__statistical_metrics

    def get_model_output(self):
        return self.__model_output

    def model_is_broken(self):
        return self.__model_is_broken

    def __nam(self):
        try:
            interval = self.__interval
            start = self.__start
            end = self.__end

            ds = self.__dataset
            df = ds.to_dataframe()
            df = validate_columns_for_nulls(df)
            df = validate_interval(df, interval)
            df = filter_timeseries(df, start=start, end=end)

            x = self.__parameters

            _P = df[PRECIPITATION].reset_index(drop=True).to_numpy()
            _E = df[EVAPOTRANSPIRATION].reset_index(drop=True).to_numpy()
            _T = df[TEMPERATURE].reset_index(drop=True).to_numpy()

            size = len(_P)

            qofmin, beta, pmm, carea = (
                x.get_qofmin(),
                x.get_beta(),
                x.get_pmm(),
                x.get_carea(),
            )
            spin_off = self.__spin_off

            snow, u, _l, if1, if2, of1, of2, bf = (0, 0, 0.9 * x.get_lmax(), 0, 0, 0, 0, 0.1)
            umax, lmax, cqof, ckif, ck12, tof, tif, tg, ckbf, csnow, snowtemp = (
                x.get_umax(), x.get_lmax(), x.get_cqof(), x.get_ckif(),
                x.get_ck12(), x.get_tof(), x.get_tif(), x.get_tg(),
                x.get_ckbf(), x.get_csnow(), x.get_snowtemp(),
            )
            ckif /= interval
            ck12 /= interval
            ckbf /= interval

            lfrac = _l / lmax
            fact = self.__flow_rate

            q_sim = np.zeros(size)
            l_soil, u_soil, s_snow, q_snow = (np.zeros(size) for _ in range(4))
            q_inter, e_eal, q_of, q_g, q_bf = (np.zeros(size) for _ in range(5))

            for t, (prec, evap, temp) in enumerate(zip(_P, _E, _T)):
                if temp < snowtemp:
                    snow += prec
                    qs = 0
                else:
                    qs = min(csnow * temp, snow)
                    snow -= qs

                u1 = u + (prec + qs) if temp >= 0 else u
                eau = min(u1, evap)
                eal = (evap - eau) * lfrac if u1 > evap else 0

                u2 = min(u1 - eau, umax)
                qif = (lfrac - tif) / (1 - tif) * u2 / ckif if lfrac > tif else 0

                u3 = u1 - eau - qif
                pn = max(0, u3 - umax)
                u = min(u3, umax)

                n = int(pn / pmm) + 1
                pnlst = pn - (n - 1) * pmm
                eal /= n

                qofsum, gsum = 0, 0
                for i in range(n):
                    pn = pmm if i < n - 1 else pnlst
                    qof = cqof * (lfrac - tof) / (1 - tof) * pn if lfrac > tof else 0
                    qofsum += qof
                    g = (lfrac - tg) / (1 - tg) * (pn - qof) if lfrac > tg else 0
                    gsum += g

                c = np.exp(-1.0 / ckbf)
                bf = bf * c + gsum * carea * (1 - c)

                c = np.exp(-1.0 / ck12)
                if1 = if1 * c + qif * (1 - c)
                if2 = if2 * c + if1 * (1 - c)

                of = 0.5 * (of1 + of2) / interval
                ckqof = ck12 * (of / qofmin) ** (-beta) if of > qofmin else ck12
                c = np.exp(-1.0 / ckqof)
                of1 = of1 * c + qofsum * (1 - c)
                of2 = of2 * c + of1 * (1 - c)

                if t >= spin_off:
                    q_sim[t] = fact * (if2 + of2 + bf)
                    l_soil[t], u_soil[t] = lfrac, u
                    s_snow[t], q_snow[t] = snow, qs
                    q_inter[t], e_eal[t] = qif, eal
                    q_of[t], q_g[t], q_bf[t] = qofsum, gsum, bf

                    dl = pn - qofsum - gsum
                    _l = min(_l + dl - eal, lmax)
                    lfrac = _l / lmax

            timestamp = df[TIMESTAMP].reset_index(drop=True).to_numpy()
            q_obs = df[DISCHARGE].reset_index(drop=True).to_numpy()
            self.__model_output = ModelOutput(
                timestamp, q_obs,
                q_sim, u_soil, s_snow, q_snow,
                q_inter, e_eal, q_of, q_g, q_bf, l_soil
            )
            self.__statistical_metrics = StatisticalMetrics(
                mse(q_sim, q_obs),
                rmse(q_sim, q_obs),
                nse(q_sim, q_obs),
                r2(q_sim, q_obs),
                pbias(q_obs, q_sim),
                fbias(q_obs, q_sim)
            )
        except Exception as e:
            self.__model_is_broken = True
            raise e
        self.__model_is_broken = False

    @contextlib.contextmanager
    def __before_compute(self):
        yield
        self.__nam()

    def update_dataset(self, dataset: Dataset, interval: float):
        with self.__before_compute():
            self.__dataset = dataset
            self.__interval = interval

    def update_parameters(self, parameters: Parameters):
        with self.__before_compute():
            self.__parameters = parameters

    def update_area(self, area: float):
        with self.__before_compute():
            self.__area = area
            self.__flow_rate = self.__area / (3.6 * self.__interval)

    def update_time_range(self, start: Optional[datetime], end: Optional[datetime]):
        with self.__before_compute():
            self.__start = start if start is not None else self.__dataset.get_timestamp()[0]
            self.__end = end if end is not None else self.__dataset.get_timestamp()[-1]

    def update_spin_off(self, spin_off: float):
        with self.__before_compute():
            self.__spin_off = spin_off

    def update_name(self, name: str):
        self.__name = name

    def __objective(self, x):
        with self.__before_compute():
            self.__parameters = Parameters(*x)
        return rmse(
            self.__model_output.get_q_sim(),
            self.__model_output.get_q_obs()
        )

    def optimize(
            self, method: Literal['SLSQP', 'L-BFGS-B'], bounds=Parameters.bounds,
            maxiter: float = 1e8,
            disp: bool = False,
            eps: float = 0.01,
    ):
        parameters = minimize(
            self.__objective,
            np.array(Parameters().to_array()),
            method=method,
            bounds=bounds,
            options={"maxiter": maxiter, "disp": disp, "eps": eps},
        ).x

        with self.__before_compute():
            self.__parameters = Parameters(*parameters)

    def reload(self):
        self.__nam()

    def plot_q(
            self, only_obs_and_sim: bool = False, figsize=(10, 6)
    ):
        mo = self.__model_output
        ts = mo.get_timestamp()

        plt.figure(figsize=figsize)
        plt.plot(
            ts, mo.get_q_obs(), label="Q_obs", color="blue", linestyle="--", marker="o"
        )
        plt.plot(
            ts, mo.get_q_sim(), label="Q_sim", color="red", linestyle="--", marker="o"
        )

        if not only_obs_and_sim:
            plt.plot(ts, mo.get_q_snow(), label="Q_snow")
            plt.plot(ts, mo.get_q_inter(), label="Q_inter")
            plt.plot(ts, mo.get_q_of(), label="Q_of")
            plt.plot(ts, mo.get_q_g(), label="Q_g")
            plt.plot(ts, mo.get_q_bf(), label="Q_bf")

        plt.xlabel("Timestamp")
        plt.ylabel("Q")
        plt.legend()
        plt.grid(True)

        buf = io.BytesIO()
        plt.savefig(buf, format="PNG")
        buf.seek(0)

        image = Image.open(buf)
        plt.close()

        return image
