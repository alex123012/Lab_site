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
        filename = check_status(request)  # Import file name if exists (after POST)
        form = self.form_class()
        if filename:
            return render(request, os.path.join("LKalign", "index.html"),
                          {'form': form, 'filename': filename})

        return render(request, os.path.join("LKalign", "index.html"), {'form': form})

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)  # Getting form for template
        files = request.FILES.getlist('file_field')

        resp = request.POST
        if form.is_valid():
            matrix = os.path.join('LKalign', 'static', 'matrix.txt')
            names = resp['title'].split()
            proteins = request.POST['similarity'].split()
            for file, name, sim_search in zip(files, names, proteins):
                try:

                    filename = os.path.join(request.COOKIES['sessionid'], f'{name}.aln')
                    filename = os.path.join('LKalign', 'static', 'media', filename)
                    with open(filename, 'w') as f:
                        tmp = ''
                        for chunk in file.chunks():
                            tmp += chunk.decode()
                        f.write(tmp)

                    cmd = ClustalwCommandline('clustalw', infile=filename, gapext=0.5, align=True,
                                              gapopen=10, matrix=matrix, pwmatrix=matrix,
                                              type='PROTEIN', outfile=filename, quiet=True,
                                              terminalgap=10
                                              )
                    cmd()
                    alignment = AlignIO.read(filename, "clustal")
                    reference = [(str(i.seq), i.id) for i in alignment if sim_search in i.id][0]
                    max_len = max([len(i.id) + 1 for i in alignment])
                    if sim_search:
                        alignment = ''.join([str(i.id) + ' ' * (
                                max_len - len(i.id)) + str(i.seq) + similarity(
                        i.seq, reference[0], i.id, reference[1]) + '\n' for i in alignment])
                    else:
                        alignment = ''.join([str(i.id) + ' ' * (
                                max_len - len(i.id)) + str(i.seq) + '\n' for i in alignment])
                except Exception:
                    return redirect(request.path)

                with open(filename, 'w') as f:
                    f.write(alignment)
                os.remove(filename.replace('aln', 'dnd'))  # remove tree
                filename = os.path.join(request.COOKIES['sessionid'], f'{name}.aln')
                list_names = request.session.get('filenames', )
                request.session['filenames'] = (list_names + [filename]) if list_names else [filename]

        return redirect(request.path)


def check_status(request):

    if not request.COOKIES.get('sessionid', ) or not request.COOKIES['sessionid']:  # set session cookie
        request.session.create()
        request.COOKIES['sessionid'] = request.session.session_key

    path = os.path.join('LKalign', 'static', 'media')
    if not os.path.exists(path):  # Create new folders for storing graphs
        os.mkdir(path)
        request.session['filenames'] = []

    path = os.path.join(path, request.COOKIES.get('sessionid', ))
    if not os.path.exists(path):
        os.mkdir(path)
        request.session['filenames'] = []

    return request.session['filenames']


def similarity(x, y, inid, reference):
    d = {'G': 0, 'A': 0, 'V': 0, 'L': 0, 'I': 0, 'P': 0, 'M': 0, 'F': 0, 'W': 0,
         'S': 1, 'T': 1, 'C': 1, 'Y': 1, 'N': 1, 'Q': 1,
         'D': 2, 'E': 2,
         'K': 3, 'R': 3, 'H': 3, '-': 4}
    res = 0
    if inid in reference:
        return f'  {len(y)}/{len(x)}'
    for i, j in enumerate(x):
        # if j == '-' or y[i] == '-':
        #     continue
        if d[j] == d[y[i]]:
            res += 1
    return f'  {res}/{len(x)}'
