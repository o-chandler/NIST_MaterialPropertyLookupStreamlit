import matplotlib.pyplot as plt
import numpy as np


def youngsModulus(material, temp):

    if (  # Check if temperature is within data range
        temp < material.youngsModulusDataRange[0]
        or temp >= material.youngsModulusDataRange[-1]
    ):
        return (
            None,
            None,
            None,
            None,
            None,
            None,
        )  # Set values to none if temperature is out of range

    ylabel = "Young's Modulus (GPa)"
    title = (
        "Young's Modulus of "
        + material.name
        + " from "
        + str(material.youngsModulusDataRange[0])
        + "K to "
        + str(material.youngsModulusDataRange[-1])
        + "K"
    )

    if len(material.youngsModulus) > 5:
        return handle_piecewise_youngsModulus(material, temp, ylabel, title)
    else:
        return handle_single_range_youngsModulus(material, temp, ylabel, title)


def handle_piecewise_youngsModulus(material, temp, ylabel, title):
    # Split data into two sets of coefficients and ranges
    material_properties1, material_properties2 = (
        material.youngsModulus[:5],
        material.youngsModulus[5:],
    )
    start_value1, end_value1, start_value2, end_value2 = material.youngsModulusDataRange

    # Determine which range temp belongs to
    if temp <= end_value1:
        T1, results1, value_at_temp1 = find_youngsModulus(
            start_value1, end_value1, material_properties1, temp
        )
        T2, results2, value_at_temp2 = find_youngsModulus(
            start_value2, end_value2, material_properties2, -1
        )
        value_at_temp = value_at_temp1
    else:
        T1, results1, value_at_temp1 = find_youngsModulus(
            start_value1, end_value1, material_properties1, -1
        )
        T2, results2, value_at_temp2 = find_youngsModulus(
            start_value2, end_value2, material_properties2, temp
        )
        value_at_temp = value_at_temp2

    total_temp_range = np.hstack((T1, T2))
    full_results = np.hstack((results1, results2))

    return total_temp_range, full_results, temp, value_at_temp, ylabel, title


# Finds youngs modulus if range is singular
def handle_single_range_youngsModulus(material, temp, ylabel, title):
    material_properties = material.youngsModulus
    start_value, end_value = material.youngsModulusDataRange
    T, results, value_at_temp = find_youngsModulus(
        start_value, end_value, material_properties, temp
    )

    return T, results, temp, value_at_temp, ylabel, title


def find_youngsModulus(start_value, end_value, material_properties, temp):
    T = np.arange(start_value, end_value + 1, 1)
    a, b, c, d, e = material_properties
    equation = []
    for temperature in T:
        equation.append(
            a
            + b * temperature
            + c * temperature**2
            + d * temperature**3
            + e * temperature**4
        )
    if temp != -1:
        value_at_temp = a + b * temp + c * temp**2 + d * temp**3 + e * temp**4
        plt.plot(temp, value_at_temp, color="red", marker="o")
    else:
        value_at_temp = 0

    return T, equation, value_at_temp
