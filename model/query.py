from groq import Groq
import time

import sentiment
import filter

client = Groq(
    api_key=""
)

def query(client, system_prompt, prompt, max_tries=5):
    output = ""
    for retry in range(max_tries):
        try:
            completion = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": prompt
                    },
                ],
                temperature=0.39,
                max_tokens=1024,
                top_p=1,
                stream=False,
                stop=None,
                )
            output = completion.choices[0].message.content
            return output
        except Exception as e:
            print(f"An error occured : {e}")
            print(f"Retrying {retry} time(s) ...")
            print("waiting 60 seconds ...")
            time.sleep(60)

def call_sentiment_api(comment:str, context:list[str]):
    prompt = sentiment.build_prompt(comment, context)
    system_prompt = sentiment.build_system_prompt()
    response:str = query(client, system_prompt=system_prompt, prompt=prompt)
    return response.strip()

def call_filter_api(title:str, body:str):
    prompt = filter.build_prompt(title, body)
    system_prompt = filter.build_system_prompt()
    response:str = query(client, system_prompt=system_prompt, prompt=prompt)
    return response.strip().lower()

# if __name__ == '__main__':
#     var = call_filter_api(title="Roadside Tesla Semi fire where temperatures reached 1,000 degrees draws in NTSB investigative team",
#                           body="A crash and large fire along a California freeway involving an electric Tesla Semi has drawn the attention of federal safety investigators.\n\nThe U.S. National Transportation Safety Board said Thursday it\u2019s sending a team of investigators from the Office of Highway Safety mainly to look into fire risks posed by lithium-ion batteries.\n\nThe team will work with the California Highway Patrol to \u201cexamine the wreckage and gather details about the events leading up to the collision and the subsequent fire response,\u201d the agency said in a statement.\n\nThe Los Angeles Times reported that the Tesla rig was traveling east on Interstate 80 around 3:15 a.m. Monday near Emigrant Gap, about 70 miles (113 kilometers) northeast of Sacramento, when it went off the road and collided with trees near the right shoulder.\n\nThe battery caught fire, spewing toxic fumes and reaching a temperature of 1,000 degrees, forcing firefighters to wait for it to burn out, the Highway Patrol told the newspaper. The Tesla driver walked away from the crash and was taken to a hospital, and the freeway was temporarily closed.\n\nThe battery burned into the late afternoon while firefighters tried to cool it down for cleanup, and the freeway didn\u2019t reopen until 7:20 p.m., authorities said.\n\nA message was left Thursday seeking comment on the crash and fire from Tesla.\n\nAfter an investigation that ended in 2021 the NTSB determined that high-voltage electric vehicle battery fires pose risks to first responders and that guidelines from manufacturers about how to deal with them were inadequate.\n\nThe agency, which has no enforcement powers and can only make recommendations, called for manufacturers to write vehicle-specific response guides for fighting battery fires and limiting chemical thermal runaway and reignition. The guidelines also should include information on how to safely store vehicles with damaged lithium-ion batteries, the agency said.\n\nTesla began delivering the electric Semis in December of 2022, more than three years after CEO Elon Musk said his company would start making the trucks. Musk has said the Semi has a range per charge of 500 miles (800 kilometers) when pulling an 82,000-pound (37,000-kilo) load.\n\nSource: https://www.cnbc.com/2024/08/22/roadside-tesla-semi-fire-where-temperatures-reached-1000-degrees-draws-in-ntsb-investigative-team.html")
#     print(var.__class__)