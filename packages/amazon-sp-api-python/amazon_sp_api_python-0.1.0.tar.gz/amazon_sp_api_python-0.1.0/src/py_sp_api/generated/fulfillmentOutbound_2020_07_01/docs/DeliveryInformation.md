# DeliveryInformation

The delivery information for the package. This information is available after the package is delivered.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**delivery_document_list** | [**List[DeliveryDocument]**](DeliveryDocument.md) | A list of delivery documents for a package. | [optional] 
**drop_off_location** | [**DropOffLocation**](DropOffLocation.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.delivery_information import DeliveryInformation

# TODO update the JSON string below
json = "{}"
# create an instance of DeliveryInformation from a JSON string
delivery_information_instance = DeliveryInformation.from_json(json)
# print the JSON string representation of the object
print(DeliveryInformation.to_json())

# convert the object into a dict
delivery_information_dict = delivery_information_instance.to_dict()
# create an instance of DeliveryInformation from a dict
delivery_information_from_dict = DeliveryInformation.from_dict(delivery_information_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


