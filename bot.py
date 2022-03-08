import configparser
import discord
import operator
import os

intents = discord.Intents.default()
client = discord.Client(intents=intents)

option = configparser.ConfigParser()
option.read("setting.ini", encoding="utf-8")
number = option["setting"]["number"]
invite_role = option["setting"]["invite_role"]
list_role = option["setting"]["list_role"]
channel = option["setting"]["channel"]


@client.event
async def on_ready():
    print('login')
    print(client.user.id)
    print('------------------------')
    game = discord.Game("/명령어")
    await client.change_presence(status=discord.Status.online, activity=game)


@client.event
async def on_message(message):
    if message.content != "" and message.channel.id == int(channel):
        with open('chat.txt', 'a', encoding='utf-8') as f:
            f.write(message.author.name + " : " + message.content+"\n\n")

    if message.content.startswith("/초대"):
        r = message.guild.get_role(int(invite_role))
        mem = await message.guild.fetch_member(message.author.id)
        list = await message.guild.invites()
        count = 0
        for i in list:
            if i.inviter.id == message.author.id:
                count += i.uses
        await message.channel.send(message.author.name + "님은 지금까지 " + str(count) + "명을 초대했습니다.")
        if count >= int(number) and r not in mem.roles:
            await mem.add_roles(r)
            await message.channel.send(str(number) + "명을 초대해 " + r.name + " 역할이 되셨습니다.")

    if message.content.startswith("/순위"):
        list = await message.guild.invites()
        ls = {}
        for i in list:
            try:
                if ls[i.inviter.id]:
                    c1 = ls[i.inviter.id]
                    ls[i.inviter.id] = c1 + i.uses
            except:
                ls[i.inviter.id] = i.uses

        ls = sorted(ls.items(), key=operator.itemgetter(1), reverse=True)
        l = ""
        try:
            for i in range(100):
                mem = await message.guild.fetch_member(ls[i][0])
                l = l + str(i + 1) + ". " + mem.name + " - " + str(ls[i][1]) + "명\n"
        except:
            pass
        await message.channel.send(l)

    if message.content.startswith("/인증"):
        r = message.guild.get_role(int(list_role))
        with open('member.txt', 'r', encoding='utf-8') as file:
            cli = file.readlines()
            if message.author.name in cli:
                mem = await message.guild.fetch_member(message.author.id)
                if r not in mem.roles:
                    await mem.add_roles(r)
                    await message.channel.send("인증되었습니다. 역할이 부여됩니다.")
                else:
                    await message.channel.send("이미 인증되어 역할이 부여되었습니다.")

            else:
                await message.channel.send("멤버 명단에 없습니다.")

################################################################################################

    if not message.author.guild_permissions.administrator:
        return

    if message.content.startswith("/채팅"):
        await message.channel.send(file=discord.File('chat.txt'))

    if message.content.startswith("/삭제"):
        with open('chat.txt', 'w', encoding='utf-8') as f:
            f.write("")

    if message.content.startswith("/멤버추가"):
        with open('member.txt', 'a', encoding='utf-8') as file:
            file.write(message.content[6:]+"\n")

    if message.content.startswith("/멤버삭제"):
        with open('member.txt', 'r', encoding='utf-8') as file:
            text = file.read()
        with open('member.txt', 'w', encoding='utf-8') as file:
            a = text.replace(message.content[6:]+"\n", "")
            file.write(a)

    if message.content.startswith("/멤버확인"):
        await message.channel.send(file=discord.File('member.txt'))

    if message.content.startswith("/명령어"):
        await message.channel.send("```/채팅 - 채팅백업파일 다운\n"
                                   "/삭제 - 백업파일 리셋\n"
                                   "/멤버추가 - 인증멤버 추가(/멤버추가 유저이름)\n"
                                   "/멤버삭제 - 인증멤버 삭제(/멤버삭제 유저이름)\n"
                                   "/멤버확인 - 인증멤버 목록확인\n"
                                   "/초대 - 본인의 초대자 수 확인\n"
                                   "/순위 - 초대 순위\n"
                                   "/인증 - 명단에 본인 이름이 있으면 역할획득```")

token = os.environ["TOKEN"]
client.run(token)
