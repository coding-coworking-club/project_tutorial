## Politician youtube video wordcloud & sentiment analysis
--- 
A project contains web scraper for youtube video comment with wordcloud visualization and sentiment analysis


### Getting Started 
1. Initialize a virtualenv to manage all required packages

        # ~/politician_analysis/
        pip3 install pipenv
        pipenv --python 3

2. Install packages
   
   Install all required packages based on Pipfile.

        # ~/politician_analysis/
        pipenv sync


3. Update the configaration file
   
   Find src/config.ini (in the folder named src) then edit it if necessary.

   - Change the default value
        - for *VIDEO_ID*
  
            Fill the ids of youtube video you want to analyzeid. The video ID will be located in the URL of the video page, right after the v= URL parameter. In this case, the URL of the video is: https://www.youtube.com/watch?v=aqz-KE-bpKQ. Therefore, the ID of the video is aqz-KE-bpKQ .

4. Execute the project 

        # ~/politician_analysis/
        pipenv run python src/main.py

5. Open Notebook to check wordcloud visualization and sentiment analysis


## Project Orginaztion

        ├── notebook
        ├── src
        │   ├── scraper.py
        │   ├── main.py
        │   └── config.ini
        ├── Pipfile
        ├── Pipfile.lock
        └── README.md
