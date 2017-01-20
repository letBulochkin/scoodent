from __future__ import unicode_literals

import random

from datetime import date

from scoodent.models import Actor, Genre, Customer, Disk, Rental


def get_random_date(start, end):
    """Random date from datetime.date range.

    :param datetime.date start: left limit
    :param datetime.date end: right limit
    :return: random datetime.date from range
    """

    return date.fromordinal(random.randint(start.toordinal(), end.toordinal()))


def random_name():
    """Return random name.

    :rtype: str
    """

    return random.choice([
        "Жожа", "Авраам", "Вильгельм", "Азис", "Абстракт", "Иона", "Варган",
        "Бенжамин", "Анубис-гер-Метрономус", "Пётр", "Вектор", "Виктор",
        "Перегей"
    ])


def random_surname():
    """Return random surname.

    :rtype: str
    """

    return random.choice([
        "Фурриганов", "Пертрпровский-Розмаринов", "Керамич", "Копыч", "Бро",
        "Ганзинский", "Исмаислёв", "Ашмак-вэчетыре", "Амазонов", "Березовский",
        "Петров"
    ])


def random_birthdate():
    """Random approximate birthdate.

    :return: random datetime.date from range
    """

    start = date(1992, 1, 1)
    end = date(2000, 12, 30)

    return get_random_date(start, end)


def random_pass_date():
    """Return random date for report."""

    ranges = [
        ((2014, 12, 15), (2014, 12, 28)),
        ((2015, 5, 15), (2015, 5, 28)),
        ((2015, 12, 15), (2015, 12, 28)),
        ((2016, 5, 15), (2016, 5, 28)),
        ((2016, 12, 15), (2016, 12, 28)),
    ]

    start, end = random.choice(ranges)
    return get_random_date(date(*start), date(*end))


def random_address():
    """Random address.

    :rtype: str
    """

    return random.choice([
        "г. Москва, ул. Лобызова, д. {0} кв. {1}",
        "г. Москва, ул. Морозная, д. {0} кв. {1}",
        "г. Москва, ул. Маршалла Алигнмента, д. {0} кв. {1}",
        "г. Москва, ул. Первая-2, д. {0} кв. {1}",
        "г. Москва, ул. Новомосковское ш., д. {0} кв. {1}",
        "г. Пенза, ул. Ленина, д. {0} кв. {1}",
        "г. Октябрьск, ул. Ленина, д. {0} кв. {1}",
        "г. Кемерово, ул. Ленина, д. {0} кв. {1}",
        "г. Окск-на-волге, ул. Ленина, д. {0} кв. {1}",
        "г. Дзержинск, ул. Ленина, д. {0} кв. {1}",
        "г. Краснознаменск, ул. Дообедова, д. {0} кв. {1}",
        "г. Москва, ул. 5-й квартал Капотни, д. {0} кв. {1}",
        ]).format(random.randint(1, 160), random.randint(1, 200))


def random_phone():
    return "+7({0}){1}-{2}-{3}".format(
        random.randint(900, 999),
        random.randint(100, 999),
        random.randint(10, 99),
        random.randint(10, 99))


def random_customer():
    customer = {
        "phone_number": random_phone(),
        "name": random_name(),
        "passport": random_passport(),
        "ordered": bool(random.getrandbits(1)),
    }


def random_disk():
    disk = {
        "title": 
    }

'''
def random_student():
    student = {
        "name": random_name(),
        "surname": random_surname(),
        "birthdate": random_birthdate(),
        "address": random_address(),
        "phone": random_phone(),
        "parents_phone": random_phone(),
        "school": "Школа №{0}".format(random.randint(1, 1800)),
    }
    enter_date = student["birthdate"]
    enter_date.replace(year=enter_date.year + 17, month=9, day=1)
    student["enter_date"] = enter_date

    return student
'''
'''
def random_report():
    """Return random report."""

    return {
        "mark": random.randint(2, 6),
        "mark_date": random_pass_date(),
        "report_type": random.choice(TReportEnum._fields),
    }
'''


def random_passport():
    """Return random passport data."""

    return "{0}_{1}".format(
        random.randint(1000,9999), random.randint(100000, 499999))


def random_film_name():
    """Return film names tuple"""

    return (
        "Yost and Sons",
        "Nikolaus-Leannon",
        "Rutherford LLC",
        "Boyer, Sauer and Gerlach",
        "Marks-Emard",
        "Kuphal, Leannon and Bayer",
        "Kuhic, Kilback and Weimann",
        "Blanda, Von and Hoeger",
        "Farrell-Dach",
        "Parker Group",
        "Crist-Cronin",
        "Kunze-Mitchell",
        "Zboncak-Nader",
        "Breitenberg LLC",
        "Spencer-Moore",
        "Schimmel Inc",
        "Bins Group",
        "Kulas and Sons",
        "Durgan Inc",
        "Jacobs Group",
        "Gibson LLC",
        "Murray-Huel",
        "Mayert-Gibson",
        "Hilll Inc",
        "Mosciski-Wyman",
        "Huels and Sons",
        "Raynor-Wolf",
        "Yost, Vandervort and Smith",
        "Powlowski Inc",
        "Koss, Murray and Kihn",
        "Hickle LLC",
        "Renner Group",
        "Jenkins, Prohaska and Heidenreich",
        "O'Keefe, Sipes and Schneider",
        "Wehner-Russel",
        "Wilderman-Balistreri",
        "Hoeger and Sons",
        "Kreiger-Dietrich",
        "Abshire LLC",
        "Metz Inc",
        "Mayert Group",
        "Hodkiewicz and Sons",
        "Smith, Crist and Kreiger",
        "Torphy-Wilkinson",
        "Cartwright, Feest and Moen",
        "Hirthe, Wintheiser and Weissnat",
        "Renner-Abernathy",
        "Gibson and Sons",
        "Schaefer-Okuneva",
        "Bogisich Inc",
    )

def get_actors():
    """Return actors."""

    return (
        "Julia Richardson",
        "Justin Lane",
        "Terry Robinson",
        "Andrea Morgan",
        "Pamela Morga",
        "Jean Russell",
        "Nicole Arnold",
        "Sharon Simmons",
        "Keith Watkins",
        "Anna Howell",
        "Fred Robertson",
        "Jane Walker",
        "Robin Webb",
        "Christina Carpenter",
        "Larry Hawkins",
        "Larry Burns",
        "Barbara Spencer",
        "Beverly Kennedy",
        "Jose Stanley",
        "Kevin Garcia",
    )


def get_genres():
    """Return genres."""

    return (
        "thriller",
        "comedy",
        "documentary",
        "romance",
        "series",
        "sci-fi",
        "fantasy",
        "detective",
        "historical",
        "musicle",
    )


def generate_data(session):
    """Generate testing data and fill DB via session."""

    customers = (random_customer() for _ in range(20))

    genres = list(map(lambda it: Genre(film_genre=it), get_genres()))
    session.add_all(genres)
    session.commit()

    actors = list(map(lambda it: Actor(name=it), get_actors()))
    session.add_all(actors)
    session.commit()

    for customer in customers:
        # get random foreign keys

        customer = Customer(**customer)

        disk["customer"] = customer

        group = random.choice(groups)
        student["student_group"] = group

        report = random_report()
        report["student"] = student
        report["discipline"] = random.choice(disciplines)

        session.add(Report(**report))
        session.add(student)

    session.commit()
