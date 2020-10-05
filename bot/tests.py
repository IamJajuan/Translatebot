from django.test import TestCase
import tweepy
from google.cloud import vision
from google.cloud import translate_v2 as translate

import io
# Create your tests here.
import os
from .helper import access_twitter_api
from   .tasks import check_mentions , reply
from .models import Mention



class BotTestCase(TestCase):
    """
    use the manage.py test bot.tests.BotTestCase to test cases
    """


    def setUp(self):
        """
        setup database
        """
        check_mentions(2)

    def test_check_db(self):
        """
        test_check_db check if database is populated
        """
        self.assertGreaterEqual(Mention.objects.count(),1)
    
    def test_reply(self):
        """
        Test the reply function
        """
        reply("user")
        
        

class TwitterTestCase(TestCase):

    

    def test_get_access_twitter(self):
        """
        Make sure you can access your twitter account
        """
    
        consumer_key = os.environ['CONSUMER_KEY']
        consumer_secret = os.environ['CONSUMER_SECRET']
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        access_token = os.environ['ACCESS_TOKEN'],
        access_token_secret = os.environ['ACCESS_TOKEN_SECRET']
        auth.set_access_token(access_token[0], access_token_secret)
        api = tweepy.API(auth)
        user = api.get_user('twitter')
        ms= api.mentions_timeline()
        self.assertEqual(user.screen_name,"Twitter")

    def test_check_mention(self):
            """
            check mentions
            """
            check_mentions(1)
            self.assertEqual(Mention.objects.count(),1)



class GoogleTestCase(TestCase):

    def test_vision(self):
        """
        Make sure google can read image text
        """

        file_name = "C:\\Users\jajua\Pictures\Stop sign.jpg"
        client = vision.ImageAnnotatorClient()

        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        response = client.text_detection(image=image)
        text = response.text_annotations
        self.assertEqual(text[0].description,"STOP\n")
    
   

    def test_translate_img_text(self):
        """
        Make sure google can translate text from imgage
        """

        file_name = "C:\\Users\jajua\Pictures\Stop sign.jpg"
        vision_client = vision.ImageAnnotatorClient()
        translate_client = translate.Client()

        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        response = vision_client.text_detection(image=image)
        text = response.text_annotations
        text = translate_client.translate(text[0].description, target_language='de')
        self.assertEqual(text['translatedText'],'HALT')



    
        