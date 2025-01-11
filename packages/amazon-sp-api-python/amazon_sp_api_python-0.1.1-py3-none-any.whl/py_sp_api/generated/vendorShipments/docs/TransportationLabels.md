# TransportationLabels

The request schema for the GetShipmentLabels operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**Pagination**](Pagination.md) |  | [optional] 
**transport_labels** | [**List[TransportLabel]**](TransportLabel.md) | A list of one or more ShipmentLabels. | [optional] 

## Example

```python
from py_sp_api.generated.vendorShipments.models.transportation_labels import TransportationLabels

# TODO update the JSON string below
json = "{}"
# create an instance of TransportationLabels from a JSON string
transportation_labels_instance = TransportationLabels.from_json(json)
# print the JSON string representation of the object
print(TransportationLabels.to_json())

# convert the object into a dict
transportation_labels_dict = transportation_labels_instance.to_dict()
# create an instance of TransportationLabels from a dict
transportation_labels_from_dict = TransportationLabels.from_dict(transportation_labels_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


