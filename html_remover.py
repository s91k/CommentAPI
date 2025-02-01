import re

htmlRemover = re.compile(r'<.*?>')

def removeHtmlTags(text):
    return htmlRemover.sub('', text)