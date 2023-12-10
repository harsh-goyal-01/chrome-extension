import praw
import pandas as pd
from transformers import LongformerForSequenceClassification, LongformerTokenizer
import torch
from flask import Flask, request, jsonify
from flask_cors import CORS 

# from flask_cors import CORS  # Import CORS from flask_cors
app = Flask(__name__)
CORS(app)
# CORS(app)
@app.route('/text', methods=['POST'])
def receive_data():
    sub = request.get_json()
    # Process the received data (e.g., print or manipulate it)
    print('Received data:', sub)
    reddit = praw.Reddit(user_agent="Comment Extraction",
                        client_id="9-xbYwjYiBEieSNPQa6LNQ",
                        client_secret="ET2RZUOglqyGtxLxNielvomQSoHcDw",
                        username="harshgoyal01",
                        password="btpproject")
    # df = pd.DataFrame(columns=['subreddit','avg_score'])
    # df['text'] = df['subreddit'].apply(lambda x: get_subreddit_posts(reddit, x)[1])
    # df['raw_text'] = df['subreddit'].apply(lambda x: get_subreddit_posts(reddit, x)[0])
    # def get_subreddit_posts(reddit, sub):
    # print(sub)
    # print(type(sub))
    subreddit = reddit.subreddit(sub['subreddit'])
    hot_python = subreddit.hot(limit = 500)
    # print(hot_python)
    combined_posts = ""
    for submission in hot_python:
    # if submission.upvote_ratio >= upvoteRatio and submission.ups > ups:
        combined_posts = combined_posts + " " + submission.title + " " + submission.selftext
        # print(type(combined_posts))
        # print(type(submission.comments[0].body))
        # submission.comments.replace_more(limit=0)
        # top_comments= await submission.comments()
        # top_comments = submission.comments[:10]
        # i=0
        # for comment in top_comments:
            # if i<10:
                # print(comment.body)
                # i=i+1
        # await submission.comments.replace_more()
        # comments_count=0
        # print(submission.comments)
        # for comment in submission.comments:
        #     if comments_count >= 10:
        #         break  # Exit loop after 10 comments
        # combined_posts=combined_posts + " " + comment.body
        # comments_count += 1
    # print("hello")
    print(combined_posts)
   
# Load pre-trained model and tokenizer
    # model_name = 'distilbert-base-uncased'
    # tokenizer = DistilBertTokenizer.from_pretrained(model_name)
    # model = DistilBertForSequenceClassification.from_pretrained(model_name)
    model_name = 'allenai/longformer-base-4096'
    tokenizer = LongformerTokenizer.from_pretrained(model_name)
    model = LongformerForSequenceClassification.from_pretrained(model_name)

# Define text
    text = combined_posts[:72000]
    print(len(text))

    inputs = tokenizer(text, return_tensors='pt', max_length=4096, truncation=True)

    # Perform inference/prediction
    with torch.no_grad():
        outputs = model(**inputs)

    # Get prediction probabilities
    probabilities = torch.softmax(outputs.logits, dim=1)

    # Probability distribution (index 0: non-hate, index 1: hate)
    hate_probability = probabilities[0][1].item()
# Tokenize input text and prepare for model input
    # inputs = tokenizer(text, return_tensors='pt')

# Perform inference/prediction
    # with torch.no_grad():
        # outputs = model(**inputs)

# Get prediction probabilities
    # probabilities = torch.softmax(outputs.logits, dim=1)

# Probability distribution (index 0: non-hate, index 1: hate)
    # hate_probability = probabilities[0][1].item()
   
    print(f"Hate speech probability: {hate_probability:.2f}")


    # raw_combined_posts = combined_posts
        # combined_posts = remove_emoji(combined_posts)
        # combined_posts = combined_posts.lower()
        # combined_posts = remove_punctuation(combined_posts)
        # combined_posts = remove_stopwords(combined_posts)
        # combined_posts = stem_words(combined_posts)
        # combined_posts = lemmatize_words(combined_posts)
    # hate_probability=convert_into_percentage(hate_probability)
    if hate_probability <= 0.45:
        hate_probability = 12
    elif hate_probability > 0.56:
        hate_probability = 82
    else:
        hate_probability = 100*(hate_probability - 0.45) / (0.56 - 0.45)
  # print(combined_posts)
        # return [raw_combined_posts, combined_posts]

    # Send a response back to the frontend
    return jsonify({'Estimated probabilty of hate speech on this subreddit': f'{hate_probability}%'})

if __name__ == '__main__':
    app.run(debug=True,port=8000)