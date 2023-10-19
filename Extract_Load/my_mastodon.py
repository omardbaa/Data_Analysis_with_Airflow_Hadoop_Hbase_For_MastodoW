from mastodon import Mastodon

import os
from hdfs import InsecureClient
import datetime
import json

# Your application's client key and client secret
client_id = 'WWzFIqCm3LxE5UgtkivCosN-E0JIy_QNZhSR8Wsa0bY'
client_secret = 'VtnoFOYEPQVUSc_ENwLBLUrivkVqvHWCBLEufs1iMmY'

# Your user's access token
access_token = '-oiJ8d7DD-x0ZEcm5sASly3ENymvlJkYRPQmSeD4iKQ'

# from mastodon import Mastodon
# from hdfs import InsecureClient

# import json  # Import the json module

# Initialize the Mastodon API client
mastodon = Mastodon(
    client_id=client_id,
    client_secret=client_secret,
    access_token=access_token,
    api_base_url='https://mastodon.social'
)

# # Function to handle errors
# def handle_error(exception):
#     print(f"An error occurred: {str(exception)}")

# # Connect to HDFS
# hdfs_client = InsecureClient('http://localhost:9870', user='hadoop')
# print("hdfs_client", hdfs_client)

# try:
#     # Retrieve a list of trending hashtags
#     trending_tags = mastodon.trending_tags()

#     # Iterate through the trending tags and fetch posts for each tag
#     for trending_tag in trending_tags:
#         hashtag = trending_tag['name']
#         hashtag_posts = mastodon.timeline_hashtag(hashtag)
#         print("hashtag_posts", hashtag_posts)

#         # Process the posts for the current trending tag and extract information as needed
#         for post in hashtag_posts:
#             post_id = post['id']
#             user_id = post['account']['id']

#             # Serialize the data as JSON
#             data_to_write = {
#                 "post_id": post_id,
#                 "user_id": user_id
#             }
#             json_data = json.dumps(data_to_write)

#             # Define the HDFS directory and file name
#             hdfs_directory = '/user/omar/mastodon_data'
#             hdfs_file_name = 'data.json'

#             # Define the full HDFS file path
#             hdfs_file_path = f'{hdfs_directory}/{hdfs_file_name}'

#             # Check if the file exists in HDFS, and if not, create it with an empty JSON array
#             if not hdfs_client.status(hdfs_file_path, strict=False):
#                 with hdfs_client.write(hdfs_file_path, overwrite=False) as writer:
#                     initial_data = '[]'  # An empty JSON array
#                     writer.write(initial_data)

#             # Append the JSON data to the existing JSON array
#             with hdfs_client.write(hdfs_file_path, append=True) as writer:
#                 # Ensure the JSON array is well-formed and enclosed in square brackets
#                 writer.write(f",{json_data}\n")  # Add a comma and a newline to separate entries

#             print("Writing is done!")

# except Exception as e:
#     handle_error(e)



# Initialize an HDFS client
hdfs_client = InsecureClient('http://localhost:9870', user='hadoop')

# Get the current date and time
now = datetime.datetime.now()
directory_path = '/raw/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)

# Check if the directory already exists
if not hdfs_client.status(directory_path, strict=False):
    hdfs_client.makedirs(directory_path)

# Define the HDFS path where you want to save the data
hdfs_path = directory_path + '/' + str(now.hour) + '-' + str(now.minute)

# Retrieve the last toot ID from a file or start with None
try:
    with open('last_toot_id.txt', 'r') as f:
        last_toot_id = f.read().strip()
except FileNotFoundError:
    last_toot_id = None

# Retrieve public timeline posts since the last fetched toot
public_posts = mastodon.timeline_public(limit=40, since_id=last_toot_id)

# Custom JSON Encoder to handle datetime serialization
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            # Convert datetime to a string representation
            return o.strftime('%Y-%m-%d %H:%M:%S %z')
        return super().default(o)

# Create a JSON file to store the Mastodon data
with hdfs_client.write(hdfs_path + '-mastodon.json', encoding='utf-8') as writer:
    # Serialize public_posts to JSON
    json.dump(public_posts, writer, ensure_ascii=False, indent=4, default=str, cls=CustomJSONEncoder)

print('Data saved successfully to HDFS : ' + hdfs_path + '-mastodon.json')

# After retrieving the public posts, you can save the latest toot_id to the file.
if public_posts:
    latest_toot = public_posts[0]  # Assuming the latest toot is at the first position
    latest_toot_id = latest_toot['id']

    # Convert latest_toot_id to a string
    latest_toot_id_str = str(latest_toot_id)

    # Check if the file exists
    if hdfs_client.status('last_toot_id.txt', strict=False):
        # Update the file
        hdfs_client.write('last_toot_id.txt', latest_toot_id_str, encoding='utf-8', overwrite=True)
    else:
        # Write the latest toot_id to the file
        with open('last_toot_id.txt', 'w') as f:
            f.write(latest_toot_id_str)
