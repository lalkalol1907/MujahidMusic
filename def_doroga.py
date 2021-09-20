import vk_api
from vk_api.audio import VkAudio


def searcher(text):

    login, password = 'login', 'password'
    vk_session = vk_api.VkApi(login, password)

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    vkaudio = VkAudio(vk_session)
    tracks = vkaudio.search(text, count=1)
    for n, track in enumerate(tracks, 1):
        print('{}. {} {}'.format(n, track['title'], track['url']))

    return track['url']



searcher("лсп тело")