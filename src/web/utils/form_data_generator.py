import json
import random

from faker import Faker

from src.web.pages.automation_practice_form import Genders, Hobbies


class RandomFormData:
    def __init__(self):
        self._faker = Faker()
        self._hobbies = []
        self._states_and_cities = {
            "NCR": ["Delhi", "Gurgaon", "Noida"],
            "Uttar Pradesh": ["Agra", "Merrut", "Lucknow"],
        }

        self.first_name = self._faker.first_name()
        self.last_name = self._faker.last_name()
        self.email = self._faker.email()
        self.gender = random.choice([Genders.MALE, Genders.FEMALE, Genders.OTHER])
        self.mobile_phone = self._faker.random_number(digits=10, fix_len=True)
        self.date_of_birth = self._faker.date_of_birth(minimum_age=18, maximum_age=90).strftime('%d %B %Y')
        self.hobbies = random.sample(
            [Hobbies.SPORTS, Hobbies.READING, Hobbies.MUSIC],
            k=random.randint(1, 3))
        self.current_address = self._faker.address()
        self.state = random.choice(list(self._states_and_cities.keys()))
        self.city = random.choice(self._states_and_cities[self.state])

    def to_dict(self):
        return {
            "Student Name": f'{self.first_name} {self.last_name}',
            "Student Email": self.email,
            "Gender": self.gender.name.capitalize(),
            "Mobile": self.mobile_phone,
            # "Date of Birth": self.date_of_birth,
            "Hobbies": ', '.join([i.name.capitalize() for i in self.hobbies]),
            # "Address": self.current_address,
            # "state": self.state,
            # "city": self.city,
        }

    def __str__(self):
        return json.dumps(self.to_dict(), indent=4)
