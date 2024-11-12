"""
author: Olivia Chandler

"""

import numpy as np
import matplotlib.pyplot as plt
import math as m


def thermal_conductivity(material, temp):

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
        log_temp = m.log10(temperature)
        equation.append(
            10
            ** (
                a
                + b * log_temp
                + c * log_temp**2
                + d * log_temp**3
                + e * log_temp**4
                + f * log_temp**5
                + g * log_temp**6
                + h * log_temp**7
                + i * log_temp**8
            )
        )

    # Find the value at specified temp
    log_temp = m.log10(temp)
    value_at_temp = 10 ** (
        a
        + b * log_temp
        + c * log_temp**2
        + d * log_temp**3
        + e * log_temp**4
        + f * log_temp**5
        + g * log_temp**6
        + h * log_temp**7
        + i * log_temp**8
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
