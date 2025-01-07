# src.cudo_compute.ObjectStorageApi

All URIs are relative to *https://rest.compute.cudo.org*

Method | HTTP request | Description
------------- | ------------- | -------------
[**activate**](ObjectStorageApi.md#activate) | **POST** /v1/projects/{projectId}/object-storage/activate | Allow the use of S3 compatible storage in a project
[**create_object_storage_user**](ObjectStorageApi.md#create_object_storage_user) | **POST** /v1/projects/{projectId}/object-storage/users | Create user that stores keys for storage buckets
[**delete_object_storage_key**](ObjectStorageApi.md#delete_object_storage_key) | **POST** /v1/projects/{projectId}/object-storage/users/{id}/keys | Delete object storage user
[**delete_object_storage_user**](ObjectStorageApi.md#delete_object_storage_user) | **DELETE** /v1/projects/{projectId}/object-storage/users/{id} | Delete object storage user
[**generate_object_storage_key**](ObjectStorageApi.md#generate_object_storage_key) | **POST** /v1/projects/{projectId}/object-storage/users/{id} | Generate access key for storage buckets
[**get_object_storage_bucket**](ObjectStorageApi.md#get_object_storage_bucket) | **GET** /v1/projects/{projectId}/object-storage/buckets/{id} | Get details for a bucket
[**get_object_storage_session_key**](ObjectStorageApi.md#get_object_storage_session_key) | **GET** /v1/projects/{projectId}/object-storage/session-key | Generate temporary key for storage bucket access
[**list_object_storage_buckets**](ObjectStorageApi.md#list_object_storage_buckets) | **GET** /v1/projects/{projectId}/object-storage/buckets | List buckets
[**list_object_storage_keys**](ObjectStorageApi.md#list_object_storage_keys) | **GET** /v1/projects/{projectId}/object-storage/users/{id}/keys | List storage user keys
[**list_object_storage_users**](ObjectStorageApi.md#list_object_storage_users) | **GET** /v1/projects/{projectId}/object-storage/users | List storage users


# **activate**
> object activate(project_id, activate_body)

Allow the use of S3 compatible storage in a project

### Example
```python
from __future__ import print_function
import time
import src.cudo_compute
from src.cudo_compute.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = src.cudo_compute.ObjectStorageApi()
project_id = 'project_id_example' # str | 
activate_body = src.cudo_compute.ActivateBody() # ActivateBody | 

try:
    # Allow the use of S3 compatible storage in a project
    api_response = api_instance.activate(project_id, activate_body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ObjectStorageApi->activate: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **activate_body** | [**ActivateBody**](ActivateBody.md)|  | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_object_storage_user**
> ObjectStorageUser create_object_storage_user(project_id, create_object_storage_user_body)

Create user that stores keys for storage buckets

### Example
```python
from __future__ import print_function
import time
import src.cudo_compute
from src.cudo_compute.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = src.cudo_compute.ObjectStorageApi()
project_id = 'project_id_example' # str | 
create_object_storage_user_body = src.cudo_compute.CreateObjectStorageUserBody() # CreateObjectStorageUserBody | 

try:
    # Create user that stores keys for storage buckets
    api_response = api_instance.create_object_storage_user(project_id, create_object_storage_user_body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ObjectStorageApi->create_object_storage_user: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **create_object_storage_user_body** | [**CreateObjectStorageUserBody**](CreateObjectStorageUserBody.md)|  | 

### Return type

[**ObjectStorageUser**](ObjectStorageUser.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_object_storage_key**
> DeleteObjectStorageKeyResponse delete_object_storage_key(project_id, id, access_key=access_key)

Delete object storage user

### Example
```python
from __future__ import print_function
import time
import src.cudo_compute
from src.cudo_compute.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = src.cudo_compute.ObjectStorageApi()
project_id = 'project_id_example' # str | 
id = 'id_example' # str | 
access_key = 'access_key_example' # str |  (optional)

try:
    # Delete object storage user
    api_response = api_instance.delete_object_storage_key(project_id, id, access_key=access_key)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ObjectStorageApi->delete_object_storage_key: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **id** | **str**|  | 
 **access_key** | **str**|  | [optional] 

### Return type

[**DeleteObjectStorageKeyResponse**](DeleteObjectStorageKeyResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_object_storage_user**
> DeleteObjectStorageUserResponse delete_object_storage_user(project_id, id)

Delete object storage user

### Example
```python
from __future__ import print_function
import time
import src.cudo_compute
from src.cudo_compute.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = src.cudo_compute.ObjectStorageApi()
project_id = 'project_id_example' # str | 
id = 'id_example' # str | 

try:
    # Delete object storage user
    api_response = api_instance.delete_object_storage_user(project_id, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ObjectStorageApi->delete_object_storage_user: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **id** | **str**|  | 

### Return type

[**DeleteObjectStorageUserResponse**](DeleteObjectStorageUserResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **generate_object_storage_key**
> ObjectStorageKey generate_object_storage_key(project_id, id, generate_object_storage_key_body)

Generate access key for storage buckets

### Example
```python
from __future__ import print_function
import time
import src.cudo_compute
from src.cudo_compute.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = src.cudo_compute.ObjectStorageApi()
project_id = 'project_id_example' # str | 
id = 'id_example' # str | 
generate_object_storage_key_body = NULL # object | 

try:
    # Generate access key for storage buckets
    api_response = api_instance.generate_object_storage_key(project_id, id, generate_object_storage_key_body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ObjectStorageApi->generate_object_storage_key: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **id** | **str**|  | 
 **generate_object_storage_key_body** | **object**|  | 

### Return type

[**ObjectStorageKey**](ObjectStorageKey.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_object_storage_bucket**
> ObjectStorageBucket get_object_storage_bucket(project_id, id)

Get details for a bucket

### Example
```python
from __future__ import print_function
import time
import src.cudo_compute
from src.cudo_compute.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = src.cudo_compute.ObjectStorageApi()
project_id = 'project_id_example' # str | 
id = 'id_example' # str | 

try:
    # Get details for a bucket
    api_response = api_instance.get_object_storage_bucket(project_id, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ObjectStorageApi->get_object_storage_bucket: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **id** | **str**|  | 

### Return type

[**ObjectStorageBucket**](ObjectStorageBucket.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_object_storage_session_key**
> GetObjectStorageSessionKeyResponse get_object_storage_session_key(project_id, data_center_id=data_center_id)

Generate temporary key for storage bucket access

### Example
```python
from __future__ import print_function
import time
import src.cudo_compute
from src.cudo_compute.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = src.cudo_compute.ObjectStorageApi()
project_id = 'project_id_example' # str | 
data_center_id = 'data_center_id_example' # str |  (optional)

try:
    # Generate temporary key for storage bucket access
    api_response = api_instance.get_object_storage_session_key(project_id, data_center_id=data_center_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ObjectStorageApi->get_object_storage_session_key: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **data_center_id** | **str**|  | [optional] 

### Return type

[**GetObjectStorageSessionKeyResponse**](GetObjectStorageSessionKeyResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_object_storage_buckets**
> ListObjectStorageBucketsResponse list_object_storage_buckets(project_id, page_number=page_number, page_size=page_size)

List buckets

### Example
```python
from __future__ import print_function
import time
import src.cudo_compute
from src.cudo_compute.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = src.cudo_compute.ObjectStorageApi()
project_id = 'project_id_example' # str | 
page_number = 56 # int |  (optional)
page_size = 56 # int |  (optional)

try:
    # List buckets
    api_response = api_instance.list_object_storage_buckets(project_id, page_number=page_number, page_size=page_size)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ObjectStorageApi->list_object_storage_buckets: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **page_number** | **int**|  | [optional] 
 **page_size** | **int**|  | [optional] 

### Return type

[**ListObjectStorageBucketsResponse**](ListObjectStorageBucketsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_object_storage_keys**
> ListObjectStorageKeysResponse list_object_storage_keys(project_id, id, page_number=page_number, page_size=page_size)

List storage user keys

### Example
```python
from __future__ import print_function
import time
import src.cudo_compute
from src.cudo_compute.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = src.cudo_compute.ObjectStorageApi()
project_id = 'project_id_example' # str | 
id = 'id_example' # str | 
page_number = 56 # int |  (optional)
page_size = 56 # int |  (optional)

try:
    # List storage user keys
    api_response = api_instance.list_object_storage_keys(project_id, id, page_number=page_number, page_size=page_size)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ObjectStorageApi->list_object_storage_keys: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **id** | **str**|  | 
 **page_number** | **int**|  | [optional] 
 **page_size** | **int**|  | [optional] 

### Return type

[**ListObjectStorageKeysResponse**](ListObjectStorageKeysResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_object_storage_users**
> ListObjectStorageUsersResponse list_object_storage_users(project_id, page_number=page_number, page_size=page_size)

List storage users

### Example
```python
from __future__ import print_function
import time
import src.cudo_compute
from src.cudo_compute.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = src.cudo_compute.ObjectStorageApi()
project_id = 'project_id_example' # str | 
page_number = 56 # int |  (optional)
page_size = 56 # int |  (optional)

try:
    # List storage users
    api_response = api_instance.list_object_storage_users(project_id, page_number=page_number, page_size=page_size)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ObjectStorageApi->list_object_storage_users: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **page_number** | **int**|  | [optional] 
 **page_size** | **int**|  | [optional] 

### Return type

[**ListObjectStorageUsersResponse**](ListObjectStorageUsersResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

