from pyrogram import Client
from pyrogram.types import Message,ReplyKeyboardMarkup,InlineKeyboardButton,ReplyKeyboardRemove,InlineKeyboardMarkup,CallbackQuery,InlineQuery,InlineQueryResultArticle,InputTextMessageContent

client = Client(session_name=''
                ,bot_token=''
                ,api_id=0
                ,api_hash='')

def IKM(data):
    return InlineKeyboardMarkup([[InlineKeyboardButton(text,cbd)] for text,cbd in data])


def IKM2d(data):
    return InlineKeyboardMarkup([[InlineKeyboardButton(text,cbd) for text,cbd in row] for row in data])


def check(move_list):
    #row
    for i in range(3):
        if move_list[i][0][0]==move_list[i][1][0] ==move_list[i][2][0] and (move_list[i][0][0]=='❌' or move_list[i][0][0]=='⭕️'):
            if move_list[i][0][0]=='❌':
                return 'the player ❌ won!'
            return 'user_2: ⭕️ '
    #column
    for j in range(3):
        if move_list[0][j][0] == move_list[1][j][0] == move_list[2][j][0]  and (move_list[0][j][0]=='❌' or move_list[0][j][0]=='⭕️'):
            if move_list[0][j][0] == '❌':
                return 'player ❌ won!'
            return 'player ⭕️ won!'
    #diagonal
    if move_list[0][0][0] == move_list[1][1][0] == move_list[2][2][0] and (move_list[0][0][0]=='❌' or move_list[0][0][0]=='⭕️'):
        if move_list[0][0][0] == '❌':
            return 'player ❌ won!'
        return 'player ⭕️ won!'

    if move_list[0][2][0] == move_list[1][1][0] == move_list[2][0][0] and (move_list[0][2][0]=='❌' or move_list[0][2][0]=='⭕️'):
        if move_list[0][2][0] == '❌':
            return 'player ❌ won!'
        return 'player ⭕️ won!'
    return

shoro=IKM([('start','start')])
table=IKM2d([[(' ','0'),(' ','1'),(' ','2')],[(' ','3'),(' ','4'),(' ','5')],[(' ','6'),(' ','7'),(' ','8')]])

player_dict={}
player_list=[]
move_list=[[[' ','0'],[' ','1'],[' ','2']],[[' ','3'],[' ','4'],[' ','5']],[[' ','6'],[' ','7'],[' ','8']]]
turn=0
used_cell=[]


@client.on_inline_query()
def handel_inline_query(bot:client,query:InlineQuery):

    global player_dict
    global player_list
    global turn

    results=[InlineQueryResultArticle('❌⭕️ game!', InputTextMessageContent('waiting for second player...'),reply_markup=shoro)]
    bot.answer_inline_query(query.id, results)
    
    player_dict = {}
    player_list = []
    turn=0
    player_dict[query.from_user.id]='❌'
    player_list+=[query.from_user.id]
    turn=player_list[0]


@client.on_callback_query()
def handel_callback_query(bot=client,query=CallbackQuery):

    global player_dict
    global player_list
    global move_list
    global turn
    global used_cell

    if query.from_user.id not in player_list:
        if query.data=='start':
            bot.edit_inline_text(query.inline_message_id,'the game was started!',reply_markup=table)
            
            move_list = [[[' ', '0'], [' ', '1'], [' ', '2']],
                         [[' ', '3'], [' ', '4'], [' ', '5']],
                         [[' ', '6'], [' ', '7'], [' ', '8']]]
            used_cell = []
            player_dict[query.from_user.id]='⭕️'
            player_list+=[query.from_user.id]

    elif turn==query.from_user.id and query.data not in used_cell and query.data!='start':
        move_list[int(query.data)//3][int(query.data)-(int(query.data)//3)*3][0]=player_dict[query.from_user.id]
        used_cell += [query.data]
        bot.edit_inline_text(query.inline_message_id, 'the game was started!', reply_markup=IKM2d(move_list))
        if turn==player_list[0]:
            turn=player_list[1]
        elif turn==player_list[1]:
            turn = player_list[0]
        barande = check(move_list)
        if barande:
            bot.edit_inline_text(query.inline_message_id, barande)
        elif len(used_cell)==9:
            bot.edit_inline_text(query.inline_message_id, 'Draw!')


client.run()