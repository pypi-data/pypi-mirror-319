# ShipmentLabels

Shipment labels.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**label_download_url** | **str** | URL to download generated labels. | [optional] 
**label_status** | [**LabelStatus**](LabelStatus.md) |  | 

## Example

```python
from py_sp_api.generated.awd_2024_05_09.models.shipment_labels import ShipmentLabels

# TODO update the JSON string below
json = "{}"
# create an instance of ShipmentLabels from a JSON string
shipment_labels_instance = ShipmentLabels.from_json(json)
# print the JSON string representation of the object
print(ShipmentLabels.to_json())

# convert the object into a dict
shipment_labels_dict = shipment_labels_instance.to_dict()
# create an instance of ShipmentLabels from a dict
shipment_labels_from_dict = ShipmentLabels.from_dict(shipment_labels_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


