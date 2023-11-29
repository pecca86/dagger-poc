from configs.app_config import AppConfig
from analytics_teams.instagram_analytics import InstagramAnalytics
from social_media_teams.agents.instagram_publisher_agent import InstagramPublisherAgent
from research_teams.agents.critic import Critic
from social_media_teams.team_image import TeamImage
from social_media_teams.agents.ingredient_agent import IngredientAgent
from social_media_teams.agents.marketing_agent import MarketingAgent
from social_media_teams.utils.instagram_publisher import InstagramPublisher
from data_collection_teams.instagram_api_team.instagram_api_team import InstagramApiTeam
from configs.prompt_config import *
from utils import file_utils
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
import autogen
import logging
from chromadb.utils import embedding_functions
import re
import random

logger = logging.getLogger(__name__)


class TeamInstagram:
    def __init__(self, data: str):
        self.data = data
        self.config = AppConfig()

    #=====================
    # USER FLOW
    #=====================
    def publish_user_content(self):
        logging.info("** PHASE: Instagram Team - User engagement **")
        # 1. Get post id from txt file
        media_id = file_utils.read_first_line("./analytics_data/ig_user_content.txt")
        # 2. Get comments from post
        instagram_api = InstagramApiTeam()
        comments = instagram_api.all_comments_from_media(media_id)

        # 3. Select one comment, determine if right format 'a and b' or 'a & b'
        valid_comment = None
        username = None
        for comment in comments:
            if re.search(r"\b(\w+)\s+(and|&)\s+(\w+)\b", comment["text"]):
                valid_comment = comment
                break
        if valid_comment is not None:
            idxs = re.search(r"\b(\w+)\s+(and|&)\s+(\w+)\b", valid_comment["text"])
            ingredients = valid_comment["text"][idxs.start() : idxs.end()]
            username = instagram_api.comment_info(valid_comment["id"])["from"]["username"]
            instagram_api.reply_to_comment(valid_comment["id"], f"Congrats @{username}! Your recipe will was picked and your ingredients will be featured in the next post, stay tuned!")
        else:
            ingredients = "default"

        print(valid_comment)
        # 4. Create a post with that incorporates the comment
        caption = self._create_caption(username, ingredients)

        # 5. Create image
        team_image = TeamImage(caption)
        filename = team_image.create_image("instagram_images")

        # 6. Publish the post, with the text: 'This week's ingredients were from @username, if you want to create your own recipe, please blow in the form of 'a and b' or 'a & b. Recipe'
        logging.info("Publishing post...")
        instagram_publisher = InstagramPublisher()
        response = instagram_publisher.publish(filename, caption)

        # 7. Save the post ID to a file so we can use this id next time in this flow
        logging.info("Published successfully! Saving post id...")
        file_utils.save_to_text_file("./analytics_data/ig_user_content.txt", response["id"], True)


    def _create_caption(self, username, ingredients: str) -> str:
        ingredient_agent_prompt = instagram_prompts["ingredient_agent"]["prompt"]
        ingredient_agent_name = instagram_prompts["ingredient_agent"]["name"]
        ingredient_agent = IngredientAgent(
            name=ingredient_agent_name,
            system_message=ingredient_agent_prompt,
            agent_config=self.config.autogen_config_list,
        )
        ingredient_agent_agent = ingredient_agent.retrieve_agent()

        ingredient_user = autogen.UserProxyAgent(
            name=instagram_prompts["ingredient_user"]["name"],
            human_input_mode="NEVER",
            max_consecutive_auto_reply=0,
            code_execution_config=False,
        )

        if ingredients != "default":
            ingredient_user.initiate_chat(
                ingredient_agent_agent,
                message=instagram_prompts["ingredient_user"]["prompt"].replace("{username}", username).replace("{ingredients}", ingredients)
            )

        else:
            random_ingredients = instagram_prompts["random_ingredients"]
            random_ingredient_1 = random.choice(random_ingredients)
            random_ingredient_2 = random.choice(random_ingredients)
            ingredient_user.initiate_chat(
                ingredient_agent_agent,
                message=instagram_prompts["ingredient_user_random"]["prompt"].replace("{random_ingredient_1}", random_ingredient_1).replace("{random_ingredient_2}", random_ingredient_2)
            )

        for v in ingredient_agent_agent._oai_messages.values():
            agent_caption = v[-1]["content"]

        # CHAT LOGS
        msg_dic = ingredient_agent_agent._oai_messages
        for k, v in msg_dic.items():
            for item in v:
                print(f"[{item['role']}]: {item['content']}\n")
                logging.info(f"[{item['role']}]: {item['content']}\n")
            break

        return agent_caption


    #=====================
    # MARKETING FLOW
    #=====================
    def publish_marketing_content(self, theme) -> None:
        logging.info("** PHASE: Instagram Team - Marketing **")

        marketing_agent_name = instagram_prompts["marketing_agent"]["name"]
        marketing_agent = MarketingAgent(
            marketing_agent_name,
            system_message=instagram_prompts["marketing_agent"]["prompt"],
            agent_config=self.config.autogen_config_list,
        )
        marketing_agent_agent = marketing_agent.retrieve_agent()

        user_proxy = autogen.UserProxyAgent(
            name="marketing_user",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=0,
            code_execution_config=False,
        )

        user_proxy.initiate_chat(
            marketing_agent_agent,
            message=instagram_prompts["marketing_user"]["prompt"],
        )

        random_number = random.randint(0, 9)
        image_url = f"https://cdn.shopify.com/s/files/1/0522/7357/8152/files/instagram{random_number}.jpg"

        caption = ""
        for v in user_proxy._oai_messages.values():
            caption = v[-1]["content"]
        instagram_publisher = InstagramPublisher()
        response = instagram_publisher.publish_with_url(image_url, caption)

        # LOGGING
        msg_dic = marketing_agent_agent._oai_messages
        for k, v in msg_dic.items():
            for item in v:
                print(f"[{item['role']}]: {item['content']}\n")
                logging.info(f"[{item['role']}]: {item['content']}\n")
            break


        logger.info(f"Published successfully! {response}")


    #=====================
    # FUN FACT FLOW
    #=====================
    def publish_fun_content(self, theme) -> None:
        logging.info("** PHASE: Instagram Team - Fun fact **")
        # ----------------------------------------
        #          C R E A T E  C O N T E N T  W I T H  A N A L Y T I C S
        # ----------------------------------------

        # ANALYTICS AGENT
        analytics_agent = autogen.AssistantAgent(
            name="analyst",
            system_message="You are a data analyst specialized in analyzing trends in instagram data, given to you by the raqproxy agent. You will reiterate according to feedback given by the critic.",
            llm_config= {
                "config_list": self.config.autogen_config_list,
                "temperature": 0,
            }
        )

        # RAG USER PROXY AGENT
        # Embedding function
        openai_ef = embedding_functions.OpenAIEmbeddingFunction(
            api_key=self.config.openai_api_key,
            model_name="text-embedding-ada-002",
        )

        ragproxyagent = RetrieveUserProxyAgent(
            name="ragproxyagent",
            system_message="You are the ragproxyagent. You will retrieve content for the analyst to analyze.",
            human_input_mode="NEVER",
            retrieve_config={
                "task": "qa",
                "docs_path": "./analytics_data/ig_top_10_data.csv",
                "embedding_function": openai_ef,
            },
        )

        # INSTAGRAM PUBLISHER AGENT
        publisher_name = instagram_prompts["publisher_agent"]["name"]
        publisher = InstagramPublisherAgent(
            publisher_name,
            # instagram_publisher_agent["prompt"]
            instagram_prompts["publisher_agent"]["prompt"]
            .replace("{instagram_publisher_name}", publisher_name)
            .replace("{theme}", theme),
            self.config.autogen_config_list,
        )
        publisher_agent = publisher.retrieve_agent()

        # CRITIC AGENT
        criteria_list = str(instagram_prompts["publisher_critic"]["criteria_list"])
        critic_name = instagram_prompts["publisher_critic"]["name"]
        critic = Critic(
            critic_name,
            instagram_prompts["publisher_critic"]["prompt"]
            .replace("{critic_name}", critic_name)
            .replace("{criteria_list}", criteria_list)
            .replace("{instagram_publisher_name}", publisher_name)
            .replace("{theme}", theme),
            self.config.autogen_config_list,
        )
        critic_agent = critic.retrieve_agent()

        # User
        user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=0,
            code_execution_config=False
        )

        group_chat = autogen.GroupChat(
            agents=[analytics_agent, publisher_agent, critic_agent, user_proxy],
            messages=[],
            max_round=10,
        )

        manager = autogen.GroupChatManager(
            name="manager",
            groupchat=group_chat,
            llm_config={"config_list": self.config.autogen_config_list},
        )

        # Start prompt
        ragproxyagent.initiate_chat(
            manager,
            problem=instagram_prompts["publisher_user"]["prompt"].replace(
                "{theme}", theme
            ),
        )

        # ----------------------------------------
        #          L O G S
        # ----------------------------------------
        msg_dic = user_proxy._oai_messages
        for k, v in msg_dic.items():
            for item in v:
                logging.info(f"[{item['name']}]: {item['content']}\n")
            break


        # ----------------------------------------
        #          I M A G E
        # ----------------------------------------
        instagram_caption = ""
        for v in user_proxy._oai_messages.values():
            instagram_caption = v[-2]["content"]

        team_image = TeamImage(instagram_caption)
        filename = team_image.create_image("instagram_images")

        # ----------------------------------------
        #          P U B L I S H
        # ----------------------------------------
        publisher = InstagramPublisher()
        publisher.publish(filename, instagram_caption)
