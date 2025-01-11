# ShippingConstraints

Delivery constraints applicable to this order.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pallet_delivery** | [**ConstraintType**](ConstraintType.md) |  | [optional] 
**signature_confirmation** | [**ConstraintType**](ConstraintType.md) |  | [optional] 
**recipient_identity_verification** | [**ConstraintType**](ConstraintType.md) |  | [optional] 
**recipient_age_verification** | [**ConstraintType**](ConstraintType.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.ordersV0.models.shipping_constraints import ShippingConstraints

# TODO update the JSON string below
json = "{}"
# create an instance of ShippingConstraints from a JSON string
shipping_constraints_instance = ShippingConstraints.from_json(json)
# print the JSON string representation of the object
print(ShippingConstraints.to_json())

# convert the object into a dict
shipping_constraints_dict = shipping_constraints_instance.to_dict()
# create an instance of ShippingConstraints from a dict
shipping_constraints_from_dict = ShippingConstraints.from_dict(shipping_constraints_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


