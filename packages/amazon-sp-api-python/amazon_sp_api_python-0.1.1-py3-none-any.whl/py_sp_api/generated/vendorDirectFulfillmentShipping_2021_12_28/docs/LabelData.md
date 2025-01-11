# LabelData

Details of the shipment label.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**package_identifier** | **str** | Identifier for the package. The first package will be 001, the second 002, and so on. This number is used as a reference to refer to this package from the pallet level. | [optional] 
**tracking_number** | **str** | Package tracking identifier from the shipping carrier. | [optional] 
**ship_method** | **str** | Ship method to be used for shipping the order. Amazon defines Ship Method Codes indicating shipping carrier and shipment service level. Ship Method Codes are case and format sensitive. The same ship method code should returned on the shipment confirmation. Note that the Ship Method Codes are vendor specific and will be provided to each vendor during the implementation. | [optional] 
**ship_method_name** | **str** | Shipping method name for internal reference. | [optional] 
**content** | **str** | This field will contain the Base64encoded string of the shipment label content. | 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.models.label_data import LabelData

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


