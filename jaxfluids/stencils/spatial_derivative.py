from abc import ABC, abstractmethod
from typing import List

import jax.numpy as jnp


class SpatialDerivative(ABC):
    """Abstract parent class for the computation of spatial derivatives.

    Calculates either the first spatial derivative wrt to axis direction (derivative_xi),
    or calculates the second spatial derivative wrt to axis1 and axis2 directions (
    derivative_xi_xj).
    """

    eps = jnp.finfo(jnp.float64).eps

    def __init__(self, nh: int, inactive_axis: List, offset: int = 0) -> None:
        self.n = nh - offset
        self.nhx = jnp.s_[:] if "x" in inactive_axis else jnp.s_[self.n : -self.n]
        self.nhy = jnp.s_[:] if "y" in inactive_axis else jnp.s_[self.n : -self.n]
        self.nhz = jnp.s_[:] if "z" in inactive_axis else jnp.s_[self.n : -self.n]

        self.eps = jnp.finfo(jnp.float64).eps

    @abstractmethod
    def derivative_xi(
        self, buffer: jnp.DeviceArray, dxi: jnp.DeviceArray, axis: int
    ) -> jnp.DeviceArray:
        """Calculates the derivative in the direction indicated by axis.

        :param buffer: Buffer for which the derivative will be calculated
        :type buffer: jnp.DeviceArray
        :param dxi: Cell sizes along axis direction
        :type dxi: jnp.DeviceArray
        :param axis: Spatial axis along which derivative is calculated
        :type axis: int
        :return: Buffer with numerical derivative
        :rtype: jnp.DeviceArray
        """
        pass

    def derivative_xi_xj(
        self, buffer: jnp.DeviceArray, dxi: jnp.DeviceArray, dxj: jnp.DeviceArray, i: int, j: int
    ) -> jnp.DeviceArray:
        """Calculates the second derivative in the directions indicated by i and j.

        :param buffer: Buffer for which the second derivative will be calculated
        :type buffer: jnp.DeviceArray
        :param dxi: Cell sizes along i direction
        :type dxi: jnp.DeviceArray
        :param dxj: Cell sizes along j direction
        :type dxj: jnp.DeviceArray
        :param i: Spatial axis along which derivative is calculated
        :type i: int
        :param j: Spatial axis along which derivative is calculated
        :type j: int
        :return: Buffer with numerical derivative
        :rtype: jnp.DeviceArray
        """
        pass
