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
