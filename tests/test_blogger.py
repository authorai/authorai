from authorai import blogger
import os

post = blogger.BlogPost()
post.set_keywords(['Earth', 'Mars', 'Travel'])

class TestOpenai:
    def test_openai_completion(self):
        response = blogger.openai_completion('Where are the great pyramids located?')
        response = response.choices[0].text.strip().lower()
        assert 'egypt' in response, 'expect "egypt" in completion for great pyramids location'

class TestCompletionList:
    def test_completion_list_response(self):
        response, response_list = blogger.completion_list('List top 10 highest grossing movies.')
        response_test = ','.join(response_list).lower()
        assert 'avatar' in response_test, 'expect "avatar" in top 10 grossing movies'

    def test_completion_list_length(self):
        response, response_list = blogger.completion_list('List 10 famous scientists.', tokens=200)
        assert len(response_list) == 10, 'expect 10 items in completion'

class TestIdeate:
    def test_concepts_combining_keywords(self):
        response, response_list = blogger.concepts_combining_keywords(post.get_keywords())
        post.set_concept(response_list[5])
        assert len(response_list) == 10, 'expect 10 concepts combining keywords'

class TestResearch:
    def test_describe_concept(self):
        response = blogger.describe_concept('Quantum Computing', words=200, grade=2)
        post.set_topic(response)
        assert 'quantum computing' in response.lower(), 'expect "quantum computing" phrase in response'

class TestWrite:
    def test_titles_from_topic(self):
        response, response_list = blogger.titles_from_topic(post.get_topic())
        post.set_title(response_list[3])
        assert len(response_list) == 10, 'expect 10 titles'

    def test_tags_from_topic(self):
        response, response_list = blogger.tags_from_topic(post.get_topic())
        post.set_tags(response_list)
        assert len(response_list) == 10, 'expect 10 tags'

class TestEnhance:
    def test_qna(self):
        answer = blogger.qna('Which country has the Taj Mahal?')
        assert 'india' in answer.lower(), 'expect "india" in completion for taj mahal location'
    
    def test_quote(self):
        response_quote = blogger.quote(post.get_topic())
        assert len(response_quote.split(" ")) > 7, 'expect more than 7 words in quote'

    def test_leaderboard(self):
        response, response_list = blogger.leaderboard(post.get_topic(), 'Famous People')
        assert len(response_list) == 10, 'expect 10 titles'
    
    def test_summarize(self):
        summary = blogger.summarize(post.get_topic(), words=20, grade=10)
        assert len(summary.split(" ")) > 10, 'expect >10 words'

class TestIllustrate:
    # # Comment for CI testing to save on DALL.E image generation API calls
    # def test_image_from_description(self):
    #    url = blogger.image_from_description('space ship flying away from blue sun in night sky with three moons')
    #    assert '.png' in url.lower() and url[0 : 4].lower() == 'http', 'expect png image returned as url'

    def test_strip_filename(self):
        stripped_filename = blogger.strip_filename('long file name with / and $ in the text which should be stripped')
        assert '/' not in stripped_filename and '$' not in stripped_filename, 'expect stripped file name'

    def test_save_image(self):
        url = 'https://upload.wikimedia.org/wikipedia/commons/1/10/Empire_State_Building_%28aerial_view%29.jpg'
        filename = 'empire state building'
        local_file = blogger.save_image(url, filename, ext='jpg')
        assert os.path.exists(local_file) == True, 'check if local file exists'
        os.remove(local_file)

# class TestPublish:
#     # Comment for CI testing to avoid local file generation and save on DALL.E calls 
#     def test_auto_generate(self):
#         local_image, local_html, local_md = blogger.auto_generate(post.get_keywords())
#         assert os.path.exists(local_image) == True and \
#             os.path.exists(local_html) == True and os.path.exists(local_md) == True, \
#                 'expect image, html, md files to be saved locally'
#         os.remove(local_image)
#         os.remove(local_html)
#         os.remove(local_md)

