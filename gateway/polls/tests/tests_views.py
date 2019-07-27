from rest_framework.test import APITestCase

from . import create_question


class QuestionAPIViewTests(APITestCase):

    question = None
    future_question = None

    @classmethod
    def setUpClass(cls):
        cls.question = create_question('Question #1', -1)
        cls.question.choices.create(choice_text='Choice A')
        cls.question.choices.create(choice_text='Choice B')
        cls.question.choices.create(choice_text='Choice C')

        cls.future_question = create_question('Question #2', 1)
        cls.future_question.choices.create(choice_text='Choice D')
        cls.future_question.choices.create(choice_text='Choice E')
        cls.future_question.choices.create(choice_text='Choice F')

    @classmethod
    def tearDownClass(cls):
        cls.question.delete()
        cls.future_question.delete()

    def test_get_questions(self):
        response = self.client.get('/questions/', format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(
            response.data['results'][0]['question_text'],
            'Question #1')
        self.assertIsNotNone(response.data['results'][0]['pub_date'])
        self.assertIsNotNone(
            response.data['results'][0]['was_published_recently'])
        self.assertEqual(len(response.data['results'][0]['choices']), 3)
        self.assertEqual(
            response.data['results'][0]['choices'],
            [
                {
                    "id": 3,
                    "choice_text": "Choice C",
                    "votes": 0
                },
                {
                    "id": 2,
                    "choice_text": "Choice B",
                    "votes": 0
                },
                {
                    "id": 1,
                    "choice_text": "Choice A",
                    "votes": 0
                }
            ])

    def test_get_questions_with_futures(self):
        response = self.client.get(
            '/questions/', {'includeFuture': True}, format='json')

        self.assertEqual(
            response.data['results'][0]['question_text'],
            'Question #2')
        self.assertIsNotNone(response.data['results'][0]['pub_date'])
        self.assertIsNotNone(
            response.data['results'][0]['was_published_recently'])
        self.assertEqual(len(response.data['results'][0]['choices']), 3)
        self.assertEqual(
            response.data['results'][0]['choices'],
            [
                {
                    "id": 6,
                    "choice_text": "Choice F",
                    "votes": 0
                },
                {
                    "id": 5,
                    "choice_text": "Choice E",
                    "votes": 0
                },
                {
                    "id": 4,
                    "choice_text": "Choice D",
                    "votes": 0
                }
            ])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(
            response.data['results'][1]['question_text'],
            'Question #1')
        self.assertIsNotNone(response.data['results'][1]['pub_date'])
        self.assertIsNotNone(
            response.data['results'][1]['was_published_recently'])
        self.assertEqual(len(response.data['results'][1]['choices']), 3)
        self.assertEqual(
            response.data['results'][1]['choices'],
            [
                {
                    "id": 3,
                    "choice_text": "Choice C",
                    "votes": 0
                },
                {
                    "id": 2,
                    "choice_text": "Choice B",
                    "votes": 0
                },
                {
                    "id": 1,
                    "choice_text": "Choice A",
                    "votes": 0
                }
            ])

    def test_voting(self):
        response = self.client.post(
            '/questions/2/vote/', {'choice': 5}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data['choices'],
            [
                {
                    "id": 6,
                    "choice_text": "Choice F",
                    "votes": 0
                },
                {
                    "id": 5,
                    "choice_text": "Choice E",
                    "votes": 1
                },
                {
                    "id": 4,
                    "choice_text": "Choice D",
                    "votes": 0
                }
            ])
