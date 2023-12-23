import re

def read_file(filename="telegram_messages.json"):
    try:
        with open (filename,'r') as file:
            text = file.read()
        return text
    except FileNotFoundError as err:
        print(err)

def extract_youtube_links(text):
    pattern = re.compile(r'https://www\.youtube\.com/[\w@]+/videos')
    youtube_links = pattern.findall(text)
    return youtube_links


if __name__ == "__main__":
    text = read_file()
    youtube_links = extract_youtube_links(text)

    print(*youtube_links,sep="\n")