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
        config.read("src/convenience/config.ini", encoding="utf-8")
        site = ConvenienceEvaluation(
            address=config['GOOGLE_MAPS']["ADDRESS"], key=config["GOOGLE_MAPS"]["KEY"])
        fields = [field for field, value in config.items(
            "INTERESTED_FIELDS") if bool(value)]
        site.type_mapping(fields=fields)
        site.search(radius=config["SEARCH_RANGE"]["RADIUS"])
        types = [
            each_type for field in fields for each_type in site.search_fields[field]]
        grading_manual = {
            each_type: config["GRADING_MANUAL"][each_type.upper()] for each_type in types}
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
    except Exception as e:
        print(f"error message: {e}")
        print("500 - Server Error. Please provide your error message/config.ini to the author.")


if __name__ == '__main__':
    main()
