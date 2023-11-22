import json

# Specify the path to the JSON file
file_path = "./configs/prompts.json"

# Open the file in read mode
with open(file_path, "r") as file:
    # Load the JSON data
    data = json.load(file)

"""
I N S T A G R A M
"""
instagram_prompts = {
    # INSTAGRAM RESEARCH TEAM
    "research_user": data['instagram']['research']['roles'][0],
    "research_agent": data['instagram']['research']['roles'][1],
    "research_critic": data['instagram']['research']['roles'][2],

    # INSTAGRAM CONTENT TEAM
    ## ANALYTICS
    "analytics_user": data['instagram']['publish']['roles'][0],
    "analytics_agent": data['instagram']['publish']['roles'][1],

    ## PUBLISH
    "publisher_user": data['instagram']['publish']['roles'][2],
    "publisher_agent": data['instagram']['publish']['roles'][3],
    "publisher_critic": data['instagram']['publish']['roles'][4],

    ## IMAGE TEAM
    "image_user": data['instagram']['image']['roles'][0],
    "image_creator": data['instagram']['image']['roles'][1],
}

"""
T W I T T E R
"""
twitter_prompts = {
    # INSTAGRAM RESEARCH TEAM
    "research_user": data['twitter']['research']['roles'][0],
    "research_agent": data['twitter']['research']['roles'][1],
    "research_critic": data['twitter']['research']['roles'][2],

    # INSTAGRAM CONTENT TEAM
    ## ANALYTICS
    "analytics_user": data['twitter']['tweet']['roles'][0],
    "analytics_agent": data['twitter']['tweet']['roles'][1],

    ## PUBLISH
    "tweet_user": data['twitter']['tweet']['roles'][2],
    "tweet_agent": data['twitter']['tweet']['roles'][3],
    "tweet_critic": data['twitter']['tweet']['roles'][4],

    ## IMAGE TEAM
    "image_user": data['twitter']['image']['roles'][0],
    "image_creator": data['twitter']['image']['roles'][1],
}
