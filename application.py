# coding=UTF-8
from flask import Flask, jsonify, request
import base64
import datetime
import json
import random,string
import numpy as np
from firebase import firebase
import face_recognition as face_recognition
import face_recognition_models

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
fb = firebase.FirebaseApplication('https://voice-kit-v2-demo.firebaseio.com', None)
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'enter api system'


@app.route('/face_id', methods=['POST'])
def api_article1():
    json_data = open('data.json').read()
    data = json.loads(json_data)

    known_face_encodings = []
    known_face_names = []

    print('Start getting data:')
    start_time = datetime.datetime.now()
    for item in data['people']:
        for face_code in item['infos'][0]['face_image']:
            known_face_names.append(item['infos'][0]['label'])
            for code in face_code['face_embedding_code']:
                known_face_encodings.append(code)
    print("Finish...")
    print("Total time:",datetime.datetime.now()-start_time)
    print("Avg :", (datetime.datetime.now() - start_time)/len(known_face_encodings))


    print(known_face_names)
    known_face_encodings = np.array(known_face_encodings)
    fb = firebase.FirebaseApplication('https://voice-kit-v2-demo.firebaseio.com', None)

    text = request.json['text']
    voice_kit_id = request.json['vocie_kit_id']
    vision_kit_id = request.json['vision_kit_id']

    fh = open("face.jpeg", "wb")
    fh.write(base64.decodebytes(bytes(text, 'utf-8')))
    fh.close()

    print("Start:", datetime.datetime.now())
    face_image = face_recognition.load_image_file("face.jpeg")
    face_encodings = face_recognition.face_encodings(face_image)
    name = "Unknown"

    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        print("Start compare:",datetime.datetime.now())
        start_time = datetime.datetime.now()
        match = face_recognition.compare_faces(known_face_encodings, face_encoding)
        print("Finish compare,total time:", datetime.datetime.now()-start_time)
        print(match)
        if True in match:
            first_match_index = match.index(True)
            name = known_face_names[first_match_index]
            #name = known_face_names[first_match_index]
            print("Identify user successful: {}!".format(name))

            result = fb.get('/vision_kit', vision_kit_id)
            result["user"] = name
            result = fb.put('/vision_kit', vision_kit_id, result)
            print("Update:", datetime.datetime.now())

            result = fb.get('/voice_kit', voice_kit_id)
            result["status"] = True
            result = fb.put('/voice_kit', voice_kit_id, result)

            return "Identify user successful: {}!".format(name)

    result = fb.get('/voice_kit', voice_kit_id)
    result["status"] = True
    result = fb.put('/voice_kit', voice_kit_id, result)
    print("Finish:", datetime.datetime.now())
    return "New user"


@app.route('/insert_new_user', methods=['POST'])
def api_article2():
    user_image = request.files['image']
    user_label = request.form['label']
    json_data = open('data.json').read()
    data = json.loads(json_data)

    try:
        if str(user_image.filename).split(".")[1].lower() in ALLOWED_EXTENSIONS:
            user_image.save("face.jpeg")

            print("Start:", datetime.datetime.now())
            with open("face.jpeg", "rb") as imageFile:
                image_str = base64.b64encode(imageFile.read()).decode('utf-8')

            face_image = face_recognition.load_image_file("face.jpeg")
            face_embedding_code = face_recognition.face_encodings(face_image)
            print(user_label.encode("utf-8"))
            label = user_label.encode("utf-8")
            print(label.decode("utf-8"))
            label = label.decode("utf-8")
            user_id = label+"_"+''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            user_infos = {
                "user_id":user_id,
                "infos":[
                    {
                        "label":label,
                        "face_image":[]
                    }
                ]
            }
            face_detail = {
                "image_label":user_image.filename,
                "image_str":image_str,
                "face_embedding_code":np.array(face_embedding_code).tolist()
            }
            user_infos['infos'][0]['face_image'].append(face_detail)
            data['people'].append(user_infos)
            result = insert_new_user_db(user_id,label,image_str)

            if result is True:
                print(data)
                with open('data.json', 'w') as outfile:
                    json.dump(data, outfile)
                    result = {
                        'status': 'success'
                    }
                print("Finish...", datetime.datetime.now())
        else:
            result = {
                'status': 'fail',
                'exception': 'Wrong type of image, only support'
            }
        return jsonify(result)
    except Exception as ex:
        result = {
            'status': 'fail',
            'exception': str(ex)
        }
    return jsonify(result)


@app.route('/insert_exist_user', methods=['POST'])
def api_article3():
    json_data = open('data.json').read()
    data = json.loads(json_data)

    user_id = request.form['user_id']
    user_image = request.files['image']
    if str(user_image.filename).split(".")[1].lower() in ALLOWED_EXTENSIONS:
        user_image.save("face.jpeg")
    with open("face.jpeg", "rb") as imageFile:
        image_str = base64.b64encode(imageFile.read()).decode('utf-8')

    face_image = face_recognition.load_image_file("face.jpeg")
    face_embedding_code = face_recognition.face_encodings(face_image)

    for item in data['people']:
        if item['user_id'] == user_id:
            image = {
                'image_label':user_image.filename,
                'image_str':image_str,
                'face_embedding_code':np.array(face_embedding_code).tolist()
            }
            item['infos'][0]['face_image'].append(image)

    result = get_user_db()
    if result is not None:
        for items in result:
            item = result[items]
            if item['user_id'] == user_id:
                item['user_image'].append(image_str)
                result = insert_exist_user(item,items)
                if result is True:
                    with open('data.json', 'w') as outfile:
                        json.dump(data, outfile)
                    result = {
                        'status':True
                    }
                else:
                    result = {
                        'status': False
                    }
    else:
        result ={
            'status':False,
            'exception':'Null request'
        }
    return jsonify(result)


@app.route('/list_all_user', methods=['GET'])
def api_article4():
    result = get_user_db()
    if result is not None:
        res_result = {
            'status':True,
            'user_detail':[]
        }
        for items in result:
            item = result[items]
            res_result['user_detail'].append(
                {
                    'user_id': item['user_id'],
                    'user_label': item['user_label']
                }
            )
    else:
        res_result ={
            'status':False,
            'exception':'Null request'
        }
    return jsonify(res_result)


@app.route('/delete_user', methods=['POST'])
def api_article5():
    json_data = open('data.json').read()
    data = json.loads(json_data)

    new_data = {"people":[]}
    user_id = request.json['user_id']
    for items in data['people']:
        if items['user_id'] != user_id:
            new_data['people'].append(items)

    result = get_user_db()

    if result is not None:
        res_result = {
            'status':True,
        }
        for items in result:
            item = result[items]
            if item['user_id'] == user_id:
                print(items)
                delete_user_db(items)
                data = new_data
                with open('data.json', 'w') as outfile:
                    json.dump(data, outfile)
    else:
        res_result ={
            'status':False,
            'exception':'Null request'
        }
    return jsonify(res_result)


@app.route('/delete_image', methods=['POST'])
def api_article6():
    image_str = ""
    user_id = request.json["user_id"]
    image_label = request.json["image_label"]
    json_data = open('data.json').read()
    data = json.loads(json_data)

    new_data = {
        "people": []
    }

    result = get_user_db()

    for items in data['people']:
        new_item = {
            "user_id": items['user_id'],
            "infos": [
                {
                    "label": items['infos'][0]["label"],
                    "face_image": []
                }
            ]
        }
        print(new_item)
        for item in items['infos'][0]["face_image"]:
            if item["image_label"] != image_label:
                print("image_label:",item["image_label"])
                new_item["infos"][0]["face_image"].append(item)
            else:
                image_str = item["image_str"]

        new_data["people"].append(new_item)

    for items in result:
        id = items
        if result[items]["user_id"] == user_id:
            new_result = {
                'user_id': user_id,
                'user_label': result[items]["user_label"],
                'user_image': []
            }
            for item in result[items]["user_image"]:
                if item == image_str:
                    print("found")
                else:
                    print(item)
                    new_result["user_image"].append(item)
            print(new_result)
            update_user(id,new_result)

    with open('data.json', 'w') as outfile:
        json.dump(new_data, outfile)
    return jsonify({"status":"Success"})


def get_user_db():
    result = fb.get('/webservice', None)
    return result


def update_user(user_id,item):
    try:
        result = fb.put('/webservice', item, user_id)
        return True
    except Exception as ex:
        print(ex)
        return False


def insert_new_user_db(user_id,user_label,user_image):
    try:
        result = {
            'user_id':user_id,
            'user_label':user_label,
            'user_image':[]
        }
        result['user_image'].append(user_image)
        result = fb.post('/webservice', result)
        return True
    except:
        return False


def insert_exist_user(user_fb_id,result):
    try:
        result = fb.put('/webservice', result, user_fb_id)
        return True
    except Exception as ex:
        print(ex)
        return False


def delete_user_db(user_id):
    try:
        result = fb.delete('/webservice',user_id)
        return True
    except Exception as ex:
        print(ex)
        return False


if __name__ == '__main__':
    # app.run(host="192.168.31.117", port="8888")
    app.run(host="54.169.37.160",port="5000")
