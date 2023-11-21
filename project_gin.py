from research_teams.research_team import ResearchTeam
from enums.platform import Platform
from social_media_teams.team_twitter import TeamTwitter
from social_media_teams.team_instagram import TeamInstagram
from analytics_teams.instagram_analytics import InstagramAnalytics
from configs.app_config import AppConfig
import random
import argparse
import os
import shutil
import logging
import datetime

config = AppConfig()

def collect_analytics(platforms: list):
    """
    COLLECT ANALYTICS DATA
    """
    logging.info("Collecting analytics...")
    if "instagram" in platforms:
        instagram_analytics = InstagramAnalytics()
        instagram_analytics.collect_data()
    
    if "twitter" in platforms:
        print("Twitter analytics")

    if "facebook" in platforms:
        print("Facebook analytics")


def main(theme: str, platforms: list, analytics: bool = False, clear_cache:bool = False) -> None:

    # ----------------------------------------
    #          Init Log
    # ----------------------------------------
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    logging.basicConfig(filename=f"./logs/log-{timestamp}.log", level=logging.INFO,
                        format='[%(asctime)s %(levelname)s] %(message)s',
                        datefmt='%Y-%d-%m %H:%M:%S', encoding="utf-8")





    if clear_cache:
        if os.path.exists('.cache') and os.path.isdir('.cache'):
            print('Deleting previous work...')
            shutil.rmtree('.cache')

    # If analytics is True, only collect analytics data
    if analytics:
        collect_analytics(platforms)
        return
    
    themes = [
        "Gin recepie",
        "Gin fun fact",
        "Accurate information of product from Stookers Gin",
    ]

    theme = theme if theme is not None else random.choice(themes)

    print("The theme is: ", theme)

    """
    TWITTER FLOW
    """
    if "twitter" in platforms:
        print("Twitter flow")

        # Refine collected data
        research_team = ResearchTeam(theme=theme, platform=Platform.TWITTER)
        research_data = research_team.research_results()

        # Create social media content based on the collected data
        twitter_team = TeamTwitter(data=research_data)
        twitter_team.post_tweet(
            theme, with_image=config.twitter_with_image
        )  # TODO: add a way to present a random theme

    """
    INSTAGRAM FLOW
    """
    if "instagram" in platforms:
        print("Instagram flow")

        research_team = ResearchTeam(theme=theme, platform=Platform.INSTAGRAM)
        research_data = research_team.research_results()

        instagram_team = TeamInstagram(data=research_data)
        instagram_team.publish_content(theme=theme)

    # Collect analytics data
    collect_analytics(['instagram', 'twitter', 'facebook'])
    logging.info("Program finished.")
    logging.shutdown()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Team Stookers",
        exit_on_error=True,
    )

    parser.add_argument(
        "--clear-cache",
        "-c",
        type=bool,
        help="Cleare the cache before running the application.",
    )

    parser.add_argument(
        "--analytics",
        "-a",
        type=bool,
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
        nargs="+",
        choices=["twitter", "instagram", "facebook"],
        help="Choose the platforms you want to generate content for.",
    )

    parser.add_argument(
        "--platforms",
        "-p",
        action="store_const",
        const="-p",
        help="Add all the platforms you want to generate content for.",
    )

    args = parser.parse_args()
    print(args)
    main(args.theme, args.platforms, args.analytics, args.clear_cache)

else:
    raise ImportError(
        "This is the entry point of the application, must be run directly"
    )
