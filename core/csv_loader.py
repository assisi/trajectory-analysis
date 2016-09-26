import csv

from bee import Bee


class CSVLoader(object):
    @staticmethod
    def load_from_csv(filename, bee_num=None):
        frame = 0
        bees = {}
        with open(filename, 'rb') as f:
            f_reader = csv.reader(f)

            for row in f_reader:
                for idx in range(0, len(row), 6):
                    id = int(float(row[idx]))

                    if id < 0:
                        continue

                    if bee_num == 1:
                        name = 'bee_0'
                    else:
                        name = 'bee_' + str(id)

                    path = (float(row[idx + 1]), float(row[idx + 2]))
                    bee_len = float(row[idx + 3])
                    bee_width = float(row[idx + 4])
                    bee_angle = float(row[idx + 5])

                    if name not in bees.keys():
                        bees[name] = Bee(name, path, bee_len, bee_width,
                                         bee_angle, frame)

                    else:
                        bees[name].refresh_params(path, bee_len, bee_width,
                                                  bee_angle)

                    if bee_num == 1:
                        break

                frame += 1

            for key, value in bees.iteritems():
                value.calculate_end_frame()

        return bees
