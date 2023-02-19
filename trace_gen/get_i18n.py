# get_i18n.py

import os



# use i18n library:
# https://github.com/danhper/python-i18n
# https://pypi.org/project/python-i18n/
import i18n

LOCALE_RELATIVE_PATH = 'locales'


# relative to current .py file location
localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), LOCALE_RELATIVE_PATH)



i18n.load_path.append(localedir)
i18n.get('available_locales').insert(0, 'ru')  # ?? do I need to add it manually?

i18n.set('locale', 'ru')
# i18n.set('fallback', 'en')  # 'en' seems to be the default
i18n.set('error_on_missing_translation', True)  # False by default
i18n.set('error_on_missing_placeholder', True)  # False by default

# cache translations in memory!
i18n.set('enable_memoization', True)  # False by default


def set_locale(locale_code='en'):
	i18n.set('locale', locale_code)

def get_translations(_namespace, _key, _default=None, **kwargs) -> dict:
	tr_d = {}
	for loc in i18n.get('available_locales'):
		try:
			tr_d[loc] = i18n.t(f'{_namespace}.{_key}', locale=loc, **kwargs).strip()
		except KeyError:
			print(f'[WARN] no translation/no keys for "action.{_key}".format({dict(**kwargs)})')
			tr_d[loc] = _default
	return tr_d


#### Getters for specific namespaces ####

def action(key, **kwargs):
	return get_translations('action', key, _default='<%s>' % key, **kwargs)


if __name__ == '__main__':
	# print(localedir)
	# print(i18n.get('available_locales'))
	print(action('program'))
	print(action('if', cond_name='C4', extra='1'))
