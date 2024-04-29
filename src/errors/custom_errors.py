class EaterNotExist(Exception):
    def __init__(self, message="EaterNotExist") -> None:
        self.message = message
        super().__init__(self.message)


class ExistingReservationDuringTimeFrame(Exception):
    def __init__(self, message="ExistingReservationDuringTimeFrame") -> None:
        self.message = message
        super().__init__(self.message)


class RestaurantCantFulfillReservation(Exception):
    def __init__(self, message="RestaurantCantFulfillReservation") -> None:
        self.message = message
        super().__init__(self.message)
