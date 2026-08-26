import csv

from catalog_app.models import Good


def load_data() -> list[tuple[str, str]]:
    result = []
    with open("certs.csv", "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            result.append((row[0], row[1]))
        return result


def load_serts() -> None:
    for data in load_data():
        good = Good.objects.filter(code=data[0]).first()
        if good:
            good.registry_link = data[1]
            good.save()


if __name__ == "__main__":
    load_serts()
