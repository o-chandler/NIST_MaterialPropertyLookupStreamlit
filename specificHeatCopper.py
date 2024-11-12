"""
author: Olivia Chandler

"""

import numpy as np
import matplotlib.pyplot as plt
import math as m


def specific_heat_copper(material, temp):

    if (  # Check if temperature is within data range
        temp < material.specificHeatDataRange[0]
        or temp >= material.specificHeatDataRange[-1]
    ):
        return (
            None,
            None,
            None,
            None,
            None,
            None,
        )  # Set values to none if temperature is out of range

    title = (
        "Specific Heat of "
        + material.name
        + " from "
        + str(material.specificHeatDataRange[0])
        + "K to "
        + str(material.specificHeatDataRange[-1])
        + "K"
    )
    ylabel = "Specific Heat (J/kg-K)"

    T = np.arange(
        material.specificHeatDataRange[0], material.specificHeatDataRange[1], 0.1
    )  # Make an array of values from start temp to end temp
    a, b, c, d, e, f, g, h, i = material.specificHeat  # Set coefficients

    equation = []  # Initialize equation list

    for temperature in T:  # Find Specific Heat at each temperature
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

    title = (
        "Specific Heat of "
        + material.name
        + " from "
        + str(material.specificHeatDataRange[0])
        + "K to "
        + str(material.specificHeatDataRange[-1])
        + "K"
    )
    ylabel = "Specific Heat (J/kg-K)"

    return T, equation, temp, value_at_temp, ylabel, title
