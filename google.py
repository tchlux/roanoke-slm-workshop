# This file provides a function to easily query google.

import os
GOOGLE_SEARCH_API_ENGINE_AND_KEY_LOCATION = os.path.expanduser("~/.google_api_key")
# ^^ This file should look likle the following:
# 
# ------------- FILE START --------------
# 000a00000a000000a
# AAa0aAaA0aaA0a-AaAa0aa0AAA0-aaAAAa0aAa0
# -------------- FILE END ---------------
# 
# 
# You can get a search engine ID (first line) and Google Search API key from
#   https://developers.google.com/custom-search/v1/overview#prerequisites
# 
# 
with open(GOOGLE_SEARCH_API_ENGINE_AND_KEY_LOCATION) as f:
    GOOGLE_SEARCH_ENGINE_ID, GOOGLE_SEARCH_API_KEY = f.read().strip().split("\n")


from functools import lru_cache  # For caching repeated calls to reduce unnecessary internet usage.


# Given a string, search for it on Google and return the result as a dictionary.
# If an image search is desired instead of a text search, pass "images=True".
# 
@lru_cache
def search(query, images=False, n=5, start=1, **params):
    num_results = n  # Rename for local readability.
    assert (num_results <= 100), f"At most 100 results can be returned by a search with the Google API."
    # Libraries needed to execute the search.
    import urllib.request
    import urllib.parse
    import json
    # Define the parameters
    params = {
        # Refernece example:
        #   https://developers.google.com/custom-search/v1/reference/rest/v1/cse/list?apix=true&apix_params=%7B%22c2coff%22%3A%221%22%2C%22cx%22%3A%228591e881e3108483e%22%2C%22hl%22%3A%22en%22%2C%22num%22%3A5%2C%22q%22%3A%22how%20many%20apples%20are%20in%20the%20world%3F%22%7D
        #   https://developers.google.com/custom-search/v1/reference/rest/v1/cse/list?apix_params=%7B%22c2coff%22%3A%221%22%2C%22cx%22%3A%228591e881e3108483e%22%2C%22hl%22%3A%22en%22%2C%22num%22%3A3%2C%22q%22%3A%22how%20many%20apples%20are%20in%20the%20world%3F%22%7D
        # 
        "q": query, # The search query
        "start": str(start), # The starting index for the resturned items.
        "num": str(min(10,num_results)), # Number of results to return (up to 10, use "start=11" to get the next 10 up to 100).
        "hl": "en", # English results.
        "c2coff": "1", # Disables simplified traditional chinese search
        "lr": "lang_en", # Restricts results to documents written in a particular language
        # 
        # "exactTerms": "", # Terms that *must* be included
        # "excludeTerms": "", # Word or phrase that should *not* appear
        # "orTerms": "", # Words that at least *one* of these must appear in the document
        # 
        "cx": GOOGLE_SEARCH_ENGINE_ID, # Google custom search engine identifier
        "key": GOOGLE_SEARCH_API_KEY, # Google Search API key
    }
    # Special keyword insertion for image searches to make it mores usable.
    if (images):
        params["searchType"] = "image" # Use this to get image results.
    # Add in any custom parameters.
    params.update(params)
    # Encode the parameters
    encoded_params = urllib.parse.urlencode(params)
    # Construct the URL
    url = f"https://customsearch.googleapis.com/customsearch/v1?{encoded_params}"
    # Make the request
    request = urllib.request.Request(url, headers={'Accept': 'application/json'})
    # Handle the response.
    with urllib.request.urlopen(request) as response:
        # When the response is successful, parse the JSON and return it.
        if response.status == 200:
            response_body = response.read()
            parsed_response = json.loads(response_body.decode('utf-8'))
            search_results = parsed_response["items"]
            # If more results are needed, recursively call this function.
            if (num_results > 10):
                search_results += search(
                    query,
                    images=images,
                    n=num_results-10,
                    start=start+10,
                    **params
                )
            # Return the sum of all items.
            return search_results
        # When the response is unsuccessful, provide the status as a result.
        else:
            return [dict(error=response.status)]


# Function to turn an nested object (dict, list) into a nicely formatted string.
def to_str(o, indent=2, gap=0):
    if (type(o) is dict):
        string = " "*gap + "{"
        for k,v in o.items():
            string += "\n" + " "*(gap+indent) + f"'{k}': " + to_str(v, indent=indent, gap=gap+indent).lstrip(" ")
        string += "\n" + " "*gap + "}"
    elif (type(o) is list):
        string = " "*gap + "["
        for v in o:
            string += "\n" + to_str(v, indent=indent, gap=gap+indent)
        string += "\n" + " "*gap + "]"
    else:
        string = " "*gap + repr(o)
    return string



if __name__ == "__main__":
    # 
    # Demo simple google search:
    # 
    result = search_google("How many apples are there in the world?")
    for item in result:
        print()
        print(to_str(item))

    # Output will look like this:
    # 
    # 
    # {
    #   'kind': 'customsearch#result'
    #   'title': 'How many apples are there in the world at any one time? : r/estimation'
    #   'htmlTitle': '<b>How many apples are there in the world</b> at any one time? : r/estimation'
    #   'link': 'https://www.reddit.com/r/estimation/comments/a69m38/how_many_apples_are_there_in_the_world_at_any_one/'
    #   'displayLink': 'www.reddit.com'
    #   'snippet': 'Dec 14, 2018 ... Rotting and non rotting apples can be counted.'
    #   'htmlSnippet': 'Dec 14, 2018 <b>...</b> Rotting and non rotting <b>apples</b> can be counted.'
    #   'cacheId': 'g2lkjsdlEJ'
    #   'formattedUrl': 'https://www.reddit.com/.../how_many_apples_are_there_in_the_world_at_...'
    #   'htmlFormattedUrl': 'https://www.reddit.com/.../<b>how_many</b>_<b>apples_are_there_in_the_world</b>_at_...'
    #   'pagemap': {
    #     'cse_thumbnail': [
    #       {
    #         'src': 'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcQ1NXYBDSq4zgQm-Ko9EYuqO9SxhfATacEtjHepyv7F6w'
    #         'width': '225'
    #         'height': '225'
    #       }
    #     ]
    #     'metatags': [
    #       {
    #         'og:image': 'https://share.redd.it/preview/post/a69m38'
    #         'theme-color': '#000000'
    #         'og:image:width': '1200'
    #         'og:type': 'website'
    #         'og:image:alt': 'An image containing a preview of the post'
    #         'twitter:card': 'summary_large_image'
    #         'twitter:title': 'r/estimation on Reddit: How many apples are there in the world at any one time?'
    #         'og:site_name': 'Reddit'
    #         'og:title': 'r/estimation on Reddit: How many apples are there in the world at any one time?'
    #         'og:image:height': '630'
    #         'msapplication-navbutton-color': '#000000'
    #         'og:description': 'Posted by u/barefoot_vagrant - 16 votes and 4 comments'
    #         'twitter:image': 'https://share.redd.it/preview/post/a69m38'
    #         'apple-mobile-web-app-status-bar-style': 'black'
    #         'twitter:site': '@reddit'
    #         'viewport': 'width=device-width, initial-scale=1, viewport-fit=cover'
    #         'apple-mobile-web-app-capable': 'yes'
    #         'og:ttl': '600'
    #         'og:url': 'https://www.reddit.com/r/estimation/comments/a69m38/how_many_apples_are_there_in_the_world_at_any_one/'
    #       }
    #     ]
    #     'cse_image': [
    #       {
    #       }
    #     ]
    #   }
    # }
    # 
    # {
    #   'kind': 'customsearch#result'
    #   'title': 'Blog | How Many Types Of Apples Are There | Select Health'
    #   'htmlTitle': 'Blog | <b>How Many</b> Types Of <b>Apples Are There</b> | Select Health'
    #   'link': 'https://selecthealth.org/blog/2020/02/how-many-types-of-apples-are-there-and-which-is-best'
    #   'displayLink': 'selecthealth.org'
    #   'snippet': "You're not going to see this many kinds of apples in the grocery store, but there are 7,500 varieties of apples in existence throughout the world—2,500 of which\xa0..."
    #   'htmlSnippet': 'You&#39;re not going to see this <b>many</b> kinds of <b>apples</b> in the grocery store, but <b>there</b> are 7,500 varieties of <b>apples</b> in existence throughout the <b>world</b>—2,500 of which&nbsp;...'
    #   'cacheId': 'Olkd_o01klkjd'
    #   'formattedUrl': 'https://selecthealth.org/.../how-many-types-of-apples-are-there-and-which-i...'
    #   'htmlFormattedUrl': 'https://selecthealth.org/.../<b>how-many</b>-types-of-<b>apples-are-there</b>-and-which-i...'
    #   'pagemap': {
    #     'cse_thumbnail': [
    #       {
    #         'src': 'https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcQn1Oux7Ys1Dbcr-qHs9dbN8dm6ULUSMKajun23yjJagM_EWqDuv3Sjhis'
    #         'width': '275'
    #         'height': '183'
    #       }
    #     ]
    #     'metatags': [
    #       {
    #         'p:domain_verify': '166486484bbefd308aa8005a543b52b8'
    #         'referrer': 'no-referrer-when-downgrade'
    #         'og:image': 'selecthealth.org/-/media/selecthealth/blogs/post/2022/08/apple_types_fb_sm.jpg?h=630&iar=0&w=1200&hash=B433544ECC616AA86170969898021540'
    #         'twitter:card': 'summary'
    #         'og:type': 'website'
    #         'og:site_name': 'SelectHealth.org'
    #         'viewport': 'width=device-width, initial-scale=1.0'
    #         'og:title': 'Blog | How Many Types Of Apples Are There | Select Health'
    #         'og:description': 'Here’s a quick rundown on America’s favorite fruit. We’ll answer how many types of apples there are, look at a few new types of apples, and decipher which one is best.'
    #       }
    #     ]
    #     'cse_image': [
    #       {
    #         'src': 'https://selecthealth.org/blog/2020/02/selecthealth.org/-/media/selecthealth/blogs/post/2022/08/apple_types_blog_lg.jpg'
    #       }
    #     ]
    #   }
    # }
    # 
    # ...
