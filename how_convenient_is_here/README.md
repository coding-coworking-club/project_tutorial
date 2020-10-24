# Convience Evaluation

This tool helps you to evaluate how convenient it is easily. Just provide site address and radius, it brings that information around the site and point which reflects the convenience of site.

## Getting Started

1. Initialize a virtualenv to manage all required packages

    ```bash
    # ~/how_convenient_is_here/
    pip3 install pipenv
    pipenv --python 3
    ```

2. Install packages

   Install all required packages based on `Pipfile`.

   ```bash
   # ~/how_convenient_is_here/
   pipenv install [package name]
   ```

3. Update the configaration file

    Find config.ini in convenience folder then edit it if necessary.
    - Get Google API key

        <https://developers.google.com/maps/documentation/maps-static/get-api-key>

    - Change the default value

        - for `GOOGLE_MAPS` :

            Update address you are interested in and fill in Google API Key.

        - for `INTERESTED_FIELDS` :

            For the fields you do not want to regard with, leave it blank like `FOOD =`.

        - for `GRADING_MANUAL` :

            Give different weights by yourself.
            For `RESTAURANT` and `CAFE`, we use rating/√distance (inverse distance weighting).

        - for `SEARCH_RANGE` :

            Fill in radius in meters.

4. Execute the project

    ```bash
    # ~/how_convenient_is_here/
    pipenv run python src/main.py
    ```

## Project Orginaztion

├── results
├── src
│   ├── convenience
│   │   ├─ _init_.py
│   │   ├─ config,ini
│   │   └─ conveninece_evaluation.py
│   └── main.py
├── Pipfile
├── Pipfile.lock
└── README.md
