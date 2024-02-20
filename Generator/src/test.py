def generate(content,question,Local=False):
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
        from openai import OpenAI
        from os import getenv
        
        # gets API Key from environment variable OPENAI_API_KEY
        hf = ChatOpenAI(
            model="mistralai/mistral-7b-instruct:free",
            openai_api_key=getenv("OPENROUTER_API_KEY"),
            openai_api_base="https://openrouter.ai/api/v1",
            temperature=0,
        )
    #------------------------------------------------------------
    
    from langchain.prompts import PromptTemplate
    # template = """Question: {question}
    # Answer: Let's think step by step, """
    template = """Use the following pieces of context to answer the question at the end. \\ seperate each chrunk, END OF RESULT\\ means the end of retrieved content. If you don't know the answer, just say that you don't know, don't try to make up an answer.
    
    {context}
    
    Question: {question}
    Helpful Answer:"""
    
    # question = "Who is Mao ZeDong?"
    prompt = PromptTemplate.from_template(template)
    
    chain = prompt | hf
    
    
    print()
    print('- '*40)
    print(chain.invoke({"context":context,"question": question}))
    print('- '*40)

if __name__ == '__main__':
    content = """
    CHAI is a student in Hong Kong PolyU\\
    CHAI is from China\\
    END OF RESULT\\
    """
    question = "Who is CHAI?"
    generate(content,question)
