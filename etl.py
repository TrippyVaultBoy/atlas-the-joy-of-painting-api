import pandas as pandas
import json
import re
from datetime import datetime


def load_colors(filepath):
    datafile = pandas.read_csv(filepath)
    datafile['colorNames'] = datafile['colors'].apply(lambda c: [
        color.strip().replace('\r\n', '')
        for color in eval(c)
    ])

    datafile['episodeCode'] = datafile.apply(
        lambda row: f"S{int(row['season']):02}E{int(row['episode']):02}",
        axis=1
    )

    return datafile[['img_src', 'painting_title', 'season', 'episode', 'num_colors', 'youtube_src', 'colors', 'episodeCode', 'colorNames']].rename(columns={
        'painting_title': 'title',
        'img_src': 'imageUrl',
        'youtube_src': 'youtubeUrl'
    })


def load_episode_dates(filepath):
    date_map = {}
    with open(filepath, 'r') as file:
        for line in file:
            match = re.match(r'"(.+)" \((.+)\)', line.strip())
            if match:
                title, date_str = match.groups()
                try:
                    date_obj = datetime.strptime(date_str.strip(), "%B %d, %Y")
                    date_map[title.upper()] = {
                        'airDate': date_obj.strftime("%Y-%m-%d"),
                        'month': date_obj.strftime("%B")
                    }
                except ValueError:
                    continue
    return date_map


def load_subject_matter(filepath):
    datafile = pandas.read_csv(filepath)
    datafile['episodeCode'] = datafile['EPISODE'].str.strip().str.upper()
    datafile['subjects'] = datafile.apply(lambda row: [
        col for col in datafile.columns[2:] if row[col] == 1
    ], axis=1)

    return dict(zip(datafile['episodeCode'], datafile['subjects']))


def merge_data(colors, dates, subjects):
    merged = []
    for _, row in colors.iterrows():
        title_key = row['title'].strip().upper()
        air_dates = dates.get(title_key, {})
        subjects_list = subjects.get(row['episodeCode'], [])

        episode = {
            'title': row['title'],
            'season': int(row['season']),
            'episode': int(row['episode']),
            'episodeCode': row['episodeCode'],
            'imageUrl': row['imageUrl'],
            'youtubeUrl': row['youtubeUrl'],
            'colorNames': row['colorNames'],
            'airDate': air_dates.get('airDate'),
            'month': air_dates.get('month'),
            'subjects': subjects_list
        }
        merged.append(episode)
    return merged


def save_to_json(data, filepath):
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=2)


if __name__ == "__main__":
    paintings = load_colors('csv_files/colors_used')
    air_dates = load_episode_dates('csv_files/episode_dates')
    subjects = load_subject_matter('csv_files/subject_matter')

    merged_data = merge_data(paintings, air_dates, subjects)
    save_to_json(merged_data, 'joy_of_painting.json')

    print(f"Exported {len(merged_data)} episodes to joy_of_painting.json")
