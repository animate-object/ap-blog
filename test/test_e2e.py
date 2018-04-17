from json import loads, dumps

from mock import patch

from chalice.config import Config
from chalice.local import LocalGateway
from app import app

LIST_OBJECTS_RESPONSE = {
        "Contents": [
            {
                "LastModified": "1999-11-11T07:07:07.000Z", 
                "ETag": "\"fdbf123f-4666-4a1a-b22d-0dc4c519579c\"", 
                "StorageClass": "STANDARD", 
                "Key": "treatise_on_cetacea.md", 
                "Owner": {
                    "DisplayName": "test.account", 
                    "ID": "fdbf123f-4666-4a1a-b22d-0dc4c519579cfdbf123f-4666-4a1a-b22d-0dc4c519579c"
                    }, 
                "Size": 223 
                }, 
            {
                "LastModified": "1998-11-11T07:07:07.000Z", 
                "ETag": "\"fdbf123f-4666-4a1a-b22d-0dc4c519579c\"", 
                "StorageClass": "STANDARD", 
                "Key": "list_of_fruit.md", 
                "Owner": {
                    "DisplayName": "test.account", 
                    "ID": "fdbf123f-4666-4a1a-b22d-0dc4c519579cfdbf123f-4666-4a1a-b22d-0dc4c519579c"
                    }, 
                "Size": 489
                }
            ]
        }



lg = LocalGateway(app, Config())

HEADER = {'Content-Type': 'application/json'}

def test_ping():
    response = lg.handle_request(
            method='GET', path='/ping', headers=HEADER, body=''
            )

    assert response['body'] == '{"a": "blog"}'

@patch('chalicelib.methods.S3')
def test_post_list_returns_objects_newest_first(mock_s3_client):
    mock_s3_client.list_objects.return_value = LIST_OBJECTS_RESPONSE
    response = lg.handle_request(
            method='GET', path='/posts', headers=HEADER, body=''    
    )

    assert loads(response['body']) == ['treatise_on_cetacea.md', 'list_of_fruit.md']

