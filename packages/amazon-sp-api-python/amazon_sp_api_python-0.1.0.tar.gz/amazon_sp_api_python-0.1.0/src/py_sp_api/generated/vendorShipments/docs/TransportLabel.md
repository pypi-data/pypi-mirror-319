# TransportLabel

A list of one or more ShipmentLabels.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**label_create_date_time** | **datetime** | Date on which label is created. | [optional] 
**shipment_information** | [**ShipmentInformation**](ShipmentInformation.md) |  | [optional] 
**label_data** | [**List[LabelData]**](LabelData.md) | Indicates the label data,format and type associated . | [optional] 

## Example

```python
from py_sp_api.generated.vendorShipments.models.transport_label import TransportLabel

# TODO update the JSON string below
json = "{}"
# create an instance of TransportLabel from a JSON string
transport_label_instance = TransportLabel.from_json(json)
# print the JSON string representation of the object
print(TransportLabel.to_json())

# convert the object into a dict
transport_label_dict = transport_label_instance.to_dict()
# create an instance of TransportLabel from a dict
transport_label_from_dict = TransportLabel.from_dict(transport_label_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


