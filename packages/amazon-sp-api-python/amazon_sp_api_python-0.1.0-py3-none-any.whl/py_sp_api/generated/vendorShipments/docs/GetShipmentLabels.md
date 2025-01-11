# GetShipmentLabels

The response schema for the GetShipmentLabels operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**TransportationLabels**](TransportationLabels.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.vendorShipments.models.get_shipment_labels import GetShipmentLabels

# TODO update the JSON string below
json = "{}"
# create an instance of GetShipmentLabels from a JSON string
get_shipment_labels_instance = GetShipmentLabels.from_json(json)
# print the JSON string representation of the object
print(GetShipmentLabels.to_json())

# convert the object into a dict
get_shipment_labels_dict = get_shipment_labels_instance.to_dict()
# create an instance of GetShipmentLabels from a dict
get_shipment_labels_from_dict = GetShipmentLabels.from_dict(get_shipment_labels_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


