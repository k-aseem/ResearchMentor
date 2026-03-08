"""
Analyze NotebookLLM vs Research Mentor comparison results.

Reads comparison_tracking.csv and generates a comprehensive report.
"""

import csv
import statistics
from typing import List, Dict


TRACKING_CSV = "notebooklm_comparison/comparison_tracking.csv"
REPORT_FILE = "notebooklm_comparison/COMPARISON_REPORT.md"


def load_comparison_data():
    """Load data from CSV."""
    with open(TRACKING_CSV, "r") as f:
        reader = csv.DictReader(f)
        return list(reader)


def parse_float_safe(value, default=None):
    """Safely parse float, return default if invalid."""
    try:
        return float(value) if value.strip() else default
    except (ValueError, AttributeError):
        return default


def calculate_metrics(rows: List[Dict]) -> Dict:
    """Calculate all comparison metrics."""

    # Filter out rows without NotebookLLM data
    valid_rows = [
        row for row in rows
        if row.get("NotebookLM_Response_Time_Seconds", "").strip()
    ]

    if not valid_rows:
        return {
            "error": "No NotebookLLM data found in CSV. Please complete Part 2 of the experiment."
        }

    # Speed metrics
    nbllm_times = [parse_float_safe(row["NotebookLM_Response_Time_Seconds"]) for row in valid_rows]
    rm_times = [parse_float_safe(row["RM_Response_Time_Seconds"]) for row in valid_rows]

    nbllm_times = [t for t in nbllm_times if t is not None]
    rm_times = [t for t in rm_times if t is not None]

    # Quality metrics
    nbllm_quality = [parse_float_safe(row["NotebookLM_Answer_Quality_1_10"]) for row in valid_rows]
    rm_quality = [parse_float_safe(row["RM_Answer_Quality_1_10"]) for row in valid_rows]

    nbllm_quality = [q for q in nbllm_quality if q is not None]
    rm_quality = [q for q in rm_quality if q is not None]

    # Citation behavior
    nbllm_cites = sum(1 for row in valid_rows if row.get("NotebookLM_Cites_Papers", "").lower() == "yes")

    # Mode detection (RM)
    librarian_mode_count = sum(1 for row in valid_rows if row.get("RM_Mode", "") == "librarian")

    # Winner breakdown
    nbllm_wins = sum(1 for row in valid_rows if "NotebookLLM" in row.get("Winner", ""))
    rm_wins = sum(1 for row in valid_rows if row.get("Winner", "") == "RM")
    ties = sum(1 for row in valid_rows if "tie" in row.get("Winner", "").lower())

    return {
        "total_tests": len(valid_rows),
        "nbllm_avg_time": statistics.mean(nbllm_times) if nbllm_times else 0,
        "nbllm_median_time": statistics.median(nbllm_times) if nbllm_times else 0,
        "rm_avg_time": statistics.mean(rm_times) if rm_times else 0,
        "rm_median_time": statistics.median(rm_times) if rm_times else 0,
        "nbllm_avg_quality": statistics.mean(nbllm_quality) if nbllm_quality else 0,
        "rm_avg_quality": statistics.mean(rm_quality) if rm_quality else 0,
        "nbllm_citation_rate": 100 * nbllm_cites / len(valid_rows) if valid_rows else 0,
        "rm_librarian_mode_rate": 100 * librarian_mode_count / len(valid_rows) if valid_rows else 0,
        "nbllm_wins": nbllm_wins,
        "rm_wins": rm_wins,
        "ties": ties,
        "valid_rows": valid_rows
    }


def generate_report(metrics: Dict) -> str:
    """Generate markdown report."""

    if "error" in metrics:
        return f"# Error\n\n{metrics['error']}"

    report_lines = []

    report_lines.append("# NotebookLLM vs Research Mentor Comparison Report")
    report_lines.append("")
    report_lines.append(f"**Date**: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"**Total Questions Tested**: {metrics['total_tests']}/30")
    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")

    # Speed comparison
    report_lines.append("## Speed Comparison")
    report_lines.append("")
    report_lines.append("| Metric | NotebookLLM | Research Mentor | Winner |")
    report_lines.append("|--------|-------------|-----------------|--------|")

    speed_winner = "NotebookLLM" if metrics['nbllm_avg_time'] < metrics['rm_avg_time'] else "RM"
    report_lines.append(f"| **Average Time** | {metrics['nbllm_avg_time']:.2f}s | {metrics['rm_avg_time']:.2f}s | **{speed_winner}** |")

    median_winner = "NotebookLLM" if metrics['nbllm_median_time'] < metrics['rm_median_time'] else "RM"
    report_lines.append(f"| **Median Time** | {metrics['nbllm_median_time']:.2f}s | {metrics['rm_median_time']:.2f}s | **{median_winner}** |")

    time_diff = abs(metrics['nbllm_avg_time'] - metrics['rm_avg_time'])
    time_diff_pct = 100 * time_diff / max(metrics['nbllm_avg_time'], metrics['rm_avg_time'])
    report_lines.append("")
    report_lines.append(f"**Speed Difference**: {time_diff:.2f}s ({time_diff_pct:.1f}%)")
    report_lines.append("")

    # Quality comparison
    report_lines.append("## Quality Comparison")
    report_lines.append("")
    report_lines.append("| Metric | NotebookLLM | Research Mentor | Winner |")
    report_lines.append("|--------|-------------|-----------------|--------|")

    quality_winner = "NotebookLLM" if metrics['nbllm_avg_quality'] > metrics['rm_avg_quality'] else "RM"
    report_lines.append(f"| **Average Quality (1-10)** | {metrics['nbllm_avg_quality']:.2f} | {metrics['rm_avg_quality']:.2f} | **{quality_winner}** |")
    report_lines.append(f"| **Citation Rate** | {metrics['nbllm_citation_rate']:.1f}% | N/A | NotebookLLM |")
    report_lines.append(f"| **Librarian Mode Rate** | N/A | {metrics['rm_librarian_mode_rate']:.1f}% | RM |")
    report_lines.append("")

    quality_diff = abs(metrics['nbllm_avg_quality'] - metrics['rm_avg_quality'])
    report_lines.append(f"**Quality Difference**: {quality_diff:.2f} points")
    report_lines.append("")

    # Head-to-head results
    report_lines.append("## Head-to-Head Results")
    report_lines.append("")
    report_lines.append(f"- **NotebookLLM Wins**: {metrics['nbllm_wins']} ({100*metrics['nbllm_wins']/metrics['total_tests']:.1f}%)")
    report_lines.append(f"- **Research Mentor Wins**: {metrics['rm_wins']} ({100*metrics['rm_wins']/metrics['total_tests']:.1f}%)")
    report_lines.append(f"- **Ties**: {metrics['ties']} ({100*metrics['ties']/metrics['total_tests']:.1f}%)")
    report_lines.append("")

    # Overall winner
    report_lines.append("## Overall Assessment")
    report_lines.append("")

    if metrics['nbllm_avg_time'] < metrics['rm_avg_time'] and metrics['nbllm_avg_quality'] > metrics['rm_avg_quality']:
        overall_winner = "NotebookLLM"
        reason = "faster AND higher quality"
    elif metrics['rm_avg_time'] < metrics['nbllm_avg_time'] and metrics['rm_avg_quality'] > metrics['nbllm_avg_quality']:
        overall_winner = "Research Mentor"
        reason = "faster AND higher quality"
    elif metrics['nbllm_wins'] > metrics['rm_wins']:
        overall_winner = "NotebookLLM"
        reason = f"won more head-to-head comparisons ({metrics['nbllm_wins']} vs {metrics['rm_wins']})"
    elif metrics['rm_wins'] > metrics['nbllm_wins']:
        overall_winner = "Research Mentor"
        reason = f"won more head-to-head comparisons ({metrics['rm_wins']} vs {metrics['nbllm_wins']})"
    else:
        overall_winner = "Tie"
        reason = "both systems performed equally well"

    report_lines.append(f"**Overall Winner**: **{overall_winner}**")
    report_lines.append(f"**Reason**: {reason}")
    report_lines.append("")

    # Key insights
    report_lines.append("## Key Insights")
    report_lines.append("")

    if metrics['nbllm_avg_time'] < metrics['rm_avg_time']:
        report_lines.append(f"1. **NotebookLLM is {time_diff_pct:.1f}% faster** on average")
    else:
        report_lines.append(f"1. **Research Mentor is {time_diff_pct:.1f}% faster** on average")

    if metrics['nbllm_avg_quality'] > metrics['rm_avg_quality']:
        report_lines.append(f"2. **NotebookLLM provides higher quality answers** (+{quality_diff:.2f} points)")
    else:
        report_lines.append(f"2. **Research Mentor provides higher quality answers** (+{quality_diff:.2f} points)")

    report_lines.append(f"3. **NotebookLLM cites papers {metrics['nbllm_citation_rate']:.1f}% of the time**")
    report_lines.append(f"4. **Research Mentor uses Librarian mode {metrics['rm_librarian_mode_rate']:.1f}% of the time** (expected: 100% for Known tests)")
    report_lines.append("")

    # Recommendations
    report_lines.append("## Recommendations")
    report_lines.append("")

    if metrics['rm_librarian_mode_rate'] < 70:
        report_lines.append("- **Research Mentor**: Mode detection accuracy is low. Consider lowering similarity threshold from 0.55 to 0.50")

    if metrics['nbllm_citation_rate'] > 80:
        report_lines.append("- **NotebookLLM**: Excellent citation behavior, consistently references source papers")
    elif metrics['nbllm_citation_rate'] < 50:
        report_lines.append("- **NotebookLLM**: Low citation rate, often provides answers without referencing papers")

    if metrics['nbllm_avg_time'] > 2 * metrics['rm_avg_time']:
        report_lines.append("- **NotebookLLM**: Significantly slower than RM, may not be suitable for real-time use cases")

    if metrics['rm_avg_quality'] < 7:
        report_lines.append("- **Research Mentor**: Consider improving RAG retrieval or using a better base LLM")

    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")
    report_lines.append("## Next Steps")
    report_lines.append("")
    report_lines.append("1. Review individual test cases where NotebookLLM significantly outperformed RM")
    report_lines.append("2. Analyze why RM failed to use Librarian mode for Known questions")
    report_lines.append("3. Discuss findings with professor")
    report_lines.append("4. Consider running Gap and Hallucination tests with NotebookLLM")
    report_lines.append("")

    return "\n".join(report_lines)


def main():
    print("Loading comparison data...")
    rows = load_comparison_data()

    print("Calculating metrics...")
    metrics = calculate_metrics(rows)

    if "error" in metrics:
        print(f"\n❌ {metrics['error']}")
        return

    print(f"Analyzed {metrics['total_tests']} test results")

    print("\nGenerating report...")
    report = generate_report(metrics)

    with open(REPORT_FILE, "w") as f:
        f.write(report)

    print(f"✅ Report saved to: {REPORT_FILE}")
    print("\nKey Findings:")
    print(f"  - Average Speed: NotebookLLM {metrics['nbllm_avg_time']:.2f}s vs RM {metrics['rm_avg_time']:.2f}s")
    print(f"  - Average Quality: NotebookLLM {metrics['nbllm_avg_quality']:.2f} vs RM {metrics['rm_avg_quality']:.2f}")
    print(f"  - Winner: NotebookLLM {metrics['nbllm_wins']}, RM {metrics['rm_wins']}, Ties {metrics['ties']}")


if __name__ == "__main__":
    main()
