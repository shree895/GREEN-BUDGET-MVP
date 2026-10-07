
import streamlit as st
import pandas as pd
import plotly.express as px

from backend.enginee import (
    load_model1,
    evaluate_budget,
    get_recommendation,
    get_failure_reason,
)


# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="Green Budget",
    page_icon="🌱",
    layout="wide",
)


# -----------------------------
# Header
# -----------------------------
st.title("🌱 Green Budget")

st.write(
    "Give AI an environmental budget. Let it choose the model."
)

st.write(
    "Set your accuracy, carbon, energy and water limits "
    "to find the most sustainable feasible configuration."
)

st.divider()


# -----------------------------
# Load model data
# -----------------------------
try:
    models = load_model1("data/model1.csv")
except Exception as e:
    st.error(f"Could not load model data: {e}")
    st.stop()
st.write("DEBUG COLUMNS:", models.columns.tolist())
st.write("DEBUG DATA:", models)


# -----------------------------
# Budget inputs
# -----------------------------
st.subheader("🎯 Define Your Environmental Budget")

col1, col2, col3, col4 = st.columns(4)

with col1:
    min_accuracy = st.number_input(
        "Minimum Accuracy (%)",
        min_value=0.0,
        max_value=100.0,
        value=92.0,
        step=0.1,
    )

with col2:
    max_co2 = st.number_input(
        "Maximum CO₂ (g)",
        min_value=0.0,
        value=30.0,
        step=0.5,
    )

with col3:
    max_energy = st.number_input(
        "Maximum Energy (Wh)",
        min_value=0.0,
        value=60.0,
        step=1.0,
    )

with col4:
    max_water = st.number_input(
        "Maximum Water (L)",
        min_value=0.0,
        value=5.0,
        step=0.1,
    )


st.write("")


# -----------------------------
# Evaluate models
# -----------------------------
if st.button(
    "🔍 Evaluate Models",
    type="primary",
    use_container_width=True,
):

    result = evaluate_budget(
        models,
        min_accuracy,
        max_co2,
        max_energy,
        max_water,
    )

    recommendation = get_recommendation(result)

    st.divider()

    # -----------------------------
    # Recommendation
    # -----------------------------
    st.subheader("🏆 Recommendation")

    if recommendation is None:

        st.warning(
            "No configuration satisfies all four budget constraints."
        )

    else:

        st.success(
            f"Recommended configuration: "
            f"**{recommendation['configuration']}**"
        )

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "Accuracy",
                f"{recommendation['accuracy']:.1f}%",
            )

        with c2:
            st.metric(
                "CO₂",
                f"{recommendation['co2_g']:.1f} g",
            )

        with c3:
            st.metric(
                "Energy",
                f"{recommendation['energy_wh']:.1f} Wh",
            )

        with c4:
            st.metric(
                "Water",
                f"{recommendation['water_l']:.1f} L",
            )

        st.write(
            f"**Green Score:** "
            f"{recommendation['green_score']:.3f}"
        )


    # -----------------------------
    # Model comparison
    # -----------------------------
    st.subheader("📊 Model Evaluation")

    display_df = result[
        [
            "configuration",
            "accuracy",
            "co2_g",
            "energy_wh",
            "water_l",
            "green_score",
            "feasible",
        ]
    ].copy()

    display_df["accuracy"] = (
        display_df["accuracy"]
    ).round(1)

    display_df["green_score"] = (
        display_df["green_score"].round(3)
    )

    display_df = display_df.rename(
        columns={
            "configuration": "Configuration",
            "accuracy": "Accuracy (%)",
            "co2_g": "CO₂ (g)",
            "energy_wh": "Energy (Wh)",
            "water_l": "Water (L)",
            "green_score": "Green Score",
            "feasible": "Feasible",
        }
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )


    # -----------------------------
    # Constraint analysis
    # -----------------------------
    st.subheader("🔎 Constraint Analysis")

    reasons_df = result[
        ["configuration", "feasible"]
    ].copy()

    reasons_df["Reason"] = result.apply(
        get_failure_reason,
        axis=1,
    )

    reasons_df = reasons_df.rename(
        columns={
            "configuration": "Configuration",
            "feasible": "Feasible",
        }
    )

    st.dataframe(
        reasons_df,
        use_container_width=True,
        hide_index=True,
    )


    # -----------------------------
    # Environmental comparison
    # -----------------------------
    st.subheader("🌍 Environmental Comparison")

    chart_df = result[
        [
            "configuration",
            "co2_g",
            "energy_wh",
            "water_l",
        ]
    ].copy()

    chart_df = chart_df.rename(
        columns={
            "configuration": "Configuration",
            "co2_g": "CO₂ (g)",
            "energy_wh": "Energy (Wh)",
            "water_l": "Water (L)",
        }
    )

    chart_long = chart_df.melt(
        id_vars="Configuration",
        var_name="Metric",
        value_name="Value",
    )

    fig = px.bar(
        chart_long,
        x="Configuration",
        y="Value",
        color="Metric",
        barmode="group",
        title="Environmental Resource Consumption",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


# -----------------------------
# Disclaimer
# -----------------------------
st.divider()

st.caption(
    "Disclaimer: MVP environmental values are benchmark/estimated inputs. "
    "Production deployment would use measured workload data and documented "
    "regional environmental factors."
)

