## uses python-twitter, tensorflow
import sqlite3
import twitter
from datetime import datetime


## function taken from tutorial at https://towardsdatascience.com/experimenting-with-twitter-data-using-tensorflow-ea88a8078fd
## calculates day since last post
def get_days_quan_after(created_at):
    splitted_created_at = created_at.split()
    month = splitted_created_at[1]
    day = splitted_created_at[2]
    year = created_at[-4:]

    concated_date = (' '.join([month, day, year]))
    datetime_object = datetime.strptime(concated_date, '%b %d %Y')
    today = datetime.now()
    diff = today - datetime_object
    diff_days = diff.days
    return diff_days

api = twitter.Api(consumer_key="T2bsRBmhkBOOhR2zKO1WrAiMh",
                  consumer_secret="vMEUrsDQe1eP98fULVA77OXUMTddx8EE7FcGXgJYjHPj4FGyRD",
                  access_token_key="1079695556241440769-urh9XWAqKQVD1gR2iy1uHWINXqVi32",
                  access_token_secret="YNN74TJ4UMrupw5mLxeLdxULNcThUOU39ZSS8sCITDBxJ")

##twitter: SocialM14074431
twitter_rockstar = (api.GetUser(screen_name='ml_review'))
followers_of_twitter_rockstar = api.GetFollowerIDs(twitter_rockstar.id_str, cursor=0, count=10)

my_followers = api.GetFollowerIDs()
my_friends = api.GetFriendIDs()

conn = sqlite3.connect('twitter.sqlite')
cur = conn.cursor()


cur.execute('''CREATE TABLE IF NOT EXISTS users
        (
        id varchar(255),
        user_name varchar(255),
        created_at int,
        favourites_count int,
        followers_count int,
        friends_count int,
        name varchar(255),
        statuses_count int,
        follows_me int,
        i_am_following int,
        days_after_last_post int
        )
        ''')

for i, follower_id in enumerate(followers_of_twitter_rockstar[120:140]):
    try:
        user = (api.GetUser(user_id=follower_id))
        is_user_protected = int(user.protected)
        if not is_user_protected:
            # below taken from https://towardsdatascience.com/experimenting-with-twitter-data-using-tensorflow-ea88a8078fd
            # applies certain filters to parse through followers
            aim_user_user_name = user.screen_name
            user_id = user.id_str
            user_created_at = int(user.created_at[-4:])
            user_favourites_count = user.favourites_count
            user_followers_count = user.followers_count
            user_friends_count = user.friends_count
            user_name = user.name
            user_statuses_count = user.statuses_count
            user_follows_me = int(follower_id in my_followers)
            user_is_friend = int(follower_id in my_friends)
            last_post_created_at = user.status.created_at
            user_bio = user.description.lower()
            last_post_creation_date = user.status.created_at  # Mon Sep 17 17:44:03 +0000 2018
            user_days_after_last_post = get_days_quan_after(last_post_creation_date)

            print(id,
                 user_name,
                 user_created_at,
                 user_favourites_count,
                 user_followers_count,
                 user_friends_count,
                 user_name,
                 user_statuses_count,
                 user_follows_me,
                 user_is_friend,
                 user_days_after_last_post)
            interests = ['python', 'machine', 'deep', 'code', 'engineer', 'software', 'data', 'developer',
                         'artificial', 'programmer', 'science', 'statistic', 'nlp', 'learning', 'tech', 'computer',
                         'cs', 'programming', 'computers', 'scientist']

            if any(interest in user_bio for interest in
                   interests) and user_favourites_count > 20 and user_friends_count > 100:
                pass
    except:
        continue

    new_friend = api.CreateFriendship(user_id=user.id_str, follow=False, retweets=False)
    create_mute = api.CreateMute(user_id=user.id_str)


    cur.execute('''INSERT OR REPLACE INTO users
    (
        id, 
        user_name, 
        created_at,
        favourites_count, 
        followers_count, 
        friends_count, 
        name, 
        statuses_count, 
        follows_me,
        i_am_following,
        days_after_last_post
    )   VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (user_id,
                 user_name,
                 user_created_at,
                 user_favourites_count,
                 user_followers_count,
                 user_friends_count,
                 user_name,
                 user_statuses_count,
                 user_follows_me,
                 user_is_friend,
                 user_days_after_last_post))
    conn.commit()

    my_followers = api.GetFollowerIDs()
    my_friends = api.GetFriendIDs()

# print our sqlite3 table out!
# queryTable = "SELECT * from users"
#
# queryResults = cur.execute(queryTable)
#
# # Print the users records
#
#
# for result in queryResults:
#     print(result)
