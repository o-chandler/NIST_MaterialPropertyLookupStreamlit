"""
author: Olivia Chandler

"""

import numpy as np
import matplotlib.pyplot as plt
import math as m


def linearExpansion_copper(material, temp):

    if (  # Check if temperature is within data range
        temp < material.linearExpansionDataRange[0]
        or temp >= material.linearExpansionDataRange[-1]
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
        "Linear Expansion of "
        + material.name
        + " from "
        + str(material.linearExpansionDataRange[0])
        + "K to "
        + str(material.linearExpansionDataRange[-1])
        + "K"
    )
    ylabel = "Linear Expansion (L0-L)/(L) *10e5"

    T = np.arange(
        material.linearExpansionDataRange[0], material.linearExpansionDataRange[1], 0.1
    )  # Make an array of values from start temp to end temp
    a, b, c, d, e, f, g = material.linearExpansion  # Set coefficients

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
    )

    return T, equation, temp, value_at_temp, ylabel, title
