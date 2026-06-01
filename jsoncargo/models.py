class Container:
    """
    Represents a tracked container.

    Attributes:
        container_id (str): Container number, e.g. MSCU1234567
        container_type (str): Container type, e.g. "40' HIGH CUBE REEFER"
        status (str): Current container status
        shipping_line_name (str): Full shipping line name
        shipping_line_id (str): Internal shipping line ID
        tare (float): Tare weight in kg
        shipped_from (str): Origin location
        shipped_from_terminal (str): Origin terminal name
        shipped_to (str): Destination location
        shipped_to_terminal (str): Destination terminal name
        atd_origin (str): Actual time of departure from origin
        eta_final_destination (str): ETA at final destination
        last_location (str): Most recent known location
        last_location_terminal (str): Most recent terminal
        next_location (str): Next expected location
        next_location_terminal (str): Next expected terminal
        atd_last_location (str): ATD from last location
        eta_next_destination (str): ETA at next destination
        timestamp_of_last_location (str): Timestamp of last location update
        last_movement_timestamp (str): Timestamp of last movement
        loading_port (str): Port of loading
        discharging_port (str): Port of discharge
        customs_clearance (str): Customs clearance datetime
        bill_of_lading (str): Associated bill of lading number
        last_vessel_name (str): Name of last vessel
        last_voyage_number (str): Last voyage number
        current_vessel_name (str): Name of current vessel
        current_voyage_number (str): Current voyage number
        last_updated (str): When this data was last refreshed
        raw (dict): Full raw response data
    """

    def __init__(self, data: dict):
        self.container_id = data.get("container_id")
        self.container_type = data.get("container_type")
        self.status = data.get("container_status")
        self.shipping_line_name = data.get("shipping_line_name")
        self.shipping_line_id = data.get("shipping_line_id")
        self.tare = data.get("tare")
        self.shipped_from = data.get("shipped_from")
        self.shipped_from_terminal = data.get("shipped_from_terminal")
        self.shipped_to = data.get("shipped_to")
        self.shipped_to_terminal = data.get("shipped_to_terminal")
        self.atd_origin = data.get("atd_origin")
        self.eta_final_destination = data.get("eta_final_destination")
        self.last_location = data.get("last_location")
        self.last_location_terminal = data.get("last_location_terminal")
        self.next_location = data.get("next_location")
        self.next_location_terminal = data.get("next_location_terminal")
        self.atd_last_location = data.get("atd_last_location")
        self.eta_next_destination = data.get("eta_next_destination")
        self.timestamp_of_last_location = data.get("timestamp_of_last_location")
        self.last_movement_timestamp = data.get("last_movement_timestamp")
        self.loading_port = data.get("loading_port")
        self.discharging_port = data.get("discharging_port")
        self.customs_clearance = data.get("customs_clearance")
        self.bill_of_lading = data.get("bill_of_lading")
        self.last_vessel_name = data.get("last_vessel_name")
        self.last_voyage_number = data.get("last_voyage_number")
        self.current_vessel_name = data.get("current_vessel_name")
        self.current_voyage_number = data.get("current_voyage_number")
        self.last_updated = data.get("last_updated")
        self.raw = data

    def __repr__(self):
        return f"Container(id={self.container_id!r}, status={self.status!r})"


class BolResult:
    """
    Represents the result of a bill of lading lookup.

    Attributes:
        bill_of_lading (str): The BOL number
        shipping_line_name (str): Full shipping line name
        shipping_line_id (str): Internal shipping line ID
        associated_containers (int): Number of containers on this BOL
        associated_container_numbers (list[str]): List of container numbers
        last_updated (str): When this data was last refreshed
        raw (dict): Full raw response data
    """

    def __init__(self, data: dict):
        self.bill_of_lading = data.get("bill_of_lading")
        self.shipping_line_name = data.get("shipping_line_name")
        self.shipping_line_id = data.get("shipping_line_id")
        self.associated_containers = data.get("associated_containers")
        self.associated_container_numbers = data.get("associated_container_numbers", [])
        self.last_updated = data.get("last_updated")
        self.raw = data

    def __repr__(self):
        return (
            f"BolResult(bol={self.bill_of_lading!r}, "
            f"containers={self.associated_containers})"
        )


class VesselBasic:
    """
    Represents a vessel from the basic tracking endpoint.

    Attributes:
        uuid (str): Internal vessel UUID
        name (str): Vessel name
        mmsi (str): Maritime Mobile Service Identity
        imo (str): IMO number
        eni (str): European Number of Identification
        country_iso (str): Flag country ISO code
        type (str): Vessel type
        type_specific (str): Specific vessel type
        lat (float): Latitude
        lon (float): Longitude
        speed (float): Speed over ground
        course (float): Course over ground
        heading (float): True heading
        navigation_status (str): AIS navigation status
        destination (str): Reported destination
        last_position_epoch (int): Last position time (epoch seconds)
        last_position_UTC (str): Last position time (UTC string)
        eta_epoch (int): ETA (epoch seconds)
        eta_UTC (str): ETA (UTC string)
        raw (dict): Full raw response data
    """

    def __init__(self, data: dict):
        self.uuid = data.get("uuid")
        self.name = data.get("name")
        self.mmsi = data.get("mmsi")
        self.imo = data.get("imo")
        self.eni = data.get("eni")
        self.country_iso = data.get("country_iso")
        self.type = data.get("type")
        self.type_specific = data.get("type_specific")
        self.lat = data.get("lat")
        self.lon = data.get("lon")
        self.speed = data.get("speed")
        self.course = data.get("course")
        self.heading = data.get("heading")
        self.navigation_status = data.get("navigation_status")
        self.destination = data.get("destination")
        self.last_position_epoch = data.get("last_position_epoch")
        self.last_position_UTC = data.get("last_position_UTC")
        self.eta_epoch = data.get("eta_epoch")
        self.eta_UTC = data.get("eta_UTC")
        self.raw = data

    def __repr__(self):
        return f"VesselBasic(name={self.name!r}, mmsi={self.mmsi!r})"


class VesselPro:
    """
    Represents a vessel from the pro tracking endpoint (superset of basic).

    Attributes:
        uuid (str): Internal vessel UUID
        name (str): Vessel name
        mmsi (str): Maritime Mobile Service Identity
        imo (str): IMO number
        eni (str): European Number of Identification
        country_iso (str): Flag country ISO code
        type (str): Vessel type
        type_specific (str): Specific vessel type
        lat (float): Latitude
        lon (float): Longitude
        speed (float): Speed over ground
        course (float): Course over ground
        heading (float): True heading
        navigation_status (str): AIS navigation status
        destination (str): Reported destination
        last_position_epoch (int): Last position time (epoch seconds)
        last_position_UTC (str): Last position time (UTC string)
        eta_epoch (int): ETA (epoch seconds)
        eta_UTC (str): ETA (UTC string)
        current_draught (float): Current draught
        dest_port_uuid (str): Destination port UUID
        dest_port (str): Destination port name
        dest_port_unlocode (str): Destination port UN/LOCODE
        dep_port_uuid (str): Departure port UUID
        dep_port (str): Departure port name
        dep_port_unlocode (str): Departure port UN/LOCODE
        atd_epoch (int): Actual time of departure (epoch seconds)
        atd_UTC (str): Actual time of departure (UTC string)
        timezone_offset_sec (int): Timezone offset in seconds
        timezone (str): Timezone name
        raw (dict): Full raw response data
    """

    def __init__(self, data: dict):
        self.uuid = data.get("uuid")
        self.name = data.get("name")
        self.mmsi = data.get("mmsi")
        self.imo = data.get("imo")
        self.eni = data.get("eni")
        self.country_iso = data.get("country_iso")
        self.type = data.get("type")
        self.type_specific = data.get("type_specific")
        self.lat = data.get("lat")
        self.lon = data.get("lon")
        self.speed = data.get("speed")
        self.course = data.get("course")
        self.heading = data.get("heading")
        self.navigation_status = data.get("navigation_status")
        self.destination = data.get("destination")
        self.last_position_epoch = data.get("last_position_epoch")
        self.last_position_UTC = data.get("last_position_UTC")
        self.eta_epoch = data.get("eta_epoch")
        self.eta_UTC = data.get("eta_UTC")
        self.current_draught = data.get("current_draught")
        self.dest_port_uuid = data.get("dest_port_uuid")
        self.dest_port = data.get("dest_port")
        self.dest_port_unlocode = data.get("dest_port_unlocode")
        self.dep_port_uuid = data.get("dep_port_uuid")
        self.dep_port = data.get("dep_port")
        self.dep_port_unlocode = data.get("dep_port_unlocode")
        self.atd_epoch = data.get("atd_epoch")
        self.atd_UTC = data.get("atd_UTC")
        self.timezone_offset_sec = data.get("timezone_offset_sec")
        self.timezone = data.get("timezone")
        self.raw = data

    def __repr__(self):
        return f"VesselPro(name={self.name!r}, mmsi={self.mmsi!r})"


class VesselBulkResult:
    """
    Represents the result of a bulk vessel tracking lookup.

    Attributes:
        total (int): Total number of vessels returned
        vessels (list[VesselBasic]): List of VesselBasic objects
        raw (dict): Full raw response data
    """

    def __init__(self, data: dict):
        self.total = data.get("total")
        self.vessels = [VesselBasic(v) for v in data.get("vessels", [])]
        self.raw = data

    def __repr__(self):
        return f"VesselBulkResult(total={self.total})"


class VesselInfo:
    """
    Represents a vessel's specification from the finder and specs endpoints.

    Attributes:
        uuid (str): Internal vessel UUID
        name (str): Vessel name
        name_ais (str): Vessel name as broadcast over AIS
        mmsi (str): Maritime Mobile Service Identity
        imo (str): IMO number
        eni (str): European Number of Identification
        country_iso (str): Flag country ISO code
        country_name (str): Flag country name
        callsign (str): Radio callsign
        type (str): Vessel type
        type_specific (str): Specific vessel type
        gross_tonnage (int): Gross tonnage
        deadweight (int): Deadweight tonnage
        teu (int): Twenty-foot equivalent unit capacity
        liquid_gas (float): Liquid gas capacity
        length (float): Overall length
        breadth (float): Breadth
        draught_avg (float): Average draught
        draught_max (float): Maximum draught
        speed_avg (float): Average speed
        speed_max (float): Maximum speed
        year_built (int): Year built
        is_navaid (bool): Whether the vessel is a navigation aid
        home_port (str): Home port
        raw (dict): Full raw response data
    """

    def __init__(self, data: dict):
        self.uuid = data.get("uuid")
        self.name = data.get("name")
        self.name_ais = data.get("name_ais")
        self.mmsi = data.get("mmsi")
        self.imo = data.get("imo")
        self.eni = data.get("eni")
        self.country_iso = data.get("country_iso")
        self.country_name = data.get("country_name")
        self.callsign = data.get("callsign")
        self.type = data.get("type")
        self.type_specific = data.get("type_specific")
        self.gross_tonnage = data.get("gross_tonnage")
        self.deadweight = data.get("deadweight")
        self.teu = data.get("teu")
        self.liquid_gas = data.get("liquid_gas")
        self.length = data.get("length")
        self.breadth = data.get("breadth")
        self.draught_avg = data.get("draught_avg")
        self.draught_max = data.get("draught_max")
        self.speed_avg = data.get("speed_avg")
        self.speed_max = data.get("speed_max")
        self.year_built = data.get("year_built")
        self.is_navaid = data.get("is_navaid")
        self.home_port = data.get("home_port")
        self.raw = data

    def __repr__(self):
        return f"VesselInfo(name={self.name!r}, imo={self.imo!r})"


class Port:
    """
    Represents a port from the port finder endpoint.

    Attributes:
        port_name (str): Port name
        port_code (str): Port code
        country (str): Country
        lat (float): Latitude
        lon (float): Longitude
        port_type (str): Port type
        size (str): Port size
        area (str): Area
        city (str): City
        unlocode (str): UN/LOCODE
        uuid (str): Internal port UUID
        country_iso (str): Country ISO code
        country_name (str): Country name
        area_lvl1 (str): Area level 1
        area_lvl2 (str): Area level 2
        raw (dict): Full raw response data
    """

    def __init__(self, data: dict):
        self.port_name = data.get("port_name")
        self.port_code = data.get("port_code")
        self.country = data.get("country")
        self.lat = data.get("lat")
        self.lon = data.get("lon")
        self.port_type = data.get("port_type")
        self.size = data.get("size")
        self.area = data.get("area")
        self.city = data.get("city")
        self.unlocode = data.get("unlocode")
        self.uuid = data.get("uuid")
        self.country_iso = data.get("country_iso")
        self.country_name = data.get("country_name")
        self.area_lvl1 = data.get("area_lvl1")
        self.area_lvl2 = data.get("area_lvl2")
        self.raw = data

    def __repr__(self):
        return f"Port(name={self.port_name!r}, unlocode={self.unlocode!r})"


class Terminal:
    """
    Represents a terminal from the terminal finder endpoint.

    Attributes:
        unlocode (str): UN/LOCODE
        alt_unlocode (str): Alternative UN/LOCODE
        code (str): Terminal code
        terminal_name (str): Terminal name
        company_name (str): Operating company name
        lat (float): Latitude
        lon (float): Longitude
        url (str): Terminal URL
        address (str): Terminal address
        raw (dict): Full raw response data
    """

    def __init__(self, data: dict):
        self.unlocode = data.get("unlocode")
        self.alt_unlocode = data.get("alt_unlocode")
        self.code = data.get("code")
        self.terminal_name = data.get("terminal_name")
        self.company_name = data.get("company_name")
        self.lat = data.get("lat")
        self.lon = data.get("lon")
        self.url = data.get("url")
        self.address = data.get("address")
        self.raw = data

    def __repr__(self):
        return f"Terminal(name={self.terminal_name!r}, unlocode={self.unlocode!r})"
