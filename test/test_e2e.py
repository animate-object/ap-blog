from json import loads, dumps

from mock import Mock, patch
from botocore.response import StreamingBody
from botocore.exceptions import ClientError

from chalice.config import Config
from chalice.local import LocalGateway
from app import app

LIST_OBJECTS_RESPONSE = {
        "Contents": [
            {
                "LastModified": "1999-11-11T07:07:07.000Z", 
                "Key": "treatise_on_cetacea.md", 
                },
            {
                "LastModified": "1998-11-11T07:07:07.000Z", 
                "Key": "list_of_fruit.md", 
                }
            ]
        }
MOCK_S3_OBJECT_STREAM = Mock(spec=StreamingBody)

MOCK_S3_OBJECT_STREAM.read.return_value = \
        bytes('Starfruit, Tomatoes, Apples', encoding='utf-8')
GET_OBJECT_RESPONSE = {
        'Body': MOCK_S3_OBJECT_STREAM
        }

lg = LocalGateway(app, Config())

HEADER = {'Content-Type': 'application/json'}

def test_ping():
    response = lg.handle_request(
            method='GET',
            path='/ping',
            headers=HEADER,
            body=''
    )

    assert response['body'] == '{"a": "blog"}'

@patch('chalicelib.methods.S3')
def test_post_list_returns_objects_newest_first(mock_s3_client):
    mock_s3_client.list_objects.return_value = LIST_OBJECTS_RESPONSE
    response = lg.handle_request(
            method='GET',
            path='/posts',
            headers=HEADER,
            body=''    
    )

    assert loads(response['body']) == ['treatise_on_cetacea.md', 'list_of_fruit.md']


@patch('chalicelib.methods.S3')
def test_post_list_handles_empty_bucket(mock_s3_client):
    mock_s3_client.list_objects.return_value = {}
    response = lg.handle_request(
            method='GET',
            path='/posts',
            headers=HEADER,
            body=''    
    )

    assert loads(response['body']) == []


@patch('chalicelib.methods.S3')
def test_get_post_returns_post(mock_s3_client):
    mock_s3_client.get_object.return_value = GET_OBJECT_RESPONSE
    response = lg.handle_request(
            method='GET', 
            path='/posts/list_of_fruit.md',
            headers=HEADER,
            body=''
    )
    
    assert response['body'] == 'Starfruit, Tomatoes, Apples'


@patch('chalicelib.methods.S3')
def test_get_post_handles_no_such_key(mock_s3_client):
    mock_s3_client.get_object.side_effect = \
            ClientError({'Error': {'Code': 'NoSuchKey'}}, 's3')
    response = lg.handle_request(
            method='GET', 
            path='/posts/list_of_fruit.md',
            headers=HEADER,
            body=''
    )
    
    assert response['statusCode'] == 404

