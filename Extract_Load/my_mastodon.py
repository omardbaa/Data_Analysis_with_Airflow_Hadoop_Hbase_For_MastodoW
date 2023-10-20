



from mastodon import Mastodon
import os
from hdfs import InsecureClient
import datetime
import json
import time

# Initialize the Mastodon API client
mastodon = Mastodon(
    client_id=client_id,
    client_secret=client_secret,
    access_token=access_token,
    api_base_url='https://mastodon.social'
)

# Initialize an HDFS client
hdfs_client = InsecureClient('http://localhost:9870', user='hadoop')

# Directory and HDFS path setup
now = datetime.datetime.now()
directory_path = '/raw/' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)
hdfs_path = directory_path + '/' + str(now.hour) + '-' + str(now.minute)

# Function to retrieve and store data with retries
def retrieve_and_store_data_with_retry():
    max_retries = 5
    retries = 0
    post_count = 0

    while retries < max_retries:
        try:
            # Retrieve the last toot ID from a file or start with None
            try:
                with hdfs_client.read('last_toot_id.txt') as reader:
                    last_toot_id = reader.read().strip()
            except FileNotFoundError:
                last_toot_id = None

            # Define the minimum number of posts you want to retrieve
            min_post_count = 1000
            total_posts = []

            while len(total_posts) < min_post_count:
                # Retrieve public timeline posts since the last fetched toot
                public_posts = mastodon.timeline_public(limit=40, since_id=last_toot_id)

                if not public_posts:
                    # No new data to retrieve
                    break

                total_posts.extend(public_posts)
                last_toot = public_posts[-1]
                last_toot_id = last_toot['id']
                post_count += len(public_posts)

                # Sleep briefly to avoid hitting API rate limits
                time.sleep(5)

                # Print progress
                print(f'Retrieved {post_count} posts.')

            if total_posts:
                # Serialize and format the data
                formatted_data = [json.dumps(obj, separators=(',', ':'), cls=CustomJSONEncoder) for obj in total_posts]
                formatted_data_str = '\n'.join(formatted_data)

                # Save data to HDFS
                with hdfs_client.write(hdfs_path + '-mastodon.json', encoding='utf-8') as writer:
                    writer.write(formatted_data_str)

                # Update the latest toot ID
                with hdfs_client.write('last_toot_id.txt', encoding='utf-8', overwrite=True) as writer:
                    writer.write(str(last_toot_id))

                print(f'Data saved successfully to HDFS : {hdfs_path}-mastodon.json')
                break  # Exit the retry loop upon success
            else:
                print('No new data to retrieve.')
                break  # Exit the retry loop if there's no new data

        except Exception as e:
            print(f'An error occurred: {str(e)}')
            retries += 1
            print(f'Retry attempt {retries}/{max_retries}')
            time.sleep(5)  # Wait for a minute before retrying

# Custom JSON Encoder
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S %z')
        return super().default(o)

if __name__ == "__main__":
    retrieve_and_store_data_with_retry()
