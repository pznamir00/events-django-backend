from django.contrib.gis.geos import Point
from mixer.backend.django import mixer


def pytest_configure(config):
    mixer.register(
        "core.Event",
        location=lambda: Point(
            float(mixer.faker.latitude()),
            float(mixer.faker.longitude()),
        ),
    )
