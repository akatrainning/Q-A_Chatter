from dataclasses import dataclass
import mimetypes
import os
from datetime import datetime
from http import HTTPStatus
from time import mktime
from typing import List
from urllib.parse import unquote_plus, urlparse
from wsgiref.handlers import format_date_time
import time
import threading

import requests

from dashscope.api_entities.dashscope_response import DashScopeAPIResponse
from dashscope.client.base_api import GetMixin
from dashscope.common.constants import (FILE_PATH_SCHEMA,
                                        REQUEST_CONTENT_AUDIO,
                                        REQUEST_CONTENT_IMAGE,
                                        REQUEST_CONTENT_TEXT)
from dashscope.common.error import InvalidInput, UploadFileException
from dashscope.common.logging import logger
from dashscope.common.utils import get_user_agent

@dataclass
class UploadToken:
    token: str = None
    expire_time: int = None

class UploadTokenMeta(type):
    def __init__(cls):
        cls._tokens = {} # key model, value: token and expire_time
        cls._lock = threading.Lock() # lock set
        
    @property
    def token(cls, model):
        current_time = time.perf_counter()
        upload_token: UploadToken = cls._tokens[model] if model in cls._tokens else None
        if upload_token is not None and current_time < upload_token.expire_time:
            return upload_token.token
        else:
            return None
    
    @token.setter
    def token(cls, model: str, upload_token: UploadToken):
        cls._lock.acquire()
        cls._tokens[model] = upload_token
        cls._lock.release()
    

class OssUtils(GetMixin, metaclass=UploadTokenMeta):
    SUB_PATH = 'uploads'

    @classmethod
    def _decode_response_error(cls, response: requests.Response):
        if 'application/json' in response.headers.get('content-type', ''):
            message = response.json()
        else:
            message = response.content.decode('utf-8')
        return message

    @classmethod
    def upload(cls,
               model: str,
               file_path: str,
               api_key: str = None,
               **kwargs) -> DashScopeAPIResponse:
        """Upload file for model fine-tune or other tasks.

        Args:
            file_path (str): The local file name to upload.
            purpose (str): The purpose of the file[fine-tune|inference]
            description (str, optional): The file description message.
            api_key (str, optional): The api key. Defaults to None.

        Returns:
            DashScopeAPIResponse: The upload information
        """
        upload_token = cls.token(model)
        if upload_token is None:
            upload_info = cls.get_upload_certificate(model=model, api_key=api_key)            
            if upload_info.status_code != HTTPStatus.OK:
                raise UploadFileException(
                    'Get upload certificate failed, code: %s, message: %s' %
                    (upload_info.code, upload_info.message))
            upload_info = upload_info.output
            cls.token = xx
        
        upload_info = upload_info.output
        headers = {}
        headers = {'user-agent': get_user_agent()}
        headers['Accept'] = 'application/json'
        headers['Date'] = format_date_time(mktime(datetime.now().timetuple()))
        form_data = {}
        form_data['OSSAccessKeyId'] = upload_info['oss_access_key_id']
        form_data['Signature'] = upload_info['signature']
        form_data['policy'] = upload_info['policy']
        form_data['key'] = upload_info['upload_dir'] + \
            '/' + os.path.basename(file_path)
        form_data['x-oss-object-acl'] = upload_info['x_oss_object_acl']
        form_data['x-oss-forbid-overwrite'] = upload_info[
            'x_oss_forbid_overwrite']
        form_data['success_action_status'] = '200'
        form_data['x-oss-content-type'] = mimetypes.guess_type(file_path)[0]
        url = upload_info['upload_host']
        files = {'file': open(file_path, 'rb')}
        with requests.Session() as session:
            response = session.post(url,
                                    files=files,
                                    data=form_data,
                                    headers=headers,
                                    timeout=3600)
            if response.status_code == HTTPStatus.OK:
                return 'oss://' + form_data['key']
            else:
                msg = (
                    'Uploading file: %s to oss failed, error: %s' %
                    (file_path, cls._decode_response_error(response=response)))
                logger.error(msg)
                raise UploadFileException(msg)

    @classmethod
    def get_upload_certificate(cls,
                               model: str,
                               api_key: str = None,
                               **kwargs) -> DashScopeAPIResponse:
        """Get a oss upload certificate.

        Args:
            api_key (str, optional): The api key. Defaults to None.

        Returns:
            DashScopeAPIResponse: The job info
        """
        params = {'action': 'getPolicy'}
        params['model'] = model
        return super().get(None, api_key, params=params, **kwargs)


def upload_file(model: str, upload_path: str, api_key: str):
    if upload_path.startswith(FILE_PATH_SCHEMA):
        parse_result = urlparse(upload_path)
        if parse_result.netloc:
            file_path = parse_result.netloc + unquote_plus(parse_result.path)
        else:
            file_path = unquote_plus(parse_result.path)
        if os.path.exists(file_path):
            file_url = OssUtils.upload(model=model,
                                       file_path=file_path,
                                       api_key=api_key)
            if file_url is None:
                raise UploadFileException('Uploading file: %s failed' %
                                          upload_path)
            return file_url
        else:
            raise InvalidInput('The file: %s is not exists!' % file_path)
    return None



