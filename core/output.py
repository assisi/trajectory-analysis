import os
import matplotlib.pyplot as plt


class Output(object):

    @classmethod
    def __plot_path(cls, bee_inst, sx, sy, idx, folder=None, show=False, f_name='b', rdp=''):
        fig, ax = plt.subplots()
        ax.plot(bee_inst.x_px, bee_inst.y_px, label='ctrax results')
        ax.plot(sx, sy, 'r--')
        ax.plot(sx[idx], sy[idx], 'ro', markersize=3, label='turning points')
        # ax.set_title(bee_inst.id)
        ax.set_title('Tolerance {}'.format(rdp))
        ax.set_xlabel('x_px [px]')
        ax.set_ylabel('y_px [px]')
        lgd = ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),
                        fancybox=True, shadow=True, ncol=2, numpoints=1)
        plt.grid()

        if folder:
            out_name = folder + '/' + f_name + '.png'
            fig.savefig(out_name, bbox_extra_artists=(lgd,), bbox_inches='tight')
            plt.close(fig)

        if show:
            plt.show()

    @classmethod
    def dump_to_folder(cls, bees, folder):

        # make folder if it doesn't exist
        if not os.path.isdir(folder):
            os.makedirs(folder)

        # save all bee figures in folder
        for key, val in bees.iteritems():
            for rdp in [5, 10, 20, 40, 60, 80]:
                val.RDP_TOLERANCE = rdp
                sx, sy, idx = val.filter_path_rdp()
                cls.__plot_path(val, sx, sy, idx, folder=folder,
                                f_name='tolerance_{}'.format(rdp),
                                rdp='{}'.format(rdp))

    @classmethod
    def dump_bees_to_folder(cls, bees, folder):

        # make folder if it doesn't exist
        if not os.path.isdir(folder):
            os.makedirs(folder)

        # save all bee figures in folder
        for key, val in bees.iteritems():
            rdp = 5
            val.RDP_TOLERANCE = rdp
            sx, sy, idx = val.filter_path_rdp()
            cls.__plot_path(val, sx, sy, idx, folder=folder,
                            f_name='{}_tolerance_{}'.format(val.id, rdp),
                            rdp='')

    @classmethod
    def show_bee_path(cls, bee_inst):
        sx, sy, idx = bee_inst.filter_path_rdp()
        cls.__plot_path(bee_inst, sx, sy, idx, show=True)

