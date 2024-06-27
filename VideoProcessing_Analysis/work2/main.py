'''
Copyright (c) 2024 by Huanxuan Liao, huanxuanliao@gmail.com, All Rights Reserved. 
Author: Xnhyacinth, Xnhyacinth@qq.com
Date: 2024-06-04 09:01:41
'''


from openai import OpenAI
import base64
import json
API_BASE = ""
API_KEY = ""

client = OpenAI(
    api_key=API_KEY,
    base_url=API_BASE
)
q = '''
你是一个专业的心理专家，沙盘图像描述是指根据来访者所摆放出的沙盘图像信息，结合特定的心理知识得到关于沙盘场景的描述。下面给你提供沙盘图像，请你给出你的分析。\n示例:第一张图片。\n分析：从箱庭作品中可以看到小Z内心的渴望。
（1）制作过程：小Z刚开始制作箱庭时心不在焉，会打扰别人制作箱庭，最后才慢慢安静下来。
（2）玩具选择与摆放：小Z的箱庭 右上角是海水，其他地方是大陆。水代表包容和无意识，在陆水交界处有一座桥，说明小Z渴望与人沟通。水中有山，栅栏，塔和鱼，整个布局没有规律可循，反映了小Z的内心世界很混乱，有很多压抑的情感需要被释放。
\n问题：第二张图片。\n分析：
'''
q = '''
你是一位专业的心理专家，沙盘图像描述是指根据来访者所摆放出的沙盘图像信息，结合特定的心理知识得到关于沙盘场景的描述。下面给你提供沙盘图像，请你给出详细分析,需要给出对图片的描述，展现的心理状态以及反映的心理问题等。请尽可能的详细，准确，有效。最后需要总结其反映的心理问题。\n
'''

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
outputs = []
for i in range(1):
  i = 2
  image_path = "work2/dataset/train/"
  image_path += str(i) + '/BireView.png'

  # Getting the base64 string
  base64_image = encode_image(image_path)
  print(i)
  print(image_path)
  try:
    completion = client.chat.completions.create(
        model="glm-4v",
        messages=[
          {
            "role": "user",
            "content": [
              {
                "type": "text",
                "text": q
              },
              {
                "type": "image_url",
                "image_url": {
                    "url" : f"{base64_image}" #data:image/png;base64,
                }
              }
            ]
          }
        ]
    )
    res = completion.choices[0].message.content.strip()
  except:
    res = 'fail'
  output = {'res': res,
            'id': i}
  outputs.append(output)

with open ('work2/results11.json', 'a', encoding='utf-8') as f:
  json.dump(outputs, f, indent=4, ensure_ascii=False)
