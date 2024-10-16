import praw
import json


CLIENT_ID = ''
CLIENT_SECRET = ''
USER_AGENT = ''

# Reddit API credentials
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT
)

# Subreddit to scrape
subreddit_name = 'wallstreetbets'
subreddit = reddit.subreddit(subreddit_name)

# Fetch the top posts from the subreddit
top_posts = subreddit.top(limit=10)  # Adjust 'limit' as needed

# List to hold scraped data
posts_data = []

for post in top_posts:
    post_info = {
        'title': post.title,
        'score': post.score,
        'id': post.id,
        'url': post.url,
        'num_comments': post.num_comments,
        'created': post.created,
        'body': post.selftext,
        'comments': []
    }
    
    # Fetch comments for the post
    post.comments.replace_more(limit=0)  # Replace 'more comments'
    for comment in post.comments.list():
        comment_info = {
            'comment_id': comment.id,
            'comment_body': comment.body,
            'comment_score': comment.score,
            'comment_created': comment.created
        }
        post_info['comments'].append(comment_info)
    
    posts_data.append(post_info)

# Example output: Print post titles
for post in posts_data:
    print(f"Post Title: {post['title']}, Number of Comments: {post['num_comments']}")

with open('wsb_data.json', 'w') as f:
    json.dump(posts_data, f, indent=4)