#!/bin/bash

# Configuration
API_URL="http://127.0.0.1:5000/api/timeline_post"
RANDOM_ID=$RANDOM
NAME="TestUser$RANDOM_ID"
EMAIL="test$RANDOM_ID@example.com"
CONTENT="This is a test post with ID $RANDOM_ID"

# Step 1: POST a new timeline post
echo "Posting timeline entry..."
POST_RESPONSE=$(curl -s -X POST "$API_URL" \
  -d "name=$NAME" \
  -d "email=$EMAIL" \
  -d "content=$CONTENT")

echo "Post response: $POST_RESPONSE"

# Step 2: GET timeline posts
echo "Fetching timeline entries..."
GET_RESPONSE=$(curl -s "$API_URL")

echo "Looking for the test post..."
echo "$GET_RESPONSE" | grep "$CONTENT" > /dev/null

if [ $? -eq 0 ]; then
  echo "Test post found in timeline."
else
  echo "Test post not found."
  exit 1
fi

# Step 3: Delete the post if a DELETE endpoint is implemented

POST_ID=$(echo "$POST_RESPONSE" | grep -o '"id":[0-9]*' | cut -d':' -f2)

if [ -n "$POST_ID" ]; then
  echo "Deleting post with ID $POST_ID..."
  DELETE_RESPONSE=$(curl -s -X DELETE "$API_URL/$POST_ID")
  echo "Delete response: $DELETE_RESPONSE"
else
  echo "Skipping delete: couldn't extract post ID."
fi


