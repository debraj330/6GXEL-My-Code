import inspect


class Validator:

    @staticmethod
    def validate_xApp(Xapp):
        xApp_required_attributes = [
                "node_id",
                "time_interval",
                "read_measurements",
                "send_commands",
                "cell_ids"
        ]

        # Validate that the virus object has all the required fields
        for attribute in xApp_required_attributes:
            if not hasattr(Xapp, attribute):
                raise RuntimeError("Attribute %s need to be defined on xApp object." % attribute)

        # Validate that the xApp object has all the required methods
        for method in inspect.getmembers(Xapp, predicate=inspect.ismethod):
            print(method)

        return True
