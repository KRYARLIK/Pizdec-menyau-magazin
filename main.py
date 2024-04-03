from fastapi import FastAPI
import uuid
import base64
import requests as rq
import numpy as np
import psycopg2 as pg2

url = "" # url для подключения к сервису распознавания

conn = pg2.connect(database="sample_db", user="postgres",
                    password="sample_pwd", host="sample_url", port="sample_port")
cursor = conn.cursor()

api = FastAPI()

@api.post("/upload_image")
def upload_image(img, user_id = "1"): # user_id == "1" -> guest
    img = open(img, 'rb')
    np_img = np.array(img)
    b64 = base64.encode(np_img.read())
    data = {"image_data": b64, "image_id": uuid.uuid4(), "user_id": user_id}
    response = rq.Request('POST', url=url, data=data, headers = {"Content-Type": "application/json"})
    return response.text


@api.get("/get_saved_data")
def get_saved_data(user_id = "0", cursor=cursor): # user_id == "0" -> demo
    data = cursor.execute(f'''SELECT * FROM image_data WHERE ID = {user_id};''')
    return data


@api.post("/save_data")
def save_data(data:str, user_id = "1", cursor=cursor):
    data_list = data.split(",")
    cursor.execute(f'''INSERT INTO image_data(user_id, image_id, image_data) VALUES({data_list[2]}, {data_list[1]}, {data_list[0]})''')
