<div class="code-line">
{{#pad}}{{/pad}}{{#partial}}btn_play{{/partial}}{{#kw}}while{{/kw}}{{#partial}}btn_stop{{/partial}} ({{#use}}cond{{/use}})  {{#comment}}{{ name }}{{> value_hint }}{{/comment}}
</div>
<div class="code-line">
{{#pad}}{{/pad}}{<!-- while-body begin -->{{#use}}body/sequence as btn_play{{/use}}{{! << use context of body to give btn_play access to body's variables }}
</div>
{{#use}}body/sequence/body as stmt_list{{/use}}
<div class="code-line">
{{#pad}}{{/pad}}}<!-- while-body end -->{{#use}}body/sequence as btn_stop{{/use}}
</div>
