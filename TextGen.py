import google.generativeai as genai
import re
import json 

# Gen AI Configuration
genai.configure(api_key="AIzaSyA3xtb9-icFxB0DqHL5zoaoQjWj48eSxqo")
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to get answer from AI model


# Text-cleaner function
def clean_text_for_ppt(input_text):
    cleaned_text = re.sub(r'\s+', ' ', input_text.strip())
    cleaned_text = re.sub(r'[^\w\s]', '', cleaned_text)
    cleaned_text = cleaned_text.replace('\n', ' ')
    return cleaned_text
def answer(q):
    response = model.generate_content(q)
    response= response.text
    return response

def answer2(q,length):
    question = f"Clearly explain the 2 problem statements, the solution the user has given to the 2 problem statement , what is the market opportunity for this idea described by the user for the idea {q} the output template is Problem Statement:['put the problem statement clearly in formatted way problem_statement1:'First problem statement {length} words' problem_statement2:'Second problem statement {length} words'], Solution:['put the solution clearly in formatted way solution1:'First problem statement solution {length} words' solution2:'Second problem statement solution {length} words'], Market opportunity:['put the market opportunity clearly in formatted way tell 4 market opportunity m1:'opportunity 1' m2:'opportunity 2' m3:'opportunity 3' m4:'opportunity 4' everything in {length} words'] Business Model:[put the business model by the user in 25 words]"
    response = model.generate_content(question)
    response= response.text

    ps1 = clean_text_for_ppt(response[response.find("problem_statement1") + len("problem_statement1"):response.find("problem_statement2")])
    ps2 = clean_text_for_ppt(response[response.find("problem_statement2") + len("problem_statement2"):response.find("Solution:")])
    s1 = clean_text_for_ppt(response[response.find("solution1") + len("solution1"):response.find("solution2")])
    s2 = clean_text_for_ppt(response[response.find("solution2") + len("solution2"):response.lower().find("market opportunity")])
    mo1 = clean_text_for_ppt(response[response.find("m1") + len("m1"):response.find("m2")])
    mo2 = clean_text_for_ppt(response[response.find("m2") + len("m2"):response.find("m3")])
    mo3 = clean_text_for_ppt(response[response.find("m3") + len("m3"):response.find("m4")])
    mo4 = clean_text_for_ppt(response[response.find("m4") + len("m4"):response.lower().find("business model")])
    bm = clean_text_for_ppt(response[response.lower().find("business model")+len("Business Model"):])
    return [ps1,ps2,s1,s2,mo1,mo2,mo3,mo4,bm]
def GenText(input_idea, length):
    #Problem Statement 
    ps = answer(f"{input_idea} Explain the main two problem statements mentioned in the idea in the output format of problem statement1:Subtopic_of_problem_statement — actual problem statement , problem statement2:Subtopic_of_problem_statement — actual problem statement in {length} number of words")
    ps1=ps[ps.find("Problem Statement 1:")+len("Problem Statement 1:"):ps.find("Problem Statement 2:")]

    ps1t=ps1[:ps1.find("—")].strip()   
    ps1=ps1[ps1.find("—")+1:].strip()



    ps2=ps[ps.find("Problem Statement 2:")+len("Problem Statement 2:"):]

    ps2t=ps2[:ps2.find("—")].strip()   
    ps2=ps2[ps2.find("—")+1:].strip()

    #Solution
    s=answer(f"for this problem statement {ps} from this idea {input_idea} explain the two solutions from the user idea ,the output template is solution 1: subtopic_of_solution1 — actual solution 1, solution 2: subtopic_of_solution2 — actual solution 2")
    s1=s[s.lower().find("solution 1:")+len("solution 1:"):ps.lower().find("solution 2:")]

    s1t=s1[:s1.find("—")].strip()
    s1=s1[s1.find("—")+1:].strip()


    s2=s[s.lower().find("solution 2:")+len("solution 2:"):]
    s2t=s2[:s2.find("—")].strip()
    s2=s2[s2.find("—")+1:].strip()

    #market opportunity 
    def MnT(m):
        mnt,mn=m.split("\n")[:2]
        mnt.replace("**Topic:**","")
        mn.replace("Content:","")
        return mnt,mn
    m=answer(f"{input_idea} explain 4 market opportunities in the idea which is mentioned by the user , split 4 opportunity with '—' delimiter with maximum word count is {length} for each opportunity with a topic and content in template **topic:** content ")
    m1,m2,m3,m4=m.split("—")
    print
    m1t,m1=MnT(m1)
    m2t,m2=MnT(m2)
    m3t,m3=MnT(m3)
    m4t,m4=MnT(m4)
    
    #Business model:
    bm=answer(f"{input_idea} Explain the business model in the user given idea with word count of 50")

    return {"ps1t":ps1t,"ps1":ps1,"ps2t":ps2t,"ps2":ps2,"s1t":s1t,"s1":s1,"s2t":s2t,"s2":s2,"m1t":m1t,"m1":m1,"m2t":m2t,"m2":m2,"m3t":m3t,"m3":m3,"m4t":m4t,"m4":m4,"bm":bm}
import json

def GenText2(input_idea, length,content_lenght):
    # JSON-based prompt for structured response
    prompt = f"""
    Based on the idea: "{input_idea}", generate the following details in JSON format:
    {{
        "problem_statements": [
            {{
                "title": "Subtopic_of_problem_statement1",
                "description": "Actual problem statement 1 in {content_lenght} words"
            }},
            {{
                "title": "Subtopic_of_problem_statement2",
                "description": "Actual problem statement 2 in {content_lenght} words"
            }}
        ],
        "solutions": [
            {{
                "title": "Subtopic_of_solution1",
                "description": "Actual solution 1 in {content_lenght} words"
            }},
            {{
                "title": "Subtopic_of_solution2",
                "description": "Actual solution 2 in {content_lenght} words"
            }}
        ],
        "market_opportunities": [
            {{
                "title": "Topic of opportunity 1",
                "content": "Content for opportunity 1 in {content_lenght+25} words"
            }},
            {{
                "title": "Topic of opportunity 2",
                "content": "Content for opportunity 2 in {content_lenght+25} words"
            }},
            {{
                "title": "Topic of opportunity 3",
                "content": "Content for opportunity 3 in {content_lenght+25} words"
            }},
            {{
                "title": "Topic of opportunity 4",
                "content": "Content for opportunity 4 in {content_lenght+25} words"
            }}
        ],
        "business_model": "Brief explanation of the business model in {length} words."
    }}
    """
    
    # Get the response as a string
    response = answer(prompt)
    
    # Clean the response to remove `json` code formatting if present
    cleaned_response = response.strip().strip("```").strip("json").strip()

    # Attempt to parse the cleaned response into JSON
    try:
        response_json = json.loads(cleaned_response)
        
        # Extract data into the required dictionary format
        problem_statements = response_json["problem_statements"]
        ps1t = problem_statements[0]["title"]
        ps1 = problem_statements[0]["description"]
        ps2t = problem_statements[1]["title"]
        ps2 = problem_statements[1]["description"]

        solutions = response_json["solutions"]
        s1t = solutions[0]["title"]
        s1 = solutions[0]["description"]
        s2t = solutions[1]["title"]
        s2 = solutions[1]["description"]

        market_opportunities = response_json["market_opportunities"]
        m1t = market_opportunities[0]["title"]
        m1 = market_opportunities[0]["content"]
        m2t = market_opportunities[1]["title"]
        m2 = market_opportunities[1]["content"]
        m3t = market_opportunities[2]["title"]
        m3 = market_opportunities[2]["content"]
        m4t = market_opportunities[3]["title"]
        m4 = market_opportunities[3]["content"]

        business_model = response_json["business_model"]

        # Return the formatted dictionary
        return {
            "ps1t": ps1t, "ps1": ps1, "ps2t": ps2t, "ps2": ps2,
            "s1t": s1t, "s1": s1, "s2t": s2t, "s2": s2,
            "m1t": m1t, "m1": m1, "m2t": m2t, "m2": m2,
            "m3t": m3t, "m3": m3, "m4t": m4t, "m4": m4,
            "bm": business_model
        }

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        print(f"Cleaned Response: {cleaned_response}")
        return {}

    except KeyError as e:
        print(f"Missing key in JSON response: {e}")
        return {}

'''res=GenText2(
    "Our aim is to build a next level ai platform where startup founders can find their investors and make pitchdeck out of ai , the platform helps the founders to have ai search engine through the investors , here the problems like spam investors , outdateded vc database and unrelabile contact information are eliminated , the platform provides high quality data and connections to vc helpping founders rise fund. business model is a subscription based model where user pays to platform to use high quality ai feed to make pitch deck and find investors",
    30
)
print(res)'''