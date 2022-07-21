import time
import urllib3
import os
import json
import base64
from random import choice
from string import ascii_letters
from datetime import date
from google.cloud import storage
from google.oauth2 import service_account
from moviepy.editor import AudioFileClip, ImageClip

os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"

cred = 'eyAidHlwZSI6ICJzZXJ2aWNlX2FjY291bnQiLCAicHJvamVjdF9pZCI6ICJsbGwtcmFkaW8iLCAicHJpdmF0ZV9rZXlfaWQiOiAiMTJmNzZhYmRhZDg4ZjIzMjc2Mjg0ZjE3MDZjNTY0ZDAyMTBmM2M1MyIsICJwcml2YXRlX2tleSI6ICItLS0tLUJFR0lOIFBSSVZBVEUgS0VZLS0tLS0KTUlJRXZRSUJBREFOQmdrcWhraUc5dzBCQVFFRkFBU0NCS2N3Z2dTakFnRUFBb0lCQVFDcTc2UGl2ZlJvSHB1MwpEMXcwdDFoSGx2cEl0b3ArVXlQMis0a3pqRS81VmszV0R1MWVua1puMnFtWGF5SFV2M0RHNXFMSnY5dUxqaEl5CjNqanAxb1lVR3BIdm14ZlZDSDYyenMvaHpVbGRZdmhwdFZmdjJKemlFNk1qZFI4cHpIaFJtc05jN25jNnRFMVIKV0duNlhNRFpYMi9rRUlxVTdxTDVvZ3ovQzVMTzR6Skhjd0N6Qzg5MnE3TngzZWVVNE53ZklWSlk4dkxrb2w1ZwpLUW1pN29FTU90eXZMNElCRUZCR0o5cEp4ODJEVjBjaE82L0JLWHJYUUVYT1hzdU8yNzVxNjNIZ01zSGQ4UGxZCklydU95dlF1Y2xvR1RldStOTTBkYlhTZngwMnp3V3RoSjhONkVWM1c2T255cW1kVVJMcHpvN1l4bE9WUC9QVSsKSTFJZFNJdWJBZ01CQUFFQ2dnRUFGbCtiY2RndkgxbXlRL21zdGZHeGlsMUdrVEhqV3JtRElaYTIxSnB1OVZISQppbFlWMTZhYnpJZ2dYb05WUUVWMmUzSkFxR3VHVHZQZmllendRaHNrSFltRXhIbm1XcW5yKy8yQjFDcE1pZjZrClNTSEZTczF0YTJIcW5uOTcvcnFXblFmR3Zta3dEZXovbWNBYXp2eEkrYXEyT0lHNXdkaWlXRTVQcVNwWW90OS8KTlBpLzM2YUhXN2lrQU1BQU9hTEo0cy8rSTVaT2JpTmhnOEJsR05idCtSTGpPL3hsM1RQUnRrOGJra2ZoRlFqZQp6VGJBN1dvN2MrZC9qRzQwMTcyeFhmdnFVN1czZjAxTDA3U0pFSXJ6dFVaZnRxY0JtTTJmU1h6Tkh0NWwxWG43CkZZUy9vQ3ExY0E1M3BhUnBWWFdIRVhaRlFRZG9pYm9XS3VhUUJ5Smw4UUtCZ1FEVjJia3V1TkxGVkVIUExFajEKcmZTRDhvR2xMUkVPRUgrUjZuOVdwWEhRVWkrNEppeW00S0NGTjNLdVlrbFBsM3VCZFBqQ2xEc1BRTy81Nk5YWgpCT0VRUHhvL1UzRE5HTkIvTU5EekRFcWs1ZUt1WTY3QjhjT0E0MDZMOG9XYjdBQWQ5RVhEeld2cmsrNU9oNXVoCmdiTEhYMzVSMldwczEzdm5BY1JtUEVPV1h3S0JnUURNb0pTNm9LM3YrOXNDQTYvR2RkZytkZnUrK0ltczFCVDIKSmI1eDlCMkdLMTFTeEZvQkdaVUN6VVFCNXdoeTZWcGYxK2dFb0xETCtvQXVwdDdNd2lFV0NZU3JNSW4rSzVZMQpBV2d6Nmt3aW9WKzJPcC9mUVNlelJqd1Q5Y3FZeG1OSEhRYWMzVGpUcGg5eGRGNENPdkFlNjJZdytXd0ZQV1VRCnRwYlNLYVY4UlFLQmdEakpieVpjQ0FSRWdwRThKa2V2SU40aytJNWZNRWMyMUZsd0ZzNXdjbytxTTJmSUkxVlIKRXU4dE1UUGpmNm8yQktMMDU5WHJ2TjhwRkZDZHBxUFJhdDZBa3p5N3NKbVYvRSs2SzlKT3NrZWxrQk5VL3lRYgpTaG9nd2t2aFk5OXF4UUV2UzVOYUtrMU5aQnZRWU9CN2Eza0wvNlJHZ3I5U1hXR1RrNDYrZEFnckFvR0FCazBECmgyT2ZOMzZIMWQ0TE1ZODdZMkQ2cVh5NXNJcXZRbzBTK2l0TUpXOThaaW9KbzNNSU5aZmdlamFFK2hUWlpZNGUKWk5ZVjI1SVJGRjZyQ1o4SXFjY05RTUF6MzVHMEJGblF2WmgvVTZtb2F0SVBUaTZSYkdIRFE5SVR0UFNXNWYrcwp6bk81WmpyOVNOOE9iZjhtbWEwaDdtd2Z1V0dVbFJrcU43cDBrQWtDZ1lFQXhrTENBR1NPa2dIRGp6MGFKa2NLCnZQdDE0TnVoMFl3U1hxNnR0MTVQcmx1dWdraFZFeEFKSXJYdDBqZHdRblNVb2xsa0ZTQUdoQmFmdXVxdTQ1QzQKMWtqbDdidU1nYlBJdVQ1YVgxRDU0eVlIY2J1a2U4dlZJdFRMRVhtZWo1amwzY0JPVmFQdHQ3U1dnd0VYSkRFcQo5aVBVUFViN1pTc2JkR2hnSWRyTGxrRT0KLS0tLS1FTkQgUFJJVkFURSBLRVktLS0tLQoiLCAiY2xpZW50X2VtYWlsIjogIm1lZGlhLTQ1MEBsbGwtcmFkaW8uaWFtLmdzZXJ2aWNlYWNjb3VudC5jb20iLCAiY2xpZW50X2lkIjogIjEwOTI4NDU4ODg5MDQ2MTMyOTE4MSIsICJhdXRoX3VyaSI6ICJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20vby9vYXV0aDIvYXV0aCIsICJ0b2tlbl91cmkiOiAiaHR0cHM6Ly9vYXV0aDIuZ29vZ2xlYXBpcy5jb20vdG9rZW4iLCAiYXV0aF9wcm92aWRlcl94NTA5X2NlcnRfdXJsIjogImh0dHBzOi8vd3d3Lmdvb2dsZWFwaXMuY29tL29hdXRoMi92MS9jZXJ0cyIsICJjbGllbnRfeDUwOV9jZXJ0X3VybCI6ICJodHRwczovL3d3dy5nb29nbGVhcGlzLmNvbS9yb2JvdC92MS9tZXRhZGF0YS94NTA5L21lZGlhLTQ1MCU0MGxsbC1yYWRpby5pYW0uZ3NlcnZpY2VhY2NvdW50LmNvbSJ9'
gcp_json_credentials_dict = json.loads(base64.b64decode(cred.encode('ascii')).decode('ascii'), strict=False)

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