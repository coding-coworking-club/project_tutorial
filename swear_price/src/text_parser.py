import logging
import re

import cn2an
from hanziconv import HanziConv

logging.basicConfig(level=logging.INFO)


def get_parsed_result(text, regex):
    regex = re.compile(regex, re.IGNORECASE)
    result = regex.findall(text)
    return result


def char_to_number(word):
    try:
        normal_char_dict = {
            "〇": "零",
            "貮": "二",
            "參": "三",
            "叄": "三"
        }
        word = f"一{word}" if word[0] in "十拾百佰千仟萬億兆" else word
        char_list = [normal_char_dict[char]
                     if char in normal_char_dict else char for char in word]
        word = "".join(char_list)
        number = cn2an.cn2an(HanziConv.toSimplified(word),  "smart")
        return number
    except ValueError as e:
        logging.error(
            f'error message: {e}. Please refine the script of function of "char_to_number"')
        return 0
