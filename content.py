from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse, RedirectResponse
import openai
import json
app = FastAPI()
import re
import os
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
# CORS middleware to allow requests from any origin 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

openai.api_key = "vtunDOr-Okj3MlgVtATbdDCSWsuCKolyED-PFcTd7XVAA "
PROMPT_TEMPLATE = """
You are an expert career coach and professional content writer.

Your task is to generate a comprehensive and practical interview preparation guide for the role of "{job_name}". The guide should be well-structured, insightful, and tailored specifically to the job title. All sections must contain meaningful content and must not be left empty, regardless of the job title.

The output must be in valid JSON format with the following structure:
{{
  "job_name": "{job_name}",
  "interview_guide": {{
    "H1": "{job_name} Interview Questions",
    "sub_line": "Prepare for your next {job_name} interview in 2025 with expert-picked questions, explanations, and sample answers.",
    
    "Interviewing_as": {{
      "title": "Interviewing as a {job_name}",
      "paragraph_1": "Write a ~105-word paragraph describing what it’s like to interview as a {job_name}.",
      "paragraph_2": "Write a ~120-word paragraph discussing the expectations, challenges, and key competencies for a {job_name} interview."
    }},
    
    "Types_of_Questions": {{
      "title": "Types of Questions to Expect in a {job_name} Interview",
      "intro_paragraph": "Write a ~100-word paragraph introducing the types of questions typically asked in a {job_name} interview.",
      "categories": {{
        "randome_title_1": "Write explaine about randometitle_1 questions for {job_name}, content must be length  in 1000 words.",
        "randome_title_2": "Write explaine about randome_title_1 questions relevant to {job_name} , content lenght should be strictly 1000 words, no more then that in any case.",
        "randome_title_3": "Write explaine describing randome_title_3 questions for {job_name} , content lenght should be strictly 1000 words, no more then that in any case.",
        "randome_title_4": "Write explaine about randome_title_4 questions for {job_name}, content lenght should be strictly 1000 words, no more then that in any case.",
        "randome_title_5": "Write explaine about questions randome_title_5 {job_name} , content lenght should be strictly 1000 words, no more then that in any case."
      }}
    }},

    "Questions_and_Answers": {{
      "title": "{job_name} Interview Questions and Answers",
      "qa_pairs": [
        {{
          "question": "Give me random question about {job_name}?",
          "answer": "Give answer of above question in detaile. for a {job_name}.",
          "how_to_answer_it": "Explain how to structure the answer and what key skills or tools to mention.",
          "example_answer": "Provide a 40-word example answer related to this question for a {job_name}."
        }},
        {{
          "question": Give me random question about {job_name} .",
          "answer": "Give answer of above question in detaile.",
          "how_to_answer_it": "Mention STAR method and focus on results.",
          "example_answer": "Write a 100-word realistic example related to a challenge in a {job_name} role."
        }},
        {{
          "question": "Give me random question about {job_name} work?",
          "answer": "Give answer of above question in detaile. in about 100 words.",
          "how_to_answer_it": "Mention software, frequency of use, and technical proficiency.",
          "example_answer": "Give a 40-word example mentioning tools like Excel, ERP systems, etc., relevant to a {job_name}."
        }}
        ,
        {{
          "question": "Give me random question about {job_name} work?",
          "answer": "Give answer of above question in detaile. in about 100 words.",
          "how_to_answer_it": "Mention software, frequency of use, and technical proficiency.",
          "example_answer": "Give a 40-word example mentioning tools like Excel, ERP systems, etc., relevant to a {job_name}."
        }}
        ,
        {{
          "question": "Give me random question about {job_name} work?",
          "answer": "Give answer of above question in detaile. in about 100 words.",
          "how_to_answer_it": "Mention software, frequency of use, and technical proficiency.",
          "example_answer": "Give a 40-word example mentioning tools like Excel, ERP systems, etc., relevant to a {job_name}."
        }},
         {{
          "question": "Give me random question about {job_name} work?",
          "answer": "Give answer of above question in detaile. in about 100 words.",
          "how_to_answer_it": "Mention software, frequency of use, and technical proficiency.",
          "example_answer": "Give a 40-word example mentioning tools like Excel, ERP systems, etc., relevant to a {job_name}."
        }}
        , {{
          "question": "Give me random question about {job_name} work?",
          "answer": "Give answer of above question in detaile. in about 100 words.",
          "how_to_answer_it": "Mention software, frequency of use, and technical proficiency.",
          "example_answer": "Give a 40-word example mentioning tools like Excel, ERP systems, etc., relevant to a {job_name}."
        }}
        , {{
          "question": "Give me random question about {job_name} work?",
          "answer": "Give answer of above question in detaile. in about 100 words.",
          "how_to_answer_it": "Mention software, frequency of use, and technical proficiency.",
          "example_answer": "Give a 40-word example mentioning tools like Excel, ERP systems, etc., relevant to a {job_name}."
        }}
        , {{
          "question": "Give me random question about {job_name} work?",
          "answer": "Give answer of above question in detaile. in about 100 words.",
          "how_to_answer_it": "Mention software, frequency of use, and technical proficiency.",
          "example_answer": "Give a 40-word example mentioning tools like Excel, ERP systems, etc., relevant to a {job_name}."
        }},
         {{
          "question": "Give me random question about {job_name} work?",
          "answer": "Give answer of above question in detaile. in about 100 words.",
          "how_to_answer_it": "Mention software, frequency of use, and technical proficiency.",
          "example_answer": "Give a 40-word example mentioning tools like Excel, ERP systems, etc., relevant to a {job_name}."
        }}, {{
          "question": "Give me random question about {job_name} work?",
          "answer": "Give answer of above question in detaile. in about 100 words.",
          "how_to_answer_it": "Mention software, frequency of use, and technical proficiency.",
          "example_answer": "Give a 40-word example mentioning tools like Excel, ERP systems, etc., relevant to a {job_name}."
        }}

      ]
    }},

    "Questions_to_Ask": {{
      "title": "Smart Questions to Ask in a {job_name} Interview",
      "paragraph": "Explain why asking good questions is important in a {job_name} interview (~100 words).",
      "good_questions": [
        {{
          "question": "",//Give me random question about {job_name}  ?
          "answer": "", //Give answer of above question in detail. Each answer should be relevant to {job_name} role and must be between 50 to 100 words not less than 50 words.
        }},// limit of 5 questions, repeat the same format for each question

      ]
    }},

      "Good_Candidate_Profile": {{
      "title": "What Makes a Strong {job_name} Candidate?",
      "paragraph_1": "Write a 150 word paragraph describing essential highlighting the ideal qualifications, relevant certifications, and years of experience suited soft skills (e.g., problem-solving, collaboration, communication) that a great {job_name} should have.",
      "good_candidate_1": {{
        "heading": "dynamic_heading_1",
        "description": "" //Explain why dynamic_heading_1 is important in the {job_name} role, with examples of how it influences their tasks or success.
      }}, repeat headings and descriptions for 4 more dynamic headings, each relevant to the {job_name} role.  eg. heading ,heading, heading, heading along with their descriptions.

    }},

    "Interview_FAQs": {{
      "title": "Frequently Asked Interview Questions for {job_name}",
      "faqs": [
        {{
          "question": "What is one of the most common interview questions for {job_name}?",
          "answer": "Provide a 50-word answer."
        }},
        {{
          "question": "How should a candidate discuss past failures or mistakes in a {job_name} interview?",
          "answer": "Provide a 50-word answer explaining how to frame failures positively."
        }}
      ]
    }}
  }}
}}
"""




def generate_interview_guide(job_name: str) -> str:
    prompt = PROMPT_TEMPLATE.format(job_name=job_name)
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[

            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Generate a comprehensive interview guide for the job title: {job_name}"}
        ]
    )
    return response.choices[0].message.content

@app.get("/")
async def read_index():
    return JSONResponse(content={"message": "Welcome to the Interview Guide API. Use POST /generate with 'job_name' to generate guide."})

@app.post("/generate")
async def generate_post(job_name: str = Form(...)):
    # Instead of redirect, return JSON with a link or direct content
    guide_content = generate_interview_guide(job_name)
    return JSONResponse(content={
        "job_name": job_name,
        "interview_guide": guide_content
    })



class GuideRequest(BaseModel):
    job_name: str

def strip_markdown(text: str) -> str:
    # Remove Markdown headings and formatting
    text = re.sub(r'\*{1,2}(.*?)\*{1,2}', r'\1', text)  # **bold** or *italic*
    text = re.sub(r'#+\s*', '', text)  # # or ## headers
    text = re.sub(r'\n{2,}', '\n\n', text)  # Reduce excessive newlines
    return text.strip()
# Optional: If you want a GET endpoint for guide too

@app.get("/guide")
async def get_guide(job: str):
    guide = generate_interview_guide(job)
    clean_guide = strip_markdown(guide)
    response_data = {
        "job_name": job,
        "interview_guide": clean_guide,
    }
    json_str = json.dumps(response_data, ensure_ascii=False, indent=2)
    print("Clean JSON String:", json_str)
    return JSONResponse(content=json_str)
