from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from user.models import User
from recipes.models import Recipe, RecipeRating, Ingredient

class UserLogInViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@gmail.com")
        self.user.set_password("test")
        self.user.save()

    def test_invalid_user_credentials_for_log_in(self):

        response = self.client.post(reverse('login'), data={
                                                            'email': 'test@gmail.com',
                                                            'password': 'test1'
                                                            })
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {'detail': 'No active account found with the given credentials'})

    def test_invalid_password_for_log_in(self):

        response = self.client.post(reverse('login'), data={
                                                            'email': 'test@gmail.com',
                                                            'password': 'pass'
                                                            })
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {'detail': 'No active account found with the given credentials'})

    def test_valid_user_credentials_for_log_in(self):
    
        response = self.client.post(reverse('login'), data={
                                                            'email': 'test@gmail.com',
                                                            'password': 'test'
                                                            })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)

class UserRegisterViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@gmail.com")
        self.user.set_password("test")
        self.user.save()

    def test_successful_user_registration(self):
        response = self.client.post(reverse('register'), data={
                                                                "email": "anovic.nikola3@gmail.com",
                                                                "password": "nindza11",
                                                                "password2": "nindza11",
                                                                "first_name": "Nikola",
                                                                "last_name": "Van Dam"
                                                               })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {
                                            "email": "anovic.nikola3@gmail.com",
                                            "first_name": "Nikola",
                                            "last_name": "Van Dam"
                                          })

    def test_invalid_email(self):
        response = self.client.post(reverse('register'), data={
                                                                "email": "anovic.nikola3@gimejl.com",
                                                                "password": "nindza11",
                                                                "password2": "nindza11",
                                                                "first_name": "Nikola",
                                                                "last_name": "Van Dam"
                                                               })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': ['Email is not valid']})

    def test_email_already_exists(self):
        response = self.client.post(reverse('register'), data={
                                                                "email": "test@gmail.com",
                                                                "password": "nindza11",
                                                                "password2": "nindza11",
                                                                "first_name": "Nikola",
                                                                "last_name": "Van Dam"
                                                                })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {
                                            "email": ["user with this Email already exists."]
                                          })

    def test_password_not_matching_with_password2(self):
        response = self.client.post(reverse('register'), data={
                                                                "email": "anovic.nikola3@gmail.com",
                                                                "password": "nindza11",
                                                                "password2": "nindza12",
                                                                "first_name": "Nikola",
                                                                "last_name": "Van Dam"
                                                                })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {
                                            "password": ["Password fields didn't match."]
                                          })

    def test_password_too_short(self):
        response = self.client.post(reverse('register'), data={
                                                                "email": "anovic.nikola3@gmail.com",
                                                                "password": "nind",
                                                                "password2": "nind",
                                                                "first_name": "Nikola",
                                                                "last_name": "Van Dam"
                                                                })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {
                                            "password": ["This password is too short. It must contain at least 8 characters."]
                                          })

class UserInfoViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@gmail.com", first_name="Nikola", last_name="Anovic")
        self.user.set_password("test")
        self.user.save()

        self.otherUser = User.objects.create(email="test2@gmail.com")
        self.otherUser.set_password("test2")
        self.otherUser.save()

        self.client.force_authenticate(user=self.user)
        self.maxDiff = None

    def test_user_info_view(self):
        response = self.client.get(reverse('info', kwargs={"pk": self.user.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
                                            "email": "test@gmail.com",
                                            "first_name": "Nikola",
                                            "last_name": "Anovic",
                                            'clear_bit': {'company': None,
                           'person': {'avatar': 'https://d1ts43dypk8bqh.cloudfront.net/v1/avatars/8df66063-279b-44df-b9ef-0f6dbfd23379',
                           'bio': None,
                           'email': 'test@gmail.com',
                           'emailProvider': True,
                           'employment': {'domain': None,
                                          'name': 'http://cardioworkout.healthtipsbysam.com',
                                          'role': 'health_professional',
                                          'seniority': None,
                                          'subRole': 'fitness',
                                          'title': 'Certified Fitness Trainer'},
                           'facebook': {'handle': None},
                           'fuzzy': False,
                           'geo': {'city': 'Indianapolis',
                                   'country': 'United States',
                                   'countryCode': 'US',
                                   'lat': 39.768403,
                                   'lng': -86.158068,
                                   'state': 'Indiana',
                                   'stateCode': 'IN'},
                           'github': {'avatar': 'https://avatars.githubusercontent.com/u/31654?v=4',
                                      'blog': 'Hacked',
                                      'company': 'Hacked',
                                      'followers': 14,
                                      'following': 0,
                                      'handle': 'amagri',
                                      'id': 31654},
                           'googleplus': {'handle': None},
                           'gravatar': {'avatar': None,
                                        'avatars': [],
                                        'handle': 'test87',
                                        'urls': []},
                           'id': '8df66063-279b-44df-b9ef-0f6dbfd23379',
                           'indexedAt': '2022-11-24T00:16:21.365Z',
                           'linkedin': {'handle': None},
                           'location': 'Indianapolis, IN, US',
                           'name': {'familyName': 'Brolyle',
                                    'fullName': 'Elizabeth Brolyle',
                                    'givenName': 'Elizabeth'},
                           'site': 'Hacked',
                           'timeZone': 'America/Indiana/Indianapolis',
                           'twitter': {'avatar': None,
                                       'bio': None,
                                       'favorites': None,
                                       'followers': None,
                                       'following': None,
                                       'handle': None,
                                       'id': None,
                                       'location': None,
                                       'site': None,
                                       'statuses': None},
                           'utcOffset': -5}},
                           'email': 'test@gmail.com',
                           'first_name': 'Nikola',
                           'last_name': 'Anovic'})
    def test_other_users_info(self):
        self.client.force_authenticate(user=self.otherUser)
        response = self.client.get(reverse('info', kwargs={"pk": self.user.id}))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'detail': 'You do not have permission to perform this action.'})

class ListAllRecipesViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@gmail.com")
        self.user.set_password("test")
        self.user.save()

        self.ingredient = Ingredient.objects.create(
            name = "ingredient 1"
        )
        
        self.recipe = Recipe.objects.create(
            recipe_author = self.user,
            name = "banana recipe",
            text = "Ovo je banana recept",
        )
        self.recipe.ingredient.add(self.ingredient.id)
        self.client.force_authenticate(user=self.user)

    def test_view_all_recipes_unauthorized(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('all_recipes'))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {'detail': 'Authentication credentials were not provided.'})

    def test_view_all_recipes_authorized(self):
        response = self.client.get(reverse('all_recipes'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'count': 1,
                                           'next': None,
                                           'previous': None,
                                           'results': [{'avg_rating': None,
                                                        'ingredient': [{'name': 'ingredient 1'}],
                                                        'name': 'banana recipe',
                                                        'recipe_author': 1,
                                                        'text': 'Ovo je banana recept'}]})

class CreateRecipesViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@gmail.com")
        self.user.set_password("test")
        self.user.save()
        
        self.ingredient = Ingredient.objects.create(
            name = "Banana"
        )
        
        self.client.force_authenticate(user=self.user)

    def test_recipe_creation(self):
        response = self.client.post(reverse('create_recipes'), data={'name': 'banana recipe',
                                                                     'text': 'Ovo je banana recept',
                                                                     'ingredient': [self.ingredient.id]
                                                                     })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {'ingredient': [1], 
                                            'name': 'banana recipe', 
                                            'text': 'Ovo je banana recept'
                                           })

class ListOwnRecipesViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@gmail.com")
        self.user.set_password("test")
        self.user.save()

        self.otherUser = User.objects.create(email="test2@gmail.com")
        self.otherUser.set_password("test2")
        self.otherUser.save()

        self.ingredient = Ingredient.objects.create(
            name = "ingredient 1"
        )
        
        self.recipe = Recipe.objects.create(
            recipe_author = self.user,
            name = "banana recipe",
            text = "Ovo je banana recept",
        )
        self.recipe.ingredient.add(self.ingredient.id)
        self.client.force_authenticate(user=self.user)

    def test_list_own_recipes(self):

        response = self.client.get(reverse('user_recipes'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [{'avg_rating': None,
                                            'ingredient': [{'name': 'ingredient 1'}],
                                            'name': 'banana recipe',
                                            'recipe_author': 1,
                                            'text': 'Ovo je banana recept'}])

    def test_list_another_users_recipes(self):
        self.client.force_authenticate(user=self.otherUser)

        response = self.client.get(reverse('user_recipes'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [])

class RecipeRatingViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@gmail.com")
        self.user.set_password("test")
        self.user.save()

        self.otherUser = User.objects.create(email="test2@gmail.com")
        self.otherUser.set_password("test2")
        self.otherUser.save()

        self.ingredient1 = Ingredient.objects.create(name="ingredient 1")
        self.ingredient2 = Ingredient.objects.create(name="ingredient 2")
        
        self.recipe1 = Recipe.objects.create(
            recipe_author = self.user,
            name = "banana recipe",
            text = "Ovo je banana recept",
        )

        self.recipe2 = Recipe.objects.create(
            recipe_author = self.otherUser,
            name = "ice cream recipe",
            text = "Ovo je recept za sladoled",
        )
        self.recipe1.ingredient.add(self.ingredient1.id)
        self.recipe2.ingredient.add(self.ingredient2.id)
        
    def test_rate_recipe(self):
        self.client.force_authenticate(user=self.otherUser)
        response = self.client.post(reverse('rate'), data={"recipe": self.recipe1.id,
                                                           "rating": 3
                                                          })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {'recipe': self.recipe1.id, 'rating': 3})

    def test_rate_own_recipe(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('rate'), data={"recipe": self.recipe1.id,
                                                           "rating": 3
                                                          })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), ['You can not rate your own recipe!'])

class IngredientsViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@gmail.com")
        self.user.set_password("test")
        self.user.save()

        self.ingredient1 = Ingredient.objects.create(name="ingredient 1")
        self.ingredient2 = Ingredient.objects.create(name="ingredient 2")

        self.client.force_authenticate(user=self.user)

    def test_list_of_ingredients(self):
        response = self.client.get(reverse('ingredients'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [{'name': 'ingredient 1'}, 
                                           {'name': 'ingredient 2'}])

    def test_creating_ingredients(self):
        response = self.client.post(reverse('ingredients'), data={"name": "banana"})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {'name': 'banana'})

class MostUsedIngredientsViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@gmail.com")
        self.user.set_password("test")
        self.user.save()

        self.ingredient1 = Ingredient.objects.create(name="ingredient 1")
        self.ingredient2 = Ingredient.objects.create(name="ingredient 2")
        self.ingredient3 = Ingredient.objects.create(name="ingredient 3")
        self.ingredient4 = Ingredient.objects.create(name="ingredient 4")
        self.ingredient5 = Ingredient.objects.create(name="ingredient 5")
        self.ingredient6 = Ingredient.objects.create(name="ingredient 6")
        
        self.recipe1 = Recipe.objects.create(
            recipe_author = self.user,
            name = "banana recipe",
            text = "Ovo je banana recept",
        )

        self.recipe2 = Recipe.objects.create(
            recipe_author = self.user,
            name = "ice cream recipe",
            text = "Ovo je recept za sladoled",
        )
        self.client.force_authenticate(user=self.user)
        self.recipe1.ingredient.add(self.ingredient1.id, self.ingredient6.id)
        self.recipe2.ingredient.add(self.ingredient1.id, self.ingredient2.id, 
                                    self.ingredient3.id, self.ingredient4.id, 
                                    self.ingredient6.id)
        
    def test_top_5_most_used_ingredients(self):
        response = self.client.get(reverse('top_5_most_used_ingredients'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [{'name': 'ingredient 1'}, 
                                           {'name': 'ingredient 6'},
                                           {'name': 'ingredient 2'},
                                           {'name': 'ingredient 3'},
                                           {'name': 'ingredient 4'}])