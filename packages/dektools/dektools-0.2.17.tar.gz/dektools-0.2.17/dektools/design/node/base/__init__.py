import re
from ....dict import assign_list, assign
from ...base import TypeBase, TypesBase
from ....yaml import yaml


class NodeBase(TypeBase):
    _cls_suffix = 'Node'

    def __init__(self, manager, res):
        self.manager = manager
        self.res = res

    def make(self, args, params, attrs):
        raise NotImplementedError()

    def merge_args(self, a, b, params):
        return assign_list(self.manager.translate_list(a or [], params), b or [])

    def merge_params(self, a, b):
        return assign(self.manager.translate_map(a or {}, b), b)


class MixinTrans:
    assign_marker = '<<'
    re_var = r'\$\$([^\W0-9]\w*)[\^]?'

    def trans_var(self, s, params):
        if s.startswith(self.assign_marker):
            return self._translate_assign(self.trans_var(s[len(self.assign_marker):], params), params)
        return yaml.loads(re.sub(self.re_var, lambda x: str(params[x.group(1)]), s))

    def _translate_assign(self, s, params):
        pass

    def translate_list(self, data, params):
        result = []
        for item in data:
            if isinstance(item, str):
                item = self.trans_var(item, params)
            result.append(item)
        return result

    def translate_map(self, data, params):
        result = {}
        for k, v in data.items():
            if isinstance(v, str) and v:
                v = self.trans_var(v, params)
            if v is not None:
                result[k] = v
        return result


class NodeTypes(TypesBase):
    pass


class NodeManager(MixinTrans):
    types: NodeTypes = None

    def __init__(self, set_manager, res_manager):
        self.set_manager = set_manager
        self.res_manager = res_manager

    def load_path(self, *paths):
        self.res_manager.load_path(*paths)

    def load_path_item(self, path):
        return self.res_manager.load_path_item(path)

    def get_node(self, name):
        res = self.res_manager.find_res(name)
        typed = None
        if isinstance(res, self.res_manager.unknown_res_cls):
            typed = res.name
        elif res is not None:
            typed = res.get_typed()
        if typed is not None:
            node_cls = self.types.get(typed)
            if node_cls is not None:
                return node_cls(self, res)

    def make(self, name, args=None, params=None, attrs=None, init=None, final=None):
        node = self.set_manager.get_node(self, name)
        if init is not None:
            init(node)
        args, params, attrs = args or [], params or {}, attrs or {}
        result = node.make(args, params, attrs)
        if self is not node.manager:
            result = self.set_manager.trans(self, node, result, args, params, attrs)
        if final is not None:
            return final(node, result)
        return result
