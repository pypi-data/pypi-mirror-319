import logging
from typing import Final

from shapely.geometry.base import BaseGeometry

from roseau.load_flow import ALPHA, ALPHA2, RoseauLoadFlowException, RoseauLoadFlowExceptionCode, TransformerParameters
from roseau.load_flow.typing import Float, Id, JsonDict
from roseau.load_flow.units import Q_, ureg_wraps
from roseau.load_flow_engine.cy_engine import CySingleTransformer
from roseau.load_flow_single.models.branches import AbstractBranch
from roseau.load_flow_single.models.buses import Bus

logger = logging.getLogger(__name__)

# TODO: add more vector groups
_K_DIRECT_SYS_FACTOR: Final = {
    ("D", "d", 0): 1 + 0j,
    ("Y", "y", 0): 1 + 0j,
    ("D", "z", 0): 3 + 0j,
    ("D", "d", 6): -1 + 0j,
    ("Y", "y", 6): -1 + 0j,
    ("D", "z", 6): -3 + 0j,
    ("D", "y", 1): 1 - ALPHA,
    ("Y", "z", 1): 1 - ALPHA,
    ("Y", "d", 1): 1 / (1 - ALPHA2),
    ("D", "y", 5): ALPHA2 - 1,
    ("Y", "z", 5): ALPHA2 - 1,
    ("Y", "d", 5): 1 / (ALPHA - 1),
    ("D", "y", 11): 1 - ALPHA2,
    ("Y", "z", 11): 1 - ALPHA2,
    ("Y", "d", 11): 1 / (1 - ALPHA),
}


class Transformer(AbstractBranch[CySingleTransformer]):
    """A generic transformer model.

    The model parameters are defined using the ``parameters`` argument.
    """

    def __init__(
        self,
        id: Id,
        bus1: Bus,
        bus2: Bus,
        *,
        parameters: TransformerParameters,
        tap: Float = 1.0,
        max_loading: Float | Q_[Float] = 1.0,
        geometry: BaseGeometry | None = None,
    ) -> None:
        """Transformer constructor.

        Args:
            id:
                A unique ID of the transformer in the network transformers.

            bus1:
                Bus to connect the HV side of the transformer to.

            bus2:
                Bus to connect the LV side of the transformer to.

            parameters:
                Parameters defining the electrical model of the transformer. This is an instance of
                the :class:`TransformerParameters` class and can be used by multiple transformers.

            tap:
                The tap of the transformer. For example, `1.0` means the tap is at the neutral
                position, `1.025` means a `+2.5%` tap, and `0.975` means a `-2.5%` tap. The value
                must be between 0.9 and 1.1.

            max_loading:
                The maximum loading of the transformer (unitless). It is used with ``parameters.sn``
                to compute the maximum allowed power of the transformer and to determine if the
                transformer is overloaded.

            geometry:
                The geometry of the transformer.
        """
        super().__init__(id=id, bus1=bus1, bus2=bus2, n=2, geometry=geometry)

        if parameters.type != "three-phase":
            msg = f"{parameters.type.capitalize()} transformers are not allowed in a balanced three-phase load flow."
            logger.error(msg)
            raise RoseauLoadFlowException(msg=msg, code=RoseauLoadFlowExceptionCode.BAD_TRANSFORMER_TYPE)

        self.tap = tap
        self._parameters = parameters
        self.max_loading = max_loading

        # Equivalent direct-system (positive-sequence) parameters
        z2, ym, k = self._get_direct_sys_zyk(parameters)

        self._cy_element = CySingleTransformer(z2=z2, ym=ym, k=k * tap)
        self._cy_connect()

    @staticmethod
    def _get_direct_sys_zyk(tp: TransformerParameters) -> tuple[complex, complex, complex]:
        """Get the equivalent direct-system (positive-sequence) transformer parameters."""
        w1, w2 = tp.winding1[0], tp.winding2[0]
        z2, ym = tp._z2, tp._ym
        if w1 == "D":
            ym *= 3.0
        if w2 == "d":
            z2 /= 3.0
        k = tp._k * _K_DIRECT_SYS_FACTOR[w1[0], w2[0], tp.phase_displacement]
        return z2, ym, k

    @property
    def tap(self) -> float:
        """The tap of the transformer, for example 1.02."""
        return self._tap

    @tap.setter
    def tap(self, value: Float) -> None:
        if value > 1.1:
            logger.warning(f"The provided tap {value:.2f} is higher than 1.1. A good value is between 0.9 and 1.1.")
        if value < 0.9:
            logger.warning(f"The provided tap {value:.2f} is lower than 0.9. A good value is between 0.9 and 1.1.")
        self._tap = float(value)
        self._invalidate_network_results()
        if self._cy_element is not None:
            z2, ym, k = self._get_direct_sys_zyk(self.parameters)
            self._cy_element.update_transformer_parameters(z2, ym, k * value)

    @property
    def parameters(self) -> TransformerParameters:
        """The parameters of the transformer."""
        return self._parameters

    @parameters.setter
    def parameters(self, value: TransformerParameters) -> None:
        # Note here we allow changing the vector group as the model is the same
        if value.type != "three-phase":
            msg = f"{value.type.capitalize()} transformers are not allowed in a balanced three-phase load flow."
            logger.error(msg)
            raise RoseauLoadFlowException(msg=msg, code=RoseauLoadFlowExceptionCode.BAD_TRANSFORMER_TYPE)
        self._parameters = value
        self._invalidate_network_results()
        if self._cy_element is not None:
            z2, ym, k = self._get_direct_sys_zyk(value)
            self._cy_element.update_transformer_parameters(z2, ym, k * self.tap)

    @property
    @ureg_wraps("", (None,))
    def max_loading(self) -> Q_[float]:
        """The maximum loading of the transformer (unitless)"""
        return self._max_loading

    @max_loading.setter
    @ureg_wraps(None, (None, ""))
    def max_loading(self, value: Float | Q_[Float]) -> None:
        if value <= 0:
            msg = f"Maximum loading must be positive: {value} was provided."
            logger.error(msg)
            raise RoseauLoadFlowException(msg=msg, code=RoseauLoadFlowExceptionCode.BAD_MAX_LOADING_VALUE)
        self._max_loading = float(value)

    @property
    def sn(self) -> Q_[float]:
        """The nominal power of the transformer (VA)."""
        # Do not add a setter. The user must know that if they change the nominal power, it changes
        # for all transformers that share the parameters. It is better to set it on the parameters.
        return self._parameters.sn

    @property
    def max_power(self) -> Q_[float] | None:
        """The maximum power loading of the transformer (in VA)."""
        sn = self.parameters._sn
        return None if sn is None else Q_(sn * self._max_loading, "VA")

    @property
    @ureg_wraps("VA", (None,))
    def res_power_losses(self) -> Q_[complex]:
        """Get the total power losses in the transformer (in VA)."""
        power1, power2 = self._res_powers_getter(warning=True)
        return power1 + power2

    def _res_loading_getter(self, warning: bool) -> float:
        sn = self._parameters._sn
        power1, power2 = self._res_powers_getter(warning=warning)
        return max(abs(power1), abs(power2)) / sn

    @property
    @ureg_wraps("", (None,))
    def res_loading(self) -> Q_[float]:
        """Get the loading of the transformer (unitless)."""
        return self._res_loading_getter(warning=True)

    @property
    def res_violated(self) -> bool:
        """Whether the transformer power loading exceeds its maximal loading."""
        # True if either the primary or secondary is overloaded
        loading = self._res_loading_getter(warning=True)
        return bool(loading > self._max_loading)

    #
    # Json Mixin interface
    #
    def _to_dict(self, include_results: bool) -> JsonDict:
        res = super()._to_dict(include_results=include_results)
        res["tap"] = self.tap
        res["params_id"] = self.parameters.id
        res["max_loading"] = self._max_loading

        return res

    def _results_to_dict(self, warning: bool, full: bool) -> JsonDict:
        current1, current2 = self._res_currents_getter(warning)
        results = {
            "id": self.id,
            "current1": [current1.real, current1.imag],
            "current2": [current2.real, current2.imag],
        }
        if full:
            voltage1, voltage2 = self._res_voltages_getter(warning=False)
            results["voltage1"] = [voltage1.real, voltage1.imag]
            results["voltage2"] = [voltage2.real, voltage2.imag]
            power1, power2 = self._res_powers_getter(
                warning=False,
                voltage1=voltage1,
                voltage2=voltage2,
                current1=current1,
                current2=current2,
            )
            results["power1"] = [power1.real, power1.imag]
            results["power2"] = [power2.real, power2.imag]

            power_losses = power1 + power2
            results["power_losses"] = [power_losses.real, power_losses.imag]

            loading = max(abs(power1), abs(power2)) / self.parameters._sn
            results["loading"] = loading

        return results
