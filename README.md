# strangertweets
Monitor a twitter stream for a term then spell it out on a wall using addressable LED lights over letters like the mother's wall in Stranger Things.

# Needed these python packages
pip install -U twython

pip install -U python-dotenv

Create a twitter application at apps.twitter.com following the guide at https://learn.sparkfun.com/tutorials/raspberry-pi-twitter-monitor

Create a .env file with, replacing the <> bits:
APP_KEY=<YOUR_CONSUMER_KEY>
APP_SECRET=<YOUR_CONSUMER_SECRET>
OAUTH_TOKEN=<YOUR_ACCESS_TOKEN>
OAUTH_TOKEN_SECRET=<YOU_ACCESS_TOKEN_SECRET>
