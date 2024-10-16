import praw
from datetime import datetime
import pytz
import json

CLIENT_ID = ''
CLIENT_SECRET = ''
USER_AGENT = ''

# Initialize Reddit instance
reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     user_agent=USER_AGENT)

def fetch_comments(comment_forest):
    comments = []
    for comment in comment_forest:
        if isinstance(comment, praw.models.MoreComments):
            continue
        comments.append({
            'id': comment.id,
            'body': comment.body,
            'score': comment.score,
            'created': datetime.fromtimestamp(comment.created_utc, tz=pytz.utc).isoformat(),
            'num_comments': len(comment.replies),
            # Recursively fetch subcomments
            'replies': fetch_comments(comment.replies)
        })
    return comments

def fetch_post_with_comments(submission):
    post_data = {
        'id': submission.id,
        'title': submission.title,
        'score': submission.score,
        'url': submission.url,
        'num_comments': submission.num_comments,
        'created': datetime.fromtimestamp(submission.created_utc, tz=pytz.utc).isoformat(),
        'body': submission.selftext,
        'comments': fetch_comments(submission.comments)
    }
    return post_data

# Fetch the newest posts from r/wallstreetbets
subreddit = reddit.subreddit('wallstreetbets')
posts_data = []

for i,submission in enumerate(subreddit.new(limit=None)):  # Adjust the limit to fetch more posts if needed
    print(f"Submission {i} : {submission.title}")
    post_data = fetch_post_with_comments(submission)
    posts_data.append(post_data)

# Save the data to a JSON file
with open('wsb_new_nested.json', 'w') as f:
    json.dump(posts_data, f, indent=4)

print("Data has been saved to wallstreetbets_posts.json")
