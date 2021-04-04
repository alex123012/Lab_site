from django import forms


class FileFieldForm(forms.Form):
    title = forms.CharField(max_length=50, label='Title for Graph', required=False)
    min_time = forms.IntegerField(max_value=90, min_value=0, label='Min time for graph')
    max_time = forms.IntegerField(max_value=90, min_value=0, label='Max time for graph')
    format = forms.ChoiceField(choices=(('png', "PNG"),
                                        ('svg', "SVG"),
                                        ('jpeg', 'JPG'),
                                        ('jpg', 'JPEG')))
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),
                                 label='Upload file(s)')
