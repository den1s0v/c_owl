<div class="code-line">
{{#pad}}{{/pad}}{{#partial}}btn_play{{/partial}}{{#kw}}if{{/kw}}{{#partial}}btn_stop{{/partial}} 

{{#branches}}
    {{#if}}
({{#use}}cond{{/use}})  {{#comment}}{{name}}{{/comment}}
</div>
{{#pad}}{{/pad}}{ {{#partial}}btn_play{{/partial}}
{{#use}}body as stmt_list{{/use}}{{#pad}}
{{/pad}}} {{#partial}}btn_stop{{/partial}}
    {{/if}}
    {{#else-if}}
<div class="code-line">
{{#pad}}{{/pad}}{{#kw}}else if{{/kw}} ({{#use}}cond{{/use}})
</div>
{{#pad}}{{/pad}}{ {{#partial}}btn_play{{/partial}}
{{#use}}body as stmt_list{{/use}}{{#pad}}
{{/pad}}} {{#partial}}btn_stop{{/partial}}
    {{/else-if}}
    {{#else}}
<div class="code-line">
{{#pad}}{{/pad}}{{#kw}}else{{/kw}}
</div>
{{#pad}}{{/pad}}{ {{#partial}}btn_play{{/partial}}
{{#use}}body as stmt_list{{/use}}{{#pad}}
{{/pad}}} {{#partial}}btn_stop{{/partial}}
	{{/else}}{{/branches}}