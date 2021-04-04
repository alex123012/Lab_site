from Bio.Align.Applications import ClustalwCommandline
from Bio import AlignIO
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from .forms import FileFieldForm
import os


class FileFieldView(FormView):

    form_class = FileFieldForm  # Upload from from forms.py for template
    template_name = os.path.join("LKalign", "index.html")  # Basic template

    def get(self, request, **kwargs):
        form = self.form_class()
        check(request)
        path = os.path.join('LKalign', 'static', 'media')
        path = os.path.join(path, request.COOKIES.get('sessionid', ), 'graph.png')

        cook = os.path.join(request.COOKIES['sessionid'], 'graph.png') if os.path.exists(path) else None

        return render(request, os.path.join("LKalign", "index.html"), {'form': form,
                                                                       'img': cook,
                                                                       'result': request.session.get('result', '')},)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)  # Getting form for template
        files = request.FILES.getlist('file_field')
        resp = request.POST
        if form.is_valid():
            matrix = os.path.join('LKalign', 'static', 'matrix.txt')
            for file in files:
                # x = 'Only_blast/apl_lynx2_blast.fasta'
                filename = os.path.join(request.COOKIES['sessionid'], f"{str(resp['title'])}.aln")
                filename = os.path.join('LKalign', 'static', 'media', filename)
                out = os.path.join('static', 'media', request.COOKIES.get('sessionid', ), filename)
                cmd = ClustalwCommandline('clustalw', infile=file, gapext=0.5, align=True,
                                          gapopen=10, matrix=matrix,
                                          pwmatrix=matrix,
                                          type='PROTEIN', outfile=out, quiet=True)
                cmd()
                alignment = AlignIO.read(out, "clustal")
                alignment = ''.join([str(i.id) + '\t' + str(i.seq) + '\n' for i in alignment])
                # os.remove('align.aln')
                with open(filename, 'w') as f:
                    f.write(alignment)
        return redirect(request.path)


def check(request):
    if not request.COOKIES.get('sessionid', '') or not request.COOKIES['sessionid']:  # set session cookie
        request.session.create()
        request.COOKIES['sessionid'] = request.session.session_key

    path = os.path.join('LKalign', 'static')
    if not os.path.exists(path):
        os.mkdir(path)
    path = os.path.join(path, 'media')
    if not os.path.exists(path):
        os.mkdir(path)
    path = os.path.join(path, request.COOKIES.get('sessionid', ))
    if not os.path.exists(path):
        os.mkdir(path)
