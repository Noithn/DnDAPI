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
    if channel == 'character-questions' or message.guild is None or channel == 'test_response':
        ###Spell functionality is good. Provides the user with quick reference to all needed spell info.
        input=format_the_request
        if 'skill' in input:
            input = format_the_request.replace('skill: ', '').replace(' ', '-')
            try:
                print(input)
                skills_request = requests.get(f'https://www.dnd5eapi.co/api/skills/{input}')
                print(str(skills_request))
                json_to_text = skills_request.json()
                print(str(json_to_text))
                data = pd.DataFrame(pd.json_normalize(json_to_text))
                print((data.columns))
                show_to_player = (f'{data["name"][0]}'
                                        f'\nDescription: '
                                        f'\n{(data["desc"][0])}'
                                        f'\nAbility Score: '
                                        f'\n{(data["ability_score.name"][0])}'
                                        f'\nSo you roll a d20, add your {(data["ability_score.name"][0])}, and your proficiency if its a skill you have.')
                print(show_to_player)
                await message.channel.send(show_to_player)
            except:
                await message.channel.send('Hmmmm. I can\'t find that skill. Is it spelled right?')
        if 'spell' in input:
            try:
                if 'minute meteors' in input:
                    await message.channel.send(f'Melf\'s Minute Meteors: '
                    f'\nDescription: '
                    f'\nYou create six tiny meteors in your space. They float in the air and orbit you for the spell\'s duration. When you cast the spell — and as a bonus action on each of your turns thereafter — you can expend one or two of the meteors, '
                    f'\nsending them streaking toward a point or points you choose within 120 feet of you. Once a meteor reaches its destination or impacts against a solid surface, the meteor explodes.'
                    f'\nEach creature within 5 feet of the point where the meteor explodes must make a Dexterity saving throw. A creature takes 2d6 fire damage on a failed save, or half as much damage on a successful one.'
                    f'\nAt Higher Levels. When you cast this spell using a spell slot of 4th level or higher, the number of meteors created increases by two for each slot level above 3rd.'
                    f'\nRange: Self'
                    f'\nComponents: V, S, M'
                    f'\nMaterials: Niter, Sulfur, and pine tar formed into a bead'
                    f'\nDuration: 10 minutes'
                    f'\nConcentration: No'
                    f'\nRitual: No'
                    f'\nCasting Time: 1 Action')

                elif 'shape water' in input:
                    await message.channel.send(f'Shape Water: '
                    f'\nDescription: '
                    f'\nYou choose an area of water that you can see within range and that fits within a 5-foot cube. You manipulate it in one of the following ways: You instantaneously move or otherwise change the flow of the water as you direct, up to 5 feet in any direction. This movement doesn\'t have enough force to cause damage. You cause the water to form into simple shapes and animate at your direction. This change lasts for 1 hour.You change the water\'s color or opacity. The water must be changed in the same way throughout. This change lasts for 1 hour.You freeze the water, provided that there are no creatures in it. The water unfreezes in 1 hour.If you cast this spell multiple times, you can have no more than two of its non-instantaneous effects active at a time, and you can dismiss such an effect as an action.'
                    f'\nRange: 30 feet'
                    f'\nComponents: S'
                    f'\nDuration: Instantaneous or 1 Hour'
                    f'\nConcentration: No'
                    f'\nRitual: No'
                    f'\nCasting Time: 1 Action')
                    
                elif 'absorb elements' in input:
                    await message.channel.send(f'Absorb Elements: '
                    f'\nDescription: '
                    f'\nThe spell captures some of the incoming energy, lessening its effect on you and storing it for your next melee attack. You have resistance to the triggering damage type until the start of your next turn. Also, the first time you hit with a melee attack on your next turn, the target takes an extra 1d6 damage of the triggering type, and the spell ends.'
                    f'\nAt Higher Levels. When you cast this spell using a spell slot of 2nd level or higher, the extra damage increases by 1d6 for each slot level above 1st.'
                    f'\nRange: Self'
                    f'\nComponents: S'
                    f'\nDuration: 1 Round'
                    f'\nConcentration: No'
                    f'\nRitual: No'
                    f'\nCasting Time: 1 Reaction(You cast this as a reaction to getting hit with acid, cold, fire, lightning, or thunder)')
                    
                elif 'thunderclap' in input:
                    await message.channel.send(f'Thunderclap:'
                    f'\nYou create a burst of thunderous sound that can be heard up to 100 feet away. Each creature within range, other than you, must succeed on a Constitution saving throw or take 1d6 thunder damage. The spell\'s damage increases by 1d6 when you reach 5th level (2d6), 11th level (3d6), and 17th level (4d6).'
                    f'\nRange: 5ft'
                    f'\nComponents: S'
                    f'\nDuration: Instantaneous'
                    f'\nConcentration: No'
                    f'\nRitual: No'
                    f'\nCasting Time: 1 Action')
                elif 'spell: ' in input:
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
                    if 'higher_level' in data.columns:
                        show_to_player = (f'{data["name"][0]}'
                                            f'\nDescription: '
                                            f'\n{(data["desc"][0])}'
                                            f'\nRange: {data["range"][0]}'
                                            f'\nComponents: {data["components"][0]}'
                                            f'\nHigher Levels: {data["higher_level"][0]}'
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
                else:
                    input = format_the_request.replace('spell:', '').replace(' ', '-')
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
                await message.channel.send("Classes are a WIP. Check back later!")
        ###features functionality needs: exploded lists for any nested columns, as well as a quick write up about what the 'quick reference' info would need.
        ##### PAY ATTENTION TO THE COLUMNS. features are messy, fickle, and wildly different. It could be rough. #####
        if 'features' in input:
            try:
                if 'bardic inspiration' in input:
                    await message.channel.send('Bardic Inspiration: • 3 / Short Rest'
                    f'\nAs a bonus action, a creature (other than yourself) within 60 ft. that can hear you gains an inspiration die (1d10). For 10 minutes, the creature can add it to one ability check, attack roll, or saving throw. '
                    f'\nThis can be added after seeing the roll, but before knowing the outcome. You can use it equal to your CHA modifier before recharging on a long rest.'
                    f'\nDice Per Level: 1d6 levels 1-4, 1d8 levels 5-9, 1d10 levels 10-14, 1d12 levels 15 +')
                else:
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
                if 'lucky' in input:
                    await message.channel.send("Lucky: "
                        f"\n You have 3 luck points per long rest. Whenever you make an attack roll, an ability check, or a saving throw (or when an attack roll is made against you), you can spend one to roll an additional d20 and you choose which die to use. You can choose to spend luck points after you roll the die, but before the outcome is determined. ")
                    return
                if 'crossbow exp' in input:
                    await message.channel.send("Crossbow Expert Attack "
                    f'\nWhen you use the Attack action and attack with a one-handed weapon, you can use a bonus action to attack with a hand crossbow you are holding. TIM! This means you get a second attack, +9 to hit, 1d8+5 piercing damage in addition to main attack.'
                    f'\nHey! Tim! If you have sneak attack on the target, you also get 5d6 extra damage for a successful hit. Sneak attack requires advantage on the target, or the enemy is fighting someone within 5ft of it, and you don\'t have disadvantage for some reason.')
                    return
                if 'sharpshooter' in input:
                    await message.channel.send("Sharpshooter: "
                    f"\nAttacking at long range doesn't impose disadvantage on your ranged weapon attack rolls and your ranged weapon attacks ignore half cover and three-quarters cover. Before you make an attack with a ranged weapon that you are proficient with, you can choose to take a -5 penalty to the attack roll to add +10 to the attack's damage. "
                    f"\nTimothy! This doesn't prevent you from getting +10 on the damage, so you can totally use a regular, an off hand, sneak attack, and this all in one massive blow out."
                    f"\nTotal damage count as of Level 10:2d8+21, and 5d6 sneak attack."
                    f"\nIf you're using special ammo, you have to figure that out on your own, bro.")
                    return
                else: 
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
try:
    client.run(token)
except:
    print('Token did not initialize.')