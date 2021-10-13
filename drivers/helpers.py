

def get_auth_data_by_driver_name(driver_name):
    driver_module = __import__(f"drivers.drivers.{driver_name}", fromlist=[driver_name])
    class_ = getattr(driver_module, driver_name)
    return class_.get_required_fields()