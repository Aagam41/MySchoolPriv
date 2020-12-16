from django import forms
from .models import *


class PaperEntryForm(forms.ModelForm):
    class Meta:
        model = PaperEntry
        fields = ['paper_entry_name', 'subject', 'paper_type', 'paper_entry_status', 'paper_entry_date']


class MapPaperEntrySubjectChapterForm(forms.ModelForm):
    class Meta:
        model = MapPaperEntrySubjectChapter
        fields = ['paper_entry', 'subject_chapter']


class PaperPatternEntryForm(forms.ModelForm):
    class Meta:
        models = PaperPatternEntry
        fields = ['paper_entry', 'paper_question']


class PaperQuestionForm(forms.ModelForm):
    class Meta:
        models = PaperQuestion
        fields = ['paper_question_text', 'rau_type', 'total_marks', 'chapter_topic']
