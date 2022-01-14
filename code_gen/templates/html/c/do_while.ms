<div class="code-line">
{{#pad}}{{/pad}}{{#partial}}btn_play{{/partial}}{{#kw}}do{{/kw}}{{#partial}}btn_stop{{/partial}}  {{#comment}}{{ name }}{{/comment}}
</div>
{{#pad}}{{/pad}}{ {{#use}}body/sequence/body as btn_play{{/use}}
{{#use}}body/sequence/body as stmt_list{{/use}}
<div class="code-line">
{{#pad}}{{/pad}}} {{#use}}body/sequence/body as btn_stop{{/use}}
</div>
<div class="code-line">
{{#pad}}{{/pad}}{{#kw}}while{{/kw}} ({{#use}}cond{{/use}});
</div>
