from django.contrib.auth.models import User
from django.core.exceptions import *

from MySchoolHome import models as msh
from StudentPerformance import models as sp
from StudentPerformancePrediction import models as spp

from aagam_packages.terminal_yoda.terminal_yoda import *


def get_myschool_user(username: str):
    """
    Fetches the MySchool_User from the User model in contrib.auth.models.
    :param username: String that uniquely identifies the User
    :return: Returns MySchoolUser object
    """
    auth_user = User.objects.get(username=username)
    user = msh.MySchoolUser.objects.get(auth_user=auth_user)
    return user


def get_user_section(user: msh.MySchoolUser):
    """
    Gets the StandardSection of MySchoolUser
    :param user: MySchoolUser object
    :return: Returning StandardSection object
    """
    standard_section = sp.MapMySchoolUserStandardSection.objects.filter(myschool_user=user)
    return standard_section


def get_subject(standard_section):
    """
    Gets subject of MyschoolUser object
    :param standard_section: It is a StandardSection object
    :return: Returns list of TblSubjects in a standard
    """
    subject_list = sp.Tblsubject.objects.filter(standard=standard_section[0:1])
    return subject_list


def get_prediction_data(user: msh.MySchoolUser):
    """
    Gets StudentEfficacy object based on the MySchoolUser provided.
    :param user: MySchoolUser object
    :return: Returns StudentEfficacy object of MySchoolUser
    """
    try:
        prediction_data = spp.StudentEfficacy.objects.get(student=user)
        return prediction_data
    except ObjectDoesNotExist:
        print(yoda_saberize(YodaSaberColor.RED) + "")



def marks(user, paper_pattern_entry):
    """
    Sums of the marks obtained field in the map_myschool_user_paper_pattern_question.
    :param user: MySchoolUser object
    :param paper_pattern_entry: PaperPatternEntry object
    :return: Returns a integer
    """
    paper_pattern_entry = get_paper_pattern_entry(paper_pattern_entry)
    paper_pattern_question = get_paper_pattern_question(paper_pattern_entry)
    user_marks = get_map_student_question(user, paper_pattern_question)
    sum = [x + x for x in user_marks.marks_obtained]
    return sum