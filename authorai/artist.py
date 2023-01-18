from authorai import blogger

class Art:
    # Basics properties
    painting_styles = ['Realism', 'Photorealism', 'Expressionism', 'Impressionism', 'Abstract', 'Surrealism', 'Pop Art', 
        'Symbolist', 'Artivism', 'Religious', 'Mythological', 'Modernism', 'Outsider']
    painting_mediums = ['Oil', 'Watercolour', 'Acrylic', 'Gouache', 'Pastel', 'Encaustic', 'Fresco', 'Spray Paint', 'Digital', 
        'Hot wax', 'Ink', 'Enamel', 'Tempera']
    painting_surfaces = ['walls', 'paper', 'canvas', 'wood', 'glass', 'lacquer', 'pottery', 'leaf', 'copper', 'concrete', 'matte']
    painting_basics = {'styles': painting_styles, 'mediums': painting_mediums, 'surfaces': painting_surfaces}

    # Advanced properties
    painting_subjects = ['History Painting', 'Concept Art' , 'Portrait Painting', 'Genre Painting', 'Landscape Painting', 'Still Life Painting']
    painting_materials = ['sand', 'clay', 'paper', 'plaster', 'gold leaf']
    painting_origins = ['indian', 'japanese', 'chinese', 'islamic', 'indonesian', 'mughal']
    painting_advanced = {'subjects': painting_subjects, 'materials': painting_materials, 'origins': painting_origins}

    def __init__(self):
        self.style = ''
        self.medium = ''
        self.surface = ''
        self.subject = ''
        self.material = ''
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
        return self.style, self.medium, self.subject

    def set_advanced(self, subject='', material='', origin=''):
        self.subject = subject
        self.material = material
        self.origin = origin

    def get_advanced(self):
        return self.subject, self.material, self.origin


def create_art(art: Art, size="1024x1024") -> str:
    prompt = art.description
    prompt += (' in ' + art.style + ' style') if art.style != '' else ''
    prompt += (' on ' + art.medium + ' medium') if art.medium != '' else ''
    prompt += (' which is ' + art.subject) if art.subject != '' else ''
    prompt += (' drawn on ' + art.surface + ' surface') if art.surface != '' else ''
    prompt += (' using ' + art.material + ' material') if art.material != '' else ''
    prompt += (' from ' + art.origin + ' origin') if art.origin != '' else ''
    url = blogger.image_from_description(prompt, size=size)
    return url, prompt
