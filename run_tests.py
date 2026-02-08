"""
Test Runner for Research Mentor System

Runs all test cases and generates evaluation reports.
Compares Research Mentor outputs against Baseline LLM using Judge agent.

Usage:
    python run_tests.py                    # Run all tests
    python run_tests.py --category known   # Run only known tests
    python run_tests.py --limit 5          # Run first 5 tests per category
    python run_tests.py --test-id gap_001  # Run a specific test
"""

import argparse
import json
import time
from datetime import datetime
from typing import List, Dict, Any

from research_mentor import ResearchMentorSystem
from test_cases import KNOWN_TESTS, GAP_TESTS, HALLUCINATION_TESTS, get_test_summary


def run_single_test(mentor: ResearchMentorSystem, test_case: dict, verbose: bool = True) -> dict:
    """Run a single test case and return results."""
    test_id = test_case["id"]
    query = test_case["query"]
    expected_mode = test_case["expected_mode"]

    if verbose:
        print(f"\n{'='*60}")
        print(f"Running: {test_id}")
        print(f"Query: {query[:60]}...")
        print(f"Expected Mode: {expected_mode}")
        print('='*60)

    start_time = time.time()

    try:
        # Run the evaluation
        results = mentor.process_query_for_eval(query)
        elapsed_time = time.time() - start_time

        # Determine if mode matched expectation
        actual_mode = results["mode"]
        mode_correct = (
            (expected_mode == "librarian" and actual_mode == "librarian") or
            (expected_mode == "research_mentor" and actual_mode == "research_mentor")
        )

        # Build result
        test_result = {
            "test_id": test_id,
            "query": query,
            "expected_mode": expected_mode,
            "actual_mode": actual_mode,
            "mode_correct": mode_correct,
            "similarity": results["similarity"],
            "confidence": results["confidence"],
            "judge_winner": results["judge_result"]["winner"],
            "judge_score_baseline": results["judge_result"]["score_baseline"],
            "judge_score_rm": results["judge_result"]["score_rm"],
            "judge_reasoning": results["judge_result"]["reasoning"],
            "elapsed_time": elapsed_time,
            "status": "success",
            "error": None
        }

        if verbose:
            print(f"  Actual Mode: {actual_mode} ({'CORRECT' if mode_correct else 'WRONG'})")
            print(f"  Similarity: {results['similarity']:.4f}")
            print(f"  Judge: {results['judge_result']['winner'].upper()} wins")
            print(f"  Scores: Baseline={results['judge_result']['score_baseline']}, RM={results['judge_result']['score_rm']}")
            print(f"  Time: {elapsed_time:.2f}s")

    except Exception as e:
        elapsed_time = time.time() - start_time
        test_result = {
            "test_id": test_id,
            "query": query,
            "expected_mode": expected_mode,
            "actual_mode": None,
            "mode_correct": False,
            "similarity": None,
            "confidence": None,
            "judge_winner": None,
            "judge_score_baseline": None,
            "judge_score_rm": None,
            "judge_reasoning": None,
            "elapsed_time": elapsed_time,
            "status": "error",
            "error": str(e)
        }
        if verbose:
            print(f"  ERROR: {e}")

    return test_result


def run_test_category(
    mentor: ResearchMentorSystem,
    tests: List[dict],
    category_name: str,
    limit: int = None,
    verbose: bool = True
) -> List[dict]:
    """Run all tests in a category."""
    if limit:
        tests = tests[:limit]

    print(f"\n{'#'*60}")
    print(f"# Running {category_name.upper()} Tests ({len(tests)} tests)")
    print('#'*60)

    results = []
    for i, test in enumerate(tests, 1):
        print(f"\n[{i}/{len(tests)}]", end="")
        result = run_single_test(mentor, test, verbose)
        results.append(result)

        # Small delay to avoid rate limiting
        time.sleep(1)

    return results


def generate_report(results: Dict[str, List[dict]], output_file: str = None) -> str:
    """Generate a summary report of test results."""
    report_lines = []
    report_lines.append("="*70)
    report_lines.append("RESEARCH MENTOR TEST REPORT")
    report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("="*70)

    total_tests = 0
    total_correct_mode = 0
    total_rm_wins = 0
    total_baseline_wins = 0
    total_ties = 0

    for category, category_results in results.items():
        report_lines.append(f"\n## {category.upper()} TESTS")
        report_lines.append("-"*50)

        correct_mode = sum(1 for r in category_results if r["mode_correct"])
        rm_wins = sum(1 for r in category_results if r["judge_winner"] == "research_mentor")
        baseline_wins = sum(1 for r in category_results if r["judge_winner"] == "baseline")
        ties = sum(1 for r in category_results if r["judge_winner"] == "tie")
        errors = sum(1 for r in category_results if r["status"] == "error")

        total_tests += len(category_results)
        total_correct_mode += correct_mode
        total_rm_wins += rm_wins
        total_baseline_wins += baseline_wins
        total_ties += ties

        report_lines.append(f"Total Tests: {len(category_results)}")
        report_lines.append(f"Mode Detection Accuracy: {correct_mode}/{len(category_results)} ({100*correct_mode/len(category_results):.1f}%)")
        report_lines.append(f"Judge Results:")
        report_lines.append(f"  - Research Mentor Wins: {rm_wins}")
        report_lines.append(f"  - Baseline Wins: {baseline_wins}")
        report_lines.append(f"  - Ties: {ties}")
        if errors > 0:
            report_lines.append(f"  - Errors: {errors}")

        # Average scores
        valid_results = [r for r in category_results if r["status"] == "success"]
        if valid_results:
            avg_rm_score = sum(r["judge_score_rm"] for r in valid_results) / len(valid_results)
            avg_baseline_score = sum(r["judge_score_baseline"] for r in valid_results) / len(valid_results)
            report_lines.append(f"Average Scores:")
            report_lines.append(f"  - Research Mentor: {avg_rm_score:.2f}/10")
            report_lines.append(f"  - Baseline: {avg_baseline_score:.2f}/10")

    # Overall summary
    report_lines.append("\n" + "="*70)
    report_lines.append("OVERALL SUMMARY")
    report_lines.append("="*70)
    report_lines.append(f"Total Tests Run: {total_tests}")
    report_lines.append(f"Mode Detection Accuracy: {total_correct_mode}/{total_tests} ({100*total_correct_mode/total_tests:.1f}%)")
    report_lines.append(f"Judge Results:")
    report_lines.append(f"  - Research Mentor Wins: {total_rm_wins} ({100*total_rm_wins/total_tests:.1f}%)")
    report_lines.append(f"  - Baseline Wins: {total_baseline_wins} ({100*total_baseline_wins/total_tests:.1f}%)")
    report_lines.append(f"  - Ties: {total_ties} ({100*total_ties/total_tests:.1f}%)")

    report = "\n".join(report_lines)

    if output_file:
        with open(output_file, "w") as f:
            f.write(report)
        print(f"\nReport saved to: {output_file}")

    return report


def main():
    parser = argparse.ArgumentParser(description="Run Research Mentor tests")
    parser.add_argument("--category", choices=["known", "gap", "hallucination", "all"],
                       default="all", help="Test category to run")
    parser.add_argument("--limit", type=int, default=None,
                       help="Limit number of tests per category")
    parser.add_argument("--test-id", type=str, default=None,
                       help="Run a specific test by ID")
    parser.add_argument("--output", type=str, default=None,
                       help="Output file for report")
    parser.add_argument("--quiet", action="store_true",
                       help="Reduce output verbosity")
    parser.add_argument("--save-results", type=str, default=None,
                       help="Save detailed results to JSON file")

    args = parser.parse_args()

    # Initialize system
    print("Initializing Research Mentor System...")
    mentor = ResearchMentorSystem()
    mentor.ingest_dummy_data()

    # Show test summary
    summary = get_test_summary()
    print(f"\nTest Cases Available:")
    print(f"  Known: {summary['known_count']}")
    print(f"  Gap: {summary['gap_count']}")
    print(f"  Hallucination: {summary['hallucination_count']}")
    print(f"  Total: {summary['total']}")

    results = {}

    # Run specific test
    if args.test_id:
        from test_cases import get_test_by_id
        test = get_test_by_id(args.test_id)
        if test:
            result = run_single_test(mentor, test, verbose=not args.quiet)
            results["single"] = [result]
        else:
            print(f"Test ID '{args.test_id}' not found.")
            return
    else:
        # Run by category
        if args.category in ["known", "all"]:
            results["known"] = run_test_category(
                mentor, KNOWN_TESTS, "known", args.limit, not args.quiet
            )

        if args.category in ["gap", "all"]:
            results["gap"] = run_test_category(
                mentor, GAP_TESTS, "gap", args.limit, not args.quiet
            )

        if args.category in ["hallucination", "all"]:
            results["hallucination"] = run_test_category(
                mentor, HALLUCINATION_TESTS, "hallucination", args.limit, not args.quiet
            )

    # Generate report
    if results:
        report = generate_report(results, args.output)
        print("\n" + report)

    # Save detailed results
    if args.save_results:
        with open(args.save_results, "w") as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\nDetailed results saved to: {args.save_results}")


if __name__ == "__main__":
    main()
