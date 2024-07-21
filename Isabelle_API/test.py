import openai
from openai import OpenAI
import subprocess
import os

openai.api_key = 'YOUR_OPENAI_API_KEY'

def generate_isabelle_code(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert in Isabelle theorem proving."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content'].strip()

def run_isabelle_code():
    result = subprocess.run(['isabelle', 'build', '-D', '.'], capture_output=True, text=True)
    return result.stdout, result.stderr

def log_error(error_message):
    with open('error_log.txt', 'a') as f:
        f.write(error_message + '\n')

def handle_user_prompt(user_prompt):
    prompt = f"Generate Isabelle code to {user_prompt}"
    isabelle_code = generate_isabelle_code(prompt)
    
    with open('GeneratedTheory.thy', 'w') as f:
        f.write(f"theory GeneratedTheory\nimports Main\nbegin\n\n{isabelle_code}\n\nend\n")
    
    stdout, stderr = run_isabelle_code()
    
    if stderr:
        log_error(stderr)
        refined_prompt = f"{user_prompt} Here is the error: {stderr}"
        return handle_user_prompt(refined_prompt)
    return stdout

if __name__ == "__main__":
    user_prompt = input("Enter the theorem or proof goal: ")
    result = handle_user_prompt(user_prompt)
    print("Final result: ", result)
