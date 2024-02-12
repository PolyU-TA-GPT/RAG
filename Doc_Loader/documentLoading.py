from langchain_community.document_loaders import PyPDFLoader, TextLoader, PyPDFium2Loader, MathpixPDFLoader, UnstructuredPDFLoader, PDFMinerLoader
import requests

class DocumentLoading:
    def determine_pdf(self, url):
        # determine if we can get the .pdf file or not when we type the url in browser
        response = requests.get(url)
        if response.headers['content-type'] == 'application/pdf':
            return True
        else:
            return False

    def load_syllabus1(self, file_path):
        # Using the PyPDFLoader to load the syllabus
        with open(file_path, 'r') as file:
            while (True):
                line = file.readline()
                if not line:
                    break
                # ignore the url if the return code is 404
                if line.startswith('404'):
                    continue
                url = line[4:] if line.startswith('404') else line  # strip '404' from the beginning of the line
                if DocumentLoading.determine_pdf(self, url.strip()):
                    loader = PyPDFLoader(url.strip())  # strip() is used to remove leading/trailing whitespace
                    loader.load_and_split()

    def load_syllabus2(self, file_path):
        # Using the PyPDFium2Loader to load the syllabus
        # type after load: list
        with open(file_path, 'r') as file:
            while (True):
                line = file.readline()
                if not line:
                    break
                # ignore the url if the return code is 404
                if line.startswith('404'):
                    continue
                url = line[4:] if line.startswith('404') else line
                if DocumentLoading.determine_pdf(self, url.strip()):
                    loader = PyPDFium2Loader(url.strip())
                    loader.load()

    # def load_syllabus3(file_path):
    #     # Using MathPixPDFLoader to load the syllabus
    #     with open(file_path, 'r') as file:
    #         while(True):
    #             line = file.readline()
    #             if not line:
    #                 break
    #             # ignore the url if the return code is 404
    #             if line.startswith('404'):
    #                 continue
    #             url = line[4:] if line.startswith('404') else line
    #             loader = MathpixPDFLoader(url.strip())
    #             data = loader.load()
    #             print(type(data))

    # def load_syllabus4(file_path):
    #     # Using UnstructuredPDFLoader to load the syllabus
    #     with open(file_path, 'r') as file:
    #         while(True):
    #             line = file.readline()
    #             if not line:
    #                 break
    #             # ignore the url if the return code is 404
    #             if line.startswith('404'):
    #                 continue
    #             url = line[4:] if line.startswith('404') else line
    #             loader = UnstructuredPDFLoader(url.strip())
    #             data = loader.load()
    #             print(type(data))

    def load_syllabus5(self, file_path):
        # Using PDFMiner to load the syllabus
        # type after load: list
        with open(file_path, 'r') as file:
            while (True):
                line = file.readline()
                if not line:
                    break
                # ignore the url if the return code is 404
                if line.startswith('404'):
                    continue
                url = line[4:] if line.startswith('404') else line
                if DocumentLoading.determine_pdf(self, url.strip()):
                    loader = PDFMinerLoader(url.strip())
                    loader.load()

    def load_text(self, file_path):
        loader = TextLoader(file_path)
        loader.load()

    def load_single_pdf(self, file_path):
        loader = PyPDFLoader(file_path)
        loader.load_and_split()

    def load_pdf_within_links(self, file_path):
        with open(file_path, 'r') as file:
            while (True):
                line = file.readline()
                if not line:
                    break
                # ignore the url if the return code is 404
                if line.startswith('404'):
                    continue
                url = line[4:] if line.startswith('404') else line
                # load the url which contains 'pdf'
                if 'pdf' in url.strip() and DocumentLoading.determine_pdf(self, url.strip()):
                    loader = PyPDFLoader(url.strip())
                    loader.load_and_split()

if __name__ == "__main__":
# Example of usage
    dl = DocumentLoading()
    # return type is list
    dl.load_syllabus5("./Data/syllabus/af_course_info.txt")
    # return type is <Document...>
    dl.load_syllabus1("./Data/syllabus/aae_course_info.txt")
    # return type is list
    dl.load_syllabus2("./Data/syllabus/mm_course_info.txt")
    # load the pure text file from website
    dl.load_text("./Data/summer_exchange/summer_exchange_info.txt")
    # load the pdf file within links
    dl.load_pdf_within_links("./Data/summer_exchange/summer_exchange_links.txt")
    # load the sigle pdf file
    dl.load_single_pdf("./Data/summer_exchange/Summer_Outbound_Info_Session.pdf")
    print("____Done____")