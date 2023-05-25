<div class="code-line">
{{#pad}}{{/pad}}{{#kw}}{{return_type}}{{/kw}} {{#partial}}span | {class: variable, content: '{{name}}'}{{/partial}} ({{#param_list}}{{ param }}{{^last}}, {{/last}}{{/param_list}})
</div>
<div class="code-line">
{{#pad}}{{/pad}}{
</div>
{{#use}}body/sequence/body as stmt_list{{/use}}
<div class="code-line">
{{#pad}}{{/pad}}}
</div>
<br>
