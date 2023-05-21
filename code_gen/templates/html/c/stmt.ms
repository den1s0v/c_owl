<div class="code-line">
{{#pad}}{{/pad}}<!-- 
{{! no func: }} -->{{^has_func_call}}{{#partial}}btn_play{{/partial}}{{#partial}}span | {class: variable, content: '{{name}}'}{{/partial}};
{{/has_func_call}}<!-- 
{{! func call: }} -->{{#has_func_call}}{{#prefix_part_of_action}}{{#partial}}btn_play{{/partial}}{{/prefix_part_of_action}}{{>wrapped_func_call}};
{{/has_func_call}}
</div>
