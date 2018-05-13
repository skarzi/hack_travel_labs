from google.cloud.vision import (
    ImageAnnotatorClient,
    types,
)

from hack_travel_labs.location_finder.exceptions import GoogleCloudVisionException


class GoogleLocationService:
    image_annotator = ImageAnnotatorClient()

    def find(self, image_file):
        image = types.Image(content=image_file.read())
        response = self.image_annotator.landmark_detection(image)
        self._raise_for_error(response)
        return self._make_response(response.landmark_annotations)

    def _make_response(self, landmark_annotations):
        try:
            landmark = landmark_annotations[0]
        except IndexError:
            raise GoogleCloudVisionException(detail='Landmark not found.')
        return self._landmark_annotation_to_dict(landmark)

    @staticmethod
    def _raise_for_error(response):
        if response.HasField('error'):
            raise GoogleCloudVisionException(
                detail=response.error.message,
            )

    @staticmethod
    def _landmark_annotation_to_dict(landmark_annotation):
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
