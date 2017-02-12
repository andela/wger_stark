# This file is part of wger Workout Manager.
#
# wger Workout Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wger Workout Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License

import logging

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from wger.core.tests.base_testcase import WorkoutManagerTestCase

logger = logging.getLogger(__name__)


class Api_RegistrationTestCase(WorkoutManagerTestCase):
    '''
    Tests registering a new user
    '''
    def test_api_register(self):

        # Fetch the registration page
        response = self.client.get(reverse('core:user:api_registration'))
        self.assertEqual(response.status_code, 200)

        # Fill in the registration form
        registration_data = {'username': 'myusername',
                             'password1': 'secret',
                             'email': 'not an email'}
        count_before = User.objects.count()

        # Correct email
        registration_data['email'] = 'my.email@example.com'
        response = self.client.post(reverse('core:user:api_registration'),
                                    registration_data)
        count_after = User.objects.count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(count_before, count_after)
        self.user_logout()

        # Username already exists
        response = self.client.post(reverse('core:user:api_registration'),
                                    registration_data)
        count_after = User.objects.count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(count_before, count_after)

        # Email already exists
        registration_data['username'] = 'my.other.username'
        response = self.client.post(reverse('core:user:api_registration'),
                                    registration_data)
        count_after = User.objects.count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(count_before, count_after)

    def test_api_registration_added(self):
        '''
        Test that with deactivated registration no users can register
        '''
        # Fetch the registration page
        response = self.client.get(reverse('core:user:api_registration'))
        self.assertEqual(response.status_code, 200)

        # Fill in the registration form
        registration_data = {'username': 'myusername',
                             'password': 'secret',
                             'email': 'my.email@example.com', }
        count_before = User.objects.count()

        response = self.client.post(reverse('core:user:api_registration'),
                                    registration_data)
        count_after = User.objects.count()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(count_before+1, count_after)
