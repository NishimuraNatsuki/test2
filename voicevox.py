import requests
import json
import sounddevice as sd
import numpy as np


host = '127.0.0.1'
port = "50021"
speaker = 3

# 音声合成用のクエリを作成する
def post_audio_query(text:str) -> dict:
    params = {"text":text, "speaker":speaker}
    
    res = requests.post(
        f"http://{host}:{port}/audio_query",
        params=params,
    )
    
    query_data = res.json()
    
    return query_data

# クエリを元に音声合成を実行する関数
def post_synthesis(query_data:dict) -> bytes:
    params = {"speaker" : speaker}
    headers = {"content-type":"application/json"}
    
    res = requests.post(
        f"http://{host}:{port}/synthesis",
        data=json.dumps(query_data),
        params=params,
        headers=headers,
    )
    
    return res.content

# VOICEVOXで合成した音声を再生するための関数
def play_wavefile(wav_data:bytes):
    sample_rate = 24000 #サンプリングレート
    wav_array = np.frombuffer(wav_data,dtype=np.int16)#バイトデータをnumpy配列に格納
    sd.play(wav_array,sample_rate,blocking=True)#音声の再生

#  
def text_to_voice(text):
    res = post_audio_query(text)
    wav = post_synthesis(res)
    play_wavefile(wav)
        
if __name__ == "__main__":
    text_to_voice()
    