import requests

# with open("mv2.mp4", "rb") as file:
#     res = requests.post("http://192.168.50.63:4995/upload", files={"file": file}, data={"name": "cheat.mp4"})
#
#     print(res.text)

# for i in range(1):
#     res = requests.post("http://192.168.50.205:5000/delete", data={"name": "cheat" + str(i) + ".mp4"})
#     print(res.text)

res = requests.post("http://10.10.3.2:5000/cdn",
                    data={"name": "mv.mp4", "lat": 100, "lng": 100, "dur": 5})
print(res.text)