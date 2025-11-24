"""
Matching logic for the TalentSync demo.

This file contains the TalentSyncAnalyzer class and a helper function
that builds a sample in memory data set.
"""

from talentsync_models import JobDescription, CandidateResume, MatchResult


class TalentSyncAnalyzer:
    """
    A small simple version of TalentSync. Ideally this would use Large Language Models and be backed by a database

    This class covers:
    - Job description upload (store a new job with required skills).
    - Resume upload (add candidate resumes).
    - Matching and feedback (generate match scores, matched and missing skills).
    """

    def __init__(self):
        self.jobs = {}
        self.candidates = {}

    # Job methods

    def add_job_description(self, job):
        """
        Store a job description in memory.
        """
        self.jobs[job.job_id] = job

    def get_job(self, job_id):
        if job_id not in self.jobs:
            raise ValueError("No job found with id " + str(job_id))
        return self.jobs[job_id]

    # Resume methods

    def add_candidate_resume(self, resume):
        """
        Store a candidate resume in memory.
        """
        self.candidates[resume.candidate_id] = resume

    # Matching

    def analyze_for_job(self, job_id):
        """
        Compare all stored candidate resumes against one job description.
        """
        job = self.get_job(job_id)
        job_skills = set(job.normalized_skills())

        if not job_skills:
            raise ValueError("Job has no required skills defined.")

        results = []

        for candidate in self.candidates.values():
            candidate_skills = set(candidate.normalized_skills())

            matched = sorted(job_skills.intersection(candidate_skills))
            missing = sorted(job_skills.difference(candidate_skills))

            # Score = percentage of required skills the candidate has
            score = (float(len(matched)) / float(len(job_skills))) * 100.0

            result = MatchResult(
                candidate_name=candidate.name,
                job_title=job.title,
                match_score=score,
                matched_skills=matched,
                missing_skills=missing,
            )
            results.append(result)

        # Sort by score, highest first
        results.sort(key=lambda r: r.match_score, reverse=True)
        return results

    def analyze_resume_without_job(self, candidate_id):
        """
        Very simple feedback if the applicant uploads a resume
        without a job description.
        """
        if candidate_id not in self.candidates:
            raise ValueError("No candidate found with id " + str(candidate_id))

        resume = self.candidates[candidate_id]
        num_skills = len(resume.skills)

        if num_skills == 0:
            return (
                "Resume for " + resume.name + " has no listed skills. "
                "Please add at least some technical or soft skills."
            )
        elif num_skills < 4:
            return (
                "Resume for " + resume.name + " lists only " + str(num_skills) + " skills. "
                "Consider adding more relevant skills for better ATS visibility."
            )
        else:
            return (
                "Resume for " + resume.name + " already lists " + str(num_skills) + " skills. "
                "You can now compare it with a specific job description for targeted feedback."
            )


def build_sample_analyzer():
    """
    Helper function that builds one analyzer instance with
    one job and four candidate resumes. This object is reused
    by the tests and by the manual demo.
    """
    analyzer = TalentSyncAnalyzer()

    data_scientist_job = JobDescription(
        job_id=1,
        title="Junior Data Scientist",
        required_skills=[
            "Python",
            "Pandas",
            "Machine Learning",
            "SQL",
            "Data Visualization",
        ],
    )
    analyzer.add_job_description(data_scientist_job)

    # Strong match candidate
    alice = CandidateResume(
        candidate_id=101,
        name="Alice",
        skills=[
            "Python",
            "Machine Learning",
            "SQL",
            "Pandas",
            "Data Visualization",
            "Statistics",
        ],
    )
    analyzer.add_candidate_resume(alice)

    # Partial match candidate
    bob = CandidateResume(
        candidate_id=102,
        name="Bob",
        skills=[
            "Python",
            "Excel",
            "Data Visualization",
            "Communication",
        ],
    )
    analyzer.add_candidate_resume(bob)

    # Very low match candidate
    charlie = CandidateResume(
        candidate_id=103,
        name="Charlie",
        skills=[
            "Java",
            "Spring Boot",
            "Docker",
        ],
    )
    analyzer.add_candidate_resume(charlie)

    # Candidate with no skills to test feedback messages
    dana = CandidateResume(
        candidate_id=104,
        name="Dana",
        skills=[],
    )
    analyzer.add_candidate_resume(dana)

    return analyzer
