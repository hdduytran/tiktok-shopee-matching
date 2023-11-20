
from datetime import datetime
import re
from urllib.parse import urlparse



class Common:
    @classmethod
    def get_dict_data_by_path(cls, _dict, keys):
        return cls.get_dict_data_by_path(_dict[keys[0]], keys[1:]) \
            if keys else _dict

    @staticmethod
    def set_value_from_other_key_when_first_key_not_exist(_dict, first_key, second_key, default_value):
        if first_key not in _dict:
            _dict[first_key] = _dict.get(second_key, default_value)
        return _dict

    @staticmethod
    def logging_exceptions_and_bypass(f, *args, **kwargs):
        try:
            f(*args, **kwargs)
        except Exception as e:
            print("we have a problem: {0}".format(e))

    @staticmethod
    def remove_key(dict_: dict, list_key: list):
        """
        Remove key replaced
        Input:
            - dict (dict): dict to remove key
        Output:
            - list_key (list): key list want to remove
        """
        for key in list_key:
            try:
                del dict_[key]
            except KeyError:
                continue

    @staticmethod
    def parse_url(url: str):
        """
        Input:
            - url (str): url need to parse
        Output:
            - url_object (ParseResult): elements of url
        """
        url_object = urlparse(url)
        return url_object

    @staticmethod
    def get_highest_value_from_dict(dict_target: dict, list_order: list):
        target_value = None
        if isinstance(dict_target, dict) and isinstance(list_order, list):
            for key in list_order:
                if key in dict_target:
                    target_value = dict_target[key]
                    break
        return target_value

    @staticmethod
    def get_all_javascript_object_text(text: str, contain_text: str = None) -> list:
        """
        Get all javascript object from text
        Input:
            - text (str): text
            - contain_text (str): text need to contain
        Output:
            - list_javascript_object (list): list json object
        """

        import chompjs

        # Remove newlines, tabs, and multiple whitespaces
        text = re.sub(r'[\n\t]+|\s{2,}', '', text)

        # Replace ', }' with '}' and remove trailing commas
        text = re.sub(r',\s*}', '}', text)
        patterns = [r'\{\w+\:.*?\}\);', r'\(\w+\,\s*\{.*?\}\);']
        matches = []
        return_objects = []
        for pattern in patterns:
            matches += re.findall(pattern, text, re.DOTALL)
        if contain_text:
            matches = [match for match in matches if contain_text in match]

        for match in matches:
            try:
                match = match.replace(');', '')
                match = match.replace('({', '{')
                # print(match)
                py_obj = chompjs.parse_js_object(match)
                return_objects.append(py_obj)
                # print(py_obj)
            except Exception:
                continue

        return return_objects

    @staticmethod
    def safest_get(dct, *keys):
        for key in keys:
            try:
                dct = dct[key]
            except (KeyError, TypeError):
                return None
        return dct

    @classmethod
    def find_key_path(cls, dictionary, target_key, current_path=None):
        if current_path is None:
            current_path = []

        if isinstance(dictionary, dict):
            for key, value in dictionary.items():
                if key == target_key:
                    current_path.append(key)
                    return current_path
                elif isinstance(value, (dict, list)):
                    found_path = cls.find_key_path(
                        value, target_key, current_path + [key])
                    if found_path:
                        return found_path
        elif isinstance(dictionary, list):
            for index, item in enumerate(dictionary):
                found_path = cls.find_key_path(
                    item, target_key, current_path + [index])
                if found_path:
                    return found_path

        return None

    @classmethod
    def find_key_paths(cls, dictionary, target_keys, current_path=None):
        if current_path is None:
            current_path = []

        paths = []

        if isinstance(dictionary, dict):
            for key, value in dictionary.items():
                if target_keys == key:
                    paths.append(current_path + [key])
                if isinstance(value, (dict, list)):
                    found_paths = cls.find_key_paths(
                        value, target_keys, current_path + [key])
                    paths.extend(found_paths)
        elif isinstance(dictionary, list):
            for index, item in enumerate(dictionary):
                found_paths = cls.find_key_paths(
                    item, target_keys, current_path + [index])
                paths.extend(found_paths)

        return paths

    @classmethod
    def get_nested_value(cls, data, keys):
        return cls.get_nested_value(data[keys[0]], keys[1:]) if keys else data

    @classmethod
    def mapping_data(cls, data: dict, mapping_fields: dict, remove_fields: list = None, convert_int: list = []):
        """
        Mapping collected data to stored data format

        Input:
            - data (dict): dota collected
            - mapping_fields (dict): key-value pairs
               + key: field name of data after mapping
               + value (list): list keys as a path to direct to target value
            - remove_fields (list): list of fields need to be removed
            - convert_int (list): list of fields need to be converted to int
        """
        mapped_data = dict()
        # mapped_data.update(data)

        for key, value in mapping_fields.items():
            try:
                if isinstance(value, str):
                    mapped_data[key] = data.get(value)
                elif isinstance(value, list):
                    mapped_data[key] = cls.get_nested_value(data, value)
            except Exception as e:
                print(e)
                mapped_data[key] = None
                continue
        #     if key in convert_int and isinstance(mapped_data[key], str) and mapped_data[key].isdigit():
        #         mapped_data[key] = int(mapped_data[key])
        # if remove_fields:
        #     [mapped_data.pop(key) for key in remove_fields if mapping_fields.get(key)]
        return mapped_data

    @staticmethod
    def convert_timestamp_to_datetime(timestamp: int, format: str = '%Y-%m-%d %H:%M:%S') -> str:
        """
        Convert timestamp to datetime string
        """
        return datetime.fromtimestamp(timestamp).strftime(format)

    @staticmethod
    def convert_view_count(view_count: str) -> int:
        """ Convert view count from string (K,M,B,T) to int """
        view_char_dict = {'K': 1000, 'M': 1000000,
                          'B': 1000000000, 'T': 1000000000000}
        if view_count[-1] in view_char_dict:
            return int(float(view_count[:-1]) * view_char_dict[view_count[-1]])

        if view_count.isdigit():
            return int(view_count)
        return 0
    
    @staticmethod
    def check_file_exist(file_name, result_dir = 'result_crawl', file_type = 'json'):
        result_dir = Path(result_dir)
        # if file not exist return file path else append _{index} to file path
        file_name_path = result_dir / file_name
        i = 0
        while file_name_path.exists():
            file_name = file_name.split('.')[0] + f'{i}.{file_type}'
            file_name_path = result_dir / file_name
            i += 1
            
        return file_name_path
