import json

######################
# INSTAGRAM FUN FACT
######################

instagram_fun_fact_path = "./configs/instagram_fun_fact.json"
instagram_fun_fact_data = None
with open(instagram_fun_fact_path, "r") as file:
    instagram_fun_fact_data = json.load(file)

######################
# INSTAGRAM USER
######################

instagram_user_file_path = "./configs/instagram_user.json"
with open(instagram_user_file_path, "r") as file:
    instagram_user_data = json.load(file)

######################
# INSTAGRAM MARKETING
######################

instagram_user_file_path = "./configs/instagram_marketing.json"
with open(instagram_user_file_path, "r") as file:
    instagram_marketing_data = json.load(file)

######################
# TWITTER FUN FACT
######################
twitter_fun_fact_file_path = "./configs/twitter_fun_facts.json"
with open(twitter_fun_fact_file_path, "r") as file:
    twitter_fun_fact_data = json.load(file)

######################
# TWITTER MARKETING
######################
twitter_marketing_file_path = "./configs/twitter_marketing.json"
with open(twitter_marketing_file_path, "r") as file:
    twitter_marketing_data = json.load(file)


instagram_prompts = {
    #=====================
    # FUN FACT
    #=====================
    # INSTAGRAM RESEARCH TEAM
    "research_user": instagram_fun_fact_data['instagram_fun_fact']['research']['roles'][0],
    "research_agent": instagram_fun_fact_data['instagram_fun_fact']['research']['roles'][1],
    "research_critic": instagram_fun_fact_data['instagram_fun_fact']['research']['roles'][2],

    # INSTAGRAM CONTENT TEAM
    ## ANALYTICS
    "analytics_user": instagram_fun_fact_data['instagram_fun_fact']['publish']['roles'][0],
    "analytics_agent": instagram_fun_fact_data['instagram_fun_fact']['publish']['roles'][1],

    ## PUBLISH
    "publisher_user": instagram_fun_fact_data['instagram_fun_fact']['publish']['roles'][2],
    "publisher_agent": instagram_fun_fact_data['instagram_fun_fact']['publish']['roles'][3],
    "publisher_critic": instagram_fun_fact_data['instagram_fun_fact']['publish']['roles'][4],

    ## IMAGE TEAM
    "image_user": instagram_fun_fact_data['instagram_fun_fact']['image']['roles'][0],
    "image_creator": instagram_fun_fact_data['instagram_fun_fact']['image']['roles'][1],

    #=====================
    # USER
    #=====================
    "ingredient_agent": instagram_user_data['ingredient_agent'],
    "ingredient_user": instagram_user_data['ingredient_user'],
    "ingredient_user_random": instagram_user_data['ingredient_user_random'],
    "random_ingredients": instagram_user_data['random_ingredients'],

    #=====================
    # MARKETING
    #=====================
    "marketing_agent": instagram_marketing_data['marketing_agent'],
    "marketing_user": instagram_marketing_data['marketing_user'],
}

"""
T W I T T E R
"""
twitter_prompts = {
    #=====================
    # FUN FACT
    #=====================
    # INSTAGRAM RESEARCH TEAM
    "research_user": twitter_fun_fact_data['twitter_fun_facts']['research']['roles'][0],
    "research_agent": twitter_fun_fact_data['twitter_fun_facts']['research']['roles'][1],
    "research_critic": twitter_fun_fact_data['twitter_fun_facts']['research']['roles'][2],

    # INSTAGRAM CONTENT TEAM
    ## ANALYTICS
    "analytics_user": twitter_fun_fact_data['twitter_fun_facts']['tweet']['roles'][0],
    "analytics_agent": twitter_fun_fact_data['twitter_fun_facts']['tweet']['roles'][1],

    ## PUBLISH
    "tweet_user": twitter_fun_fact_data['twitter_fun_facts']['tweet']['roles'][2],
    "tweet_agent": twitter_fun_fact_data['twitter_fun_facts']['tweet']['roles'][3],
    "tweet_critic": twitter_fun_fact_data['twitter_fun_facts']['tweet']['roles'][4],

    ## IMAGE TEAM
    "image_user": twitter_fun_fact_data['twitter_fun_facts']['image']['roles'][0],
    "image_creator": twitter_fun_fact_data['twitter_fun_facts']['image']['roles'][1],

    #=====================
    # MARKETING
    #=====================
    "marketing_agent": twitter_marketing_data['marketing_agent'],
    "marketing_user": twitter_marketing_data['marketing_user'],
}
