import glob
import os
from bs4 import BeautifulSoup
import bs4
import string
from docx import Document
import sys
import numpy as np
from itertools import islice
from collections import deque
import sys
import csv


##Full-Document = the original document without any modifications 
##Citation = The metadata, usually includes author, date, credentials, and a URL or paper location
##Extract = the human made underlined portions of the document. Forms an extractive summary. 
##Abstract = the human abstractively made summary and the "arguement" made by the debater
##OriginalDebateFileName = The original word document where this card was find from Open Evidence - helps with tracability


num_of_cards = 0
#os.chdir("/home/lain/lain/CX_DB8/card_data")

card_set = set() ## Force the documents to be unique - still possible for near duplicates to filter through though - seems rare in practice..

cards = dict()

location_of_html5 = "/home/lain/lain/CX_DB8/card_data/all_data/*.html5" 
output_file_name = 'debateall.csv'

with open(output_file_name, 'a') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["Full-Document", "Citation", "Extract", "Abstract", "#CharsDocument", "#CharsAbstract", "#CharsExtract", "#WordsDocument", "#WordsAbstract", "#WordsExtract", "AbsCompressionRatio", "ExtCompressionRatio", "OriginalDebateFileName"]) ##write the header
    for file in glob.glob(location_of_html5):
        print("File parsed: " + file)
        with open(file) as fp:
            soup = BeautifulSoup(fp, "lxml")
            all_card_tags = soup.find_all('h4')
            print(num_of_cards)
            for h4 in all_card_tags:
                try:
                    abstract = h4.text ## this is the abstract 
                    abs_length = len(abstract) # character length of abstract 
                    abs_word_length = len(abstract.split())
                    citation = h4.find_next("p").text ##get the citation information
                    card = h4.find_next("p").find_next("p")
                    full_doc = card.text ##get the full document
                    doc_length = len(full_doc)
                    doc_word_length = len(full_doc.split())
                    if doc_word_length >= 20:
                        if full_doc not in card_set:
                            card_set.add(full_doc)
                            extract_tags = card.find_all("span") ##should get anything underlined
                            list_of_inner_text = [x.text for x in extract_tags]
                            extract = ' '.join(list_of_inner_text)
                            extract_len = len(extract)
                            extract_word_length = len(extract.split())
                            current_file = os.path.basename(file)
                            compression_ratio_abs = abs_word_length / doc_word_length
                            compression_ratio_extract = extract_word_length / doc_word_length
                            if extract_word_length > 10:
                                if abs_word_length > 3:
                                    if compression_ratio_abs < 1: 
                                        if compression_ratio_extract < 1:
                                            row_to_write = [full_doc, citation, extract, abstract, doc_length, abs_length, extract_len, doc_word_length, abs_word_length, extract_word_length, compression_ratio_abs, compression_ratio_extract, current_file]
                                            csvwriter.writerow(row_to_write)
                                            num_of_cards += 1
                except AttributeError:
                    pass      

print("written to disk!")
print("Number of cards processed: " + str(num_of_cards))


