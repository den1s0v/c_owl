<div class="code-line">
{{#pad}}{{/pad}}{{#partial}}btn_play{{/partial}}{{#kw}}return{{/kw}}{{#return_expr}} <!-- {{! no func: }} -->{{^has_func_call}}{{#partial}}span | {class: variable, content: '{{return_expr}}'}{{/partial}}{{/has_func_call}}<!-- {{! func call: }} -->{{#has_func_call}}{{>wrapped_func_call}}{{/has_func_call}}{{/return_expr}};
</div>
