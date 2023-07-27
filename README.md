# YT_analytics_reader

This script is designed to analyze the views of videos uploaded by a specific YouTube channel within the past year using the YouTube Data API and the YouTube Analytics API. The code follows these steps:

It imports the necessary libraries for working with Google APIs and handling dates.

Sets up OAuth 2.0 authorization to access the YouTube Data API and YouTube Analytics API using the provided client secrets file and specified scopes.

Initializes the YouTube Data API and YouTube Analytics API clients using the obtained credentials through the authorization process.

Retrieves the list of videos uploaded by the designated YouTube channel within the past year. The channel ID and the time range for the past year are specified.

channel_id: The unique identifier of the YouTube channel.
start_time: The start date for the search query, which is calculated as the current date minus 365 days (approximately 1 year).
Defines a function called get_views_between_dates to calculate the number of views for a specific video within a specified date range. The function leverages the YouTube Analytics API.

The function takes the start date, end date, and video ID as input and retrieves the view count for the video within the specified date range.
Initializes an empty list called videos to store video data.

Iterates through the list of videos obtained from the YouTube Data API response.

For each video, it fetches additional information such as the publish date and title using the YouTube Data API.
Calculates the end date for the "First 24 Hours" view count, which is set to 1 day after the video's publish date.
Calls the get_views_between_dates function to obtain the view count for the video within the first 24 hours.
Creates a dictionary containing video information (title, video ID, and "First 24 Hours" views) and appends it to the videos list.
After processing all videos, the code sorts the list of videos based on the "First 24 Hours" views in descending order.

Finally, it prints the sorted list of videos along with their titles, video IDs, and view counts for the first 24 hours.

Note that certain parts of the code are commented out to focus on analyzing the views within the first 24 hours. You have the option to uncomment those sections if you wish to analyze views for the first 30 days and 90 days as well. Feel free to customize the code to meet your specific requirements and preferences.
