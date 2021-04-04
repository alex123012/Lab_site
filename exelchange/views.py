from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from .forms import ExelForm
# from .exchange import DataFrame
import matplotlib.pyplot as plt
from scipy import stats
import os


class FileFieldView(FormView):

    form_class = ExelForm  # Upload from from forms.py for template
    template_name = os.path.join("exelchange", "index.html")  # Basic template

    def get(self, request, **kwargs):
        form = self.form_class()
        check(request)
        path = os.path.join('exelchange', 'static', 'media')
        path = os.path.join(path, request.COOKIES.get('sessionid', ), 'graph.png')

        cook = os.path.join(request.COOKIES['sessionid'], 'graph.png') if os.path.exists(path) else None

        return render(request, os.path.join("exelchange", "index.html"), {'form': form,
                                                                          'img': cook,
                                                                          'result': request.session.get('result', '')},)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)  # Getting form for template
        if form.is_valid():
            x = list(map(float, request.POST['x_coord'].split()))
            y = list(map(float, request.POST['y_coord'].split()))
            appr = stats.linregress(x, y)
            a = round(appr.slope, 4)
            b = round(appr.intercept, 4)
            y1 = [a * i + b for i in x]
            label = f'y = {a}*x {b}' if b < 0 else f'{a}*x + {b}'

            result = [((float(i) - b) / a, float(i)) for i in request.POST['absorb'].split()]
            request.session['result'] = result
            fig = plt.figure(figsize=(15, 10))
            ax = fig.add_subplot(111)
            ax.set_title('Approximation curve',
                         fontsize=25,
                         color='black',
                         pad=10)
            ax.plot(x, y, label='initial', color='black')
            ax.plot(x, y1, label=label, color='orange')
            for i, j in result:
                ax.plot(i, j, 'o', color='green', markersize=20)

            plt.legend(fontsize='xx-large')
            plt.grid()
            check(request)
            fig.savefig(os.path.join('exelchange', 'static', 'media', request.COOKIES['sessionid'], 'graph.png'))
            # print(request.COOKIES['result'])
        return redirect(request.path)


def check(request):
    if not request.COOKIES.get('sessionid', '') or not request.COOKIES['sessionid']:  # set session cookie
        request.session.create()
        request.COOKIES['sessionid'] = request.session.session_key

    path = os.path.join('exelchange', 'static')
    if not os.path.exists(path):
        os.mkdir(path)
    path = os.path.join(path, 'media')
    if not os.path.exists(path):
        os.mkdir(path)
    path = os.path.join(path, request.COOKIES.get('sessionid', ))
    if not os.path.exists(path):
        os.mkdir(path)
