import re


class PrePro:
    code = None

    @staticmethod
    def filter(code):
        processed = ""
        processed = re.sub(r"(#=)((.|\n)*?)(=#)", '', code)
        return processed
