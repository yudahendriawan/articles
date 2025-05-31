# Essential Libraries: These are the tools we just installed!
import os
import requests
import json
from typing import List
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display, update_display
from openai import OpenAI # Our connection to the text-generating engine

# for UI interface
import gradio as gr # oh yeah!

# --- Initial Setup ---
# Load our secret API key from the .env file
load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

# A quick check to make sure our key loaded correctly!
if api_key and api_key.startswith('sk-proj-') and len(api_key) > 10:
    print("API key successfully loaded! Ready to build. 🎉")
else:
    print("Uh oh! There might be a problem with your API key. Double-check your .env file and your OpenAI account. 😕")

# We'll use a specific version of the text-generating engine, 'gpt-4o-mini', for efficiency.
TEXT_GENERATION_MODEL = "gpt-4o-mini"
# This is how we'll send requests to the text-generating engine.
text_engine_client = OpenAI()

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
# test_url = "https://www.example.com" # Feel free to change this!
# my_website_explorer = Website(test_url)

# print(f"Our explorer visited: {my_website_explorer.url}")
# print(f"Page Title: {my_website_explorer.title}")
# print(f"Found {len(my_website_explorer.all_links)} links.")
# # print(my_website_explorer.get_clean_contents()[:500] + "..." if len(my_website_explorer.get_clean_contents()) > 500 else my_website_explorer.get_clean_contents()) # Uncomment to see some of the text!

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

    print(f"🧠 Asking the text engine to filter links from {main_website_url}...")
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
# print("\n--- Testing our Smart Link Filter for Hugging Face ---")
# Replace with any website you want to test!
# huggingface_links_filtered = get_relevant_links_from_ai("https://huggingface.co")

# print("✨ Our smart filter found these relevant links:")
# # Nicely print the links that the AI identified as important
# for link_item in huggingface_links_filtered.get("links", []):
#     print(f"  - Type: {link_item.get('type', 'Unknown')}, URL: {link_item.get('url', 'N/A')}")

def gather_all_website_content(main_website_url):
    """
    Collects the text content from the main URL and then from all the
    relevant sub-links identified by our smart filter.
    """
    all_combined_content = ""
    print(f"📖 Starting to gather content from the main page: {main_website_url}")
    
    # Get content from the main page
    main_page_explorer = Website(main_website_url)
    if main_page_explorer.text_content:
        all_combined_content += "--- MAIN LANDING PAGE CONTENT ---\n" + main_page_explorer.get_clean_contents()
    else:
        print(f"Could not get content from the main page: {main_website_url}. This might affect brochure quality.")
        # We'll still try to proceed if possible, but warn the user.

    # Now, use our smart filter to get the relevant sub-links
    print("🔎 Asking our smart filter for relevant sub-links...")
    relevant_sub_links_data = get_relevant_links_from_ai(main_website_url)

    if not relevant_sub_links_data or not relevant_sub_links_data.get("links"):
        print("Our smart filter found no additional relevant links. Brochure will be based only on the main page.")
        return all_combined_content # Return what we have so far

    print(f"🌐 Found {len(relevant_sub_links_data['links'])} additional relevant pages. Now fetching their content...")
    
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
        print("\n⚠️ Note: The collected website content was very long and has been truncated to fit the AI's input limits.")
        user_request += full_website_content[:30000]
    else:
        user_request += full_website_content
    
    return user_request

# --- For testing, this will show you the full text sent to the AI (it can be VERY long!) ---
# print(prepare_brochure_request_message("Hugging Face", "https://huggingface.co")[:1000] + "..." if len(prepare_brochure_request_message("Hugging Face", "https://huggingface.co")) > 1000 else prepare_brochure_request_message("Hugging Face", "https://huggingface.co"))

def create_company_brochure_stream(company_name, main_website_url):
    """
    Orchestrates the entire process: gathers all relevant website content,
    and then instructs the text-generating engine to create the brochure.
    """
    print(f"\n--- Get ready! Generating your brochure for {company_name} from {main_website_url} ---")
    
    # Prepare the complete request message for the text engine
    final_request_message = prepare_brochure_request_message(company_name, main_website_url)

    print("✍️ Our expert writer is now crafting your brochure. This might take a moment...")
    try:
        # Send the final request to the text-generating engine
        stream = text_engine_client.chat.completions.create(
            model=TEXT_GENERATION_MODEL, # Our chosen engine version
            messages=[
                {"role": "system", "content": brochure_creation_instructions}, # The brochure writing instructions
                {"role": "user", "content": final_request_message}      # The company's full story
            ],
            temperature=0.7, # A bit more creativity here for compelling writing, but not too wild.
            stream=True
        )
        # Get the brochure content from the AI's response
        # generated_brochure_content = response.choices[0].message.content
        print("\n--- Brochure Complete! Here's your masterpiece! ---")
        
        # Display the generated Markdown content beautifully (especially good in Jupyter!)
        # display(Markdown(generated_brochure_content))

        response = ""
        display_handle = display(Markdown(""), display_id=True)
        for chunk in stream:
            response += chunk.choices[0].delta.content or ''
            response = response.replace("```","").replace("markdown", "")
            yield response
            # update_display(Markdown(response), display_id=display_handle.display_id)
        
        # yield from response
        # return response
    except Exception as e:
        print(f"\n❌ Oh no! An error occurred during brochure generation: {e}")
        print("This often happens if the input content was too long, or there was a network issue. Try a different URL or reduce complexity.")
        return None

# 🎉 And now, the moment you've been waiting for!
# Let's create a brochure! Try it with your favorite company or a well-known public website.
# Example:
# create_company_brochure_stream("Tokopedia", "https://tokopedia.com")

# Or try with another one!
# create_company_brochure("OpenAI", "https://openai.com")

view = gr.Interface(
    fn=create_company_brochure_stream,
    inputs=[
        gr.Textbox(label="Company name:"),
        gr.Textbox(label="Landing page URL including http:// or https://")],
    outputs=[gr.Markdown(label="Brochure:")],
    flagging_mode="never"
)
view.launch(inbrowser=True)