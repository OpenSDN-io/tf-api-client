REST API Details
================
The configuration API server provides a means of accessing and manipulating configuration
elements of the system using HTTP operations on resources represented in JSON.

The configuration element types (also referred to as resource types) have a hierarchical relationship 
described in :doc:`vnc_cfg.xsd` schema. JSON representation of these objects are what is 
expected on the wire.

For each resource type, the following APIs are available:
    * Create a resource
    * Read a resource given its UUID
    * Update a resource
    * Delete a resource given its UUID
    * List resources of given type

In addition, the following APIs are also available:
    * Listing all resource types
    * Convert FQ name to UUID
    * Convert UUID to FQ name
    * Add/Delete/Update a reference between two objects

Creating a resource
-------------------
To create a resource, a ``POST`` has to be issued on the collection URL.
So for a resource of type *example-resource*,

    * *METHOD*: POST 
    * *URL*: http://<ip>:<port>/example_resources/ 
    * *BODY*: JSON representation of example-resource type
    * *RESPONSE*: UUID and href of created resource

Example request ::

    curl -X POST -H "X-Auth-Token: $OS_TOKEN" -H "Content-Type: application/json; charset=UTF-8" -d '{"virtual-network": {"parent_type": "project", "fq_name": ["default-domain", "admin", "vn-blue"], "network_ipam_refs": [{"attr": {"ipam_subnets": [{"subnet": {"ip_prefix": "10.1.1.0", "ip_prefix_len": 24}}]}, "to": ["default-domain", "default-project", "default-network-ipam"]}]}}' http://10.84.14.2:8082/virtual-networks

Response ::

    {"virtual-network": {"fq_name": ["default-domain", "admin", "vn-blue"], "parent_uuid": "df7649a6-3e2c-4982-b0c3-4b5038eef587", "parent_href": "http://10.84.14.2:8082/project/df7649a6-3e2c-4982-b0c3-4b5038eef587", "uuid": "8c84ff8a-30ac-4136-99d9-f0d9662f3eee", "href": "http://10.84.14.2:8082/virtual-network/8c84ff8a-30ac-4136-99d9-f0d9662f3eee", "name": "vn-blue"}}

Reading a resource
-------------------
To read a resource, a ``GET`` has to be issued on the resource URL.

    * *METHOD*: GET
    * *URL*: http://<ip>:<port>/example_resource/<example-resource-uuid>
    * *BODY*: None
    * *RESPONSE*: JSON representation of the resource

Example request ::

    curl -X GET -H "X-Auth-Token: $OS_TOKEN" -H "Content-Type: application/json; charset=UTF-8" http://10.84.14.2:8082/virtual-network/8c84ff8a-30ac-4136-99d9-f0d9662f3eee

Response ::

    {"virtual-network": {"virtual_network_properties": {"network_id": 4, "vxlan_network_identifier": null, "extend_to_external_routers": null}, "fq_name": ["default-domain", "admin", "vn-blue"], "uuid": "8c84ff8a-30ac-4136-99d9-f0d9662f3eee", "access_control_lists": [{"to": ["default-domain", "admin", "vn-blue", "vn-blue"], "href": "http://10.84.14.2:8082/access-control-list/24b9c337-7be8-4883-a9a0-60197edf64e4", "uuid": "24b9c337-7be8-4883-a9a0-60197edf64e4"}], "network_policy_refs": [{"to": ["default-domain", "admin", "policy-red-blue"], "href": "http://10.84.14.2:8082/network-policy/f215a3ec-5cbd-4310-91f4-7bbca52b27bd", "attr": {"sequence": {"major": 0, "minor": 0}}, "uuid": "f215a3ec-5cbd-4310-91f4-7bbca52b27bd"}], "parent_uuid": "df7649a6-3e2c-4982-b0c3-4b5038eef587", "parent_href": "http://10.84.14.2:8082/project/df7649a6-3e2c-4982-b0c3-4b5038eef587", "parent_type": "project", "href": "http://10.84.14.2:8082/virtual-network/8c84ff8a-30ac-4136-99d9-f0d9662f3eee", "id_perms": {"enable": true, "description": null, "created": "2013-09-13T00:26:05.290644", "uuid": {"uuid_mslong": 10125498831222882614, "uuid_lslong": 11086156774262128366}, "last_modified": "2013-09-13T00:47:41.219833", "permissions": {"owner": "cloud-admin", "owner_access": 7, "other_access": 7, "group": "cloud-admin-group", "group_access": 7}}, "routing_instances": [{"to": ["default-domain", "admin", "vn-blue", "vn-blue"], "href": "http://10.84.14.2:8082/routing-instance/732567fd-8607-4045-b6c0-ff4109d3e0fb", "uuid": "732567fd-8607-4045-b6c0-ff4109d3e0fb"}], "network_ipam_refs": [{"to": ["default-domain", "default-project", "default-network-ipam"], "href": "http://10.84.14.2:8082/network-ipam/a01b486e-2c3e-47df-811c-440e59417ed8", "attr": {"ipam_subnets": [{"subnet": {"ip_prefix": "10.1.1.0", "ip_prefix_len": 24}, "default_gateway": "10.1.1.254"}]}, "uuid": "a01b486e-2c3e-47df-811c-440e59417ed8"}], "name": "vn-blue"}}

Updating a resource
--------------------
To update a resource, a ``PUT`` has to be issued on the resource URL.

    * *METHOD*: PUT
    * *URL*: http://<ip>:<port>/example_resource/<example-resource-uuid>
    * *BODY*: JSON representation of resource attributes that are changing
    * *RESPONSE*: UUID and href of updated resource

References to other resources are specified as a list of dictionaries with
"to" and  "attr" keys where "to" is the fully-qualified name of the resource
being referred to and "attr" is the data associated with the relation (if any).

Example request ::

    curl -X PUT -H "X-Auth-Token: $OS_TOKEN" -H "Content-Type: application/json; charset=UTF-8" -d '{"virtual-network": {"fq_name": ["default-domain", "admin", "vn-blue"],"network_policy_refs": [{"to": ["default-domain", "admin", "policy-red-blue"], "attr":{"sequence":{"major":0, "minor": 0}}}]}}' http://10.84.14.2:8082/virtual-network/8c84ff8a-30ac-4136-99d9-f0d9662f3eee

Response ::

    {"virtual-network": {"href": "http://10.84.14.2:8082/virtual-network/8c84ff8a-30ac-4136-99d9-f0d9662f3eee", "uuid": "8c84ff8a-30ac-4136-99d9-f0d9662f3eee"}}

Deleting a resource
-------------------
To delete a resource, a ``DELETE`` has to be issued on the resource URL 

    * *METHOD*: DELETE
    * *URL*: http://<ip>:<port>/example_resource/<example-resource-uuid>
    * *BODY*: None
    * *RESPONSE*: None

Example Request ::

    curl -X DELETE -H "X-Auth-Token: $OS_TOKEN" -H "Content-Type: application/json; charset=UTF-8" http://10.84.14.2:8082/virtual-network/47a91732-629b-4cbe-9aa5-45ba4d7b0e99

Response *None*

Listing Resources
-----------------
To list a set of resources, a ``GET`` has to be issued on the collection URL
with an optional query parameter mentioning the parent resource that contains
this collection. If parent resource is not mentioned, a resource named
'default-<parent-type>' is assumed.

    * *METHOD*: GET
    * *URL*: http://<ip>:<port>/example_resources
             http://<ip>:<port>/example_resources?parent_id=<parent_uuid> *OR*
             http://<ip>:<port>/example_resources?parent_fq_name_str=<parent's fully-qualified name delimited by ':'> *OR*
             http://<ip>:<port>/example_resources?obj_uuids=<example1_uuid>,<example2_uuid>&detail=True *OR*
             http://<ip>:<port>/example_resources?back_ref_id=<back_ref_uuid> *OR*
    * *BODY*: None
    * *RESPONSE*: JSON list of UUID and href of collection if detail not specified, else JSON list of collection dicts


Example request ::

    curl -X GET -H "X-Auth-Token: $OS_TOKEN" -H "Content-Type: application/json; charset=UTF-8" http://10.84.14.2:8082/virtual-networks

Response ::

    {"virtual-networks": [{"href": "http://10.84.14.2:8082/virtual-network/8c84ff8a-30ac-4136-99d9-f0d9662f3eee", "fq_name": ["default-domain", "admin", "vn-blue"], "uuid": "8c84ff8a-30ac-4136-99d9-f0d9662f3eee"}, {"href": "http://10.84.14.2:8082/virtual-network/47a91732-629b-4cbe-9aa5-45ba4d7b0e99", "fq_name": ["default-domain", "admin", "vn-red"], "uuid": "47a91732-629b-4cbe-9aa5-45ba4d7b0e99"}, {"href": "http://10.84.14.2:8082/virtual-network/f423b6c8-deb6-4325-9035-15a8c8bb0a0d", "fq_name": ["default-domain", "default-project", "__link_local__"], "uuid": "f423b6c8-deb6-4325-9035-15a8c8bb0a0d"}, {"href": "http://10.84.14.2:8082/virtual-network/d44a51b0-f2d8-4644-aee0-fe856f970683", "fq_name": ["default-domain", "default-project", "default-virtual-network"], "uuid": "d44a51b0-f2d8-4644-aee0-fe856f970683"}, {"href": "http://10.84.14.2:8082/virtual-network/aad9e80a-8638-449f-a484-5d1bfd58065c", "fq_name": ["default-domain", "default-project", "ip-fabric"], "uuid": "aad9e80a-8638-449f-a484-5d1bfd58065c"}]}

Discovering API server resources
--------------------------------
The resources managed by the server can be be obtained at the root URL(home-page). ::

    curl http://10.84.14.1:8082/ | python -m json.tool

Here is a sample output ::

    {
      "href": "http://10.84.14.2:8082",
      "links": [
        {
          "link": {
            "href": "http://10.84.14.2:8082/documentation/index.html",
            "name": "documentation",
            "rel": "documentation"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/config-root",
            "name": "config-root",
            "rel": "root"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/domains",
            "name": "domain",
            "rel": "collection"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/service-instances",
            "name": "service-instance",
            "rel": "collection"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/instance-ips",
            "name": "instance-ip",
            "rel": "collection"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/network-policys",
            "name": "network-policy",
            "rel": "collection"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/virtual-DNS-records",
            "name": "virtual-DNS-record",
            "rel": "collection"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/route-targets",
            "name": "route-target",
            "rel": "collection"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/floating-ips",
            "name": "floating-ip",
            "rel": "collection"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/floating-ip-pools",
            "name": "floating-ip-pool",
            "rel": "collection"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/bgp-routers",
            "name": "bgp-router",
            "rel": "collection"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/virtual-routers",
            "name": "virtual-router",
            "rel": "collection"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/global-system-configs",
            "name": "global-system-config",
            "rel": "collection"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/namespaces",
            "name": "namespace",
            "rel": "collection"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/provider-attachments",
            "name": "provider-attachment",
            "rel": "collection"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/virtual-DNSs",
            "name": "virtual-DNS",
            "rel": "collection"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/customer-attachments",
            "name": "customer-attachment",
            "rel": "collection"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/virtual-machines",
            "name": "virtual-machine",
            "rel": "collection"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/service-templates",
            "name": "service-template",
            "rel": "collection"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/security-groups",
            "name": "security-group",
            "rel": "collection"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/access-control-lists",
            "name": "access-control-list",
            "rel": "collection"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/network-ipams",
            "name": "network-ipam",
            "rel": "collection"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/virtual-networks",
            "name": "virtual-network",
            "rel": "collection"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/projects",
            "name": "project",
            "rel": "collection"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/routing-instances",
            "name": "routing-instance",
            "rel": "collection"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/virtual-machine-interfaces",
            "name": "virtual-machine-interface",
            "rel": "collection"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/domain",
            "name": "domain",
            "rel": "resource-base"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/service-instance",
            "name": "service-instance",
            "rel": "resource-base"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/instance-ip",
            "name": "instance-ip",
            "rel": "resource-base"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/network-policy",
            "name": "network-policy",
            "rel": "resource-base"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/virtual-DNS-record",
            "name": "virtual-DNS-record",
            "rel": "resource-base"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/route-target",
            "name": "route-target",
            "rel": "resource-base"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/floating-ip",
            "name": "floating-ip",
            "rel": "resource-base"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/floating-ip-pool",
            "name": "floating-ip-pool",
            "rel": "resource-base"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/bgp-router",
            "name": "bgp-router",
            "rel": "resource-base"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/virtual-router",
            "name": "virtual-router",
            "rel": "resource-base"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/config-root",
            "name": "config-root",
            "rel": "resource-base"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/global-system-config",
            "name": "global-system-config",
            "rel": "resource-base"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/namespace",
            "name": "namespace",
            "rel": "resource-base"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/provider-attachment",
            "name": "provider-attachment",
            "rel": "resource-base"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/virtual-DNS",
            "name": "virtual-DNS",
            "rel": "resource-base"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/customer-attachment",
            "name": "customer-attachment",
            "rel": "resource-base"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/virtual-machine",
            "name": "virtual-machine",
            "rel": "resource-base"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/service-template",
            "name": "service-template",
            "rel": "resource-base"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/security-group",
            "name": "security-group",
            "rel": "resource-base"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/access-control-list",
            "name": "access-control-list",
            "rel": "resource-base"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/network-ipam",
            "name": "network-ipam",
            "rel": "resource-base"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/virtual-network",
            "name": "virtual-network",
            "rel": "resource-base"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/project",
            "name": "project",
            "rel": "resource-base"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/routing-instance",
            "name": "routing-instance",
            "rel": "resource-base"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/virtual-machine-interface",
            "name": "virtual-machine-interface",
            "rel": "resource-base"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/fqname-to-id",
            "name": "name-to-id",
            "rel": "action"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/id-to-fqname",
            "name": "id-to-name",
            "rel": "action"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/useragent-kv",
            "name": "useragent-keyvalue",
            "rel": "action"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/virtual-network/%s/ip-alloc",
            "name": "virtual-network-ip-alloc",
            "rel": "action"
          }
        },
        {
          "link": {
            "href": "http://10.84.14.2:8082/virtual-network/%s/ip-free",
            "name": "virtual-network-ip-free",
            "rel": "action"
          }
        }
      ]
    }

Converting FQ name to UUID
--------------------------
To find the UUID of a resource, given its fq name ::

    curl -X POST -H "X-Auth-Token: $OS_TOKEN" -H "Content-Type: application/json; charset=UTF-8" -d '{"fq_name": ["default-domain", "admin", "vn-blue"], "type": "virtual-network"}' http://10.84.14.2:8082/fqname-to-id

Here is a sample output ::

    {"uuid": "e3a20048-8cc7-4cff-8c3b-ada61eb822ed"}
    
Converting UUID to FQ name
--------------------------
To find the type and FQ name of a resource, given its UUID ::

    curl -X POST -H "X-Auth-Token: $OS_TOKEN" -H "Content-Type: application/json; charset=UTF-8" -d '{"uuid": "e3a20048-8cc7-4cff-8c3b-ada61eb822ed"}' http://10.84.14.2:8082/id-to-fqname

Here is a sample output ::

    {"type": "virtual-network", "fq_name": ["default-domain", "admin", "vn-blue"]}
    
Adding/Deleting/Updating a reference between two objects
--------------------------------------------------------

To add/delete/update a reference between two objects, you don't need to read and send the entire object. You can atomically update a single reference by using this API. 
To add or update a reference::

    curl -X POST -H "X-Auth-Token: $OS_TOKEN" -H "Content-Type: application/json; charset=UTF-8" -d '{"operation": "ADD", "uuid": "e3a20048-8cc7-4cff-8c3b-ada61eb822ed", "type": "virtual-network", "ref-type": "network-policy", "ref-uuid": "7810b656-97d9-4c43-94c7-bd52cc4b055d", "attr": {"sequence": {"major": 0, "minor": 0}}}' http://10.84.14.2:8082/ref-update

Note that instead of the ref-uuid, you can also specify ref-fq-name::

    curl -X POST -H "X-Auth-Token: $OS_TOKEN" -H "Content-Type: application/json; charset=UTF-8" -d '{"operation": "ADD", "uuid": "e3a20048-8cc7-4cff-8c3b-ada61eb822ed", "type": "virtual-network", "ref-type": "network-policy", "ref-fq-name": ["default-domain", "default-project", "default-network-policy"], "attr": {"sequence": {"major": 0, "minor": 0}}}' http://10.84.14.2:8082/ref-update

To delete a reference::

    curl -X POST -H "X-Auth-Token: $OS_TOKEN" -H "Content-Type: application/json; charset=UTF-8" -d '{"operation": "DELETE", "uuid": "e3a20048-8cc7-4cff-8c3b-ada61eb822ed", "type": "virtual-network", "ref-type": "network-policy", "ref-uuid": "7810b656-97d9-4c43-94c7-bd52cc4b055d"}' http://10.84.14.2:8082/ref-update



Updating a property collection
------------------------------

To add, delete, or modify elements within a list or map property atomically, you can use the property collection update API. This is particularly useful for managing large collections (like key-value pairs or community lists) without re-sending the entire object.

The supported operations depend on the collection type:
    * **Lists**: ``ADD``, ``MODIFY``, ``DELETE`` (requires a ``position`` index).
    * **Maps**: ``SET``, ``DELETE`` (requires a ``field`` key).

To update a collection property::

    curl -X POST -H "X-Auth-Token: $OS_TOKEN" -H "Content-Type: application/json; charset=UTF-8" -d '{
        "uuid": "e3a20048-8cc7-4cff-8c3b-ada61eb822ed",
        "updates": [
            {
                "field": "annotations",
                "operation": "SET",
                "value": {"key": "deployment-stage", "value": "production"}
            }
        ]
    }' http://10.84.14.2:8082/prop-collection-update

For list properties, you can specify the position for a ``MODIFY`` or ``DELETE`` operation::

    curl -X POST -H "X-Auth-Token: $OS_TOKEN" -H "Content-Type: application/json; charset=UTF-8" -d '{
        "uuid": "e3a20048-8cc7-4cff-8c3b-ada61eb822ed",
        "updates": [
            {
                "field": "community_list",
                "operation": "DELETE",
                "position": "0"
            }
        ]
    }' http://10.84.14.2:8082/prop-collection-update


Reading a property collection
-----------------------------

To retrieve specific elements from a list or map property without fetching the entire resource, use the property collection get API. This method is optimized for querying large data sets stored within object properties.

    * **METHOD**: GET
    * **URL**: ``http://<ip>:<port>/prop-collection-get?uuid=<obj_uuid>&fields=<field1,field2>&position=<index_or_key>``
    * **PARAMS**:
        * ``uuid``: (Mandatory) The UUID of the resource.
        * ``fields``: (Mandatory) A comma-separated list of property names (must be of type ListProperty or MapProperty).
        * ``position``: (Optional) A specific index for lists or a key for maps to filter the result.
    * **RESPONSE**: JSON object containing the requested collection data.

Example request ::

    curl -X GET -H "X-Auth-Token: $OS_TOKEN" "http://10.84.14.2:8082/prop-collection-get?uuid=e3a20048-8cc7-4cff-8c3b-ada61eb822ed&fields=community_list"

Example request with position filtering ::

    curl -X GET -H "X-Auth-Token: $OS_TOKEN" "http://10.84.14.2:8082/prop-collection-get?uuid=e3a20048-8cc7-4cff-8c3b-ada61eb822ed&fields=annotations&position=deployment-stage"

Response ::

    {"annotations": [{"key": "deployment-stage", "value": "production"}]}

Atomic Reference Updates
------------------------

To manage relationships between resources without modifying the entire object, use the reference update API. This allows for atomic addition or removal of links (references) between two existing objects.

    * **METHOD**: POST
    * **URL**: ``http://<ip>:<port>/ref-update``
    * **BODY**: A JSON object specifying the source, the target, and the operation.

**Key Parameters:**
    * ``type``: Type of the source resource (e.g., "virtual-network").
    * ``uuid``: UUID of the source resource.
    * ``ref-type``: Type of the target resource to be linked/unlinked.
    * ``operation``: Either ``ADD`` or ``DELETE``.
    * ``ref-uuid`` or ``ref-fq-name``: Identification of the target resource.
    * ``attr``: (Optional) Metadata associated with the reference (e.g., sequence numbers, properties).

Adding or Updating a reference::

    curl -X POST -H "X-Auth-Token: $OS_TOKEN" -H "Content-Type: application/json" -d '{
        "type": "virtual-network",
        "uuid": "e3a20048-8cc7-4cff-8c3b-ada61eb822ed",
        "ref-type": "network-policy",
        "operation": "ADD",
        "ref-uuid": "7810b656-97d9-4c43-94c7-bd52cc4b055d",
        "attr": {"sequence": {"major": 0, "minor": 0}}
    }' http://10.84.14.2:8082/ref-update

Deleting a reference::

    curl -X POST -H "X-Auth-Token: $OS_TOKEN" -H "Content-Type: application/json" -d '{
        "type": "virtual-network",
        "uuid": "e3a20048-8cc7-4cff-8c3b-ada61eb822ed",
        "ref-type": "network-policy",
        "operation": "DELETE",
        "ref-fq-name": ["default-domain", "default-project", "default-network-policy"]
    }' http://10.84.14.2:8082/ref-update

Note that if the reference already exists, an ``ADD`` operation will update the associated ``attr`` data.

Relaxing References for Deletion
--------------------------------

In systems with strict referential integrity, an object cannot be deleted if it is still being referenced by other objects. The Reference Relax API allows you to bypass these constraints for a specific relationship, marking it as "relaxed" so the target object can be safely removed.

    * **METHOD**: POST
    * **URL**: ``http://<ip>:<port>/ref-relax-for-delete``
    * **BODY**: A JSON object specifying the source and the target of the reference.

**Key Parameters:**
    * ``uuid``: UUID of the object that *holds* the reference.
    * ``ref-uuid``: UUID of the object being *pointed to* (the one you intend to delete).

Example request ::

    curl -X POST -H "X-Auth-Token: $OS_TOKEN" -H "Content-Type: application/json" -d '{
        "uuid": "source-object-uuid-12345",
        "ref-uuid": "target-object-uuid-67890"
    }' http://10.84.14.2:8082/ref-relax-for-delete

Response ::

    {"uuid": "source-object-uuid-12345"}

.. note::
   This is an advanced administrative operation. Use it only when standard reference deletion (via ``ref-update``) is insufficient or when dealing with complex circular dependencies.

Converting FQ name to UUID
--------------------------

This API translates a resource's fully-qualified name (FQ Name) into its internal unique identifier (UUID). It is commonly used as a discovery step before performing operations that require a UUID.

    * **METHOD**: POST
    * **URL**: ``http://<ip>:<port>/fqname-to-id``
    * **BODY**: A JSON object containing the resource type and its FQ Name.

**Key Parameters:**
    * ``type``: The resource type (e.g., "virtual-network", "project").
    * ``fq_name``: An array of strings representing the full path to the object.

Example request ::

    curl -X POST -H "X-Auth-Token: $OS_TOKEN" -H "Content-Type: application/json" -d '{
        "type": "virtual-network",
        "fq_name": ["default-domain", "admin", "vn-blue"]
    }' http://10.84.14.2:8082/fqname-to-id

Response ::

    {"uuid": "e3a20048-8cc7-4cff-8c3b-ada61eb822ed"}

.. note::
   The API server performs a permission check before returning the UUID. If the authenticated user does not have at least ``READ`` permissions for the identified object, the request will fail even if the name is correct.

Converting UUID to FQ name
--------------------------

This API performs a reverse lookup, converting an internal UUID into its resource type and fully-qualified name (FQ Name).

    * **METHOD**: POST
    * **URL**: ``http://<ip>:<port>/id-to-fqname``
    * **BODY**: A JSON object containing the resource UUID.

**Key Parameters:**
    * ``uuid``: The internal unique identifier of the resource.

Example request ::

    curl -X POST -H "X-Auth-Token: $OS_TOKEN" -H "Content-Type: application/json" -d '{
        "uuid": "e3a20048-8cc7-4cff-8c3b-ada61eb822ed"
    }' http://10.84.14.2:8082/id-to-fqname

Response ::

    {
        "type": "virtual-network",
        "fq_name": ["default-domain", "admin", "vn-blue"]
    }

.. note::
   Access control is strictly enforced. Even if a UUID exists in the database, the server will return a ``403 Forbidden`` or ``404 Not Found`` if the user's token does not grant ``READ`` permissions for that specific resource.

User-Agent Key-Value Store
--------------------------

The API server provides a simple key-value storage service. This can be used to store, retrieve, or delete arbitrary string data associated with specific keys.

    * **METHOD**: POST
    * **URL**: ``http://<ip>:<port>/useragent-kv``
    * **BODY**: A JSON object containing the operation, key, and optional value.

**Operations:**
    * ``STORE``: Saves or updates the value for a given key.
    * ``RETRIEVE``: Returns the value associated with the key.
    * ``DELETE``: Removes the key and its value from the store.

Example: Storing a value ::

    curl -X POST -H "X-Auth-Token: $OS_TOKEN" -H "Content-Type: application/json" -d '{
        "operation": "STORE",
        "key": "my-custom-metadata",
        "value": "some-random-string-data"
    }' http://10.84.14.2:8082/useragent-kv

Example: Retrieving a value ::

    curl -X POST -H "X-Auth-Token: $OS_TOKEN" -H "Content-Type: application/json" -d '{
        "operation": "RETRIEVE",
        "key": "my-custom-metadata"
    }' http://10.84.14.2:8082/useragent-kv

Response ::

    {"value": "some-random-string-data"}

Database Consistency Check
--------------------------

The Database Check API allows administrators to perform a comprehensive scan of the underlying Cassandra database to identify inconsistencies or read errors.

This is a read-only operation that does not modify any data.

    * **METHOD**: POST
    * **URL**: ``http://<ip>:<port>/db-check``
    * **BODY**: None
    * **RESPONSE**: A JSON object containing a list of scan results and any encountered anomalies.

**What this operation does:**
    * **Full Database Walk**: The server iterates through all resource types and UUIDs stored in the database.
    * **Metadata Validation**: Checks if essential fields like ``type`` and ``fq_name`` are present and correctly formatted (JSON-parseable).
    * **Caching**: During the scan, it populates the internal UUID-to-FQ-Name cache to optimize subsequent operations.
    * **Error Reporting**: Captures and reports read exceptions or structural issues for each object type.

Example request ::

    curl -X POST -H "X-Auth-Token: $OS_TOKEN" http://10.84.14.2:8082/db-check

Response ::

    {
        "results": [
            "Consistency check passed for 500 virtual-networks",
            "Error in db walk read: Invalid JSON in type field for UUID 8c84ff8a-..."
        ]
    }

.. note::
   Since this operation performs a full walk of the Cassandra Column Family, it can be resource-intensive on large deployments. It is recommended to run this during maintenance windows or when database corruption is suspected.

Fetching All Database Records
-----------------------------

The Fetch Records API performs a global read operation, retrieving the complete JSON representation of every resource stored in the configuration database.

    * **METHOD**: POST
    * **URL**: ``http://<ip>:<port>/fetch-records``
    * **BODY**: None
    * **RESPONSE**: A JSON object containing nested arrays of all objects.

**Key Difference from db-check:**
Unlike ``db-check``, which only validates the existence and metadata of objects, ``fetch-records`` extracts the **entire payload** of every resource. Use this for full system audits or data migrations.

**Operational Details:**
    * **Raw Data Access**: Bypasses standard API filters to fetch records directly as they are stored in the backend.
    * **Explicit Identity**: Each record in the result is automatically injected with its ``type`` and ``uuid`` fields by the server for easy parsing.
    * **Resilience**: The process is designed to skip individual corrupted records (logging them as errors) without halting the entire export.

Example request ::

    curl -X POST -H "X-Auth-Token: $OS_TOKEN" http://10.84.14.2:8082/fetch-records

Response ::

    {
        "results": [
            [
                {
                    "type": "virtual-network",
                    "uuid": "8c84ff8a-30ac-4136-99d9-f0d9662f3eee",
                    "name": "vn-blue",
                    "id_perms": {...},
                    "virtual_network_properties": {...}
                }
            ]
        ]
    }

.. warning::
   **High Resource Usage**: This operation is the most expensive in the API. On large databases, it may lead to high memory consumption on the API server and increased load on Cassandra.

Bulk Collection Listing
-----------------------

Standard GET requests for collections have URL length limits. The Bulk Collection API allows you to query large sets of resources by providing parameters in a JSON body via a POST request.

    * **METHOD**: POST
    * **URL**: ``http://<ip>:<port>/list-bulk-collection``
    * **BODY**: A JSON object containing filtering and pagination criteria.

**Key Parameters:**
    * ``type``: (Mandatory) Resource type to list (e.g., "virtual-network").
    * ``obj_uuids``: A comma-separated string of specific UUIDs to retrieve.
    * ``parent_id``: Filter by parent UUIDs (comma-separated).
    * ``back_ref_id``: Filter by back-reference UUIDs (comma-separated).
    * ``detail``: Boolean. If true, returns full object details instead of just references.
    * ``fields``: Comma-separated list of specific fields to include in the response.
    * ``filters``: Key-value pairs for attribute-based filtering.
    * ``page_limit`` / ``page_marker``: Parameters for pagination.

Example: Fetching specific details for a large list of UUIDs ::

    curl -X POST -H "X-Auth-Token: $OS_TOKEN" -H "Content-Type: application/json" -d '{
        "type": "virtual-machine-interface",
        "obj_uuids": "uuid-1,uuid-2,uuid-3,...,uuid-500",
        "detail": true,
        "fields": "virtual_machine_interface_mac_addresses,routing_instance_refs"
    }' http://10.84.14.2:8082/list-bulk-collection

Response ::

    {
        "virtual-machine-interfaces": [
            { "uuid": "uuid-1", "virtual_machine_interface_mac_addresses": {...}, ... },
            ...
        ]
    }

Checking Object Permissions
---------------------------

The Object Permissions API allows you to inspect the current user's access level for a specific resource, as well as retrieve metadata about the authenticated session (roles, domain, and project context).

    * **METHOD**: GET
    * **URL**: ``http://<ip>:<port>/obj-perms?uuid=<obj_uuid>``
    * **PARAMS**:
        * ``uuid``: (Optional) The UUID of the resource to check permissions for.
    * **RESPONSE**: A JSON object containing token information and effective permissions.

**Response Fields:**
    * ``token_info``: Detailed information about the Keystone token (roles, project, domain).
    * ``is_cloud_admin_role``: Boolean. True if the user has administrative privileges.
    * ``is_global_read_only_role``: Boolean. True if the user has global read-only access.
    * ``permissions``: (Returned only if UUID is provided) A string representing access level, e.g., ``"RWX"`` (Read, Write, Execute).

Example request ::

    curl -X GET -H "X-Auth-Token: $OS_TOKEN" "http://10.84.14.2:8082/obj-perms?uuid=e3a20048-8cc7-4cff-8c3b-ada61eb822ed"

Response ::

    {
        "is_cloud_admin_role": false,
        "is_global_read_only_role": true,
        "permissions": "R",
        "token_info": { ... }
    }

.. note::
   If authentication is disabled in the API server configuration, this method will always return ``permissions: "RWX"`` and ``is_cloud_admin_role: false``.

Changing Resource Ownership (chown)
-----------------------------------

The ``chown`` API allows administrators or resource owners to transfer ownership of a configuration object to a different project or user. Ownership is stored within the ``perms2`` control block of the resource.

    * **METHOD**: POST
    * **URL**: ``http://<ip>:<port>/obj-chown``
    * **BODY**: A JSON object specifying the target resource and the new owner.

**Key Parameters:**
    * ``uuid``: (Mandatory) The UUID of the resource to be modified.
    * ``owner``: (Mandatory) The UUID of the new owner (typically a Project UUID).

Example request ::

    curl -X POST -H "X-Auth-Token: $OS_TOKEN" -H "Content-Type: application/json" -d '{
        "uuid": "e3a20048-8cc7-4cff-8c3b-ada61eb822ed",
        "owner": "df7649a6-3e2c-4982-b0c3-4b5038eef587"
    }' http://10.84.14.2:8082/obj-chown

Response ::

    {}

.. note::
   **Permissions Requirement**: To perform a ``chown`` operation, the authenticated user must have both Read (R) and Write (W) permissions on the target object. If these permissions are missing, the server returns a ``403 Forbidden`` error.

Changing Access Permissions (chmod)
-----------------------------------

The ``chmod`` API provides fine-grained control over resource access. It allows you to modify the owner's access level, share the resource with specific projects (tenants), or set global permissions.

These permissions are stored in the ``perms2`` block and govern how the RBAC (Role-Based Access Control) engine evaluates requests.

    * **METHOD**: POST
    * **URL**: ``http://<ip>:<port>/obj-chmod``
    * **BODY**: A JSON object containing the target UUID and the desired permission changes.

**Permission Bitmask Values:**
    * ``7``: Full access (Read, Write, Execute)
    * ``5``: Read and Execute
    * ``4``: Read only
    * ``0``: No access

**Key Parameters:**
    * ``uuid``: (Mandatory) The UUID of the resource to modify.
    * ``owner``: (Optional) New owner UUID (normalizes by removing dashes).
    * ``owner_access``: (Optional) Integer bitmask for the owner's access level.
    * ``global_access``: (Optional) Integer bitmask for all users in the system. Setting this to a non-zero value automatically sets the ``is_shared`` flag.
    * ``share``: (Optional) A list of dictionaries for sharing with specific projects/domains.
        * ``tenant``: Format is ``domain:<uuid>`` or ``tenant:<uuid>``.
        * ``tenant_access``: Integer bitmask for that specific tenant.

Example: Sharing a resource with another project ::

    curl -X POST -H "X-Auth-Token: $OS_TOKEN" -H "Content-Type: application/json" -d '{
        "uuid": "e3a20048-8cc7-4cff-8c3b-ada61eb822ed",
        "share": [
            {
                "tenant": "tenant:df7649a6-3e2c-4982-b0c3-4b5038eef587",
                "tenant_access": 4
            }
        ],
        "global_access": 0
    }' http://10.84.14.2:8082/obj-chmod

Response ::

    {}

.. important::
   **Security Pre-requisite**: Just like ``chown``, the user must already have **Read (R)** and **Write (W)** permissions on the object to call ``chmod``.

Global AAA Mode Management
==========================

The AAA (Authentication, Authorization, and Accounting) Mode API is the master switch for the API Server's security posture. It defines the global strategy for validating user identity and enforcing access controls.

Setting the Operating Mode
--------------------------

This operation allows a Cloud Administrator to dynamically transition the cluster between different security levels.

* **Method**: ``PUT``
* **URL**: ``/aaa-mode``
* **Authentication**: Required (must have Cloud Admin privileges).
* **Body Parameters**:
    * ``aaa-mode`` (string, mandatory): The security level to enforce.

**Valid AAA Modes:**

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - Mode
     - Description
   * - ``no-auth``
     - **Disabled**. No token validation is performed. Every request is treated as having full administrative privileges.
   * - ``cloud-admin``
     - **Token-based**. Requires a valid OpenStack Keystone token. Access is granted based on the presence of the admin role.
   * - ``rbac``
     - **Role-Based Access Control**. The strictest mode. Validates tokens AND checks every action against the internal RBAC rule database.



Request Example::

    curl -X PUT -H "X-Auth-Token: $OS_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{"aaa-mode": "rbac"}' \
         http://127.0.0.1:8082/aaa-mode

Response Example::

    {
        "aaa-mode": "rbac"
    }

Detailed Internal Logic
-----------------------

### 1. Multi-Stage Authorization
Before the mode is updated, the API Server performs a rigorous check to prevent unauthorized security changes:

1. **Token Validation**: The server extracts the token from ``X-Auth-Token`` or ``X-User-Token``. It uses an internal ``AuthProtocol`` middleware (Keystone) to verify the token's signature and expiration.
2. **Identity Isolation**: During validation, the server creates an ``ApiInternalRequest``. This ensures the authentication check happens in a clean context, preventing side effects on other active sessions.
3. **Admin Privilege Verification**: The method ``is_admin_request()`` inspects the ``X-Role`` or ``X-API-Role`` headers. The change is rejected with a ``403 Forbidden`` error unless the user possesses the specific ``cloud_admin_role`` defined in the configuration.



### 2. Automatic RBAC Initialization
A critical safety mechanism is triggered when switching to ``rbac`` mode:

* **Default Rule Creation**: If the mode is set to ``rbac``, the server immediately executes ``_create_default_rbac_rule()``.
* **Prevention of Lockouts**: This ensures that even if no custom rules have been defined yet, a baseline set of permissions is created so that administrators can still access the API to configure further rules. Without this, enabling RBAC would immediately block all API access.

### 3. Middleware Interaction
The server interacts with OpenStack's ``auth_token`` middleware using the ``delay_auth_decision = True`` flag. This allows the API Server to:
* Receive the validation results without the middleware automatically terminating the request.
* Log detailed security errors via the ``config_object_error`` mechanism.
* Decide whether to allow the request based on internal logic (e.g., allowing internal IPC requests even if the token is missing).



Error Codes
-----------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - Code
     - Condition
   * - **400**
     - Invalid ``aaa-mode

Inspecting the Object Cache (dump-cache)
========================================

The ``dump-cache`` API provides a diagnostic view of the API Server's internal memory. It allows administrators to inspect the current state of cached objects, which is essential for troubleshooting synchronization issues between the API Server and the backend database (Cassandra).

Cache Management Overview
-------------------------

The API Server maintains an in-memory cache managed by the ``_obj_cache_mgr``. This cache stores Python object representations of resources to avoid repeated database lookups and JSON parsing.

* **Method**: ``POST``
* **URL**: ``/obj-cache``
* **Authentication**: Required (Cloud Admin privileges).
* **Body Parameters**:
    * ``uuids`` (list, optional): A specific list of UUIDs to retrieve from the cache.
    * ``count`` (integer, optional): The maximum number of records to return if no specific UUIDs are provided. Default is ``10``.



Request Example::

    curl -X POST -H "X-Auth-Token: $OS_TOKEN" \
         -H "Content-Type: application/json" \
         -d '{"count": 2, "uuids": ["e3a20048-8cc7-4cff-8c3b-ada61eb822ed"]}' \
         http://127.0.0.1:8082/obj-cache

Detailed Internal Logic
-----------------------

### 1. Extraction Strategy
The method ``dump_cache`` operates in two distinct modes based on the input:

1. **Targeted Mode (UUID-based)**:
   The server iterates through the provided ``obj_uuids``. If an object exists in the ``_cache`` dictionary, it is extracted. If a UUID is missing from the cache, it is silently skipped (no error is raised), allowing for batch inspection of potentially cached items.

2. **Sampling Mode (Count-based)**:
   If the ``uuids`` list is empty or not provided, the server performs a partial dump of the cache. It iterates through the internal keys up to the limit specified by ``count``. This is useful for checking the general health and variety of cached data without overloading the response.

### 2. Object-to-JSON Serialization
Since the cache stores live Python objects (instances of resource classes), they cannot be directly returned as JSON. The method employs a custom serialization logic:

* **Lambda Transformer**: It uses a specialized ``default`` handler in ``json.dumps``:
  ``lambda o: dict((k, v) for k, v in list(o.__dict__.items()))``
* **Reflective Inspection**: This logic dynamically converts the object's internal ``__dict__`` (which contains all attributes and values) into a standard Python dictionary.
* **Consistency Check**: After transforming the object to a JSON string, it is immediately parsed back into a dictionary using ``json.loads``. This ensures that the returned data is a clean, serializable snapshot that doesn't contain active memory references.



### 3. Response Structure
The response is returned as a numbered dictionary where keys represent the sequence of extraction (e.g., ``"1"``, ``"2"``, etc.). Each value is a complete representation of the cached object including:
* Metadata (perms, UUIDs).
* Resource-specific properties.
* Current reference states.

Operational Impact
------------------

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - Aspect
     - Impact Description
   * - **Performance**
     - Large ``count`` values or very large objects can lead to temporary spikes in CPU usage due to the intensive JSON serialization/deserialization process.
   * - **Security**
     - This dump contains raw object data. It should only be accessible by trusted administrators as it may reveal internal system structures and relationships.
   * - **Consistency**
     - A ``KeyError`` during Targeted Mode indicates that the object is not currently in memory. This helps determine if the server is correctly caching resources under load.

.. note::
   The cache dump represents a point-in-time snapshot. In high-churn environments, objects may be evicted or updated immediately after the dump is generated.

Error Handling
--------------

* **400 Bad Request**: Raised if the JSON body is malformed.
* **Empty Result**: If the specified UUIDs are not found in the cache, the API returns an empty dictionary ``{}`` rather than a 404 error, signifying that while the API call was successful, the cache does not contain those specific entries.

Remote Job Execution (execute-job)
==================================

The ``execute-job`` API is the gateway for triggering automated workflows (Jobs) in the Contrail/OpenSDN controller. It serves as an asynchronous coordinator that validates requests, gathers cluster context, and hands off tasks to the Job Manager via a message bus.

Operation Overview
------------------

Unlike standard resource CRUD operations, this API initiates a background process. The API server acts as a **Producer**, publishing a job request to RabbitMQ, where it is later consumed by a Job Manager worker.

* **Method**: ``POST``
* **URL**: ``/execute-job``
* **Authentication**: Required (Keystone token).
* **Return Value**: A unique ``job_execution_id`` for tracking.



Request Body Structure
----------------------

The request must identify a pre-configured **Job Template** and optionally provide parameters for execution.

.. list-table::
   :widths: 25 15 60
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - ``job_template_id``
     - UUID
     - The UUID of the job template (Mandatory if FQ Name is missing).
   * - ``job_template_fq_name``
     - List
     - The Fully Qualified Name of the job template (e.g., ``["default-global-system-config", "my-playbook"]``).
   * - ``input``
     - JSON
     - Custom data schema required by the specific Ansible playbook.
   * - ``params``
     - JSON
     - Execution parameters, such as ``device_list`` (a list of target device UUIDs).

Example Request::

    curl -X POST -H "X-Auth-Token: $OS_TOKEN" -H "Content-Type: application/json" -d '{
        "job_template_id": "8c84ff8a-30ac-4136-99d9-f0d9662f3eee",
        "params": {
            "device_list": ["7810b656-97d9-4c43-94c7-bd52cc4b055d"]
        }
    }' http://127.0.0.1:8082/execute-job

Detailed Execution Workflow
---------------------------

### 1. Template Resolution and Validation
The server ensures that the job template exists and is correctly identified:
* **Cross-Resolution**: If you provide a UUID, the server lookups the FQ Name; if you provide an FQ Name, it retrieves the UUID. Both are added to the final request payload.
* **Device Validation**: If a ``device_list`` is provided, the server strictly validates that every entry is a syntactically correct UUID (string format).

### 2. Context Gathering
To allow the Job Manager to interact back with the API, the server enriches the request with:
* **Auth Tokens**: The current ``X-Auth-Token`` is embedded into the payload so the background job can authenticate its own API calls.
* **Cluster Context**: Retrieves the ``X-Cluster-ID`` and a list of all active **Config Nodes** (API Server IP addresses) from the database. This allows the job to know which API servers are available for callback.

### 3. Execution ID Generation
A unique identifier is generated using a combination of the current timestamp (in milliseconds) and a random UUID4:
``execution_id = <timestamp>_<uuid4>``
This ensures that job results can be tracked uniquely even if multiple jobs are triggered at the exact same millisecond.

### 4. RabbitMQ Publishing (Reliable Delivery)
The final payload is sent to the ``JOB_REQUEST_EXCHANGE``. The system uses a robust retry policy to ensure the job is not lost if the message broker is temporarily busy:
* **Routing Key**: Uses a specific key defined for job requests.
* **Retry Policy**: 12 attempts with exponential backoff (starting at 2s, increasing to a maximum of 15s between tries).



Error Handling
--------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - Code
     - Condition
   * - **400**
     - Malformed input, such as an invalid ``device_list`` (not a list) or invalid UUID strings.
   * - **404**
     - The specified ``job_template_id`` or ``fq_name`` does not exist in the database.
   * - **500**
     - Failed to fetch the Config Node list or failed to publish the message to RabbitMQ after all retries.

Lifecycle Notice
----------------

The ``job_execution_id`` returned by this API does not mean the job is finished. It only confirms the job has been **queued**. To check the status or output of the job, you must query the corresponding ``job-status`` UVEs (User Visible Entities) via the Analytics API.

Aborting a Remote Job (abort-job)
=================================

The ``abort-job`` API provides a mechanism to request the cancellation of a previously initiated background job. Since jobs (like Ansible playbooks) run asynchronously on distributed Job Managers, the API Server acts as a signaling service to broadcast the abort request.

Operation Overview
------------------

Aborting a job is a non-blocking, asynchronous operation. The API Server does not kill the process directly; instead, it publishes an "abort signal" to a specific RabbitMQ exchange. The Job Manager responsible for the task listens for these signals and handles the graceful (or forced) termination of the execution.

* **Method**: ``POST``
* **URL**: ``/abort-job``
* **Authentication**: Required (Cloud Admin or Job Owner privileges).
* **Return Value**: An empty JSON object ``{}`` upon successful queuing of the abort request.



Request Body Structure
----------------------

The request must contain the unique identifier of the execution you wish to stop.

.. list-table::
   :widths: 25 15 60
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - ``job_execution_id``
     - String
     - (Mandatory) The unique ID returned by the initial ``execute-job`` call.
   * - ``job_template_id``
     - UUID
     - (Optional) The UUID of the template associated with the job.

Example Request::

    curl -X POST -H "X-Auth-Token: $OS_TOKEN" -H "Content-Type: application/json" -d '{
        "job_execution_id": "1708865400000_8c84ff8a-30ac-4136-99d9-f0d9662f3eee"
    }' http://127.0.0.1:8082/abort-job

Detailed Internal Logic
-----------------------

### 1. Context Enrichment
Similar to the execution process, the API Server attaches environmental context to the abort signal. This ensures the Job Manager can verify the legitimacy of the abort request:
* **Identity Headers**: The server captures ``X-Auth-Token`` and ``X-Cluster-ID`` from the current request and embeds them into the RabbitMQ payload.
* **API Host List**: The server provides a list of active Config Nodes (API Servers). This allows the Job Manager to report the "Aborted" status back to any available API node.

### 2. Signal Transmission (RabbitMQ)
The core of the operation is the ``publish_job_abort`` method.
* **Exchange**: Uses the same ``JOB_REQUEST_EXCHANGE`` as the execution API.
* **Routing Key**: Uses a dedicated ``JOB_ABORT_ROUTING_KEY``. This allows Job Managers to filter for abort signals specifically without processing new job requests.
* **Reliability**: The system uses an identical retry policy to the execution API (12 retries with exponential backoff), ensuring the signal is delivered even during transient RabbitMQ congestion.



### 3. Execution ID Tracking
The ``job_execution_id`` is the primary key used by the Job Manager to identify which local process or thread to terminate. Without a valid ID, the signal will be ignored by the workers.

Error Handling
--------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - Code
     - Condition
   * - **400**
     - Malformed JSON or missing ``job_execution_id``.
   * - **404**
     - No active Config Nodes found to populate the ``api_server_host`` list.
   * - **500**
     - Persistent failure to publish the abort signal to RabbitMQ after all retries.

Important Considerations
------------------------

.. warning::
   **Graceful vs. Hard Termination**: Sending an abort request does not guarantee instantaneous termination. The Job Manager must reach a "cancellation point" in its playbook or script to stop. If a task is in the middle of a critical non-interruptible network operation, there may be a delay before the job status changes to "Aborted".

.. note::
   To confirm that the job has actually stopped, administrators should monitor the Analytics API for UVE updates related to the specific ``job_execution_id``.

Direct AMQP Publishing (amqp-publish)
=====================================

The ``amqp-publish`` API is a low-level utility that allows internal components or administrative scripts to publish messages directly to the RabbitMQ message bus through the API Server. This is a generic gateway used for inter-service communication that bypasses the standard resource-based REST logic.

Operation Overview
------------------

The API Server acts as an AMQP Producer. It validates the existence of the target exchange, creates it on the fly if necessary, and routes the provided payload to the broker.

* **Method**: ``POST``
* **URL**: ``/amqp-publish``
* **Authentication**: Required (Cloud Admin privileges).
* **Return Code**: ``202 Accepted`` (Indicates the message has been accepted for delivery to the broker).



Request Body Structure
----------------------

The payload must be a JSON object containing the AMQP routing metadata and the message content.

.. list-table::
   :widths: 25 15 60
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - ``exchange``
     - String
     - **Mandatory**. The name of the AMQP exchange (e.g., ``vnc_config.resource.update``).
   * - ``exchange_type``
     - String
     - **Mandatory**. The type of exchange: ``direct``, ``topic``, ``headers``, or ``fanout``.
   * - ``payload``
     - Object
     - **Mandatory**. The actual message content (JSON-serializable object).
   * - ``routing_key``
     - String
     - The routing key used by the exchange to determine which queues receive the message.
   * - ``headers``
     - Dictionary
     - Optional AMQP message headers for header-based routing or metadata.

Example Request::

    curl -X POST -H "X-Auth-Token: $OS_TOKEN" -H "Content-Type: application/json" -d '{
        "exchange": "custom_notifications",
        "exchange_type": "topic",
        "routing_key": "system.events.audit",
        "payload": {"event": "security_check", "status": "passed"},
        "headers": {"priority": "high"}
    }' http://127.0.0.1:8082/amqp-publish

Detailed Internal Logic
-----------------------

### 1. Dynamic Exchange Management
A unique feature of this method is its ability to manage the AMQP topology dynamically:
* **Existence Check**: Before publishing, the server calls ``get_exchange()``.
* **Auto-Provisioning**: If the exchange does not exist in the current AMQP client session, it calls ``add_exchange()`` using the provided ``exchange_type``. This ensures that the message is never "lost" due to a missing exchange configuration on the broker.

### 2. Message Routing
The server forwards the ``payload``, ``routing_key``, and ``headers`` directly to the internal AMQP client.
* **Decoupling**: The API Server does not wait for a consumer to read the message.
* **Status 202**: The ``202 Accepted`` response specifically means the API Server has successfully handed the message to RabbitMQ, but processing by other services (like the Control node or Schema Transformer) is still pending.



### 3. Logging and Debugging
The method provides high visibility for troubleshooting messaging issues:
* **SYS_INFO**: Logs the entry into the publish sequence.
* **SYS_DEBUG**: Dumps the **entire body** of the request into the system logs. This is vital for debugging malformed payloads or incorrect routing keys in a distributed environment.

Security Considerations
-----------------------

.. warning::
   **Direct Bus Access**: This API provides raw access to the system's message bus. Injecting malformed messages into core exchanges (like those used for resource updates) can cause system-wide instability or inconsistencies in the Control Plane.

.. note::
   Access to this endpoint should be strictly restricted to the ``cloud-admin`` role and internal system services.

Error Handling
--------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - Code
     - Condition
   * - **400**
     - Malformed JSON or missing mandatory fields (``exchange`` or ``exchange_type``).
   * - **401/403**
     - Authentication failed or insufficient privileges to access the AMQP gateway.
   * - **500**
     - Internal error in the AMQP client (e.g., lost connection to the RabbitMQ broker).

Synchronous AMQP Request (amqp-request)
=======================================

The ``amqp-request`` API implements a Remote Procedure Call (RPC) pattern over AMQP. It allows a client to send a message to a specific service via RabbitMQ and wait synchronously for a response. This is typically used for operations where the API Server acts as a proxy to other internal services that don't have their own REST interfaces.

Operation Overview
------------------

The process follows a strict "Request-Response" lifecycle. The API Server creates a transient consumer (callback) specifically for this request, publishes the payload, and blocks the HTTP thread until the response arrives or a timeout occurs.

* **Method**: ``POST``
* **URL**: ``/amqp-request``
* **Authentication**: Required (Cloud Admin privileges).
* **Return Value**: The JSON body received from the remote service via AMQP.



Request Body Structure
----------------------

The payload requires both routing information for the outgoing request and instructions on where to listen for the reply.

.. list-table::
   :widths: 25 15 60
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - ``exchange``
     - String
     - **Mandatory**. The name of the exchange to publish the request to.
   * - ``exchange_type``
     - String
     - **Mandatory**. The AMQP exchange type (direct, topic, etc.).
   * - ``routing_key``
     - String
     - The routing key for the target service (request destination).
   * - ``response_key``
     - String
     - **Mandatory**. The routing key the API Server will listen on for the response.
   * - ``payload``
     - Object
     - The message body to be sent to the remote service.
   * - ``amqp_timeout``
     - Integer
     - Optional. Max time (seconds) to wait for a response. Defaults to system settings.

Detailed Internal Logic
-----------------------

### 1. Dynamic Topology Setup
Like the publish method, ``amqp-request`` ensures the target exchange exists using ``get_exchange`` and ``add_exchange``. It uses the ``kombu`` library to define exchanges as non-durable by default for RPC patterns.

### 2. Transient Consumer Creation
To receive the reply, the server generates a unique, one-time consumer:
* **Naming**: The consumer is named using the pattern ``amqp_request.<hostname>.<unique-uuid>``.
* **AmqpWorker**: A specialized worker is instantiated to manage a local ``gevent.queue``.
* **Auto-Cleanup**: The consumer is created with ``auto_delete=True`` and is explicitly removed in the ``finally`` block to prevent resource leaks in RabbitMQ.

### 3. Synchronous Blocking (Gevent)
Once the message is published, the server calls ``amqp_worker.queue.get(block=True, timeout=amqp_timeout)``.
* This suspends the specific greenlet (thread) handling the HTTP request.
* If a response arrives at the ``response_key``, the ``handle_message`` callback puts the data into the queue, unblocking the server.
* If no message arrives within the timeout period, a ``gevent.queue.Empty`` exception is raised.



### 4. Response Handling
* **Success (200 OK)**: The body received from the AMQP bus is returned directly as the HTTP response body.
* **Timeout (500 Error)**: If the remote service fails to respond in time, the server returns a 500 Internal Server Error, indicating the RPC call failed.

Security and Best Practices
---------------------------

.. warning::
   **Thread Exhaustion**: Because this is a blocking operation, a slow or non-responsive AMQP service can tie up API Server worker threads. Always specify a reasonable ``amqp_timeout`` to prevent the API Server from becoming unresponsive under high load.

.. note::
   The ``response_key`` should be unique to the request or the server instance to ensure that responses are not accidentally consumed by other services.

Error Codes
-----------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - Code
     - Condition
   * - **200**
     - Request was successfully processed and a response was received via AMQP.
   * - **400**
     - Malformed JSON or missing mandatory fields.
   * - **500**
     - AMQP timeout reached before the remote service could reply.

Host-Based Service Templates (hbs-get)
======================================

The ``hbs-get`` API is a specialized endpoint used to retrieve the orchestration manifests (templates) for Host-Based Services. It acts as a template aggregator, fetching details for a specific ``host-based-service`` object and generating the corresponding Kubernetes-style definitions for networking and deployment.

Operation Overview
------------------

This API does not just read a database record; it dynamically constructs a collection of templates (Namespace, DaemonSet, and Virtual Networks) based on the configuration of the HBS object.

* **Method**: ``POST``
* **URL**: ``/hbs-get``
* **Authentication**: Required (Read permissions on the HBS object).
* **Return Value**: A JSON object containing a list of generated YAML-like templates for the service.



Request Body Structure
----------------------

The request must identify the HBS resource either by its UUID or its Fully Qualified Name (FQ Name).

.. list-table::
   :widths: 25 15 60
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - ``hbs_uuid``
     - UUID
     - The unique identifier of the host-based-service object.
   * - ``hbs_fq_name``
     - List
     - The FQ Name of the HBS object (e.g., ``["default-domain", "hbs-template-1"]``).

Example Request::

    curl -X POST -H "X-Auth-Token: $OS_TOKEN" -H "Content-Type: application/json" -d '{
        "hbs_uuid": "8c84ff8a-30ac-4136-99d9-f0d9662f3eee"
    }' http://127.0.0.1:8082/hbs-get

Detailed Internal Logic
-----------------------

### 1. Identity Resolution and RBAC
* **UUID Lookup**: If only ``hbs_fq_name`` is provided, the server first resolves it to a UUID via the database. If the name is not found, a ``404 Not Found`` error is returned.
* **Security Check**: The server performs a mandatory RBAC check (``check_perms_read``). The user must have at least **Read (R)** access to the HBS object to fetch its templates.

### 2. Template Aggregation
The server uses the ``host-based-service`` resource class to build a composite response:

1. **HBS Info**: Fetches the core attributes of the service (metadata, namespace, associated networks).
2. **Networking Templates**: Generates templates for the "Left" and "Right" Virtual Networks (VNs) associated with the service. This includes mapping the VN UUIDs to the target namespace.
3. **DaemonSet Template**: Constructs the Kubernetes DaemonSet manifest (``ds_template``) using the service parameters (images, resource limits, etc.).
4. **Namespace**: Retrieves the definition for the Kubernetes Namespace where these components will reside.



### 3. Response Format
The API returns a structured list of templates under the ``hbs`` key. These templates are typically consumed by a provisioning agent or a Kubernetes operator to apply the configuration to a cluster.

Response Example::

    {
        "hbs": [
            { "kind": "Network", "name": "left-vn", ... },
            { "kind": "Network", "name": "right-vn", ... },
            { "kind": "DaemonSet", "metadata": { "name": "hbs-ds" }, ... }
        ]
    }

Error Handling
--------------

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - Code
     - Condition
   * - **400**
     - Missing both ``hbs_uuid`` and ``hbs_fq_name``, or malformed JSON.
   * - **403**
     - Permission denied. The user does not have read access to the specified HBS object.
   * - **404**
     - The specified HBS resource could not be found in the configuration database.

==========================================
OpenSDN Advanced API & Admin Reference
==========================================

This document provides a detailed technical reference for the streaming, diagnostic, and administrative capabilities of the OpenSDN API Server.

Real-time Monitoring with Watch API
===================================

The ``/watch`` endpoint implements **Server-Sent Events (SSE)**, allowing clients to receive an uninterrupted stream of resource changes.

Overview
--------

* **Method**: ``GET``
* **URL**: ``/watch?resource_type=<type1,type2>&<type>_fields=<field1,field2>``
* **Headers**:
    * ``Accept: text/event-stream``
    * ``Cache-Control: no-cache``

Detailed Execution Flow
-----------------------

1. **Multi-Resource Validation**: The server splits the ``resource_type`` string and validates each type against the internal schema.
2. **Synchronous RBAC Check**: For every resource type, the server executes a full RBAC validation (identity, role, and project context).
3. **Queue Registration**: A unique ``WatcherQueue`` (based on ``gevent.queue``) is created for the client.
4. **Initialization Phase**: The server pushes initial state events to synchronize the client.
5. **Event Loop**: The server enters a non-blocking loop, yielding SSE-formatted data whenever a CRUD operation occurs.



Operational Scenarios for Watch
-------------------------------

**Scenario A: Security & Firewall Automation**
Update external security hardware whenever a new Virtual Network or Security Group is created.
* **Request**: ``GET /watch?resource_type=security_group&security_group_fields=security_group_entries``
* **Benefit**: Eliminates the need for polling; the security agent reacts in milliseconds.

**Scenario B: Real-time Topology Visualization**
Draw network links instantly as Virtual Machine Interfaces (VMIs) are attached.
* **Request**: ``GET /watch?resource_type=virtual_machine_interface,instance_ip``
* **Focus**: Monitor the ``data`` field for the ``create`` event to map the new VMI to its IP.

**Scenario C: Infrastructure Health Monitoring**
Track the availability of vRouter agents.
* **Request**: ``GET /watch?resource_type=virtual_router``
* **Alert**: A ``delete`` event on a ``virtual_router`` indicates a compute node has been decommissioned or lost from the config database.



SDN Administrator Toolkit
=========================

Strategic scenarios and methods for maintaining a healthy SDN cluster.

1. Database Integrity Check
---------------------------
**Method**: ``POST /db-check``

* **Usage**: Use when objects cannot be deleted or GUI displays inconsistent data.
* **What to look for**: Look for UUIDs in the response marked with errors. These are "zombie" or orphaned records that lack a proper body in Cassandra but still have references.

2. Global Data Export (Backup/Audit)
------------------------------------
**Method**: ``POST /fetch-records``

* **Usage**: Before major upgrades or for deep security audits.
* **Key Detail**: Unlike standard GETs, this bypasses API filters to show the **raw** state of objects.
* **Audit Tip**: Check the ``perms2`` field. If many objects are owned by a non-existent Project UUID, it's time for a manual cleanup.



3. Troubleshooting Access (RBAC)
-------------------------------
**Method**: ``GET /obj-perms?uuid=<uuid>``

* **Usage**: When a user reports "Permission Denied" errors.
* **Analysis**:
    * Check the ``permissions`` string (e.g., ``"RWX"``).
    * If ``permissions`` is only ``"R"``, the user cannot modify the resource.
* **Fix**: Use ``POST /obj-chmod`` to adjust the bitmask (e.g., set ``global_access: 4`` for shared read access).

4. Performance & Synchronization
--------------------------------
**Method**: ``POST /obj-cache``

* **Usage**: When data in the database is correct, but the API Server returns "stale" (old) values.
* **Check**: Compare the JSON from ``obj-cache`` with a direct Database read. A mismatch indicates that the RabbitMQ cache-invalidation signal was missed.



5. Synchronous Troubleshooting (RPC)
------------------------------------
**Method**: ``POST /amqp-request``

* **Usage**: Verifying if background services (like Device Manager) are responsive.
* **Failure Analysis**: If the response is a **500 Internal Server Error** with a ``gevent.queue.Empty`` message, it means the target service is down or the AMQP bus is overloaded.

Quick-Reference Troubleshooting Table
=====================================

.. list-table::
   :widths: 30 40 30
   :header-rows: 1

   * - Symptom in Response
     - Internal Meaning
     - Recommended Action
   * - ``"is_shared": true``
     - Object is visible to all projects.
     - Verify if this is intentional for security.
   * - ``HTTP 414 URI Too Long``
     - GET request parameters are too large.
     - Switch to ``POST /list-bulk-collection``.
   * - ``"event": "stop"``
     - The API server is shutting down.
     - Implement client-side reconnect logic.
   * - ``:\n\n`` (SSE Comment)
     - Keep-alive heartbeat.
     - Ignore; it prevents connection timeout.



.. important::
   All administrative methods listed above require ``cloud-admin`` privileges. Misuse of ``amqp-publish`` or ``obj-chmod`` can lead to system-wide instability or security breaches.

Understanding System Logs & Diagnostics
=======================================

OpenSDN uses the **Sandesh** protocol for logging and state reporting. For an administrator, understanding the structure of these logs is crucial for debugging complex asynchronous operations like Jobs or RBAC failures.

Logging Levels (SandeshLevel)
-----------------------------

The API Server classifies messages into several levels. Understanding these helps in filtering noise during troubleshooting:

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - Level
     - Description and Usage
   * - ``SYS_DEBUG``
     - **Verbose**. Contains full request bodies, internal state dumps, and raw AMQP payloads. Essential for developers.
   * - ``SYS_INFO``
     - **Operational**. Logs entry/exit points of major methods (e.g., "Entered execute-job"). Shows normal system flow.
   * - ``SYS_NOTICE``
     - **Auditing**. Records significant changes like ``chmod``, ``chown``, or RBAC rule updates.
   * - ``SYS_ERR`` / ``SYS_WARN``
     - **Critical**. Records database connection losses, AMQP timeouts, or internal exceptions.



Tracing Key API Operations
--------------------------

### 1. Job Execution Trace
When you call ``execute-job``, the log sequence follows this pattern:
1. ``SYS_INFO``: "Entered execute-job" — confirm the request reached the API.
2. ``SYS_DEBUG``: "Job Input <json_body>" — check if the parameters were parsed correctly.
3. ``SYS_INFO``: "Published job message to RabbitMQ. Execution id: <uuid>" — confirms the hand-off to the message bus.

**Troubleshooting Tip**: If you see "Entered", but never "Published", check for database errors in ``dbe_list`` while the server was fetching the Config Node list.

### 2. RBAC & Permissions Trace
The ``validate_request`` method provides deep insights into why a request was denied:
* **Log Entry**: ``rbac: u=<user>, r=<roles>, o=<obj_type>, op=<operation>``
* **What to check**:
    * ``u``: Is the username correct?
    * ``r``: Does the user have the expected roles (e.g., ``admin``)?
    * ``rules``: How many RBAC rules were evaluated? If this is ``0``, the user is likely hitting a "Deny All" default.



### 3. AMQP Request/Response Trace
For synchronous RPC calls (``amqp-request``), logs are the only way to see the "hidden" interaction:
* **Request**: ``Amqp request <payload>``
* **Response**: ``Amqp response, status <status>, body <body>``

**Troubleshooting Tip**: A status ``500`` in the log with an empty body usually points to a timeout. Check the ``amqp_timeout`` value in your request compared to the actual processing time of the backend service.

Log Collection & Inspection
---------------------------

Logs can be accessed in two ways:

1. **Local Files**: Typically located at ``/var/log/contrail/contrail-api.log``.
2. **Introspect Port**: The API Server provides a diagnostic web interface (usually on port ``8084``) where you can view active Sandesh messages and traces in real-time.



Operational Best Practices
--------------------------

.. note::
   **Log Rotation**: Ensure log rotation is configured. At ``SYS_DEBUG`` level, a busy API server can generate gigabytes of logs per hour due to the full JSON dumps of ``fetch-records`` or ``dump-cache``.

.. warning::
   **Sensitive Data**: ``SYS_DEBUG`` logs contain authentication tokens and raw payloads. Secure access to log files to prevent exposure of sensitive infrastructure data.
