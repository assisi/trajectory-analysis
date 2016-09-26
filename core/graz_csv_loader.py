import csv


class GrazCsvLoader(object):
    @staticmethod
    def load_from_csv(filename):
        all_params = GrazParameters()

        with open(filename, 'rb') as f:
            f_reader = csv.reader(f, dialect='excel-tab')

            for row in f_reader:
                if row[0] == 'Frame' or row[0] == 'AVG':
                    continue

                pos_px = (float(row[1]), float(row[2]))
                pos_cm = (float(row[3]), float(row[4]))
                speed_px = None if len(row) <= 5 else float(row[5])
                speed_cm = None if len(row) <= 6 else float(row[6])
                angle = None if len(row) <= 7 else float(row[7])

                all_params.add_new_params(pos_px, pos_cm, speed_px,
                                          speed_cm, angle)

        return all_params


class GrazParameters(object):
    def __init__(self):
        self.x_px = []
        self.y_px = []
        self.x_cm = []
        self.y_cm = []
        self.speed_px_s = []
        self.speed_cm_s = []
        self.angle = []

    def add_new_params(self, pos_px, pos_cm, speed_px, speed_cm, angle):
        self.x_px.append(pos_px[0])
        self.y_px.append(pos_px[1])

        self.x_cm.append(pos_cm[0])
        self.y_cm.append(pos_cm[1])

        self.speed_px_s.append(speed_px)
        self.speed_cm_s.append(speed_cm)
        self.angle.append(angle)
