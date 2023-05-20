<div class="code-line">
{{#pad}}{{/pad}}{{#kw}}{{return_type}}{{/kw}} {{#partial}}span | {class: variable, content: '{{name}}'}{{/partial}} ({{#param_list}}{{ param }}{{^last}}, {{/last}}{{/param_list}})
</div>
<div class="code-line">
{{#pad}}{{/pad}}{<!-- func-body begin -->{{#use}}body/sequence as btn_play{{/use}}{{! << use context of body to give btn_play access to body's variables }}
</div>
{{#use}}body/sequence/body as stmt_list{{/use}}
<div class="code-line">
{{#pad}}{{/pad}}}<!-- func-body end -->{{#use}}body/sequence as btn_stop{{/use}}
</div>
<br>
