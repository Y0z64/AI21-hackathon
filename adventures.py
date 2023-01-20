import gradio as gr
import requests
from prompt_generator import generate_prompt
import argparse


#presets for the prompt
fantasy_preset = "You are an adventurer from a medieval fantasy world like The Hobit. At the start of each adventure you will wake up with no memory of who you are and then explore your surroundings. Every time you analyze your surroundings you will and say in a dramatic and lyrical tone what you see and the consequences of your previous action. After each analysis you make, you will be able to make 3 actions related to your environment.\nSelected action:\nHistory: You wake up in the middle of a field filled with tall green grass and surrounded by mountains.\nActions: Observe your surroundings\n##\nSelected action: Observe your surroundings\nHistory: You find yourself in the middle of a field. The field is surrounded by a dense and tall forest. In the middle of the field there is an abandoned village filled with ruins of destroyed buildings.\nActions: Go to village - Go to forest\n##\nSelected action: Go to forest\nHistory: You approach the dark forest that surrounds the tall grass field. The forest is dense and dark, there is a creepy silence in the ambient\nActions: Explore further - Go to grass field\n##\nSelected action: Explore further\nHistory: You explore deeper into the forest. As you do you find the entrance of a deep cave in the dark forest.\nActions: Explore further - Enter cave\n##\nSelected action: Enter cave\nHistory: You enter the cave, inside you find a deep cavern filled with bio-luminescent insects that shine in neon colors and illuminate the cavern.\nActions: Explore further - Exit cave\n##\nSelected action: Explore further\nHistory: You continue to explore the cave, inside you find a cavern filled with stalactites that hang from the ceiling and beautiful rock formations.\nActions: Explore further - Exit cave\n##\nSelected action:\nHistory:"

#preset of start of adventure
start_1 = "You find yourself in the middle of a forest. The forest is dense and filled with strange flowers and animals of exotic colors."

#Adventure save
save = []

#Start adventure
def start_chat(preset, start, key):
    default_prompt = f"{preset}{start}"
    request = requests.post("https://api.ai21.com/studio/v1/j1-jumbo/complete",
            headers={"Authorization": f"Bearer {key}"},
            json={
                "prompt": default_prompt,
                "numResults": 1,
                "maxTokens": 200,
                "temperature": 1,
                "topKReturn": 0,
                "topP":1,
                "countPenalty": {
                    "scale": 0,
                    "applyToNumbers": False,
                    "applyToPunctuations": False,
                    "applyToStopwords": False,
                    "applyToWhitespaces": False,
                    "applyToEmojis": False
                },
                "frequencyPenalty": {
                    "scale": 0,
                    "applyToNumbers": False,
                    "applyToPunctuations": False,
                    "applyToStopwords": False,
                    "applyToWhitespaces": False,
                    "applyToEmojis": False
                },
                "presencePenalty": {
                    "scale": 0,
                    "applyToNumbers": False,
                    "applyToPunctuations": False,
                    "applyToStopwords": False,
                    "applyToWhitespaces": False,
                    "applyToEmojis": False
            },
            "stopSequences":["##"]
            }
        )
    
    #generation of the prompt
    actions = request.json()["completions"][0]["data"]["text"]

    return actions, default_prompt


def chatbot_requests(input_prompt, actions, default_prompt, Temperature, key, history=[]):
    #generate the prompt
    prompt = f"{default_prompt}{actions}\n##\nSelected action:{''.join(save)}{input_prompt}\nHistory:"

    ##make the request with the generated prompt
    request = requests.post("https://api.ai21.com/studio/v1/j1-jumbo/complete",
            headers={"Authorization": f"Bearer {key}"},
            json={
                "prompt": prompt,
                "numResults": 1,
                "maxTokens": 150,
                "temperature": Temperature,
                "topKReturn": 0,
                "topP":1,
                "countPenalty": {
                    "scale": 0,
                    "applyToNumbers": False,
                    "applyToPunctuations": False,
                    "applyToStopwords": False,
                    "applyToWhitespaces": False,
                    "applyToEmojis": False
                },
                "frequencyPenalty": {
                    "scale": 0,
                    "applyToNumbers": False,
                    "applyToPunctuations": False,
                    "applyToStopwords": False,
                    "applyToWhitespaces": False,
                    "applyToEmojis": False
                },
                "presencePenalty": {
                    "scale": 0,
                    "applyToNumbers": False,
                    "applyToPunctuations": False,
                    "applyToStopwords": False,
                    "applyToWhitespaces": False,
                    "applyToEmojis": False
            },
            "stopSequences":["##"]
            }
        )
    
    #get the generation
    completion = request.json()["completions"][0]["data"]["text"]

    #separate from the message and the actions
    message, actions = completion.split("Actions:")
    message = message.replace("Selected action:", "")

    #update the prompt
    follow_up = f"{completion}\n##\nSelected action:"
    save.append(follow_up)

    #update hystory
    history.append((input_prompt, message))
    
    #return actions, history, history
    return history, history, actions, message


#--------------------------------------------------------------main
#start the adventure
if __name__ == "__main__":
  api_key = input("Input your API key: ")
  something, something2 = start_chat(fantasy_preset, start_1, api_key)

  demo = gr.Interface(fn=display_chatbot,
          inputs=["text", gr.Slider(0, 1), "state"],
          outputs=["chatbot", "state", "text"])

  demo.launch()
