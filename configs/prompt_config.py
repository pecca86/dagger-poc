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

# INSTAGRAM RESEARCH TEAM
instagram_research_user = data['instagram']['research']['roles'][0]
instagram_research_agent = data['instagram']['research']['roles'][1]
instagram_research_critic = data['instagram']['research']['roles'][2]

# INSTAGRAM CONTENT TEAM
## ANALYTICS
instagram_analytics_user = data['instagram']['publish']['roles'][0]
instagram_analytics_agent = data['instagram']['publish']['roles'][1]

## PUBLISH
instagram_publisher_user = data['instagram']['publish']['roles'][2]
instagram_publisher_agent = data['instagram']['publish']['roles'][3]
instagram_publisher_critic = data['instagram']['publish']['roles'][4]

## IMAGE TEAM
instagram_image_user = data['instagram']['image']['roles'][0]
instagram_image_creator = data['instagram']['image']['roles'][1]


"""
T W I T T E R
"""