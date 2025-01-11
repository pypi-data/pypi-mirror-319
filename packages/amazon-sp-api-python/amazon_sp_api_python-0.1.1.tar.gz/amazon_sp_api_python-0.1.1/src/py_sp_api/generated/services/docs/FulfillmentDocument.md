# FulfillmentDocument

Document that captured during service appointment fulfillment that portrays proof of completion

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**upload_destination_id** | **str** | The identifier of the upload destination. Get this value by calling the &#x60;createServiceDocumentUploadDestination&#x60; operation of the Services API. | [optional] 
**content_sha256** | **str** | Sha256 hash of the file content. This value is used to determine if the file has been corrupted or tampered with during transit. | [optional] 

## Example

```python
from py_sp_api.generated.services.models.fulfillment_document import FulfillmentDocument

# TODO update the JSON string below
json = "{}"
# create an instance of FulfillmentDocument from a JSON string
fulfillment_document_instance = FulfillmentDocument.from_json(json)
# print the JSON string representation of the object
print(FulfillmentDocument.to_json())

# convert the object into a dict
fulfillment_document_dict = fulfillment_document_instance.to_dict()
# create an instance of FulfillmentDocument from a dict
fulfillment_document_from_dict = FulfillmentDocument.from_dict(fulfillment_document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


