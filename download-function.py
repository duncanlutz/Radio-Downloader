import time
import urllib3
import os
from random import choice
from string import ascii_letters
from datetime import date
from google.cloud import storage
from google.oauth2 import service_account
from moviepy.editor import AudioFileClip, ImageClip

os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"

gcp_json_credentials_dict = {
    "type": "service_account",
    "project_id": "lll-radio",
    "private_key_id": "7148afe61cade903fc89957bcdd59beae960164e",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQC64OpstkElQNn8\nOvJmTCan5HLXxXS0OVVAI+/uO+T9iRkX22/OghzRdRfVDeGjNd9d4kh9UEr42qKR\nvmXC3IPhJIbArncBQa7NiDAzZhLaFc6NWfeMCO3E6h4rXFXVyrnj/QlXmgdEx58r\np4Uy/eQXbLXEsq2nZj62hBAgjpUvTcG26f/DqKHNvmt9J2Z/GREbICvaa1Z941aO\ncv4Hc9xeRU/82GNB6eAWtTn6GEKgUzitGPKkMhg+DQa6PZMX4B1nOy3hZSJe6UqY\nkerqGPzf92/uNZBc8nZXk23ZRjA7dPwp/Tdz2dSvv7/1vn3qerp2Mainjwss1ykS\nBUv/xkE1AgMBAAECggEAJOmiRGDnk0UxCYpXMO+fvw/3wzkEaUjd1vKCROtdutqm\nszir5/15VcIsN/Aq/oL4oOG+cco3VNpSvDkAfrHx9rmxSEPty7i+n2hkJPLnjF48\nU11O8UEePgQEe4ochkMp3qevfbc18lb/0K6hN8ZAlIPrj3O/q04d2w1Q5i1juFjs\nGkl/npc32VaK3W8B2XjCaAB2xtrzBOFk8C9yG0F34BWRyS8c6zjFsYX9Ivp1CUNE\nYVPf5GZYszWLtiu8Sa7GjoNRvXIDzO2HEQ05+1Z3MNCV3Q+HIL2GDsv9qfYP7REQ\nkjHKhSZ4yLN1r4UWbl9bT0Klv4rCVzv7ahfcQPCPAQKBgQDfYEcx33jkuK1MWlpa\nj8EryDj4o2n017zJqnbq2QUphBgquJKhciom5BoSFZMvJXGbTWnLjkbbIfhUx7IK\nZTxDCKxE6ee8dDXMQCr3/zxR+5Ak2tBAxLYzlAy9yv9BA31fpDUq8sl9ht6Tn7j0\n6FRsDs0q2MXhENbXdNLum4CXdQKBgQDWLAvgOM+jcQ6WFsKKPA/k1Yu4hLXrNs29\ncur2gxoODFHF84yIg47l8eK2R8OCMQMVL0R/GmIwcSwIRnIXzuse8l3IEG6j73Xu\nWFE25WUcf+gKjcMBeWlaoIWNJvFx9H3lv3X24+JxFSNqQUf2slaGwNICt+UcOg3p\nbsbvUpOKwQKBgQDPHxbkx7HxYsxN3/mnv2P+lMk+w0ecH+6Nj+J0IIcI19MQydQs\nnw82wIrr+dVgAfg1aLKQbHyG9Bivg/syaGxYO9KAk+Kse5TmrxkomyHzYq9lfP9d\nDwljCgRGd9P3FKVL6ZbjG/x4yHXZrGBztnmROKhE8nuJFXQgk9KCLO4vgQKBgQCt\nLcaYkzeKwIN754F9B54OeoJVPLJhNNpeI0tM86ugymNg/lOXm1F0LAgXPqYfYwRM\nIAFyCWJ2KzzgoB3nlIBYcMBWYrskQiAJD070Zb9BsUdvKTwSuBrxljUHcwLvEzSu\nDwgTECftKpuNcqX/HCuNIONwIUTYczUGmXWw1QPKwQKBgQCTEYWryST2KN8ru0B+\nyWuyanBdKJQzk+22qSwi0+Na70r3n1jbvT9Pk2Trb8o5J52W6Gs9739wp1GWG/Qu\niENic/Iy7XprcAkEi8EKtijBdZn9udh+QW93Odi7SyQX/ws8riFf7F4SZOkiebrF\n4NqBfB1Dp7GQopVQmvZy3LZ7eA==\n-----END PRIVATE KEY-----\n",
    "client_email": "media-451@lll-radio.iam.gserviceaccount.com",
    "client_id": "100947444195919711951",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/media-451%40lll-radio.iam.gserviceaccount.com"
}

credentials = service_account.Credentials.from_service_account_info(
    gcp_json_credentials_dict)

storage_client = storage.Client(
    project=gcp_json_credentials_dict['project_id'], credentials=credentials)


def upload_file(bucket_name, source_file_name, destination_blob_name):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob._get_download_url
    blob.upload_from_filename(source_file_name)


def get_image_file(bucket_name, file_name):
    bucket = storage_client.bucket(bucket_name)
    final_file_name = file_name.join(choice(
        ascii_letters) for i in range(10))
    blob = bucket.blob("Assets/Show_art.png")
    read_file = blob.download_as_bytes()
    file = open('/tmp/' + final_file_name + '.png', 'xb')
    file.write(read_file)
    file.close()
    global image_path
    image_path = "/tmp/" + final_file_name + ".png"
    return image_path


def create_video(bucket_name, audio_path, output_path):
    image = get_image_file(bucket_name, "show_art")
    audio_clip = AudioFileClip(audio_path)
    image_clip = ImageClip(image)
    video_clip = image_clip.set_audio(audio_clip)
    video_clip.duration = audio_clip.duration
    video_clip.fps = 1
    video_clip.write_videofile(output_path)
    global video_path
    video_path = output_path


def run_download():
    url = "https://live.wostreaming.net/direct/alphacorporate-kdutfmaac-ibc4?source=TuneIn&gdpr=0&us_privacy=1YNY"
    print("Connecting to "+url)

    con = urllib3.PoolManager()
    response = con.request("GET", url, preload_content=False)
    name_string = "el_show_de_el_potro-" + date.today().strftime("%b-%d-%Y")
    fname = name_string + ".wav"
    f = open("/tmp/"+fname, 'wb')
    block_size = 1024
    t_end = time.time() + 3
    while time.time() < t_end:
        try:
            audio = response.read(block_size)
            if not audio:
                break
            f.write(audio)

            print(".")

        except Exception as e:
            print("Error "+str(e))

    response.release_conn()
    f.close()
    global audio_path
    audio_path = "/tmp/" + fname
    create_video("lll-radio-bucket", "/tmp/"+fname,
                 "/tmp/" + name_string + ".mp4")
    upload_file("lll-radio-bucket", "/tmp/" +
                name_string + ".mp4", name_string + ".mp4")

    print("")
    print("File uploaded to Google Cloud")
    os.remove(audio_path)
    os.remove(video_path)
    os.remove(image_path)
    
run_download()