#_*_encoding:utf-8_*_
import time
import hashlib
import requests
import json


appKey = "168932340900019b"
secretKey = "2574faba477fb1ee5980c27e22195196"

baseURL = "https://api.speechsuper.com/"

timestamp = str(int(time.time()))

coreType = "sent.eval.cn" # Change the coreType according to your needs.
refText = "绿 是 阳春 烟 景 大块 文章 的 底色 四月 的 林 峦 更是 绿 得 鲜活 秀媚 诗意 盎然" # Change the reference text according to your needs.
slack = 1
audioPath = "A2_0.wav" # Change the audio path corresponding to the reference text.

# y, s = librosa.load(audioPath, sr=16000)
# sf.write("output.wav", y, 16000)
# audioPath = "output.wav"

audioType = "wav" # Change the audio type corresponding to the audio file.
audioSampleRate = 16000
userId = "guest"

url = baseURL + coreType
connectStr = (appKey + timestamp + secretKey).encode("utf-8")
connectSig = hashlib.sha1(connectStr).hexdigest()
startStr = (appKey + timestamp + userId + secretKey).encode("utf-8")
startSig = hashlib.sha1(startStr).hexdigest()

params={
	"connect":{
		"cmd":"connect",
		"param":{
			"sdk":{
				"version":16777472,
				"source":9,
				"protocol":2
			},
			"app":{
				"applicationId":appKey,
				"sig":connectSig,
				"timestamp":timestamp
			}
		}
	},
	"start":{
		"cmd":"start",
		"param":{
			"app":{
				"userId":userId,
				"applicationId":appKey,
				"timestamp":timestamp,
				"sig":startSig
			},
			"audio":{
				"audioType":audioType,
				"channel":1,
				"sampleBytes":2,
				"sampleRate":audioSampleRate
			},
			"request":{
				"coreType":coreType,
				"refText":refText,
				"tokenId":"tokenId",
				"slack":slack
			}

		}
	}
}

datas=json.dumps(params)
data={'text':datas}
headers={"Request-Index":"0"}
files={"audio":open(audioPath,'rb')}
res=requests.post(url, data=data, headers=headers, files=files)
print(res.text.encode('utf-8', 'ignore').decode('utf-8'))
