import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import setup_db, Movie, Actor
from app import app
from auth import setup_auth0


class Testingmovies(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client
        self.database_name = "agency_test"
        link = "postgres://{}/{}".format('localhost:5432', self.database_name)
        self.database_path = link
        setup_db(app, self.database_path)

        db = SQLAlchemy()
        migrate = Migrate()
        AT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjVSQmpwSXg3UTJscVdsdHB1V2hjaCJ9.eyJpc3MiOiJodHRwczovL2Rldi1hZzEyMy51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDExMzYwOTE4NTg5NTk3MDkyOTciLCJhdWQiOiJhZ2VuY3ktYXBpIiwiaWF0IjoxNjE2NTMxNTQzLCJleHAiOjE2MTY2MTc5NDMsImF6cCI6Im1sQUJZRU9lbzNyOTdkeUp0TTdjZnc3Q0NuM2UzNTRXIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGUgYWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.KaXAjaEbv4gmIeRL8D8OBGUV2DEZHDtPKE0MTW19Q9W-RS-7IXJ6saZbCAHrvfKs8mT0a4i4377J7bbsBgmwIqm4sQZfsNYPz_RxmhcveHa3rGabI3Dai_yPxPwHeZbW-ZrV7OUDkfnQXqK4yGYzD9xDb6ykLvybOcy-0tzv-Vj1hRlt4BudGadkQPx-m9hIJTTdOtgMXzZqd2yIxfi8nKPXPV2f-o32-Xs3k2ZK2PO1b_l0ArfJO8v4F7axld-zYI7ILpOXGvHcHT7SjvRQkavn1V1-WGRu2b9Fofe7F67lAMCp5McMhKIx4Y1jPv1lB839K_p-uZbycr9h5RuC6A'
        self.access_token = AT
        self.authorized_header = {
                                "Authorization": "Bearer " + self.access_token}

        def tearDown(self):
            pass

    def test_non_valid_token_unauthorized_client(self):
        res = self.client().get(
            'movies', headers={"Authorization": "Bearer " + "unauthorized"})
        data = res.get_json()
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_show_all_movies(self):
        res = self.client().get('/movies', headers=self.authorized_header)
        data = res.get_json()
        self.assertEqual(res.status_code, 200)

    def test_add_new_movie_with_incorrect_parameters(self):
        res = self.client().post("/movies", json={
            'title': 'test_movie',
            'description': 'this is for test only',
            'release_date': '2020:3:4'
        }, headers=self.authorized_header)
        data = res.get_json()
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_update_non_existing_movie(self):
        res = self.client().patch("/movies/2000000",json={
            'title': "update test",
            'period': '3h23m'
        },headers= self.authorized_header)
        data = res.get_json()
        self.assertEqual(res.status_code,401)
        self.assertFalse(data['success'])

    def test_add_new_actor_with_correct_parameters(self):
        res = self.client().post("/actors",json={
            'name': "mahmoud sharshar",
            'age': '22',
            'gender': 'male',
            'bio': "nothing!!!!",
            'birthdate': '1998-5-29'
        }, headers = self.authorized_header)
        data = res.get_json()
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['success'])
        inserted_actor = Actor.query.filter(Actor.name=='mahmoud sharshar').all()
        self.assertIsNotNone(inserted_actor)
        inserted_actor[0].delete()

    def test_add_new_actor_with_incorrect_parameters(self):
        res = self.client().post("/actors",json={
            'fullname': "mahmoud sharshar",
            'ae': '22',
            'gende': 'male',
            'biograph': "nothing!!!!",
            'birthdate': '1998-5-29'
        }, headers = self.authorized_header)
        data = res.get_json()
        self.assertEqual(res.status_code,401)
        self.assertFalse(data['success'])        

    def test_show_all_actors(self):
        res = self.client().get("/actors",headers=self.authorized_header)
        data = res.get_json()
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['success'])
    
    def test_delete_non_existing_actor(self):
        res = self.client().delete("/actors/2000000",headers=self.authorized_header)
        data = res.get_json()
        self.assertEqual(res.status_code,401)
        self.assertFalse(data['success'])


if __name__ == "__main__":
    setup_auth0()
    unittest.main()
