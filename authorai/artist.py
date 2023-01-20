import os
import io
from PIL import Image

from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

import urllib.request
import datetime
import random
import warnings

from authorai import core

class Art:
    # Basics properties
    painting_styles = ['realism', 'photorealism', 'expressionism', 'impressionism', 'abstract', 'surrealism', 'pop art', 
        'symbolist', 'artivism', 'religious', 'mythological', 'modernism', 'outsider']
    painting_mediums = ['oil', 'watercolour', 'acrylic', 'gouache', 'pastel', 'encaustic', 'fresco', 'spray paint', 'digital', 
        'hot wax', 'ink', 'enamel', 'tempera', 'matte']
    painting_surfaces = ['walls', 'paper', 'canvas', 'wood', 'glass', 'lacquer', 'pottery', 'leaf', 'copper', 'concrete']
    painting_basics = {'style': painting_styles, 'medium': painting_mediums, 'surface': painting_surfaces}

    # Advanced properties
    painting_subjects = ['history painting', 'concept art' , 'portrait painting', 'genre painting', 'landscape painting', 'still life painting']
    painting_origins = ['indian', 'japanese', 'chinese', 'islamic', 'indonesian', 'mughal']
    painting_advanced = {'subject': painting_subjects, 'origin': painting_origins}

    def __init__(self):
        self.style = ''
        self.medium = ''
        self.surface = ''
        self.subject = ''
        self.origin = ''
        self.description = ''

    def set_description(self, description):
        self.description = description

    def get_description(self):
        return self.description

    def set_basics(self, style='', medium='', surface=''):
        self.style=style
        self.medium=medium
        self.surface=surface

    def get_basics(self):
        return self.style, self.medium, self.surface

    def set_advanced(self, subject='', origin=''):
        self.subject = subject
        self.origin = origin

    def get_advanced(self):
        return self.subject, self.origin

def image_from_description(description, size="1024x1024"):
    """Uses DALL.E Image generation API to create an image based on description provided.
    
    Args:
        description: Description of the image to be generated.
    Returns:
        image_url: Generated PNG image url.
    """
    response = core.openai.Image.create(
      prompt=description,
      n=1,
      size=size
    )
    image_url = response['data'][0]['url']
    return image_url

def save_image(url, description, folder='', ext='png'):    
    """Saves a PNG  image to a local folder from a source URL using description as file name.

    Args:
        url: PNG image url to save.
        description: Long file name to use.
        folder: Folder where image will be saved locally.
    Returns:
        filename: Local image file name.
    """
    description = description[:225] if len(description) > 225 else description

    now = datetime.datetime.now()
    timestamp = now.strftime('%Y%m%d%H%M%S')
    filename = description + ' ' + timestamp + '.' + ext
    local_file_path = os.path.join(folder, filename)
    urllib.request.urlretrieve(url, local_file_path)
    return filename

def prompt_art(art: Art) -> str:
    prompt = art.description
    prompt += (' in ' + art.style + ' style') if art.style else ''
    prompt += (' on ' + art.medium + ' medium') if art.medium else ''
    prompt += (' which is ' + art.subject) if art.subject else ''
    prompt += (' drawn on ' + art.surface + ' surface') if art.surface else ''
    prompt += (' from ' + art.origin + ' origin') if art.origin else ''
    return prompt

def prompt_random_art(description='', words=20, basics=True, advanced=False) -> str:
    art = Art()
    if description == '':
        description = core.openai_completion(
        prompt="Suggest a unique and interesting painting description",
        tokens=int(words * 4/3 + 1),
        temperature=0.9).choices[0].text.strip().replace('.', ',').replace('"', '')
    art.set_description(description)
    if basics: 
        art.set_basics(style=random.choice(Art.painting_basics['style']), 
                medium=random.choice(Art.painting_basics['medium']), 
            surface=random.choice(Art.painting_basics['surface']))
    if advanced: 
        art.set_advanced(subject=random.choice(Art.painting_advanced['subject']), 
            origin=random.choice(Art.painting_advanced['origin']))
    return prompt_art(art)

def generate_art(prompt, size="1024x1024", folder='') -> str:
    url = image_from_description(prompt, size=size)
    filename = save_image(url, description=prompt, folder=folder, ext='png')
    local_file_path = os.path.join(folder, filename)
    return local_file_path

stability_api = client.StabilityInference(
    key=os.environ['STABILITY_KEY'], # API Key reference.
    verbose=True, # Print debug messages.
    engine="stable-diffusion-v1-5", # Set the engine to use for generation. 
    # Available engines: stable-diffusion-v1 stable-diffusion-v1-5 stable-diffusion-512-v2-0 stable-diffusion-768-v2-0 
    # stable-diffusion-512-v2-1 stable-diffusion-768-v2-1 stable-inpainting-v1-0 stable-inpainting-512-v2-0
)

def generate_art_sd(prompt, size=512, folder='') -> str:
    answers = stability_api.generate(
        prompt=prompt,
        cfg_scale=8.0,
        width=size, # Generation width, defaults to 512 if not included.
        height=size, # Generation height, defaults to 512 if not included.
        sampler=generation.SAMPLER_K_DPMPP_2M # Choose which sampler we want to denoise our generation with.
        # Defaults to k_dpmpp_2m if not specified. Clip Guidance only supports ancestral samplers.
        # (Available Samplers: ddim, plms, k_euler, k_euler_ancestral, k_heun, k_dpm_2, k_dpm_2_ancestral, 
        # k_dpmpp_2s_ancestral, k_lms, k_dpmpp_2m)
    )

    # Set up our warning to print to the console if the adult content classifier is tripped.
    # If adult content classifier is not tripped, save generated images.
    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                warnings.warn(
                    "Your request activated the API's safety filters and could not be processed."
                    "Please modify the prompt and try again.")
            if artifact.type == generation.ARTIFACT_IMAGE:
                filename = prompt[:225] if len(prompt) > 225 else prompt
                img = Image.open(io.BytesIO(artifact.binary))
                filename = filename + '-' + str(artifact.seed)+ ".png"
                local_file_path = os.path.join(folder, filename)
                img.save(local_file_path) # Save our generated images with their seed number as the filename.  
                return local_file_path  

def help(style='', medium='', surface='', subject='', origin=''):
    prompt = 'Suggest a matching style, medium and surface for ' + subject + '.' \
        if subject and not style and not medium and not surface and not origin else ''
    prompt = 'Suggest a matching painting style, medium and surface for ' + origin + ' origin painting.' \
        if origin and not style and not medium and not surface and not subject else ''
    prompt = 'Suggest a matching painting style, medium and surface for ' + origin + ' origin ' + subject + '.' \
        if origin and not style and not medium and not surface and not subject else ''
    if not prompt:
        prompt = 'What is the best painting '
        prompt += ' style to use on ' if not style and medium and surface else ''
        prompt += ' medium to use with ' if not medium and style and surface else ''
        prompt += ' surface to paint for ' if not surface and style and medium else ''
        prompt += ' style and using which medium to paint on ' if not style and not medium and surface else ''
        prompt += ' medium to use on which surface for ' if not medium and style and not surface else ''
        prompt += ' style and surface to paint with ' if not surface and not style and medium else ''
        prompt += style + ' style' if style else ''
        prompt += medium + ' medium' if medium else ''
        prompt += surface + ' surface' if surface else ''
        prompt += '?'
    completion = core.openai_completion(
        prompt=prompt,
        tokens=200,
        temperature=0.3).choices[0].text.strip()
    return completion

# generate a prompt to create a professional quality painting based on a list of keywords
def generate_prompt(keywords, words=50):
    prompt = '''As a professional artist suggest a unique and
        interesting painting description based on keywords: ''' + ', '.join(keywords) + '.'
    prompt = core.openai_completion(
        prompt=prompt,
        tokens=int(words * 4/3 + 1),
        temperature=0.9).choices[0].text.strip()
    return prompt