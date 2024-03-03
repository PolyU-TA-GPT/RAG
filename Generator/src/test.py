from bs4 import BeautifulSoup as BS
def generate(context,question,Local=False,temp=0):
    if Local:
        from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
        from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
        from transformers import file_utils
        print(file_utils.default_cache_path)
        
        
        import torch
        import intel_extension_for_pytorch as ipex
        torch.manual_seed(0)
        
        path = 'openbmb/MiniCPM-2B-dpo-bf16'
        tokenizer = AutoTokenizer.from_pretrained(
            path,
            #low_cpu_mem_usage=True,
        )
        
        model = AutoModelForCausalLM.from_pretrained(
            path,
            low_cpu_mem_usage=True,
            torch_dtype=torch.bfloat16,
            device_map='auto',
            trust_remote_code=True
        )
        
        model.eval()
        model = ipex.llm.optimize(
            model,
            dtype=torch.bfloat16,
            inplace=True,
            deployment_mode=True
        )
        
        
        #responds, history = model.chat(
        #    tokenizer,
        #    "山东省最高的山是哪座山, 它比黄山高还是矮？差距多少？",
        #    temperature=0.8,
        #    top_p=0.8
        #)
        #print(responds)
        print(model.device)
        #print()
        
        
        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            batch_size=1,
            max_new_tokens=2,
            num_beams=4,
            do_sample=True,
            top_p=0.8,
            temperature=0.8,
            bos_token_id=1,
            eos_token_id=2,
            pad_token_id=2,
            repetition_penalty=1.5
        )
        
        #import time
        #t = time.time()
        #dt=0
        #response = ''
        #prompt = "Hey, "
        #print(prompt)
        #for i in range(50):
        #    t = time.time()
        #    inputs = tokenizer(response, return_tensors="pt")
        #    generate_ids = model.generate(
        #        inputs.input_ids, 
        #        max_new_tokens=1,
        #        bos_token_id=1,
        #        eos_token_id=2,
        #        pad_token_id=2,
        #        use_cache = False
        #    )
        #    response = tokenizer.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        #    print('- '*40+'\n',i,time.time()-t-dt,(time.time()-t)/(1+i),response)
        #    dt=time.time()-t
        
        hf = HuggingFacePipeline(pipeline=pipe,max_new_tokens=200)
    else:
        from langchain_openai import ChatOpenAI
        from os import getenv
        
        # gets API Key from environment variable OPENAI_API_KEY
        hf = ChatOpenAI(
          base_url="https://openrouter.ai/api/v1",
          openai_api_key=getenv("OPENROUTER_API_KEY"),
          temperature=temp
        )
    #------------------------------------------------------------
    
    from langchain.prompts import PromptTemplate
    # template = """Question: {question}
    # Answer: Let's think step by step, """
    template = """Use the following pieces of context to answer the question at the end. 
Provide precise answer based on the context and attach the source coordinate SC of your answer in [SC]:
```
------------------------------------------------------------
    @3603a49a-d26c-4a2d-a9f1-0a608211b3ba//HAER is a current student of CBS//
    @7628b67b-3eb1-437c-b302-f0df15847605//HAER is a boy//
    @fbb63230-714f-4b53-bfcc-20ca1f4ff734//HAER is from USA//
    END OF RESULT//
------------------------------------------------------------
    Question: Who is HAER?
------------------------------------------------------------
```
Think and response with [@SC] in several complete and logical sentense: 
```
THOUGHT: The question ~~Who is HAER?~~ is asking for HAER's information.

ANSWER: HAER is a student from USA[SC: @fbb63230-714f-4b53-bfcc-20ca1f4ff734] and currently in CBS[SC: @3603a49a-d26c-4a2d-a9f1-0a608211b3ba].

THOUGHT: 'HAER is a student from USA[SC: @fbb63230-714f-4b53-bfcc-20ca1f4ff734]' is not related to '@7628b67b-3eb1-437c-b302-f0df15847605//HAER is a boy//'.

FINAL ANSWER: As far as I know, HAER is a student from USA[SC: @e956dd] and currently in CBS[SC: @0a3f01].
```

If don't know the answer or the question is not related, think and response like this: 
```
THOUGHT: The question ~~xxx~~ is asking for xxx.

ANSWER: No information for 'xxx'.

THOUGHT: 'xxx' is NOT related to the context.

FINAL ANSWER: 'xxx' is NOT related to the context[SC: NO INFORMATION].
```
Now do the real task below!

------------------------------------------------------------
    {context}
------------------------------------------------------------
    Question: {question}
------------------------------------------------------------

"""
    
    # question = "Who is Mao ZeDong?"
    prompt = PromptTemplate.from_template(template)
    
    chain = prompt | hf
    
    return chain.invoke({"context":context,"question": question}).content

def rephrase(question, rephrase_num, temp=0):
    from langchain_openai import ChatOpenAI
    from os import getenv
    
    # gets API Key from environment variable OPENAI_API_KEY
    hf = ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        openai_api_key=getenv("OPENROUTER_API_KEY"),
        temperature=temp
    )
    from langchain.prompts import PromptTemplate
    # template = """Question: {question}
    # Answer: Let's think step by step, """
    template = """
    Please provide only 1 brief rephrased versions of the original question as the following example:
    ```
    <original_question>What are available summer exchange types in PolyU?</origina_question>
    <rephrased_question>What are PolyU available summer exchange opportunities?</rephrased_question>
    
    ```
    Now do the real task below:
    <original_question>{question}</original_question>
"""
    

    prompt = PromptTemplate.from_template(template)
    
    chain = prompt | hf
    result = [question]
    for i in range(rephrase_num):
        for j in range (3):
            response = BS(chain.invoke({"question": question}).content, features="lxml")
            text = response.find('rephrased_question').text
            if len(text) > 1:
                result.append(text)
                break      
    return result


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
    result = generate(context,question,temp=0)
    print(result)
    for i in range(1,10,2):
        if result.find('FINAL ANSWER:')<0:
            time.sleep(5)
            result = generate(context,question,temp=i/10)
            print(i/10,result)
        else:
            break
    result = result[result.find('FINAL ANSWER:')+14:]
    print()
    print('- '*40)
    print(result)
    print('- '*40)
