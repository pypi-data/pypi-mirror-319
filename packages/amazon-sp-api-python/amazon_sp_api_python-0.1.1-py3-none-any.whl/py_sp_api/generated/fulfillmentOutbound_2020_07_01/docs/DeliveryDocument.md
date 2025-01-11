# DeliveryDocument

A delivery document for a package.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**document_type** | **str** | The delivery document type. Values are &#x60;SIGNATURE&#x60; and &#x60;DELIVERY_IMAGE&#x60;. | 
**url** | **str** | A URL that you can use to download the document. This URL has a &#x60;Content-Type&#x60; header. Note that the URL expires after one hour. To get a new URL, you must call the API again. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.delivery_document import DeliveryDocument

# TODO update the JSON string below
json = "{}"
# create an instance of DeliveryDocument from a JSON string
delivery_document_instance = DeliveryDocument.from_json(json)
# print the JSON string representation of the object
print(DeliveryDocument.to_json())

# convert the object into a dict
delivery_document_dict = delivery_document_instance.to_dict()
# create an instance of DeliveryDocument from a dict
delivery_document_from_dict = DeliveryDocument.from_dict(delivery_document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


