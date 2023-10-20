#!/usr/bin/env python3
import sys

current_user = None
earliest_followers = float('inf')
earliest_time = "00:00:00"
engagement_rate_sum = 0.0
count = 1

for line in sys.stdin:
    user, data = line.strip().split('\t')
    followers = int(data.split('@')[1])
    time = data.split('@')[0]
    engagement_rate = float(data.split('@')[2])

    if current_user == user:
        if time < earliest_time:
            earliest_time = time
            earliest_followers = followers
        engagement_rate_sum += engagement_rate
        count += 1
    else:
        if current_user is not None:
            if count > 0:
                engagement_rate_avg = engagement_rate_sum / count
                print(f"{current_user}\tengagement_rate:{engagement_rate_avg:.4f}")
                print(f"{current_user}\tfollowers:{earliest_followers}")
        current_user = user
        earliest_followers = followers
        earliest_time = time
        engagement_rate_sum = engagement_rate
        count = 1

# Print the last user's data
if current_user is not None:
    if count > 0:
        engagement_rate_avg = engagement_rate_sum / count
        print(f"{current_user}\tfollowers:{earliest_followers}")
        print(f"{current_user}\tengagement_rate:{engagement_rate_avg:.4f}")