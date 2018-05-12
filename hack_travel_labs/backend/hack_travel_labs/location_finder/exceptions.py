from rest_framework.exceptions import APIException


class GoogleCloudVisionException(APIException):
    default_code = 'google_cloud_vision_error'
    default_detail = 'Google Cloud Vision Error'


class MissingImageException(APIException):
    default_code = 'missing_image'
    default_detail = 'Missing Image Error.'

    def __init__(self, *args, image_key=None, **kwargs):
        super().__init__(*args, **kwargs)
        if image_key:
            self.detail = f'{self.detail} Send image under "{image_key}" key.'
