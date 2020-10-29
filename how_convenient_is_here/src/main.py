import configparser
import os
import sys
import time
from datetime import date

import pandas as pd

from convenience.convenience_evaluation import ConvenienceEvaluation


def main():
    try:
        start_time = time.time()
        config = configparser.ConfigParser()
        config.read("src/config.ini", encoding="utf-8")
        site = ConvenienceEvaluation(
            address=config['GOOGLE_MAPS']["ADDRESS"], key=config["GOOGLE_MAPS"]["KEY"])
        fields = [field for field, value in config.items(
            "INTERESTED_FIELDS") if bool(value)]
        site.type_mapping(fields=fields)
        site.search(radius=config["SEARCH_RANGE"]["RADIUS"])
        grading_manual = {key: float(value)
                          for key, value in config["GRADING_MANUAL"].items()}
        site.get_point(grading_manual=grading_manual)
        end_time = time.time()
        print(f"Site you'd like to know: {config['GOOGLE_MAPS']['ADDRESS']}")
        print(
            f"It's {site.total:.2f} points in {config['SEARCH_RANGE']['RADIUS']} meters")
        print(f"Time consumption: {(end_time - start_time):.2f} seconds")
        is_yes = input(
            "Do you want to save detail inforamation of this site? (Y/N)")
        if is_yes == 'Y':
            project_dir = os.path.abspath(os.path.dirname(sys.argv[0]) or '.')
            today = date.today().strftime("%Y%m%d")
            file_name = f"{config['GOOGLE_MAPS']['ADDRESS']}_{config['SEARCH_RANGE']['RADIUS']}m_{today}"
            csv_path = os.path.join(
                project_dir, f"../results/{file_name}.xlsx")
            with pd.ExcelWriter(csv_path) as writer:
                site.places_table.to_excel(
                    writer, encoding="utf_8_sig", sheet_name="places_info")
                site.points.to_excel(
                    writer, encoding="utf_8_sig", sheet_name="points")
            print("Detail Infomation is saved to 'results'")
    except NameError as e:
        print(
            f"error message: {e}. Make sure all require modules are imported in correct name.")
    except ValueError as e:
        print(
            f"error message: {e}. Make sure your API key is correct.")
    except KeyError as e:
        print(
            f"error message: {e}. Make sure you give all parameters for types you'd like to consider in.")
    except Exception as e:
        print(f"error message: {e}")
        print("Other error. Please provide your error message/config.ini to the author.")


if __name__ == '__main__':
    main()
