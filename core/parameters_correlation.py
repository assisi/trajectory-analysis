import numpy as np

import matplotlib.pyplot as plt

from plot_correlation import PlotCorrelation


class ParametersCorrelation(object):
    MAX_OFFSET = 25

    @classmethod
    def run(cls, graz_params, ctrax_params, save_dir):
        save = save_dir
        file = str(save_dir) + '/'
        solutions = {}
        sol_mse = []

        # find solution with min error by changing the offset
        for ofst in xrange(cls.MAX_OFFSET):
            name = 'Solution_{}'.format(ofst)
            tmp = CorrelationSolutions(graz_params, ctrax_params, ofst)

            solutions[name] = tmp
            sol_mse.append((name, tmp.mse))

        min_sol_name = min(sol_mse, key=lambda x: x[1])[0]
        best_sol = solutions[min_sol_name]
        print '\n{}\nBest offset : {}'.format('=' * 40, best_sol.ofst)

        # plot mse distribution over offset values
        mse_val = [val for _, val in sol_mse]
        # cls.__plot_results(mse_val, 'mse', 'offset')

        # plot differences in x_px in px values
        diff_x = best_sol.get_x_px_diff()
        PlotCorrelation.plot_results(diff_x, f=file + 'diff_x_px',
                                     title='x_px [px]', save=save)

        # plot differences in y_px in px values
        diff_y = best_sol.get_y_px_diff()
        PlotCorrelation.plot_results(diff_y, f=file + 'diff_y_px',
                                     title='y_px [px]', save=save)

        # plot differences in x_px in cm values
        diff_x_cm = best_sol.get_x_cm_diff()
        PlotCorrelation.plot_results(diff_x_cm, f=file + 'diff_x_cm',
                                     title='x_px [cm]', save=save)

        # plot differences in y_px in cm values
        diff_y_cm = best_sol.get_y_cm_diff()
        PlotCorrelation.plot_results(diff_y_cm, f=file + 'diff_y_cm',
                                     title='y_px [cm]', save=save)

        # plot differences in speed [px/s] calculation
        diff_speed_px = best_sol.get_speed_px_s_diff()
        PlotCorrelation.plot_results(diff_speed_px, f=file + 'diff_speed_px_s',
                                     title='speed [px/s]', save=save)

        # plot differences in speed [cm/s] calculation
        diff_speed_cm = best_sol.get_speed_cm_s_diff()
        PlotCorrelation.plot_results(diff_speed_cm, f=file + 'diff_speed_cm_s',
                                     title='speed [cm/s]', save=save)

        # plot differences in angle calculation
        diff_angle = best_sol.angle_graz_style_diff()
        PlotCorrelation.plot_results(diff_angle, f=file + 'diff_angle',
                                     title='angle', save=save)

        # plot paths for x_px [px]
        last_idx = len(best_sol.g_params.x_px) * 25
        c_path_x = best_sol.c_params.x_px[:last_idx:25]
        PlotCorrelation.plot_paths_1d(best_sol.g_params.x_px, c_path_x,
                                      f=file + 'paths_x', y='x_px [px]', save=save)

        # plot paths for y_px [px]
        last_idx = len(best_sol.g_params.y_px) * 25
        c_path_y = 576 - np.array(best_sol.c_params.y_px[:last_idx:25])
        PlotCorrelation.plot_paths_1d(best_sol.g_params.y_px, c_path_y,
                                      f=file + 'paths_y', y='y_px [px]', save=save)

        # plot paths for x_px and y_px [px]
        PlotCorrelation.plot_paths_2d(best_sol.g_params.x_px,
                                      best_sol.g_params.y_px,
                                      c_path_x, c_path_y, f=file + 'x_y_px',
                                      lab='[1 FPS]', save=save)

        # plot paths for x_px and y_px [px] ctrax-25 FPS
        y_params = 576 - np.array(best_sol.c_params.y_px)
        PlotCorrelation.plot_paths_2d(best_sol.g_params.x_px,
                                      best_sol.g_params.y_px,
                                      best_sol.c_params.x_px, y_params,
                                      f=file + 'x_y_px_25_fps', lab='[25 FPS]',
                                      save=save)

        # plot paths for x_px and y_px [px] in 30 framse ctrax 1 FPS
        PlotCorrelation.plot_paths_2d(best_sol.g_params.x_px[:30],
                                      best_sol.g_params.y_px[:30],
                                      c_path_x[:30], c_path_y[:30],
                                      f=file + 'x_y_30_frames',
                                      a=' [30 frames]',
                                      lab='[1 FPS]', save=save)

        # plot paths for x_px and y_px [px] ctrax 25 FPS
        y_params = 576 - np.array(best_sol.c_params.y_px[:30 * 25])
        PlotCorrelation.plot_paths_2d(best_sol.g_params.x_px[:30],
                                      best_sol.g_params.y_px[:30],
                                      best_sol.c_params.x_px[:30 * 25],
                                      y_params, f=file + 'x_y_30_frames_25_fps',
                                      a=' [30 frames]', lab='[25 FPS]',
                                      save=save)

        # plot paths for x_px and y_px [px] ctrax 1 FPS and 25 FPS
        y_params_25 = 576 - np.array(best_sol.c_params.y_px[:30 * 25])
        PlotCorrelation.plot_paths_3d(best_sol.g_params.x_px[:30],
                                      best_sol.g_params.y_px[:30],
                                      best_sol.c_params.x_px[:30 * 25],
                                      y_params_25, c_path_x[:30], c_path_y[:30],
                                      f=file + 'x_y_30_frames_1_25_fps',
                                      a=' [30 frames]', save=save)

        # plot paths for x_px and y_px [px] ctrax 1 FPS and 25 FPS
        y_params_25 = 576 - np.array(best_sol.c_params.y_px)
        PlotCorrelation.plot_paths_3d(best_sol.g_params.x_px,
                                      best_sol.g_params.y_px,
                                      best_sol.c_params.x_px,
                                      y_params_25, c_path_x, c_path_y,
                                      f=file + 'x_y_px_1_25_fps', save=save)

        plt.show()
        return best_sol


class CorrelationSolutions(object):
    CTRAX_FPS = 25

    def __init__(self, graz_params, ctrax_params, offset):
        self.g_params = graz_params
        self.c_params = ctrax_params
        self.ofst = offset
        self.mse = self.__calc_mse()

    def __min_square_error(self, params1, params2):
        return ((params1 - params2) ** 2).mean()

    def __calc_mse(self):
        last_idx = len(self.g_params.x_px) * self.CTRAX_FPS + self.ofst

        graz_x = np.array(self.g_params.x_px)
        ctrax_x = np.array(self.c_params.x_px[self.ofst:last_idx:self.CTRAX_FPS])

        return self.__min_square_error(graz_x, ctrax_x)

    def get_x_px_diff(self):
        last_idx = len(self.g_params.x_px) * self.CTRAX_FPS + self.ofst

        graz_x = np.array(self.g_params.x_px)
        ctrax_x = np.around(
            np.array(self.c_params.x_px[self.ofst:last_idx:self.CTRAX_FPS]))

        return graz_x - ctrax_x

    def get_x_cm_diff(self):
        last_idx = len(self.g_params.x_cm) * self.CTRAX_FPS + self.ofst

        graz_x = np.array(self.g_params.x_cm)
        c_x_px = np.array(self.c_params.x_px[self.ofst:last_idx:self.CTRAX_FPS])

        ctrax_x_cm = ((c_x_px - 132) * 60) / 512

        return graz_x - ctrax_x_cm

    def get_y_px_diff(self):
        last_idx = len(self.g_params.y_px) * self.CTRAX_FPS + self.ofst

        graz_y = np.array(self.g_params.y_px)

        ctrax_y_inv = np.array(
            self.c_params.y_px[self.ofst:last_idx:self.CTRAX_FPS])
        ctrax_y = 576 - ctrax_y_inv

        return graz_y - ctrax_y

    def get_y_cm_diff(self):
        last_idx = len(self.g_params.y_px) * self.CTRAX_FPS + self.ofst

        graz_y = np.array(self.g_params.y_cm)

        ctrax_y_inv = np.array(
            self.c_params.y_px[self.ofst:last_idx:self.CTRAX_FPS])
        c_y_px = 576 - ctrax_y_inv

        ctrax_y_cm = ((c_y_px - 10) * 60) / 544

        return graz_y - ctrax_y_cm

    def get_speed_px_s_diff(self):
        last_idx = len(self.g_params.y_px) * self.CTRAX_FPS + self.ofst

        graz_speed = np.array(self.g_params.speed_px_s)

        ctrax_x = np.around(
            np.array(self.c_params.x_px[self.ofst:last_idx:self.CTRAX_FPS]))
        ctrax_y_inv = np.array(
            self.c_params.y_px[self.ofst:last_idx:self.CTRAX_FPS])
        ctrax_y = 576 - ctrax_y_inv

        c_speed = np.sqrt((ctrax_x[1:] - ctrax_x[:-1]) ** 2 +
                          (ctrax_y[1:] - ctrax_y[:-1]) ** 2)

        return graz_speed[1:] - c_speed

    def get_speed_cm_s_diff(self):
        last_idx = len(self.g_params.x_cm) * self.CTRAX_FPS + self.ofst

        graz_speed = np.array(self.g_params.speed_cm_s)

        c_x_px = np.array(self.c_params.x_px[self.ofst:last_idx:self.CTRAX_FPS])
        ctrax_y_inv = np.array(
            self.c_params.y_px[self.ofst:last_idx:self.CTRAX_FPS])
        c_y_px = 576 - ctrax_y_inv

        ctrax_x_cm = ((c_x_px - 132) * 60) / 512
        ctrax_y_cm = ((c_y_px - 10) * 60) / 544

        c_speed = np.sqrt((ctrax_x_cm[1:] - ctrax_x_cm[:-1]) ** 2 +
                          (ctrax_y_cm[1:] - ctrax_y_cm[:-1]) ** 2)

        return graz_speed[1:] - c_speed

    def __calc_triangle_side(self, x_0, x_1, y_0, y_1):
        return np.sqrt((x_0 - x_1) ** 2 + (y_0 - y_1) ** 2)

    def __is_right(self, ax, ay, bx, by, cx, cy):
        tmp = (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)
        # print '\n'.join('{}'.format(x_px) for x_px in tmp < 0)
        return tmp < 0

    def __calc_graz_angle(self, x_params, y_params):
        # calculate the angle in triangle abc, where c is the
        # side across desired angle value

        a = self.__calc_triangle_side(x_params[0:-2], x_params[1:-1],
                                      y_params[0:-2], y_params[1:-1])

        b = self.__calc_triangle_side(x_params[1:-1], x_params[2:],
                                      y_params[1:-1], y_params[2:])

        c = self.__calc_triangle_side(x_params[0:-2], x_params[2:],
                                      y_params[0:-2], y_params[2:])

        plus_dir = self.__is_right(x_params[0:-2], y_params[0:-2],
                                   x_params[1:-1], y_params[1:-1],
                                   x_params[2:], y_params[2:])

        gama_rad = np.arccos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b))
        gama_deg = np.degrees(gama_rad) - 180
        gama = np.where(plus_dir, gama_deg * (-1), gama_deg)
        return gama

    def angle_graz_style_diff(self):
        last_idx = len(self.g_params.x_px) * self.CTRAX_FPS + self.ofst

        graz_x = np.array(self.g_params.x_px)
        ctrax_x = np.array(self.c_params.x_px[self.ofst:last_idx:self.CTRAX_FPS])

        graz_y = np.array(self.g_params.y_px)

        ctrax_y_inv = np.around(
            np.array(self.c_params.y_px[self.ofst:last_idx:self.CTRAX_FPS]))
        ctrax_y = np.around(576 - ctrax_y_inv)

        ctrax_angle = self.__calc_graz_angle(ctrax_x, ctrax_y)

        # print ctrax_x
        # print ctrax_y
        angle_ctrax = np.degrees(
            np.array(self.c_params.bee_angle[self.ofst::25]))
        # print ctrax_angle
        # return np.array(self.g_params.angle[2:]), ctrax_angle
        # print '\n'.join(['{} -> {} -- {}'.format(*x) for x in
        #                  zip(np.array(self.g_params.angle[2:]), ctrax_angle,
        #                      angle_ctrax)])
        #
        # print self.__min_square_error(np.array(self.g_params.angle[2:]),
        #                               ctrax_angle)
        return np.array(self.g_params.angle[2:]) - ctrax_angle
