"""
author: Olivia Chandler

"""

import numpy as np
import math as m


def specific_heat(material, temp):
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

    # Handle case where material has more than 9 coefficients (piecewise range)
    if len(material.specificHeat) > 9:
        return handle_piecewise_specific_heat(material, temp, ylabel, title)
    else:
        return handle_single_range_specific_heat(material, temp, ylabel, title)


# Finds properties if specific heat is piecewise
def handle_piecewise_specific_heat(material, temp, ylabel, title):
    # Split data into two sets of coefficients and ranges
    material_properties1, material_properties2 = (
        material.specificHeat[:9],
        material.specificHeat[9:],
    )
    start_value1, end_value1, start_value2, end_value2 = material.specificHeatDataRange

    # Determine which range temp belongs to
    if temp <= end_value1:
        T1, results1, value_at_temp1 = find_specific_heat(
            start_value1, end_value1, material_properties1, temp
        )
        T2, results2, value_at_temp2 = find_specific_heat(
            start_value2, end_value2, material_properties2, -1
        )
        value_at_temp = value_at_temp1
    else:
        T1, results1, value_at_temp1 = find_specific_heat(
            start_value1, end_value1, material_properties1, -1
        )
        T2, results2, value_at_temp2 = find_specific_heat(
            start_value2, end_value2, material_properties2, temp
        )
        value_at_temp = value_at_temp2

    total_temp_range = np.hstack((T1, T2))
    full_results = np.hstack((results1, results2))

    return total_temp_range, full_results, temp, value_at_temp, ylabel, title


# Finds specific heat if range is singular
def handle_single_range_specific_heat(material, temp, ylabel, title):
    material_properties = material.specificHeat
    start_value, end_value = material.specificHeatDataRange
    T, results, value_at_temp = find_specific_heat(
        start_value, end_value, material_properties, temp
    )

    return T, results, temp, value_at_temp, ylabel, title


# Finds specific heat
def find_specific_heat(start_value, end_value, material_properties, temp):
    T = np.arange(start_value, end_value + 1, 1)
    a, b, c, d, e, f, g, h, i = material_properties

    # Calculate the equation for the temperature range
    equation = [
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
        for log_temp in map(m.log10, T)
    ]

    # Calculate the specific heat at the given temp (if it's valid)
    value_at_temp = 0
    if temp != -1:
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

    return T, equation, value_at_temp
