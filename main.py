import requests, discord, os
from zeep.helpers import serialize_object
from dotenv import load_dotenv
import pandas as pd
load_dotenv(dotenv_path='.env')
intents = discord.Intents.default()
intents.message_content = True
client = discord.Bot(intents=intents)
token = os.getenv('TOKEN')
@client.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    try:
        channel = str(message.channel.name)
    except:
        channel = ''
    user_message = message.content
    format_the_request = str(user_message).lower()
    if message.author == client.user:
            return
    if message.guild is None:
        ###Spell functionality is good. Provides the user with quick reference to all needed spell info.
        input=format_the_request
        if 'spell:' in input:
            try:
                input = format_the_request.replace('spell: ', '').replace(' ', '-')
                print(input)
                spells_request = requests.get(f'https://www.dnd5eapi.co/api/spells/{input}')
                print(str(spells_request))
                json_to_text = spells_request.json()
                data = pd.DataFrame(pd.json_normalize(json_to_text))
                joined_desc = ''
                joined_desc.join(data['desc'][0:].astype(str))
                print(joined_desc)
                if 'material' in data.columns:
                    show_to_player = (f'{data["name"][0]}'
                                        f'\nDescription: '
                                        f'\n{(data["desc"][0])}'
                                        f'\nRange: {data["range"][0]}'
                                        f'\nComponents: {data["components"][0]}'
                                        f'\nMaterials: {data["material"][0]}'
                                        f'\nDuration: {data["duration"][0]}'
                                        f'\nConcentration: {data["concentration"][0]}'
                                        f'\nRitual: {data["ritual"][0]}'
                                        f'\n{data["casting_time"][0]}')
                else:
                    show_to_player = (f'{data["name"][0]}'
                                        f'\nDescription: '
                                        f'\n{data["desc"][0]}'
                                        f'\nRange: {data["range"][0]}'
                                        f'\nComponents: {data["components"][0]}'
                                        f'\nDuration: {data["duration"][0]}'
                                        f'\nConcentration: {data["concentration"][0]}'
                                        f'\nRitual: {data["ritual"][0]}'
                                        f'\n{data["casting_time"][0]}')
                print(show_to_player)
                await message.channel.send(f'Here you, go {username}!')
                if len(show_to_player) >= 2000 and len(show_to_player) < 4000:
                    await message.channel.send(show_to_player[0:len(show_to_player)//2])
                    await message.channel.send(show_to_player[len(show_to_player)//2 if len(show_to_player)%2==0 else ((len(show_to_player)//2)+1):])
                elif len(show_to_player) < 2000:
                    await message.channel.send(show_to_player)
                else:
                    await message.channel.send("Wow thats a big spell! Discord can't fit all of that.")
                return
            except:
                await message.channel.send("Hmmm. I couldn't find that spell. Are you sure its spelled right?")
        ###Class functionality needs: exploded lists for the double nested columns. Also, write out what the 'quick reference' info here would even be.
        if 'class' in input:
            # try:
            #     input=str(format_the_request).replace('class: ', '')
            #     #print(input)
            #     class_request = requests.get(f'https://www.dnd5eapi.co/api/classes/{input}')
            #     print(input)
            #     json_to_text = class_request.json()
            #     data = pd.json_normalize(json_to_text, max_level=2)
            #     df = pd.DataFrame(data)
            #     print(df.columns)
            #     if 'spells' in data.columns:
            #         show_to_player = (f'{data["name"][0]}'
            #                             f'\nHit Dice: 1d{data["hit_die"][0]} per level'
            #                             f'\nProficiency Choices: {data["proficiency_choices"][0]}'
            #                             f'\nProficiencies: {data["proficiencies"][0]}'
            #                             f'\nSaving Throws: {data["saving_throws"][0]}'
            #                             f'\nClass Levels: {data["class_levels"][0]}'
            #                             f'\nSubclasses: {data["subclasses"][0]}'
            #                             f'\nSpells: {data["spells"][0]}')
            #     else:
            #         show_to_player = (f'{data["name"]}'
            #                             f'\n{data["hit_die"]}'
            #                             f'\nProficiency Choices: {data["proficiency_choices"]}'
            #                             f'\nProficiencies: {data["proficiencies"]}'
            #                             f'\nSaving Throws: {data["saving_throws"]}'
            #                             f'\nClass Levels: {data["class_levels"]}'
            #                             f'\nSubclasses: {data["subclasses"]}')
            #     print(show_to_player)
            #     await message.channel.send(f'Here you, go {username}!')
            #     if len(show_to_player) >= 2000 and len(show_to_player) < 4000:
            #         await message.channel.send(show_to_player[0:len(show_to_player)//2])
            #         await message.channel.send(show_to_player[len(show_to_player)//2 if len(show_to_player)%2==0 else ((len(show_to_player)//2)+1):])
            #     elif len(show_to_player) < 2000:
            #         await message.channel.send(show_to_player)
            #     else:
            #         await message.channel.send("Wow thats a big spell! Discord can't fit all of that.")
            #     return
            # except:
                await message.channel.send("Stephen hasn't implemented classes yet, please check back alter. Try a spell or a feature!")
        ###features functionality needs: exploded lists for any nested columns, as well as a quick write up about what the 'quick reference' info would need.
        ##### PAY ATTENTION TO THE COLUMNS. featuress are messy, fickle, and wildly different. It could be rough. #####
        if 'features' in input:
            try:
                input=str(format_the_request).replace('features: ', '').replace(' ', '-')
                #print(input)
                class_request = requests.get(f'https://www.dnd5eapi.co/api/features/{input}')
                print(f'https://www.dnd5eapi.co/api/features/{input}')
                json_to_text = class_request.json()
                print(json_to_text)
                data = pd.DataFrame(pd.json_normalize(json_to_text))
                print(data)
                show_to_player = (f'{data["name"][0]}'
                                    f'\nLevel: {data["level"][0]}'
                                    f'\nDesc: {data["desc"][0]}'
                                    f'\nClass: {data["class.name"][0]}'
                                    #f'\nPrerequisites: {data["prerequisites"]}'
                                    )
                print(show_to_player)
                await message.channel.send(f'Here you, go {username}!')
                if len(show_to_player) >= 2000 and len(show_to_player) < 4000:
                    await message.channel.send(show_to_player[0:len(show_to_player)//2])
                    await message.channel.send(show_to_player[len(show_to_player)//2 if len(show_to_player)%2==0 else ((len(show_to_player)//2)+1):])
                elif len(show_to_player) < 2000:
                    await message.channel.send(show_to_player)
                else:
                    await message.channel.send("Wow thats a big feature! Discord can't fit all of that.")
                return
            except:
                await message.channel.send("Hmmm. I couldn't find that feature. Are you sure its spelled right?")
        if 'feat' in input:
            try:
                input=str(format_the_request).replace('feat: ', '').replace(' ', '-')
                #print(input)
                class_request = requests.get(f'https://www.dnd5eapi.co/api/feats/{input}')
                print(f'https://www.dnd5eapi.co/api/feats/{input}')
                json_to_text = class_request.json()
                print(json_to_text)
                data = pd.DataFrame(pd.json_normalize(json_to_text))
                print(data)
                show_to_player = (f'{data["name"][0]}'
                                    f'\nLevel: {data["level"][0]}'
                                    f'\nDesc: {data["desc"][0]}'
                                    f'\nClass: {data["class.name"][0]}'
                                    #f'\nPrerequisites: {data["prerequisites"]}'
                                    )
                print(show_to_player)
                await message.channel.send(f'Here you, go {username}!')
                if len(show_to_player) >= 2000 and len(show_to_player) < 4000:
                    await message.channel.send(show_to_player[0:len(show_to_player)//2])
                    await message.channel.send(show_to_player[len(show_to_player)//2 if len(show_to_player)%2==0 else ((len(show_to_player)//2)+1):])
                elif len(show_to_player) < 2000:
                    await message.channel.send(show_to_player)
                else:
                    await message.channel.send("Wow thats a big features! Discord can't fit all of that.")
                return
            except:
                await message.channel.send("At the time of creation, there is only the 'grappler' feat in the API. I don't know why, either.")
    if channel == 'test_response':
        input=format_the_request
        if 'spell:' in input:
            try:
                input = format_the_request.replace('spell: ', '').replace(' ', '-')
                spells_request = requests.get(f'https://www.dnd5eapi.co/api/spells/{input}')
                json_to_text = spells_request.json()
                data = pd.DataFrame(pd.json_normalize(json_to_text))
                if 'material' in data.columns:
                    show_to_player = (f'{data["name"][0]}'
                                        f'\nDescription: '
                                        f'\n{(data["desc"][0])}'
                                        f'\nRange: {data["range"][0]}'
                                        f'\nComponents: {data["components"][0]}'
                                        f'\nMaterials: {data["material"][0]}'
                                        f'\nDuration: {data["duration"][0]}'
                                        f'\nConcentration: {data["concentration"][0]}'
                                        f'\nRitual: {data["ritual"][0]}'
                                        f'\n{data["casting_time"][0]}')
                else:
                    show_to_player = (f'{data["name"][0]}'
                                        f'\nDescription: '
                                        f'\n{data["desc"][0]}'
                                        f'\nRange: {data["range"][0]}'
                                        f'\nComponents: {data["components"][0]}'
                                        f'\nDuration: {data["duration"][0]}'
                                        f'\nConcentration: {data["concentration"][0]}'
                                        f'\nRitual: {data["ritual"][0]}'
                                        f'\n{data["casting_time"][0]}')
                await message.channel.send(f'Here you, go {username}!')
                if len(show_to_player) >= 2000 and len(show_to_player) < 4000:
                    await message.channel.send(show_to_player[0:len(show_to_player)//2])
                    await message.channel.send(show_to_player[len(show_to_player)//2 if len(show_to_player)%2==0 else ((len(show_to_player)//2)+1):])
                elif len(show_to_player) < 2000:
                    await message.channel.send(show_to_player)
                else:
                    await message.channel.send("Wow thats a big spell! Discord can't fit all of that.")
                return
            except:
                await message.channel.send("Hmmm. I couldn't find that spell. Are you sure its spelled right?")
        if 'class' in input:
            ###Needs some major work to make functional###
            # try:
            #     input=str(format_the_request).replace('class: ', '')
            #     #print(input)
            #     class_request = requests.get(f'https://www.dnd5eapi.co/api/classes/{input}')
            #     print(input)
            #     json_to_text = class_request.json()
            #     data = pd.json_normalize(json_to_text, max_level=2)
            #     df = pd.DataFrame(data)
            #     print(df.columns)
            #     if 'spells' in data.columns:
            #         show_to_player = (f'{data["name"][0]}'
            #                             f'\nHit Dice: 1d{data["hit_die"][0]} per level'
            #                             f'\nProficiency Choices: {data["proficiency_choices"][0]}'
            #                             f'\nProficiencies: {data["proficiencies"][0]}'
            #                             f'\nSaving Throws: {data["saving_throws"][0]}'
            #                             f'\nClass Levels: {data["class_levels"][0]}'
            #                             f'\nSubclasses: {data["subclasses"][0]}'
            #                             f'\nSpells: {data["spells"][0]}')
            #     else:
            #         show_to_player = (f'{data["name"]}'
            #                             f'\n{data["hit_die"]}'
            #                             f'\nProficiency Choices: {data["proficiency_choices"]}'
            #                             f'\nProficiencies: {data["proficiencies"]}'
            #                             f'\nSaving Throws: {data["saving_throws"]}'
            #                             f'\nClass Levels: {data["class_levels"]}'
            #                             f'\nSubclasses: {data["subclasses"]}')
            #     print(show_to_player)
            #     await message.channel.send(f'Here you, go {username}!')
            #     if len(show_to_player) >= 2000 and len(show_to_player) < 4000:
            #         await message.channel.send(show_to_player[0:len(show_to_player)//2])
            #         await message.channel.send(show_to_player[len(show_to_player)//2 if len(show_to_player)%2==0 else ((len(show_to_player)//2)+1):])
            #     elif len(show_to_player) < 2000:
            #         await message.channel.send(show_to_player)
            #     else:
            #         await message.channel.send("Wow thats a big spell! Discord can't fit all of that.")
            #     return
            # except:
                await message.channel.send("Stephen hasn't implemented classes yet, please check back later. Try a spell or a class feature!")
        ###features functionality needs: exploded lists for any nested columns, as well as a quick write up about what the 'quick reference' info would need.
        ##### PAY ATTENTION TO THE COLUMNS. featuress are messy, fickle, and wildly different. It could be rough. #####
        if 'features' in input:
            try:
                input=str(format_the_request).replace('features: ', '').replace(' ', '-')
                #print(input)
                class_request = requests.get(f'https://www.dnd5eapi.co/api/features/{input}')
                print(f'https://www.dnd5eapi.co/api/features/{input}')
                json_to_text = class_request.json()
                print(json_to_text)
                data = pd.DataFrame(pd.json_normalize(json_to_text))
                print(data)
                show_to_player = (f'{data["name"][0]}'
                                    f'\nLevel: {data["level"][0]}'
                                    f'\nDesc: {data["desc"][0]}'
                                    f'\nClass: {data["class.name"][0]}'
                                    #f'\nPrerequisites: {data["prerequisites"]}'
                                    )
                print(show_to_player)
                await message.channel.send(f'Here you, go {username}!')
                if len(show_to_player) >= 2000 and len(show_to_player) < 4000:
                    await message.channel.send(show_to_player[0:len(show_to_player)//2])
                    await message.channel.send(show_to_player[len(show_to_player)//2 if len(show_to_player)%2==0 else ((len(show_to_player)//2)+1):])
                elif len(show_to_player) < 2000:
                    await message.channel.send(show_to_player)
                else:
                    await message.channel.send("Wow thats a big feature! Discord can't fit all of that.")
                return
            except:
                await message.channel.send("Hmmm. I couldn't find that feature. Are you sure its spelled right?")
        if 'feat' in input:
            try:
                input=str(format_the_request).replace('features: ', '').replace(' ', '-')
                #print(input)
                class_request = requests.get(f'https://www.dnd5eapi.co/api/features/{input}')
                print(f'https://www.dnd5eapi.co/api/features/{input}')
                json_to_text = class_request.json()
                print(json_to_text)
                data = pd.DataFrame(pd.json_normalize(json_to_text))
                print(data)
                show_to_player = (f'{data["name"][0]}'
                                    f'\nLevel: {data["level"][0]}'
                                    f'\nDesc: {data["desc"][0]}'
                                    f'\nClass: {data["class.name"][0]}'
                                    #f'\nPrerequisites: {data["prerequisites"]}'
                                    )
                print(show_to_player)
                await message.channel.send(f'Here you, go {username}!')
                if len(show_to_player) >= 2000 and len(show_to_player) < 4000:
                    await message.channel.send(show_to_player[0:len(show_to_player)//2])
                    await message.channel.send(show_to_player[len(show_to_player)//2 if len(show_to_player)%2==0 else ((len(show_to_player)//2)+1):])
                elif len(show_to_player) < 2000:
                    await message.channel.send(show_to_player)
                else:
                    await message.channel.send("Wow thats a big features! Discord can't fit all of that.")
                return
            except:
                await message.channel.send("**Currently the API only lists grappler as a possible feat.**")
                #await message.channel.send("Hmmm. I couldn't find that feature. Are you sure its spelled right? **NOTE**")
try:
    client.run(token)
except:
    print('Token did not initialize.')