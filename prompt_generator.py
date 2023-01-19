import requests

#presets for the prompt
presets = """ studio ghibli, fantasy elegant, highly detailed, digital painting, art station, concept art, smooth, sharp focus, wide angle, art book, wallpaper, splash art, cinematic lighting"""

#structure the prompt
def format_prompt(prompt, presets):
    filter = ["\n", "##", "Summarized:"]
    prompt = ''.join([i for i in prompt if not i in filter])
    return f"{prompt},{presets}"

#make a request to summarize propmt
def generate_prompt(prompt, key):
    x = requests.post("https://api.ai21.com/studio/v1/j1-jumbo/complete",
        headers={"Authorization": f"Bearer {key}"},
        json={
            "prompt": f"Summarize the following setting description:\nYou are in an abandoned village filled with ruins and debris, the air is filled with an smell of ash and burnt wood. The barriers of the village have collapsed a long time ago and there is abandoned skeletons on the streets.\n\nSummarized:\nAbandoned village in ruins\n\n##\nSummarize the following setting description:\nYou find yourself in the middle of a green field surrounded by mountains and forest.\n\nSummarized:\nGreen field with mountains\n\n##\nSummarize the following setting description:\nYou are in the interior of a castle, the walls are adorned with golden ornaments and at the end of the hall there is golden throne.\n\nSummarized:\nGolden castle hall with a golden throne\n\n##\nSummarize the following setting description:\nYou find yourself in the middle of a dark cavern, the only source of light is your torch and the reflection in the eyes of the bats that hang from the roof\n\nSummarized:\nCavern with bats hanging from the roof\n\n##\nSummarize the following setting description:\nYou find yourself entering a small village, the light of the flickering flames from the torches that hang above the street illuminates the cobble stoned alleys of the village.\n\nSummarized:\nVillage with torches hanging above the streets\n\n##\nSummarize the following setting description:\n{prompt}\n\nSummarized:\n",
            "numResults": 1,
            "maxTokens": 200,
            "temperature": 1,
            "topKReturn": 0,
            "topP":0.98,
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

    #get response in correct format
    response = x.json()["completions"][0]["data"]["text"]

    #format propmt correctly
    procceced_propmt = format_prompt(response, presets)

    #return formated propmt
    return procceced_propmt


#testing
if __name__ == "__main__":
    prompt = input("Prompt: ")
    key = "WJRgTozs6f0dHPwy4At4j69JYZEZedWY"
    procceced_prompt = generate_prompt(prompt, key)
    print(procceced_prompt)