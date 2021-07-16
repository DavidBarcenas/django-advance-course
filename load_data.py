import csv
from cride.circles.models.circles import Circle

def import_csv(csv_filename):
    with open(csv_filename, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            circle = Circle(**row)
            circle.is_limited = bool(int(circle.members_limit))
            circle.save()
            print(circle.name)


if __name__ == '__main__':
    import_csv('circles.csv')