# SubmitShipments

The request schema for the SubmitShipments operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**shipments** | [**List[Shipment]**](Shipment.md) | A list of one or more shipments with underlying details. | [optional] 

## Example

```python
from py_sp_api.generated.vendorShipments.models.submit_shipments import SubmitShipments

# TODO update the JSON string below
json = "{}"
# create an instance of SubmitShipments from a JSON string
submit_shipments_instance = SubmitShipments.from_json(json)
# print the JSON string representation of the object
print(SubmitShipments.to_json())

# convert the object into a dict
submit_shipments_dict = submit_shipments_instance.to_dict()
# create an instance of SubmitShipments from a dict
submit_shipments_from_dict = SubmitShipments.from_dict(submit_shipments_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


