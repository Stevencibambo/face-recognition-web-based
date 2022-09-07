# # import the necessary package
#
# from app.test.base import BaseTestCase
# import unittest
# import json
#
# def register_user(self):
#     return self.client.post(
#         '/user/',
#         data=json.dumps(dict(
#             email='example@gmail.com',
#             username='username',
#             password='123456',
#             max_connection="100"
#         )),
#         content_type='application/json'
#     )
#
# def login_user(self):
#     return self.client.post(
#         '/auth/login',
#         data=json.dumps(dict(
#             email='example@gmail.com',
#             password='123456'
#         )),
#         content_type='application/json'
#     )
# class TestAuthBlueprint(BaseTestCase):
#     def test_registered_user_login(self):
#         """Test for login of registered-user login"""
#         with self.client:
#             # user registration
#             user_response = register_user(self)
#             response_data = json.loads(user_response.data.decode())
#             self.assertTrue(response_data['Authorization'])
#             self.assertEqual(user_response.status_code, 201)
#
#             login_response = login_user(self)
#             data = json.loads(login_response.data.decode())
#             self.assertTrue(data['Authorization'])
#             self.assertTrue(login_response.status_code, 200)
#
#     def test_valid_logout(self):
#         """Test for logout before token expires"""
#         with self.client:
#             user_response = register_user(self)
#             response_data = json.loads(user_response.data.decode())
#             self.assertTrue(response_data['Authorization'])
#             self.assertTrue(user_response.status_code, 201)
#
#             login_response = login_user(self)
#             data = json.loads(login_response.data.decode())
#             self.assertTrue(data['Authorization'])
#             self.assertEqual(login_response.status_code, 200)
#
#             response = self.client.post(
#                 '/auth/logout',
#                 headers=dict(
#                     Authorization='Bearer' + json.loads(
#                         login_response.data.decode()
#                     )['Authorization']
#                 )
#             )
#             data = json.loads(response.data.decode())
#             self.assertTrue(data['status'] == 'success')
#             self.assertEqual(response.status_code, 200)
#
# if __name__ == '__main__':
#     unittest.main()