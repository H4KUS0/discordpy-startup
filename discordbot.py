# インストールした discord.py を読み込む
import discord
import pickle
import random
import os

if not os.path.isfile("./Members.pkl"):
    Members = [x,x,x,x,x,x]
    pickle.dump(Members,open('Members.pkl','wb'))
else:
    Members = pickle.load(open('Members.pkl','rb'))
if not os.path.isfile("./MemberID.pkl"):
    MemberID = 0
    pickle.dump(MemberID,open('MemberID.pkl','wb'))
else:
    MemberID = pickle.load(open('MemberID.pkl','rb'))

# 自分のBotのアクセストークンに置き換えてください
TOKEN = 'NzA1MzgxMDcyMDYxMzMzNTA1.XrvTFA.iaCznRwGXpTKhA_fvefUWQD5czI'

# 接続に必要なオブジェクトを生成
client = discord.Client()

# 変数
x = ':x:'# 絵文字
#GatherMsg = f"| CTF | 3on3 | : [ {Members[0]} - {Members[1]} - {Members[2]} - {Members[3]} - {Members[4]} - {Members[5]} ]"
ServerURL = 'soldat://153.127.11.50:23053/nihonnokimutaku39'

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    global Members, MemberID
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    if message.content == '!add':
        if MemberID == 0:
            embed = discord.Embed(description="**Gather募集開始**")
            await message.channel.send(embed=embed)
        if  Members.count(message.author.mention) > 0:
            embed = discord.Embed(description=f"{message.author.mention}は既に参加しています。")
            await message.channel.send(embed=embed)
            return
        Members[MemberID] = message.author.mention
        if MemberID < 5:
            MemberID += 1
            embed = discord.Embed(description=f"| CTF | 3on3 | : [ {Members[0]} - {Members[1]} - {Members[2]} - {Members[3]} - {Members[4]} - {Members[5]} ]", color=0x80ffff)
            await message.channel.send(embed=embed)
            pickle.dump(Members,open('Members.pkl','wb'))
            pickle.dump(MemberID,open('MemberID.pkl','wb'))
            return
        else:
            random.shuffle(Members)
            embed=discord.Embed(title="参加者がそろいました。\n下記のServerにJoinしてください。", description=f"{ServerURL}", color=0x80ffff)
            embed.add_field(name=":train: Alpha", value=f"[ {Members[0]} - {Members[1]} - {Members[2]} ]", inline=False)
            embed.add_field(name=":bullettrain_side: Bravo", value=f"[ {Members[3]} - {Members[4]} - {Members[5]} ]", inline=False)
            await message.channel.send(embed=embed)
            #await message.channel.send('参加者がそろいました。下記のServerにJoinしてください。\nsoldat://153.127.11.50:23053/nihonnokimutaku39')
            #await message.channel.send('[ :train:**Alpha** : ' + Members[0] + ' - ' + Members[1] + ' - ' + Members[2] + ' ]')
            #await message.channel.send('[ :bullettrain_side:**Bravo** : ' + Members[3] + ' - ' + Members[4] + ' - ' + Members[5] + ' ]')
            Members = [x,x,x,x,x,x]
            MemberID = 0
            pickle.dump(Members,open('Members.pkl','wb'))
            pickle.dump(MemberID,open('MemberID.pkl','wb'))
            return
    if message.content == '!del':
        if  Members.count(message.author.mention) == 0:
            return
        index = Members.index(message.author.mention)
        del Members[index]
        Members.append(x)
        MemberID -= 1
        embed = discord.Embed(description=f"| CTF | 3on3 | : [ {Members[0]} - {Members[1]} - {Members[2]} - {Members[3]} - {Members[4]} - {Members[5]} ]", color=0x80ffff)
        await message.channel.send(embed=embed)
        if MemberID == 0:
            embed = discord.Embed(description="Gather募集停止")
            await message.channel.send(embed=embed)
        pickle.dump(Members,open('Members.pkl','wb'))
        pickle.dump(MemberID,open('MemberID.pkl','wb'))
        return
    if message.content == '!info':
        if MemberID == 0:
            embed = discord.Embed(description="Gatherは募集中じゃないです")
            await message.channel.send(embed=embed)
        else:
            embed=discord.Embed(title="**Gather募集中**", description=f"| CTF | 3on3 | : [ {Members[0]} - {Members[1]} - {Members[2]} - {Members[3]} - {Members[4]} - {Members[5]} ]", color=0x80ffff)
            await message.channel.send(embed=embed)
        return
    #if message.content == '電車':
    #    await message.channel.send(':train:')
    #    return

# メンバのステータスが変更されたら
@client.event
async def on_member_update(before, after):
    global Members, MemberID
    if before.status != after.status:
        if str(after.status) == "offline":
            i = 0
            for offline in Members:
                if after.mention in offline:
                    del Members[i]
                    Members.append(x)
                    MemberID -= 1
                    pickle.dump(Members,open('Members.pkl','wb'))
                    pickle.dump(MemberID,open('MemberID.pkl','wb'))
                    break
                i += 1
        return

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
