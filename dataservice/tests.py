import os
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from dataservice.models import DataFile
from common.util import create_admin

class ApiTests(APITestCase):
    def setUp(self):
        self.datafile_url = 'http://localhost:8000/api/datafile/'
        self.aggregate_url = 'http://localhost:8000/api/aggregate/'
        self.admin = create_admin()
        self.authenticated = self.client.login(username='admin', password='admin')
        self.good_sample_file_path = os.path.join(os.path.dirname(__file__), 'test_data/JDS_Sample-phone_20140401_10k.json')
        self.good_sample_chunk_file_path = os.path.join(os.path.dirname(__file__), 'test_data/sample_chunk.json')
        self.bad_sample_file_path = os.path.join(os.path.dirname(__file__), 'test_data/bad_sample_chunk.json')
        self.wrong_frmt_sample_file_path = os.path.join(os.path.dirname(__file__), 'test_data/test.txt')
        self.sample_row_file_path = os.path.join(os.path.dirname(__file__), 'test_data/sample_row.json')
        self.uploaded_files = []

    def tearDown(self):
        for file_path in self.uploaded_files:
            rel_path = "." + file_path
            if os.path.exists(rel_path):
                os.remove(rel_path)

    def test_new_upload_with_file(self):
        """
        Test datafile endpoit with all data present
        """
        self.assertTrue(self.authenticated)
        data = {'filename':'test_file', 'description':'test description'}
        with open(self.good_sample_chunk_file_path, 'r') as fp:
            data['file'] = fp
            response = self.client.post(self.datafile_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.uploaded_files.append(response.data['file'][17:])
        self.assertEqual(DataFile.objects.count(), 1)
        self.assertEqual(DataFile.objects.get().filename, 'test_file')

    def test_new_upload_without_file(self):
        """
        Test datafile endpoint without providing a file
        """
        self.assertTrue(self.authenticated)
        data = {'filename':'test_file', 'description':'test description'}
        response = self.client.post(self.datafile_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(DataFile.objects.count(), 0)

    def test_aggregate_for_existing_field(self):
        """
        Test aggregate endpoint for an existing field
        """
        self.assertTrue(self.authenticated)
        data = {'filename':'sample_row', 'description':'test a sample row froma file'}
        with open(self.sample_row_file_path, 'r') as fp:
            data['file'] = fp
            response = self.client.post(self.datafile_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.uploaded_files.append(response.data['file'][17:])
        file_id = response.data['id']
        aggregate_field = "event_duration"
        url = "{0}{1}/{2}".format(self.aggregate_url, file_id, aggregate_field)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'], "295")

    def test_aggregate_for_nonexisting_field(self):
        """
        Test aggregate endpoint for an existing field
        """
        self.assertTrue(self.authenticated)
        data = {'filename':'sample_row', 'description':'test a sample row froma file'}
        with open(self.sample_row_file_path, 'r') as fp:
            data['file'] = fp
            response = self.client.post(self.datafile_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.uploaded_files.append(response.data['file'][17:])
        file_id = response.data['id']
        aggregate_field = "event_duratio"
        url = "{0}{1}/{2}".format(self.aggregate_url, file_id, aggregate_field)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_aggregate_for_nonexisting_file(self):
        """
        Test aggregate endpoint for an existing field
        """
        self.assertTrue(self.authenticated)
        data = {'filename':'sample_row', 'description':'test a sample row froma file'}
        with open(self.sample_row_file_path, 'r') as fp:
            data['file'] = fp
            response = self.client.post(self.datafile_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.uploaded_files.append(response.data['file'][17:])
        aggregate_field = "event_duratio"
        url = "{0}{1}/{2}".format(self.aggregate_url,'999', aggregate_field)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_aggregate_for_bad_file_formatting(self):
        """
        Test aggregate endpoint for an existing field
        """
        self.assertTrue(self.authenticated)
        data = {'filename':'sample_row', 'description':'test a sample row froma file'}
        with open(self.bad_sample_file_path, 'r') as fp:
            data['file'] = fp
            response = self.client.post(self.datafile_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.uploaded_files.append(response.data['file'][17:])
        file_id = response.data['id']
        aggregate_field = "event_duration"
        url = "{0}{1}/{2}".format(self.aggregate_url, file_id, aggregate_field)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
