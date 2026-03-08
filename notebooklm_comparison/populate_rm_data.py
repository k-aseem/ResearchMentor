"""
Populate Research Mentor data in the comparison tracking CSV.

Reads rm_baseline_results.json and fills in RM columns in comparison_tracking.csv.
"""

import csv
import json
import os

# File paths
RESULTS_JSON = "notebooklm_comparison/rm_baseline_results.json"
TRACKING_CSV = "notebooklm_comparison/comparison_tracking.csv"


def load_rm_results():
    """Load RM results from JSON file."""
    if not os.path.exists(RESULTS_JSON):
        raise FileNotFoundError(
            f"{RESULTS_JSON} not found. Run: python run_tests.py --category known --save-results {RESULTS_JSON}"
        )

    with open(RESULTS_JSON, "r") as f:
        data = json.load(f)

    return data.get("known", [])


def populate_csv(rm_results):
    """Update CSV with RM data."""
    # Read existing CSV
    rows = []
    with open(TRACKING_CSV, "r") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    # Create lookup dict by test_id
    rm_lookup = {result["test_id"]: result for result in rm_results}

    # Update rows
    for row in rows:
        test_id = row["Test_ID"]
        if test_id in rm_lookup:
            rm_data = rm_lookup[test_id]

            # Fill in RM columns
            row["RM_Response_Time_Seconds"] = f"{rm_data['elapsed_time']:.2f}"
            row["RM_Mode"] = rm_data["actual_mode"]
            row["RM_Judge_Score"] = str(rm_data["judge_score_rm"])
            row["RM_Answer_Quality_1_10"] = str(rm_data["judge_score_rm"])

            # Determine winner based on judge
            if rm_data["judge_winner"] == "research_mentor":
                row["Winner"] = "RM"
            elif rm_data["judge_winner"] == "baseline":
                row["Winner"] = "Baseline (tie with NotebookLLM?)"
            else:
                row["Winner"] = "TBD"

    # Write updated CSV
    with open(TRACKING_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ Updated {TRACKING_CSV} with RM data")
    print(f"   - {len(rm_results)} test results processed")
    print(f"   - RM columns populated: Response Time, Mode, Judge Score, Quality")


def main():
    print("Loading Research Mentor results...")
    rm_results = load_rm_results()

    print(f"Found {len(rm_results)} test results")

    print("\nPopulating CSV with RM data...")
    populate_csv(rm_results)

    print("\n✅ Done! You can now:")
    print("   1. Fill in NotebookLLM columns manually")
    print("   2. Run: python notebooklm_comparison/analyze_comparison.py")


if __name__ == "__main__":
    main()
