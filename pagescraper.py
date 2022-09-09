from pickle import FALSE, TRUE
import sys
import getopt
import urllib.request
import urllib3
import requests as rq
import re
import time
import json


def open_html():
    html = "<html><body><head></head><table>"
    return html

def url_html(url):
    html = "<tr><td><a href='" + url + "' target='_blank'>" + url + "</a></td></tr>"
    return html

def close_html():
    html = "</table></body</html>"
    return html

def get_page(url):
    """ loads a web page """
    src = ''

    try:
        page = urllib.request.urlopen(url)
        chunk = True
        code_chunk = ''
        while chunk:
            code_chunk = page.read().decode("utf-8")
            src += code_chunk
            if code_chunk == '':
                chunk = False
        page.close()
    except IOError:
        print("can't open", url)
        return src

    return src


arguments = sys.argv[1:]
options = "ua"
longOptions = ["user", "archive"]
#outputFile = ""
twitterHandle = "MyLibbyNinjah" #mlnpl0sln2 #"H16hF1d3l17Y"
outputFile = twitterHandle + ".html"
archive = FALSE

args, opts = getopt.getopt(arguments, options, longOptions)

for arg, opt in args:
    if arg == "-u":
        twitterHandle = opt
    elif arg == "-a":
        archive = TRUE

dataUrl = "https://web.archive.org/cdx/search/cdx?url=twitter.com/" + twitterHandle + "/*&collapse=digest&output=json"

waybackUrls = rq.get(dataUrl).text
parsedWaybackUrls = json.loads(waybackUrls)
fileContents = ""

url_list = []
for i in range(1,len(parsedWaybackUrls)):
    orig_url = parsedWaybackUrls[i][2]
    tstamp = parsedWaybackUrls[i][1]
    waylink = tstamp+'/'+orig_url
    url_list.append(waylink)

fileContents += open_html()

i = 0
for url in url_list:
    i += 1
    final_url = 'https://web.archive.org/web/' + url
    if outputFile == "":
        print(final_url)
    else:
        fileContents += url_html(final_url)
        if archive == TRUE and i < 11:
            pageSrc = rq.get(final_url).text
            if pageSrc != "":
                archiveFile = twitterHandle + "_" + str(i) + ".html"
                f = open(archiveFile, "w")
                f.write(pageSrc)
                f.close()
        #fileContents += "\n" + final_url

fileContents += close_html()

print(twitterHandle)
print(outputFile)

if outputFile != "":
    f = open(outputFile, "w")
    f.write(fileContents)
    f.close()

#print(url)
#archivesrc = "<td class=\"url sorting_1\"><a href=\"https://web.archive.org/web/*/https://twitter.com/doctor_haber/status/1374555983314354177\">https://twitter.com/doctor_haber/status/1374555983314354177</a></td>"
#print(url_list)

# linkPattern = "<td[\s{1}]class=\"url[\s{1}]sorting_1\">(?s).*</td.*?>"
# match_results = re.search(linkPattern, archivesrc, re.IGNORECASE)
# if match_results is None:
#     print("No Matches found")
# else:
#     title = match_results.group()
#     print(title)




