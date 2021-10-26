from configparser import RawConfigParser


def get_config_info(filename, section):
    """Returns the content of config file by section

    Args:
        filename (str): Name of the config file.
        section (str): Name of the section on config file.

    Returns:
        dict : Specified section of config file.

    Usage Example:
        config.get_config_info('service.ini')
    """
    parser = RawConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} not found in the {1} file'.format(section, filename))
    return db
