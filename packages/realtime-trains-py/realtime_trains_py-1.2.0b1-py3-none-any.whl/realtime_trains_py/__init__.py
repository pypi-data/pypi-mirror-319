# Import classes from board_data and service_data
try:
    from realtime_trains_py.services.board_data import Boards
    from realtime_trains_py.services.service_data import ServiceAdvanced, ServiceSimple, ServiceDetails
except:
    from services.board_data import Boards
    from services.service_data import ServiceAdvanced, ServiceSimple, ServiceDetails


class RealtimeTrainsPy():
    def __init__(self, complexity = "s", username: str = None, password: str = None) -> None: 
        """
        ## Initialize realtime_trains_py.
        ### complexity (optional)
            A string representing the complexity level of the data. The default is "s".
        
        ### username (required)
            A string representing the username for authentication.

        ### password (required)
            A string representing the password for authentication.

        ## Example
        ```python
        rtt = RealtimeTrainsPy(complexity = "s", username = "a_username", password = "1234567890")
        ```
        """
        # Check if the username and password have been entered
        if username == None or password == None:
            # If at least one is missing, raise an error
            raise ValueError("Missing authentication details. Both username and password must be provided. Not all required fields were provided.")

        self._username = username
        self.__password = password

        # Check if selected complexity is valid
        if complexity.lower() not in ["s", "s.p", "s.n", "a", "a.p", "a.n", "c"]:
            # If complexity is not in the valid range, raise an error
            raise ValueError("Complexity not recognised. Select a valid type.")
        
        self.__services = ServiceDetails(username = self._username, password = self.__password, complexity = complexity.lower())
        self.__boards = Boards(username = self._username, password = self.__password, complexity = complexity.lower())

    def get_departures(self, tiploc: str, filter: str = None, date: str = None, rows: int = None, time: str = None) -> list | str:
        """
        ## Parameters

        ### tiploc (required)

            A string representing the Timing Point Location Code (TIPLOC) or Computer Reservation Code (CRS) of the station.

        ### filter (optional)
            A string representing the Timing Point Location Code (TIPLOC) or Computer Reservation Code (CRS) of the filter station.

        ### date (optional)
            A string representing the date in the format YYYY/MM/DD.

        ### rows (optional)
            An integer representing the maximum number of rows to return. (Only available for simple and advanced complexity.)

        ### time (optional)
            A string representing the time in the format HHMM. 

        ### Examples
        ```python
        get_departures(tiploc = "KNGX", filter = "STEVNGE", date = "2024/11/16", time = "1800", rows = 10)

        get_departures(tiploc = "YORK", date = "2024/11/16", time = "1800")
        ```
        """
        return self.__boards._get_dep_board_details(tiploc = tiploc, search_filter = filter, date = date, rows = rows, time = time)

    def get_arrivals(self, tiploc: str, filter: str = None, date: str = None, rows: int = None, time: str = None) -> list | str:
        """
        ## Parameters

        ### tiploc (required)

            A string representing the Timing Point Location Code (TIPLOC) or Computer Reservation Code (CRS) of the station.

        ### filter (optional)
            A string representing the Timing Point Location Code (TIPLOC) or Computer Reservation Code (CRS) of the filter station.

        ### date (optional)
            A string representing the date in the format YYYY/MM/DD.

        ### rows (optional)
            An integer representing the maximum number of rows to return. (Only available for simple and advanced complexity.)

        ### time (optional)
            A string representing the time in the format HHMM. 

        ### Examples
        ```python
        get_arrivals(tiploc = "KNGX", filter = "STEVNGE", date = "2024/11/16", time = "1800", rows = 10)

        get_arrivals(tiploc = "YORK", date = "2024/11/16", time = "1800")
        ```
        """
        return self.__boards._get_arr_board_details(tiploc = tiploc, search_filter = filter, date = date, rows = rows, time = time)

    def get_service(self, service_uid: str, date: str = None) -> ServiceAdvanced | ServiceSimple | str:
        """
        ## Parameters

        ### service_uid (required)
            A string representing the Service Unique Identity (UID) code.

        ### date (optional)
            A string representing the date in the format YYYY/MM/DD.

        ### time (optional)
            A string representing the time in the format HHMM. 

        ### Examples
        ```python
        get_service(service_uid = "G54071", date = "2024/11/16", time = "1800")

        get_service(service_uid = "G26171")
        ```
        """
        return self.__services._get_service_details(service_uid = service_uid, date = date)
    
    def get_station(self, tiploc: str, filter: str = None, date: str = None, rows: int = None, time: str = None) -> list | str:
        """
        ## This feature is only available for complex mode

        ### tiploc (required)

            A string representing the Timing Point Location Code (TIPLOC) or Computer Reservation Code (CRS) of the station.

        ### filter (optional)
            A string representing the Timing Point Location Code (TIPLOC) or Computer Reservation Code (CRS) of the filter station.

        ### date (optional)
            A string representing the date in the format YYYY/MM/DD.

        ### rows (optional)
            An integer representing the maximum number of rows to return. (Only available for simple and advanced complexity.)

        ### time (optional)
            A string representing the time in the format HHMM. 

        ### Examples
        ```python
        get_station(tiploc = "KNGX", filter = "STEVNGE", date = "2024/11/16", time = "1800", rows = 10)

        get_station(tiploc = "YORK", date = "2024/11/16", time = "1800")
        ```
        """
        return self.__boards._get_stat_board_details(tiploc = tiploc, search_filter = filter, date = date, rows = rows, time = time)