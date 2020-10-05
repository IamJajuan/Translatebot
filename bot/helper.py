import tweepy
import os
import requests
from google.cloud import vision
from google.cloud import translate_v2 as translate

def access_twitter_api():
    """
    returns an authenticated api
    """
    consumer_key = os.environ['CONSUMER_KEY']
    consumer_secret = os.environ['CONSUMER_SECRET']
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    access_token = os.environ['ACCESS_TOKEN'],
    access_token_secret = os.environ['ACCESS_TOKEN_SECRET']
    auth.set_access_token( access_token[0], access_token_secret)
    api = tweepy.API(auth)

    return api



def translate_img_text(url):
    """
    translate an image text from url
    """
    response = requests.get(url)
    
    if not response.ok:
        raise Exception("Unable to grab img")

    content = response.content
    vision_client = vision.ImageAnnotatorClient()
    translate_client = translate.Client()
    image = vision.Image(content=content)
    response = vision_client.text_detection(image=image)
    text = response.text_annotations
    text = translate_client.translate(text[0].description, target_language='de')
    return text['translatedText']