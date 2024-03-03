import requests
import os


cur_dir = os.path.dirname(os.path.abspath(__file__))

def download_course(subject):
    with open("{}/{}_course_info.txt".format(cur_dir, subject), "r", encoding="utf-8") as f:
        pdf_links = f.readlines()
        for url in pdf_links:
            url = url.strip()
            response = requests.get(url)
            if response.status_code != 200:
                continue
            local_file_path = "{}/{}/{}".format(cur_dir, subject, url.split("/")[-1].strip())
            response.raise_for_status()

            with open(local_file_path, "wb") as file:
                file.write(response.content)

# download_course("abct")
# download_course("af")
# download_course("ap")
# download_course("bme")
# download_course("cbs")
# download_course("cee")
# download_course("chc")
# download_course("comp")
# download_course("eee")
# download_course("engl")
# download_course("fsn")
# download_course("lms")
# download_course("ise")
# download_course("lsgi")
# download_course("me")
# download_course("mm")
# download_course("shtm")
            
def rename(subject):
    folder_path = "{}/{}".format(cur_dir, subject)

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # 确保是文件而不是文件夹
        if os.path.isfile(file_path):
            new_file_path = file_path + ".pdf"
            
            # 重命名文件
            os.rename(file_path, new_file_path)

rename("bme")
