from uuid import UUID


class BaseDAO:
    def _convert_uuids_to_strings(self, data_dict) -> dict:
        converted_data = {}
        for key, value in data_dict.items():
            if isinstance(value, UUID):
                converted_data[key] = str(value)
            else:
                converted_data[key] = value
        return converted_data
