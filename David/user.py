"""

This is the place to begin the user interface for the program.

Auther: Ding Honghe

"""

from Initialization import Initialization
from Generator2 import Generator2
from Generator1 import *
from Retriever1 import Retriever
from Embeddings import sentenceEmbeddings
import os
import uuid
import json
import time

# init = Initialization()
# init.summer_exchange_init()

embedder = sentenceEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2",
                              max_seq_length=256, huggingface=True)
retriever = Retriever()
cur_dir = os.path.dirname(os.path.abspath(__file__))
separate_line = "-"*60


def main_page():
    print(separate_line)
    print("Welcome to this system!")
    print(separate_line)
    print("1. Summer Exchange")
    print("2. Syllabus")
    print("3. CAR")
    print("4. Minor")
    print("5. Scholarship")
    print("6. SRS")
    print("7. WIE")
    print("8. Exit")
    print(separate_line)
    print("Please enter the number of the module you want to use:")
    module = input()
    return module

def major_display():
    print(separate_line)
    print("Major list")
    print(separate_line)
    print("1. Accounting and Finance")
    print("2. Applied Physics")
    print("3. Chinese History Culture")
    print("4. Civil Environmental Engineering")
    print("5. Computing and AI")
    print("6. Electical and Electronic Engineering")
    print("7. English")
    print("8. Food Science and Nutrition")
    print("9. Land Surveying and Geo-Informatics")
    print("10. Logistics Maritime Studies")
    print("11. Management Marketing")
    print("12. Mechanical Engineering")
    print("13. School of Hotel and Tourism Management")
    print(separate_line)
    print("Please enter the number of the major you want to use:")
    major = input()
    return major

def syllabus_query(major_num, history, rephrase_num=1):
    major = ""
    if major_num == "1":
        major = "AccountingFinance"
    elif major_num == "2":
        major = "AppliedPhysics"
    elif major_num == "3":
        major = "ChineseHistoryCulture"
    elif major_num == "4":
        major = "CivilEnvironmentalEngineering"
    elif major_num == "5":
        major = "Computing"
    elif major_num == "6":
        major = "ElecticalElectronicEngineering"
    elif major_num == "7":
        major = "English"
    elif major_num == "8":
        major = "FoodScienceNutrition"
    elif major_num == "9":
        major = "LandSurveyingGeoInformatics"
    elif major_num == "10":
        major = "LogisticsMaritimrStudies"
    elif major_num == "11":
        major = "ManagementMarketing"
    elif major_num == "12":
        major = "MechanicalEngineering"
    elif major_num == "13":
        major = "SchoolHotelTourismManagement"
    else:
        print("Invalid input!")
        return
    collection_name = major
    print(separate_line)
    print("Your Query:")
    print(separate_line)
    query_text = input()
    print(separate_line)
    print("rephrasing...")
    rephrase_num = rephrase_num
    #query_list = rephrase(question=query_text, rephrase_num=rephrase_num, temp=0)
    query_list = Generator2.strengthenUserQuestion(query_text, rephrase_num)
    query_list.append(query_text)
    print(query_list)
    print("rephrase done!")
    print(separate_line)
    print("querying...")
    query_embeddings = embedder.encode(query_list).tolist()  # tensor to list
    query_result = retriever.query(collection_name=collection_name, query_embeddings=query_embeddings)

    query_result_chunks = [j for i in range (rephrase_num + 1) for j in query_result["documents"][i]]
    query_result_ids = [j for i in range (rephrase_num + 1) for j in query_result["ids"][i]]
    with open("{}/assets/retrieval/{}_{}.json".format(cur_dir, collection_name, str(uuid.uuid4())).format(),
              'w') as retrieval:
        json.dump(query_result, retrieval, indent=4)

    num = len(query_result_chunks)
    for i in range(num):
        query_result_chunks[i] = query_result_chunks[i].replace('\n',' ')

    context = '//\n'.join(["@" + query_result_ids[i] + "//" + query_result_chunks[i] for i in range(num)])
    with open("{}/assets/context/{}_{}.txt".format(cur_dir, collection_name, str(uuid.uuid4())).format(),
              'w') as context_file:
        context_file.write(context)
    print("query done!")
    print(separate_line)
    print("This is context")
    print(context)
    # result = generate(context=context, question=query_text, temp=0)
    # result = Generator2.generate(context=context, question=query_text, temp=0)
    # # for i in range(1,10,2):
    # #     if result.find('FINAL ANSWER:')<0:
    # #         time.sleep(5)
    # #         #result = Generator2.generate(context,query_text,temp=i/10)
    # #         result = generate(context=context, question=query_text, temp=i/10)
    # #         print('retrying with temperature:',i/10)
    # #     else:
    # #         break
    # # result = result[result.find('FINAL ANSWER:')+14:]
    # print(result)
    # print(separate_line)
    results = []
    for question in query_list:
        result = Generator2.generate(context, question, history)
        # print(result)
        # for i in range(1, 10, 2):
        #     if result.find('FINAL ANSWER:') < 0:
        #         time.sleep(5)
        #         result = Generator2.generate(context, question, temp=i / 10)
        #         print('retrying with temperature:', i / 10)
        #     else:
        #         break
        # result = result[result.find('FINAL ANSWER:') + 14:]
        results += [result]
        # print()
        # print('- '*40)
        # print(result)
        # print('- '*40)

        # print(results)

    summary = Generator2.AnswersToFinalAnswer(results)
    print(summary)
    return query_text, summary

def david_query(collection_name, history, rephrase_num=1):
    collection_name = collection_name
    print(separate_line)
    print("Your Query:")
    print(separate_line)
    query_text = input()
    
    print("rephrasing...")
    rephrase_num = rephrase_num
    #query_list = rephrase(question=query_text, rephrase_num=rephrase_num, temp=0)
    query_list = Generator2.strengthenUserQuestion(query_text, rephrase_num)
    query_list.append(query_text)
    print(query_list)
    print("rephrase done!")
    print(separate_line)
    print("querying...")
    query_embeddings = embedder.encode(query_list).tolist()  # tensor to list
    query_result = retriever.query(collection_name=collection_name, query_embeddings=query_embeddings)

    query_result_chunks = [j for i in range (rephrase_num + 1) for j in query_result["documents"][i]]
    query_result_ids = [j for i in range (rephrase_num + 1) for j in query_result["ids"][i]]
    with open("{}/assets/retrieval/{}_{}.json".format(cur_dir, collection_name, str(uuid.uuid4())).format(),
              'w') as retrieval:
        json.dump(query_result, retrieval, indent=4)

    num = len(query_result_chunks)
    for i in range(num):
        query_result_chunks[i] = query_result_chunks[i].replace('\n',' ')

    context = '//\n'.join(["@" + query_result_ids[i] + "//" + query_result_chunks[i] for i in range(num)])
    with open("{}/assets/context/{}_{}.txt".format(cur_dir, collection_name, str(uuid.uuid4())).format(),
              'w') as context_file:
        context_file.write(context)
    print("query done!")
    print(separate_line)
    print("This is context")
    print(context)

    results = []
    for question in query_list:
        result = Generator2.generate(context, question, history)
        # print(result)
        # for i in range(1, 10, 2):
        #     if result.find('FINAL ANSWER:') < 0:
        #         time.sleep(5)
        #         result = Generator2.generate(context, question, temp=i / 10)
        #         print('retrying with temperature:', i / 10)
        #     else:
        #         break
        # result = result[result.find('FINAL ANSWER:') + 14:]
        results += [result]
        # print()
        # print('- '*40)
        # print(result)
        # print('- '*40)

        # print(results)

    summary = Generator2.AnswersToFinalAnswer(results)
    print(summary)
    return query_text, summary

def summer_exchange_query(history, rephrase_num=1):
    collection_name = "SummerExchange"
    print(separate_line)
    print("Your Query:")
    print(separate_line)
    query_text = input()
    
    print("rephrasing...")
    rephrase_num = rephrase_num
    #query_list = rephrase(question=query_text, rephrase_num=rephrase_num, temp=0)
    query_list = Generator2.strengthenUserQuestion(query_text, rephrase_num)
    query_list.append(query_text)
    print(query_list)
    print("rephrase done!")
    print(separate_line)
    print("querying...")
    query_embeddings = embedder.encode(query_list).tolist()  # tensor to list
    query_result = retriever.query(collection_name=collection_name, query_embeddings=query_embeddings)

    query_result_chunks = [j for i in range (rephrase_num + 1) for j in query_result["documents"][i]]
    query_result_ids = [j for i in range (rephrase_num + 1) for j in query_result["ids"][i]]
    with open("{}/assets/retrieval/{}_{}.json".format(cur_dir, collection_name, str(uuid.uuid4())).format(),
              'w') as retrieval:
        json.dump(query_result, retrieval, indent=4)

    num = len(query_result_chunks)
# for i in range(len(retrivedContent)):
#         retrivedContent[i] = retrivedContent[i].replace('\n',' ')
    
    for i in range(num):
        query_result_chunks[i] = query_result_chunks[i].replace('\n',' ')


    context = '//\n'.join(["@" + query_result_ids[i] + "//" + query_result_chunks[i] for i in range(num)])
    with open("{}/assets/context/{}_{}.txt".format(cur_dir, collection_name, str(uuid.uuid4())).format(),
              'w') as context_file:
        context_file.write(context)
    print("query done!")
    print(separate_line)
    print("This is context")
    print(context)
    # result = generate(context=context, question=query_text, temp=0)

    results = []
    for question in query_list:
        result = Generator2.generate(context, question, history)
        # print(result)
        # for i in range(1, 10, 2):
        #     if result.find('FINAL ANSWER:') < 0:
        #         time.sleep(5)
        #         result = Generator2.generate(context, question, temp=i / 10)
        #         print('retrying with temperature:', i / 10)
        #     else:
        #         break
        # result = result[result.find('FINAL ANSWER:') + 14:]
        results += [result]
        # print()
        # print('- '*40)
        # print(result)
        # print('- '*40)

        # print(results)


    summary = Generator2.AnswersToFinalAnswer(results)
    print(summary)
    return query_text, summary


    # result = Generator2.generate(context=context, question=query_text, temp=0)
    #
    # # for i in range(1,10,2):
    # #     if result.find('FINAL ANSWER:')<0:
    # #         time.sleep(5)
    # #         # result = Generator2.generate(context,query_text,temp=i/10)
    # #         result = generate(context=context, question=query_text, temp=i/10)
    # #         print('retrying with temperature:',i/10)
    # #     else:
    # #         break2
    # # result = result[result.find('FINAL ANSWER:')+14:]
    # # result = result[result.find('ANSWER:')+8:]
    # print(result)
    # print(separate_line)

if __name__ == "__main__":
    module = main_page()
    history = {"question": "", "answer": ""}
    while module != "8":
        if module == "1":
            query, answer  = summer_exchange_query(history)
            history["question"] = query
            history["answer"] = answer
            print("Do you want to continue? (y/n)")
            continue_or_not = input()
            if continue_or_not == "y":
                module = main_page()
            else:
                break
        elif module == "2":
            major = major_display()
            query, answer = syllabus_query(major, history)
            history["question"] = query
            history["answer"] = answer
            print("Do you want to continue? (y/n)")
            continue_or_not = input()
            if continue_or_not == "y":
                module = main_page()
            else:
                break
        elif module == "3":
            query, answer =  david_query("CAR", history)
            history["question"] = query
            history["answer"] = answer
            print("Do you want to continue? (y/n)")
            continue_or_not = input()
            if continue_or_not == "y":
                module = main_page()
            else:
                break
        elif module == "4":
            query, answer = david_query("Minor", history)
            history["question"] = query
            history["answer"] = answer
            print("Do you want to continue? (y/n)")
            continue_or_not = input()
            if continue_or_not == "y":
                module = main_page()
            else:
                break
        elif module == "5":
            query, answer = david_query("Scholarship", history)
            history["question"] = query
            history["answer"] = answer
            print("Do you want to continue? (y/n)")
            continue_or_not = input()
            if continue_or_not == "y":
                module = main_page()
            else:
                break
        elif module == "6":
            query, answer = david_query("SRS", history)
            history["question"] = query
            history["answer"] = answer
            print("Do you want to continue? (y/n)")
            continue_or_not = input()
            if continue_or_not == "y":
                module = main_page()
            else:
                break
        elif module == "7":
            query, answer = david_query("WIE", history)
            history["question"] = query
            history["answer"] = answer
            print("Do you want to continue? (y/n)")
            continue_or_not = input()
            if continue_or_not == "y":
                module = main_page()
            else:
                break
        elif module == "8":
            break
        else:
            print("Invalid input!")
            module = main_page()



# What are COMP1433's intended learning outcomes?
# What are AF3313's pre-requisites?
# What are summer exchange types of PolyU?
# What are universites in Singapore that provided summer exchange?