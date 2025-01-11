# CartonReferenceDetails

Carton reference details.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**carton_count** | **int** | Pallet level carton count is mandatory for single item pallet and optional for mixed item pallet. | [optional] 
**carton_reference_numbers** | **List[str]** | Array of reference numbers for the carton that are part of this pallet/shipment. Please provide the cartonSequenceNumber from the &#39;cartons&#39; segment to refer to that carton&#39;s details here. | 

## Example

```python
from py_sp_api.generated.vendorShipments.models.carton_reference_details import CartonReferenceDetails

# TODO update the JSON string below
json = "{}"
# create an instance of CartonReferenceDetails from a JSON string
carton_reference_details_instance = CartonReferenceDetails.from_json(json)
# print the JSON string representation of the object
print(CartonReferenceDetails.to_json())

# convert the object into a dict
carton_reference_details_dict = carton_reference_details_instance.to_dict()
# create an instance of CartonReferenceDetails from a dict
carton_reference_details_from_dict = CartonReferenceDetails.from_dict(carton_reference_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


