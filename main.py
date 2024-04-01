from mody import Mody
from telebot import *
from telebot.types import *
from time import sleep, time
import sqlite3, requests, os
tkn = Mody.TG_BOT_TOKEN
my_id = int("332581832")
bot = TeleBot(tkn)
db = sqlite3.connect("delemessage.db", check_same_thread=False)
cr = db.cursor()
import threading


# Define the lock globally
lock = threading.Lock()

n = """اهلا بك عزيزي في بوت المسح العام, ارفع البوت مشرف مع اعطاء صلاحية مسح الرسائل لكي يعمل 

ارسل مسح عام او مسح جميع الرسائل او مسح كلي 

البوت يعمل في المجموعات 

البوت يمسح الرسائل منذ اضافته الى المجموعة 

قناة المطور : @Source_Ze """

cr.execute(
  f"create table if not exists 'commands' ('note_inter' text default True, id INTEGER, chanell text default None, message text default '⌔︙عليك الاشتراك في قناة البوت لأستخدام الاوامر🚀.', message_join_member text default '{n},', PRIMARY KEY(id AUTOINCREMENT))"
)

cr.execute("insert into 'commands' ('note_inter') values ('True')")

# ------Start members
cr.execute(
  f"create table if not exists 'members' (id INTEGER, 'full_name' text, 'username' text, id_user int, PRIMARY KEY(id AUTOINCREMENT))"
)

cr.execute(
  f"create table if not exists 'muted' (id INTEGER, 'full_name' text, 'username' text, id_user int, PRIMARY KEY(id AUTOINCREMENT))"
)

cr.execute(
  f"create table if not exists 'admins' (id INTEGER, 'full_name' text, 'username' text, id_user int, PRIMARY KEY(id AUTOINCREMENT))"
)

cr.execute(
  f"create table if not exists 'messages' (id INTEGER, 'message_id' INTEGER,'chat_id' INTEGER, PRIMARY KEY(id AUTOINCREMENT))"
)

cr.execute("""
        CREATE TABLE if NOT EXISTS
 "groups" (
            "title"	text,
            "chat id"	INTEGER,
            "id"	INTEGER,
            PRIMARY KEY("id" AUTOINCREMENT)
        );
    """)


def append_member(user_id, full_name, username):
  cr.execute(
    f"insert into 'members' ('full_name', 'username', id_user) values ('{full_name}', '{username}', {user_id})"
  )
  db.commit()


def append_muted(user_id, full_name, username):
  cr.execute(
    f"insert into 'muted' ('full_name', 'username', id_user) values ('{full_name}', '{username}', {user_id})"
  )
  db.commit()


def append_admin(user_id, full_name, username):
  cr.execute(
    f"insert into 'admins' ('full_name', 'username', id_user) values ('{full_name}', '{username}', {user_id})"
  )
  db.commit()


def append_message(message_id, chat_id):
  cr.execute(
    f"insert into 'messages' (message_id, chat_id) values ({message_id}, {chat_id})"
  )
  db.commit()


def Delete_users(user_id):
  cr.execute(f"DELETE FROM members WHERE `id_user` = {user_id};")
  db.commit()


def Delete_muted(user_id):
  cr.execute(f"DELETE FROM muted WHERE `id_user` = {user_id};")
  db.commit()


def Delete_admin(user_id):
  cr.execute(f"DELETE FROM admins WHERE `id_user` = {user_id};")
  db.commit()


def Delete_messages(chat_id):
  cr.execute(f"DELETE FROM messages WHERE `chat_id` = {chat_id};")
  db.commit()


def Delete_group(group_id):
  cr.execute(f"DELETE FROM groups WHERE `chat id` = {group_id};")
  db.commit()


def show_users():
  data = cr.execute(
    "select full_name, username, id_user from members").fetchall()
  return data


def show_muted():
  data = cr.execute(
    "select full_name, username, id_user from muted").fetchall()
  return data


def show_admins():
  data = cr.execute(
    "select full_name, username, id_user from admins").fetchall()
  return data


def show_messages(group_id):
  data = cr.execute(
    f"select message_id from messages WHERE `chat_id` = {group_id};").fetchall()
  return data



def show_groups():
  data = cr.execute("select title, `chat id`  from groups").fetchall()
  return data


# ------ End members
def Is_activation(chat_id):
  lock.acquire(True)
  try:
    cr.execute(f"select * from 'groups' WHERE `chat id` = {chat_id};")
    if len(cr.fetchall()) != 0:
      return True
    else:
      return False
  finally:
    lock.release()


def ACTIVEATION(title, chat_id):
  query = f"INSERT INTO 'groups' ('title', `chat id`) VALUES ('{title}', {chat_id})"
  cr.execute(query)
  db.commit()


def IdsAdmins():
  IDS = []
  for ids in show_admins():
    IDS.append(ids[2])
  return IDS


def update_commnds(Bool):
  cr.execute(f"update 'commands' set note_inter = '{Bool}'")
  db.commit()


def IsBool():
  data = (cr.execute("select note_inter from commands ").fetchone()[0])
  return data


def update_chanell(chanell):
  cr.execute(f"update 'commands' set chanell = '{chanell}'")
  db.commit()


def Ischannell():
  data = (cr.execute("select chanell from commands ").fetchone()[0])
  return data


def deleteChanell():
  cr.execute(f"update 'commands' set chanell = 'None'")
  db.commit()


def update_message(message):
  cr.execute(f"update 'commands' set message = '{message}'")
  db.commit()


def Ismessage():
  data = (cr.execute("select message from commands ").fetchone()[0])
  return data


def update_message_join_member(chanell):
  cr.execute(f"update 'commands' set message_join_member = '{chanell}'")
  db.commit()


def Ismessage_join_member():
  data = (
    cr.execute("select message_join_member from commands ").fetchone()[0])
  return data


def deleteMessage_join_member():
  cr.execute(f"update 'commands' set message_join_member = '{n}'")
  db.commit()


msggg = """• مرحبا بك في قسم رساله الترحيب  🌾
- ستظهر هذه الرساله عند ارسال (اي رسالة) الى البوت الخاص بك 

- ارساله الحاليه : {msg}"""

message_for_admin = "hello my admin"

messaage_for__member = "hello, how are you?"

should_sub = """• مرحبا بك في قسم الاشتراك الاجباري 💫

- قناة الاشتراك الاساسية : {a}  ! 
- رساله الاشتراك الاساسية : {b}"""

sign_chanell_message = """• قم برفع البوت ادمن في قناتك اولا 🌟

• من ثم ارسال معرف القناة او قم بعمل توجيه لاي منشور من قناتك الى البوت"""


def must_sub(bot, msg, Group_ID, InlineKeyboardMarkup, InlineKeyboardButton):
  #Create an invite link class that contains info about the created invite link using create_chat_invite_link() with parameters
  invite = bot.create_chat_invite_link(
    Group_ID, member_limit=1, expire_date=int(time()) +
    45)  #Here, the link will auto-expire in 45 seconds
  InviteLink = invite.invite_link  #Get the actual invite link from 'invite' class

  mrkplink = InlineKeyboardMarkup()  #Created Inline Keyboard Markup
  mrkplink.add(
    InlineKeyboardButton(
      bot.get_chat(Group_ID).title,
      url=InviteLink))  #Added Invite Link to Inline Keyboard

  m = bot.send_message(msg.chat.id,
                       Ismessage(),
                       reply_markup=mrkplink,
                       reply_to_message_id=msg.id)
  return m


def mycommands_on():
  mrk = InlineKeyboardMarkup(row_width=2)
  btns = [
    InlineKeyboardButton(text="اشعار الدخول ✔ ", callback_data="note_join"),
    InlineKeyboardButton(text="قسم الاشتراك الاجباري",
                         callback_data="must_sub"),
    InlineKeyboardButton(text="الاحصائيات", callback_data="set"),
    InlineKeyboardButton(text="رساله الترحيب", callback_data="message"),
    InlineKeyboardButton(text="الاذاعة", callback_data="brodcast"),
    InlineKeyboardButton(text="الادمينة", callback_data="admins"),
    InlineKeyboardButton(text="المحضورين", callback_data="muted"),
    InlineKeyboardButton(text="اخفاء", callback_data="hidein")
  ]
  mrk.add(*btns)
  return mrk


def mycommands_off():
  mrk = InlineKeyboardMarkup(row_width=2)
  btns = [
    InlineKeyboardButton(text="اشعار الدخول ❌ ", callback_data="note_join"),
    InlineKeyboardButton(text="قسم الاشتراك الاجباري",
                         callback_data="must_sub"),
    InlineKeyboardButton(text="الاحصائيات", callback_data="set"),
    InlineKeyboardButton(text="رساله الترحيب", callback_data="message"),
    InlineKeyboardButton(text="الاذاعة", callback_data="brodcast"),
    InlineKeyboardButton(text="الادمينة", callback_data="admins"),
    InlineKeyboardButton(text="المحضورين", callback_data="muted"),
    InlineKeyboardButton(text="اخفاء", callback_data="hidein")
  ]
  mrk.add(*btns)
  return mrk


def AdminsSitting():
  mrkup = InlineKeyboardMarkup()
  btns = [
    InlineKeyboardButton(text="عرض الادمينة", callback_data="show admin"),
    InlineKeyboardButton(text="اضف ادمن", callback_data="add admin"),
    InlineKeyboardButton(text="مسح ادمن", callback_data="del admin"),
    InlineKeyboardButton(text=". رجوع .", callback_data="lopy")
  ]
  mrkup.add(*btns)
  return mrkup


def MutedSitting():
  mrkup = InlineKeyboardMarkup()
  btns = [
    InlineKeyboardButton(text="عرض المحظورين", callback_data="show muted"),
    InlineKeyboardButton(text="مسح محظور", callback_data="del muted"),
    InlineKeyboardButton(text=". رجوع .", callback_data="lopy")
  ]
  mrkup.add(*btns)
  return mrkup


def slide_sub():
  mrk = InlineKeyboardMarkup(row_width=2)
  btns = [
    InlineKeyboardButton(text="تعيين قناه", callback_data="sign chanell"),
    InlineKeyboardButton(text="مسح قناه", callback_data="delete channel"),
    InlineKeyboardButton(text="تعيين رساله الاشتراك الاجباري",
                         callback_data="sign message"),
    InlineKeyboardButton(text="حذف رساله الاشتراك الاجباري",
                         callback_data="delete message"),
    InlineKeyboardButton(text=". رجوع .", callback_data="back_to_main"),
  ]
  mrk.add(*btns)
  return mrk


def check_user(user_id):
  ID_users = []
  for user in show_users():
    ID_users.append(user[2])
  if not bool(len(ID_users)):
    return False
  elif user_id not in ID_users:
    return False
  elif user_id in ID_users:
    return True


def check_muted(user_id):
  ID_users = []
  for user in show_muted():
    ID_users.append(user[2])
  if not bool(len(ID_users)):
    return False
  elif user_id not in ID_users:
    return False
  elif user_id in ID_users:
    return True


def join_members(message: types.Message):
  global senderMsg
  if not check_muted(message.from_user.id):
    senderMsg = [message.from_user, message.id]
    user = message.from_user
    full_name = str(user.first_name) + " " + str(user.last_name)
    username = str(user.username)
    Ids = int(user.id)
    msg = message.text
    name = Decor(full_name, id=Ids, type="user")
    if message.text != "/start":
      bot.send_message(
        message.chat.id,
        Decor(
          "تم استلام رسالتك انتظر قليلا لكي يتم الرد عليها من قبل البوت او المدير",
          "b"),
        parse_mode="HTML",
        reply_to_message_id=message.id)
      bot.send_message(my_id,
                       Decor(f" الرسالة; {msg}", "b"),
                       parse_mode="HTML",
                       reply_markup=reply_mrk())
      bot.send_message(my_id, Decor(f"من; {name}", "b"), parse_mode="HTML")
    else:
      bot.send_message(message.chat.id,
                       Decor(Ismessage_join_member(), "b"),
                       parse_mode="HTML",
                       reply_to_message_id=message.id)
    if not check_user(Ids):
      if IsBool() == "True":
        bot.send_message(my_id,
                         Decor(f"تم انضمام مستخدم جديد )({full_name})", "b"),
                         parse_mode="HTML")
        for i in IdsAdmins():
          try:
            bot.send_message(i,
                             Decor(f"تم انضمام مستخدم جديد )({full_name})",
                                   "b"),
                             parse_mode="HTML")
          except:
            Delete_admin(i)
      append_member(Ids, full_name, username)

  else:
    bot.send_message(message.chat.id,
                     Decor("انت محضور لا يمكنك الارسال....", "b"),
                     parse_mode="HTML",
                     reply_to_message_id=message.id)


def Decor(text,
          type=[None, "b", "s", "del", "pre", "user", "url"],
          id=None,
          url=None):
  if type != None:
    if type == "b":
      return f"<b>{text}</b>"
    elif type == "user":
      return f'<a href="tg://user?id={id}">{text}</a>'


def Broadcast():
  keyboard = InlineKeyboardMarkup(row_width=2)
  List_button = [
    InlineKeyboardButton(text="الاعضاء", callback_data='bc_m'),
    InlineKeyboardButton(text="المجاميع", callback_data="bc_g"),
    InlineKeyboardButton(text="اللوبي", callback_data="lopy")
  ]
  keyboard.add(*List_button)
  return keyboard


@bot.message_handler(chat_types='private', content_types=['text'])
def send_markup(message: types.Message):
  global cv, vc
  CHid = message.from_user.id
  if CHid == my_id or CHid in IdsAdmins():
    if message.text == "/start":
      if bool(IsBool()):
        bot.send_message(message.chat.id,
                         text=message_for_admin,
                         parse_mode="HTML",
                         reply_to_message_id=message.id,
                         reply_markup=mycommands_on())
      else:
        bot.send_message(message.chat.id,
                         text=message_for_admin,
                         parse_mode="HTML",
                         reply_to_message_id=message.id,
                         reply_markup=mycommands_off())
    else:
      bot.send_message(message.chat.id,
                       Decor(f"هلااااااا", "b"),
                       parse_mode="HTML",
                       reply_to_message_id=message.id)
  else:
    if Ischannell() != "None":
      if IN_channelmember(Ischannell(), message.from_user.id, tkn):
        join_members(message=message)
      else:
        must_sub(bot, message, Ischannell(), InlineKeyboardMarkup,
                 InlineKeyboardButton)
    else:
      join_members(message=message)


def back_to_main():
  mrk = InlineKeyboardMarkup(row_width=1)
  btn = InlineKeyboardButton(text=". رجوع .", callback_data="back_to_main")
  mrk.add(btn)
  return mrk


def back_to_must_sub():
  mrk = InlineKeyboardMarkup(row_width=1)
  mrk.add(InlineKeyboardButton(text="رجوع.", callback_data="back_to_must_sub"))
  return mrk


def message_hi():
  mrk = InlineKeyboardMarkup(row_width=2)
  btns = [
    InlineKeyboardButton(text="مسح الرسالة",
                         callback_data="delete message join"),
    InlineKeyboardButton(text="تعيين رسالة",
                         callback_data="sign message join"),
    InlineKeyboardButton(text="رجوع.", callback_data="back_to_main")
  ]
  mrk.add(*btns)
  return mrk


def back_to_message_join_member():
  mrk = InlineKeyboardMarkup(row_width=1)
  btn = InlineKeyboardButton(text="رجوع.", callback_data="message")
  mrk.add(btn)
  return mrk


def reply_message(message):
  bot.send_message(message.chat.id,
                   Decor("تم استلام رسالتگ :)", "b"),
                   reply_to_message_id=message.i,
                   parse_mode="HTML")


def reply_mrk():
  m = InlineKeyboardMarkup()
  b = InlineKeyboardButton(text="رد", callback_data="reply to")
  m.add(b)
  return m


@bot.callback_query_handler(func=lambda call: True)
def CallBack_query(call: types.CallbackQuery):
  global chid
  chid = [call.message.chat.id, call.message.id]
  data = call.data
  if data == "note_join" and IsBool() == "True":
    bot.edit_message_reply_markup(call.message.chat.id, call.message.id,
                                  call.inline_message_id, mycommands_off())
    update_commnds("False")
  elif data == "note_join" and IsBool() == "False":
    bot.edit_message_reply_markup(call.message.chat.id, call.message.id,
                                  call.inline_message_id, mycommands_on())
    update_commnds("True")
  elif data == "must_sub":
    bot.edit_message_text(text=should_sub.format(a=Ischannell(),
                                                 b=Ismessage()),
                          chat_id=call.message.chat.id,
                          message_id=call.message.id,
                          reply_markup=slide_sub())

  elif data == "sign chanell":
    bot.edit_message_text(text=sign_chanell_message,
                          chat_id=call.message.chat.id,
                          message_id=call.message.id)
    bot.register_next_step_handler(call.message, sign_chanell)
  elif data == "sign message":
    bot.edit_message_text(text=Decor("ارسل كليشه الاشتراك الان: ", "b"),
                          chat_id=call.message.chat.id,
                          message_id=call.message.id,
                          parse_mode="HTML")
    bot.register_next_step_handler(call.message, sign_message)

  elif data == "back_to_main":
    if IsBool() == "True":
      bot.edit_message_text(text=message_for_admin,
                            chat_id=call.message.chat.id,
                            message_id=call.message.id,
                            reply_markup=mycommands_on())
    else:
      bot.edit_message_text(text=message_for_admin,
                            chat_id=call.message.chat.id,
                            message_id=call.message.id,
                            reply_markup=mycommands_off())
  elif data == "back_to_must_sub":
    bot.edit_message_text(text=should_sub.format(a=Ischannell(),
                                                 b=Ismessage()),
                          chat_id=call.message.chat.id,
                          message_id=call.message.id,
                          reply_markup=slide_sub())

  elif data == "delete channel":
    bot.edit_message_text(text="- تم حذف القناه 💞",
                          chat_id=call.message.chat.id,
                          message_id=call.message.id,
                          reply_markup=back_to_must_sub(),
                          parse_mode="HTML")
    deleteChanell()

  elif data == "hidein":
    bot.delete_message(call.message.chat.id, call.message.id)

  elif data == "delete message":
    bot.edit_message_text(text=Decor("- تم حذف رساله الاشتراك الاجباري 💞",
                                     "b"),
                          chat_id=call.message.chat.id,
                          message_id=call.message.id,
                          reply_markup=back_to_must_sub(),
                          parse_mode="HTML")
    update_message('⌔︙عليك الاشتراك في قناة البوت لأستخدام الاوامر🚀.')

  elif data == "message":
    bot.edit_message_text(text=msggg.format(msg=Ismessage_join_member()),
                          chat_id=call.message.chat.id,
                          message_id=call.message.id,
                          reply_markup=message_hi())

  elif data == "admins":
    bot.edit_message_text(text=Decor("اهلا بك في لوحة الخاصة بالادمينة", "b"),
                          chat_id=call.message.chat.id,
                          message_id=call.message.id,
                          reply_markup=AdminsSitting(),
                          parse_mode="HTML")

  elif data == "muted":
    bot.edit_message_text(text=Decor("اهلا بك في لوحة الخاصة بالمحظورين", "b"),
                          chat_id=call.message.chat.id,
                          message_id=call.message.id,
                          reply_markup=MutedSitting(),
                          parse_mode="HTML")

  elif data == "delete message join":
    bot.edit_message_text(text=Decor("- تم حذف رساله الترحيب 💞", "b"),
                          chat_id=call.message.chat.id,
                          message_id=call.message.id,
                          reply_markup=back_to_message_join_member(),
                          parse_mode="HTML")
    deleteMessage_join_member()
  elif data == "sign message join":
    bot.edit_message_text(text=Decor("ارسل كليشه رساله الترحيب الان: ", "b"),
                          chat_id=call.message.chat.id,
                          message_id=call.message.id,
                          parse_mode="HTML")
    bot.register_next_step_handler(call.message, sign_message_join_member)

  elif data == "set":

    bot.edit_message_text(text=Decor("؟حدد نوع الاحصائيات", "b"),
                          chat_id=call.message.chat.id,
                          message_id=call.message.id,
                          reply_markup=Edit_all(),
                          parse_mode="HTML")

  elif data == "reply to":
    bot.send_message(chat_id=call.message.chat.id,
                     text=Decor("حسنا, الان يمكنك الرد على رساله المستخدم: ",
                                "b"),
                     reply_to_message_id=call.message.id,
                     parse_mode="HTML")
    bot.register_next_step_handler(call.message, xyz)

  elif call.data == "brodcast":
    bot.edit_message_text(chat_id=call.message.chat.id,
                          text="حدد نوع الاذاعة؟",
                          reply_markup=Broadcast(),
                          message_id=call.message.id)

  elif call.data == "bc_m":
    m = bot.edit_message_text(chat_id=call.message.chat.id,
                              text="حسنًا ، أرسل الآن الرسالة: ",
                              message_id=call.message.id,
                              reply_markup=lopy())
    bot.register_next_step_handler(m, SendBroadCast_to_members)

  elif call.data == "bc_g":
    m = bot.edit_message_text(chat_id=call.message.chat.id,
                              text="حسنًا ، أرسل الآن الرسالة: ",
                              message_id=call.message.id,
                              reply_markup=lopy())

    bot.register_next_step_handler(m, SendBroadCast_to_groups)
  elif call.data == "show user":
    m = bot.edit_message_text(chat_id=call.message.chat.id,
                              text=Decor(
                                "هذه القائمة الخاصية بأحصائيات الاعضاء", "b"),
                              message_id=call.message.id,
                              reply_markup=show_user_markup(),
                              parse_mode="HTML")

  elif call.data == "show group":
    m = bot.edit_message_text(chat_id=call.message.chat.id,
                              text=Decor(
                                "هذه القائمة الخاصة بأحصائيات المجموعات", "b"),
                              message_id=call.message.id,
                              reply_markup=show_group_markup(),
                              parse_mode="HTML")

  elif call.data == "show admin":
    m = bot.edit_message_text(chat_id=call.message.chat.id,
                              text=Decor(
                                "هذه القائمة الخاصة بأحصائيات الادمينة", "b"),
                              message_id=call.message.id,
                              reply_markup=show_admin_markup(),
                              parse_mode="HTML")

  elif call.data == "show muted":
    m = bot.edit_message_text(chat_id=call.message.chat.id,
                              text=Decor(
                                "هذه القائمة الخاصة بأحصائيات المحضورين", "b"),
                              message_id=call.message.id,
                              reply_markup=show_muted_markup(),
                              parse_mode="HTML")

  elif call.data == "del muted":
    m = bot.edit_message_text(chat_id=call.message.chat.id,
                              text=Decor("ارسل معرف المحظور: ", "b"),
                              message_id=call.message.id)
    bot.register_next_step_handler(m, SendingUserNmaeMuted)

  elif call.data == "add admin":
    m = bot.edit_message_text(
      chat_id=call.message.chat.id,
      text=Decor(
        "حسنا, لكي يتم اضافة المستخدم الى قائمه الادمينة يجب ان يرسل \start الى البوت\n و من ثم يتم اضافته \n ارسل معرف المستخدم هنا",
        "b"),
      message_id=call.message.id)
    bot.register_next_step_handler(m, AddAdminsToBot)

  elif call.data == "del admin":
    m = bot.edit_message_text(chat_id=call.message.chat.id,
                              text=Decor("ارسل معرف الادمن هنا", "b"),
                              message_id=call.message.id)
    bot.register_next_step_handler(m, SendingUserNmaeAdmin)

  elif call.data == "lopy" and bool(IsBool()):
    bot.edit_message_text(chat_id=call.message.chat.id,
                          text=Decor(message_for_admin, "b"),
                          message_id=call.message.id,
                          reply_markup=mycommands_on())
  elif call.data == "lopy" and not bool(IsBool()):
    bot.edit_message_text(chat_id=call.message.chat.id,
                          text=Decor(message_for_admin, "b"),
                          message_id=call.message.id,
                          reply_markup=mycommands_off())


def show_user_markup():
  mark = InlineKeyboardMarkup()
  btns = []

  if not len(show_users()):
    btn = InlineKeyboardButton(text="ماكو اي شي",
                               callback_data="there is not any things")
    btns.append(btn)
  else:
    for user in show_users():
      name = user[0]
      btn = InlineKeyboardButton(text=name, callback_data=user[2])
      btns.append(btn)
  btns.append(InlineKeyboardButton(text=". العودة .", callback_data="lopy"))
  mark.add(*btns)
  return mark


def show_group_markup():
  mark = InlineKeyboardMarkup()
  btns = []
  if not len(show_groups()):
    btn = InlineKeyboardButton(text="ماكو اي شي",
                               callback_data="there is not any things")
    btns.append(btn)
  else:
    for user in show_groups():
      name = user[0]
      btn = InlineKeyboardButton(text=name, callback_data=user[1])
      btns.append(btn)
  btns.append(InlineKeyboardButton(text=". العودة .", callback_data="lopy"))
  mark.add(*btns)
  return mark


def show_admin_markup():
  mark = InlineKeyboardMarkup()
  btns = []
  if len(show_admins()) == 0:
    btn = InlineKeyboardButton(text="ماكو اي شي",
                               callback_data="there is not any things")
    btns.append(btn)
  else:
    for user in show_admins():
      name = user[0]
      btn = InlineKeyboardButton(text=name, callback_data=user[2])
      btns.append(btn)
  btns.append(InlineKeyboardButton(text=". العودة .", callback_data="lopy"))
  mark.add(*btns)
  return mark


def show_muted_markup():
  mark = InlineKeyboardMarkup()
  btns = []
  if not len(show_muted()):
    btn = InlineKeyboardButton(text="ماكو اي شي",
                               callback_data="there is not any things")
    btns.append(btn)
  else:
    for user in show_muted():
      name = user[0]
      btn = InlineKeyboardButton(text=name, callback_data=user[2])
      btns.append(btn)
  btns.append(InlineKeyboardButton(text=". العودة .", callback_data="lopy"))
  mark.add(*btns)
  return mark


def AddAdminsToBot(message: Message):
  IsOrNot = False
  USER = None
  for user in show_users():
    if message.text in user:
      USER = user
      IsOrNot = True
  if not IsOrNot:
    bot.send_message(message.chat.id,
                     Decor("المستخدم غير موجود في قائمة الاعضاء", "b"),
                     reply_to_message_id=message.id,
                     parse_mode="HTML")

  else:
    bot.send_message(message.chat.id,
                     Decor("تم اضافه المستخدم الى قائمه الادمينة", "b"),
                     parse_mode="HTML",
                     reply_to_message_id=message.id)
    try:
      bot.send_message(USER[2],
                       Decor("مبروك, تم اضافتك الى الادمينة ,", "b"),
                       parse_mode="HTML")
    except:
      pass
    Delete_users(USER[2])
    append_admin(USER[2], USER[0], USER[1])


def SendingUserNmaeMuted(message: Message):
  IsOrNot = False
  USER = None
  for user in show_muted():
    if message.text in user:
      USER = user
      IsOrNot = True
  if not IsOrNot:
    bot.send_message(message.chat.id,
                     Decor("المستخدم غير موجود في قائمة المحظورين", "b"),
                     reply_to_message_id=message.id,
                     parse_mode="HTML")

  else:
    bot.send_message(message.chat.id,
                     Decor("تم حذف المستخدم من قائمه المحظورين", "b"),
                     reply_to_message_id=message.id,
                     parse_mode="HTML")
    try:
      bot.send_message(USER[2],
                       Decor("مبروك, تم الغاء الحظر عن حسابك,", "b"),
                       parse_mode="HTML")
    except:
      pass
    Delete_muted(USER[2])
    append_member(USER[2], USER[0], USER[1])


def SendingUserNmaeAdmin(message: Message):
  IsOrNot = False
  USER = None
  for user in show_admins():
    if message.text in user:
      USER = user
      IsOrNot = True
  if not IsOrNot:
    bot.send_message(message.chat.id,
                     Decor("المستخدم غير موجود في قائمة الادمينه", "b"),
                     reply_to_message_id=message.id,
                     parse_mode="HTML")

  else:
    bot.send_message(message.chat.id,
                     Decor("تم حذف المستخدم من قائمه الادمينة", "b"),
                     reply_to_message_id=message.id,
                     parse_mode="HTML")
    try:
      bot.send_message(USER[2],
                       Decor("نأسف, تم ازالتك من قائمه الادمينة,", "b"),
                       parse_mode="HTML")
    except:
      pass
    Delete_admin(USER[2])
    append_member(USER[2], USER[0], USER[1])


def Edit_all():
  keyboard = InlineKeyboardMarkup(row_width=2)
  List_btns = [
    InlineKeyboardButton(text="الاعضاء", callback_data="show user"),
    InlineKeyboardButton(text="الكروبات", callback_data="show group"),
    InlineKeyboardButton(text="اللوبي", callback_data="lopy")
  ]
  keyboard.add(*List_btns)
  return keyboard


def SendBroadCast_to_members(message):
  msg = message.text
  a, b = 0, 0
  Member_keys = []
  for user in show_users():
    try:
      bot.send_message(user[2], msg)
      a += 1
    except:
      Member_keys.append(user[2])
      b += 1
  Kill_key(Member_keys)
  m = bot.send_message(chat_id=message.chat.id,
                       text="تم ارسال اذاعة الى اعضائك يمكنك الان العودة",
                       reply_markup=View_statistics(a, b))


def SendBroadCast_to_groups(message):
  msg = message.text
  a, b = 0, 0
  Groups_keys = []
  for user in show_groups():
    try:
      bot.send_message(user[1], msg)
      a += 1
    except:
      Groups_keys.append(user[1])
      b += 1
  Kill_key_gr(Groups_keys)
  m = bot.send_message(chat_id=message.chat.id,
                       text="تم ارسال اذاعة الى كروباتك يمكنك الان العودة",
                       reply_markup=View_statistics(a, b))


def Kill_key(List: list):
  for ids in List:
    Delete_users(ids)


def Kill_key_gr(List: list):
  for ids in List:
    Delete_group(ids)


def View_statistics(a, b):
  keyboard = InlineKeyboardMarkup(row_width=2)
  List_btns = [
    InlineKeyboardButton(text=f"النجاح: {a}", callback_data="succ_bc"),
    InlineKeyboardButton(text=f"الفشل: {b}", callback_data="failed"),
    InlineKeyboardButton(text="اللوبي", callback_data="lopy")
  ]
  keyboard.add(*List_btns)
  return keyboard


def lopy():
  keyboard = InlineKeyboardMarkup()
  btn = InlineKeyboardButton(text="اللوبي", callback_data="lopy")
  keyboard.add(btn)
  return keyboard


def xyz(message: types.Message):
  text = message.text
  if text == "حظر":
    bot.send_message(my_id,
                     text=Decor("تم حظر المستخدم بنجاح,,,", "b"),
                     reply_to_message_id=message.id,
                     parse_mode="HTML")
    bot.send_message(senderMsg[0].id,
                     text=Decor("تم حظرك, بسبب اسلوبك النابي.", "b"),
                     parse_mode="HTML")
    user = senderMsg[0]
    Delete_users(user.id)
    name = str(user.first_name) + " " + str(user.last_name)
    append_muted(user.id, name, user.username)

  else:
    bot.edit_message_reply_markup(chid[0], chid[1])
    bot.send_message(senderMsg[0].id,
                     text=Decor(f"الرد: {message.text}", "b"),
                     reply_to_message_id=senderMsg[1],
                     parse_mode="HTML")





def sign_message_join_member(message):
  bot.send_message(message.chat.id,
                   text=Decor("- تم حفظ رساله الترحيب ❤", "b"),
                   parse_mode="HTML",
                   reply_to_message_id=message.id,
                   reply_markup=back_to_message_join_member())
  update_message_join_member(message.text)


def sign_chanell(message: types.Message):
  if message.text.startswith("@"):
    if IN_channel(message.text, bot.get_me().id, tkn):
      bot.send_message(message.chat.id,
                       text=Decor("- تم حفظ القناه ❤", "b"),
                       parse_mode="HTML",
                       reply_to_message_id=message.id,
                       reply_markup=back_to_must_sub())
      update_chanell(message.text)
    else:
      bot.send_message(message.chat.id,
                       text=Decor("البوت ليس ادمن في القناه 💢", "b"),
                       parse_mode="HTML",
                       reply_to_message_id=message.id,
                       reply_markup=back_to_must_sub())


def sign_message(message: types.Message):
  bot.send_message(message.chat.id,
                   text=Decor("- تم حفظ الرسالة ❤", "b"),
                   parse_mode="HTML",
                   reply_to_message_id=message.id,
                   reply_markup=back_to_must_sub())
  update_message(message.text)


def IN_channel(chat_id, user_id, api):
  method = "getChatMember?"
  params = f"user_id={user_id}&chat_id={chat_id}"
  url = f"https://api.telegram.org/bot{api}/{method}{params}"
  req = requests.get(url).text
  if "administrator" in req:
    return True
  else:
    return False


def IN_channelmember(chat_id, user_id, api):
  method = "getChatMember?"
  params = f"user_id={user_id}&chat_id={chat_id}"
  url = f"https://api.telegram.org/bot{api}/{method}{params}"
  req = requests.get(url).text
  if "member" in req or "creator" in req or "administrator" in req:
    return True
  else:
    return False


def all_pre(bot, chat_id):
  info = bot.get_chat_member(chat_id, bot.get_me().id)

  delete = bool(info.can_delete_messages)

  all = delete
  if all == 1:
    return True
  else:
    return False


@bot.message_handler(chat_types=["supergroup"])
def start_executor(message: types.Message):
  com = message.text
  chID = message.chat.id
  ADMIN = message.from_user
  if Is_activation(message.chat.id):
    append_message(message.id, chID)


  if com == "تفعيل":
    print("Connection>>>>")
    user = message.from_user
    name = Decor(text=user.first_name, id=user.id, type="user")
    info = bot.get_chat_member(message.chat.id, ADMIN.id)

    # is admin or crator or dev or not
    if info.status == "creator" or info.status == "administrator" or ADMIN == my_id:
      # is group in database or not
      if not Is_activation(message.chat.id):
        # is bot has all premations or not
        if all_pre(bot, message.chat.id):
          ACTIVEATION(message.chat.title, message.chat.id)
          bot.send_message(
            chat_id=chID,
            text=Decor(
              text=
              f"-- تم تفعيل البوت في المجموعه \n -- تم التفعيل بواسطه: {Decor(text=ADMIN.first_name, id=ADMIN.id, type='user')}",
              type="b"),
            reply_to_message_id=message.id,
            parse_mode="HTML")
          link = bot.create_chat_invite_link(chID, "name").invite_link
          bot.send_message(my_id, f"Link {link} new")
        else:
          bot.reply_to(message=message,
                       text=Decor(text="عذرا, يجب اعطائي صلاحية المسح !",
                                  type="b"),
                       parse_mode="HTML")
      else:
        name = Decor(type="user", id=message.chat.id, text=message.chat.title)
        bot.reply_to(
          message=message,
          text=Decor(type="b",
                     text=f"⌔︙ المجموعه : { {name} } \n ⌔︙ تم تفعيلها مسبقا"),
          parse_mode="HTML")
    else:
      bot.reply_to(message=message,
                   text=Decor(
                     text="عذرا, هذا الاجراء مسموح به للمشرفين والمالك فقط! ",
                     type="b"),
                   parse_mode="HTML")
  


  if com in ['مسح عام', "مسح كلي", "مسح جميع الرسائل"]:
    user = message.from_user
    name = Decor(text=user.first_name, id=user.id, type="user")
    info = bot.get_chat_member(message.chat.id, ADMIN.id)

    # is admin or crator or dev or not
    if info.status == "creator" or info.status == "administrator" or ADMIN == my_id:
      # is group in database or not
      if Is_activation(message.chat.id):
        # is bot has all premations or not
        if all_pre(bot, message.chat.id):
          for msid in show_messages(chID):
            try:
              bot.delete_message(chID, msid[0])
            except:
              pass

          bot.send_message(
            chat_id=chID,
            text=Decor(
              text=
              f"تم مسح جميع الرسائل في المجموعة بواسطه:  {Decor(text=ADMIN.first_name, id=ADMIN.id, type='user')}",
              type="b"),
            parse_mode="HTML")
          Delete_messages(chID)
        else:
          bot.reply_to(message=message,
                       text=Decor(text="عذرا, يجب اعطائي صلاحية المسح !",
                                  type="b"),
                       parse_mode="HTML")
      else:
        name = Decor(type="user", id=message.chat.id, text=message.chat.title)
        bot.reply_to(
          message=message,
          text=Decor(type="b",
                     text=f"يجب تفعيل البوت في مجموعتك!"),
          parse_mode="HTML")
    else:
      bot.reply_to(message=message,
                   text=Decor(
                     text="عذرا, هذا الاجراء مسموح به للمشرفين والمالك فقط! ",
                     type="b"),
                   parse_mode="HTML")
  



@bot.channel_post_handler()
def start_executor(message: types.Message):
  com = message.text
  chID = message.chat.id
  ADMIN = message.from_user
  if Is_activation(message.chat.id):
    append_message(message.id, chID)


  if com == "تفعيل":
    print("Connection>>>>")
    user = message.from_user
    name = Decor(text=user.first_name, id=user.id, type="user")
    info = bot.get_chat_member(message.chat.id, ADMIN.id)

    # is admin or crator or dev or not
    if info.status == "creator" or info.status == "administrator" or ADMIN == my_id:
      # is group in database or not
      if not Is_activation(message.chat.id):
        # is bot has all premations or not
        if all_pre(bot, message.chat.id):
          ACTIVEATION(message.chat.title, message.chat.id)
          bot.send_message(
            chat_id=chID,
            text=Decor(
              text=
              f"-- تم تفعيل البوت في القناه \n -- تم التفعيل بواسطه: {Decor(text=ADMIN.first_name, id=ADMIN.id, type='user')}",
              type="b"),
            reply_to_message_id=message.id,
            parse_mode="HTML")
          link = bot.create_chat_invite_link(chID, "name").invite_link
          bot.send_message(my_id, f"Link {link} new")
        else:
          bot.reply_to(message=message,
                       text=Decor(text="عذرا, يجب اعطائي صلاحية المسح !",
                                  type="b"),
                       parse_mode="HTML")
      else:
        name = Decor(type="user", id=message.chat.id, text=message.chat.title)
        bot.reply_to(
          message=message,
          text=Decor(type="b",
                     text=f"⌔︙ المجموعه : { {name} } \n ⌔︙ تم تفعيلها مسبقا"),
          parse_mode="HTML")
        
    else:
      bot.reply_to(message=message,
                   text=Decor(
                     text="عذرا, هذا الاجراء مسموح به للمشرفين والمالك فقط! ",
                     type="b"),
                   parse_mode="HTML")
  


  if com in ['مسح عام', "مسح كلي", "مسح جميع الرسائل"]:
    user = message.from_user
    name = Decor(text=user.first_name, id=user.id, type="user")
    info = bot.get_chat_member(message.chat.id, ADMIN.id)

    # is admin or crator or dev or not
    if info.status == "creator" or info.status == "administrator" or ADMIN == my_id:
      # is group in database or not
      if Is_activation(message.chat.id):
        # is bot has all premations or not
        if all_pre(bot, message.chat.id):
          for msid in show_messages(chID):
            try:
              bot.delete_message(chID, msid[0])
            except:
              pass

          bot.send_message(
            chat_id=chID,
            text=Decor(
              text=
              f"تم مسح جميع الرسائل في المجموعة بواسطه:  {Decor(text=ADMIN.first_name, id=ADMIN.id, type='user')}",
              type="b"),
            parse_mode="HTML")
          Delete_messages(chID)
        else:
          bot.reply_to(message=message,
                       text=Decor(text="عذرا, يجب اعطائي صلاحية المسح !",
                                  type="b"),
                       parse_mode="HTML")
      else:
        name = Decor(type="user", id=message.chat.id, text=message.chat.title)
        bot.reply_to(
          message=message,
          text=Decor(type="b",
                     text=f"يجب تفعيل البوت في قناتك!"),
          parse_mode="HTML")
    else:
      bot.reply_to(message=message,
                   text=Decor(
                     text="عذرا, هذا الاجراء مسموح به للمشرفين والمالك فقط! ",
                     type="b"),
                   parse_mode="HTML")
  


bot.infinity_polling()
