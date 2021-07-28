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


b = {"age": index}

merge_dict_lists({'name': 'lei'}, b)
print(b)
