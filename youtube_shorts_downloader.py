import yt_dlp
import os
import sys
import re
from pathlib import Path

def is_valid_youtube_url(url):
    # Check if it's a valid YouTube URL
    youtube_regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(shorts/|watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    return bool(re.match(youtube_regex, url))

def download_shorts(url):
    try:
        if not is_valid_youtube_url(url):
            print(f"Error: Invalid YouTube URL: {url}")
            return False

        # Configure yt-dlp options
        ydl_opts = {
            'format': 'best',  # Download best quality
            'outtmpl': '%(title)s.%(ext)s',  # Output template
            'quiet': False,  # Show progress
            'no_warnings': False,  # Show warnings
            'extract_audio': False,  # Don't extract audio
            'merge_output_format': 'mp4',  # Merge into mp4
        }

        print(f"\nProcessing URL: {url}")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Get video info
            info = ydl.extract_info(url, download=False)
            print(f"Downloading: {info['title']}")
            print(f"Views: {info.get('view_count', 'N/A')}")
            print(f"Length: {info.get('duration', 'N/A')} seconds")
            
            # Download the video
            ydl.download([url])
            
            # Get the filename
            filename = f"{info['title']}.mp4"
            # Clean the filename
            filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_', '.')).rstrip()
            
            print(f"Download completed successfully!")
            print(f"Saved to: {filename}")
            return True
            
    except Exception as e:
        print(f"An error occurred while processing {url}: {str(e)}")
        return False

def process_urls_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            urls = [line.strip() for line in file if line.strip()]
        
        if not urls:
            print("No URLs found in the file.")
            return
        
        total_urls = len(urls)
        successful_downloads = 0
        
        print(f"\nFound {total_urls} URLs to process")
        
        for i, url in enumerate(urls, 1):
            print(f"\nProcessing URL {i}/{total_urls}")
            if download_shorts(url):
                successful_downloads += 1
        
        print(f"\nDownload Summary:")
        print(f"Total URLs processed: {total_urls}")
        print(f"Successful downloads: {successful_downloads}")
        print(f"Failed downloads: {total_urls - successful_downloads}")
        
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred while reading the file: {str(e)}")

def print_usage():
    print("\nYouTube Shorts Downloader")
    print("=========================")
    print("\nUsage:")
    print("1. For single URL:")
    print("   python youtube_shorts_downloader.py <youtube_shorts_url>")
    print("   Example: python youtube_shorts_downloader.py https://youtube.com/shorts/XXXXXXXX")
    print("\n2. For bulk download:")
    print("   python youtube_shorts_downloader.py <path_to_urls_file>")
    print("   Example: python youtube_shorts_downloader.py urls.txt")
    print("\nNote: For bulk download, create a text file with one URL per line.")
    print("\nRequirements:")
    print("Make sure you have installed yt-dlp:")
    print("pip install yt-dlp")

def main():
    if len(sys.argv) != 2:
        print_usage()
        sys.exit(1)
    
    input_arg = sys.argv[1]
    
    # Check if the input is a file
    if os.path.isfile(input_arg):
        process_urls_from_file(input_arg)
    else:
        # Treat as single URL
        download_shorts(input_arg)

if __name__ == "__main__":
    main() 