# Face id
A source code which connect to AWS ec2 ubuntu env

## application.py
The main file of api, run it <br >

PS1: for modify the host port, data file, image file, modify file config
PS2: Modify the file location in ex
PS3: Insert all requirement in requirement.txt
PS4: If fail insert in dlib, ref "Dlib install"

## setting in EC2 (insert requirement)
```bash
sudo apt-get update
sudo apt-get install build-essential cmake
sudo apt-get install libgtk-3-dev
sudo apt-get install libboost-all-dev
```

## setting in EC2 (auto start setting)
```bash
cd /usr/sbin
sudo touch api.sh
sudo chown root:root api.sh
sudo chmod +x api.sh
code in api.sh : python3.5 /home/username/face_id_api/application.py
crontab -e
add: @reboot /usr/sbin/application.py
sudo reboot
```

## Dlib install
```bash
git clone https://github.com/davisking/dlib.git
cd dlib
sudo python3 setup.py install
```

## api link:
http://ec2-54-169-37-160.ap-southeast-1.compute.amazonaws.com:5000

### list_all_user
Format: GET <br >
Url: /list_all_user<br >
Time cost: < 3000ms
Output JSON format:
```json
{
    "status": true,
    "user_detail": [
        {
            "user_id": user_id_in_firebase,
            "user_label": user_label
        },
    ]
}
```

Output JSON format:
```json
{
    "status": true/false
}
```

### insert_new_user
Format: POST <br >
Url: /insert_exist_user
Time cost: < 2000ms
Input Form-data format:
```form-data
{
    "label": label,
    "image": file
}
```

Output JSON format:
```json
{
    "status": true/false
}
```

### insert_exist_user
Format: POST <br >
Url: /insert_exist_user
Time cost: < 7000ms, affect by image size
Input Form-data format:
```form-data
{
    "user_id": user_id_in_firebase,
    "image": file
}
```

Output JSON format:
```json
{
    "status": true/false
}
```

### delete_user
Format: POST <br >
Url: /delete_user
Time cost: < 4000ms
Input JSON format:
```json
{
    "user_id": user_id_in_firebase
}
```

Output JSON format:
```json
{
    "status": true/false
}
```

### face_id
Format: POST <br >
Url: /face_id
Time cost: < 4000ms
Input JSON format:
```json
{
    "vision_kit_id": target_vision_kit_id,
    "vocie_kit_id": target_vocie_kit_id,
    "text": base64_to_str_image
}
```

Output html:
```html
Identify user successful: <username>!
```

### face_id_image
Format: POST <br >
Url: /face_id_image
Time cost: < 4000ms
Input Form-data format:
```form-data
{
    "image": file
}
```

Output JSON format:
```json
{
    "status": true/false,
    "user_label": username
}
```
