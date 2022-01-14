<div class="code-line">
{{#pad}}{{/pad}}{{#partial}}btn_play{{/partial}}{{#kw}}while{{/kw}}{{#partial}}btn_stop{{/partial}} ({{#use}}cond{{/use}})  {{#comment}}{{ name }}{{/comment}}
</div>
{{#pad}}{{/pad}}{ {{#use}}body/sequence/body as btn_play{{/use}}{{! << use context of body to give btn_play access to body's variables }}
{{#use}}body/sequence/body as stmt_list{{/use}}
<div class="code-line">
{{#pad}}{{/pad}}} {{#use}}body/sequence/body as btn_stop{{/use}}
</div>
