import tweepy
from google.cloud import vision
from google.cloud import translate_v2 as translate
import io
from .helper import access_twitter_api, translate_img_text
from .models import Mention




def reply(user):
    """
    reply to mentions
    """
    api = access_twitter_api()
    mentions = Mention.objects.all()
    
    for mention in mentions:

        if not mention.replied:
            Mention.objects.filter(id=mention.id).update(replied = True)
            text = translate_img_text(mention.img)
            api.update_status(f'@{mention.name} {text}', mention.tweet_id)
            
            

    



def check_mentions(user):
    """
    checks_mentions checks your mentions
from bot.tasks import check_mentions
    """
    
    api = access_twitter_api()
    mentions = api.mentions_timeline()
    
    for mention in mentions:
   
        #print(f'Mention {mention._json } \n')
        tweet = mention._json['text']
        tweet_id = mention._json['id']
        entry = mention._json['user']
        if 'media' in mention._json['entities'].keys():
            media= mention._json['entities']['media']
            name = mention._json['user']['screen_name']
           # print(f"Media: {media}  Name: {name}")
            media_url = media[0]['media_url']
            tweet_obj = Mention.objects.filter(tweet=tweet,tweet_id=tweet_id,name=name,img = media_url).first() 
            if tweet_obj == None:
               tweet_obj=Mention.objects.create(tweet=tweet,tweet_id =tweet_id,name = name,img = media_url)
               tweet_obj.save()
            #from .models import Mention 
            #Mention.objects.filter(tweet ='Hello Handsome',tweet_id = 123,name='john')

            #print(f'URL {media_url}')
        #has_it = Mention.objects.filter(tweet_id = mention.id)
        #print(f'has_it {has_it}')
    


    
   



