from typing import List

import jax.numpy as jnp

from jaxfluids.stencils.spatial_derivative import SpatialDerivative


class DerivativeSecondOrderFace(SpatialDerivative):
    """2nd order stencil for 1st derivative at the cell face
        x
    |   |     |
    | i | i+1 |
    |   |     |
    """

    def __init__(self, nh: int, inactive_axis: List, offset: int = 0) -> None:
        super(DerivativeSecondOrderFace, self).__init__(
            nh=nh, inactive_axis=inactive_axis, offset=offset
        )

        self.s_ = [
            [
                jnp.s_[..., self.n - 1 : -self.n, self.nhy, self.nhz],  # i
                jnp.s_[
                    ...,
                    jnp.s_[self.n : -self.n + 1] if self.n != 1 else jnp.s_[self.n : None],
                    self.nhy,
                    self.nhz,
                ],
            ],  # i+1
            [
                jnp.s_[..., self.nhx, self.n - 1 : -self.n, self.nhz],
                jnp.s_[
                    ...,
                    self.nhx,
                    jnp.s_[self.n : -self.n + 1] if self.n != 1 else jnp.s_[self.n : None],
                    self.nhz,
                ],
            ],
            [
                jnp.s_[..., self.nhx, self.nhy, self.n - 1 : -self.n],
                jnp.s_[
                    ...,
                    self.nhx,
                    self.nhy,
                    jnp.s_[self.n : -self.n + 1] if self.n != 1 else jnp.s_[self.n : None],
                ],
            ],
        ]

    def derivative_xi(
        self, buffer: jnp.DeviceArray, dxi: jnp.DeviceArray, axis: int
    ) -> jnp.DeviceArray:
        s1_ = self.s_[axis]
        deriv_xi = (1.0 / dxi) * (-buffer[s1_[0]] + buffer[s1_[1]])
        return deriv_xi