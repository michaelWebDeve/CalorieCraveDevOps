import unittest
from app import app
from db import AppUser
from db import db
from flask import session


class TestCalorieCrave(unittest.TestCase):  # erbt von der klasse Testcase
    def setUp(self):
        self.app = app.test_client()  # Instanz des testclients
        self.app.testing = True

    def client(self):
        app.config['TESTING'] = True
        return app.test_client()  # gibt tesclient zurück welcher benötigt wird um http anfragen zu senden

    def test_landing_page(self):
        with self.client() as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 302)

    def test_change_password(self):
        with app.app_context():
            with self.client() as client:
                current_password = '12345678'
                email = 'michaelepic72@gmail.com'
                response = client.post('/change_password',
                                       data=dict(current_password='12345678', new_password='123456789#',
                                                 confirm_password='123456789#'))
                self.assertEqual(response.status_code, 302)
                # Überprüfen, ob das Passwort in der Datenbank geändert wurde
                #updated_user = db.session.query(AppUser).filter_by(email)
                #self.assertNotEqual(current_password, updated_user.pwd)# current pw ist nicht gleich updated pw

                # Zurücksetzen des Passworts in der Datenbank
               # updated_user.pwd = current_password
                #db.session.commit()

    def test_login(self):
        with self.client() as client:
            response = client.post('/login', data=dict(email='michaelepic72@gmail.com', password='12345678'))
            self.assertEqual(response.status_code, 302)

    def test_populate_db(self):
        with self.client() as client:
            client.get('/populate-db')
            self.assertEqual(client.get('/populate-db').status_code, 200, msg="Database populated!")

    def test_get_recipe(self):
        with self.client() as client:
            client.get('/recipe/1')
            self.assertEqual(client.get('/recipe/1').status_code, 200)
