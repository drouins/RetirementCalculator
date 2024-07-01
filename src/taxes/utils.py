import re


def get_percentage(text):
    # TODO: if more than one match, do something like raise or return them all?
    percentage = re.findall(r'(\d+\.?\d+?%)', text)[0]
    return float(percentage.replace(r'%', '')) / 100
