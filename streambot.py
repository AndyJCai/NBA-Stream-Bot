from bs4 import BeautifulSoup
import praw
import re

client_id = "FItKtFrpFPdUQA"
client_secret = "tD_rK3gQm8y_gm2MfkWWIa5QPaA"
user_agent = "nbastream_bot"

#create reddit instance by inputting the client_id, client_secret,
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)

#function that does all the dirty work!
def collectGameURl():
    existGame = False
    game_names = []
    game_links = []
    #grab the subreddit of NBA streams
    subreddit = reddit.subreddit('nbastreams')
    for submission in subreddit.hot():
        title = submission.title
        if "Game Thread: " in title:
            game_names.append(title)
            existGame = True
            list_of_comments = submission.comments.list()
            subLinkList = []
            for comment in list_of_comments:
                soup = BeautifulSoup(comment.body_html)
                for row in soup.findAll('a', attrs={'href': re.compile("^http://")}):
                    subLinkList.append(row.get('href'))
            game_links.append(subLinkList)


    if (existGame):
        print("This is a list of available stream websites: ")
        dictionary = dict(zip(game_names, game_links))
        for k, v in dictionary.items():
            print(k)
            for i in range(len(v)):
                if (validateURL(v[i])):
                    print(i+1,  ": ", v[i])
    else:
        print("There is no available nba game right now, check back later!")

#Below function validates the format of the url
def validateURL(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

collectGameURl()