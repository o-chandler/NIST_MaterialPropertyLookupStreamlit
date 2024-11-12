"""
author: Olivia Chandler

"""

import numpy as np
import matplotlib.pyplot as plt
import math as m


def linearExpansion(material, temp):
    if not is_temp_in_range(material.linearExpansionDataRange, temp):
        return None, None, None, None, None, None

    material_properties = material.linearExpansion
    start_value = material.linearExpansionDataRange[0]
    end_value = material.linearExpansionDataRange[1]

    T, equation, value_at_temp = find_linearExpansion(
        start_value, end_value, material_properties, temp, material
    )

    title = f"Linear Expansion of {material.name} from {material.linearExpansionDataRange[0]}K to {material.linearExpansionDataRange[1]}K"
    ylabel = "Linear Expansion 10^5*(L0-L)/(L)"

    return T, equation, temp, value_at_temp, ylabel, title


def is_temp_in_range(data_range, temp):
    return data_range[0] <= temp < data_range[-1]


def find_linearExpansion(start_value, end_value, material_properties, temp, material):
    if material.linearExpansionTlow != 0:
        T = np.arange(material.linearExpansionTlow, end_value + 1, 1)
        T_low_region = np.arange(start_value, material.linearExpansionTlow + 1, 1)
    else:
        T = np.arange(start_value, end_value + 1, 1)

    a, b, c, d, e, f = material_properties
    equation = []
    value_Tlow = []
    for temperature in T:
        equation.append(
            a
            + (b) * temperature
            + (c) * temperature**2
            + (d) * temperature**3
            + (e) * temperature**4
        )

    if material.linearExpansionTlow != 0:  # Check if we have T_low value
        if (
            temp < material.linearExpansionTlow
        ):  # Check if given temp is below Tlow value
            value_at_temp = f  # Set to T_low value (f) if it is
        else:  # Otherwise solve for it
            value_at_temp = (
                a + (b) * temp + (c) * temp**2 + (d) * temp**3 + (e) * temp**4
            )
        for (
            temperature
        ) in T_low_region:  # Set array with values for f for length of T_low
            value_Tlow.append(f)
        entire_values = np.hstack((value_Tlow, equation))
        T_total = np.hstack((T_low_region, T))
        return T_total, entire_values, value_at_temp
    else:
        value_at_temp = a + (b) * temp + (c) * temp**2 + (d) * temp**3 + (e) * temp**4
        return T, equation, value_at_temp
