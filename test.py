import requests as r
import json

url = 'http://localhost:8000/'

# this function will make 100 api requests and make sure each element is the correct type
def validate_get_request():
    for i in range(0, 99):
        response = r.get(url).json()
        assert type(response['text']) == str
        assert type(response['exclude']) == list

    print('GET request validated.')

# ensure that a malformed request returns a 400 error
def check_post_request_validation():
    header = {'Content-Type':'application/json'}

    sample1 = {'text' : ['this', 'is', 'not', 'a', 'string'],
              'count': {'count' : 3}, 'exclude':['is', 'not']}

    post1 = r.post(url, data=json.dumps(sample1), headers=header)

    assert post1.status_code==400

    sample2 = {'text' : 'this is a string',
              'count': [3], 'exclude':['is', 'a']}

    post2 = r.post(url, data=json.dumps(sample2), headers=header)

    assert post2.status_code==400

    sample3 = {'text' : 'this is a sring',
              'count': {'this' : 1, 'string' : 1}, 'exclude':'is'}

    post3 = r.post(url, data=json.dumps(sample3), headers=header)

    assert post3.status_code==400

    print('POST request type checking validated.')

    sample4 = {'text' : 'this is also a string', 'count':{'string':1}}

    post4 = r.post(url, data=json.dumps(sample4), headers=header)

    assert post4.status_code==400

if __name__ == '__main__':
    validate_get_request()
    check_post_request_validation()
