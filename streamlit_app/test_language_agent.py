import requests

url = "http://127.0.0.1:8003/summarize/"
data = {
    "answers": [
        "Today, Asia tech stocks rose by 3.2% led by gains in TSMC and Samsung Electronics.",
        "The overall AUM allocation in Asia tech now stands at 22%, up from 18% yesterday.",
        "TSMC reported quarterly earnings beating analyst expectations by 4%, while Samsung missed by 2%.",
        "Global investor sentiment remains cautious due to rising bond yields in the US."
    ]
}

response = requests.post(url, json=data)
print(response.json())
