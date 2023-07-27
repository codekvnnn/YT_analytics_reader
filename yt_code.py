import datetime
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

# Set up OAuth 2.0 authorization
scopes = ["https://www.googleapis.com/auth/youtube", "https://www.googleapis.com/auth/yt-analytics.readonly"]
api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "client_secret.json"

flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
credentials = flow.run_local_server(port=0)

# Initialize YouTube Data API client
youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

# Initialize YouTube Analytics API client
analytics = googleapiclient.discovery.build("youtubeAnalytics", "v2", credentials=credentials)

# Get the list of videos uploaded in the past year
channel_id = "YOUR_YOUTUBE_CHANNEL_ID_HERE"
now = datetime.datetime.now()
start_time = (now - datetime.timedelta(days=365)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
request = youtube.search().list(part="id", channelId=channel_id, type="video", publishedAfter=start_time, maxResults=50)
response = request.execute()

# Function to get views between two dates
def get_views_between_dates(start_date, end_date, video_id):
    request = analytics.reports().query(
        ids="channel==%s" % channel_id,
        startDate=start_date.strftime("%Y-%m-%d"),
        endDate=end_date.strftime("%Y-%m-%d"),
        metrics="views",
        dimensions="video",
        filters="video==%s" % video_id,
        maxResults=1
    )
    analytics_response = request.execute()
    if analytics_response.get("rows"):
        return analytics_response["rows"][0][1]
    else:
        return 0

# List to store video data
videos = []

# Get the "First 24 Hours" views for each video
for item in response["items"]:
    try:
        video_id = item["id"]["videoId"]

        # Get the video's publish date and title
        video_info = youtube.videos().list(id=video_id, part='snippet').execute()
        video_publish_date = video_info['items'][0]['snippet']['publishedAt']
        video_title = video_info['items'][0]['snippet']['title']
        publish_datetime = datetime.datetime.strptime(video_publish_date, '%Y-%m-%dT%H:%M:%SZ')

        # Get views for the first 24 hours
        end_datetime_24_hours = publish_datetime + datetime.timedelta(days=1)
        first_24_hours_views = get_views_between_dates(publish_datetime, end_datetime_24_hours, video_id)

        video_data = {
            "title": video_title,
            "id": video_id,
            "24h_views": first_24_hours_views,
        }
        videos.append(video_data)
    except googleapiclient.errors.HttpError as e:
        print(f"Failed to process video ID {video_id}, error: {e}")

# After the loop ends, sort the list of videos based on the "First 24 Hours" views
sorted_videos_24h = sorted(videos, key=lambda x: x["24h_views"], reverse=True)

# Now you can print or do whatever with your sorted list.
# For example, print all the videos based on the views in the first 24 hours:
print("\n---First 24 Hours Views---")
for i, video in enumerate(sorted_videos_24h):
    print(f"{i+1}. Video Title: {video['title']}, Video ID: {video['id']}, Views: {video['24h_views']}")
