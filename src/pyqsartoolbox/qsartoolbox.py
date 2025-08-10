import requests
import json
import pandas as pd
from urllib.parse import quote

class QSARToolbox():
    """
    A class to connect to the local web server of the QSAR Toolbox. It requires 
    the QSAR Toolbox to be installed and running in the local computer. The user need to find the address and the 
    port of the local server and provide it to the class.
    Note:
    The port number can also be found automatically by running the following code:
    ```python
    import requests
    from requests.exceptions import RequestException
    import psutil
    from tqdm import tqdm

    def find_open_port(endpoint="/about/toolbox/version"):
        # Get a list of all open ports on localhost with status LISTEN
        open_ports = [conn.laddr.port for conn in psutil.net_connections() if conn.status == "LISTEN" and conn.laddr.ip == "127.0.0.1"]
        
        for port in tqdm(open_ports):
            url = f"http://127.0.0.1:{port}/api/v6{endpoint}"
            try:
                response = requests.get(url, timeout=1)
                if response.status_code == 200:
                    return port
            except RequestException:
                continue
        return None

    # Example usage
    port = find_open_port()
    if port:
        print(f"Server found on port {port}")
    else:
        print("Server not found within the specified port range")
    ```
    """
    def __init__(self, port, address="http://127.0.0.1", api_version="v6", timeout=60,
                 headers = {"accept": "text/plain"}):
        self.address = address
        self.port = port
        self.api_version = api_version
        self.headers = headers
        self.base_url = f"{self.address}:{self.port}/api/{self.api_version}"
        self.timeout = timeout
        # call version to check if the server is running
        try:
            self.toolbox_version()
        except:
            raise ValueError("The QSAR Toolbox server is not running. Please start the server and try again.")

    def toolbox_version(self, timeout=None):
        """
        Get the version of the QSAR Toolbox
        If timeout is not provided, it will use the timeout provided in the class initialization.
        Example:
        qs = QSARToolbox(port=52675)
        qs.toolbox_version()
        """
        if timeout is None:
            timeout = self.timeout
        response = requests.get(f"{self.base_url}/about/toolbox/version", 
                                headers=self.headers, timeout=timeout)
        if response.status_code == 200:
            return response.text
        else:
            raise ValueError(f"Error: {response.status_code}")
        
    def webapi_version(self, timeout=None):
        """
        Get the version of the API
        Example:
        qs = QSARToolbox(port=52675)
        qs.api_version()
        """
        if timeout is None:
            timeout = self.timeout
        response = requests.get(f"{self.base_url}/about/webapi/version", 
                                timeout=timeout,
                                headers=self.headers)
        if response.status_code == 200:
            return response.text
        else:
            raise ValueError(f"Error: {response.status_code}")
        
    def get_object_info(self, object_guid):
        """
        Get the information of an object by its GUID
        Example:
        qs = QSARToolbox(port=52675)
        qs.get_object_info("6bfe3c72-dff2-4e37-b5a1-ffa9a1a111d1")
        The output is a JSON object.
        """
        response = requests.get(f"{self.base_url}/about/object/{object_guid}")
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Error: {response.status_code}")
        
    def get_object_info_html(self, object_guid):
        """
        Get the information of an object by its GUID in HTML format
        Example:
        qs = QSARToolbox(port=52675)
        qs.get_object_info_html("6bfe3c72-dff2-4e37-b5a1-ffa9a1a111d1")
        The output is in html format.
        """
        response = requests.get(f"{self.base_url}/about/object/{object_guid}/html")
        if response.status_code == 200:
            return response.text
        else:
            raise ValueError(f"Error: {response.status_code}")
    
    def get_available_calculators(self, timeout=None):
        """
        Get all the available calculators in the QSAR Toolbox
        [
            {
                "Caption": "string",
                "Guid": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "Units": "string",
                "Is3D": true,
                "IsExperimental": true,
                "Description": "string"
            }
        ]
        """
        if timeout is None:
            timeout = self.timeout
        response = requests.get(f"{self.base_url}/calculation", headers=self.headers, 
                                timeout=timeout)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Error: {response.status_code}")
        
    def run_calculator(self, calculation_guid, chem_id, timeout=None):
        """
        Get the result of a calculation for a chemical; parameter chem_id comes from the
        results of one of the search_ functions. the calculation_guid comes from the get_calculations() function.
        """
        if timeout is None:
            timeout = self.timeout
        response = requests.get(f"{self.base_url}/calculation/{calculation_guid}/{chem_id}", 
                                headers=self.headers, timeout=timeout)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Error: {response.status_code}")
        
    def run_all_calculators(self, chem_id, timeout=120):
        """
        Get all the calculations for a chemical; parameter chem_id comes from the
        results of one of the search_ functions.
        """
        if timeout is None:
            timeout = self.timeout
        response = requests.get(f"{self.base_url}/calculation/all/{chem_id}", 
                                headers=self.headers,
                                timeout=timeout)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Error: {response.status_code}")

    def get_endpoints_tree(self, timeout=None):
        """
        Get the endpoint tree. Returns a dictionary of the available endpoint calculation methods depending on your installation of the QSAR Toolbox.
        """
        if timeout is None:
            timeout = self.timeout
        response = requests.get(f"{self.base_url}/data/endpointtree", 
                                headers=self.headers, timeout=timeout)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Error: {response.status_code}")
        
    def get_metadata_hierarchy(self, timeout=None):
        """
        Get the metadata hierarchy. Returns a dictionary of the available metadata hierarchy depending on your installation of the QSAR Toolbox.
        """
        if timeout is None:
            timeout = self.timeout
        response = requests.get(f"{self.base_url}/data/metadatahierarchy",
                                headers=self.headers, timeout=timeout)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Error: {response.status_code}")
    
    def get_endpoints_from_tree(self, position: str, timeout=None):
        """
        Get the available endpoints at the given position. Returns a dictionary of the available endpoint depending on your installation of the QSAR Toolbox.
        position is a string that represents the position in the endpoint tree. For example, "Physical Chemical Properties#Vapour pressure"
        Example
        qs = QSARToolbox(port=52675)
        qs.get_endpoint_from_tree("Physical Chemical Properties#Vapour pressure")
        """
        if timeout is None:
            timeout = self.timeout
        # make position url friendly
        position = quote(position)
        response = requests.get(f"{self.base_url}/data/endpoint?position={position}",
                                headers=self.headers, timeout=timeout)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Error: {response.status_code}")
        
    def get_endpoint_units_from_tree(self, position, endpoint, timeout=None):
        """
        Get the units for an endpoint from the endpoint tree
        """
        if timeout is None:
            timeout = self.timeout
        # make position url friendly
        position = quote(position)
        # make endpoint url friendly
        endpoint = quote(endpoint)
        response = requests.get(f"{self.base_url}/data/units?position={position}&endpoint={endpoint}",
                                headers=self.headers, timeout=timeout)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Error: {response.status_code}")
    
    def get_endpoint_data(self, chem_id, position, endpoint, includeMetadata=False, timeout=120):
        """
        Get the endpoint data for a chemid. Retrieves data for the specified endpoint at 
        the given position for the selected chemical
        Example:
        qs = QSARToolbox(port=52675)
        """
        if timeout is None:
            timeout = self.timeout
        # make position url friendly
        position = quote(position)
        # make endpoint url friendly
        endpoint = quote(endpoint)
        if includeMetadata:
            includeMetadata = "true"
        else:
            includeMetadata = "false"

        response = requests.get(f"{self.base_url}/data/{chem_id}?position={position}&endpoint={endpoint}&includeMetadata={includeMetadata}",
                                headers=self.headers, timeout=timeout)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Error: {response.status_code}")
    
    def get_all_endpoint_data(self, chem_id, includeMetadata=False):
        """
        Get all the endpoint data for a chemid. It can take a long time to return the data. Consider increasing the timeout.
        """
        if includeMetadata:
            includeMetadata = "true"
        else:
            includeMetadata = "false"
        response = requests.get(f"{self.base_url}/data/all/{chem_id}?includeMetadata={includeMetadata}", timeout=self.timeout)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Error: {response.status_code}")
    
    def get_databases_for_endpoint(self, position, endpoint, timeout=None):
        """
        Get the databases for an endpoint
        """
        if timeout is None:
            timeout = self.timeout
        # make position url friendly
        position = quote(position)
        # make endpoint url friendly
        endpoint = quote(endpoint)
        response = requests.get(f"{self.base_url}/data/databases?position={position}&endpoint={endpoint}",
                                headers=self.headers, timeout=timeout)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Error: {response.status_code}")
    
    def get_databases(self):
        """
        returns a list of the available databases in the QSAR Toolbox
        """
        response = requests.get(f"{self.base_url}/search/databases")
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Error: {response.status_code}")
        
    def get_profilers(self):
        """
        Get all available profilers.
        """
        response = requests.get(f"{self.base_url}/profiling")
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Error: {response.status_code}")

    def get_profiling_categories(self, profiler_guid):
        """
        Get the categories for a profiler.
        """
        response = requests.get(f"{self.base_url}/profiling/{profiler_guid}")
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Error: {response.status_code}")
        
    def profile_chemical(self, profiler_guid, chem_id, simulator_guid):
        """
        Profile a chemical using a profiler.
        """
        response = requests.get(f"{self.base_url}/profiling/{profiler_guid}/{chem_id}/{simulator_guid}")
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Error: {response.status_code}")
        
    def all_profile_chemicals(self, chem_id):
        """
        All Profilers for the specified chemical.
        """
        response = requests.get(f"{self.base_url}/profiling/all/{chem_id}")
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Error: {response.status_code}")
        
    # TODO: add the rest of the profiling functions

    def get_qsar_models(self, position):
        """
        Get the QSAR models for a position in the endpoint tree.
        """
        # make position url friendly
        position = quote(position)
        response = requests.get(f"{self.base_url}/qsar/list/{position}")
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Error: {response.status_code}")
        
    def apply_qsar_chemical(self, chem_id, qsar_model_guid):
        """
        apply the specified QSAR model to a chemical.
        """
        response = requests.get(f"{self.base_url}/qsar/apply/{qsar_model_guid}/{chem_id}")
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Error: {response.status_code}")
        
    def applicability_domain_qsar_chemical(self, chem_id, qsar_model_guid):
        """
        Get the applicability domain for a QSAR model and a chemical. returns a string that specifies whether the chemical is in the domain or not.
        """
        response = requests.get(f"{self.base_url}/qsar/domain/{qsar_model_guid}/{chem_id}")
        if response.status_code == 200:
            return response
        else:
            raise ValueError(f"Error: {response.status_code}")
        
    def search_CAS(self, casrn, ignoreStereo=True):
        """
        Search for a chemical by CASRN; casrn is an integer without dashes. Returns a JSON object.
        Example output:
        [
            {
                "SubstanceType": "Unknown",
                "ChemId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "Cas": 0,
                "ECNumber": "string",
                "Smiles": "string",
                "Names": [
                "string"
                ],
                "CasSmilesRelation": "string"
            }
        ]
        """
        if type(casrn) == str:
            casrn = int(casrn.replace("-", ""))
        if ignoreStereo:
            ignoreStereo = "true"
        else:
            ignoreStereo = "false"
        response = requests.get(f"{self.base_url}/search/cas/{casrn}/{ignoreStereo}")
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Error: {response.status_code}")
        
    def search_name(self, name, options="ExactMatch", ignoreStereo=True):
        """
        Search for a chemical by name. Returns a JSON object.
        options can be: "ExactMatch", "StartWith", "Contains"
        Example output:
        [
            {
                "SubstanceType": "Unknown",
                "ChemId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "Cas": 0,
                "ECNumber": "string",
                "Smiles": "string",
                "Names": [
                "string"
                ],
                "CasSmilesRelation": "string"
            }
        ]
        """
        acceptable_options = ["ExactMatch", "StartWith", "Contains"]
        if options not in acceptable_options:
            raise ValueError(f"options must be one of {acceptable_options}")
        if ignoreStereo:
            ignoreStereo = "true"
        else:
            ignoreStereo = "false"
        response = requests.get(f"{self.base_url}/search/name/{name}/{options}/{ignoreStereo}")
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Error: {response.status_code}")
        
    def search_smiles(self, smiles, registerUnknown = True, ignoreStereo=True):
        """
        search for a chemical by SMILES. Returns a JSON object.
        Example output:
        [
            {
                "SubstanceType": "Unknown",
                "ChemId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "Cas": 0,
                "ECNumber": "string",
                "Smiles": "string",
                "Names": [
                "string"
                ],
                "CasSmilesRelation": "string"
            }
        ]
        """
        if ignoreStereo:
            ignoreStereo = "true"
        else:
            ignoreStereo = "false"
        if registerUnknown:
            registerUnknown = "true"
        else:
            registerUnknown = "false"
        # convert smiles to url format using the requests library
        smiles_url = quote(smiles)
        response = requests.get(f"{self.base_url}/search/smiles/{registerUnknown}/{ignoreStereo}?smiles={smiles_url}")
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Error: {response.status_code}")
    
    def search_chemid(self, chemid: str):
        """
        Search for a chemical by ChemId. Returns a JSON object.
        Example output:
        {
            "SubstanceType": "Unknown",
            "ChemId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "Cas": 0,
            "ECNumber": "string",
            "Smiles": "string",
            "Names": [
            "string"
            ],
            "CasSmilesRelation": "string"
        }
        """
        response = requests.get(f"{self.base_url}/search/chemical/{chemid}")
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Error: {response.status_code}")
        
    def canonize_smiles(self, smiles):
        """
        Canonize a SMILES string. Returns a string.
        """
        # convert smiles to url format using the requests library
        smiles_url = quote(smiles)
        response = requests.get(f"{self.base_url}/structure/canonize?smiles={smiles_url}")
        if response.status_code == 200:
            return response
        else:
            raise ValueError(f"Error: {response.status_code}")
        
    def get_workflows(self):
        """
        Get the workflows. Returns a dictionary of the available workflows depending on your installation of the QSAR Toolbox.
        """
        response = requests.get(f"{self.base_url}/workflows")
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Error: {response.status_code}")
        
    def workflow_on_chemical(self, workflow_guid, chem_id, timeout=None):
        """
        Run a workflow on a chemical.
        """
        if timeout is None:
            timeout = self.timeout
        response = requests.get(f"{self.base_url}/workflows/{workflow_guid}/{chem_id}", timeout=timeout)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Error: {response.status_code}")
        
    # metabolism
    def get_metabolism_simulators(self):
        """
        Get all available metabolism simulators.
        """
        response = requests.get(f"{self.base_url}/metabolism")
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Error: {response.status_code}")
        
    def call_metabolism_simulator(self, simulator_guid, chem_id, timeout=None):
        """
        Call a metabolism simulator for a chemical.
        """
        if timeout is None:
            timeout = self.timeout
        response = requests.get(f"{self.base_url}/metabolism/{simulator_guid}/{chem_id}", timeout=timeout)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Error: {response.status_code}")
        
    def call_metabolism_simulator_on_SMILES(self, simulator_guid, smiles, timeout=None):
        """
        Call a metabolism simulator for a chemical.
        """
        if timeout is None:
            timeout = self.timeout
        # convert smiles to url format using the requests library
        smiles_url = quote(smiles)
        response = requests.get(f"{self.base_url}/metabolism/{simulator_guid}?smiles={smiles_url}", timeout=timeout)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Error: {response.status_code}")
        
    def get_CASRN_from_SMILES(self, smiles):
        """
        Get the CASRN from a SMILES string. Returns a string.
        """
        raise NotImplementedError("This function is not implemented yet.")
        pass

        
    def call_qsar_model(self, chem_id, model_name="EPI Suite", end_point="VP"):
        """
        Call a QSAR model for a chemical. Returns a Dictionary.
        """
        raise NotImplementedError("This function is not implemented yet.")
        pass

    def extract_experimental_data(self, chem_id, end_point="VP"):
        """
        Extract end point data for a chemical. Returns a Dictionary.
        """
        raise NotImplementedError("This function is not implemented yet.")
        pass
