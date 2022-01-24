<div class="code-line">
{{#pad}}{{/pad}}{{#partial}}btn_play{{/partial}}{{#kw}}for{{/kw}}{{#partial}}btn_stop{{/partial}} ({{#use}}
init as stmt_inline{{/use}}; {{#use}}
cond{{/use}}; {{#use}}
update as stmt_inline{{/use}})  {{#comment}}{{ name }}{{/comment}}
</div>
<div class="code-line">
{{#pad}}{{/pad}}{<!-- loop-body begin -->{{#use}}body/sequence as btn_play{{/use}}{{! << use context of body to give btn_play access to body's variables }}
</div>
{{#use}}body/sequence/body as stmt_list{{/use}}
<div class="code-line">
{{#pad}}{{/pad}}}<!-- loop-body end -->{{#use}}body/sequence as btn_stop{{/use}}
</div>
