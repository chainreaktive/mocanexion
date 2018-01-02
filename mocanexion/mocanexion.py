import pandas as pd
import requests
import xml.etree.ElementTree as et

class MocaNexion ():
    """
    A class to connect to MOCA.
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

    def build_xml(self, ):
        """
        Builds the XML request to send
        """



    def parse_response(self, response):
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
        headers = {'Content-Type': 'application/moca-xml'}
        ping = build_xml(user, "ping")

        try:
            requests.post(conn, data=ping, headers=headers)

            check_signon = build_xml(user, "check single signon where usr_id = '" + user + "'")
            response = et.fromstring(requests.post(conn, data=check_signon, headers=headers)).text)
            status = response.find("./status[1]").text

            if status == 0:
                single_signon = response.find("./moca-results/data/row/field[3]").text

                login_query = "login user where usr_id = '" + user + "' and usr_pswd = '" + password + "'"

                if single_signon == 1:
                    login_query += " and single_signon_flg = '1'"

                login = build_xml(user, login_query, None, device, warehouse, locale)

                response = et.fromstring(requests.post(conn, data=login, headers=headers)).text)
                login_status = response.find("./status[1]").text

                if login_status == 0:
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

        except requests.exceptions.RequestException as err:
            # do something here?


    def execute(self, cmd):
        """
        Executes a command on the server
        """
        #validate user is connected successfully here first

         command = build_xml(self.user, cmd, self.session_key, self.device, self.warehouse, self.locale)
         response = et.fromstring(requests.post(self.conn, data=command, headers=headers)).text)

         #try catch in case response is null? no data found? etc.?

         results = parse_response(response)

         return results
