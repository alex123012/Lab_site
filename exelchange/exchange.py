# import matplotlib.pyplot as plt
import pandas as pd
import os


class DataFrame(pd.DataFrame):

    def __init__(self, x=None):
        super().__init__(self.__initial_start(x))
        # try:
        #     self.set_index('Unnamed: 0', inplace=True)
        # except KeyError:
        #     pass

    def __initial_start(self, x):

        if isinstance(x, (list, tuple)):
            return {'x': x[0], 'y': x[1]}

        else:
            _, file_extension = os.path.splitext(x)
            try:
                print(file_extension)
                if file_extension == '.csv':
                    print(pd.read_csv(x))
                    return pd.read_csv(x)
                elif file_extension == '.tsv':
                    return pd.read_csv(x, sep='\t')
                else:
                    return pd.read_exel(x)
            except:
                print('Cant open file')
                return 1

        # elif x is None:
        #     try:
        #         xaxis = list(map(float, input('Enter x (abscissa) axis values divided by spaces: ').split()))
        #         yaxis = list(map(float, input('Enter y (ordinate) axis values divided by spaces: ').split()))
        #     except ValueError:
        #         'Invalid value(s)'
        #
        #     return {'x': xaxis, 'y': yaxis}
        #
