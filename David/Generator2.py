class Generator2:
    """A class to generate questions and answers using RAG model."""
    PRINTDETAIL = True
    @staticmethod
    def generate(context,question, history:dict, Local=False,temp=0):
        """Generate an answer to the user question based on the given context.
        Parameters
        ----------
        context : str
            The context to generate the answer.
        question : str
            The user question.
        history: dict
            The history of the conversation.
            {
                "question": question,
                "answer": answer
            }
        Local : bool
            Whether to use local model or not.
        temp : float
            The temperature of the model.
        Returns
        -------
        str
            The generated answer.
        """
        if Local:
            # from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
            # from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
            # from transformers import file_utils
            # print(file_utils.default_cache_path)
            # import torch
            # import intel_extension_for_pytorch as ipex
            # torch.manual_seed(0)
            
            # path = 'openbmb/MiniCPM-2B-dpo-bf16'
            # tokenizer = AutoTokenizer.from_pretrained(
            #     path,
            #     #low_cpu_mem_usage=True,
            # )
            
            # model = AutoModelForCausalLM.from_pretrained(
            #     path,
            #     low_cpu_mem_usage=True,
            #     torch_dtype=torch.bfloat16,
            #     device_map='auto',
            #     trust_remote_code=True
            # )
            
            # model.eval()
            # model = ipex.llm.optimize(
            #     model,
            #     dtype=torch.bfloat16,
            #     inplace=True,
            #     deployment_mode=True
            # )
            
            
            # #responds, history = model.chat(
            # #    tokenizer,
            # #    "山东省最高的山是哪座山, 它比黄山高还是矮？差距多少？",
            # #    temperature=0.8,
            # #    top_p=0.8
            # #)
            # #print(responds)
            # print(model.device)
            # #print()
            
            
            # pipe = pipeline(
            #     "text-generation",
            #     model=model,
            #     tokenizer=tokenizer,
            #     batch_size=1,
            #     max_new_tokens=2,
            #     num_beams=4,
            #     do_sample=True,
            #     top_p=0.8,
            #     temperature=0.8,
            #     bos_token_id=1,
            #     eos_token_id=2,
            #     pad_token_id=2,
            #     repetition_penalty=1.5
            # )
            
            # #import time
            # #t = time.time()
            # #dt=0
            # #response = ''
            # #prompt = "Hey, "
            # #print(prompt)
            # #for i in range(50):
            # #    t = time.time()
            # #    inputs = tokenizer(response, return_tensors="pt")
            # #    generate_ids = model.generate(
            # #        inputs.input_ids, 
            # #        max_new_tokens=1,
            # #        bos_token_id=1,
            # #        eos_token_id=2,
            # #        pad_token_id=2,
            # #        use_cache = False
            # #    )
            # #    response = tokenizer.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
            # #    print('- '*40+'\n',i,time.time()-t-dt,(time.time()-t)/(1+i),response)
            # #    dt=time.time()-t
            
            # hf = HuggingFacePipeline(pipeline=pipe,max_new_tokens=200)
            pass
        else:
            from langchain_openai import ChatOpenAI
            from os import getenv
            
            # gets API Key from environment variable OPENAI_API_KEY
            hf = ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            openai_api_key="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",#getenv("OPENROUTER_API_KEY"),
            model_name="openai/gpt-4o",
            temperature=temp
            )
        #------------------------------------------------------------
        
        from langchain.prompts import PromptTemplate
        # template = """Question: {question}
        # Answer: Let's think step by step, """
        template = """Use the following pieces of context to answer the question at the end. 

    Provide precise answer based on the context and attach the source coordinate SC of your answer in [SC]. If there are Multiple Sources, use all of them in the answer and attach the source coordinates in [SC]. Do not cut the SC if it is too long.
    ```
    ------------------------------------------------------------
        @0a3f01-47bac0d//HAER is a current student of CBS//
        @01f588-5a68e3f//HAER is a boy//
        @e956dd-00a1b2//HAER is from USA//
        END OF RESULT//
    ------------------------------------------------------------
        Question: Who is HAER?
    ------------------------------------------------------------
    ```
    Think and response with [@SC] in several complete and logical sentense: 
    ```
    THOUGHT: The question ~~Who is HAER?~~ is asking for HAER's information.

    ANSWER: HAER is a student from USA[SC: @01f588] and currently in CBS[SC: @0a3f01-47bac0d].

    THOUGHT: 'HAER is a student from USA[SC: @01f588-5a68e3f]' is not related to '@01f588//HAER is a boy//'.

    FINAL ANSWER: As far as I know, HAER is a boy from USA[SC: @e956dd-00a1b2, @01f588-5a68e3f] and currently a student of CBS[SC: @0a3f01-47bac0d].
    ```

    If don't know the answer or the question is not related, think and response like this: 
    ```
    THOUGHT: The question ~~xxx~~ is asking for xxx.

    ANSWER: No information for 'xxx'.

    THOUGHT: 'xxx' is NOT related to the context.

    FINAL ANSWER: 'xxx' is NOT related to the context[SC: NO INFORMATION].
    ```

    Now do the real task below!
    If the history question and answers is not empty, please refer to the history question and answer if history is related to the current question,.
    The history question is {history_question}
    The history answer is {history_answer}
    ------------------------------------------------------------
        {context}
    ------------------------------------------------------------
        Question: {question}
    ------------------------------------------------------------

    """
        
        # question = "Who is Mao ZeDong?"
        prompt = PromptTemplate.from_template(template)
        
        chain = prompt | hf
        
        res = chain.invoke({"context":context,"question": question,
                            "history_question": history["question"], "history_answer": history["answer"]}).content

        if Generator2.PRINTDETAIL:
            print(res)
            print()
        return res

    def strengthenUserQuestion(question,num=1,temp=0):
        """ Strengthen the user question to make it more precise and clear for RAG, but avoid changing the meaning of the question.
        Parameters
        ----------
        question : str
            The user question.
        num : int
            The number of strong questions to generate.
        temp : float
            The temperature of the model.
        Returns
        -------
        list
            A list of strong questions.
        """
        from langchain_openai import ChatOpenAI
        from os import getenv
        
        # gets API Key from environment variable OPENAI_API_KEY
        hf = ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            openai_api_key="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",#getenv("OPENROUTER_API_KEY"),
            temperature=temp
        )

        #------------------------------------------------------------
        from langchain.prompts import PromptTemplate
        template = """Strengthen the question to make it more precise and clear for RAG, but avoid changing the meaning of the question. Do not add any new information. 
For example:
```OUTPUT 5 Different STRONG QUESTIONS
QUESTION: Dragon friit?
```
STRONG QUESTION (1/5): What is the name of the fruit that is also called "Dragon fruit"?
STRONG QUESTION (2/5): Is "Dragon fruit" the name of a fruit?
STRONG QUESTION (3/5): Do you know the name of the fruit that is also called "Dragon fruit"?
STRONG QUESTION (4/5): Tell me more about the fruit that is also called "Dragon fruit".
STRONG QUESTION (5/5): Give me more information about the fruit that is also called "Dragon fruit".
------------------------------------------------------------
Now do the real task below!
```OUTPUT {num1} Different STRONG QUESTIONS
QUESTION: {question}
```
STRONG QUESTION (1/{num2}):"""

        prompt = PromptTemplate.from_template(template)

        chain = prompt | hf

        res = chain.invoke({"question": question,"num1":num,"num2":num}).content
        
        if Generator2.PRINTDETAIL:
            print(res)
            print()


        resList = res.split('\n')
        for i in range(len(resList)):
            if resList[i].find('STRONG QUESTION')>=0:
                resList[i] = resList[i][resList[i].find(':')+2:]
        return resList

    def AnswersToFinalAnswer(answers,temp=0):
        """ Combine the answers into a single coherent response. 
        Parameters
        ----------
        answers : list
            A list of answers.
        temp : float
            The temperature of the model.
        Returns
        -------
        str
            The combined answer.
        """

        from langchain_openai import ChatOpenAI
        from os import getenv
        
        # gets API Key from environment variable OPENAI_API_KEY
        hf = ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            openai_api_key="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",#getenv("OPENROUTER_API_KEY"),
            temperature=temp
        )

        #------------------------------------------------------------
        from langchain.prompts import PromptTemplate
        template = """Combine the answers into a single coherent response. 
You should use as much information IN DETAIL from the answers as possible to form the FINAL ANSWER. The response should be a single coherent paragraph. Avoid repeating the same information multiple times. 
Preserve [SC] in the FINAL ANSWER. If there are multiple answers, use the information from all of them to form the FINAL ANSWER in DETAIL.
For example:
```ANSWERS
ANSWER (1/5): The capital of France is Paris[SC: @1a2-b3c-4f]
ANSWER (2/5): Paris is the capital of France[SC: @1a2-b3c-4f, @4d5-e6f-00]
ANSWER (3/5): Paris has been the capital of France since the 12th century[SC: @4d5-e6f-00]
ANSWER (4/5): Napoleon Bonaparte was crowned Emperor of France in Notre-Dame Cathedral in Paris[SC: @7g8-h9i-f0]
ANSWER (5/5): The Eiffel Tower is located in Paris[SC: @j1k-2l3-4m]
```FINAL ANSWER IN DETAIL WITH SC:
Paris is the capital of France[SC: @1a2-b3c-4f, @4d5-e6f-00]. It has been the capital since the 12th century[SC: @4d5-e6f-00]. Napoleon Bonaparte was crowned Emperor of France in Notre-Dame Cathedral in Paris[SC: @7g8-h9i-f0]. The Eiffel Tower is located in Paris[SC: @j1k-2l3-4m].
------------------------------------------------------------
Now do the real task below!
```ANSWERS
{answers}
```FINAL ANSWER IN DETAIL WITH SC:
"""
        prompt = PromptTemplate.from_template(template)
        
        chain = prompt | hf

        for i in range(len(answers)):
            answers[i] = 'ANSWER ('+str(i+1)+'/'+str(len(answers))+'): '+answers[i]
            
        res = chain.invoke({"answers": '\n'.join(answers)}).content

        if Generator2.PRINTDETAIL:
            print(res)
            print()

        return res

if __name__ == '__main__':
    import argparse
    import time
    parser = argparse.ArgumentParser()
    parser.add_argument("question", help="Input User question", type=str, default="Who is CHAI?", nargs='?')
    args = parser.parse_args()
    question = args.question

    context = """
    @00ff01//CWC is an undergraduate student//
    @03a4c2//CWC is from China//
    @052b13//In 2022, Hong Kong PolyU accepted an COMP student named CWC//
    @14e0f5//CHAI Wenchang, who is also called CWC, has shown a great interest in LLM//
    END OF RESULT//
    """

    retrivedContent=[
        "Types of Summer Opportunities\nSummer Exchange\nSummer@OxBridge\nShort-term Non-local \nStudy Fund\nExploring China\nCompare programmes and prioritize your options\n\u29bf Preference on location and area of study \n\u29bf Relevance to your PolyU studies\n\u29bf Credit transferability (compulsory for Summer Exchange and Summer@OxBridge) \n\u29bf Budget and financial support \n\u29bf Your other planned engagements and obligations in Summer 2024\n4\n",
        # "Summer Exchange (Europe)\nDenmark - Copenhagen Business School \nInternational Summer University Programme 2024\n24 June - 2 August 2024 \n\u2022\nPolyU students must take ordinary 6-week courses\n(courses: 24 June - 26 July: written sit-in exam: 29 July - 2 August)\n\u2022",
        # "Summer Exchange (Europe)\nFinland - Aalto University\nSchool of Business, Mikkeli Campus \u2013 Summer Studies 2024\n20 May - 16 August 2024\nIntensive 3 weeks modules (Worth 6 ECTS credits)\nPolyU nominated students are required to complete 2 modules:\nModules & Dates\nCourses\n\u2022\nSocial Media Analytics",
        # "Summer Exchange (Europe)\nSweden - University of Gothenburg\nSummer School for Sustainability\n27 June - 2 August 2024\nAll courses are at Bachelor\u2019s level and taught in English. \nEach course earns 7.5 credits (ECTS) and running over a five week period.\nCourse Options: \n\u2022\nBiodiversity in Western Sweden",
        # "Summer Exchange (Europe)\nDenmark - Copenhagen Business School \nInternational Summer University Programme 2024\n24 June - 2 August 2024 \n\u2022\nPolyU students must take ordinary 6-week courses\n(courses: 24 June - 26 July: written sit-in exam: 29 July - 2 August)\n\u2022",
        # "Summer Exchange (Europe)\nFinland - Aalto University\nSchool of Business, Mikkeli Campus \u2013 Summer Studies 2024\n20 May - 16 August 2024\nIntensive 3 weeks modules (Worth 6 ECTS credits)\nPolyU nominated students are required to complete 2 modules:\nModules & Dates\nCourses\n\u2022\nSocial Media Analytics",
        "Summer Exchange (Asia)\nSingapore - Singapore Management University\nGlobal Summer Programme 2024\n24 June - 19 July 2024\nCourses (Three Tracks):\n\u2022\nAsian Insights \n\u2022\nDigital Intelligence\n\u2022\nSustainable Futures\nEach course confers one SMU Credit Unit, equivalent to",
        "Summer Exchange (Asia)\nSingapore - Nanyang Technological University\nGEM Trailblazer Summer Programme 2024\n26 June - 27 July 2024\nCourse syllabus (Five Tracks):\n\u2022\nTrack 1: Language and cultural studies\n\u2022\nTrack 2: Entrepreneurship and innovation*\n\u2022\nTrack 3: Creative design and media\n\u2022",
        "Summer Exchange (Asia)\nKorea - Korea Advanced Institute of Science & Technology\n2024 KAIST Research Summer School\nJuly - August 2024 (6 weeks)\n(exact programme dates for 2024 are to be confirmed) \nProgramme Link\nTuition Fee: waived for PolyU nominated students.\nExchange student has to pay a research activity fee, and a programme fee, \nwhich covers accommodation, cultural experience, etc.\n12\n"
    ]

    retrivedId = [
        "39267d66-5158-4638-844b-ae0f32018aaa",
        # "9b2f916e-b8be-45e4-9f29-748ce6c41412",
        # "bd726387-e6e5-415f-b906-b7d6c7ff5f89",
        # "cd54ee46-f29a-4eb8-906e-6c427e6eede4",
        # "b5f75397-420d-4064-9988-a61eca76a720",
        # "d22055ca-a900-4d19-a4bf-e102ac558cd4",
        "e0f8f19a-f59b-451b-816d-688f0c9a2ae3",
        "613b32b3-c255-41c7-87ab-33e555f6283d",
        "457c32e2-db99-436b-beff-bb694237c263"
    ]

    # question = "Summer Exchange?"
    # Rnumber = 3
    # question = "Any Summer Exchange in Europe?"
    # Rnumber = 3
    question = "so is there summer echange schools in asia"
    Rnumber = 5


    context = ""
    # replace the \n in the retrivedContent with ' '
    for i in range(len(retrivedContent)):
        retrivedContent[i] = retrivedContent[i].replace('\n',' ')

    for i in range(len(retrivedContent)):
        context += '@'+retrivedId[i]+'//'+retrivedContent[i]+'//\n'
    context += 'END OF RESULT//'
    print(context)

    questions = Generator2.strengthenUserQuestion(question,num=Rnumber,temp=0)

    results = []
    for question in questions:
        result = Generator2.generate(context,question)
        # print(result)
        for i in range(1,10,2):
            if result.find('FINAL ANSWER:')<0:
                time.sleep(5)
                result = Generator2.generate(context,question,temp=i/10)
                print('retrying with temperature:',i/10)
            else:
                break
        result = result[result.find('FINAL ANSWER:')+14:]
        results += [result]
        # print()
        # print('- '*40)
        # print(result)
        # print('- '*40)
    
    print(results)

    summary = Generator2.AnswersToFinalAnswer(results)
    print(summary)

