import pandas as pd
import requests
import xml.etree.ElementTree as et
from xml.dom import minidom

class MocaNexion():
    """
    A class to connect to MOCA
    """

    def __init__(self):
        """
        Class constructor
        """
        self.conn = None
        self.user = None
        self.password = None
        self.session_key = None
        self.device = None
        self.warehouse = None
        self.locale = None

    def __build_xml(self, user, query, session_key=None, device=None, warehouse=None, locale=None):
        """
        Builds the XML request to send
        """
        moca_request_tag = et.Element('moca-request')
        moca_request_tag.set('autocommit', 'True')

        environment_tag = et.SubElement(moca_request_tag, 'environment')

        var_usr_id_tag = et.SubElement(environment_tag, 'var')
        var_usr_id_tag.set('name', 'USR_ID')
        var_usr_id_tag.set('value', user)

        if session_key is not None:
            var_session_key_tag = et.SubElement(environment_tag, 'var')
            var_session_key_tag.set('name', 'SESSION_KEY')
            var_session_key_tag.set('value', session_key)

        if device is not None:
            var_devcod_tag = et.SubElement(environment_tag, 'var')
            var_devcod_tag.set('name', 'DEVCOD')
            var_devcod_tag.set('value', device)

        if warehouse is not None:
            var_wh_id_tag = et.SubElement(environment_tag, 'var')
            var_wh_id_tag.set('name', 'WH_ID')
            var_wh_id_tag.set('value', warehouse)

        if locale is not None:
            var_locale_id = et.SubElement(environment_tag, 'var')
            var_locale_id.set('name', 'LOCALE_ID')
            var_locale_id.set('value', locale)

        query_tag = et.SubElement(moca_request_tag, 'query')
        query_tag.text = query
        rough_string = et.tostring(moca_request_tag, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ", encoding='UTF-8').decode('UTF-8')


    def __parse_response(self, response):
        """
        Parses the XML ElementTree response into a dataframe
        """
        # first ensure response isInstance of ElementTree, also make sure errors are handled correctly
        columnList = []
        dataList = []

        for column in response.iter('column'):
            columnList.append(column.attrib.get('name'))

        for curRow in response.iter('row'):
            dataRow = []

            for field in curRow.findall('field'):
                dataRow.append(field.text)

            dataList.append(dataRow)

        results = pd.DataFrame(dataList, columns=columnList)

        return results

    def connect(self, conn, user, password, device=None, warehouse=None, locale=None):
        """
        Opens the Connection
        """
        s = requests.Session()
        headers = {'Content-Type': 'application/moca-xml'}

        ping = self.__build_xml(user, "ping")

        s.post(conn, data=ping, headers=headers)

        check_signon = self.__build_xml(user, "check single signon where usr_id = '" + user + "'")
        response = et.fromstring(s.post(conn, data=check_signon, headers=headers).text)

        status = response.find("./status[1]")

        if status is None:
            status = response.find("./head/title[1]")

            if status is not None:
                status = status.text
            else:
                status = '404'

        else:
            status = status.text

        if status == '0':
            single_signon = response.find("./moca-results/data/row/field[3]").text

            login_query = "login user where usr_id = '" + user + "' and usr_pswd = '" + password + "'"

            if single_signon == '1':
                login_query += " and single_signon_flg = '1'"

            login = self.__build_xml(user, login_query, None, device, warehouse, locale)

            response = et.fromstring(s.post(conn, data=login, headers=headers).text)
            login_status = response.find("./status[1]").text

            if login_status == '0':
                self.conn = conn
                self.user = user
                self.password = password
                self.session_key = response.find("./moca-results/data/row/field[5]").text
                self.device = device
                self.warehouse = warehouse
                self.locale = response.find("./moca-results/data/row/field[2]").text

            else:
                error = response.find("./message[1]").text
                raise ValueError(error)

        else:
            raise ValueError('No User Data Found')


    def execute(self, cmd):
        """
        Executes a command on the server
        """
        s = requests.Session()
        headers = {'Content-Type': 'application/moca-xml'}

        command = self.__build_xml(self.user, cmd, self.session_key, self.device, self.warehouse, self.locale)
        response = et.fromstring(s.post(self.conn, data=command, headers=headers).text)

        status = response.find("./status[1]").text

        if status == '523':
            self.connect(self.conn, self.user, self.password, self.device, self.warehouse, self.locale)
            command = self.__build_xml(self.user, cmd, self.session_key, self.device, self.warehouse, self.locale)
            response = et.fromstring(s.post(self.conn, data=command, headers=headers).text)
            status = response.find("./status[1]").text

        if status != '0' and status != '510':
            message = response.find("./message[1]").text
            results = None

        else:
            results = self.__parse_response(response)

        return status,results
