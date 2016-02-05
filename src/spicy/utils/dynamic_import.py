import sys
import traceback
from django.utils.importlib import import_module
from django.core.exceptions import ImproperlyConfigured


def load_module(path, config='SERVICE'):
    module, attr = path.rsplit('.', 1)
    try:
        mod = import_module(module)
        return getattr(mod, attr)

    except ImportError, e:
        sys.stdout.write(traceback.format_exc())
        raise ImproperlyConfigured(
            'Error importing module %s: "%s"' % (module, e))
    except ValueError, e:
        sys.stdout.write(traceback.format_exc())
        raise ImproperlyConfigured(
            'Error importing module. Is %s a correctly defined list or tuple?'
            % config)


__all__ = 'load_module',
