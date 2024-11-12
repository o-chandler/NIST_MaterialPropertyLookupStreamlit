"""
author: Olivia Chandler

"""

import numpy as np
import matplotlib.pyplot as plt
import math as m


def thermal_conductivity_copper(material, temp):

    start_value = material.thermalConductivityDataRange[0]  # Set start temp
    end_value = material.thermalConductivityDataRange[1]  # Set end temp

    if (  # Check if temperature is within data range
        temp < material.thermalConductivityDataRange[0]
        or temp >= material.thermalConductivityDataRange[-1]
    ):
        return None, None, None, None, None, None

    T = np.arange(
        start_value, end_value, 0.1
    )  # Make an array of values from start temp to end temp
    a, b, c, d, e, f, g, h, i = material.thermalConductivity  # Set coefficients

    equation = []  # Initialize equation list

    for temperature in T:  # Find thermal conductivity at each temperature
        equation.append(
            10
            ** (
                (
                    a
                    + c * temperature**0.5
                    + e * temperature
                    + g * temperature**1.5
                    + i * temperature**2
                )
                / (
                    1
                    + b * temperature**0.5
                    + d * temperature
                    + f * temperature**1.5
                    + h * temperature**2
                )
            )
        )

    # Find the value at specified temp
    value_at_temp = 10 ** (
        (a + c * temp**0.5 + e * temp + g * temp**1.5 + i * temp**2)
        / (1 + b * temp**0.5 + d * temp + f * temp**1.5 + h * temp**2)
    )

    ylabel = "Thermal Conductivity (W/m-K)"
    title = (
        "Thermal Conductivity of "
        + material.name
        + " from "
        + str(start_value)
        + "K to "
        + str(end_value)
        + "K"
    )

    return T, equation, temp, value_at_temp, ylabel, title
