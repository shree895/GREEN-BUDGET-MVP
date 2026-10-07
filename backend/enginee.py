import pandas as pd


def load_model1(csv_path="data/model1.csv"):
    """Load candidate model configurations."""
    return pd.read_csv(csv_path)


def calculate_green_score(df):
    """
    Calculate normalized environmental score.

    Lower score = better environmental performance.
    """

    result = df.copy()

    for column in ["co2_g", "energy_wh", "water_l"]:

        max_value = result[column].max()

        if max_value == 0:
            result[f"{column}_normalized"] = 0
        else:
            result[f"{column}_normalized"] = (
                result[column] / max_value
            )

    result["green_score"] = (
        0.4 * result["co2_g_normalized"]
        + 0.3 * result["energy_wh_normalized"]
        + 0.3 * result["water_l_normalized"]
    )

    return result


def evaluate_budget(
    df,
    min_accuracy,
    max_co2,
    max_energy,
    max_water
):
    """Evaluate all candidate configurations."""

    result = df.copy()

    # Accuracy requirement
    result["accuracy_ok"] = (
        result["accuracy"] >= min_accuracy
    )

    # Environmental requirements
    result["co2_ok"] = (
        result["co2_g"] <= max_co2
    )

    result["energy_ok"] = (
        result["energy_wh"] <= max_energy
    )

    result["water_ok"] = (
        result["water_l"] <= max_water
    )

    # A model is feasible only if ALL requirements pass
    result["feasible"] = (
        result["accuracy_ok"]
        & result["co2_ok"]
        & result["energy_ok"]
        & result["water_ok"]
    )

    # Calculate environmental score
    result = calculate_green_score(result)

    # Lowest environmental score first
    result = result.sort_values(
        by="green_score",
        ascending=True
    )

    return result


def get_recommendation(result):
    """Return the best feasible configuration."""

    feasible = result[result["feasible"]]

    if feasible.empty:
        return None

    return feasible.iloc[0]


def get_failure_reason(row):
    """Explain why a configuration failed."""

    reasons = []

    if not row["accuracy_ok"]:
        reasons.append("Accuracy")

    if not row["co2_ok"]:
        reasons.append("CO₂")

    if not row["energy_ok"]:
        reasons.append("Energy")

    if not row["water_ok"]:
        reasons.append("Water")

    if not reasons:
        return "Feasible"

    return "Exceeded: " + ", ".join(reasons)
