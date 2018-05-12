from google.cloud.vision import (
    ImageAnnotatorClient,
    types,
)

from .exceptions import GoogleCloudVisionException


class GoogleLocationFinder:
    image_annotator = ImageAnnotatorClient()

    def find(self, image_obj, context=None):
        image = types.Image(content=image_obj.file.read())
        response = self.image_annotator.landmark_detection(image)
        self._raise_for_error(response.error)
        return self._make_response(response.landmark_annotations)

    def _make_response(self, landmark_annotations):
        try:
            landmark = landmark_annotations[0]
        except IndexError:
            raise GoogleCloudVisionException(detail='Landmark not found.')
        return {
            'locations': self._landmark_annotation_to_dict(landmark),
        }

    def _raise_for_error(self, error):
        if error is not None:
            raise GoogleCloudVisionException(
                detail=error.message,
            )

    def _landmark_annotation_to_dict(self, landmark_annotation):
        try:
            coordinates = landmark_annotation.locations[0].lat_lng
        except IndexError:
            raise GoogleCloudVisionException(detail='Location not found.')
        return {
            'coordinates': {
                'latitude': coordinates.latitude,
                'longtitude': coordinates.longitude,
            },
            'name': landmark_annotation.description,
        }
