import vk_api
from vk_api.audio import VkAudio
a1 = "SGJ8tjrpoNS2foo4ks3L"
a2 = "611aa434611aa434611aa434996163c8b46611a611aa4340050878cda82d350694c1a9b"

def searcher(text):
    vk_session = vk_api.VkApi(app_id=7957632, client_secret=a1)
    vk_session.server_auth()
    vkaudio = VkAudio(vk_session)
    tracks = vkaudio.search(text, count=1)
    print(tracks)

searcher("лсп тело")