import matplotlib.pyplot as plt


class PlotCorrelation(object):
    @classmethod
    def plot_results(cls, diff, f, title='value', x='frame', save=False):
        fig, ax = plt.subplots()

        ax.plot(diff)
        ax.set_title('Difference in ' + title)
        ax.set_xlabel(x)
        ax.set_ylabel('diff')
        ax.grid()

        if save:
            fig.savefig(f + '.png')
            plt.close(fig)

    @classmethod
    def plot_paths_1d(cls, graz, ctrax, f, title='paths', y='', save=False):
        fig, ax = plt.subplots()

        ax.plot(graz, 'r', label='graz_parameters')
        ax.plot(ctrax, 'b', label='ctrax [1 FPS]')
        ax.set_title('Difference in ' + title)
        ax.set_xlabel('frame')
        ax.set_ylabel(y)
        lgd = ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),
                        fancybox=True, shadow=True, ncol=2)
        ax.grid()

        if save:
            fig.savefig(f + '.png', bbox_extra_artists=(lgd,),
                        bbox_inches='tight')
            plt.close(fig)

    @classmethod
    def plot_paths_2d(cls, graz_x, graz_y, ctrax_x, ctrax_y, f, title='paths',
                      a='', lab='', save=False):
        fig, ax = plt.subplots()

        ax.plot(graz_x, graz_y, 'r', label='graz_params')
        ax.plot(ctrax_x, ctrax_y, 'b', label='ctrax ' + lab)
        ax.set_title('Difference in ' + title + a)
        ax.set_xlabel('x_px [px]')
        ax.set_ylabel('y_px [px]')
        lgd = ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),
                        fancybox=True, shadow=True, ncol=2)
        ax.grid()

        if save:
            fig.savefig(f + '.png', bbox_extra_artists=(lgd,),
                        bbox_inches='tight')
            plt.close(fig)

    @classmethod
    def plot_paths_3d(cls, graz_x, graz_y, ctrax_x, ctrax_y, c_1_x, c_1_y, f,
                      title='paths', a='', save=False):
        fig, ax = plt.subplots()

        ax.plot(graz_x, graz_y, 'r', label='graz_params')
        ax.plot(ctrax_x, ctrax_y, 'b', label='ctrax [25 FPS]')
        ax.plot(c_1_x, c_1_y, 'g', label='ctrax [1 FPS]')
        ax.set_title('Difference in ' + title + a)
        ax.set_xlabel('x_px [px]')
        ax.set_ylabel('y_px [px]')
        lgd = ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),
                        fancybox=True, shadow=True, ncol=3)
        ax.grid()

        if save:
            fig.savefig(f + '.png', bbox_extra_artists=(lgd,),
                        bbox_inches='tight')
            plt.close(fig)
