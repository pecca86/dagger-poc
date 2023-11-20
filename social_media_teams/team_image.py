import autogen
from openai import OpenAI
from social_media_teams.agents.image_agent import ImageAgent
from social_media_teams.agents.coder_agent import CoderAgent
from utils.file_utils import move_file_and_add_time_stamp
import logging
import os
import shutil
import time
from configs.app_config import AppConfig
from configs.prompt_config import *


# TODO: Add logging
logger = logging.getLogger(__name__)


class TeamImage:
    def __init__(self, prompt: str) -> None:
        self.prompt = prompt
        self.config = AppConfig()

    def create_image(
        self,
        save_folder: str,
    ) -> str:
        # Image / prompt agent
        image_agent_name = "image_agent"
        image_agent = ImageAgent(
            image_agent_name,
            instagram_image_creator["prompt"].replace("{image_agent_name}", image_agent_name).replace("{prompt}", self.prompt).replace("{banned_words}", "bottle"),
            self.config.autogen_config_list,
        )
        image_agent_agent = image_agent.retrieve_agent()

        # Dall-e agent
        def call_dalle(prompt) -> str:
            dall_e_client = OpenAI(
                api_key=self.config.openai_api_key,
            )

            response = dall_e_client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )

            image_url = response.data[0].url
            print(f"Image url: {image_url}")
            return image_url

        # Function agent
        function_agent = autogen.AssistantAgent(
            name="function_agent",
            system_message="You are a helpful assistant. Reply TERMINATE when the task is done.",
            llm_config={
                "timeout": 600,
                "seed": 42,
                "config_list": self.config.autogen_config_list,
                "model": "gpt-4",  # make sure the endpoint you use supports the model
                "temperature": 0,
                "functions": [
                    {
                        "name": "call_dalle",
                        "description": "always use the call_dalle function",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "prompt": {
                                    "type": "string",
                                    "description": "prompt: the prompt to use for generating the image",
                                },
                            },
                            "required": ["prompt"],
                        },
                    }
                ],
            },
        )

        # Coder agent
        coder_agent_name = "coder_agent"
        coder = CoderAgent(
            coder_agent_name,
            f"You are the {coder_agent_name}. Your task is to create a python script to download an image file from a URL given to you by the call_dalle. The file name must be 'image' Reply TERMINATE when the task is done.",
            self.config.autogen_config_list,
        )
        coder_agent = coder.retrieve_agent()

        # User proxy / coder
        user_proxy = autogen.UserProxyAgent(
            system_message="You are tasked with running the python script for retrieving an image from a url. Save the file locally to the specified directory. You are also responsible for calling the function call_dalle which will return the image url.",
            human_input_mode="TERMINATE",
            is_termination_msg=lambda x: x.get("content", "")
            and x.get("content", "").rstrip().endswith("TERMINATE"),
            max_consecutive_auto_reply=20,
            name="user_proxy",
            code_execution_config={"work_dir": "dall_e_img", "use_docker": False},
            function_map={"call_dalle": call_dalle},
        )

        group_chat = autogen.GroupChat(
            agents=[image_agent_agent, function_agent, coder_agent, user_proxy],
            messages=[],
            max_round=10,
        )

        manager = autogen.GroupChatManager(
            name="manager",
            groupchat=group_chat,
            llm_config={"config_list": self.config.autogen_config_list},
        )

        user_proxy.initiate_chat(
            manager,
            message=instagram_image_user["prompt"].replace("{image_agent_name}", image_agent_name),
            code_execution_config=False,
        )

        # Move the image to the twitter_images folder and give it an unique name
        unique_filename = move_file_and_add_time_stamp(
            target_folder_path=os.path.join(os.getcwd(), "dall_e_img"),
            target_file_name="image.png",
            destination_folder_path=os.path.join(os.getcwd(), save_folder),
        )
        return unique_filename
