import tweepy
import openai
import schedule
import time
import os
from datetime import datetime
import random
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Credentials
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CLIENT_ID = os.getenv("TWITTER_CLIENT_ID")
CLIENT_SECRET = os.getenv("TWITTER_CLIENT_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# Initialize OpenAI
openai.api_key = OPENAI_API_KEY

# Initialize Twitter Client
client = tweepy.Client(
    consumer_key=CLIENT_ID,
    consumer_secret=CLIENT_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

def generate_affirmation():
    """Generate an affirmation using OpenAI's API"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
            {
                "role": "system",
                "content": """You are a compassionate motivational coach creating daily Twitter-optimized affirmations focused on:\n
                - Spreading love and positivity\n
                - Cultivating gratitude\n
                - Promoting mindfulness\n
                - Inspiring personal growth\n
                - Encouraging emotional wellness"""
            },
            {
                "role": "user",
                "content": """Create a concise, powerful affirmation that:\n
                - Fits Twitter's 280-character limit\n
                - Promotes emotional resilience\n
                - Encourages self-love and mindful living\n
                - Uses inclusive, uplifting language\n
                - Provides actionable positive perspective\n
                - Addresses the reader directly using 'you'"""
            }
            ],
            max_tokens=100,
            temperature=0.7
        )
        
        affirmation = response.choices[0].message.content.strip()
        
        # Ensure the affirmation fits Twitter's character limit
        if len(affirmation) > 280:
            affirmation = affirmation[:277] + "..."
            
        return affirmation
    
    except Exception as e:
        print(f"Error generating affirmation: {str(e)}")
        return None

def post_tweet():
    """Post a tweet with the generated affirmation"""
    try:
        # Generate affirmation
        affirmation = generate_affirmation()
        
        if affirmation:
            # Post to Twitter
            response = client.create_tweet(text=affirmation)
            
            # Log successful tweet
            print(f"Tweet posted successfully at {datetime.now()}")
            print(f"Tweet content: {affirmation}")
            return True
            
    except Exception as e:
        print(f"Error posting tweet: {str(e)}")
        return False

def run_bot():
    """Main function to run the bot"""
    try:
        # Post initial tweet
        post_tweet()
        
        # Schedule daily tweets
        schedule.every().day.at("09:00").do(post_tweet)  # Posts at 9 AM daily
        
        # Keep the script running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
            
    except KeyboardInterrupt:
        print("\nBot stopped by user")
    except Exception as e:
        print(f"Error running bot: {str(e)}")

if __name__ == "__main__":
    # Verify credentials before starting
    try:
        # Test Twitter credentials
        test_tweet = client.create_tweet(text="Bot initialization test - " + str(datetime.now()))
        print("Twitter credentials verified successfully!")
        
        # Delete test tweet
        client.delete_tweet(test_tweet.data['id'])
        
        # Start the bot
        print("Starting affirmation bot...")
        run_bot()
        
    except Exception as e:
        print(f"Error verifying credentials: {str(e)}")