from django import forms


class FileFieldForm(forms.Form):
    title = forms.CharField(max_length=50, label='Title for alignments divided by spaces', required=False)
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),
                                 label='Upload file(s)')
    similarity = forms.CharField(max_length=128, label='Proteins to similarity count in alignments divided by spaces',
                                 required=False)
