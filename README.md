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
Output JSON format:
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
###
