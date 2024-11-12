"""
author = Olivia Chandler

"""

import streamlit as st
import thermal_conductivity as tc
import MaterialClass as material
import specific_heat as specific_heat
import youngsModulus as ym
import linearExpansion as le
import thermalconductivitycopper as tcc
import specificHeatCopper as shc
import expansionCopper as lec
import matplotlib.pyplot as plt


# Define your available materials
material_options = [
    "Aluminum 1100",
    "Aluminum 3003F",
    "Aluminum 6061-T6",
    "Beryllium Copper",
    "Brass",
    "Copper (RRR=50)",
    "Copper (RRR=100)",
    "Copper (RRR=150)",
    "Copper (RRR=300)",
    "Copper (RRR=500)",
    "Indium",
    "Kapton",
    "Lead",
    "Nylon",
    "Stainless Steel 310",
    "Stainless Steel 304",
    "Stainless Steel 304L",
    "Stainless Steel 316",
    "Teflon",
    "G10 - Normal",
    "G10 - Warp",
]


# Helper function to get available properties for a material
def get_available_properties(selected_material_obj):
    properties = []
    if getattr(selected_material_obj, "thermalConductivity", None) is not None:
        properties.append("Thermal Conductivity")
    if getattr(selected_material_obj, "specificHeat", None) is not None:
        properties.append("Specific Heat Capacity")
    if getattr(selected_material_obj, "youngsModulus", None) is not None:
        properties.append("Young's Modulus")
    if getattr(selected_material_obj, "linearExpansion", None) is not None:
        properties.append("Linear Expansion")
    return properties


# Temperature Range Error Display
def temp_range_error(temp_datarange):
    st.error(f"Temperature exceeds bounds: [{temp_datarange[0]}, {temp_datarange[-1]}]")


# Main Calculation Function
def calculate_property(selected_material, selected_property, temp_value):
    selected_material_obj = material.find_material(selected_material)

    # Select correct calculation function based on the selected material and property
    if selected_material.startswith("Copper"):  # Copper Specific lookup functions
        if selected_property == "Thermal Conductivity":
            results = tcc.thermal_conductivity_copper(selected_material_obj, temp_value)
            if all(result is not None for result in results):
                return results
            else:
                temp_range_error(selected_material_obj.thermalConductivityDataRange)
                return None
        elif selected_property == "Specific Heat Capacity":
            results = shc.specific_heat_copper(selected_material_obj, temp_value)
            if all(result is not None for result in results):
                return results
            else:
                temp_range_error(selected_material_obj.specificHeatDataRange)
                return None
        elif selected_property == "Linear Expansion":
            results = lec.linearExpansion_copper(selected_material_obj, temp_value)
            if all(result is not None for result in results):
                return results
            else:
                temp_range_error(selected_material_obj.linearExpansionDataRange)
                return None
    else:  # Other functions
        if selected_property == "Thermal Conductivity":
            results = tc.thermal_conductivity(selected_material_obj, temp_value)
            if all(result is not None for result in results):
                return results
            else:
                temp_range_error(selected_material_obj.thermalConductivityDataRange)
                return None
        elif selected_property == "Specific Heat Capacity":
            results = specific_heat.specific_heat(selected_material_obj, temp_value)
            if all(result is not None for result in results):
                return results
            else:
                temp_range_error(selected_material_obj.specificHeatDataRange)
                return None
        elif selected_property == "Linear Expansion":
            results = le.linearExpansion(selected_material_obj, temp_value)
            if all(result is not None for result in results):
                return results
            else:
                temp_range_error(selected_material_obj.linearExpansionDataRange)
                return None
        elif selected_property == "Young's Modulus":
            results = ym.youngsModulus(selected_material_obj, temp_value)
            if all(result is not None for result in results):
                return results
            else:
                temp_range_error(selected_material_obj.youngsModulusDataRange)
                return None
    return None


# Streamlit UI
st.title("NIST Property Lookup :turtle:")
st.caption("by Olivia Chandler")
# Material selection
selected_material = st.selectbox(
    "Select a Material:",
    material_options,
    key="material_selection_key",
    index=None,
    placeholder="Select Material",
)

# Property selection based on material - find material object
selected_material_obj = material.find_material(selected_material)

# Find available properties
if selected_material_obj:
    available_properties = get_available_properties(selected_material_obj)
    selected_property = st.selectbox(
        "Select a Property:",
        available_properties,
        index=None,
        placeholder="Select Property",
    )


# Temperature input
temp_value = st.number_input(
    "Enter Temperature (K):",
    value=None,
    placeholder="Enter Temperature",
)

# Set up columns for buttons
col1, col2 = st.columns([9, 1])
with col1:
    # Calculate button
    if st.button("Calculate"):
        # Make sure all inputs are there
        if temp_value and selected_material and selected_property:
            # Perform calculation and handle errors
            results = calculate_property(
                selected_material, selected_property, temp_value
            )

            if results is not None:
                T, equation, temp, value_at_temp, ylabel, title = results
                # Display result
                # st.write("Result:", round(value_at_temp, 4))
                st.write("Result:")
                st.code(round(value_at_temp, 4), language="python")
                # Plotting
                fig, ax = plt.subplots()
                ax.plot(T, equation, label="Equation Curve")
                ax.scatter(
                    [temp],
                    [value_at_temp],
                    color="red",
                    zorder=5,
                    label=f"Point ({temp}, {value_at_temp})",
                )
                ax.grid(True)
                ax.set_title(title)
                ax.set_ylabel(ylabel)
                ax.set_xlabel("Temperature (K)")
                st.pyplot(fig)
        else:
            st.warning("Please fill in all fields to perform the calculation.")

# Clear button resets the inputs (Streamlit automatically resets on re-run)

with col2:
    if st.button("Clear"):
        # st.session_state.material_selection_key = None
        st.rerun()


st.page_link(
    "https://trc.nist.gov/cryogenics/materials/materialproperties.htm",
    label="All material properties are from the NIST Material Measurement Laboratory Index of Material Properties",
)

# st.caption(
#     "All material properties are from the NIST Material Measurement Laboratory Index of Material Properties"
# )
