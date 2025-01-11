# py_sp_api.generated.services.ServiceApi

All URIs are relative to *https://sellingpartnerapi-na.amazon.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_appointment_for_service_job_by_service_job_id**](ServiceApi.md#add_appointment_for_service_job_by_service_job_id) | **POST** /service/v1/serviceJobs/{serviceJobId}/appointments | 
[**assign_appointment_resources**](ServiceApi.md#assign_appointment_resources) | **PUT** /service/v1/serviceJobs/{serviceJobId}/appointments/{appointmentId}/resources | 
[**cancel_reservation**](ServiceApi.md#cancel_reservation) | **DELETE** /service/v1/reservation/{reservationId} | 
[**cancel_service_job_by_service_job_id**](ServiceApi.md#cancel_service_job_by_service_job_id) | **PUT** /service/v1/serviceJobs/{serviceJobId}/cancellations | 
[**complete_service_job_by_service_job_id**](ServiceApi.md#complete_service_job_by_service_job_id) | **PUT** /service/v1/serviceJobs/{serviceJobId}/completions | 
[**create_reservation**](ServiceApi.md#create_reservation) | **POST** /service/v1/reservation | 
[**create_service_document_upload_destination**](ServiceApi.md#create_service_document_upload_destination) | **POST** /service/v1/documents | 
[**get_appointment_slots**](ServiceApi.md#get_appointment_slots) | **GET** /service/v1/appointmentSlots | 
[**get_appointmment_slots_by_job_id**](ServiceApi.md#get_appointmment_slots_by_job_id) | **GET** /service/v1/serviceJobs/{serviceJobId}/appointmentSlots | 
[**get_fixed_slot_capacity**](ServiceApi.md#get_fixed_slot_capacity) | **POST** /service/v1/serviceResources/{resourceId}/capacity/fixed | 
[**get_range_slot_capacity**](ServiceApi.md#get_range_slot_capacity) | **POST** /service/v1/serviceResources/{resourceId}/capacity/range | 
[**get_service_job_by_service_job_id**](ServiceApi.md#get_service_job_by_service_job_id) | **GET** /service/v1/serviceJobs/{serviceJobId} | 
[**get_service_jobs**](ServiceApi.md#get_service_jobs) | **GET** /service/v1/serviceJobs | 
[**reschedule_appointment_for_service_job_by_service_job_id**](ServiceApi.md#reschedule_appointment_for_service_job_by_service_job_id) | **POST** /service/v1/serviceJobs/{serviceJobId}/appointments/{appointmentId} | 
[**set_appointment_fulfillment_data**](ServiceApi.md#set_appointment_fulfillment_data) | **PUT** /service/v1/serviceJobs/{serviceJobId}/appointments/{appointmentId}/fulfillment | 
[**update_reservation**](ServiceApi.md#update_reservation) | **PUT** /service/v1/reservation/{reservationId} | 
[**update_schedule**](ServiceApi.md#update_schedule) | **PUT** /service/v1/serviceResources/{resourceId}/schedules | 


# **add_appointment_for_service_job_by_service_job_id**
> SetAppointmentResponse add_appointment_for_service_job_by_service_job_id(service_job_id, body)



Adds an appointment to the service job indicated by the service job identifier specified.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 5 | 20 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The table above indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may see higher rate and burst values than those shown here. For more information, see [Usage Plans and Rate Limits in the Selling Partner API](doc:usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.services
from py_sp_api.generated.services.models.add_appointment_request import AddAppointmentRequest
from py_sp_api.generated.services.models.set_appointment_response import SetAppointmentResponse
from py_sp_api.generated.services.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.services.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.services.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.services.ServiceApi(api_client)
    service_job_id = 'service_job_id_example' # str | An Amazon defined service job identifier.
    body = py_sp_api.generated.services.AddAppointmentRequest() # AddAppointmentRequest | Add appointment operation input details.

    try:
        api_response = api_instance.add_appointment_for_service_job_by_service_job_id(service_job_id, body)
        print("The response of ServiceApi->add_appointment_for_service_job_by_service_job_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServiceApi->add_appointment_for_service_job_by_service_job_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **service_job_id** | **str**| An Amazon defined service job identifier. | 
 **body** | [**AddAppointmentRequest**](AddAppointmentRequest.md)| Add appointment operation input details. | 

### Return type

[**SetAppointmentResponse**](SetAppointmentResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success response. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference id. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**422** | Unprocessable Entity. Unable to process the contained instructions. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**500** | Encountered an unexpected condition which prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **assign_appointment_resources**
> AssignAppointmentResourcesResponse assign_appointment_resources(service_job_id, appointment_id, body)



Assigns new resource(s) or overwrite/update the existing one(s) to a service job appointment.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 1 | 2 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The table above indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may see higher rate and burst values than those shown here. For more information, see [Usage Plans and Rate Limits in the Selling Partner API](doc:usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.services
from py_sp_api.generated.services.models.assign_appointment_resources_request import AssignAppointmentResourcesRequest
from py_sp_api.generated.services.models.assign_appointment_resources_response import AssignAppointmentResourcesResponse
from py_sp_api.generated.services.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.services.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.services.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.services.ServiceApi(api_client)
    service_job_id = 'service_job_id_example' # str | An Amazon-defined service job identifier. Get this value by calling the `getServiceJobs` operation of the Services API.
    appointment_id = 'appointment_id_example' # str | An Amazon-defined identifier of active service job appointment.
    body = py_sp_api.generated.services.AssignAppointmentResourcesRequest() # AssignAppointmentResourcesRequest | 

    try:
        api_response = api_instance.assign_appointment_resources(service_job_id, appointment_id, body)
        print("The response of ServiceApi->assign_appointment_resources:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServiceApi->assign_appointment_resources: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **service_job_id** | **str**| An Amazon-defined service job identifier. Get this value by calling the &#x60;getServiceJobs&#x60; operation of the Services API. | 
 **appointment_id** | **str**| An Amazon-defined identifier of active service job appointment. | 
 **body** | [**AssignAppointmentResourcesRequest**](AssignAppointmentResourcesRequest.md)|  | 

### Return type

[**AssignAppointmentResourcesResponse**](AssignAppointmentResourcesResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success response. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference id. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**422** | Unprocessable Entity. Unable to process the contained instructions. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **cancel_reservation**
> CancelReservationResponse cancel_reservation(reservation_id, marketplace_ids)



Cancel a reservation.   **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 5 | 20 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The table above indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may see higher rate and burst values than those shown here. For more information, see [Usage Plans and Rate Limits in the Selling Partner API](doc:usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.services
from py_sp_api.generated.services.models.cancel_reservation_response import CancelReservationResponse
from py_sp_api.generated.services.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.services.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.services.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.services.ServiceApi(api_client)
    reservation_id = 'reservation_id_example' # str | Reservation Identifier
    marketplace_ids = ['marketplace_ids_example'] # List[str] | An identifier for the marketplace in which the resource operates.

    try:
        api_response = api_instance.cancel_reservation(reservation_id, marketplace_ids)
        print("The response of ServiceApi->cancel_reservation:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServiceApi->cancel_reservation: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **reservation_id** | **str**| Reservation Identifier | 
 **marketplace_ids** | [**List[str]**](str.md)| An identifier for the marketplace in which the resource operates. | 

### Return type

[**CancelReservationResponse**](CancelReservationResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Success response. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | 403 can be caused for reasons like Access Denied, Unauthorized, Expired Token, Invalid Signature or Resource Not Found. |  * x-amzn-RequestId - Unique request reference id. <br>  |
**404** | The reservation specified does not exist. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**415** | The entity of the request is in a format not supported by the requested resource. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**500** | Encountered an unexpected condition which prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **cancel_service_job_by_service_job_id**
> CancelServiceJobByServiceJobIdResponse cancel_service_job_by_service_job_id(service_job_id, cancellation_reason_code)



Cancels the service job indicated by the service job identifier specified.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 5 | 20 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The table above indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may see higher rate and burst values than those shown here. For more information, see [Usage Plans and Rate Limits in the Selling Partner API](doc:usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.services
from py_sp_api.generated.services.models.cancel_service_job_by_service_job_id_response import CancelServiceJobByServiceJobIdResponse
from py_sp_api.generated.services.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.services.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.services.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.services.ServiceApi(api_client)
    service_job_id = 'service_job_id_example' # str | An Amazon defined service job identifier.
    cancellation_reason_code = 'cancellation_reason_code_example' # str | A cancel reason code that specifies the reason for cancelling a service job.

    try:
        api_response = api_instance.cancel_service_job_by_service_job_id(service_job_id, cancellation_reason_code)
        print("The response of ServiceApi->cancel_service_job_by_service_job_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServiceApi->cancel_service_job_by_service_job_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **service_job_id** | **str**| An Amazon defined service job identifier. | 
 **cancellation_reason_code** | **str**| A cancel reason code that specifies the reason for cancelling a service job. | 

### Return type

[**CancelServiceJobByServiceJobIdResponse**](CancelServiceJobByServiceJobIdResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success response. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference id. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**422** | Unprocessable Entity. Unable to process the contained instructions. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **complete_service_job_by_service_job_id**
> CompleteServiceJobByServiceJobIdResponse complete_service_job_by_service_job_id(service_job_id)



Completes the service job indicated by the service job identifier specified.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 5 | 20 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The table above indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may see higher rate and burst values than those shown here. For more information, see [Usage Plans and Rate Limits in the Selling Partner API](doc:usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.services
from py_sp_api.generated.services.models.complete_service_job_by_service_job_id_response import CompleteServiceJobByServiceJobIdResponse
from py_sp_api.generated.services.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.services.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.services.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.services.ServiceApi(api_client)
    service_job_id = 'service_job_id_example' # str | An Amazon defined service job identifier.

    try:
        api_response = api_instance.complete_service_job_by_service_job_id(service_job_id)
        print("The response of ServiceApi->complete_service_job_by_service_job_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServiceApi->complete_service_job_by_service_job_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **service_job_id** | **str**| An Amazon defined service job identifier. | 

### Return type

[**CompleteServiceJobByServiceJobIdResponse**](CompleteServiceJobByServiceJobIdResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success response. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference id. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**422** | Unprocessable Entity. Unable to process the contained instructions. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_reservation**
> CreateReservationResponse create_reservation(marketplace_ids, body)



Create a reservation.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 5 | 20 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The table above indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may see higher rate and burst values than those shown here. For more information, see [Usage Plans and Rate Limits in the Selling Partner API](doc:usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.services
from py_sp_api.generated.services.models.create_reservation_request import CreateReservationRequest
from py_sp_api.generated.services.models.create_reservation_response import CreateReservationResponse
from py_sp_api.generated.services.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.services.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.services.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.services.ServiceApi(api_client)
    marketplace_ids = ['marketplace_ids_example'] # List[str] | An identifier for the marketplace in which the resource operates.
    body = py_sp_api.generated.services.CreateReservationRequest() # CreateReservationRequest | Reservation details

    try:
        api_response = api_instance.create_reservation(marketplace_ids, body)
        print("The response of ServiceApi->create_reservation:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServiceApi->create_reservation: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **marketplace_ids** | [**List[str]**](str.md)| An identifier for the marketplace in which the resource operates. | 
 **body** | [**CreateReservationRequest**](CreateReservationRequest.md)| Reservation details | 

### Return type

[**CreateReservationResponse**](CreateReservationResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success response. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference id. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**500** | Encountered an unexpected condition which prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_service_document_upload_destination**
> CreateServiceDocumentUploadDestination create_service_document_upload_destination(body)



Creates an upload destination.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 5 | 20 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The table above indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may see higher rate and burst values than those shown here. For more information, see [Usage Plans and Rate Limits in the Selling Partner API](doc:usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.services
from py_sp_api.generated.services.models.create_service_document_upload_destination import CreateServiceDocumentUploadDestination
from py_sp_api.generated.services.models.service_upload_document import ServiceUploadDocument
from py_sp_api.generated.services.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.services.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.services.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.services.ServiceApi(api_client)
    body = py_sp_api.generated.services.ServiceUploadDocument() # ServiceUploadDocument | Upload document operation input details.

    try:
        api_response = api_instance.create_service_document_upload_destination(body)
        print("The response of ServiceApi->create_service_document_upload_destination:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServiceApi->create_service_document_upload_destination: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ServiceUploadDocument**](ServiceUploadDocument.md)| Upload document operation input details. | 

### Return type

[**CreateServiceDocumentUploadDestination**](CreateServiceDocumentUploadDestination.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully created an upload destination for the given resource. |  * x-amzn-requestId - Unique request reference identifier. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference id. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**415** | The request&#39;s Content-Type header is invalid. |  * x-amzn-requestid - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**422** | Unprocessable Entity. Unable to process the contained instructions. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-requestid - Unique request reference ID. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_appointment_slots**
> GetAppointmentSlotsResponse get_appointment_slots(asin, store_id, marketplace_ids, start_time=start_time, end_time=end_time)



Gets appointment slots as per the service context specified.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 20 | 40 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The table above indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may see higher rate and burst values than those shown here. For more information, see [Usage Plans and Rate Limits in the Selling Partner API](doc:usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.services
from py_sp_api.generated.services.models.get_appointment_slots_response import GetAppointmentSlotsResponse
from py_sp_api.generated.services.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.services.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.services.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.services.ServiceApi(api_client)
    asin = 'asin_example' # str | ASIN associated with the service.
    store_id = 'store_id_example' # str | Store identifier defining the region scope to retrive appointment slots.
    marketplace_ids = ['marketplace_ids_example'] # List[str] | An identifier for the marketplace for which appointment slots are queried
    start_time = 'start_time_example' # str | A time from which the appointment slots will be retrieved. The specified time must be in ISO 8601 format. If `startTime` is provided, `endTime` should also be provided. Default value is as per business configuration. (optional)
    end_time = 'end_time_example' # str | A time up to which the appointment slots will be retrieved. The specified time must be in ISO 8601 format. If `endTime` is provided, `startTime` should also be provided. Default value is as per business configuration. Maximum range of appointment slots can be 90 days. (optional)

    try:
        api_response = api_instance.get_appointment_slots(asin, store_id, marketplace_ids, start_time=start_time, end_time=end_time)
        print("The response of ServiceApi->get_appointment_slots:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServiceApi->get_appointment_slots: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asin** | **str**| ASIN associated with the service. | 
 **store_id** | **str**| Store identifier defining the region scope to retrive appointment slots. | 
 **marketplace_ids** | [**List[str]**](str.md)| An identifier for the marketplace for which appointment slots are queried | 
 **start_time** | **str**| A time from which the appointment slots will be retrieved. The specified time must be in ISO 8601 format. If &#x60;startTime&#x60; is provided, &#x60;endTime&#x60; should also be provided. Default value is as per business configuration. | [optional] 
 **end_time** | **str**| A time up to which the appointment slots will be retrieved. The specified time must be in ISO 8601 format. If &#x60;endTime&#x60; is provided, &#x60;startTime&#x60; should also be provided. Default value is as per business configuration. Maximum range of appointment slots can be 90 days. | [optional] 

### Return type

[**GetAppointmentSlotsResponse**](GetAppointmentSlotsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success response. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference id. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**422** | Unprocessable Entity. Unable to process the contained instructions. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_appointmment_slots_by_job_id**
> GetAppointmentSlotsResponse get_appointmment_slots_by_job_id(service_job_id, marketplace_ids, start_time=start_time, end_time=end_time)



Gets appointment slots for the service associated with the service job id specified.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 5 | 20 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The table above indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may see higher rate and burst values than those shown here. For more information, see [Usage Plans and Rate Limits in the Selling Partner API](doc:usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.services
from py_sp_api.generated.services.models.get_appointment_slots_response import GetAppointmentSlotsResponse
from py_sp_api.generated.services.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.services.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.services.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.services.ServiceApi(api_client)
    service_job_id = 'service_job_id_example' # str | A service job identifier to retrive appointment slots for associated service.
    marketplace_ids = ['marketplace_ids_example'] # List[str] | An identifier for the marketplace in which the resource operates.
    start_time = 'start_time_example' # str | A time from which the appointment slots will be retrieved. The specified time must be in ISO 8601 format. If `startTime` is provided, `endTime` should also be provided. Default value is as per business configuration. (optional)
    end_time = 'end_time_example' # str | A time up to which the appointment slots will be retrieved. The specified time must be in ISO 8601 format. If `endTime` is provided, `startTime` should also be provided. Default value is as per business configuration. Maximum range of appointment slots can be 90 days. (optional)

    try:
        api_response = api_instance.get_appointmment_slots_by_job_id(service_job_id, marketplace_ids, start_time=start_time, end_time=end_time)
        print("The response of ServiceApi->get_appointmment_slots_by_job_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServiceApi->get_appointmment_slots_by_job_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **service_job_id** | **str**| A service job identifier to retrive appointment slots for associated service. | 
 **marketplace_ids** | [**List[str]**](str.md)| An identifier for the marketplace in which the resource operates. | 
 **start_time** | **str**| A time from which the appointment slots will be retrieved. The specified time must be in ISO 8601 format. If &#x60;startTime&#x60; is provided, &#x60;endTime&#x60; should also be provided. Default value is as per business configuration. | [optional] 
 **end_time** | **str**| A time up to which the appointment slots will be retrieved. The specified time must be in ISO 8601 format. If &#x60;endTime&#x60; is provided, &#x60;startTime&#x60; should also be provided. Default value is as per business configuration. Maximum range of appointment slots can be 90 days. | [optional] 

### Return type

[**GetAppointmentSlotsResponse**](GetAppointmentSlotsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success response. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference id. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**422** | Unprocessable Entity. Unable to process the contained instructions. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_fixed_slot_capacity**
> FixedSlotCapacity get_fixed_slot_capacity(resource_id, marketplace_ids, body, next_page_token=next_page_token)



Provides capacity in fixed-size slots.   **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 5 | 20 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The table above indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may see higher rate and burst values than those shown here. For more information, see [Usage Plans and Rate Limits in the Selling Partner API](doc:usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.services
from py_sp_api.generated.services.models.fixed_slot_capacity import FixedSlotCapacity
from py_sp_api.generated.services.models.fixed_slot_capacity_query import FixedSlotCapacityQuery
from py_sp_api.generated.services.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.services.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.services.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.services.ServiceApi(api_client)
    resource_id = 'resource_id_example' # str | Resource Identifier.
    marketplace_ids = ['marketplace_ids_example'] # List[str] | An identifier for the marketplace in which the resource operates.
    body = py_sp_api.generated.services.FixedSlotCapacityQuery() # FixedSlotCapacityQuery | Request body.
    next_page_token = 'next_page_token_example' # str | Next page token returned in the response of your previous request. (optional)

    try:
        api_response = api_instance.get_fixed_slot_capacity(resource_id, marketplace_ids, body, next_page_token=next_page_token)
        print("The response of ServiceApi->get_fixed_slot_capacity:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServiceApi->get_fixed_slot_capacity: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **resource_id** | **str**| Resource Identifier. | 
 **marketplace_ids** | [**List[str]**](str.md)| An identifier for the marketplace in which the resource operates. | 
 **body** | [**FixedSlotCapacityQuery**](FixedSlotCapacityQuery.md)| Request body. | 
 **next_page_token** | **str**| Next page token returned in the response of your previous request. | [optional] 

### Return type

[**FixedSlotCapacity**](FixedSlotCapacity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success response. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**401** | The request&#39;s Authorization header is not formatted correctly or does not contain a valid token. |  * x-amzn-RequestId - Unique request reference id. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference id. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference id. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference id. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference id. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference id. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference id. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_range_slot_capacity**
> RangeSlotCapacity get_range_slot_capacity(resource_id, marketplace_ids, body, next_page_token=next_page_token)



Provides capacity slots in a format similar to availability records.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 5 | 20 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The table above indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may see higher rate and burst values than those shown here. For more information, see [Usage Plans and Rate Limits in the Selling Partner API](doc:usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.services
from py_sp_api.generated.services.models.range_slot_capacity import RangeSlotCapacity
from py_sp_api.generated.services.models.range_slot_capacity_query import RangeSlotCapacityQuery
from py_sp_api.generated.services.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.services.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.services.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.services.ServiceApi(api_client)
    resource_id = 'resource_id_example' # str | Resource Identifier.
    marketplace_ids = ['marketplace_ids_example'] # List[str] | An identifier for the marketplace in which the resource operates.
    body = py_sp_api.generated.services.RangeSlotCapacityQuery() # RangeSlotCapacityQuery | Request body.
    next_page_token = 'next_page_token_example' # str | Next page token returned in the response of your previous request. (optional)

    try:
        api_response = api_instance.get_range_slot_capacity(resource_id, marketplace_ids, body, next_page_token=next_page_token)
        print("The response of ServiceApi->get_range_slot_capacity:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServiceApi->get_range_slot_capacity: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **resource_id** | **str**| Resource Identifier. | 
 **marketplace_ids** | [**List[str]**](str.md)| An identifier for the marketplace in which the resource operates. | 
 **body** | [**RangeSlotCapacityQuery**](RangeSlotCapacityQuery.md)| Request body. | 
 **next_page_token** | **str**| Next page token returned in the response of your previous request. | [optional] 

### Return type

[**RangeSlotCapacity**](RangeSlotCapacity.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success response. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**401** | The request&#39;s Authorization header is not formatted correctly or does not contain a valid token. |  * x-amzn-RequestId - Unique request reference id. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference id. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference id. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference id. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference id. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference id. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference id. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_service_job_by_service_job_id**
> GetServiceJobByServiceJobIdResponse get_service_job_by_service_job_id(service_job_id)



Gets details of service job indicated by the provided `serviceJobID`.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 20 | 40 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The table above indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may see higher rate and burst values than those shown here. For more information, see [Usage Plans and Rate Limits in the Selling Partner API](doc:usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.services
from py_sp_api.generated.services.models.get_service_job_by_service_job_id_response import GetServiceJobByServiceJobIdResponse
from py_sp_api.generated.services.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.services.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.services.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.services.ServiceApi(api_client)
    service_job_id = 'service_job_id_example' # str | A service job identifier.

    try:
        api_response = api_instance.get_service_job_by_service_job_id(service_job_id)
        print("The response of ServiceApi->get_service_job_by_service_job_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServiceApi->get_service_job_by_service_job_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **service_job_id** | **str**| A service job identifier. | 

### Return type

[**GetServiceJobByServiceJobIdResponse**](GetServiceJobByServiceJobIdResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success response. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference id. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**422** | Unprocessable Entity. Unable to process the contained instructions. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_service_jobs**
> GetServiceJobsResponse get_service_jobs(marketplace_ids, service_order_ids=service_order_ids, service_job_status=service_job_status, page_token=page_token, page_size=page_size, sort_field=sort_field, sort_order=sort_order, created_after=created_after, created_before=created_before, last_updated_after=last_updated_after, last_updated_before=last_updated_before, schedule_start_date=schedule_start_date, schedule_end_date=schedule_end_date, asins=asins, required_skills=required_skills, store_ids=store_ids)



Gets service job details for the specified filter query.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 10 | 40 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The table above indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may see higher rate and burst values than those shown here. For more information, see [Usage Plans and Rate Limits in the Selling Partner API](doc:usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.services
from py_sp_api.generated.services.models.get_service_jobs_response import GetServiceJobsResponse
from py_sp_api.generated.services.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.services.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.services.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.services.ServiceApi(api_client)
    marketplace_ids = ['marketplace_ids_example'] # List[str] | Used to select jobs that were placed in the specified marketplaces.
    service_order_ids = ['service_order_ids_example'] # List[str] | List of service order ids for the query you want to perform.Max values supported 20. (optional)
    service_job_status = ['service_job_status_example'] # List[str] | A list of one or more job status by which to filter the list of jobs. (optional)
    page_token = 'page_token_example' # str | String returned in the response of your previous request. (optional)
    page_size = 20 # int | A non-negative integer that indicates the maximum number of jobs to return in the list, Value must be 1 - 20. Default 20. (optional) (default to 20)
    sort_field = 'sort_field_example' # str | Sort fields on which you want to sort the output. (optional)
    sort_order = 'sort_order_example' # str | Sort order for the query you want to perform. (optional)
    created_after = 'created_after_example' # str | A date used for selecting jobs created at or after a specified time. Must be in ISO 8601 format. Required if `LastUpdatedAfter` is not specified. Specifying both `CreatedAfter` and `LastUpdatedAfter` returns an error. (optional)
    created_before = 'created_before_example' # str | A date used for selecting jobs created at or before a specified time. Must be in ISO 8601 format. (optional)
    last_updated_after = 'last_updated_after_example' # str | A date used for selecting jobs updated at or after a specified time. Must be in ISO 8601 format. Required if `createdAfter` is not specified. Specifying both `CreatedAfter` and `LastUpdatedAfter` returns an error. (optional)
    last_updated_before = 'last_updated_before_example' # str | A date used for selecting jobs updated at or before a specified time. Must be in ISO 8601 format. (optional)
    schedule_start_date = 'schedule_start_date_example' # str | A date used for filtering jobs schedules at or after a specified time. Must be in ISO 8601 format. Schedule end date should not be earlier than schedule start date. (optional)
    schedule_end_date = 'schedule_end_date_example' # str | A date used for filtering jobs schedules at or before a specified time. Must be in ISO 8601 format. Schedule end date should not be earlier than schedule start date. (optional)
    asins = ['asins_example'] # List[str] | List of Amazon Standard Identification Numbers (ASIN) of the items. Max values supported is 20. (optional)
    required_skills = ['required_skills_example'] # List[str] | A defined set of related knowledge, skills, experience, tools, materials, and work processes common to service delivery for a set of products and/or service scenarios. Max values supported is 20. (optional)
    store_ids = ['store_ids_example'] # List[str] | List of Amazon-defined identifiers for the region scope. Max values supported is 50. (optional)

    try:
        api_response = api_instance.get_service_jobs(marketplace_ids, service_order_ids=service_order_ids, service_job_status=service_job_status, page_token=page_token, page_size=page_size, sort_field=sort_field, sort_order=sort_order, created_after=created_after, created_before=created_before, last_updated_after=last_updated_after, last_updated_before=last_updated_before, schedule_start_date=schedule_start_date, schedule_end_date=schedule_end_date, asins=asins, required_skills=required_skills, store_ids=store_ids)
        print("The response of ServiceApi->get_service_jobs:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServiceApi->get_service_jobs: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **marketplace_ids** | [**List[str]**](str.md)| Used to select jobs that were placed in the specified marketplaces. | 
 **service_order_ids** | [**List[str]**](str.md)| List of service order ids for the query you want to perform.Max values supported 20. | [optional] 
 **service_job_status** | [**List[str]**](str.md)| A list of one or more job status by which to filter the list of jobs. | [optional] 
 **page_token** | **str**| String returned in the response of your previous request. | [optional] 
 **page_size** | **int**| A non-negative integer that indicates the maximum number of jobs to return in the list, Value must be 1 - 20. Default 20. | [optional] [default to 20]
 **sort_field** | **str**| Sort fields on which you want to sort the output. | [optional] 
 **sort_order** | **str**| Sort order for the query you want to perform. | [optional] 
 **created_after** | **str**| A date used for selecting jobs created at or after a specified time. Must be in ISO 8601 format. Required if &#x60;LastUpdatedAfter&#x60; is not specified. Specifying both &#x60;CreatedAfter&#x60; and &#x60;LastUpdatedAfter&#x60; returns an error. | [optional] 
 **created_before** | **str**| A date used for selecting jobs created at or before a specified time. Must be in ISO 8601 format. | [optional] 
 **last_updated_after** | **str**| A date used for selecting jobs updated at or after a specified time. Must be in ISO 8601 format. Required if &#x60;createdAfter&#x60; is not specified. Specifying both &#x60;CreatedAfter&#x60; and &#x60;LastUpdatedAfter&#x60; returns an error. | [optional] 
 **last_updated_before** | **str**| A date used for selecting jobs updated at or before a specified time. Must be in ISO 8601 format. | [optional] 
 **schedule_start_date** | **str**| A date used for filtering jobs schedules at or after a specified time. Must be in ISO 8601 format. Schedule end date should not be earlier than schedule start date. | [optional] 
 **schedule_end_date** | **str**| A date used for filtering jobs schedules at or before a specified time. Must be in ISO 8601 format. Schedule end date should not be earlier than schedule start date. | [optional] 
 **asins** | [**List[str]**](str.md)| List of Amazon Standard Identification Numbers (ASIN) of the items. Max values supported is 20. | [optional] 
 **required_skills** | [**List[str]**](str.md)| A defined set of related knowledge, skills, experience, tools, materials, and work processes common to service delivery for a set of products and/or service scenarios. Max values supported is 20. | [optional] 
 **store_ids** | [**List[str]**](str.md)| List of Amazon-defined identifiers for the region scope. Max values supported is 50. | [optional] 

### Return type

[**GetServiceJobsResponse**](GetServiceJobsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success response. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference id. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**500** | An unexpected condition occurred that prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **reschedule_appointment_for_service_job_by_service_job_id**
> SetAppointmentResponse reschedule_appointment_for_service_job_by_service_job_id(service_job_id, appointment_id, body)



Reschedules an appointment for the service job indicated by the service job identifier specified.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 5 | 20 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The table above indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may see higher rate and burst values than those shown here. For more information, see [Usage Plans and Rate Limits in the Selling Partner API](doc:usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.services
from py_sp_api.generated.services.models.reschedule_appointment_request import RescheduleAppointmentRequest
from py_sp_api.generated.services.models.set_appointment_response import SetAppointmentResponse
from py_sp_api.generated.services.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.services.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.services.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.services.ServiceApi(api_client)
    service_job_id = 'service_job_id_example' # str | An Amazon defined service job identifier.
    appointment_id = 'appointment_id_example' # str | An existing appointment identifier for the Service Job.
    body = py_sp_api.generated.services.RescheduleAppointmentRequest() # RescheduleAppointmentRequest | Reschedule appointment operation input details.

    try:
        api_response = api_instance.reschedule_appointment_for_service_job_by_service_job_id(service_job_id, appointment_id, body)
        print("The response of ServiceApi->reschedule_appointment_for_service_job_by_service_job_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServiceApi->reschedule_appointment_for_service_job_by_service_job_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **service_job_id** | **str**| An Amazon defined service job identifier. | 
 **appointment_id** | **str**| An existing appointment identifier for the Service Job. | 
 **body** | [**RescheduleAppointmentRequest**](RescheduleAppointmentRequest.md)| Reschedule appointment operation input details. | 

### Return type

[**SetAppointmentResponse**](SetAppointmentResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success response. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference id. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**422** | Unprocessable Entity. Unable to process the contained instructions. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**500** | Encountered an unexpected condition which prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_appointment_fulfillment_data**
> str set_appointment_fulfillment_data(service_job_id, appointment_id, body)



Updates the appointment fulfillment data related to a given `jobID` and `appointmentID`.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 5 | 20 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The table above indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may see higher rate and burst values than those shown here. For more information, see [Usage Plans and Rate Limits in the Selling Partner API](doc:usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.services
from py_sp_api.generated.services.models.set_appointment_fulfillment_data_request import SetAppointmentFulfillmentDataRequest
from py_sp_api.generated.services.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.services.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.services.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.services.ServiceApi(api_client)
    service_job_id = 'service_job_id_example' # str | An Amazon-defined service job identifier. Get this value by calling the `getServiceJobs` operation of the Services API.
    appointment_id = 'appointment_id_example' # str | An Amazon-defined identifier of active service job appointment.
    body = py_sp_api.generated.services.SetAppointmentFulfillmentDataRequest() # SetAppointmentFulfillmentDataRequest | Appointment fulfillment data collection details.

    try:
        api_response = api_instance.set_appointment_fulfillment_data(service_job_id, appointment_id, body)
        print("The response of ServiceApi->set_appointment_fulfillment_data:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServiceApi->set_appointment_fulfillment_data: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **service_job_id** | **str**| An Amazon-defined service job identifier. Get this value by calling the &#x60;getServiceJobs&#x60; operation of the Services API. | 
 **appointment_id** | **str**| An Amazon-defined identifier of active service job appointment. | 
 **body** | [**SetAppointmentFulfillmentDataRequest**](SetAppointmentFulfillmentDataRequest.md)| Appointment fulfillment data collection details. | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Success response. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | 403 can be caused for reasons like Access Denied, Unauthorized, Expired Token, Invalid Signature or Resource Not Found. |  * x-amzn-RequestId - Unique request reference id. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**415** | The entity of the request is in a format not supported by the requested resource. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**422** | Unprocessable Entity. Unable to process the contained instructions. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**500** | Encountered an unexpected condition which prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_reservation**
> UpdateReservationResponse update_reservation(reservation_id, marketplace_ids, body)



Update a reservation.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 5 | 20 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The table above indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may see higher rate and burst values than those shown here. For more information, see [Usage Plans and Rate Limits in the Selling Partner API](doc:usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.services
from py_sp_api.generated.services.models.update_reservation_request import UpdateReservationRequest
from py_sp_api.generated.services.models.update_reservation_response import UpdateReservationResponse
from py_sp_api.generated.services.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.services.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.services.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.services.ServiceApi(api_client)
    reservation_id = 'reservation_id_example' # str | Reservation Identifier
    marketplace_ids = ['marketplace_ids_example'] # List[str] | An identifier for the marketplace in which the resource operates.
    body = py_sp_api.generated.services.UpdateReservationRequest() # UpdateReservationRequest | Reservation details

    try:
        api_response = api_instance.update_reservation(reservation_id, marketplace_ids, body)
        print("The response of ServiceApi->update_reservation:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServiceApi->update_reservation: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **reservation_id** | **str**| Reservation Identifier | 
 **marketplace_ids** | [**List[str]**](str.md)| An identifier for the marketplace in which the resource operates. | 
 **body** | [**UpdateReservationRequest**](UpdateReservationRequest.md)| Reservation details | 

### Return type

[**UpdateReservationResponse**](UpdateReservationResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success response. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference id. <br>  |
**404** | The reservation specified does not exist. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**500** | Encountered an unexpected condition which prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_schedule**
> UpdateScheduleResponse update_schedule(resource_id, marketplace_ids, body)



Update the schedule of the given resource.  **Usage Plan:**  | Rate (requests per second) | Burst | | ---- | ---- | | 5 | 20 |  The `x-amzn-RateLimit-Limit` response header returns the usage plan rate limits that were applied to the requested operation, when available. The table above indicates the default rate and burst values for this operation. Selling partners whose business demands require higher throughput may see higher rate and burst values than those shown here. For more information, see [Usage Plans and Rate Limits in the Selling Partner API](doc:usage-plans-and-rate-limits-in-the-sp-api).

### Example


```python
import py_sp_api.generated.services
from py_sp_api.generated.services.models.update_schedule_request import UpdateScheduleRequest
from py_sp_api.generated.services.models.update_schedule_response import UpdateScheduleResponse
from py_sp_api.generated.services.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://sellingpartnerapi-na.amazon.com
# See configuration.py for a list of all supported configuration parameters.
configuration = py_sp_api.generated.services.Configuration(
    host = "https://sellingpartnerapi-na.amazon.com"
)


# Enter a context with an instance of the API client
with py_sp_api.generated.services.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = py_sp_api.generated.services.ServiceApi(api_client)
    resource_id = 'resource_id_example' # str | Resource (store) Identifier
    marketplace_ids = ['marketplace_ids_example'] # List[str] | An identifier for the marketplace in which the resource operates.
    body = py_sp_api.generated.services.UpdateScheduleRequest() # UpdateScheduleRequest | Schedule details

    try:
        api_response = api_instance.update_schedule(resource_id, marketplace_ids, body)
        print("The response of ServiceApi->update_schedule:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServiceApi->update_schedule: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **resource_id** | **str**| Resource (store) Identifier | 
 **marketplace_ids** | [**List[str]**](str.md)| An identifier for the marketplace in which the resource operates. | 
 **body** | [**UpdateScheduleRequest**](UpdateScheduleRequest.md)| Schedule details | 

### Return type

[**UpdateScheduleResponse**](UpdateScheduleResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success response. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**400** | Request has missing or invalid parameters and cannot be parsed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**403** | Indicates that access to the resource is forbidden. Possible reasons include Access Denied, Unauthorized, Expired Token, or Invalid Signature. |  * x-amzn-RequestId - Unique request reference id. <br>  |
**404** | The resource specified does not exist. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**413** | The request size exceeded the maximum accepted size. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**415** | The request payload is in an unsupported format. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**429** | The frequency of requests was greater than allowed. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**500** | Encountered an unexpected condition which prevented the server from fulfilling the request. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |
**503** | Temporary overloading or maintenance of the server. |  * x-amzn-RequestId - Unique request reference id. <br>  * x-amzn-RateLimit-Limit - Your rate limit (requests per second) for this operation. <br>  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

