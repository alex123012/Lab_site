from django import forms


class FileFieldForm(forms.Form):
    title = forms.CharField(max_length=50, label='Title for Graph', required=False)
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),
                                 label='Upload file(s)')
