---
title: How to automatically Build a Company Brochure from Website using OpenAI API ?
---

Hi everyone, welcome back to my articles.

Imagine you're a data analyst trying to understand a website. Visiting it directly can be overwhelming—there’s often too much information to sift through and summarize. But what if there were a tool where you simply enter the website URL, and it instantly gives you a clean, brochure-style summary?

On the other hand, many small businesses struggle to create brochures for their websites. It takes time, writing skills, and sometimes the help of a designer. I saw this as an opportunity to build something simpler. After some experimentation, I created a tool that helps companies generate website brochures quickly—just by answering a few questions. It’s like having a streamlined assistant that handles the writing and layout for you.

Before diving into every section, these are the outline of this article:
1. Getting Our Workshop Ready: Setting Up Your Environment
2. Our Digital Explorer: The Website Class
3. The Smart Link Filter: Guiding Our Text Engine
4. The Brochure Builder: Crafting the Story
5. Results: Brochure Created

Let's go!


## 1. Getting Our Workshop Ready: Setting Up Your Environment 
Before we dive into building, we need to make sure our Python workspace has all the necessary tools. Think of it like gathering your screwdrivers, wrenches, and blueprints before starting a construction project!

### 1.1 First Things First: Installing Our Libraries
Open up your terminal or command prompt. This is where we'll tell Python what extra tools we need. Type in this command and hit Enter:

```Bash
pip install python-dotenv requests beautifulsoup4 openai IPython
```

**What are these tools for?**
- `python-dotenv`: This is our secure storage solution. It helps us keep sensitive information (like our API key) out of our main code file.
- `requests`: This is your personal web browser within Python. It allows our program to visit websites and download their content.
- `beautifulsoup4`: Imagine a super-smart pair of scissors and a highlighter. BeautifulSoup helps us cut through the complex code of a webpage and highlight just the text and links we care about.
- `openai`: This is our direct line to the advanced text-generating engine. It lets our program send text requests and get back incredibly human-like written content.
- `IPython`: If you're working in a Jupyter notebook (which is great for this project!), IPython helps us display the final brochure beautifully formatted.

### 1.2 Your Special Pass: The API Key
To use the powerful text-generating engine, you'll need a unique key that identifies you.

1. Go to the [OpenAI Platform](https://platform.openai.com/signup).
2. Sign up or log in.
3. Find the section for API keys and generate a new secret key. It usually starts with sk-proj-.
4. **Crucial Safety Tip**: This key is like the password to your account for using the text engine. Never share it publicly or put it directly into code that others might see!

### 1.3 Keeping it Secret! Keeping it Safe: The `.env` File
To protect your API key, we'll store it in a special file called `.env`.
Create a file named `.env` in the same folder where your Python script or Jupyter notebook will be saved. Inside this file, add this line, replacing `YOUR_API_KEY_HERE` with the key you just got from OpenAI:

```yaml
OPENAI_API_KEY=YOUR_API_KEY_HERE
```

Now, our program can read this key without it being visible in the main code.

### 1.4 Powering Up Our Program: Initial Setup Code
Let's put the very first lines of code into your Python script or Jupyter notebook. This sets up our tools and connects to the text-generating engine.

**DISCLAIMER !!**

To make it clearer, I add inline comment on the code, you can just read it and type the actual code, or you can just simply copy and paste my code.

```python
# Essential Libraries: These are the tools we just installed!
import os
import requests
import json
from typing import List
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display, update_display
from openai import OpenAI # Our connection to the text-generating engine

# --- Initial Setup ---
# Load our secret API key from the .env file
load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

# A quick check to make sure our key loaded correctly!
if api_key and api_key.startswith('sk-proj-') and len(api_key) > 10:
    print("API key successfully loaded! Ready to build.")
else:
    print("Uh oh! There might be a problem with your API key. Double-check your .env file and your OpenAI account. 😕")

# We'll use a specific version of the text-generating engine, 'gpt-4o-mini', for efficiency.
TEXT_GENERATION_MODEL = "gpt-4o-mini"
# This is how we'll send requests to the text-generating engine.
text_engine_client = OpenAI()
```

Run this code block. If you see "API key successfully loaded! Ready to build.", you're all set to move on to the next exciting step!

## 2. Our Digital Explorer: The `Website` Class

Before we can create a brochure, our program needs to "visit" the website and gather all its content. We'll create a special Python blueprint, a `class` called `Website`, that knows how to do just that. Think of it as giving our program its own pair of digital eyes!

Paste this code into your script or notebook:

```python
# Websites sometimes act shy! We'll use these "headers" to make our requests look like a normal web browser.
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0"
}

class Website:
    """
    This class is our digital explorer! It visits a webpage, extracts all its readable text,
    and lists all the links it finds.
    """
    def __init__(self, url):
        self.url = url
        try:
            # Try to fetch the webpage content
            response = requests.get(url, headers=headers, timeout=10) # Set a timeout just in case!
            response.raise_for_status() # Check if the website responded with an error (like a 404 page)
            self.raw_html_body = response.content # Store the raw HTML

            # Now, let's use BeautifulSoup to make sense of the HTML
            soup = BeautifulSoup(self.raw_html_body, 'html.parser')
            self.title = soup.title.string if soup.title else "No title found" # Get the page title

            if soup.body:
                # IMPORTANT: We want clean text for our brochure.
                # So, we'll remove parts of the webpage that aren't useful text,
                # like scripts (code), styles (CSS), images, forms, footers, and navigation menus.
                for irrelevant_tag in soup.body(["script", "style", "img", "input", "footer", "nav"]):
                    irrelevant_tag.decompose() # This removes the tag and its contents

                # Now, extract all the clean, readable text from the body.
                self.text_content = soup.body.get_text(separator="\n", strip=True)
            else:
                self.text_content = "" # If no body, no text!

            # Find all the links (<a> tags) on the page
            found_links = [link.get('href') for link in soup.find_all('a')]
            # Clean up the links: filter out empty ones and transform relative links
            # (like "/about") into full URLs (like "https://example.com/about").
            # We also skip internal anchor links (like "#section")
            self.all_links = [requests.compat.urljoin(self.url, link)
                              for link in found_links if link and not link.startswith('#')]

        except requests.exceptions.RequestException as e:
            # If there's an error fetching the page (e.g., website down, network issue)
            print(f"Error fetching {url}: {e}")
            self.raw_html_body = ""
            self.title = "Error"
            self.text_content = ""
            self.all_links = [] # No links if we couldn't fetch the page

    def get_clean_contents(self):
        """
        Returns the clean title and text content of the webpage, ready for analysis.
        """
        return f"Webpage Title:\n{self.title}\nWebpage Contents:\n{self.text_content}\n\n"

# --- Let's give our Website explorer a test run! ---
# Pick any website URL you like!
test_url = "https://www.example.com" # Feel free to change this!
my_website_explorer = Website(test_url)

print(f"Our explorer visited: {my_website_explorer.url}")
print(f"Page Title: {my_website_explorer.title}")
print(f"Found {len(my_website_explorer.all_links)} links.")
# print(my_website_explorer.get_clean_contents()[:500] + "..." if len(my_website_explorer.get_clean_contents()) > 500 else my_website_explorer.get_clean_contents()) # Uncomment to see some of the text!
```

**What's happening in this code?**
- `headers`: Many websites have defenses against programs trying to scrape them. The `User-Agent` line makes our request look like it's coming from a standard web browser, helping us get the content.
- `__init__(self, url)`: This is the core logic:
   - We use `requests.get()` to download the page's HTML. We've added a `timeout` so our program doesn't get stuck if a website takes too long to respond.
    - `BeautifulSoup(self.raw_html_body, 'html.parser')` takes that raw `HTML` and turns it into an object we can easily navigate and search.
    - The loop that uses `irrelevant_tag.decompose()` is super important! It cleans up the `HTML` by removing bits that aren't useful for a brochure, like navigation links, scripts, and image tags. We only want the readable text.
    - `self.text_content` then grabs all that clean text.
    - Finally, we find all the `<a>` (link) tags and extract their `href` attributes. The `requests.compat.urljoin` magic converts any relative links (like `/about-us`) into full, usable URLs (like `https://www.example.com/about-us`), which is crucial for our next step.
- `get_clean_contents()`: A simple helper to return the cleaned title and text content.

**Output**:

If you run the code above, you will find something similar to this

```
Our explorer visited: https://www.example.com
Page Title: Example Domain
Found 1 links.
```

## 3. The Smart Link Filter: Guiding Our Text Engine

A website has tons of links! such as the above examples, most are for navigation, privacy policies, or internal sections that aren't useful for a general brochure. We need a way to find only the links that would be relevant, like "About Us," "Careers," or "Products." This is where our powerful text-generating engine comes in. We'll ask it to be a super-smart filter!

### 3.1 Our Blueprint for Filtering: The `System Message`

We need to give our text engine clear instructions on how to act. This is like handing it a detailed job description. We'll tell it to be an "expert web analyst" and even show it exactly how we want the filtered links returned (in a structured format called JSON).

```python
# This is our instruction set for the text-generating engine, telling it how to filter links.
link_filtering_instructions = """
You are an expert web analyst tasked with identifying key company information.
You will be provided with a raw list of links found on a webpage.
Your goal is to intelligently select only those links that would be **most relevant** for a concise company brochure.
Think: "What would a prospective customer, investor, or job applicant want to know?"
Prioritize links like "About Us," "Company," "Careers," "Our Team," "What We Offer," "Products," "Solutions," "Blog" (if relevant for insights).
**Absolutely exclude** irrelevant links such as: "Terms of Service," "Privacy Policy," "Contact Us" (unless it's a primary sales contact), internal navigation anchors (e.g., #section-id), or email addresses.

**Your response MUST be in strict JSON format**, like this example:

{
"links": [
{"type": "about page", "url": "https://full.url/goes/here/about"},
{"type": "careers page", "url": "https://another.full.url/careers"},
{"type": "blog", "url": "https://company.com/blog"}
]
}
"""
# You can uncomment the line below to read these instructions in full.
# print(link_filtering_instructions)
```

**Why are these instructions so important?**
- **Clear Role**: We tell the engine to act as an "expert web analyst."
- **Specific Goal**: We define exactly what kind of links we're looking for.
- **Exclusions**: Crucially, we tell it what not to include, like "Terms of Service." This saves us from a lot of unwanted links.
- **Structured Output (JSON)**: By giving it an example of JSON, we train it to respond in a format our Python code can easily understand and use.

### 3.2 The Specific Request: Building Our `User Message` for `Links`

Now, we'll combine our general instructions with the actual list of links our `Website` explorer found. This is the specific question we'll send to the text-generating engine.

```python
def prepare_link_request_message(website_object):
    """
    Creates the specific message we'll send to the text-generating engine to filter links.
    It includes instructions and the list of links from the website.
    """
    user_request = f"Okay, AI expert, I've just visited **{website_object.url}**.\n"
    user_request += "Here's the full list of links I found on that page. Please apply your expert filtering, "
    user_request += "keeping only the brochure-worthy ones and providing them in the JSON format we discussed.\n"
    user_request += "Here are the links:\n"
    # Join all the links found by our Website class into a single string for the AI
    user_request += "\n".join(website_object.all_links)
    return user_request

# Let's see what this request message looks like for our test website!
# print(prepare_link_request_message(my_website_explorer))
```

### 3.3 Sending the Request: Talking to the Text Engine!

This is where the magic happens! We'll send our instructions and the links to the text-generating engine, and it will send back a neatly filtered list.

```python
def get_relevant_links_from_ai(main_website_url):
    """
    Connects to our text-generating engine to intelligently filter and return
    only the relevant links from a given website URL.
    """
    # First, let our Website explorer visit the main URL
    website_data = Website(main_website_url)
    
    # If our explorer couldn't find any links, we can't ask the AI to filter them!
    if not website_data.all_links:
        print(f"No links found or error occurred for {main_website_url}. Skipping link filtering.")
        return {"links": []} # Return an empty list of links

    print(f"Asking the text engine to filter links from {main_website_url}...")
    try:
        # Send the request to the text-generating engine
        response = text_engine_client.chat.completions.create(
            model=TEXT_GENERATION_MODEL, # Which engine version to use
            messages=[
                {"role": "system", "content": link_filtering_instructions}, # Our job description for the AI
                {"role": "user", "content": prepare_link_request_message(website_data)} # Our specific request
            ],
            response_format={"type": "json_object"}, # Crucial: tell it we absolutely want JSON!
            temperature=0.0 # Keep it focused! No creative interpretations for link filtering.
        )
        # Get the AI's response and convert it from JSON text to a Python dictionary
        ai_response_text = response.choices[0].message.content
        return json.loads(ai_response_text)
    except json.JSONDecodeError as e:
        print(f"The text engine returned invalid JSON: {ai_response_text}. Error: {e}")
        return {"links": []} # Return empty if JSON is broken
    except Exception as e:
        print(f"An error occurred during link filtering for {main_website_url}: {e}")
        return {"links": []} # Return empty on other errors

# --- Let's put our link filter to the test! ---
print("\n--- Testing our Smart Link Filter for Hugging Face ---")
# Replace with any website you want to test!
huggingface_links_filtered = get_relevant_links_from_ai("https://huggingface.co")

print("Our smart filter found these relevant links:")
# Nicely print the links that the AI identified as important
for link_item in huggingface_links_filtered.get("links", []):
    print(f"  - Type: {link_item.get('type', 'Unknown')}, URL: {link_item.get('url', 'N/A')}")
```

**Key points in this code**
- `text_engine_client.chat.completions.create()`: This is the command that sends our request to the text-generating engine.
- `response_format={"type": "json_object"}`: This is a powerful instruction! It forces the text engine to give us back valid JSON, which makes it much easier for our Python code to process its answer.
- `temperature=0.0`: This controls how "creative" or "random" the text engine is. For filtering links, we want it to be very precise and not make up new types of links, so we set it to 0.0 (no creativity).
- `json.loads(ai_response_text)`: This line takes the text that the engine sends back (which is formatted as JSON) and converts it into a Python dictionary, so we can easily access the "links" and their "url" and "type".
- **Error Handling**: We've included try-except blocks to gracefully handle situations where the website might not respond, or the text engine might return something unexpected.

**Your Next Test**: Run the code block above for `https://huggingface.co`. 
- What "types" of `links` did our smart filter identify as important? 
- Do they make sense for a company brochure? 
- Try another well-known company website if you like!

## 4. The Brochure Builder: Crafting the Story

Now for the main event! We have the main website content, and we have the list of relevant sub-pages. It's time to feed all this information to our text-generating engine and ask it to craft a full, compelling brochure.

### 4.1 Gathering All the Raw Materials for the Brochure

First, we need to collect **all** the text from the main page and **all** the relevant sub-pages that our smart filter identified. We'll combine it all into one big chunk of text.

```python
def gather_all_website_content(main_website_url):
    """
    Collects the text content from the main URL and then from all the
    relevant sub-links identified by our smart filter.
    """
    all_combined_content = ""
    print(f"Starting to gather content from the main page: {main_website_url}")
    
    # Get content from the main page
    main_page_explorer = Website(main_website_url)
    if main_page_explorer.text_content:
        all_combined_content += "--- MAIN LANDING PAGE CONTENT ---\n" + main_page_explorer.get_clean_contents()
    else:
        print(f"Could not get content from the main page: {main_website_url}. This might affect brochure quality.")
        # We'll still try to proceed if possible, but warn the user.

    # Now, use our smart filter to get the relevant sub-links
    print("Asking our smart filter for relevant sub-links...")
    relevant_sub_links_data = get_relevant_links_from_ai(main_website_url)

    if not relevant_sub_links_data or not relevant_sub_links_data.get("links"):
        print("Our smart filter found no additional relevant links. Brochure will be based only on the main page.")
        return all_combined_content # Return what we have so far

    print(f"Found {len(relevant_sub_links_data['links'])} additional relevant pages. Now fetching their content...")
    
    # Visit each relevant sub-link and add its content
    for link_details in relevant_sub_links_data["links"]:
        page_type = link_details.get("type", "Relevant Page")
        page_url = link_details.get("url")
        
        if page_url:
            try:
                print(f"  - Fetching content for {page_type}: {page_url}")
                sub_page_explorer = Website(page_url)
                if sub_page_explorer.text_content:
                    all_combined_content += f"\n\n--- {page_type.upper()} CONTENT ({page_url}) ---\n" + sub_page_explorer.get_clean_contents()
                else:
                    print(f"    (No content retrieved for {page_url})")
            except Exception as e:
                print(f"    (Error fetching content for {page_url}: {e})")
        else:
            print(f"    (Skipping link with no valid URL: {link_details})")

    return all_combined_content

# --- Warning: This can generate a LOT of text! ---
# Use this for testing, but be aware the output can be very long.
# collected_huggingface_content = gather_all_website_content("https://huggingface.co")
# print("\n--- ALL COLLECTED WEBSITE CONTENT (first 1000 characters) ---")
# print(collected_huggingface_content[:1000] + "..." if len(collected_huggingface_content) > 1000 else collected_huggingface_content)
```

**What's goin' on here?**
- We first use our `Website` explorer to grab the content of the `main_website_url`.
- Then, we call our `get_relevant_links_from_ai` function to get that intelligently filtered list of important sub-pages.
- We loop through each of those important sub-pages, use our `Website` explorer again to fetch their content, and then append it all to our `all_combined_content` string. Now, our text engine will have a complete picture of the company!

### 4.2 The Brochure's Master Plan: Our `System Message` for Brochure Building

This is the big one! We're telling our text engine: "You are now a seasoned marketing copywriter and content strategist. Here's all the info; create a brilliant brochure for these specific audiences!"

```python
# These are the detailed instructions for our text-generating engine to write the brochure.
brochure_creation_instructions = """
You are an expert marketing copywriter and content strategist.
Your mission is to analyze the provided text content from a company's website (including its main page and relevant sub-pages)
and craft a concise, compelling, and professional brochure.

**Your brochure should be designed to appeal to three key audiences simultaneously:**
1.  **Prospective Customers:** Emphasize the value, solutions, and unique benefits the company offers. How do they solve problems?
2.  **Investors:** Focus on the company's vision, growth potential, innovation, and market position. Why is this a good investment?
3.  **Potential Recruits:** Highlight the company culture, mission, team values, and career opportunities. Why should someone work here?

**Structure your brochure with clear, logical sections (if information is available in the provided content):**
* **Introduction:** A captivating hook that introduces the company and its core purpose.
* **About [Company Name]:** Who is this company, what do they do, and what is their overarching mission or vision?
* **What We Offer / Solutions:** Detail their products, services, or solutions and how they benefit users.
* **Our Impact / Success Stories:** Showcase achievements, key customers, or positive results.
* **Culture & Team:** Describe the work environment, company values, and what makes their team special.
* **Careers / Join Us:** Provide insight into job opportunities and why someone should join their team.
* **Conclusion / Call to Action:** A brief summary and clear next steps (e.g., visit website, contact us).

**Formatting Guidelines:**
* Respond entirely in clean, readable **Markdown format**.
* Use clear headings (e.g., `## About [Company Name]`, `### Our Solutions`).
* Employ bullet points for lists of features, benefits, or cultural values.
* Keep the language concise and impactful. Avoid overly technical jargon unless absolutely necessary and explained.
* Ensure a professional, engaging tone that suits a company brochure.

**Crucial Rule:** Only use information directly found in the provided website content. Do not invent facts, details, or statistics. If specific information for a section is not present, gracefully omit that section or provide a general statement based on available context.

"""

# Want to try a different tone? Uncomment the humorous version below and swap it in later!
# brochure_creation_instructions_humorous = """
# You're not just any copywriter; you're a stand-up comedian of content!
# Analyze this company's website content and whip up a hilariously engaging,
# slightly cheeky, but still super informative brochure for customers, investors, and recruits.
# Make it witty, throw in a clever joke or two, but still get the main points across.
# Keep it in Markdown, use fun headings, and don't be afraid to make 'em smile.
# """
```

**Why this detailed instruction set is the 'secret sauce'?**
- **Role Definition**: "You are an expert marketing copywriter..." helps the engine adopt the right writing style.
- **Target Audiences**: Explicitly mentioning customers, investors, and recruits ensures the brochure covers all angles.
- **Structured Sections**: This guides the engine to organize the information logically, just like a real brochure.
- **Formatting Rules (Markdown)**: We tell it how to format the output, so it's easy to read and use.
- **"Crucial Rule: Do Not Invent"**: This is vital for preventing the engine from "hallucinating" or making up information. It ensures the brochure is factual, based only on the website content.

### 4.3 Your Company's Story: The Specific `User Message` for Brochure Building

This is the final message we send to the text-generating engine. It simply states the company's name and provides all the collected website content.

```python
def prepare_brochure_request_message(company_name, main_website_url):
    """
    Prepares the final message containing the company name and all the
    gathered website content, ready to be sent for brochure generation.
    """
    user_request = f"Alright, master copywriter, here's the company we're focusing on: **{company_name}**.\n"
    user_request += f"I've diligently gathered all the relevant content from its website (starting at {main_website_url}) "
    user_request += "and its key sub-pages. Please use this information to craft that amazing, concise, and professional brochure, "
    user_request += "following all the guidelines we discussed.\n\n"
    
    # Get all the actual text content from the website
    full_website_content = gather_all_website_content(main_website_url)
    
    # Important: Large text inputs can hit the text engine's limits.
    # We'll truncate the content if it's too long (30,000 characters is a safe rough estimate for 'gpt-4o-mini').
    if len(full_website_content) > 30000:
        print("\nNote: The collected website content was very long and has been truncated to fit the AI's input limits.")
        user_request += full_website_content[:30000]
    else:
        user_request += full_website_content
    
    return user_request

# --- For testing, this will show you the full text sent to the AI (it can be VERY long!) ---
# print(prepare_brochure_request_message("Hugging Face", "https://huggingface.co")[:1000] + "..." if len(prepare_brochure_request_message("Hugging Face", "https://huggingface.co")) > 1000 else prepare_brochure_request_message("Hugging Face", "https://huggingface.co"))
```

**Why the if `len(full_website_content) > 30000`: line?** 

Text-generating engines have a maximum amount of text they can process in one go (called "context window" or "token limit"). For very large websites, our `full_website_content` might exceed this. Truncating it ensures our request will fit, though for extremely large sites, you might need more advanced techniques like summarizing chunks of text before feeding them to the main generation step.

### 4.4 The Grand Reveal: Generating Your Brochure!

This is the climax! We send our final request to the text-generating engine, and it works its magic to produce the brochure.

```python
def create_company_brochure(company_name, main_website_url):
    """
    Orchestrates the entire process: gathers all relevant website content,
    and then instructs the text-generating engine to create the brochure.
    """
    print(f"\n--- Get ready! Generating your brochure for {company_name} from {main_website_url} ---")
    
    # Prepare the complete request message for the text engine
    final_request_message = prepare_brochure_request_message(company_name, main_website_url)

    print("Our expert writer is now crafting your brochure. This might take a moment...")
    try:
        # Send the final request to the text-generating engine
        response = text_engine_client.chat.completions.create(
            model=TEXT_GENERATION_MODEL, # Our chosen engine version
            messages=[
                {"role": "system", "content": brochure_creation_instructions}, # The brochure writing instructions
                {"role": "user", "content": final_request_message}      # The company's full story
            ],
            temperature=0.7 # A bit more creativity here for compelling writing, but not too wild.
        )
        # Get the brochure content from the AI's response
        generated_brochure_content = response.choices[0].message.content
        print("\n--- Brochure Complete! Here's your masterpiece! ---")
        
        # Display the generated Markdown content beautifully (especially good in Jupyter!)
        display(Markdown(generated_brochure_content))
        return generated_brochure_content
    except Exception as e:
        print(f"\nOh no! An error occurred during brochure generation: {e}")
        print("This often happens if the input content was too long, or there was a network issue. Try a different URL or reduce complexity.")
        return None

# And now, the moment you've been waiting for!
# Let's create a brochure! Try it with your favorite company or a well-known public website.
# Example:
create_company_brochure("Tokopedia", "https://tokopedia.com")
```

**Understanding the Final Step**

- We're making one last call to `text_engine_client.chat.completions.create()`.
- We provide the `brochure_creation_instructions` (our detailed blueprint for the brochure) and the `final_request_message` (containing all the collected website content).
- `temperature=0.7`: Notice we've increased the temperature a bit here (from 0.0 for filtering). For creative writing tasks like a brochure, a slightly higher temperature allows the engine to be a bit more imaginative in its phrasing, making the output more engaging, but without going completely off-topic.
- `display(Markdown(generated_brochure_content))`: If you're in a Jupyter notebook, this line will render the Markdown output into a nicely formatted, readable brochure right in your output cell!

**Your Final Challenge**: Run the `create_company_brochure` function! Try it with `https://huggingface.co, https://openai.com, https://tokopedia.com`, or even a local business website you know. See the magic unfold!

## 5. Results

After running `create_company_brochure("Tokopedia", "https://tokopedia.com")`. 

This is my results:

---

--- Brochure Complete! Here's your masterpiece! ---
# Tokopedia Brochure

## Introduction

Welcome to Tokopedia, Indonesia's leading online marketplace dedicated to creating equal economic opportunities. Our mission is to break down barriers and build a super ecosystem where anyone can start and discover anything.

## About Tokopedia

Tokopedia is a pioneering technology company focused on achieving digital economic equality across the vast archipelago of Indonesia. With over 12 million registered sellers and 638 million products listed, we are committed to empowering people and businesses by providing a comprehensive platform for e-commerce, logistics, and advertising.

## What We Offer / Solutions

At Tokopedia, we provide a multitude of services designed to simplify commerce for both buyers and sellers:
- **E-Commerce Platform**: A diverse marketplace featuring various products, including digital goods and instant commerce options.
- **Integrated Logistics & Fulfillment**: Streamlined shipping solutions that make delivery easy and efficient.
- **Advertising & Marketing Technology**: Tools to help sellers promote their businesses, including Pay for Performance (P4P) Advertising and customized marketing packages.

## Our Impact / Success Stories

Our commitment to Indonesia's economy has led to remarkable achievements:

- **Empowerment of Micro-Sellers**: 90% of our sellers are micro-businesses, benefiting from digital adoption during challenging times.
- **Volume Growth**: 7 out of 10 businesses report increased sales through our platform, with a 133% sales growth during the pandemic.
- **Financial Inclusion**: Promoting digital payment methods, facilitating access to e-wallets and mobile banking for consumers.

## Culture & Team

At Tokopedia, we prioritize the well-being of our team, known as Nakama. Our culture is built on inclusivity and development, offering:

- **Career Growth Opportunities**: We support our employees' professional journeys.
- **Comprehensive Health Benefits**: Ensuring our Nakama's health and wellness is a top priority.
- **Diverse Leave Options**: Promoting work-life balance with various leave policies.

## Careers / Join Us

Be part of our transformative journey! We invite passionate individuals to explore career opportunities that align with their goals and aspirations. At Tokopedia, you will be valued and empowered to make a difference.

## Conclusion / Call to Action

Discover how Tokopedia is reshaping the digital landscape in Indonesia. For more information, visit our website at [tokopedia.com](https://tokopedia.com) or join our team today! Let’s create opportunities together!

---

See ya on the next fun article!
