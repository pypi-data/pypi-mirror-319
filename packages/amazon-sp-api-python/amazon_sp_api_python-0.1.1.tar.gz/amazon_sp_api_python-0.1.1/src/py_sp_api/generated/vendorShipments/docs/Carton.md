# Carton

Details of the carton/package being shipped.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**carton_identifiers** | [**List[ContainerIdentification]**](ContainerIdentification.md) | A list of carton identifiers. | [optional] 
**carton_sequence_number** | **str** | Carton sequence number for the carton. The first carton will be 001, the second 002, and so on. This number is used as a reference to refer to this carton from the pallet level. | 
**dimensions** | [**Dimensions**](Dimensions.md) |  | [optional] 
**weight** | [**Weight**](Weight.md) |  | [optional] 
**tracking_number** | **str** | This is required to be provided for every carton in the small parcel shipments. | [optional] 
**items** | [**List[ContainerItem]**](ContainerItem.md) | A list of container item details. | 

## Example

```python
from py_sp_api.generated.vendorShipments.models.carton import Carton

# TODO update the JSON string below
json = "{}"
# create an instance of Carton from a JSON string
carton_instance = Carton.from_json(json)
# print the JSON string representation of the object
print(Carton.to_json())

# convert the object into a dict
carton_dict = carton_instance.to_dict()
# create an instance of Carton from a dict
carton_from_dict = Carton.from_dict(carton_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


