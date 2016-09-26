import csv
import itertools
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np


class DistributionAssessor(object):
    @classmethod
    def all_paths(cls, dict_params):
        # plot all paths that bees travelled in one plot
        if type(dict_params) is not dict:
            raise TypeError('The values to Distribution Assessor should be '
                            'passed as a dictionary')

        fig, ax = plt.subplots()
        ax.grid()
        for val in dict_params.values():
            ax.plot(val.x_px, val.y_px)

        plt.show()

    @classmethod
    def turn_probability(cls, bees):
        # histogram of all angles registered in csv

        # minimal significant angle
        MSA = 0.2

        angles = list(itertools.chain.from_iterable(b.bee_angle for b in bees.values()))

        # classify angles as right (R), left (L) or straight, count them
        R = sum(map(lambda x: x > MSA, angles))
        L = sum(map(lambda x: x < -MSA, angles))

        # calculate probability for each direction to occur
        p_L = L / float(len(angles))
        p_R = R / float(len(angles))
        p_S = (len(angles) - R - L) / float(len(angles))

        print '{:-^50}'.format('TURN PROBABILITY')
        print 'Probability to turn left: {:>20} %'.format(p_L * 100)
        print 'Probability to turn right: {:>19} %'.format(p_R * 100)
        print 'Probability to go straight: {:>18} %'.format(p_S * 100)
        print '-' * 50
        print '\n'

        plt.hist(angles, 50, normed=1)
        plt.title('Angles distribution')
        plt.xlabel('Angle [rad]')
        plt.ylabel('Probability')
        plt.grid()
        plt.show()

    @classmethod
    def stop_probability(cls, bees):
        # probability that the bee is not moving

        # minimum significant speed
        MSS = 0.1

        # count in how many frames the bee is not moving
        speed = list(itertools.chain.from_iterable(b.speed() for b in bees.values()))
        stop = sum(map(lambda x: x < MSS, speed))

        p_STOP = stop / float(len(speed))

        print '{:-^50}'.format('STOP PROBABILITY')
        print 'Probability to stop: {:>20} %'.format(p_STOP * 100)
        print '-' * 50
        print '\n'

        # plt.hist(speed)
        # plt.axis([-1, 60, 0, 0.08])
        # plt.grid()
        # plt.show()

    @classmethod
    def bee_meeting(cls, filename):
        # probability of bees having a meeting

        # radius multiplier, determines how big is the bee personal space
        R_MULTIPLIER = 3

        # all meetings, stored as
        # ('name_1', 'name_2') : [<frames in which they meet>]
        COLLISIONS = defaultdict(list)

        # initialization
        DIS_IDX = 0  # stores the exact value of the radius
        frame_idx = 0  # stores the number of frame we are currently examining
        bees_in_arena = []  # store num bees that are detected in each row

        with open(filename, 'rb') as f:
            f_reader = csv.reader(f)

            # check every row in csv for detection of meetings
            for row in f_reader:
                tmp_bees = []
                frame_idx += 1
                num_bees = 0

                # store bees found in that frame in tmp_bees as (<name>, x_y)
                for idx in range(0, len(row), 6):
                    id = int(float(row[idx]))

                    if id < 0:
                        continue
                    num_bees += 1
                    DIS_IDX = max(0, R_MULTIPLIER * float(row[idx + 3]))

                    name = 'bee_' + str(id)
                    x_y = (float(row[idx + 1]), float(row[idx + 2]))
                    tmp_bees.append((name, x_y))
                bees_in_arena.append(num_bees)

                # check which bees are meeting and store them in COLLISIONS
                for i in xrange(len(tmp_bees)):
                    for j in xrange(i + 1, len(tmp_bees)):
                        dist = np.sqrt(
                            (tmp_bees[i][1][0] - tmp_bees[j][1][0])**2 +
                            (tmp_bees[i][1][1] - tmp_bees[j][1][1])**2)

                        if dist <= DIS_IDX:
                            names = (tmp_bees[i][0], tmp_bees[j][0])
                            COLLISIONS[names].append(frame_idx)

        # calculate how many real bees are in the arena
        avg_bees = sum(bees_in_arena) / len(bees_in_arena)

        # sum many frames with collisions there are
        sum_col = sum(len(v) for v in COLLISIONS.values())

        area = frame_idx * (avg_bees - 1) * avg_bees / 2
        p_C = sum_col / float(area)

        print '{:-^50}'.format('MEETING PROBABILITY')
        print 'Probability of collision: {:>20} %'.format(p_C * 100)
        print '-' * 50

        return COLLISIONS

    @classmethod
    def communication_time(cls, collisions):
        # calculates what is the time that bees spend in meeting

        # max number of frames distance to be still considered one meeting
        MAX_GAP = 3
        MIN_FRAMES = 2

        # stores all communication times
        comm_time = []

        for val in collisions.values():
            l_idx = val[0]
            last_frame = val[0]

            # divide to clusters that are part of the same meeting
            for frame_num in val[1:]:
                if frame_num <= last_frame + MAX_GAP:
                    last_frame = frame_num
                else:
                    tmp_time = last_frame - l_idx
                    if tmp_time < MIN_FRAMES:
                        l_idx = frame_num
                        last_frame = frame_num
                    else:
                        comm_time.append(last_frame - l_idx)
                        l_idx = frame_num
                        last_frame = frame_num
            tmp_time = last_frame - l_idx
            if tmp_time >= MIN_FRAMES:
                comm_time.append(last_frame - l_idx)

        plt.hist(comm_time, 20, normed=1)
        plt.title('Communication Time')
        plt.xlabel('Duration [frames]')
        plt.ylabel('Probability')
        plt.grid()
        plt.show()
