import csv
import os


class CarBase:

    ix_brand = 1
    ix_seats_count = 2
    ix_photo = 3
    ix_body_whl = 4
    ix_carrying = 5
    ix_extra = 6

    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = float(carrying)

    def get_photo_file_ext(self):
        return os.path.splitext(self.photo_file_name)[1]


class Car(CarBase):

    car_type = "car"

    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)

    @classmethod
    def create_obj(cls, row):
        return cls(row[cls.ix_brand], row[cls.ix_photo], row[cls.ix_carrying], row[cls.ix_seats_count])


class Truck(CarBase):

    car_type = "truck"

    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        try:
            length, width, height = (float(arg) for arg in body_whl.split('x', 2))
        except ValueError:
            length, width, height = float(0), float(0), float(0)
        self.body_length, self.body_width, self.body_height = length, width, height

    def get_body_volume(self):
        return self.body_length * self.body_width * self.body_height

    @classmethod
    def create_obj(cls, row):
        return cls(row[cls.ix_brand], row[cls.ix_photo], row[cls.ix_carrying], row[cls.ix_body_whl])


class SpecMachine(CarBase):

    car_type = "spec_machine"

    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra

    @classmethod
    def create_obj(cls, row):
        return cls(row[cls.ix_brand], row[cls.ix_photo], row[cls.ix_carrying], row[cls.ix_extra])


def get_car_list(csv_filename):
    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)
        car_list = []
        car_dict = {"car": Car, "truck": Truck, "spec_machine": SpecMachine}
        for row in reader:
            try:
                car_type = row[0]
            except IndexError:
                continue

            try:
                car_class = car_dict[car_type]
            except KeyError:
                continue

            try:
                car_list.append(car_class.create_obj(row))
            except (IndexError, ValueError):
                pass
    return car_list


def _main():
    print(get_car_list("coursera_week3_cars.csv"))


if __name__ == "__main__":
    _main()
