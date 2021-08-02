import os
import sys

add_url_rule = []


def route(rule, **options):
    def decorator(f):
        global add_url_rule
        endpoint = options.pop("endpoint", None)
        add_url_rule.append((rule, endpoint, f))
        return f

    return decorator


@route('/', endpoint='index')
def index():
    print('this is a test')


print(add_url_rule)
print(add_url_rule[0][2]())


def merge_dict_lists(self_dict, app_dict):
    """Merges self_dict into app_dict. Replaces None keys with self.name.
    Values of dict must be lists.
    """
    name = 'dict_test'
    for key, values in self_dict.items():
        key = name if key is None else f"{name}.{key}"
        print('---', values)
        app_dict.setdefault(key, []).extend(values)


# b = {"age": index}
#
# merge_dict_lists({'name': 'lei'}, b)
# print(b)


def fluent(raw_data, result=None):
    if not result:
        result = []
    for data in raw_data:
        if type(data) == list:
            fluent(data, result)
        else:
            if type(data) == dict:
                data['age'] = 12
            result.append(data)
    return result


def _get_package_path(name):
    """Returns the path to a package or cwd if that cannot be found."""
    try:
        return os.path.abspath(os.path.dirname(sys.modules[name].__file__))
    except (KeyError, AttributeError):
        return os.getcwd()


if __name__ == '__main__':
    a = [{'name': 'leichao'}, 1, 4]
    b = fluent(a)
    print(id(a), id(b))
    print(b)
    print(a)
    print(_get_package_path(__name__))