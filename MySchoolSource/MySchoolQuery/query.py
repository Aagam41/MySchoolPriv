from django.contrib.auth.models import User

import pandas as pd

from MySchoolHome import models as msh


def get_myschool_user(username: str):
    """
    Fetches the MySchool_User from the User model in contrib.auth.models.
    :param username: String that uniquely identifies the User
    :return: Returns MySchoolUser object
    """
    auth_user = User.objects.get(username=username)
    user = msh.MySchoolUser.objects.get(auth_user=auth_user)
    return user


def marks(user, paper_pattern_entry):
    """
    Sums the marks obtained field in the map_myschool_user_paper_pattern_question.
    :param user: MySchoolUser object
    :param paper_pattern_entry: PaperPatternEntry object
    :return: Returns a integer
    """
    paper_pattern_entry = get_paper_pattern_entry(paper_pattern_entry)
    paper_pattern_question = get_paper_pattern_question(paper_pattern_entry)
    user_marks = get_map_student_question(user, paper_pattern_question)
    sum = [x + x for x in user_marks.marks_obtained]
    return sum