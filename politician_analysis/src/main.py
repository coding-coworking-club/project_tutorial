import configparser
import re
import pandas as pd

from collections import Counter
from scraper import (
    find_value,
    ajax_request,
    search_dict,
    download_comments
)


def main():

    config = configparser.ConfigParser()
    config.read("src/config.ini", encoding="utf-8")
    all_id_list = config["VIDEO_ID"]["ID_LIST"]
    
    comment_df_final = pd.DataFrame()

    count = 0
    for video_id in all_id_list:
        count += 1
        comment_data = [] 
        for comment in download_comments(video_id):
            useless = '[a-zA-Z\s\d"#$%&\()*/<=>@【】?!.《》，。...:,\/]'
            remove = re.sub(useless,'',comment['text'])
            comment_data.append(remove)
            comment_df = pd.DataFrame(data = comment_data, columns=['comments'])
            comment_df['video_num'] = f'video{count}'
        
        comment_df_final = comment_df_final.append(comment_df)
        comment_df_final.to_csv('comment_data.csv',index = False)

        
if __name__ == '__main__':
    main()
