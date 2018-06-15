# Face id
A source code which connect to AWS ec2 ubuntu env

## application.py
The main file of api, run it <br >

PS: for modify the host port, modify line 362


## api link:
http://ec2-54-169-37-160.ap-southeast-1.compute.amazonaws.com:5000

### list_all_user
Format: GET <br >
url: /list_all_user<br >
Input JSON format:
```json
{
    "status": true,
    "user_detail": [
        {
            "user_id": "Wilson_DMDIWXEXTZ",
            "user_label": "Wilson"
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

### insert_exist_user
Format: POST <br >
Input JSON format:
```json
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
Input JSON format:
```json
{
    "vision_kit_id": target_vision_kit_id,
    "vocie_kit_id": target_vocie_kit_id,
    "text": base64_to_str_image
}
```

Output:
```html
Identify user successful: <username>!
```