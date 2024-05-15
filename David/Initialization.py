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
        try:
            retriever.delete_collection("SummerExchange")
        except ValueError:
            pass
        try:
            retriever.delete_collection("AccountingFinance")
        except ValueError:
            pass
        try:
            retriever.delete_collection("Computing")
        except ValueError:
            pass
        try:
            retriever.delete_collection("Scholarship")
        except ValueError:
            pass

        self.retriever = retriever
        self.cur_dir = cur_dir

    def summer_exchange_init(self):
        textSplitting = TextSplitting()
        spliter_results = {}
        spliter_results['Summer_Outbound_Info_Session.pdf'] = load_split_pdf("{}/assets/Data/summer_exchange/Summer_Outbound_Info_Session.pdf".format(self.cur_dir))
        spliter_results['Harvard_exchange.pdf'] = load_split_pdf("{}/assets/Data/summer_exchange/Harvard_exchange.pdf".format(self.cur_dir))
        #spliter_results['summer_exchange_info.html'] = textSplitting.split_html("{}/assets/Data/summer_exchange/summer_exchange_info.html".format(self.cur_dir))
        # spliter_results['summer_oxbridge_info.html'] = textSplitting.split_html("{}/assets/Data/summer_exchange/summer_oxbridge_info.html".format(self.cur_dir))

        embedder = sentenceEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2",
                                      max_seq_length=256, huggingface=True)

        for k, v in spliter_results.items():
            if k.endswith(".pdf"):
                collection_name = self.retriever.createCollection("SummerExchange")
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
                    if k == "summer_exchange_info.html":
                        collection_name = self.retriever.createCollection("SummerExchange")
                    else:
                        collection_name = self.retriever.createCollection("SummerOxbridge")
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
                v = ("This is " + course_code +  "'s " + k +" ")*3 + ": " + v
                embed_result = embedder.encode([v]).tolist()
                embeddings_list = embed_result
                documents_list = [v]
                metadata_list = [{"course_code": course_code, "information_type": k}]
                self.retriever.addDocuments(collection_name=collection_name, documents_list=documents_list, embeddings_list=embeddings_list, metadata_list=metadata_list)
            print("Done for course: ", course_code)

    def schloarship_init(self):
        embedder = sentenceEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2",
                                      max_seq_length=256, huggingface=True)
        collection_name = self.retriever.createCollection("Scholarship")
        spliter_result = load_split_pdf("{}/assets/Data/scholarship/HKJC_Scholarship_2023-Info_Sheet.pdf".format(self.cur_dir))
        embed_result = embedder.encode(spliter_result).tolist()
        num = len(spliter_result)
        embeddings_list = embed_result
        documents_list = spliter_result
        metadata_list = [{"doc_name": "HKJC_Scholarship_2023-Info_Sheet.pdf"} for i in range(num)]
        self.retriever.addDocuments(collection_name=collection_name, documents_list=documents_list, embeddings_list=embeddings_list, metadata_list=metadata_list)

    def WIE_init(self):
        embedder = sentenceEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2",
                                      max_seq_length=256, huggingface=True)
        collection_name = self.retriever.createCollection("WIE")
        spliter_result = load_split_pdf("{}/assets/Data/WIE/WIE.pdf".format(self.cur_dir))
        embed_result = embedder.encode(spliter_result).tolist()
        num = len(spliter_result)
        embeddings_list = embed_result
        documents_list = spliter_result
        metadata_list = [{"doc_name": "WIE.pdf"} for i in range(num)]
        self.retriever.addDocuments(collection_name=collection_name, documents_list=documents_list, embeddings_list=embeddings_list, metadata_list=metadata_list)

    def Minor_init(self):
        embedder = sentenceEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2",
                                      max_seq_length=256, huggingface=True)
        collection_name = self.retriever.createCollection("Minor")
        spliter_result = load_split_pdf("{}/assets/Data/Minor/AMA_Minor.pdf".format(self.cur_dir))
        embed_result = embedder.encode(spliter_result).tolist()
        num = len(spliter_result)
        embeddings_list = embed_result
        documents_list = spliter_result
        metadata_list = [{"doc_name": "AMA_Minor.pdf"} for i in range(num)]
        self.retriever.addDocuments(collection_name=collection_name, documents_list=documents_list, embeddings_list=embeddings_list, metadata_list=metadata_list)

    def CAR_init(self):
        embedder = sentenceEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2",
                                      max_seq_length=256, huggingface=True)
        collection_name = self.retriever.createCollection("CAR")
        spliter_result = load_split_pdf("{}/assets/Data/CAR/CAR_requirements.pdf".format(self.cur_dir))
        embed_result = embedder.encode(spliter_result).tolist()
        num = len(spliter_result)
        embeddings_list = embed_result
        documents_list = spliter_result
        metadata_list = [{"doc_name": "CAR_requirements.pdf"} for i in range(num)]
        self.retriever.addDocuments(collection_name=collection_name, documents_list=documents_list, embeddings_list=embeddings_list, metadata_list=metadata_list)

    def SRS_init(self):
        embedder = sentenceEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2",
                                      max_seq_length=256, huggingface=True)
        collection_name = self.retriever.createCollection("SRS")
        spliter_result = load_split_pdf("{}/assets/Data/SRS/SRS_info.pdf".format(self.cur_dir))
        embed_result = embedder.encode(spliter_result).tolist()
        num = len(spliter_result)
        embeddings_list = embed_result
        documents_list = spliter_result
        metadata_list = [{"doc_name": "SRS_info.pdf"} for i in range(num)]
        self.retriever.addDocuments(collection_name=collection_name, documents_list=documents_list, embeddings_list=embeddings_list, metadata_list=metadata_list)

if __name__ == "__main__":
    init = Initialization()
    init.summer_exchange_init()
    init.syllabus_init("AccountingFinance")
    init.syllabus_init("Computing")
    init.schloarship_init()
    init.WIE_init()
    init.Minor_init()
    init.CAR_init()
    init.SRS_init()
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