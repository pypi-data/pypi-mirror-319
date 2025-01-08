import requests
import json
from configparser import ConfigParser
import os
from typing import Optional, Dict, Any
from datetime import datetime, timedelta


class TriaHRAPI:
    def __init__(self, base_url: str, client_id: str, client_secret: str):
        """
        Initialize the Tria HR API client

        Args:
            base_url: Base URL of the API (e.g., https://stage.decasport.triahr.com)
            client_id: OAuth client ID
            client_secret: OAuth client secret
        """
        self.base_url = base_url.rstrip('/')
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.token_expires_at = None

    @classmethod
    def from_config(cls, config_path: str = 'config.ini', environment: str = 'stage'):
        """
        Create an instance from a configuration file

        Args:
            config_path: Path to the configuration file
            environment: Environment to use (stage, prod, etc.)
        """
        config = ConfigParser()
        config.read(config_path)

        return cls(
            base_url=config['Environment'][environment],
            client_id=config['OAuth']['client_id'],
            client_secret=config['OAuth']['client_secret']
        )

    @classmethod
    def from_json(cls, base_url: str, credentials_json: dict):
        """
        Create an instance from parsed JSON credentials dictionary

        Args:
            base_url: Base URL of the API (e.g., https://stage.company.triahr.com)
            credentials_json: Parsed JSON dictionary containing client_id and client_secret

        Returns:
            TriaHRAPI instance
        """
        try:
            return cls(
                base_url=base_url,
                client_id=credentials_json['client_id'],
                client_secret=credentials_json['client_secret']
            )
        except KeyError as e:
            raise ValueError(f"Missing required field: {e}")

    def _ensure_valid_token(self):
        """Ensure we have a valid access token"""
        if (not self.access_token or
                not self.token_expires_at or
                datetime.now() >= self.token_expires_at):
            self._get_access_token()

    def _get_access_token(self):
        """Get a new OAuth2 access token"""
        token_url = f"{self.base_url}/oauth/v2/token"

        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.post(token_url, data=data, headers=headers)
        response.raise_for_status()

        token_data = response.json()
        self.access_token = token_data['access_token']
        # Set token expiration 5 minutes before actual expiration to be safe
        expires_in = token_data.get('expires_in', 3600) - 300
        self.token_expires_at = datetime.now() + timedelta(seconds=expires_in)

    def _make_request(self, method: str, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make an authenticated request to the API

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint (e.g., /api/v1/ping/)
            params: Query parameters
        """
        self._ensure_valid_token()

        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }

        url = f"{self.base_url}{endpoint}"
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            params=params
        )

        response.raise_for_status()
        return response.json()

    def format_response(self, response: Dict[str, Any], save_to_file: Optional[str] = None) -> None:
        """
        Pretty print the response and optionally save to a JSON file with proper Unicode handling

        Args:
            response: API response to format
            save_to_file: Optional filename to save the response as JSON
        """
        # Pretty print with ensure_ascii=False to properly display Unicode characters
        formatted = json.dumps(response, indent=2, ensure_ascii=False)
        print(formatted)

        # Save to file if requested, with proper encoding
        if save_to_file:
            with open(save_to_file, 'w', encoding='utf-8') as f:
                f.write(formatted)

    def undefined_request(
            self,
            endpoint: str,
            method: str = 'GET',
            params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make a custom request to any API endpoint

        Args:
            endpoint: API endpoint (e.g., '/api/v1/custom-endpoint/')
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            params: Optional query parameters dictionary

        Returns:
            API response as dictionary

        Example:
            # GET request with parameters
            response = api.undefined_request(
                endpoint='/api/v1/custom-endpoint/',
                params={'param1': 'value1', 'param2': 'value2'}
            )

            # POST request with data
            response = api.undefined_request(
                endpoint='/api/v1/custom-endpoint/',
                method='POST'
            )
        """
        # Ensure endpoint starts with /
        if not endpoint.startswith('/'):
            endpoint = f'/{endpoint}'

        # Ensure endpoint ends with /
        if not endpoint.endswith('/'):
            endpoint = f'{endpoint}/'

        return self._make_request(
            method=method.upper(),
            endpoint=endpoint,
            params=params
        )

    def ping(self) -> Dict[str, Any]:
        """Test the API connection"""
        return self._make_request('GET', '/api/v1/ping/')

    def organization_units(self, company_id: str) -> Dict[str, Any]:
        """
        Get organization units for a specific company

        Args:
            company_id: ID of the company to get units for
        """
        params = {'company_id': company_id}
        return self._make_request('GET', '/api/v1/organization-units/', params)

    def attendance_organization_units(self, company_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get plannable organization units for attendance

        Args:
            company_id: Optional ID to filter by company
        """
        params = {'company_id': company_id} if company_id else None
        return self._make_request('GET', '/api/v1/attendance-organization-units/', params)

    def companies(self) -> Dict[str, Any]:
        """
        Get list of companies in the application

        Returns:
            Dict containing list of companies and their basic information
        """
        return self._make_request('GET', '/api/v1/companies/')

    def attendance_plan(
            self,
            date_from: str,
            date_to: str,
            unit_id: Optional[int] = None,
            user_id: Optional[int] = None,
            company_id: Optional[int] = None,
            include_explicit_unit_id: bool = True,
            mode: str = 'plan'
    ) -> Dict[str, Any]:
        """
        Get attendance plan data for a specified time range and organizational unit or user

        Args:
            date_from: Start date in YYYY-MM-DD format
            date_to: End date in YYYY-MM-DD format
            unit_id: Organization unit ID (required unless user_id and company_id provided)
            user_id: User ID (optional)
            company_id: Company ID (optional)
            include_explicit_unit_id: Search for both unit_id & explicit unit_id (default: True)
            mode: Get published (reality) or unpublished (plan) plan (default: 'plan')
        """
        params = {
            'date_from': date_from,
            'date_to': date_to,
            'include_explicit_unit_id': str(include_explicit_unit_id).lower(),  # Convert to lowercase 'true'/'false'
            'mode': mode
        }

        if unit_id:
            params['unit_id'] = str(unit_id)  # Convert to string
        if user_id:
            params['user_id'] = str(user_id)  # Convert to string
        if company_id:
            params['company_id'] = str(company_id)  # Convert to string

        return self._make_request('GET', '/api/v1/attendance-plan/', params)

    def get_unit_ids(
            self,
            company_id: str,
            include_activated: bool = True,
            include_deactivated: bool = False
    ) -> list[int]:
        """
        Get all unit IDs for a company from attendance organization units.

        Args:
            company_id: Company identifier
            include_activated: Whether to include active units (default: True)
            include_deactivated: Whether to include deactivated units (default: False)

        Returns:
            list[int]: List of unit IDs matching the criteria
        """
        if not include_activated and not include_deactivated:
            raise ValueError("At least one of include_activated or include_deactivated must be True")

        response = self.attendance_organization_units(company_id)
        units = response.get('data', [])
        unit_ids = []

        for unit in units:
            unit_id = int(unit['id'])
            is_deactivated = unit.get('deactivated', False)

            if (include_activated and not is_deactivated) or \
                    (include_deactivated and is_deactivated):
                unit_ids.append(unit_id)

        return unit_ids

    def attendance_plans(
            self,
            date_from: str,
            date_to: str,
            company_id: str,
            mode: str = 'plan',
            include_activated: bool = True,
            include_deactivated: bool = False
    ) -> list[tuple[int, Dict[str, Any]]]:
        """
        Get attendance plans for all units in a company.

        Args:
            date_from: Start date in YYYY-MM-DD format
            date_to: End date in YYYY-MM-DD format
            company_id: Company identifier
            mode: Get published (reality) or unpublished (plan) plan (default: 'plan')
            include_activated: Whether to include active units (default: True)
            include_deactivated: Whether to include deactivated units (default: False)

        Returns:
            List of tuples (unit_id, attendance_plan_response) for each unit
        """
        unit_ids = self.get_unit_ids(
            company_id,
            include_activated=include_activated,
            include_deactivated=include_deactivated
        )
        results = []

        for unit_id in unit_ids:
            attendance = self.attendance_plan(
                date_from=date_from,
                date_to=date_to,
                unit_id=unit_id,
                company_id=company_id,
                mode=mode
            )
            results.append((unit_id, attendance))

        return results

# Example usage
if __name__ == "__main__":
    # Example 1: Direct initialization
    api = TriaHRAPI(
        base_url="https://stage.company.triahr.com",
        client_id="your_client_id",
        client_secret="your_client_secret"
    )

    # Example 2: Initialize from config file
    api = TriaHRAPI.from_config()

    # Example 3: Initialize from JSON (e.g., when using in Databricks)
    import json
    credentials = json.loads('{"client_id": "your_client_id", "client_secret": "your_client_secret"}')
    api = TriaHRAPI.from_json(
        base_url="https://stage.company.triahr.com",
        credentials_json=credentials
    )

    # Test connection
    print("Testing connection...")
    result = api.ping()
    api.format_response(result)

    # Get organization units for a company
    company_id = "158"  # Example company ID
    print(f"\nGetting organization units for company {company_id}...")
    org_units = api.organization_units(company_id)
    api.format_response(org_units)

    # Get attendance organization units
    print("\nGetting attendance organization units...")
    attendance_units = api.attendance_organization_units(company_id)
    api.format_response(attendance_units)

    # Get attendance plans for all units
    print("\nGetting attendance plans...")
    plans = api.attendance_plans(
        date_from="2024-01-01",
        date_to="2024-01-31",
        company_id=company_id,
        include_activated=True,
        include_deactivated=False
    )