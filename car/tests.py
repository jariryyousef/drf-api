from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Car

class CarModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user = get_user_model().objects.create_user(username='jariry',password='123456')
        test_user.save()

        test_car = Car.objects.create(
            auther = test_user,
            title = 'bmw',
            descripton = 'descripton for bmw',
            year = 2020
            
        )
        test_car.save()

    def test_blog_content(self):
        car = Car.objects.get(id=1)

        self.assertEqual(str(car.auther), 'jariry')
        self.assertEqual(car.title, 'bmw')
        self.assertEqual(car.descripton, 'descripton for bmw')

class APITest(APITestCase):
    def test_list(self):
        response = self.client.get(reverse('car_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail(self):

        test_user = get_user_model().objects.create_user(username='jariry',password='123456')
        test_user.save()

        test_car = Car.objects.create(
            auther = test_user,
            title = 'bmw',
            descripton = 'descripton for bmw',
            year = 2020
        )
        test_car.save()

        response = self.client.get(reverse('car_detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'id':1,
            'title': test_car.title,
            'descripton': test_car.descripton,
            'auther': test_user.id,
            'year': test_car.year,
        })


    def test_create(self):
        test_user = get_user_model().objects.create_user(username='jariry',password='123456')
        test_user.save()

        url = reverse('car_list')
        data = {
            "title":"bmw",
            "descripton":"descripton for bmw",
            "auther":test_user.id,
            "year" : 2020
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, test_user.id)

        self.assertEqual(Car.objects.count(), 1)
        self.assertEqual(Car.objects.get().title, data['title'])

    def test_update(self):
        test_user = get_user_model().objects.create_user(username='jariry',password='123456')
        test_user.save()

        test_car = Car.objects.create(
            auther = test_user,
            title = 'bmw',
            descripton = 'descripton foe bmw',
            year = 2020
        )

        test_car.save()

        url = reverse('car_detail',args=[test_car.id])
        data = {
            "title":"bmw",
            "auther":test_car.auther.id,
            "descripton":test_car.descripton,
            "year": test_car.year
        }

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK, url)

        self.assertEqual(Car.objects.count(), test_car.id)
        self.assertEqual(Car.objects.get().title, data['title'])


    def test_delete(self):
        """Test the api can delete a car."""

        test_user = get_user_model().objects.create_user(username='jariry',password='123456')
        test_user.save()

        test_car = Car.objects.create(
            auther = test_user,
            title = 'bmw',
            descripton = 'descripton for bmw',
            year = 2020
        )

        test_car.save()

        car = Car.objects.get()

        url = reverse('car_detail', kwargs={'pk': car.id})


        response = self.client.delete(url)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT, url)