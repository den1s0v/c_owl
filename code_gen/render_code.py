# render_code.py

import copy  # to make a copy of data dict to safe original data untouched
import os, os.path
import sys   # measure stack size
from itertools import count


from chevron import render as chevron_render
from chevron.renderer import _html_escape  # use for monkey-patch to fix issue of double-escaping via double-rendering of variables
import fs
import yaml


_dir_path = os.path.dirname(os.path.realpath(__file__)) # dir of current .py file


if __name__ == '__main__' or True:  # to import from upper directory
    import sys
    sys.path.insert(1, os.path.join(_dir_path, '../'))

from trace_gen.get_i18n import action
from trace_gen.txt2algntr import find_by_keyval_in, find_by_predicate


LOCALES_BY_DEFAULT = ('ru', 'en', )  # what to use for quick-fix of "act_name" key absence

TEMPLATES_PATH = os.path.join(_dir_path, 'templates')

TEMPLATE_EXT = '.ms'.casefold()
CONFIG_FILE_NAME = 'config.yml'.casefold()

FIX_DOUBLE_ESCAPING_ISSUE = True  # see below; here is place to turn hacks OFF
USE_HTML_ESCAPING = False

BUTTON_TIP_FREFIX = {
    "ru": {
        'performed': 'Выполнится',
        'started': 'Начнётся',
        'finished': 'Закончится',
    },
    "en": {
        'performed': 'Perform',
        'started': 'Start',
        'finished': 'Finish',
    }
}

# padding step
PADDING = {
    'text': (' ' * 4),
    # 'html': ('&nbsp;' * 4),  # just four spaces
    'html': '<span class="left-border">%s</span>' % ('&nbsp;' * 4),  # four spaces with light line at left side (making vertical rulers)
}

_LOG_RENDERING = False
_DEBUG_RENDERING = False



###################################################
#######                                     #######
####### Render code with Mustache templates #######
#######                                     #######
###################################################

if FIX_DOUBLE_ESCAPING_ISSUE:
    # redefine function called by render() internally from chevron module ...
    def _html_escape_noop(string):
        """do nothing to preserve formatting
            when multiple render of the same fragment occurs
            within chevron.render() function
        """
        return string

    chevron_render_original = chevron_render
    # patch namespace of external function so it calls our function internally
    chevron_render_original.__globals__['_html_escape'] = _html_escape_noop

    if USE_HTML_ESCAPING:  # is performed by chevron by default
        def chevron_render_wrapper(*args, **kwargs):
            'call muted functionality once at the end'
            rendered = chevron_render_original(*args, **kwargs)
            rendered = _html_escape(rendered)  # call original function from chevron.renderer ONCE
            return rendered

        # patch namespace of external function so it calls our function internally
        chevron_render_original.__globals__['render'] = chevron_render_wrapper

        # replace function with wrapper to loook nice for client code
        chevron_render = chevron_render_wrapper



def render_code(alg_dict, locale='ru', **kwargs):
    keyed_alg_data = transform_alg_dict_for_mustache(alg_dict, locale)
    if not 'debug':
        return 'debug....\n\n' + json.dumps(keyed_alg_data, indent=1, ensure_ascii=False)
    return run_rendering(keyed_alg_data, locale=locale, **kwargs)



def run_rendering(keyed_alg_data, text_mode='html', lang='c', show_buttons=True, locale='ru', raise_on_error=False, quiet=False):
    common_options = dict(
        text_mode=text_mode,  # 'html', 'text',
        lang=lang,  # 'c',  # 'python'  'pascal'
        buttons_mode='with_buttons' if show_buttons else 'no_buttons',
        locale=locale,
        stack_size_limit=200,
    )
    # PAD = '`___'
    PAD = PADDING[common_options['text_mode']]

    sw = StackWatcher(common_options['stack_size_limit'], ('<ERROR(1)!>', '<ERROR(2)!>', ''), raise_exception=raise_on_error)

    def get_partial_path(partial_name):
        ### print('partial:', partial_name)
        return partial_name.strip()
    #     return '%s/%s' % (common_options['lang'], partial_name.strip())

    def render_partial(text, render):
        if sw.is_invalid():
            print("Error rendering text:")
            print()
            print(text)
            print()
            return sw.get_warning()
        if '|' in text:
            text, data = text.split('|', maxsplit=1)
            data = render(data)
            data = yaml.load(data, Loader=yaml.FullLoader)
        else:
            data = {}
        ###
        if _LOG_RENDERING: print('Partial:', text)
        transformed = '{{> %s }}' % get_partial_path(text)
        r = render(transformed, data)
        if _DEBUG_RENDERING: print('\t%%', text, '->', transformed, '->', r)
        return r
        ## yaml.load(" { comment: ['abcd', xyz], a: b}", Loader=yaml.FullLoader)

    def use_field_with_partial(text, render):
        """ text := 'field_name'
            text := 'field_name as partial_name'
            text := 'fieldA/fieldB as partial_name'
        """
        if sw.is_invalid():
            print("Error rendering text:")
            print()
            print(text)
            print()
            return sw.get_warning()
        text = text.strip()
        parts = text.split()
        if len(parts) == 0:
            return ''
        field_name = parts[0]
        ###
        if _LOG_RENDERING: print('Use:\t', field_name)
        fields = field_name.split('/')
        if len(parts) >= 3:
            partial_name = parts[2]
        else:
            partial_name = fields[-1]  # last subpart or whole
        partial_name = get_partial_path(partial_name)
        transformed = '{{>%s}}' % partial_name
        for field in reversed(fields):
            transformed = '{{#%s}}%s{{/%s}}' % (field, transformed, field)
        r = render(transformed)
        if _DEBUG_RENDERING: print('\t%%', text, '->', transformed, '->', r)
        return r

    def comment(text, render):
        r = render(text)
        r = render('{{>%s}}' % get_partial_path('comment'), {'comment': r})
        ### print('comment:', r)
        return r

    def pad(text, render):
        try:
            depth = int(render('{{depth}}'))
        except ValueError:
            depth = 0
        text = text.strip()
        if text and text.startswith(('+', '-')):
            try:
                inc = int(text)
                depth += inc
            except ValueError: print(text)
        r = PAD * depth
        return r

    target_lang = '%s/%s' % (common_options['text_mode'], common_options['lang'])
    partials_dict = get_templates_for_language(target_lang, TEMPLATES_PATH)

    patch_path = '%s/%s' % (common_options['text_mode'], common_options['buttons_mode'])
    patch = get_templates_for_language(patch_path, TEMPLATES_PATH)
    partials_dict.update(patch)

    ## print([*partials_dict])

    args = {
        'template': '{{> algorithm }}',
        # template': '{{> root }}!',
        # 'template': '{{> java/sequence }}!',
        'data': {
            # "data": data, #['stmts']['body'],
            **(keyed_alg_data),
            # **(keyed_alg_data['sequence']),
            'partial': render_partial,
            'use': use_field_with_partial,
            'pad': pad,
            'comment': comment,
            'kw': lambda text, render: render("{{#partial}}span | {class: keyword, content: '%s'}{{/partial}}" % text)
            #### 'render': chevron_render,
        },
        'partials_dict': partials_dict,
    }

    try:
        if not quiet: print("Start rendering ...")
        rendered = chevron_render(**args, warn=True)
        if not quiet: print("... rendering complete.")
        return rendered
        # if 0 or common_options['text_mode'] == 'text':
        #     print(rendered)
        # elif common_options['text_mode'] == 'html':
        #     display(HTML(rendered))
        #     # with open(r'c:\D\Work\YDev\CompPr\c_owl\code_gen\templates\html\test.html', 'w') as f:
        #     #     f.write(rendered)
    except Exception as e:
        print(type(e).__name__, ':', e)
        if raise_on_error:
            raise e
        msg = "Exception while rendering code: %s : " % type(e).__name__ + str(e)
        return msg






#####################################################
#######                                       #######
####### Transform algorithm_dict for Mustache #######
#######                                       #######
#####################################################

if 1:
    # constants

    if_branches = ["if", "else-if", "else"]

    siblings_list = [
        "stmt return sequence alternative while_loop do_while_loop for_loop foreach_loop".split(),   # add new action classes here
        if_branches,
        #### ["sequence"],  #  moved above to other regular statements
        ['expr', 'cond_values_hint', 'func_call'],
        ['algorithm', 'functions'],
        ['func'],
        ['func_call'],
    ]
    siblings = {s: siblings for siblings in siblings_list for s in siblings}
    renamings = {k: [('name', 'branch_name')] for k in if_branches}

    def escape_name_yaml(s):
        '''  # https://riptutorial.com/yaml/example/25838/escaping-characters
        Unicode Escapes
        a. space: "\u0020"
        b. single quote: "\u0027"
        c. double quote: "\u0022"
        '''
        s = s or ''  # recover from None
        # s = s.replace("'", r"\u0027")
        # s = s.replace('"', r"\u0022")
        s = s.replace("'", r"&#39;")
        s = s.replace('"', r"&#34;")
        return s


    def transform_alg_dict_for_mustache(raw_data, locale='en'):
        assert locale in LOCALES_BY_DEFAULT, 'Unsupported locale: %s, use one of: %s' % (repr(locale), repr(LOCALES_BY_DEFAULT))
        # # locale = 'ru'
        # locale = 'en'

        def make_act_name(d, force_update=False):
            ''' Using `raw_data` as root to search parent dicts '''
            if 'act_name' in d and not force_update:
                return d['act_name']  # quick no-op
            # simple solution -- just names itself:
            #### return {L: "'%s'" % d["stmt_name"] for L in LOCALES_BY_DEFAULT}
            # full search solution:
            node_type = d["type"]
            assert type(node_type) is str, node_type
            name = escape_name_yaml(d.get('stmt_name') or d.get('name'))
            kwargs = {}
            if 'cond' in d:
                cond = d.get('cond')
                kwargs['cond_name'] = escape_name_yaml(cond.get('stmt_name') or cond.get('name'))
                ### print(node_type)

            if node_type in ('else', ):
                alt = list(find_by_predicate(raw_data,
                    lambda x: (type(x) is dict
                        and ('type' in x)
                        and x['type'] == 'alternative'
                        and ('branches' in x)
                        and (###print(x['branches'], end='\n\n') or
                            d in x['branches']
                            or d['id'] == x['branches'][-1].get('id'))
                        ),
                    find_one=True))
                if alt:
                    alt = alt[0]
                    kwargs['alt_name'] = escape_name_yaml(alt.get('stmt_name') or alt.get('name'))
                else:
                    print('[WARN] Key `alt_name` not found for dict-node `else`')
                    ### print(alt)

            elif node_type.endswith('_loop'):
                node_type = 'loop'
            elif node_type in ('sequence', ):
                loop = list(find_by_keyval_in('body', d, raw_data))
                if loop:
                    loop = loop[0]
                    kwargs['loop_name'] = escape_name_yaml(loop.get('stmt_name') or loop.get('name'))
                    node_type = 'loop-body'

            return action(node_type, name=name, **kwargs)
        # end of make_act_name() definition


        replacings = {"stmt_name": lambda d: {
                          "name": escape_name_yaml(d["stmt_name"]), 'act_name': make_act_name(d)},
                      "name": lambda d: {"name": escape_name_yaml(d["name"]), 'act_name': make_act_name(d)},
                      "act_name": lambda d: {"act_name": escape_name_yaml(d["act_name"][locale]) if type(d["act_name"]) is dict else d["act_name"]},
                      "type": lambda d: ({
                                'act_type-play': 'performed',
                                'phase-label-play': BUTTON_TIP_FREFIX[locale]['performed'],
                                ## 'phase-label-stop':  False,
                          } if d["type"] in ('expr', 'stmt', 'return', 'break', 'continue') else {
                                'act_type-play': 'started',
                                #### 'act_type-stop': 'finished',  # always constant
                                'phase-label-play':  BUTTON_TIP_FREFIX[locale]['started'],
                                'phase-label-stop': BUTTON_TIP_FREFIX[locale]['finished'],
                          })
                      }

        def inject_first_last(d, i, length):
            if type(d) is dict:
                d['first'] = (i == 0)
                d['last'] = (i == length-1)
            return d


        def type2key(d: dict, depth=-1):   # -1 is because top sequence adds 1 indent
            if isinstance(d, dict):
                if 'type' in d:
                    t = d['type']
                    for rk in replacings:
                        if rk in list(d):
                            d.update(replacings[rk](d))

                    # indent = 1 if ('body' in d and t != 'sequence') else 0
                    indent = 1 if ('body' in d and (
                        d['type'] == 'func' or
                        type(d['body']) is list and d['body'][0].get('type') != 'sequence') # do not fall too deep in a loop body
                    ) else 0
                    inner_d = {k: type2key(v, depth=depth+indent) for k, v in d.items() if k != 'type'}
                    if t in renamings:
                        # replace entries
                        for from_, to in renamings[t]:
                            if from_ in inner_d:
                                inner_d[to] = inner_d[from_]
                                del inner_d[from_]

                    inner_d['depth'] = depth
                    if t in siblings:
                        # set all absent fields to False (to avoid in-template recursion)
                        defauts = {k: False for k in siblings[t]}
                        defauts.update({t: inner_d})
                        d = defauts
                    else:
                        print("'%s'"%t, 'not in siblings')
                        d = {t: inner_d}
                    # d = [d]
                    # return {d['type']: {k: type2key(v) for k, v in d.items() if k != 'type'}}
                ### else: print('Warning: dict with unknown keys', [*d.keys()])
                return d
            if isinstance(d, list):
                return [
                    type2key(
                        inject_first_last(el, i, len(d)),
                        depth=depth+0)
                    for i, el in enumerate(d)
                ]
                # return [{'item': type2key(el)} for el in d]
            return d

        if isinstance(raw_data, list):
            raw_data = raw_data[0]

        if 'algorithm' in raw_data:
            raw_data = raw_data['algorithm']

        data = copy.deepcopy(raw_data)
        if 'entry_point' in data:
            del data['entry_point']


        question_prompt = False
        if 'inclide_question_prompt':
            question_prompt = action("question-prompt")[locale]
        data['question_prompt'] = question_prompt


        d = type2key(data)  # ['stmts']['body']
        keyed_data = d if type(d) is dict else d[0]
        return keyed_data






##################################
#######                    #######
####### Read .ms templates #######
#######                    #######
##################################

if 1:
    def read_yml(file_path):
        with open(file_path) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        return data


    def read_config_dependencies(config_file):
        data = read_yml(config_file)
        ### print(config_file, '- YML:', data)
        if isinstance(data, dict):
            return data.get('depends_on') or ()
        return ()


    def read_template(file_path):
        with open(file_path) as f:
            data = f.read()
        return data


    def read_templates_from_dir(syspath, templates=None, dependencies=None) -> (dict,list):
        ' -> [in|out] templates: dict , dependencies: list'
        templates = templates or {}
        dependencies = dependencies or []
        dirs_here = []
        for fd in os.scandir(syspath):
            if fd.is_file:
                if fd.name.casefold() == CONFIG_FILE_NAME:
                    full_path = fs.path.combine(syspath, fd.name)
                    new_deps = read_config_dependencies(full_path)
                    dependencies[:0] = new_deps  # insert to the beginning
                else:
                    name, ext = fs.path.splitext(fd.name)
                    if ext.casefold() == TEMPLATE_EXT:
                        if name not in templates:
                            templates[name] = read_template(fs.path.combine(syspath, fd.name))
        return templates, dependencies



    def get_templates_for_language(target_lang_path: str, templates_path=TEMPLATES_PATH, verbose=False) -> dict:
        templates = {}
        dependencies = []

        for subpath in fs.path.recursepath(target_lang_path, reverse=True):
            full_dir_path = fs.path.combine(templates_path, subpath)
            if not os.path.exists(full_dir_path):
                continue
            if verbose:
                print('Looking for templates in ', subpath)
            templates, dependencies = read_templates_from_dir(full_dir_path, templates, dependencies)

            # follow dependencies
            dirs_here = [fd.name for fd in os.scandir(full_dir_path) if fd.is_dir]
            for name in dependencies[:]:
                if name in dirs_here:
                    dependencies.remove(name)
                    # recurse into sibling dir
                    templates, dependencies = read_templates_from_dir(
                        fs.path.combine(full_dir_path, name),
                        templates, dependencies
                    )

        if dependencies:
            print("Did not found the following dependencies:")
            print(*dependencies, sep=', ')

        return templates


        # templates_path = r'c:\D\Work\YDev\CompPr\c_owl\code_gen\templates'
        # # target_lang = 'text/java'
        # # target_lang = 'text/cpp'
        # target_lang = 'text/python'
        # templates = get_templates_for_language(target_lang, templates_path)
        # [*templates], templates.get('comment')






###############################################
#######                                 #######
####### Detect infinite recursion tools #######
#######                                 #######
###############################################

if 1:
    # import sys
    # from itertools import count

    def stack_size4b(size_hint=8):
        """Get stack size for caller's frame.
        """
        get_frame = sys._getframe
        frame = None
        try:
            while True:
                frame = get_frame(size_hint)
                size_hint *= 2
        except ValueError:
            if frame:
                size_hint //= 2
            else:
                while not frame:
                    size_hint = max(2, size_hint // 2)
                    try:
                        frame = get_frame(size_hint)
                    except ValueError:
                        continue

        for size in count(size_hint):
            frame = frame.f_back
            if not frame:
                return size


    class StackWatcher():
        def __init__(self, max_depth=500, warnings=('Recursion is too deep'), raise_exception=False):
            self.max_depth = max_depth
            self.warnings = tuple(warnings)
            self.warn_i = -1
            self.raise_exception = bool(raise_exception)
        def is_invalid(self):
            D = stack_size4b()
            if D > self.max_depth:
                self.warn_i += 1  # min(self.warn_i + 1, len(self.warnings))
                if self.warn_i == 0:  # show once only
                    print(f"Recursion depth ({D}) exceeded user's limit ({self.max_depth}).")
                return True
            return False
        def get_warning(self):
            i = self.warn_i
            if i >= len(self.warnings):
                if self.raise_exception:
                    raise RecursionError(f"Recursion depth exceeded user's limit ({self.max_depth}).")
                i = len(self.warnings) - 1
            return self.warnings[i] if i >= 0 else ''





##############################
#######                #######
####### Debugging code #######
#######                #######
##############################

def _render_json_2_html_batch(dir_src=r'c:\Temp2\cntrflowoutput_v4_json', dest_dir=r'c:\Temp2\cntrflowoutput_v4_html', ext_pattern='*.json'):
    'convert all .json files in DIR_SRC to *.html into DEST_DIR'
    from glob import glob
    import json
    import os.path

    for i, fp in enumerate(glob(os.path.join(dir_src, ext_pattern))):
        print(f'[{i+1}]\t', fp, end='\t')

        with open(fp) as f:
            alg_json = json.load(f)

        out = os.path.splitext(
            os.path.join(
                dest_dir,
                os.path.split(fp)[1])
            )[0] + '.html'

        rendered = render_code(alg_json,
            text_mode='html',
            show_buttons=True,
            raise_on_error=True,
            quiet=True)
        with open(out, 'w') as f:
            f.write(rendered)

        print('OK')



if __name__ == '__main__':
    if 0:
        # _render_json_2_html_batch(dir_src=r'c:/Temp2/cntrflowoutput_v6_fg_json', dest_dir=r'c:/Temp2/cntrflowoutput_v6_fg_html')
        _render_json_2_html_batch(dir_src=r'c:\Temp2\manual_json', dest_dir=r'c:\Temp2\manual_html')
        exit(0)

    # import sys
    # sys.path.insert(1, '../')

    # templates = get_templates_for_language('html/c')
    # print([*templates], templates.get('comment'))
    # # exit()


    import json

    # alg_json_file = r'c:/Temp2/cntrflowoutput_v6_json/ijk_av_tree_insert__17603408635188800781__1643030101.json'
    # alg_json_file = r'c:/Temp2/manual_json/while_110.json'
    # alg_json_file = r'nk_style_from_table.json'
    # alg_json_file = r'c:/Temp2/cntrflowoutput_v7_json/cJSON_GetArraySize.json'
    # alg_json_file = r'../trace_gen/alg_dbg.json'
    alg_json_file = r'../test_data/debug/1__fill.json'

    with open(alg_json_file, encoding='utf8' or '1251') as f:
        data = json.load(f)
    if isinstance(data, list):
        data = data[0]

    # out_locale = 'ru'
    out_locale = 'en'
    rendered = render_code(data, text_mode='html', locale=out_locale, show_buttons=True, raise_on_error=True)
    with open(r'test-%s.html' % out_locale, 'w') as f:
        f.write(rendered)

    print("saved debug file.")
