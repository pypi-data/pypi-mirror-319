# ListShipmentBoxesResponse

The `listShipmentBoxes` response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**boxes** | [**List[Box]**](Box.md) | A list of boxes in a shipment. | 
**pagination** | [**Pagination**](Pagination.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.list_shipment_boxes_response import ListShipmentBoxesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListShipmentBoxesResponse from a JSON string
list_shipment_boxes_response_instance = ListShipmentBoxesResponse.from_json(json)
# print the JSON string representation of the object
print(ListShipmentBoxesResponse.to_json())

# convert the object into a dict
list_shipment_boxes_response_dict = list_shipment_boxes_response_instance.to_dict()
# create an instance of ListShipmentBoxesResponse from a dict
list_shipment_boxes_response_from_dict = ListShipmentBoxesResponse.from_dict(list_shipment_boxes_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


