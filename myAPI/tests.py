from django.test import TestCase
from rest_framework.test import APIClient
from .models import Country
from .serializers import CountrySerializer


# Create your tests here.

class Test_myAPI(TestCase):

    # ------------------------------------ Functional tests ------------------------------------#
    def setUp(self):
        self.client = APIClient()

    def test_user_posts_to_api_and_gets_countries(self):
        test_input_1 = {
            "country_name": "France",
            "spoken_language": "French",
            "population": 67390000
        }

        test_input_2 = {
            "country_name": "Poland",
            "spoken_language": "Polish",
            "population": 37950000
        }

        response = self.client.post('/countries/', test_input_1)
        self.assertEqual(response.status_code, 201)

        response = self.client.post('/countries/', test_input_2)
        self.assertEqual(response.status_code, 201)

        response = self.client.get('/countries/', format='json')

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data[0]["country_name"], "France")
        self.assertEqual(response.data[1]["country_name"], "Poland")

    def test_user_updates_and_deletes(self):
        test_input_1 = {
            "country_name": "France",
            "spoken_language": "French",
            "population": 67390000
        }

        new_data = {"country_name": "France",
                    "spoken_language": 'French',
                    "population": 67000000}

        # user posts initial entry
        response = self.client.post('/countries/', test_input_1)
        self.assertEqual(response.status_code, 201)

        # user updates the entry
        response = self.client.put('/countries/1/', new_data)
        self.assertEqual(response.status_code, 200)

        # user deletes the entry
        response = self.client.delete('/countries/1/')
        self.assertEqual(response.status_code, 204)

    def test_non_existent_endpoint(self):
        response = self.client.get('/countries/2/', format='json')
        self.assertEqual(response.status_code, 404)

    def test_existing_endpoint(self):
        response = self.client.get('/countries/')
        self.assertEqual(response.status_code, 200)

    def test_incorrect_input_format(self):
        invalid_data = {"country_name": "France",
                        "spoken_language": 'French',
                        "population": "frenchies"}
        response = self.client.post('/countries/', invalid_data)

        self.assertEqual(response.status_code, 400)

    # ------------------------------------ Unit tests ------------------------------------#

    def test_model_names(self):
        country_fields = ({"country_name": "France",
                           "spoken_language": "French",
                           "population": 67390000})
        country = Country.objects.create(**country_fields)
        self.assertEqual(country.__str__(), "France")

    def test_field_error(self):
        country_fields = ({"country_name": 'France',
                           "spoken_language": "French",
                           "population": 67390000.2})

        serializer = CountrySerializer(data=country_fields)

        self.assertFalse(serializer.is_valid())

        self.assertEqual(serializer.errors.keys(), {'population'})

    def test_char_field_too_long(self):
        invalid_country_fields = {"country_name": "France",
                                  "spoken_language": "This string is too long aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaad",
                                  "population": 67390000
                                  }

        self.assertRaises(TypeError, Country(invalid_country_fields))
