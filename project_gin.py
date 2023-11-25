from research_teams.research_team import ResearchTeam
from enums.platform import Platform
from social_media_teams.team_twitter import TeamTwitter
from social_media_teams.team_instagram import TeamInstagram
from analytics_teams.instagram_analytics import InstagramAnalytics
from configs.app_config import AppConfig
from data_collection_teams.instagram_api_team.instagram_api_team import InstagramApiTeam
import random
import argparse
import os
import shutil
import logging
import datetime

config = AppConfig()

def collect_analytics(platforms: list):
    """
    Collects analytics data for the given platforms.
    """
    logging.info("Collecting analytics...")
    if "instagram" in platforms:
        print("Collecting Instagram data...")
        logging.info("Collecting Instagram data...")
        instagram = InstagramApiTeam()
        instagram.collect_data()
    
    if "twitter" in platforms:
        logging.info("Collecting Twitter data...")
        print("Twitter analytics")

    if "facebook" in platforms:
        logging.info("Collecting Facebook data...")
        print("Facebook analytics")


def main(theme: str, platforms: list, analytics: bool = False, clear_cache:bool = False) -> None:
    # ----------------------------------------
    #          Init Log
    # ----------------------------------------
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    logging.basicConfig(filename=f"./logs/log-{timestamp}.log", level=logging.INFO,
                        format='[%(asctime)s %(levelname)s] %(message)s',
                        datefmt='%Y-%d-%m %H:%M:%S', encoding="utf-8")

    # ----------------------------------------
    #          Clear Cache (if flag is set)
    # ----------------------------------------
    if clear_cache:
        if os.path.exists('.cache') and os.path.isdir('.cache'):
            print('Deleting previous work...')
            shutil.rmtree('.cache')

    # ----------------------------------------
    #          Collect Analytics only (if flag is set)
    # ----------------------------------------
    if analytics:
        collect_analytics(platforms)
        return
    

    # ----------------------------------------
    #          Set Theme (if not set)
    # ----------------------------------------
    themes = [
        "Gin recepie",
        "Gin fun fact",
        "Accurate information of product from Stookers Gin",
    ]

    theme = theme if theme is not None else random.choice(themes)

    # ----------------------------------------
    #          Twitter Flow
    # ----------------------------------------
    if "twitter" in platforms:
        print("Twitter flow")

        # Refine collected data
        research_team = ResearchTeam(theme=theme, platform=Platform.TWITTER)
        research_data = research_team.research_results()

        # Create social media content based on the collected data
        twitter_team = TeamTwitter(data=research_data)
        twitter_team.post_tweet(
            theme, with_image=config.twitter_with_image
        )

    # ----------------------------------------
    #          Instagram Flow
    # ----------------------------------------
    if "instagram" in platforms:
        print("Instagram flow")

        # Fun fact about gin
        if "fun" in platforms:
            print("Fun fact flow")
            research_team = ResearchTeam(theme=theme, platform=Platform.INSTAGRAM)
            research_data = research_team.research_results()

            instagram_team = TeamInstagram(data=research_data)
            instagram_team.publish_fun_content(theme=theme)

        # Publish content where we encourage user interaction (e.g. give two ingredients to a recipe)
        if "user" in platforms:
            print("User flow")
            """
            1. Get the post id from the latest user post
            2. Get the comments from the post
            3. Select one comment -> determine if right fromat 'a and b' or 'a & b'
            4. Create a post with that incorporates the comment
            5. Publish the post, with the text: 'This week's ingredients were from @username, if you want to create your own recipe, please blow in the form of 'a and b' or 'a & b. Recipe'
            6. Save the post ID to a file so we can use this id next time in this flow
            """
            instagram_team = TeamInstagram(data=None)
            instagram_team.publish_user_content()

        # Stookers marketing and product information with a real image
        if "marketing" in platforms:
            print("Marketing flow")
            instagram_team = TeamInstagram(data=research_data)
            instagram_team.publish_fun_content(theme=theme)


    # ----------------------------------------
    #          Shut Down Log
    # ----------------------------------------
    logging.info("Program finished.")
    logging.shutdown()

if __name__ == "__main__":
    # ----------------------------------------
    #          Define Program Arguments
    # ----------------------------------------
    parser = argparse.ArgumentParser(
        description="Team Stookers",
        exit_on_error=True,
    )

    parser.add_argument(
        "--clear-cache",
        "-c",
        action="store_true",
        help="Cleare the cache before running the application.",
    )

    parser.add_argument(
        "--analytics",
        "-a",
        action="store_true",
        help="Skip content creation and only collect analytics data.",
    )

    parser.add_argument(
        "--theme",
        "-t",
        type=str,
        help="The theme we want to use for the content generation.",
    )

    parser.add_argument(
        "platforms",
        type=str,
        # nargs="+",
        choices=["twitter", "instagram-analytics", "instagram-user", "instagram-marketing", "instagram-fun", "facebook"],
    )

    parser.add_argument(
        "--platforms",
        "-p",
        action="store_const",
        const="-p",
        help="Add all the platforms you want to generate content for separated by a space.",
    )

    args = parser.parse_args()
    print(args)
    main(args.theme, args.platforms, args.analytics, args.clear_cache)

else:
    raise ImportError(
        "This is the entry point of the application, must be run directly"
    )
