import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from io import StringIO


def changer(x):

    """For bad unicode in Windows"""

    if not isinstance(x, (float, int)):
        return float(''.join([i for i in x if i.isdigit() or i == '.']))
    return x


class ChromoFigure:

    """ Export RAW-file chromatogram to picture graph"""

    def __init__(self):
        self.format_list = ['png', 'svg', 'jpg', 'jpeg', 'pdf']
        self.min_time = 15
        self.max_time = 45
        self.title = ''
        self.format = 'png'
        self.temp_file = ''

    def settings(self):

        """Check your settings"""

        print(f'min_time = {self.min_time}')
        print(f'max_time = {self.max_time}')
        print(f'Title = {self.title}' if self.title else 'No title')
        print(f'format = {self.format}')
        print(f'Tempfile directory = {self.temp_file}')

    def __file_normalize(self, file):

        """decoding and changing file for normal python executing"""

        tmp = ""
        for chunk in file.chunks():
            tmp += chunk.decode().replace(',', '.')

        self.temp_file = StringIO(tmp)

    def __file_read(self):

        # Variable for easy debug
        time = "Time (min)"
        value = "Value (mAU)"

        # Reading new file
        df_ref = pd.DataFrame(pd.read_csv(self.temp_file,
                                          sep='\t',
                                          skiprows=42))

        # Crutch for bad unidecoding
        if df_ref[value].dtype != 'float' or df_ref[time].dtype != 'float':
            df_ref[value] = df_ref[value].apply(changer)
            df_ref[time] = df_ref[time].apply(changer)

        # cutting off unnecessary time (slip and flushing)
        df = df_ref[df_ref[time] >= self.min_time][
            [time, value]].astype('float')
        df = df[df[time] <= self.max_time]

        x = df[time].tolist()
        y = df[value].tolist()
        return x, y

    def export(self, file):

        """Exporting chromatogramm into picture with your settings"""

        self.__file_normalize(file)

        # Coordinates for graph)
        x, y = self.__file_read()

        # Variables for more readable code
        miny = min(y)
        maxy = max(y)
        rnd = round(maxy * 0.1, -1)

        # Initializing graph
        fig, ax = plt.subplots(1, 1,
                               figsize=(15, 10),
                               tight_layout=True)

        # Graph customization
        ax.set_title(self.title,
                     fontsize=25,
                     color='black',
                     pad=10)
        ax.set_xlabel('Time (min)',
                      fontsize=25,
                      color='black',
                      labelpad=10)
        ax.set_ylabel('Absorbance (mAU)',
                      fontsize=25,
                      color='black',
                      labelpad=10)
        try:
            ax.yaxis.set_ticks(
                np.arange(round(miny, -2), round(maxy, -2) + 100, rnd)
            )
        except ZeroDivisionError:
            ax.yaxis.set_ticks(
                np.arange(round(miny, -2), round(maxy, -2) + 100)
            )
        ax.xaxis.set_ticks(
            np.arange(self.min_time, self.max_time + 1, 5)
        )

        ax.yaxis.set_tick_params(labelsize=22)
        ax.xaxis.set_tick_params(labelsize=22)

        ax.axis([self.min_time - 1,
                self.max_time + 1,
                miny - rnd / 2,
                maxy + rnd / 2])

        # Plotting
        plt.plot(x, y, '-',
                 color='black',
                 markersize=1,
                 label='VIS_1')

        return fig, ax


def main():
    fig, ax = ChromoFigure().export('test.txt')
    plt.show()


if __name__ == '__main__':
    main()
