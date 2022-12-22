# Copyright (c) 2022-present AuthorAI.org (authorai.org@gmail.com)

# Installed packages from requirements.txt
import openai
from bs4 import BeautifulSoup
import markdownify
import urllib.request

# Pre-installed packages
import os
from random import randrange
import re
import datetime
import sys

openai.api_key = os.getenv("OPENAI_KEY")
openai_model = 'text-davinci-003'

class BlogPost:
    """BlogPost is used to store completion results and then publish the blog post."""
    def __init__(self):
        self.auto = True
        self.full_feature = False
        self.keywords = []
        self.concept = ''
        self.title = ''
        self.topic = ''
        self.tags = []
        self.qna = {}
        self.leaderboard = {}
        self.quote = ''
        self.feature_image = ''

    def set_auto(self, auto: bool):
        self.auto = auto  
    def get_auto(self):
        return self.auto

    def set_full_feature(self, full_feature: bool):
        self.full_feature = full_feature  
    def get_full_feature(self):
        return self.full_feature    

    def set_keywords(self, keywords: list[str]):
        self.keywords = keywords  
    def get_keywords(self):
        return self.keywords

    def set_concept(self, concept: str):
        self.concept = concept  
    def get_concept(self):
        return self.concept
        
    def set_title(self, title: str):
        self.title = title  
    def get_title(self):
        return self.title
    
    def set_topic(self, topic: str):
        self.topic = topic  
    def get_topic(self):
        return self.topic
    
    def set_tags(self, tags: list[str]):
        self.tags = tags  
    def get_tags(self):
        return self.tags
    
    def set_qna(self, question: str, answer: str):
        self.qna[question] = answer
    def get_qna(self):
        return self.qna
    def get_answer(self, question: str):
        return self.qna[question]

    def set_quote(self, quote: str):
        self.quote = quote  
    def get_quote(self):
        return self.quote    

    def set_leaderboard(self, entity: str, top_list: str):
        self.leaderboard[entity] = top_list
    def get_leaderboard(self):
        return self.leaderboard
    def get_top_list(self, entity: str):
        return self.leaderboard[entity]
    
    def set_feature_image(self, feature_image: str):
        self.feature_image = feature_image  
    def get_feature_image(self):
        return self.feature_image


def openai_completion(prompt, temperature=0.9, tokens=70, model=openai_model):
    """AuthorAI wrapper for OpenAI Completion API.

    Args:
        prompt: Zero/few-shot learning prompt for generating a completion.
        temperature: Model takes more risks with higher values (0.9), model is deterministic at 0.
        tokens: Similar count as words in prompt plus completion. Counts towards OpenAI API cost.
        model: Model version of OpenAI GPT to run.

    Returns:
        The as-is completion response as JSON.
    """
    response = openai.Completion.create(
        model=model, prompt=prompt, temperature=temperature, max_tokens=tokens)
    return response

def completion_list(prompt, tokens=70, temperature=0.9):
    """Converts text completion to a Python list. 
    
    Use when the prompt is requesting a numbered list of items.

    Args:
        prompt: Zero/few-shot learning prompt for generating a completion.
        temperature: Model takes more risks with higher values (0.9), model is deterministic at 0.
        tokens: Similar count as words in prompt plus completion. Counts towards OpenAI API cost.

    Returns:
        response: The full-text completion.
        response_list: Completion as a Python list.
    """    
    response = openai_completion(prompt, tokens=tokens, temperature=temperature)
    response = response.choices[0].text.strip()
    response = response.replace(response[:response.find('1.')], "")
    strip_response = re.sub(r'\d+. ', '', response)
    response_list = strip_response.split('\n')
    return response, response_list

def concepts_combining_keywords(keywords, count=10):
    """Generates a list of concepts by combinining keywords.

    Args:
        keywords: Python list of keywords to combine into ideas.
        count: Number of ideas to generate.
    
    Returns:
        response: The full-text completion.
        response_list: Completion as a Python list.
    """
    prompt = 'Brainstorm a list of ' + str(count)
    prompt += ' concepts combining the keywords ' + ', '.join(keywords)
    response, response_list = completion_list(prompt, tokens=count*20)
    return response, response_list

def strip_trailing_sentence(paragraph: str) -> str:
    """Cleans incomplete last sentence returned as completion.

    Used on completions which are single or multiple paragraphs of text. 

    Args:
        paragraph: Original completion response as free text.

    Returns:
        paragraph: Stripped completion response as free text.
    """
    if not paragraph.endswith("."):
        return paragraph.rsplit(".", 1)[0] + "."
    return paragraph

def describe_concept(concept, words=50, grade=5):
    """Takes a concept and describes it in given number of words with grade N level English.

    Args:
        concept: A short sentence to be described.
        words: Number of words/tokens to be used by completion.
        grade: Completion will use this grade level English.
    
    Return:
        completion: Completion as paragraph(s) of free text.
    """
    prompt = 'Describe the concept "' + concept
    prompt += '" in ' + str(words) + ' words'
    prompt += ' using English understood by grade level ' + str(grade) + '.'
    completion = openai_completion(prompt, tokens=words, temperature=0).choices[0].text.strip()
    return strip_trailing_sentence(completion)

def titles_from_topic(topic, count=10):
    """Generate list of blog post titles based on topic.
    
    Args:
        topic: A topic description.
        count: Number of titles to return.
    
    Returns:
        response: The full-text completion.
        response_list: Completion as a Python list.
    """
    prompt = 'Suggest ' + str(count) 
    prompt += ' catchy, unique, and SEO friendly blog post titles based on the topic:\n' + topic
    return completion_list(prompt, tokens=count*20)

def tags_from_topic(topic, count=10):
    """Generates count number of tags based on a given topic.

    Args:
        topic: A topic description.
        count: Number of tags to return.
    
    Returns:
        response: The full-text completion.
        response_list: Completion as a Python list.
    """
    prompt = 'Suggest a numbered list of ' + str(count) 
    prompt += ' nouns representing the topic:\n' + topic
    return completion_list(prompt, tokens=count*20)

def qna(question):
    """Generate an answer to a question as prompt.

    Args:
        question: A question prompt to get answer.
    
    Returns:
        response: The full-text completion.
    """
    prompt='Q: '
    prompt+=question + '\nA:'
    response = openai.Completion.create(
        model=openai_model,
        prompt=prompt,
        temperature=0,
        max_tokens=100,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\n"]
    )
    return response.choices[0].text.strip()

def quote(concept):
    """Generate a quotable quote based on a concept.

    Args:
        concept: A short sentence about an idea.

    Returns:
        response_quote: A quotable quote as completion response.
    """
    prompt='Suggest a famous quote about ' + concept + '.'
    response = openai.Completion.create(
        model=openai_model,
        prompt=prompt,
        temperature=0.9,
        max_tokens=100    
    )
    response_quote = response.choices[0].text.strip()
    return response_quote

def summarize(topic, words=20, grade=5):
    """Summarizes a topic to N words and writes the completion in grade N level English.

    Args:
        topic: Free text paragraph(s) to be summarized.
        words: Number of words/tokens to be used by completion.
        grade: Completion will use this grade level English.
    
    Return:
        completion: Completion as summary in N words.
    """
    prompt = 'Summarize ' + topic
    prompt += ' in ' + str(words) + ' words '
    prompt += ' using English understood by grade level ' + str(grade) + '.'
    return openai_completion(prompt, temperature=0.9).choices[0].text.strip()

def leaderboard(topic, entity, count=10):
    """Recommends an ordered list of Top N entities.

    Args:
        topic: Free text paragraph(s) to inform the leaderboard.
        entity: The entity to recommend.
        count: Number of top N results.
    Returns:
        response: The full-text completion.
        response_list: Completion as a Python list.
    """
    prompt = 'Recommend ordered list of top ' + str(count) + ' ' + entity
    prompt += ' based on topic ' + topic + '.'
    return completion_list(prompt, tokens=count*20)

def image_from_description(description, size="1024x1024"):
    """Uses DALL.E Image generation API to create an image based on description provided.
    
    Args:
        description: Description of the image to be generated.
    Returns:
        image_url: Generated PNG image url.
    """
    response = openai.Image.create(
      prompt=description,
      n=1,
      size=size
    )
    image_url = response['data'][0]['url']
    return image_url

def strip_filename(filename: str) -> str:
    """Strip a filename of any characters which are not alphabets while preserving whitespace.

    Args:
        filename: File name to strip.
    Returns:
        filename_stripped: Stipped file name. Maybe same as input.
    """
    filename_stripped = re.sub(r'[^a-zA-Z\s]', '', filename)
    return filename_stripped


def save_image(url, description, folder='', ext='png'):    
    """Saves a PNG  image to a local folder from a source URL using description as file name.

    Args:
        url: PNG image url to save.
        description: Long file name to use.
        folder: Folder where image will be saved locally.
    Returns:
        filename: Local image file name.
    """
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y%m%d%H%M%S')
    filename = description + ' ' + timestamp + '.' + ext
    local_file_path = os.path.join(folder, filename)
    urllib.request.urlretrieve(url, local_file_path)
    return filename

def generate_html(post):
    """Generates HTML from blog post object.

    Args:
        post: Blog post object.
    Returns:
        post_html: HTML string rendering blog post.
    """
    post_html = '<html>'
    post_html += '''
        <head>
            <style>
            body {
              font-family: Verdana;  
            }

            .box {
              width: 800px;
              height: 70px;
              border: 2px solid #000;
              margin: 0 auto 20px;
              text-align: center;
              padding: 10px;
              border-radius: 5px;
            }

            .warning {
              background-color: #FFF484;
              border-color: #DCC600;
            }
            .feature  {
                float: left;
                padding-right: 15px;
            }
            .full_feature  {
                padding-bottom: 15px;
            }
            </style>
        </head>'''
    post_html += '<body>'

    if post.get_auto():
        post_html += '<div class="warning box">' 
        post_html += '''This blog post was 100% AI generated using AuthorAI API. 
            Powered by OpenAI GPT3 and DALL.E. For demo purposes only.'''
        post_html += '</div>' 
        
    post_html += '<h1 align="center">' + post.get_title() + '</h1>'
    post_html += '<h3 align="center"">' + post.get_concept() + '</h3></br>'

    if post.get_full_feature():
        post_html += '<div class="full_feature" align="center">'
        post_html += '<img src="' + post.get_feature_image() + '" width="1024" height="1024">'
        post_html += '</div>'
    else:
        post_html += '<div class="feature">'
        post_html += '<img src="' + post.get_feature_image() + '" width="356" height="356">'
        post_html += '</div>'

    post_html += '<p>' + post.get_topic() + '</p>'

    post_html += '<br><div align="center"><h2><i>' + post.get_quote() + '</i></h2></div><br>'

    post_html += '<div align="left">'
    for key, value in post.get_qna().items():
        post_html += '<b>' + key +  '</b>'
        post_html += '<p>' + value +  '</p>'
    post_html += '</div>'

    post_html += '<div align="center">'
    post_html += '<h3>' + 'Leaderboard' + '</h3>'
    post_html += '<table><tr>'
    for key in post.get_leaderboard().keys():
        post_html += '<th>' + key + '</th>'
    post_html += '</tr><tr>'
    for value in post.get_leaderboard().values():
        post_html += '<td><p>' + value + '</p></td>'
    post_html += '</tr></table>'
    post_html += '</div>'
    
    post_html += '<hr>'
    post_html += '<div align="center"> <b>Tags: </b><mark>' + ' | '.join(post.get_tags()) + '</mark></div>'
    post_html += '</body></html>'
    return post_html

def publish(post_html, filename, folder=''):
    """Saves a local copy of html and html to markdown converted file.

    Args:
        post_html: HTML string rendering the blog post.
        folder: Local folder to save HTML and markdown files.
        filename: File name prefix to use for the published HTML and markdown files.
    Returns:
       html_filename: Local HTML file name.
       md_filename: Local Markdown file name.
    """
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y%m%d%H%M%S')
    soup = BeautifulSoup(post_html, "html.parser")
    pretty_html = soup.prettify()
    html_filename = filename + '-' + timestamp + '.html'
    local_html_file = os.path.join(folder, html_filename)
    md_filename = filename + '-' + timestamp + '.md'
    local_markdown_file = os.path.join(folder, md_filename)
    markdown = markdownify.markdownify(pretty_html, heading_style="ATX")
    with open(local_html_file, 'w') as file:
        file.write(pretty_html)
    with open(local_markdown_file, 'w') as file:
        file.write(markdown)
    return html_filename, md_filename

def auto_generate(keywords, folder='', verbose = False):
    """Generates the blog post combinining features specific APIs into one call.
    
    Args:
        keywords: Keywords to use to auto generate the blog post.
        verbose: Print verbose output of each step is True.
    Returns:
        local_image: Local image file path.
        local_html_file: Local HTML file path.
        local_markdown_file: Local Markdown file path.
    """
    # Setup
    post = BlogPost()
    post.set_auto(True)
    post.set_full_feature(True)
    post.set_keywords(keywords)

    # Ideate
    response, response_list = concepts_combining_keywords(keywords)
    print(response) if verbose else None
    post.set_concept(response_list[randrange(len(response_list)-1)])
    print(post.get_concept()) if verbose else None

    # Research
    topic = describe_concept(post.get_concept(), words=200, grade=10)
    post.set_topic(topic)
    print(post.get_topic()) if verbose else None

    # Write
    response, response_list = titles_from_topic(post.get_topic())
    print(response) if verbose else None
    post.set_title(response_list[randrange(len(response_list)-1)])
    print(post.get_title()) if verbose else None
    response, response_list = tags_from_topic(post.get_topic())
    post.set_tags(response_list)

    # Enhance
    print(post.get_tags()) if verbose else None
    question = 'Is this concept ' + post.get_tags()[3] + ' ' + post.get_tags()[1] +  ' a thing?'
    post.set_qna(question, qna(question))
    question = 'What is the importance of ' + post.get_tags()[5] + '?'
    post.set_qna(question, qna(question))
    question = 'Is there a relationship between ' + post.get_tags()[2] + ' and ' + post.get_tags()[7]  + '?'
    post.set_qna(question, qna(question))
    print(post.get_qna()) if verbose else None
    response, reponse_list = leaderboard(topic, 'Movies', count=5)
    post.set_leaderboard('Movies', response)
    response, reponse_list = leaderboard(topic, 'Music Albums', count=5)
    post.set_leaderboard('Music Albums', response)
    response, reponse_list = leaderboard(topic, 'Famous People', count=5)
    post.set_leaderboard('Famous People', response)
    print(post.get_leaderboard()) if verbose else None
    quote_text = quote(post.get_topic())
    post.set_quote(quote_text)
    print(post.get_quote()) if verbose else None

    # Illustrate
    image_description = strip_filename(summarize(post.get_topic(), words=10))
    print(image_description) if verbose else None
    image_url = image_from_description('a 3d photo realistic painting of topic ' + image_description)
    local_image = save_image(url=image_url, folder=folder, description=image_description)
    post.set_feature_image(local_image)
    print(post.get_feature_image()) if verbose else None

    # Publish
    post_html = generate_html(post)
    html_path, markdown_path = publish(post_html=post_html, folder=folder, filename='-'.join(post.get_keywords()))
    return local_image, html_path, markdown_path

