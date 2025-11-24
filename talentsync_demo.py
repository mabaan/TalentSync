"""
The other files are:
- talentsync_models.py: domain classes (JobDescription, CandidateResume, MatchResult)
- talentsync_analyzer.py: matching logic and sample data
"""

from talentsync_analyzer import TalentSyncAnalyzer, build_sample_analyzer


def run_tests():
    """
    Small set of assert based tests for the matching logic.

    These tests check:
    - scores for strong, partial and weak matches
    - ranking order by score
    - feedback messages when there is no job description
    """
    analyzer = build_sample_analyzer()
    results = analyzer.analyze_for_job(1)

    alice_result, bob_result, charlie_result, dana_result = results

    # Alice should be a perfect match
    assert alice_result.match_score == 100.0
    assert len(alice_result.matched_skills) == 5
    assert len(alice_result.missing_skills) == 0

    # Bob only has 2 out of 5 skills
    assert bob_result.match_score == 40.0
    assert len(bob_result.matched_skills) == 2
    assert len(bob_result.missing_skills) == 3

    # Charlie and Dana have no matching skills
    assert charlie_result.match_score == 0.0
    assert len(charlie_result.matched_skills) == 0
    assert len(charlie_result.missing_skills) == 5

    assert dana_result.match_score == 0.0
    assert len(dana_result.matched_skills) == 0
    assert len(dana_result.missing_skills) == 5

    # Make sure Alice is ranked first
    assert results[0].candidate_name == "Alice"

    # Check feedback without a job description
    feedback_dana = analyzer.analyze_resume_without_job(104)
    assert "no listed skills" in feedback_dana

    feedback_alice = analyzer.analyze_resume_without_job(101)
    assert "already lists" in feedback_alice

    print("All tests passed successfully.")


def run_demo():
    """
    Run a small console demo that shows the test data and the
    match results in a simple, human readable way.
    """
    analyzer = build_sample_analyzer()
    results = analyzer.analyze_for_job(1)

    print("TalentSync sample run")
    print("Matching four candidates to one job")
    print()

    job = analyzer.get_job(1)
    print("Job title:", job.title)
    print("Required skills:", ", ".join(job.required_skills))
    print()

    print("Ranked candidates for this job")
    print("------------------------------")

    for result in results:
        result.pretty_print()

    print()
    print("Example of resume feedback without a job description:")
    print(analyzer.analyze_resume_without_job(101))


if __name__ == "__main__":
    # Run tests first to make sure everything works
    run_tests()
    print()
    run_demo()
