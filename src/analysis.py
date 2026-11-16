from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "raw" / "synthetic_quality_data.csv"
OUTPUT_DIR = ROOT / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

REQUIRED_COLUMNS = {
    "inspection_date", "product_family", "supplier", "production_line",
    "shift", "units_inspected", "defect_units", "defect_category",
    "severity", "downtime_minutes"
}


def load_data(path: Path) -> pd.DataFrame:
    """Load the synthetic dataset and perform basic data validation."""
    data = pd.read_csv(path, parse_dates=["inspection_date"])
    missing_columns = REQUIRED_COLUMNS - set(data.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    if data[list(REQUIRED_COLUMNS)].isna().any().any():
        raise ValueError("The dataset contains missing values in required columns.")
    if (data["units_inspected"] <= 0).any():
        raise ValueError("units_inspected must be greater than zero.")
    if (data["defect_units"] < 0).any() or (
        data["defect_units"] > data["units_inspected"]
    ).any():
        raise ValueError("defect_units must be between zero and units_inspected.")
    if (data["downtime_minutes"] < 0).any():
        raise ValueError("downtime_minutes cannot be negative.")

    return data


def main() -> None:
    data = load_data(DATA_PATH)
    data["defect_rate"] = data["defect_units"] / data["units_inspected"]
    data["month"] = data["inspection_date"].dt.to_period("M").astype(str)

    total_inspected = int(data["units_inspected"].sum())
    total_defects = int(data["defect_units"].sum())
    overall_rate = total_defects / total_inspected

    kpis = pd.DataFrame([{
        "inspection_records": len(data),
        "units_inspected": total_inspected,
        "defect_units": total_defects,
        "overall_defect_rate": overall_rate,
        "total_downtime_minutes": int(data["downtime_minutes"].sum())
    }])
    kpis.to_csv(OUTPUT_DIR / "kpi_summary.csv", index=False)

    monthly = (
        data.groupby("month", as_index=False)
        .agg(units_inspected=("units_inspected", "sum"),
             defect_units=("defect_units", "sum"))
    )
    monthly["defect_rate"] = monthly["defect_units"] / monthly["units_inspected"]
    monthly.to_csv(OUTPUT_DIR / "monthly_quality_summary.csv", index=False)

    supplier = (
        data.groupby("supplier", as_index=False)
        .agg(units_inspected=("units_inspected", "sum"),
             defect_units=("defect_units", "sum"),
             inspection_records=("supplier", "size"))
    )
    supplier["defect_rate"] = supplier["defect_units"] / supplier["units_inspected"]
    supplier.sort_values("defect_rate", ascending=False).to_csv(
        OUTPUT_DIR / "supplier_quality_summary.csv", index=False
    )

    category = (
        data.groupby("defect_category", as_index=False)
        .agg(defect_units=("defect_units", "sum"))
        .sort_values("defect_units", ascending=False)
    )
    category.to_csv(OUTPUT_DIR / "defect_category_summary.csv", index=False)

    ax = monthly.plot(
        x="month", y="defect_rate", kind="line", marker="o",
        title="Monthly Defect Rate", legend=False
    )
    ax.set_xlabel("Month")
    ax.set_ylabel("Defect rate")
    ax.tick_params(axis="x", rotation=45)
    ax.figure.tight_layout()
    ax.figure.savefig(OUTPUT_DIR / "monthly_defect_rate.png", dpi=150)
    plt.close(ax.figure)

    print(f"Analysis complete. Overall defect rate: {overall_rate:.2%}")
    print(f"Outputs saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
