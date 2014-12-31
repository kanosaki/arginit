
import sys
import inspect
import itertools
import argparse
import re

PAT_PARAM_HELP = re.compile("(\w+) -- (.+)")


class InitMethodReader(object):
    def __init__(self, fn):
        # fn should be function (not method)
        assert fn.__name__ == '__init__'
        self.fn = fn
        self.sig = inspect.signature(fn)

    def params(self):
        all_params = self.sig.parameters.values()
        return list(itertools.islice(all_params, 1, None))  # remove 'self'

    def pos_args(self):
        return [
            p
            for p in self.params()
            if p.kind == p.POSITIONAL_OR_KEYWORD and
            p.default == p.empty]

    def opt_args(self):
        return [
            p
            for p in self.params()
            if p.kind == p.POSITIONAL_OR_KEYWORD and
            p.default != p.empty]

    def _parse_param_docs(self):
        docstring = self.fn.__doc__
        scanner = PAT_PARAM_HELP.scanner(docstring)
        for match in iter(scanner.search, None):
            yield (match.group(1), match.group(2))

    def param_docs(self):
        return dict(self._parse_param_docs())


class ArgparseByType(object):
    def __init__(self, ttype):
        self.target = ttype
        self.init_reader = InitMethodReader(ttype.__init__)

    def description(self):
        return self.doc_firstline()

    def register_argumetns(self, ap):
        reader = self.init_reader
        helps = reader.param_docs()
        for pa in reader.pos_args():
            ap.add_argument(
                pa.name,
                metavar=pa.name,
                help=helps.get(pa.name)
            )
        for oa in reader.opt_args():
            long_argname = '--{}'.format(oa.name)
            char_argname = '-{}'.format(oa.name[0])
            ap.add_argument(
                char_argname, long_argname,
                default=oa.default,
                help=helps.get(oa.name)
            )

    def create_argparse(self):
        ap = argparse.ArgumentParser(description=self.description())
        self.register_argumetns(ap)
        return ap

    def doc_firstline(self):
        try:
            return self.target.__doc__.split('\n')[0]
        except (IndexError, AttributeError):
            return ""


def create(cls, args=None):
    args = args or sys.argv[1:]
    ap = ArgparseByType(cls).create_argparse()
    namespace = ap.parse_args(args)
    return cls(**namespace.__dict__)
