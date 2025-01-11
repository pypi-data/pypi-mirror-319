# LabelData

Label details as part of the transport label response

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**label_sequence_number** | **int** | A sequential number assigned to each label within a shipment. | [optional] 
**label_format** | **str** | The format of the label. | [optional] 
**carrier_code** | **str** | Unique identification of the carrier. | [optional] 
**tracking_id** | **str** | Tracking Id for the transportation. | [optional] 
**label** | **str** | The base-64 encoded string that represents the shipment label. | [optional] 

## Example

```python
from py_sp_api.generated.vendorShipments.models.label_data import LabelData

# TODO update the JSON string below
json = "{}"
# create an instance of LabelData from a JSON string
label_data_instance = LabelData.from_json(json)
# print the JSON string representation of the object
print(LabelData.to_json())

# convert the object into a dict
label_data_dict = label_data_instance.to_dict()
# create an instance of LabelData from a dict
label_data_from_dict = LabelData.from_dict(label_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


