import asyncio
import json
import time
import aiohttp
import requests
from salesmanago_tools.utils.constants import export_url, job_status_url, export_pages_url, import_url, contact_list_url
from salesmanago_tools.service.sales_manago_actions import create_import_payload, get_file, process_data_to_csv
from salesmanago_tools.utils.util_funcs import round_to_thousands


class SalesmanagoBaseClient:
    def __init__(self, clientId, apiKey, sha, owner):
        """
        Initialize the SalesmanagoClient with required credentials.
        """
        self.api_key = apiKey
        self.sha = sha
        self.client_id = clientId
        self.owner_email = owner
    
    async def _wait_for_response(self, job_status_url: str, payload: dict) -> str:
        """Waiting for the export task to complete and getting a link to the file."""
        while True:
            response_data = await self._post_request(job_status_url, payload)
            if response_data.get("message") == []:
                file_url = response_data.get("fileUrl")
                print("FILE URL: ", file_url)
                return file_url
            await asyncio.sleep(5)

    async def _post_request(self, url: str, payload: dict) -> dict:
        """Sending a POST request to the API and returning a JSON response."""
        timeout = aiohttp.ClientTimeout(total=120)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, json=payload) as response:
                if response.status != 200:
                    raise Exception(await response.text())
                print("RESPONSE: ", await response.json(), flush=True)
                return await response.json()
        
    async def _check_job_status(self, request_id):
        """
        Helper function to check job status and retrieve file URL.

        :param request_id: The ID of the job to check status for.
        :return: File URL of the completed job.
        """
        job_status_payload = {
            "clientId": self.client_id,
            "apiKey": self.api_key,
            "requestTime": int(time.time()),
            "sha": self.sha,
            "owner": self.owner_email,
            "requestId": request_id,
        }
        return await self._wait_for_response(job_status_url, job_status_payload)


class SalesmanagoDataClient(SalesmanagoBaseClient):
    async def export_data(self, value: str, addresseeType: str = "tag"):
        export_request_payload = {
            "clientId": self.client_id,
            "apiKey": self.api_key,
            "requestTime": int(time.time()),
            "sha": self.sha,
            "owner": self.owner_email,
            "contacts": [
                {"addresseeType": addresseeType, "value": value},
            ],
            "data": [
                {"dataType": "CONTACT"},
                {"dataType": "TAG"},
                {"dataType": "EXT_EVENT"},
                {"dataType": "VISITS"},
                {"dataType": "EMAILS"},
                {"dataType": "FUNNELS"},
                {"dataType": "NOTES"},
                {"dataType": "TASKS"},
                {"dataType": "COUPONS"},
                {"dataType": "SMS"},
                {"dataType": "CONSENTS"},
                {"dataType": "PROPERTIES"},
                {"dataType": "DICTIONARY_PROPERTIES"}
            ]
        }

        try:
            export_response = await self._post_request(export_url, export_request_payload)
            print("EXPORT RESPONSE: ", export_response, flush=True)
            request_id = export_response.get("requestId")
            if not request_id:
                raise ValueError("Failed to get requestId")

            file_url = await self._check_job_status(request_id)

            file_content = await get_file(file_url)

            csv_generator = process_data_to_csv(file_content)

            return csv_generator

        except aiohttp.ClientError as e:
            raise Exception(f"Error executing request: {str(e)}")

    async def fetch_all_contacts_from_salesmanago(self, page_size=1000, page=1):
        """
        Fetches all contacts from SalesManago and returns them as a list.
        """
        contacts_list = []

        try:
            while True:
                export_pages_payload = {
                    "clientId": self.client_id,
                    "apiKey": self.api_key,
                    "requestTime": int(time.time()),
                    "sha": self.sha,
                    "owner": self.owner_email,
                    "page": page,
                    "size": page_size,
                }

                # Отправляем запрос на экспорт контактов
                export_response = await self._post_request(export_pages_url, export_pages_payload)
                request_id = export_response.get("requestId")

                print(f"REQUEST_ID: {request_id}. EXPORT_PAGES_PAYLOAD: {export_pages_payload}", flush=True)

                if not request_id:
                    print("Export initiation failed. Message:", export_response.get("message", []))
                    break

                file_url = await self._check_job_status(request_id)

                # Скачиваем и обрабатываем файл
                file_content = await get_file(file_url)
                contacts = json.loads(file_content)

                # Если контактов больше нет, завершаем цикл
                if not isinstance(contacts, dict) or "contacts" not in contacts or not contacts["contacts"]:
                    break

                for item in contacts["contacts"]:
                    if isinstance(item, dict):
                        # Формируем список в нужном формате
                        formatted_contact = [
                            item.get("success"),
                            item.get("email"),
                            item.get("exists"),
                            item.get("id", None),  # contact_id
                            item.get("name", None),
                            item.get("country", None),
                            item.get("phone", None),
                        ]
                        print("formatted_contact: ", formatted_contact, flush=True)
                        contacts_list.append(formatted_contact)
                    else:
                        print("BAD ITEM: ", item, flush=True)
                        print("BAD ITEM TYPE: ", type(item), flush=True)

                print(f"Page {page}: Retrieved {len(contacts['contacts'])} contacts.", flush=True)
                page += 1

            return contacts_list

        except Exception as e:
            raise Exception(f"Unexpected error occurred: {e}")

        
    async def push_people_to_salesmanago(self, people_list_to_push: list[dict], account: str = "SEOSENSE", tags: list[str] = []):
        upsert_details = []
        for person in people_list_to_push:
            try:
                print("PERSON: ", person, flush=True)
                payload = await create_import_payload(row=person, tags=tags, account=account)
                upsert_details.extend(payload["upsertDetails"])

            except Exception as e:
                raise Exception(f"Error creating payload for row: {e}")

        batch_payload = {
            "apiKey": self.api_key,
            "sha": self.sha,
            "clientId": self.client_id,
            "owner": self.owner_email,
            "requestTime": int(time.time()),
            "upsertDetails": upsert_details,
        }

        import_response = await self._post_request(import_url, batch_payload)
        print("import_response: ", import_response, flush=True)
        request_id = import_response.get("requestId")
        print("REQUEST ID: ", request_id, flush=True)
        if not request_id:
            raise ValueError("Failed to get requestId")
        
        return None


    async def update_tag_salesmanago(self, email, tags, call_id=None):
        payload = {
            "clientId": self.client_id,
            "apiKey": self.api_key,
            "requestTime": int(time.time()),
            "sha": self.sha,
            "owner": self.owner_email,
            "upsertDetails": [
                {
                    "contact": {
                        "email": email
                    }
                }
            ],
        }

        if call_id is not None:
            payload["upsertDetails"][0]["properties"] = {
                "millis_call_id": call_id
            }

        if tags is not None:
            payload["upsertDetails"][0]["tags"] = tags

        try:
            # Send the POST request
            response = await self._post_request(import_url, payload=payload)

            print("RESPONSE: ", response, flush=True)

        except Exception as e:
            raise Exception("An error occurred:", e)

    async def get_contact_info_by_email(self, contact_email):
        payload = {
            "clientId": self.client_id,
            "apiKey": self.api_key,
            "requestTime": int(time.time()),
            "sha": self.sha,
            "owner": self.owner_email,
            'email': [contact_email]
        }

        print(f"payload = {payload}")

        try:
            response_data = await self._post_request(contact_list_url, payload=payload)

            print(f"contact_data = {response_data}")

            data = response_data.get('contacts', [{}])[0]
            name = data.get('name')
            dct = data.get('properties', {})
            result = {item['name']: item['value'] for item in dct}
            traffic = round_to_thousands(result.get('traffic'))
            keywords = round_to_thousands(result.get('keywords'))
            package = round_to_thousands(result.get('package'))

            clients = round_to_thousands(result.get('clients'))
            package_short = round_to_thousands(result.get('package_short'))

            return_value = {
                "Name": name,
                "CompanyName": data.get('company'),
                "traffic": traffic,
                "keywords": keywords,
                "package": package,
                "tags": [x.get('tag') for x in data.get('contactTags', [])],
                "clients": clients,
                "package_short": package_short
            }
            if self.account_name == 'ADSSENSE':
                return_value |= {
                    "adSpend": round_to_thousands(result.get('adSpend')),
                    "agencyPercentage": int(float(result.get('agencyPercentage'))) if result.get(
                        'agencyPercentage') is not None else None,
                    "agencyRetainer": round_to_thousands(result.get('agencyRetainer')),
                    "boostedRevenue": round_to_thousands(result.get('boostedRevenue')),
                    "conversionValue": round_to_thousands(result.get('conversionValue')),
                    "increasedNetRevenue": round_to_thousands(result.get('increasedNetRevenue')),
                    "increasedRevenue": round_to_thousands(result.get('increasedRevenue')),
                }
            return return_value
        except requests.RequestException as e:
            raise Exception(f"Failed to retrieve contact details: {e}")

