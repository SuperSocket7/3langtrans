import discord
import requests

client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_ready():
    global ja_ch
    global en_ch
    global es_ch
    ja_ch = client.get_channel(1078116161222352958)
    en_ch = client.get_channel(1077797409968640001)
    es_ch = client.get_channel(1077774121938714787)


async def send(channel, message, text):
    try:
        webhooks = await channel.webhooks()
        webhook = webhooks[0]
    except IndexError:
        await channel.create_webhook(name="Translate")
    if message.attachments:
        for attachment in message.attachments:
            await webhook.send(content=text + "\n" + attachment.url,
                               username=message.author.display_name,
                               avatar_url=message.author.display_avatar.url
                               )
    else:
        await webhook.send(content=text,
                           username=message.author.display_name,
                           avatar_url=message.author.display_avatar.url
                           )


def tr(text, source, target):
    r = requests.get(f"https://script.google.com/macros/s/AKfycbzowZjdWrs8td1cnJNwjmaVuSmpfR6gpYYQHNnJ6cPHDVedJXtv1K65CWtlZZ0SSgBGHQ/exec?text={text}&source={source}&target={target}")
    return r.json()['text']


@client.event
async def on_message(message):
    if message.author.bot or message.author.discriminator == "0000":
        return
    else:
        if message.channel == ja_ch:
            await send(channel=en_ch, message=message, text=tr(text=message.content, source="ja", target="en"))
            await send(channel=es_ch, message=message, text=tr(text=message.content, source="ja", target="es"))
        elif message.channel == en_ch:
            await send(channel=ja_ch, message=message, text=tr(text=message.content, source="en", target="ja"))
            await send(channel=es_ch, message=message, text=tr(text=message.content, source="en", target="es"))
        elif message.channel == es_ch:
            await send(channel=ja_ch, message=message, text=tr(text=message.content, source="es", target="ja"))
            await send(channel=en_ch, message=message, text=tr(text=message.content, source="es", target="en"))



client.run("Token")
