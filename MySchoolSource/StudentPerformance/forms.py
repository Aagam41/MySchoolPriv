from django import forms

import models as models


class PaperEntryForm(forms.ModelForm):
    class Meta:
        model = models.PaperEntry
        fields = ['paper_entry_name', 'subject', 'paper_type', 'paper_entry_status', 'paper_entry_date']


class MapPaperEntrySubjectChapterForm(forms.ModelForm):
    class Meta:
        model = models.MapPaperEntrySubjectChapter
        fields = ['paper_entry', 'subject_chapter']


class PaperPatternEntryForm(forms.ModelForm):
    class Meta:
        models = models.PaperPatternEntry
        fields = ['paper_entry', 'paper_question']
