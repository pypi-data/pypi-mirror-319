"""
Need py3.7 min to run pytest
"""
import assetic
from datetime import datetime  #use to generate a unique asset id


class Setup(object):
    def __init__(self):
        self._api_client = None

    @property
    def api_client(self):
        return self._api_client

    @api_client.setter
    def api_client(self, value):
        self._api_client = value

    def init_asseticsdk(self):
        """
        Test initialising the SDK
        Assumes default settings
        :return: True unless exception
        """
        try:
            asseticsdk = assetic.AsseticSDK(None, None, 'INFO')
        except Exception as ex:
            raise ex
        self.api_client = asseticsdk.client
        return True

    def test_version_api(self):
        """
        Test version API by ensuring there is a response
        :return: True unless exception
        """
        version_api = assetic.VersionApi(api_client=self.api_client)
        try:
            response = version_api.version_get()
        except Exception as ex:
            print(ex)
            return False
        if "Major" not in response or response["Major"] < 2023:
            print("Major Version not found")
            return False
        print("Assetic Version: {0}.{1}.{2}.{3}".format(
            response["Major"], response["Minor"], response["Build"]
            , response["Revision"]))
        return True


class AssetTests(object):
    def __init__(self, api_client):
        self.assets_api = assetic.AssetApi(api_client=api_client)
        self.asset_tools = assetic.AssetTools(api_client=api_client)
        self.asset_config_api = assetic.AssetConfigurationApi(
            api_client=api_client)
        self.component_api = assetic.ComponentApi(api_client=api_client)
        self.maint_config_api = assetic.MaintenanceConfigurationApi(api_client=api_client)
        self._asset_id = None
        self._category_id = None
        self._asset_class = None
        self._asset_subclass = None
        self._asset_type_id = None
        self._asset_type = None
        self._asset_subtype_id = None
        self._asset_subtype = None
        self._auto_generate_asset_id = None
        self._component_type = None
        self._material = None
        self._workgroup = None
        self._workgroup2 = None
        self._criticality = None

        self.asset_category = "Buildings"

    @property
    def asset_id(self):
        return self._asset_id

    @asset_id.setter
    def asset_id(self, value):
        self._asset_id = value

    @property
    def asset_class(self):
        return self._asset_class

    @asset_class.setter
    def asset_class(self, value):
        self._asset_class = value

    @property
    def asset_subclass(self):
        return self._asset_subclass

    @asset_subclass.setter
    def asset_subclass(self, value):
        self._asset_subclass = value

    @property
    def asset_type_id(self):
        return self._asset_type_id

    @asset_type_id.setter
    def asset_type_id(self, value):
        self._asset_type_id = value

    @property
    def asset_type(self):
        return self._asset_type

    @asset_type.setter
    def asset_type(self, value):
        self._asset_type = value

    @property
    def asset_subtype_id(self):
        return self._asset_subtype_id

    @asset_subtype_id.setter
    def asset_subtype_id(self, value):
        self._asset_subtype_id = value

    @property
    def asset_subtype(self):
        return self._asset_subtype

    @asset_subtype.setter
    def asset_subtype(self, value):
        self._asset_subtype = value

    @property
    def category_id(self):
        return self._category_id

    @category_id.setter
    def category_id(self, value):
        self._category_id = value

    @property
    def autogenerate_id(self):
        return self._auto_generate_asset_id

    @autogenerate_id.setter
    def autogenerate_id(self, value):
        self._auto_generate_asset_id = value

    @property
    def component_type(self):
        return self._component_type

    @component_type.setter
    def component_type(self, value):
        self._component_type = value

    @property
    def material(self):
        return self._material

    @material.setter
    def material(self, value):
        self._material = value

    @property
    def workgroup(self):
        return self._workgroup

    @workgroup.setter
    def workgroup(self, value):
        self._workgroup = value

    @property
    def workgroup2(self):
        return self._workgroup2

    @workgroup2.setter
    def workgroup2(self, value):
        self._workgroup2 = value

    @property
    def criticality(self):
        return self._criticality

    @criticality.setter
    def criticality(self, value):
        self._criticality = value

    def get_assets(self):
        attributes = ["Zone"]
        try:
            response = self.assets_api.asset_get_0(attributes)
        except Exception as ex:
            raise ex

        if response["TotalResults"] > 0:
            self.asset_id = response["ResourceList"][0]["AssetId"]
        return True

    def get_complete_asset(self):
        if not self.asset_id:
            # no asset data to work with
            return True

        attributes = ["Zone"]
        inclusions = ["components", "dimensions", "service_criteria"]

        asset = self.asset_tools.get_complete_asset(
            assetid=self.asset_id, attributelist=attributes
            , inclusions=inclusions)
        if not asset:
            return False
        return True

    def test_get_workgroup_config(self):
        try:
            response = self.asset_config_api.asset_configuration_get_work_group()
        except Exception as ex:
            raise ex

        if response["TotalResults"] > 0:
            self.workgroup = response["ResourceList"][0]["Name"]
        if response["TotalResults"] > 1:
            self.workgroup2 = response["ResourceList"][1]["Name"]
        return True

    def test_get_asset_criticality_for_id(self):
        try:
            response = self.asset_config_api.asset_configuration_get_asset_criticality_by_id(self.category_id)
        except Exception as ex:
            raise ex

        if len(response["AssetCategoryCriticality"]) > 0:
            self.criticality = response["AssetCategoryCriticality"][0]["Label"]
        return True

    def create_test_asset_type_and_subtype(self):
        """
        Create an asset type and subtype
        """
        # generate id's based on the current time
        dt = datetime.now()
        type_name = "type{0}{1}{2}{3}{4}".format(
            dt.month, dt.day, dt.hour, dt.minute, dt.second)
        subtype_name1 = "subtype1{0}{1}{2}{3}{4}".format(
            dt.month, dt.day, dt.hour, dt.minute, dt.second)
        subtype_name2 = "subtype2{0}{1}{2}{3}{4}".format(
            dt.month, dt.day, dt.hour, dt.minute, dt.second)

        type_repr = assetic.CreateAssetTypeRepresentationForAV(name=type_name)
        subtype_repr1 = assetic.CreateAssetSubTypeRepresentationForAV(
            name=subtype_name1)
        subtype_repr2 = assetic.models.CreateAssetSubTypeRepresentationForAV(
            name=subtype_name2)
        type_repr.sub_types = [subtype_repr1, subtype_repr2]

        try:
            response = self.asset_config_api.asset_configuration_create_asset_type_and_sub_types(type_repr)
        except Exception as ex:
            raise ex

        if len(response["Data"]) > 0:
            self.asset_type_id = response["Data"][0]["Id"]
            self.asset_type = response["Data"][0]["Name"]
            if len(response["Data"][0]["SubTypes"]) > 0:
                self.asset_subtype_id = response["Data"][0]["SubTypes"][0]["Id"]
                self.asset_subtype = response["Data"][0]["SubTypes"][0]["Name"]
            else:
                return False
        else:
            return False
        return True

    def update_test_asset_type_and_subtype(self):
        if (not self.asset_type_id or not self.asset_type
                or not self.asset_subtype_id or not self.asset_subtype):
            return True
        asset_type_name_new = f"upd{self.asset_type}"
        asset_subtype_name_new = f"upd{self.asset_subtype}"
        subtype_repr = assetic.UpdateAssetSubTypeRepresentationForAV(
            id=self.asset_subtype_id, name = asset_subtype_name_new
        )
        type_repr = assetic.UpdateAssetTypeRepresentationForAV(
            id=self.asset_type_id, name=asset_type_name_new
            , sub_types=[subtype_repr]
        )

        try:
            self.asset_config_api.asset_configuration_update_asset_type_and_sub_types(type_repr)
        except Exception as ex:
            raise ex
        self.asset_type = asset_type_name_new
        self.asset_subtype = asset_subtype_name_new
        return True

    def create_test_asset_class_and_subclass(self):
        """
        Create an asset class and subclass
        """
        # generate id's based on the current time
        dt = datetime.now()
        class_name = "class{0}{1}{2}{3}{4}".format(
            dt.month, dt.day, dt.hour, dt.minute, dt.second)
        subclass_name1 = "subclass1{0}{1}{2}{3}{4}".format(
            dt.month, dt.day, dt.hour, dt.minute, dt.second)
        subclass_name2 = "subclass2{0}{1}{2}{3}{4}".format(
            dt.month, dt.day, dt.hour, dt.minute, dt.second)

        class_repr = assetic.CreateAssetClassRepresentationForAV(name=class_name)
        subclass_repr1 = assetic.CreateAssetSubClassRepresentationForAV(
            name=subclass_name1)
        subclass_repr2 = assetic.models.CreateAssetSubClassRepresentationForAV(
            name=subclass_name2)
        class_repr.sub_classes = [subclass_repr1, subclass_repr2]

        try:
            response = self.asset_config_api.asset_configuration_create_asset_class_and_sub_classes(class_repr)
        except Exception as ex:
            raise ex

        if len(response["Data"]) > 0:
            self.asset_class = response["Data"][0]["Name"]
            if len(response["Data"][0]["SubClasses"]) > 0:
                self.asset_subclass = response["Data"][0]["SubClasses"][0]["Name"]
            else:
                return False
        else:
            return False
        return True

    def create_test_asset(self):
        """
        Create a test asset
        """

        # generate a id based on the current time
        dt = datetime.now()
        unique_id = "{0}{1}{2}{3}{4}".format(
            dt.month, dt.day, dt.hour, dt.minute, dt.second)
        # instantiate the complete asset representation
        complete_asset_obj = assetic.AssetToolsCompleteAssetRepresentation()

        # create an instance of the complex asset object
        asset = assetic.ComplexAssetRepresentation()
        # mandatory fields
        asset.asset_category = self.asset_category
        asset.status = "Active"
        if self.autogenerate_id:
            # need to set ID as not autogenerated
            asset.asset_id = unique_id
        asset.asset_name = "UT{0}".format(unique_id)
        if self.asset_class and self.asset_subclass:
            asset.asset_class = self.asset_class
            asset.asset_sub_class = self.asset_subclass
        if self.asset_type and self.asset_subtype:
            asset.asset_type = self.asset_type
            asset.asset_sub_type = self.asset_subtype
        if self.workgroup:
            asset.asset_work_group = self.workgroup
            workgroups = [self.workgroup]
            if self.workgroup2:
                workgroups.append(self.workgroup2)
            asset.work_groups = workgroups
        if self.criticality:
            asset.asset_criticality = self.criticality

        complete_asset_obj.asset_representation = asset

        # array list to put component plus dimensions
        components_and_dims = []

        # instantiate complete component representation
        component_obj = assetic.AssetToolsComponentRepresentation()

        # create an instance of the component representation
        component = assetic.ComponentRepresentation()
        componentname = "{0}CMP1".format(asset.asset_name)
        component.asset_id = asset.asset_id
        component.label = "Main Label"  # "Component Name in UI
        if self.component_type:
            component.component_type = self.component_type
        else:
            component.component_type = "Main"
        component.dimension_unit = "Metre"
        component.network_measure_type = "Length"
        # optional fields
        component.design_life = 50
        component.external_identifier = "Ext{0}".format(componentname)
        if self.material:
            component.material_type = self.material
        # Add the component to the components
        component_obj.component_representation = component

        # create an array for the dimensions to be added to the component
        dimlist = []

        # Create an instance of the dimension and set minimum fields
        dim = assetic.ComponentDimensionRepresentation()
        dim.network_measure = 75.7
        dim.unit = "Metre"
        dim.record_type = "Info"  # could also be "Subtraction" or "Info"
        dim.network_measure_type = "Length"
        # can also include additional fields
        dim.comments = "Created via API"
        dim.multiplier = 2.5  # will default as 1 if undefined
        dimlist.append(dim)

        ##Create an instance of the dimension and set minimum fields
        dim = assetic.ComponentDimensionRepresentation()
        dim.network_measure = 3
        dim.unit = "Metre"
        dim.record_type = "Subtraction"  # could also be "Subtraction" or "Info"
        dim.network_measure_type = "Length"
        # can also include additional fields
        dim.comments = "Created via API"
        dim.multiplier = 1  # will default as 1 if undefined
        dimlist.append(dim)

        # Add the dimension array to the component
        component_obj.dimensions = dimlist

        # Add component to the list
        components_and_dims.append(component_obj)

        # add the component & dims array to the complete asset object
        complete_asset_obj.components = components_and_dims

        # create the complete asset
        response = self.asset_tools.create_complete_asset(complete_asset_obj)

        if len(response.asset_representation.id) > 0:
            # get some ID's
            assetid = response.asset_representation.asset_id
            self.asset_id = assetid
            return True
        else:
            return False

    def test_category_fields_api(self):
        """
        Test asset category field list api for given category id
        """
        # define page size (no of records) and page number to get
        pagesize = 50
        sortorder = "Name-desc"
        pagenum = 1
        # attfilter = None
        kwargs = {"request_params_page": pagenum,
                  "request_params_page_size": pagesize,
                  "request_params_sorts": sortorder
                  }
        # "request_params_filters": attfilter}
        if not self.category_id:
            raise Exception("Category GUID not set in test, unable to test api for get_category_fields")
        try:
            response = self.asset_config_api.asset_configuration_get_asset_attributes_by_category_id(
                self.category_id, **kwargs)
        except Exception as ex:
            raise ex
        if len(response["ResourceList"]) > 0:
            return True

    def test_category_configuration_api(self):
        """
        Test asset category configuration api
        """
        try:
            response = self.asset_config_api.asset_configuration_get_asset_category()
        except Exception as ex:
            raise ex
        for cat in response["ResourceList"]:
            if cat["Label"] == self.asset_category:
                self.category_id = cat["Id"]
                self.autogenerate_id = False
                if cat["UseAutogeneratedId"] == "true":
                    self.autogenerate_id = True
        return True

    def test_category_components(self):
        """
        Test get component types for given category id
        """
        # define page size (no of records) and page number to get
        pagesize = 50
        sortorder = "ComponentType-desc"
        pagenum = 1
        # attfilter = None
        kwargs = {"request_params_page": pagenum,
                  "request_params_page_size": pagesize,
                  "request_params_sorts": sortorder}
        #                   "request_params_filters": attfilter
        if not self.category_id:
            raise Exception("Category GUID not set in test, unable to test api for get_category_fields")
        try:
            response = self.component_api.component_get_component_types(self.category_id, **kwargs)
        except Exception as ex:
            raise ex
        if len(response["ResourceList"]) > 0:
            self.component_type = response["ResourceList"][0]["ComponentType"]
        return True

    def test_maint_material_api(self):
        """
        Test get material types (same as bill of material)
        """
        # define page size (no of records) and page number to get
        pagesize = 50
        sortorder = "Label-desc"
        pagenum = 1
        # attfilter = None
        kwargs = {"request_params_page": pagenum,
                  "request_params_page_size": pagesize,
                  "request_params_sorts": sortorder}
        #                   "request_params_filters": attfilter
        if not self.category_id:
            raise Exception("Category GUID not set in test, unable to test api for get_category_fields")
        try:
            response = self.maint_config_api.maintenance_configuration_get_material_types(**kwargs)
        except Exception as ex:
            raise ex
        if len(response["ResourceList"]) > 0:
            self.material = response["ResourceList"][0]["Label"]
        return True

class ReportingTests(object):
    """
    Tests for Reporting module
    """
    def __init__(self, api_client):
        self.report_view_api = assetic.ReportingViewApi(api_client=api_client)
        self.report_export_api = assetic.ReportingExportApi(api_client=api_client)
        self._report_id = None
        self._export_id = None

    def get_reports(self):
        try:
            response = self.report_view_api.reporting_view_get_list()
        except Exception as ex:
            print(ex)
            return False
        if len(response) > 0:
            self._report_id = response[0]["id"]
        return True

    def initiate_export(self):
        try:
            response = self.report_export_api.reporting_export_post_export(self._report_id)
        except Exception as ex:
            print(ex)
            return False
        if len(response) > 0:
            self._export_id = response["id"]
        return True

    def get_export_status(self):
        try:
            response = self.report_export_api.reporting_export_get_export(self._export_id)
        except Exception as ex:
            print(ex)
            return False
        status = response["status"]
        return True


# initiate setup class
setup_tests = Setup()
setup_tests.init_asseticsdk()
# check we have a api_client setting
if setup_tests.api_client.configuration.password == "" or \
        setup_tests.api_client.configuration.host == "https://xxx.assetic.net":
    raise Exception("Package test authorisation not set")

# initiate SDK to set client
# setup_tests.init_asseticsdk()
# Initiate other classes.
asset_tests = AssetTests(setup_tests.api_client)
reporting_tests = ReportingTests(setup_tests.api_client)

def test_setup():
    """
    test initialisation of sdk
    """
    assert setup_tests.init_asseticsdk()


def test_version():
    """
    test version API, fails if unable to get Assetic version
    """
    assert setup_tests.test_version_api()


def test_category_collection_api():
    """
    test the api that returns collection of high level category details
    """
    assert asset_tests.test_category_configuration_api()


def test_category_field_collection_api():
    """
    test the api that returns collection of fields for a category
    """
    assert asset_tests.test_category_fields_api()


def test_get_workgroup_api():
    """
    test the api that returns collection of fields for a category
    """
    assert asset_tests.test_get_workgroup_config()

def test_get_criticality_api():
    """
    test the api that returns collection of fields for a category
    """
    assert asset_tests.test_get_asset_criticality_for_id()

def test_category_component_types():
    """
    test getting a collection of component types for a given category
    """
    assert asset_tests.test_category_components()


def test_maint_config_material():
    """
    testr av material list api = gets material label and id
    """
    assert asset_tests.test_maint_material_api()

def test_asset_collection_get():
    """
    test the asset GET collection API
    """
    assert asset_tests.get_assets()


def test_create_asset_class():
    """
    test the api that creates asset class and subclasses
    """
    assert asset_tests.create_test_asset_class_and_subclass()


def test_create_asset_type():
    """
    test the api that creates asset type and subtype
    """
    assert asset_tests.create_test_asset_type_and_subtype()


def test_update_asset_type():
    """
    test the api that updates asset type and subtype
    """
    assert asset_tests.update_test_asset_type_and_subtype()

def test_get_complete_asset():
    """
    test the tool get complete asset using an asset from
    the result of test_asset_collection_get
    """
    assert asset_tests.get_complete_asset()


def test_create_complete_asset():
    """
    test the tool create asset in Buildings category
    """
    assert asset_tests.create_test_asset()


def test_get_reports_list():
    """
    test the tool get a list of saved reports
    """
    assert reporting_tests.get_reports()


def test_initiate_export_report():
    """
    test the tool get a list of saved reports
    """
    assert reporting_tests.initiate_export()


def test_get_export_report_status():
    """
    test the tool get a list of saved reports
    """
    assert reporting_tests.get_export_status()
