import os
import tempfile
import datetime


class File:

    def __init__(self, file_path):
        self.file_path = file_path
        self.cur_position = 0

        if not os.path.exists(file_path):
            with open(file_path, 'w'):
                pass

    def write(self, content):
        with open(self.file_path, 'w') as f:
            f.write(content)

    def read(self):
        with open(self.file_path, 'r') as f:
            return f.read()

    def __add__(self, other):
        new_path = os.path.join(tempfile.gettempdir(), datetime.datetime.today().strftime("%Y%m%d%H%M%S"))
        new_file = File(new_path)
        new_file.write(self.read() + other.read())
        return new_file

    def __iter__(self):
        return self

    def __next__(self):
        with open(self.file_path, 'r') as f:
            f.seek(self.cur_position)
            line = f.readline()
            if not line:
                self.cur_position = 0
                raise StopIteration('EOF')
            self.cur_position = f.tell()
            return line

    def __str__(self):
        return self.file_path
