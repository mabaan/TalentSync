"""
Domain model classes for a small TalentSync demo.

These classes represent a job description, a candidate resume,
and the result of matching a candidate to a job.
"""


class JobDescription:
    def __init__(self, job_id, title, required_skills):
        self.job_id = job_id
        self.title = title
        self.required_skills = required_skills

    def normalized_skills(self):
        """Return lowercase skills without extra whitespace."""
        result = []
        for skill in self.required_skills:
            result.append(skill.strip().lower())
        return result


class CandidateResume:
    def __init__(self, candidate_id, name, skills):
        self.candidate_id = candidate_id
        self.name = name
        self.skills = skills

    def normalized_skills(self):
        """Return lowercase skills without extra whitespace."""
        result = []
        for skill in self.skills:
            result.append(skill.strip().lower())
        return result


class MatchResult:
    def __init__(self, candidate_name, job_title, match_score, matched_skills, missing_skills):
        self.candidate_name = candidate_name
        self.job_title = job_title
        self.match_score = match_score
        self.matched_skills = matched_skills
        self.missing_skills = missing_skills

    def pretty_print(self):
        """
        Print a simple human readable summary of the result.
        """
        print("Candidate:", self.candidate_name)
        print("Job title:", self.job_title)
        print("Match score:", round(self.match_score, 1), "%")
        if self.matched_skills:
            print("Matched skills:", ", ".join(self.matched_skills))
        else:
            print("Matched skills: None")
        if self.missing_skills:
            print("Missing skills:", ", ".join(self.missing_skills))
        else:
            print("Missing skills: None")
        print("------------------------------")
