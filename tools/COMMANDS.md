```
export=https_proxy=localhost:8080

cf login -u andrew.lunde@sap.com

export globalacctguid=71f51ce6-c6b5-4583-a6ac-49e392506619

export sapcpuser=primaryuser03@gmail.com
export sapcppass=PrimaryUs3r03


cf create-service cis central ACC_CIS_CEN
cf create-service-key ACC_CIS_CEN ACC_CIS_CEN_Key
cf service-key ACC_CIS_CEN ACC_CIS_CEN_Key

authurlcen=$(cf service-key ACC_CIS_CEN ACC_CIS_CEN_Key | tail -n +3 | jq .uaa.url | tr -ds '"' '')
clientidcen=$(cf service-key ACC_CIS_CEN ACC_CIS_CEN_Key | tail -n +3 | jq .uaa.clientid | tr -ds '"' '')
clientsecretcen=$(cf service-key ACC_CIS_CEN ACC_CIS_CEN_Key | tail -n +3 | jq .uaa.clientsecret | tr -ds '"' '')
accountsurlcen=$(cf service-key ACC_CIS_CEN ACC_CIS_CEN_Key | tail -n +3 | jq .endpoints.accounts_service_url | tr -ds '"' '')
provisioningurlcen=$(cf service-key ACC_CIS_CEN ACC_CIS_CEN_Key | tail -n +3 | jq .endpoints.provisioning_service_url | tr -ds '"' '')
bearercen=$(curl -u $clientidcen:$clientsecretcen $authurlcen/oauth/token --silent --location --insecure --header 'Content-Type: application/x-www-form-urlencoded' --data-urlencode 'grant_type=password' --data-urlencode 'username='$sapcpuser --data-urlencode 'password='$sapcppass | jq .access_token | tr -ds '"' '')

cf create-service cis local ACC_CIS_LOC
cf create-service-key ACC_CIS_LOC ACC_CIS_LOC_Key
cf service-key ACC_CIS_LOC ACC_CIS_LOC_Key

authurlloc=$(cf service-key ACC_CIS_LOC ACC_CIS_LOC_Key | tail -n +3 | jq .uaa.url | tr -ds '"' '')
clientidloc=$(cf service-key ACC_CIS_LOC ACC_CIS_LOC_Key | tail -n +3 | jq .uaa.clientid | tr -ds '"' '')
clientsecretloc=$(cf service-key ACC_CIS_LOC ACC_CIS_LOC_Key | tail -n +3 | jq .uaa.clientsecret | tr -ds '"' '')
accountsurlloc=$(cf service-key ACC_CIS_LOC ACC_CIS_LOC_Key | tail -n +3 | jq .endpoints.accounts_service_url | tr -ds '"' '')
provisioningurlloc=$(cf service-key ACC_CIS_LOC ACC_CIS_LOC_Key | tail -n +3 | jq .endpoints.provisioning_service_url | tr -ds '"' '')
bearerloc=$(curl -u $clientidloc:$clientsecretloc $authurlloc/oauth/token --silent --location --insecure --header 'Content-Type: application/x-www-form-urlencoded' --data-urlencode 'grant_type=password' --data-urlencode 'username='$sapcpuser --data-urlencode 'password='$sapcppass | jq .access_token | tr -ds '"' '')

curl $accountsurlcen/accounts/v1/subaccounts --silent --location --insecure --header 'Content-Type: application/json' --header 'Authorization: Bearer '$bearercen | jq .

curl $accountsurlcen/accounts/v1/subaccounts --silent --location --insecure --request POST --header 'Content-Type: application/json' --header 'Accept: application/json' --header 'Authorization: Bearer '$bearercen --data-raw '{"betaEnabled": true, "customProperties": [ { "key": "creator", "value": "primaryuser03" } ], "description": "Subaccount created via API", "displayName": "ViaAPI", "parentGUID": "'$globalacctguid'", "region": "us21", "subaccountAdmins": [ "andrew.lunde@sap.com" ], "subdomain": "viaapi", "usedForProductionSetting": "USED_FOR_PRODUCTION"}' | jq .

Actions for accounts/subaccount
  list                  List all subaccounts in a global account
  get                   Get details about a subaccount
  create                Create a subaccount
  update                Update a subaccount
  delete                Delete a subaccount
  move                  Move a subaccount
  subscribe             Subscribe to an application from a subaccount
  unsubscribe           Unsubscribe an application from a subaccount

sapcp --format json create accounts/subaccount 
sapcp --format json  get accounts/subaccount 05623911-8ee9-43f5-8cda-b74c46e4175e
sapcp --format json create accounts/subaccount --global-account SUBDOMAIN --display-name PEAHCM --region REGION [--subdomain SUBDOMAIN] [--used-for-production VALUE] [--description DESCRIPTION] [--directory ID] [--beta-enabled] --subaccount-admins JSON [--custom-properties JSON]

lastguid=$(sapcp --format json create accounts/subaccount --global-account partner-eng --display-name PEAHCM --region us21 --subdomain partner-other --used-for-production NOT_USED_FOR_PRODUCTION --description "Azure subaccount" --beta-enabled | jq .guid | tr -ds '"' '')
sapcp --format json  get accounts/subaccount $lastguid | jq .state
sapcp --format json  delete accounts/subaccount 91a08337-7823-4645-9297-d9c0b5539d99 --confirm
sapcp --format json  get accounts/subaccount $lastguid | jq .state

curl $accountsurlcen/accounts/v1/subaccounts/$lastguid --silent --location --insecure --header 'Content-Type: application/json' --header 'Authorization: Bearer '$bearercen | jq .state | tr -ds '"' ''


curl $provisioningurlloc/provisioning/v1/availableEnvironments --silent --location --insecure --header 'Content-Type: application/json' --header 'Authorization: Bearer '$bearerloc | jq .

curl $provisioningurlloc/provisioning/v1/environments --silent --location --insecure --header 'Content-Type: application/json' --header 'Authorization: Bearer '$bearerloc | jq .


{
  "description": "BLAH",
  "environmentType": "cloudfoundry",
  "landscapeLabel": "cf-us21",
  "name": "blah-test",
  "origin": "",
  "parameters": {"instance_name":"blah-test","users":[{"email":"andrew.lunde@sap.com"}]},
  "planName": "standard",
  "serviceName": "cloudfoundry",
  "technicalKey": "string",
  "user": "andrew.lunde@sap.com"
}

curl $provisioningurlloc/provisioning/v1/environments --silent --location --insecure --request POST --header 'Content-Type: application/json' --header 'Authorization: Bearer '$bearerloc --data-raw '{"displayName": "blah-test", "environmentType": "cloudfoundry", "landscapeLabel": "cf-us21", "parameters": {"instance_name":"blah-test","users":[{"email":"andrew.lunde@sap.com"}]}, "plan": "standard", "service": "cloudfoundry", "subaccount": "c96d49c7-bdbf-436c-a35a-322b90ba2793"}' | jq .

#close to working??? #https://provisioning-service.cfapps.eu10.hana.ondemand.com/api#/

curl $provisioningurlloc/provisioning/v1/environments --silent --location --insecure --request POST --header 'Content-Type: application/json' --header 'Authorization: Bearer '$bearerloc --data-raw '{"displayName": "blah-test", "environmentType": "cloudfoundry", "landscapeLabel": "cf-us21", "dataCenterTechnicalKey": "cf-us21", "name": "blah-test", "parameters": {"instance_name":"blah-test","users":[{"email":"andrew.lunde@sap.com"}]}, "planName": "standard", "serviceName": "cloudfoundry", "subaccount": "05623911-8ee9-43f5-8cda-b74c46e4175e"}' | jq .

#AJAX call in UI
Request
dataCenterTechnicalKey: "cf-us21"
displayName: "blah-test"
environmentType: "cloudfoundry"
landscapeLabel: "cf-us21"
name: "blah-test"
parameters: {instance_name: "blah-test", users: [{email: "andrew.lunde@sap.com"}]}
planName: "standard"
serviceName: "cloudfoundry"

Response
{
	"name": "blah-test",
	"id": "EF2ED852-5471-4D37-BDEB-0C085DB8FD40",
	"subaccountGUID": "05623911-8ee9-43f5-8cda-b74c46e4175e",
	"createdDate": "1616077472032",
	"state": "CREATING",
	"stateMessage": "Creating environment instance.",
	"environmentType": "cloudfoundry",
	"landscapeLabel": "cf-us21",
	"tenantId": "05623911-8ee9-43f5-8cda-b74c46e4175e",
	"planId": "fc5abe63-2a7d-4848-babf-f63a5d316df1",
	"modifiedDate": "1616077472032",
	"labels": "{\"API Endpoint:\":\"https://api.cf.us21.hana.ondemand.com\",\"Org Name:\":\"blah-test\"}",
	"parameters": "{\"instance_name\":\"blah-test\",\"users\":[{\"email\":\"andrew.lunde@sap.com\"}]}",
	"type": "Provision",
	"planName": "standard",
	"serviceName": "cloudfoundry"
}


curl $provisioningurlloc/provisioning/v1/environments/EF2ED852-5471-4D37-BDEB-0C085DB8FD40 --silent --location --insecure --request DELETE --header 'Content-Type: application/json' --header 'Authorization: Bearer '$bearerloc | jq .

#sapcp login --url https://cpcli.cf.eu10.hana.ondemand.com --subdomain partner-eng --user andrew.lunde@sap.com
#sapcp login --url https://cpcli.cf.eu10.hana.ondemand.com --subdomain partner-eng --user primaryuser03@gmail.com
#sapcp list accounts/subaccount

Actions for accounts/environment-instance
  list                  Get all environment instances of a subaccount
  get                   Get a specific environment instance of a subaccount
  create                Create an environment instance in a subaccount
  update                Update an environment instance of a subaccount
  delete                Delete an environment instance of a subaccount

#sapcp --format json list accounts/subaccount | jq '.value[] | select(.displayName == "subA")' 
#sapcp --format json list accounts/subaccount | jq '.value[] | select(.displayName == "subA") | .guid' | tr -ds '"' ''


# Only works when logged in as andrew.lunde
# sapcp --format json create accounts/environment-instance --subaccount 05623911-8ee9-43f5-8cda-b74c46e4175e --parameters '{"instance_name":"blah-test","users":[{"email":"andrew.lunde@sap.com"}]}' --display-name blah-test --environment cloudfoundry --landscape cf-us21 --service cloudfoundry --plan standard | jq .id

sapcp --format json get accounts/environment-instance C03726E6-EC30-4585-B7A3-992F8E40C0F7 --subaccount 05623911-8ee9-43f5-8cda-b74c46e4175e | jq .status | tr -ds '"' ''

sapcp --format json delete accounts/environment-instance C03726E6-EC30-4585-B7A3-992F8E40C0F7 --subaccount 05623911-8ee9-43f5-8cda-b74c46e4175e --confirm

Usage: sapcp [OPTIONS] assign accounts/entitlement --global-account SUBDOMAIN [--to-subaccount ID] [--to-directory ID] --for-service NAME --plan NAME [--enable] [--amount NUMBER] [--auto-distribute-amount NUMBER] [--auto-assign] [--distribute]

sapcp --format json assign accounts/entitlement --global-account partner-eng --to-subaccount 05623911-8ee9-43f5-8cda-b74c46e4175e --for-service hana --plan schema --enable

sapcp --format json assign accounts/entitlement --global-account partner-eng --to-subaccount 05623911-8ee9-43f5-8cda-b74c46e4175e --for-service APPLICATION_RUNTIME --plan MEMORY --amount 1


cf update-service pehcaza -c '{"operation":"adddatabasemapping", "orgid":"5799de10-e447-4b78-9b90-52dbc109fa05", "spaceid":"d096c374-91ef-4e57-aef6-8088384b9bc0"}'

https://hana-cockpit.cfapps.us21.hana.ondemand.com/hana-inventory/sap/hana/cloud/inventory/api/v1/spaces/d096c374-91ef-4e57-aef6-8088384b9bc0/hana/ffa845c4-c70e-4774-ba37-c0a6fdf16850/mappings

database_id: "ffa845c4-c70e-4774-ba37-c0a6fdf16850"
organization_guid: "5799de10-e447-4b78-9b90-52dbc109fa05"
space_guid: "e58f90ef-d555-411b-a0a8-0462569dbe9e"

#Using mitmproxy stickycookies and authing via Firefox. + have to set x-csrf-token
curl https://hana-cockpit.cfapps.us21.hana.ondemand.com/hana-inventory/sap/hana/cloud/inventory/api/v1/96c374-91ef-4e57-aef6-8088384b9bc0/hana/ffa845c4-c70e-4774-ba37-c0a6fdf16850/mappings -x localhost:8080 --silent --location --insecure --request PUT --header 'Content-Type: application/json' --header 'x-csrf-token: ea01bc77a75398e0-gYuqGTEKQcOnLB-dc0rbZuDdBX8' --data-raw '{"database_id": "ffa845c4-c70e-4774-ba37-c0a6fdf16850", "organization_guid": "79ab0a7d-24ca-4f8b-a8f7-79d4a438f5e8", "space_guid": "ff8945f3-a403-408d-87a1-fa8f4137223c"}'

source orgs_create orgs1.txt -f
source orgs_sapcp_create orgs1.txt -f
source orgs_create orgs2.txt -f
```
