import telebot
import shelve
import os

bot = telebot.TeleBot('715925964:AAE4OfsnqtmrEf3wO8vlfe2bIBIwO-eG_1k')
chat_id = -383403724
dis = 'none'
doc_id = 'none'
msg_id = 'none'
current_directory = {}
starting_dir = []
user_id = 0


def create_keyboard(message):
    global current_directory, dis
    if current_directory[message.from_user.id] == starting_dir:
        current_directory[message.from_user.id].append(str(message.from_user.id))
    fld = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    current_folder = shelve.open('/'.join(current_directory[message.from_user.id]) + '/'
                                 + current_directory[message.from_user.id][-1])
    flag = False
    for one in current_folder:
        btn = telebot.types.InlineKeyboardButton(text=one)
        fld.add(btn)
        flag = True
    for fd in os.listdir('/'.join(current_directory[message.from_user.id])):
        if os.path.isdir('/'.join(current_directory[message.from_user.id]) + '/' + fd):
            btn = telebot.types.InlineKeyboardButton(text=fd)
            fld.add(btn)
            flag = True
    if current_directory[message.from_user.id] != starting_dir + [str(message.from_user.id)]:
        btn = telebot.types.InlineKeyboardButton(text='<=back')
        fld.add(btn)
    if not flag:
        if current_directory[message.from_user.id] == starting_dir + [str(message.from_user.id)]:
            bot.send_message(message.from_user.id, 'you have nothing in your disk. To make a file, send something.'
                                                   ' To add a folder, send command /folder')
        else:
            bot.send_message(message.from_user.id, 'start' +
                             '/' + '/'.join(current_directory[message.from_user.id][1:]))
            bot.send_message(message.from_user.id, 'this is empty', reply_markup=fld)
    else:
        if current_directory[message.from_user.id] == starting_dir + [str(message.from_user.id)]:
            bot.send_message(message.from_user.id, 'you are at start', reply_markup=fld)
        else:
            bot.send_message(message.from_user.id, 'start/' + '/'.join(current_directory[message.from_user.id][1:]),
                             reply_markup=fld)
    dis = 'open_directory'
    try:
        with shelve.open('log' + '/' + 'log') as log:
            log[str(message.from_user.id)] = 'open_directory'
    except:
        os.mkdir('log')
        with shelve.open('log' + '/' + 'log') as log:
            log[str(message.from_user.id)] = 'open_directory'


@bot.message_handler(commands=['start'])
def starter(message):
    global current_directory
    try:
        current_directory[message.from_user.id] = starting_dir[:]
        current_directory[message.from_user.id].append(str(message.from_user.id))
        os.mkdir('/'.join(current_directory[message.from_user.id]))
        bot.send_message(message.from_user.id, 'Welcome. To make a file, send a file.'
                                               ' To add a folder, send command /folder')
    except:
        bot.send_message(message.from_user.id, 'You are already in, welcome back :)')


@bot.message_handler(commands=['open_start'])
def open_directory(message):
    global dis
    global current_directory
    current_directory[message.from_user.id] = starting_dir + [str(message.from_user.id)]
    dis = 'open_directory'
    try:
        with shelve.open('log' + '/' + 'log') as log:
            log[str(message.from_user.id)] = 'open_directory'
    except:
        os.mkdir('log')
        with shelve.open('log' + '/' + 'log') as log:
            log[str(message.from_user.id)] = 'open_directory'
    create_keyboard(message)


@bot.message_handler(content_types=['document'])
def handle_document(message):
    global doc_id, current_directory
    if current_directory[message.from_user.id] == starting_dir:
        current_directory[message.from_user.id].append(str(message.from_user.id))
    doc_id = message.message_id
    msgs_id = bot.forward_message(chat_id, message.from_user.id, doc_id).message_id
    file_name = message.document.file_name
    with shelve.open('/'.join(current_directory[message.from_user.id])
                     + '/' + current_directory[message.from_user.id][-1]) as writer:
        writer[str(file_name) + '(document)'] = msgs_id
    bot.delete_message(message.from_user.id, doc_id)
    bot.send_message(message.from_user.id, 'done.')
    create_keyboard(message)


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    global doc_id, dis, current_directory, msg_id
    if current_directory[message.from_user.id] == starting_dir:
        current_directory[message.from_user.id] += [str(message.from_user.id)]
    doc_id = message.message_id
    msg_id = bot.forward_message(chat_id, message.from_user.id, doc_id).message_id
    bot.send_message(message.from_user.id, 'how do you want to name this media?')
    try:
        with shelve.open('log' + '/' + 'log') as log:
            log[str(message.from_user.id)] = 'name'
    except:
        os.mkdir('log')
        with shelve.open('log' + '/' + 'log') as log:
            log[str(message.from_user.id)] = 'name'
    dis = 'name'


@bot.message_handler(content_types=['video'])
def handle_video(message):
    global doc_id, dis, current_directory, msg_id
    if current_directory[message.from_user.id] == starting_dir:
        current_directory[message.from_user.id] += [str(message.from_user.id)]
    doc_id = message.message_id
    msg_id = bot.forward_message(chat_id, message.from_user.id, doc_id).message_id
    bot.send_message(message.from_user.id, 'how do you want to name this media?')
    dis = 'name'
    try:
        with shelve.open('log' + '/' + 'log') as log:
            log[str(message.from_user.id)] = 'name'
    except:
        os.mkdir('log')
        with shelve.open('log' + '/' + 'log') as log:
            log[str(message.from_user.id)] = 'name'


@bot.message_handler(content_types=['audio'])
def handle_audio(message):
    global doc_id, current_directory, dis, msg_id
    if current_directory[message.from_user.id] == starting_dir:
        current_directory[message.from_user.id] += [str(message.from_user.id)]
    doc_id = message.message_id
    msg_id = bot.forward_message(chat_id, message.from_user.id, doc_id).message_id
    bot.send_message(message.from_user.id, 'how do you want to name this media?')
    dis = 'name'
    try:
        with shelve.open('log' + '/' + 'log') as log:
            log[str(message.from_user.id)] = 'name'
    except:
        os.mkdir('log')
        with shelve.open('log' + '/' + 'log') as log:
            log[str(message.from_user.id)] = 'name'


@bot.message_handler(commands=['folder'])
def folder_creator(message):
    global dis
    bot.send_message(message.from_user.id, 'enter name of the folder')
    dis = 'folder'
    try:
        with shelve.open('log' + '/' + 'log') as log:
            log[str(message.from_user.id)] = 'folder'
    except:
        os.mkdir('log')
        with shelve.open('log' + '/' + 'log') as log:
            log[str(message.from_user.id)] = 'folder'


@bot.message_handler(content_types=['text'])
def distributor(message):
    global current_directory, dis, user_id
    try:
        d = shelve.open('log' + '/' + 'log')
        dis = d[str(message.from_user.id)]
        d.close()
    except NotADirectoryError:
        os.mkdir('log')
        try:
            d = shelve.open('log' + '/' + 'log')
            dis = d[str(message.from_user.id)]
            d.close()
        except:
            dis = 'none'
    except:
        dis = 'none'
    if dis == 'get':
        file_name = message.text
        try:
            with shelve.open(str(message.from_user.id) + '/' + current_directory[message.from_user.id][-1]) as reader:
                bot.forward_message(message.from_user.id, chat_id, reader[file_name])
        except:
            os.mkdir(str(message.from_user.id))
            with shelve.open(str(message.from_user.id) + '/' + current_directory[message.from_user.id][-1]) as reader:
                bot.forward_message(message.from_user.id, chat_id, reader[file_name])
    elif dis == 'open_directory':
        if message.text == '<=back' and current_directory[message.from_user.id] != [str(message.from_user.id)]:
            current_directory[message.from_user.id] = \
                current_directory[message.from_user.id][:len(current_directory[message.from_user.id]) - 1]
            create_keyboard(message)
        else:
            if os.path.isdir('/'.join(current_directory[message.from_user.id]) + '/' + message.text):
                current_directory[message.from_user.id] += [message.text]
                create_keyboard(message)
            else:
                try:
                    with shelve.open('/'.join(current_directory[message.from_user.id]) +
                                     '/' + current_directory[message.from_user.id][-1]) as reader:
                        bot.forward_message(message.from_user.id, chat_id, reader[message.text])
                except:
                    bot.send_message(message.from_user.id, 'seems like this directory does not exist')
    elif dis == 'folder':
        if current_directory == starting_dir:
            current_directory[message.from_user.id] += [str(message.from_user.id)]
        try:
            try:
                os.mkdir('/'.join(current_directory[message.from_user.id]) + '/' + message.text)
            except:
                bot.send_message(message.from_user.id, 'this directory already exists')
            create_keyboard(message)
        except NameError:
            bot.send_message(message.from_user.id, 'wrong name')
    elif dis == 'name':
        file_name = message.text + '(media)'
        with shelve.open('/'.join(current_directory[message.from_user.id]) + '/'
                         + current_directory[message.from_user.id][-1]) as writer:
            writer[str(file_name)] = msg_id
        bot.delete_message(message.from_user.id, doc_id)
        bot.send_message(message.from_user.id, 'done.')
        create_keyboard(message)


try:
    bot.polling()
except:
    print('oops')
