"""
This is a class that is used to initialize the db and other things for one user
"""

from Retriever1 import Retriever, load_split_pdf
from textSplitting import TextSplitting
from Embeddings import sentenceEmbeddings
import re

import os

class Initialization:
    def __init__(self):
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        retriever = Retriever()
        self.retriever = retriever
        self.cur_dir = cur_dir

    def summer_exchange_init(self):
        textSplitting = TextSplitting()

        spliter_results = {}
        # spliter_results['Summer_Outbound_Info_Session.pdf'] = load_split_pdf("{}/assets/Data/summer_exchange/Summer_Outbound_Info_Session.pdf".format(self.cur_dir))
        # spliter_results['Summary_Summer_Exchange.pdf'] = load_split_pdf("{}/assets/Data/summer_exchange/Summary_Summer_Exchange.pdf".format(self.cur_dir))
        spliter_results['summer_exchange_info.html'] = textSplitting.split_html("{}/assets/Data/summer_exchange/summer_exchange_info.html".format(self.cur_dir))
        # spliter_results['summer_oxbridge_info.html'] = textSplitting.split_html("{}/assets/Data/summer_exchange/summer_oxbridge_info.html".format(self.cur_dir))

        embedder = sentenceEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2",
                                      max_seq_length=256, huggingface=True)

        collection_name = self.retriever.createCollection("SummerExchange")

        for k, v in spliter_results.items():
            if k.endswith(".pdf"):
                embed_result = embedder.encode(v).tolist()
                num = len(v)
                embeddings_list = embed_result
                documents_list = v

                metadata_list = [{"doc_name": k} for i in range(num)]
                self.retriever.addDocuments(collection_name=collection_name, documents_list=documents_list, embeddings_list=embeddings_list, metadata_list=metadata_list)

            else:
                for split in v:

                    if len(split['metadata']) > 0:
                        embed_result = embedder.encode(list(split['metadata'].values())[0]+": "+split['content']).tolist()
                        embeddings_list = embed_result
                        documents_list = [list(split['metadata'].values())[0]+": "+split['content']]
                        metadata_list = [{"doc_name": k, list(split['metadata'].keys())[0]: list(split['metadata'].values())[0]}]
                    else:
                        embed_result = embedder.encode(split['content']).tolist()
                        embeddings_list = embed_result
                        documents_list = [split['content']]
                        metadata_list = [{"doc_name": k}]
                    self.retriever.addDocuments(collection_name=collection_name, documents_list=documents_list, embeddings_list=embeddings_list, metadata_list=metadata_list)

    def syllabus_init(self, subject):
        textSplitting = TextSplitting()
        syllabus = textSplitting.split_syllabus(subject)
        embedder = sentenceEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2",
                                max_seq_length=256, huggingface=True)
        collection_name = self.retriever.createCollection(subject)
        for s in syllabus:
            # pass the s if there is no "Subject Code" in the s.keys()
            if "Subject Code" not in s.keys():
                continue
            course_code = s["Subject Code"]
            information_type = ''
            for k, v in s.items():
                # check if the type of k is NoneType
                if type(k) == type(None):
                    k = information_type
                if len(k) == 0:
                    k = information_type
                k = re.sub(r'\s+', ' ', k)
                if k == "Subject Code":
                    continue
                information_type = k
                if v == None:
                    continue
                course_code = course_code.replace("\n", " ")
                v = ("This is " + course_code + " ")*3 + course_code + "'s " + k + ": " + v
                embed_result = embedder.encode([v]).tolist()
                embeddings_list = embed_result
                documents_list = [v]
                metadata_list = [{"course_code": course_code, "information_type": k}]
                self.retriever.addDocuments(collection_name=collection_name, documents_list=documents_list, embeddings_list=embeddings_list, metadata_list=metadata_list)
            print("Done for course: ", course_code)

if __name__ == "__main__":
    init = Initialization()
    # init.summer_exchange_init()
    # init.syllabus_init("AccountingFinance")
    # "IndustrialSystemsEngineering", : Attention!! docx
    # major_list = [ 
    #     "AccountingFinance", 
    #             "LogisticsMaritimeStudies", 
    #             "ManagementMarketing", 
    #             "AppliedPhysics", 
    #             "CivilEnvironmentalEngineering",
    #             "Computing",
    # "ChineseHistoryCulture",
    #             "ElectricalElectronicEngineering",
    # "English",
    #             "FoodScienceNutrition",
    #             "LandSurveyingGeoInformatics",
    #             "MechanicalEngineering",
    #             "SchoolHotelTourismManagement"]
    # for major in major_list:
    #     init.syllabus_init(major)