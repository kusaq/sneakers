import vk
from time import sleep

def ask_yorn(text):
    answer = ''
    while answer != 'y' and answer != 'n':
        answer = input(text + '(y/n) : ')
    return answer
print('[WARNING] You should have file with spam text in "text.txt" and blacklist of ids in "bl.txt" at the same directory')

login = input('login : ')
passw = input('password : ')
ban_mode = ask_yorn('Should we enter ban mode?')

if ban_mode == 'n':
    mode_type = ask_yorn('Should we enter manual mode?')

textfile = open('text.txt', 'r')
messagetext = textfile.read()
textfile.close()

vk_api = vk.API(vk.AuthSession('6728603', login, passw, "messages, friends"))
vk_v = '5.37'
vk_me = vk_api.users.get(v=vk_v)[0]['id']

for friend in vk_api.friends.get(v = vk_v, user_id = vk_me)['items']:
    if ban_mode == 'n':
        blfile = open('bl.txt', 'r')
        blacklist = [int(x.strip()) for x in blfile]
        if friend not in blacklist:
            cur_friend = vk_api.users.get(v='5.37', user_id = friend)[0]
            if mode_type == 'y':
                user_answer = ask_yorn('Send message to ' + cur_friend['first_name'] + ' ' + cur_friend['last_name'] + ' ?')
                if user_answer == 'y':
                    vk_api.messages.send(v=vk_v, user_id = friend, message = messagetext)
                sleep(2.8)
            elif mode_type == 'n':
                vk_api.messages.send(v=vk_v, user_id = friend, message = messagetext)
                print('Message sent to', cur_friend['first_name'], cur_friend['last_name'])
                sleep(5)
    else:
        blfile = open('bl.txt', 'a')
        cur_friend = vk_api.users.get(v='5.37', user_id = friend)[0]
        user_answer = ask_yorn('Add ' + cur_friend['first_name'] + ' ' + cur_friend['last_name'] + ' to blacklist?')
        if user_answer == 'y':
            blfile.write(str(friend) + '\n')

blfile.close()
