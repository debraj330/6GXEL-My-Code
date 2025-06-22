VERBOSE = True


class XappManager:
    xApps = {}

    @classmethod
    def add_xApp(cls, name, xApp):
        if VERBOSE:
            print("Registering xApp with name %s." % name)
        if name in cls.xApps:
            raise RuntimeError("An xApp with that name already exists.")

        cls.xApps[name] = xApp
