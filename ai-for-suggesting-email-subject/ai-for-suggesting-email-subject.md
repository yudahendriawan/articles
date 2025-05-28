# Build a Simple AI to Suggest Email Subjects using OpenAI API

Hi there! 👋

Have you ever stared at an email for minutes, even hours, just trying to come up with the perfect subject line?
You're not alone.

Inboxes are flooded, attention spans are short, and your email subject is the first—and sometimes only—chance to make an impression.
Yet, most people spend more time writing the body than crafting the subject.

What if we could flip that around?
What if AI could read your email and suggest a clear, catchy subject line that grabs attention instantly?

Let’s build that tool. From scratch.

In this project, we’ll create a simple AI assistant that reads the body of an email and suggests a short, suitable subject line using the OpenAI API.

Let’s break it down step by step—so even if you’re new to OpenAI or prompt engineering, you’ll be just fine.

## Step 1: Environment Setup
(Skip this if you're already set up with Python and virtual environments.)

### Create a clean workspace:
```bash
mkdir email-subject-generator
cd email-subject-generator
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate.bat on Windows
```

### Install dependencies:

```bash
pip install openai python-dotenv
```

## Step 3: Set Up API Key

If you have already got the OpenAI Api Key, you can skip this below step.

If you have not had an Open API Key, you can follow the tutorial of this [How to get an OpenAI API Key](https://www.howtogeek.com/885918/how-to-get-an-openai-api-key/).

### Create a `.env` file
This step is **important** because you are going to need to store your OpenAI Api Key in the file of `.env` in order to avoid being pushed to your online repository (GitHub/GitLab, etc)

Before executing this below command, ensure that you are already in the `email-subject-generator` directory

- On Mac/Linux
```bash
echo "OPENAI_API_KEY=your_openai_key_here" > .env
```

- On Windows (CMD)
```bash
echo OPENAI_API_KEY=your_openai_key_here > .env
```

- On Windows (PowerShell)
```bash
Set-Content .env "OPENAI_API_KEY=your_openai_key_here"
```

You can make sure that you already store your API Key correctly, you can create a Python file named `suggest-email-subject.py` and write this Python code:

```Python
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
```

Ensure that there are no error.

## Step 3: Understand the AI Logic

Let’s go through the main components that make this AI work.

You can continue writing on the `suggest-email-subject.py` code.

### System Prompt: Define the assistant's role

This prompt sets the behavior of the AI. In our case, we tell the assistant, "Hey, your job is to create subject lines, and nothing else."

```Python
system_prompt = "You are an assistant that is going to suggest an appropriate short subject line for the given email body or contents."
```

### User Prompt: Supply the email body

This part wraps the email content in clear instructions, so the AI knows what we’re asking. The `context` here is the actual email body we want to analyze.


```Python
def user_prompt_for(context):
    return f"You are looking at an email body/content.\nThe body/contents of this email is as follows; please suggest an appropriate short subject of this email:\n\n{context}"

```

### Messages: Combine system + user prompts

The OpenAI API works in a chat format, so we must send a list of messages. Here we send:

1. A `system` message (defines the AI's role)
2. A `user` message (asks the AI to do something)

```Python
def messages_for(email_body):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for(email_body)}
    ]
```

### Response: Send the request to OpenAPI

You have already import the `OpenAI` library above
```Python
from openai import OpenAI
```

Now you can continue writing the code:

```Python
def suggest_subjects(email_body):
    openai = OpenAI()
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages_for(email_body)
    )
    return response.choices[0].message.content
```

This function actually talks to OpenAI’s server.
We use the `"gpt-4o-mini"` model (you can change it), and pass in our messages.

The response is a structured object—`choices[0].message`.content gives us the actual AI output (our subject line).

- Display: Show the final result

```Python
def display_subject(context):
    subject = suggest_subjects(context)
    print("Suggested Subject Line:\n", subject)
```

This function is for the user: it takes an email body, runs it through the whole AI process, and prints the subject line.

## Run Code

Make sure your script has this at the end so it actually runs:

```Python
if __name__ == "__main__":
    display_subject(email_body)
```
Now run:
```Bash
python suggest-email-subject.py
```

You should see something like:
```Bash
Suggested Subject Line:
Application for Software Development Internship – Ronaldo
```

## Final Code 

Before running the code, we need to have the `email_body` example that we want to suggest its subject.

```Python
email_body = """
Dear HR Team,

My name is Ronaldo, a third-year Computer Science student at Universitas Teknologi Nasional. I am writing to express my interest in applying for a software development internship position at [Company Name].

I am particularly drawn to your company’s commitment to innovation and excellence in technology solutions. I have experience working with Python and JavaScript, and I am eager to contribute and learn from your dynamic team.

Attached to this email is my CV for your review. I would be grateful for the opportunity to further discuss how I can support your team during the internship period.

Thank you for considering my application. I look forward to hearing from you.

Best regards,
Ronaldo
"""
```

Finally, this is the final code of the `suggest-email-subject.py`:

```Python
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

system_prompt = "You are an assistant that is going to suggest an appropriate short subject line for the given email body or contents."

def user_prompt_for(context):
    return f"You are looking at an email body/content.\nThe body/contents of this email is as follows; please suggest an appropriate short subject of this email:\n\n{context}"

def messages_for(email_body):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for(email_body)}
    ]

def suggest_subjects(email_body):
    openai = OpenAI()
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages_for(email_body)
    )
    return response.choices[0].message.content

def display_subject(context):
    subject = suggest_subjects(context)
    print("Suggested Subject Line:\n", subject)

email_body = """
Dear HR Team,

My name is Ronaldo, a third-year Computer Science student at Universitas Teknologi Nasional. I am writing to express my interest in applying for a software development internship position at [Company Name].

I am particularly drawn to your company’s commitment to innovation and excellence in technology solutions. I have experience working with Python and JavaScript, and I am eager to contribute and learn from your dynamic team.

Attached to this email is my CV for your review. I would be grateful for the opportunity to further discuss how I can support your team during the internship period.

Thank you for considering my application. I look forward to hearing from you.

Best regards,
Ronaldo
"""

if __name__ == "__main__":
    display_subject(email_body)

```

And just like that, you’ve built your own AI subject line generator—clean, fast, and super practical.

This is more than a toy project. It’s a real-world tool powered by OpenAI that can save time, boost email open rates, and make your communication sharper.

Next time someone struggles to name their email, you’ll smile and say,
“Don’t worry. I built an AI for that.”

Go ahead—improve it, ship it, or share it. You just took a simple idea and made it smart.








