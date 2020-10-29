import requests
from bs4 import BeautifulSoup
# import PySimpleGUI
import re, os, sys, time

ABS_PATH = os.path.abspath(__file__) 
BASE_DIR = os.path.dirname(ABS_PATH)
OUTPUTS  = os.path.join(BASE_DIR, 'Downloads')

def get_file_size(file_path):
    file_size = os.path.getsize(file_path)
    return file_size

anime_name_input = str(input("Anime Name:"))
episode_range    = str(input("Episode num/range:"))

anime_name =  anime_name_input.lower().replace(" ", "-")

if '-' in episode_range:
    start = int(episode_range.split("-")[0])
    end   = int(episode_range.split("-")[-1])
else:
    start = int(episode_range)
    end   = start

for episode_no in range(start, end+1):
    site_url = f"http://www.anime1.com/watch/{anime_name}/episode-{episode_no}" 
    source = requests.get(site_url).text

    status = requests.get(site_url).status_code 

    if status != 200:
        print(f"\nNo anime named {anime_name.upper()} found.")
        break
    
    ANIME_FOLDER = os.path.join(OUTPUTS, str(anime_name))
    os.makedirs(ANIME_FOLDER, exist_ok=True)

    soup = BeautifulSoup(source, 'html.parser')

    pattern =  re.compile("file:.*")
    result = re.findall(pattern, source)[0]
    video_link = str(result).split('"')[1].replace(" ", "%20")

    video_name = os.path.join(ANIME_FOLDER, f"{anime_name}-{episode_no}.mp4")

    start_time = time.time()

    with open(video_name, 'wb') as f:
        response     = requests.get(video_link, stream=True)
        total_length = response.headers.get('content-length')
        if total_length is None:
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            print(f"Downloading {anime_name} episode {episode_no}")
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('█' * done, ' ' * (50 - done))) 
                sys.stdout.flush()
    
    end_time  = time.time()
    total_time = end_time - start_time

    print(f"\nDownloaded {video_name}")
    downloaded_file_size = get_file_size(video_name)
    file_size_mb = downloaded_file_size / 1024 / 1024
    print(f"File Size: {file_size_mb:.4f} MB")
    print(f"Download Time: {total_time:.4f} seconds.")


