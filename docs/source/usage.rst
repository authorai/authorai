Usage
=====

.. _installation:

Installation
------------

To use AuthorAI, first install it using pip:

.. code-block:: console

   (.venv) $ pip install authorai

Creating Blog Posts
-------------------

Here is an example of a 100% auto generated blog post by providing three concepts - Art, Physics, and City to AuthorAI API.

![AuthorAI Blogger Post](https://raw.githubusercontent.com/authorai/authorai/main/blogger-post.png)

You can auto generate this blog post in a single API call like so.

```
from authorai import blogger
keywords = ['Physics', 'Art', 'City']
blogger.auto_generate(keywords, verbose=True)
```

You can also customize the features and content of the blog within few lines of code using AuthorAI Blogger API.

```
from authorai import blogger

post = blogger.BlogPost()

post.set_auto(True)
post.set_full_feature(True)

keywords = ['Physics', 'Art', 'City']

response, response_list = blogger.concepts_combining_keywords(keywords)

post.set_concept(response_list[3])

topic = blogger.describe_concept(post.get_concept(), words=200, grade=10)
post.set_topic(topic)

response, response_list = blogger.titles_from_topic(post.get_topic())
post.set_title(response_list[6])

response, response_list = blogger.tags_from_topic(post.get_topic())
post.set_tags(response_list)

question = 'Is this concept ' + post.get_tags()[3] + ' ' + post.get_tags()[1] +  ' a thing?'
post.set_qna(question, blogger.qna(question))

response, reponse_list = blogger.leaderboard(topic, 'Movies', count=5)
post.set_leaderboard('Movies', response)

quote_text = blogger.quote(', '.join(concepts))
post.set_quote(quote_text)

image_description = blogger.strip_filename(blogger.summarize(post.get_topic(), words=10))
image_url = blogger.image_from_description('a 3d photo realistic painting of topic ' + image_description)

local_image = blogger.save_image(url=image_url, description=image_description)
post.set_feature_image(local_image)

post_html = blogger.generate_html(post)
html_path, markdown_path = blogger.publish(post_html=post_html, filename='-'.join(concepts))
```