from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import HTMLHeaderTextSplitter
import os
import fitz
# from llama_index.text_splitter import SentenceSplitter
# from llama_index import SimpleDirectoryReader

class TextSplitting:
    def split_character(self, file_path):
        with open(file_path, encoding="utf-8") as f:
            state_of_the_union = f.read()
        text_splitter = CharacterTextSplitter(
            separator=" ",
            chunk_size=300,
            chunk_overlap=0,
            length_function=len,
            is_separator_regex=False,
        )
        texts = text_splitter.create_documents([state_of_the_union])
        return texts
    
    # def llama_index(self, file_path):
    #     splitter = SentenceSplitter(
    #         chunk_size=100,
    #         chunk_overlap=15,
    #     )
    #     documents = SimpleDirectoryReader(
    #         input_files=[file_path]
    #     ).load_data()
    #     nodes = splitter.get_nodes_from_documents(documents)
    #     return nodes

    def split_recursive_character(self, file_path):
        with open(file_path, encoding="utf-8") as f:
            state_of_the_union = f.read()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 300, 
            chunk_overlap=20,
            length_function=len,
            is_separator_regex=False,
        )
        texts = text_splitter.create_documents([state_of_the_union])
        results = []
        for text in texts:
            results.append(text.page_content)
        return results

    def split_single_pdf(self, file_path):
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500, 
            chunk_overlap=20,
            length_function=len,
            is_separator_regex=False,
        )
        splits = []
        for doc in docs:
            doc_splits = text_splitter.split_text(doc.page_content)
            splits.extend(doc_splits)
        return splits

    def split_html(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            html_string = f.read()
        
        headers_to_split_on = [
            ("h1", "Header 1"),
            ("h2", "Header 2"),
            ("h3", "Header 3"),
            ("h4", "Header 4"),
            ("h5", "Header 5"),
            ("h6", "Header 6")
        ]

        html_splitter = HTMLHeaderTextSplitter(
            headers_to_split_on=headers_to_split_on,
        )
        html_header_splits = html_splitter.split_text(html_string)
        results = []
        for split in html_header_splits:
            if len(split.metadata)>0:
                while len(split.page_content) > 600:
                    results.append({"content":split.page_content[:600], "metadata":split.metadata})
                    split.page_content = split.page_content[570:]
                results.append({"content":split.page_content, "metadata":split.metadata})
            else:
                while len(split.page_content) > 600:
                    results.append({"content":split.page_content[:600], "metadata":{}})
                    split.page_content = split.page_content[570:]
                results.append({"content":split.page_content, "metadata":{}})
        return results


    
    def major_name_convert(self, subject):
        if subject == "AccountingFinance":
            return "af"
        elif subject == "LogisticsMaritimeStudies":
            return "lms"
        elif subject == "ManagementMarketing":
            return "mm"
        elif subject == "AppliedPhysics":
            return "ap"
        elif subject == "CivilEnvironmentalEngineering":
            return "cee"
        elif subject == "Computing":
            return "comp"
        elif subject == "ChineseHistoryCulture":
            return "chc"
        elif subject == "ElectricalElectronicEngineering":
            return "eee"
        elif subject == "English":
            return "engl"
        elif subject == "FoodScienceNutrition":
            return "fsn"
        elif subject == "IndustrialSystemsEngineering":
            return "ise"
        elif subject == "LandSurveyingGeoInformatics":
            return "lsgi"
        elif subject == "MechanicalEngineering":
            return "me"
        elif subject == "SchoolHotelTourismManagement":
            return "shtm"

    def split_syllabus(self, subject):
        ts = TextSplitting()
        subject = ts.major_name_convert(subject)
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        cur_dir += "/assets/Data/syllabus/{}".format(subject)
        results = []
        for filename in os.listdir(cur_dir):
            if filename.startswith("."):
                continue
            doc = fitz.open(cur_dir + "/" + filename)

            result = {}
            for page in doc:
                tables = page.find_tables().tables
                for table in tables:
                    for content in table.extract():
                        # Attention: ingore some row!!!!!
                        if len(content) != 2:
                            continue
                        result[content[0]] = content[1]
            results.append(result)
        return results                   


if __name__ == "__main__":
    a1 = TextSplitting()

    # texts = a1.split_character("./summer_exchange/summer_exchange_info.txt")
    # for text in texts:
    #     print(text)
    #     print("\n---------------\n")

    # nodes = a1.llama_index("./summer_exchange/summer_exchange_info.txt")
    # for node in nodes:
    #     print(node)
    #     print("\n---------------\n")
    
    # cur_dir = os.path.dirname(os.path.abspath(__file__))
    # results = a1.split_html("{}/assets/Data/summer_exchange/summer_exchange_info.html".format(cur_dir))
    # for result in results:
    #     print(result)
    #     print("\n---------------\n")
    # # for text in texts_recursive:
    #     print(type(text))
    #     print(text)
    #     print(type(text.page_content))
    #     print("\n---------------\n")

    # single_pdf_chunks = a1.split_single_pdf("./summer_exchange/Summer_Outbound_Info_Session.pdf")
    # for chunk in single_pdf_chunks:
    #     print(chunk)
    #     print("\n---------------\n")

    # with open("./syllabus/af_course_info.txt", "r", encoding="utf-8") as f:
    #     pdf_links = f.readlines()
    #     for link in pdf_links:
    #         single_pdf_chunks = a1.split_single_pdf(link.strip())
    #         for chunk in single_pdf_chunks:
    #             print(chunk)
    #             print("\n---------------\n")

    a1.split_syllabus("af")
