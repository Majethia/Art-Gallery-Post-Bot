from telethon import events, Button
from config import bot, channel, storage
import asyncio
from mongodb import ArtGalleryDB

ArtGalleryDB = ArtGalleryDB()

lock = asyncio.Lock()


@bot.on(events.NewMessage(pattern="/start", func=lambda e: e.is_private))
async def start_fn(event):
    await bot.send_message(event.chat_id, "You successfully unblocked me")


@bot.on(events.NewMessage(pattern="/help"))
async def help_function(event):
    if len(event.raw_text) == 5:
        await bot.send_message(
            event.chat_id,
            "Hey there,this is a bot where you can submit your artworks for the channel: @SnortingecstasyArt\n Feel free to submit any kind of artwork here\n\nReply to your artwork with /post or #post to send request.",
            file="pic.png"
        )
    elif event.raw_text == "/help@Art_Gallery_Post_Bot":
        await bot.send_message(
            event.chat_id,
            "Hey there,this is a bot where you can submit your artworks for the channel: @SnortingecstasyArt\n Feel free to submit any kind of artwork here\n\nReply to your artwork with /post or #post to send request.",
            file="pic.png"
        )


@bot.on(events.NewMessage(pattern=r"#post|/post"))
async def post_function(event):
    if event.photo == None:
        x = await event.get_reply_message()
        if x == None:
            return
        elif x.photo == None:
            pic = None
            return
        pic = x.photo
    else:
        pic = event.photo
    sender_name = f"@{event.sender.username}"
    if event.sender.username == None:
        sender_name = f"[{event.sender.first_name} {event.sender.last_name}]|(tg123456789//user?id={event.sender.id})"
    x = await event.reply("Please Answer some questions to me before the submission is complete!\n(check your PMs UwU)", buttons=[Button.url("Check PMs", url=("t.me/Art_Gallery_Post_Bot"))])
    try:
        async with bot.conversation(event.sender_id) as conv:
            await conv.send_message('Whats the name of the artwork? (name of character if applicable)')
            hello = await conv.get_response()
            art = hello.raw_text
            await conv.send_message('Noted! now tell me which anime/manga its from (reply with "NA" if its not applicable)')
            name = await conv.get_response()
            anime = name.raw_text
            await conv.send_message("What type of art is it?\npen, pencil, color, digital?")
            tag = await conv.get_response()
            tags = tag.raw_text
            await conv.send_message("Ok, last... \nYour instagram Username/Handle (Optional, send 'NA' if you dont want to share or dont have one...) WITHOUT '@' ")
            ig_link = await conv.get_response()
            ig_link = ig_link.raw_text
            user_name = await bot.get_entity(event.sender_id)
            user_name = user_name.first_name
            await bot.send_message(event.sender_id, "Thats all thanks for your patience")
        m = await bot.send_message(
            storage,
            f"Requested by: {sender_name}\n\n Message link: t.me/c/{str(event.chat_id)[4:]}/{event.id}\n\nData: Note* check the below data and edit this message if needed\nArtist: {sender_name}\nArt: {art}.\nAnime: {anime}.\nTags: #{user_name}  #{tags}\nInstagram: {ig_link}",
            file=pic,
            buttons=[Button.inline("Approve", data="approve"),
                     Button.inline("Reject", data="reject")]
        )
        await event.reply(f"Request sent to [Art Gallery](t.me/SnortingecstasyArt)\nYour artwork will be posted at an appropriate time\nRequest id: `{m.id}`", link_preview=False)

    except Exception as e:
        await bot.send_message(732913305, str(e))
        await x.edit("Oof you seem to have blocked me, Unblock me and try to post again. :)", buttons=[Button.url("Unblock me", url=("t.me/Art_Gallery_Post_Bot"))])


@bot.on(events.CallbackQuery(pattern=b"reject"))
async def approve_function(event):
    x = await bot.get_entity(event.query.user_id)
    await event.edit(f"Rejected, dont post this one\nRejected By: @{x.username}")


@bot.on(events.CallbackQuery(pattern=b"approve"))
async def approve_function(event):
    msg = await bot.get_messages(event.chat_id, ids=event.message_id)
    x = await bot.get_entity(event.query.user_id)
    await event.edit(f"{msg.raw_text}\n\nApproved By @{x.username}", buttons=[Button.inline("Post on Channel", data="post"), Button.inline("Back", data="back")])


@bot.on(events.CallbackQuery(pattern=b"post"))
async def posted_function(event):
    x = await bot.get_entity(event.query.user_id)
    msg = await bot.get_messages(event.chat_id, ids=event.message_id)
    data = msg.text.split("\n\n")
    useful_data = data[2].split("\n")
    useful_data.pop(0)
    artist = useful_data[0].split(":")[1]
    artist = artist.replace("|", "")
    artist = artist.replace("123456789",":")
    art = useful_data[1].split(":")[1]
    anime = useful_data[2].split(":")[1]
    tags = useful_data[3].split(":")[1]
    ig_url = useful_data[4].split(":", 1)[1].strip()
    nulls = ["NA", "na", "Na", "na.", "Na.", "NA."]
    await bot.send_message(channel, file=msg.photo, buttons=[Button.inline("❤️", "0"), Button.inline("👍", "1")])
    if anime.strip() in nulls and ig_url.strip() in nulls:
        await bot.send_message(channel, f"Artist:-{artist}\nArt:-__{art}__\n\n{tags}")
    elif ig_url.strip() in nulls:
        await bot.send_message(channel, f"Artist:-{artist}\nArt:-__{art}__\nAnime:-__{anime}__\n\n{tags}")
    elif anime.strip() in nulls:
        await bot.send_message(channel, f"Artist:-{artist}\nInstagram:- [{ig_url}](https://www.instagram.com/{ig_url})\nArt:-__{art}__\n\n{tags}", link_preview=False)
    else:
        await bot.send_message(channel, f"Artist:-{artist}\nInstagram:- [{ig_url}](https://www.instagram.com/{ig_url})\nArt:-__{art}__\nAnime:- __{anime}__\n\n{tags}", link_preview=False)

    await event.edit(f"{msg.text}\n\nPosted to channel by @{x.username}")


@bot.on(events.CallbackQuery(pattern=b"back"))
async def go_back(event):
    msg = await bot.get_messages(event.chat_id, ids=event.message_id)
    text = msg.raw_text.split("\n")
    text.pop(-1)
    caption = "\n".join(text)
    await event.edit(caption, buttons=[Button.inline("Approve👍🏻", data="approve"), Button.inline("Reject👎🏻", data="reject")])


@bot.on(events.CallbackQuery(pattern=(b"0")))
async def _(event):
    async with lock:
        data = ArtGalleryDB.find(data={"_id": int(event.query.msg_id)})
        if data == None:
            data = {
                "_id": event.query.msg_id,
                "hearts": {"count": 0, "users":[]},
                "likes": {"count": 0, "users":[]}       
            }
            ArtGalleryDB.add(data)
        likes_count = int(data["likes"]["count"])
        hearts_count = int(data["hearts"]["count"])
    
        if event.sender.id not in data["hearts"]["users"] and event.sender.id not in data["likes"]["users"]:
            hearts_count = hearts_count+1
            data["hearts"]["users"].append(event.sender.id)
            new_data = {"hearts": {"count":(hearts_count), "users": data["hearts"]["users"]}}
            await event.answer("You ❤️ this.")

            ArtGalleryDB.modify({"_id": event.query.msg_id}, new_data)

        elif event.sender.id in data["hearts"]["users"]:
            hearts_count = hearts_count-1
            data["hearts"]["users"].remove(event.sender.id)
            new_data = {"hearts": {"count":(hearts_count), "users": data["hearts"]["users"]}}
            await event.answer("You took your reaction back")

            ArtGalleryDB.modify({"_id": event.query.msg_id}, new_data)

        elif event.sender.id in data["likes"]["users"]:
            hearts_count = hearts_count+1
            likes_count = likes_count-1
            data["hearts"]["users"].append(event.sender.id)
            data["likes"]["users"].remove(event.sender.id)
            new_data_hearts = {"hearts": {"count":(hearts_count), "users": data["hearts"]["users"]}}
            new_data_likes = {"likes": {"count":(likes_count), "users": data["likes"]["users"]}}
            await event.answer("You ❤️ this.")

            ArtGalleryDB.modify({"_id": event.query.msg_id}, new_data_hearts)
            ArtGalleryDB.modify({"_id": event.query.msg_id}, new_data_likes)

        await event.edit(buttons=[Button.inline(f"❤️{hearts_count}", "0"), Button.inline(f"👍{likes_count}", "1")])


@bot.on(events.CallbackQuery(pattern=(b"1")))
async def _(event):
    async with lock:
        data = ArtGalleryDB.find(data={"_id": event.query.msg_id})
        if data == None:
            data = {
                "_id": event.query.msg_id,
                "hearts": {"count": 0, "users":[]},
                "likes": {"count": 0, "users":[]}       
            }
            ArtGalleryDB.add(data)
        likes_count = int(data["likes"]["count"])
        hearts_count = int(data["hearts"]["count"])
        if event.sender.id not in data["hearts"]["users"] and event.sender.id not in data["likes"]["users"]:
            likes_count =likes_count+1
            data["likes"]["users"].append(event.sender.id)
            new_data = {"likes": {"count":(likes_count), "users": data["likes"]["users"]}}
            await event.answer("You 👍 this.")

            ArtGalleryDB.modify({"_id": event.query.msg_id}, new_data)

        elif event.sender.id in data["likes"]["users"]:
            likes_count = likes_count-1
            data["likes"]["users"].remove(event.sender.id)
            new_data = {"likes": {"count":(hearts_count), "users": data["likes"]["users"]}}
            await event.answer("You took your reaction back")

            ArtGalleryDB.modify({"_id": event.query.msg_id}, new_data)

        elif event.sender.id in data["hearts"]["users"]:
            hearts_count = hearts_count-1
            likes_count = likes_count+1
            data["likes"]["users"].append(event.sender.id)
            data["hearts"]["users"].remove(event.sender.id)
            new_data_likes = {"likes": {"count":(likes_count), "users": data["likes"]["users"]}}
            new_data_hearts = {"hearts": {"count":(hearts_count), "users": data["hearts"]["users"]}}
            await event.answer("You 👍 this.")
            
            ArtGalleryDB.modify({"_id": event.query.msg_id}, new_data_hearts)
            ArtGalleryDB.modify({"_id": event.query.msg_id}, new_data_likes)

        await event.edit(buttons=[Button.inline(f"❤️{hearts_count}", "0"), Button.inline(f"👍{likes_count}", "1")])


@bot.on(events.NewMessage(pattern="/status"))
async def _(event):
    text = event.text
    text = text.split()
    try:
        req = await bot.get_messages(storage, ids= int(text[1]))
        if "Approved" in req.text:
            await event.reply(f"The request has been approved!!!\nIt will be posted to the channel soon.\n\nLink for admins to confirm: t.me/c/{storage}/{text[1]}")
        
        elif "Rejected" in req.text:
            await event.reply(f"Sorry, the admins reviewed your request and decided to reject your request.\n\nLink for admins to confirm: t.me/c/{storage}/{text[1]}")

        else:
            await event.reply(f"This request has yet to be reviewed by the admins please wait till we get to it.\n\nLink for admins to confirm: t.me/c/{storage}/{text[1]}")

    except Exception as e:

        await event.reply(f"Error {e}: Either the request id is wrong or you didnt use the command correctly.\nUse in the format like:\n`/status <request id>`")

bot.start()

bot.run_until_disconnected()

