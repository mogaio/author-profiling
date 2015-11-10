import os
import csv
import punctuation as punctu
from string import punctuation
from utils import *
import pandas as pd
import pprint as pp
import NER_tagger
import pos_tagging
import html_links
import countQuote
import topics_mean_stdev
import json
from av_readability import av_readability

directory = '../../data/koppel/blogs'
outdir = 'output/'

# author = get_author_info(directory+'/truth.txt')
authorFileNames = os.listdir(directory)

def features_from(docs):
    feature = {}
    feature['punctuation'] = punctu.extract_from_xml(docs)
    feature['pos'] = pos_tagging.distribution(pos_tagging.get_POS_Tags(docs))
    feature['NER'] = NER_tagger.get_NER_tags(docs)
    feature['hyperlinks_info'] = html_links.get_hyperlink_info(docs)
    feature["topic_var"] = topics_mean_stdev.getTopics(docs)
    feature["quotes"] = countQuote.getquotes(docs)
    feature["readability"] = av_readability(docs)
    return feature


def main():
    for file in filter_xml(authorFileNames):
        ofilePath = 'output/'+file.split('.')[0]+".json"
        if os.path.isfile(ofilePath) == False:
            print file
            authorInfo = get_author_info(file)
            author_id = authorInfo['Id']
            author = {}
            file_path = directory+"/"+file
            docs = gettext(file_path)
            author[author_id] = features_from(docs)
            author[author_id]['Gender'] = authorInfo['Gender']
            author[author_id]['Age'] = authorInfo['Age']

            with open(ofilePath,'w') as fp:
                json.dump(author[author_id],fp, indent=4)
        else:
            print file+":skip"

        # doing a break jsut to save testing time
        break

    # printing a sample
    # pp.pprint(author)

if __name__ == "__main__":
    main()

