from django.shortcuts import render
# Create your views here.
from .models import TblSubject, Standard, SubjectChapter, ChapterTopic


def subject_entry(request):
    if request.method == "POST":
        sub_name = request.POST['sub_name']
        std = request.POST['std']
        r_credit = request.POST['r_credit']
        ak_credit = request.POST['ak_credit']
        u_credit = request.POST['u_credit']
        s_credit = request.POST['s_credit']

        try:
            std = Standard.objects.get(standard=std)
            subject = TblSubject.objects.create_subject(subject_name=sub_name, std=std, r_credit=r_credit,
                                                        ak_credit=ak_credit, u_credit=u_credit, s_credit=s_credit)

        except:
            print('Some Error occured')
        return render(request, 'entry.html')
    else:
        return render(request, 'entry.html')


def chapter_entry(request):
    if request.method == "POST":
        sub = request.POST['subject']
        chap_id = request.POST['ch_id']
        chap_name = request.POST['ch_name']
        ch_r_credit = request.POST['ch_r_credit']
        ch_ak_credit = request.POST['ch_ak_credit']
        ch_u_credit = request.POST['ch_u_credit']
        ch_credit = request.POST['ch_credit']

        try:
            sub = TblSubject.objects.get(subject_name=sub)
            chapter = SubjectChapter.objects.create_chapter(subject=sub, ch_id=chap_id, ch_name=chap_name,
                                                            ch_r_credit=ch_r_credit,
                                                            ch_ak_credit=ch_ak_credit, ch_u_credit=ch_u_credit,
                                                            ch_credit=ch_credit)

        except:
            print('Some Error occured')
        return render(request, 'entry.html')
    else:
        return render(request, 'entry.html')


def topic_entry(request):
    if request.method == "POST":
        chap = request.POST['chapter']
        t_id = request.POST['t_id']
        t_name = request.POST['t_name']

        try:
            chap = SubjectChapter.objects.get(chapter_name=chap)
            topic = ChapterTopic.objects.create_topic(Subject_chapter=chap,topic_id=t_id,topic_name=t_name)
        except:
            print("Some error !!!")
        return render(request, 'entry.html')
    else:
        return render(request, 'entry.html')


def subject_delete(request):
    if request.method == "POST":
        sub_name = request.POST['sub_name']
        std = request.POST['std']

        try:
            std = Standard.objects.get(standard=std)
            subject = TblSubject.objects.delete_subject(subject_name=sub_name, std=std)
        except:
            print('Some Error occurred')
        return render(request, 'entry.html')
    else:
        return render(request, 'entry.html')


def chapter_delete(request):
    if request.method == "POST":
        chap_name = request.POST['chap_name']
        sub = request.POST['sub']

        try:
            sub = TblSubject.objects.get(subject_name=sub)
            chapter = SubjectChapter.objects.delete_chapter(chapter_name=chap_name,sub=sub)
        except:
            print('Some Error occurred')
        return render(request, 'entry.html')
    else:
        return render(request, 'entry.html')


def topic_delete(request):
    if request.method == 'POST':
        t_name = request.POST['topic_name']
        chap = request.POST['chap']

        try:
            chap = SubjectChapter.objects.get(chapter_name=chap)
            topic = ChapterTopic.objects.delete_topic(topic_name=t_name,chap=chap)
        except:
            print('Some Error occurred')
        return render(request, 'entry.html')
    else:
        return render(request, 'entry.html')


def subject_update(request):
    if request.method == "POST":
        sub_id = request.POST['sub_id']
        sub_name = request.POST['sub_name']
        std = request.POST['std']
        r_credit = request.POST['r_credit']
        ak_credit = request.POST['ak_credit']
        u_credit = request.POST['u_credit']
        s_credit = request.POST['s_credit']

        try:
            std = Standard.objects.get(standard=std)
            subject = TblSubject.objects.update_subject(s_id=sub_id, subject_name=sub_name, std=std, r_credit=r_credit,
                                                        ak_credit=ak_credit, u_credit=u_credit, s_credit=s_credit)

        except:
            print('Some Error occured')
        return render(request, 'entry.html')
    else:
        return render(request, 'entry.html')


def chapter_update(request):
    if request.method == "POST":
        s_c_id = request.POST['s_c_id']
        ch_id = request.POST['ch_id']
        ch_name = request.POST['ch_name']
        ch_r_credit = request.POST['ch_r_credit']
        ch_ak_credit = request.POST['ch_ak_credit']
        ch_u_credit = request.POST['ch_u_credit']
        ch_credit = request.POST['ch_credit']

        try:
            chap = SubjectChapter.objects.update_chapter(s_c_id=s_c_id, ch_id=ch_id, ch_name=ch_name,
                                                         ch_r_credit=ch_r_credit, ch_ak_credit=ch_ak_credit,
                                                         ch_u_credit=ch_u_credit, ch_credit=ch_credit)

        except:
            print("Error occurred !!")
        return render(request, 'entry.html')
    else:
        return render(request, 'entry.html')

def topic_update(request):
    if request.method == "POST":
        c_t_id = request.POST['c_t_id']
        t_id = request.POST['t_id']
        t_name = request.POST['t_name']

        try:
            topic = ChapterTopic.objects.update_topic(c_t_id=c_t_id, t_id=t_id, t_name=t_name)

        except:
            print('Some Error occurred')
        return render(request, 'entry.html')
    else:
        return render(request, 'entry.html')

