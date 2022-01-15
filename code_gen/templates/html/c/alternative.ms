<div class="code-line">
{{#pad}}{{/pad}}{{#partial}}btn_play{{/partial}}{{#kw}}if{{/kw}}{{#partial}}btn_stop{{/partial}} {{! move initial buttons out of branch so they use correct name }}

{{#branches}}
    {{#if}}
({{#use}}cond{{/use}})  {{#comment}}{{name}}{{/comment}}
</div>
<div class="code-line">
{{#pad}}{{/pad}}{<!-- -->{{#partial}}btn_play{{/partial}}
</div>

{{#use}}body as stmt_list{{/use}}

<div class="code-line">
{{#pad}}{{/pad}}}{{#partial}}btn_stop{{/partial}}
</div>
    {{/if}}
    {{#else-if}}
<div class="code-line">
{{#pad}}{{/pad}}{{#kw}}else if{{/kw}} ({{#use}}cond{{/use}})
</div>
<div class="code-line">
{{#pad}}{{/pad}}{<!-- -->{{#partial}}btn_play{{/partial}}
</div>

{{#use}}body as stmt_list{{/use}}

<div class="code-line">
{{#pad}}{{/pad}}}{{#partial}}btn_stop{{/partial}}
</div>
    {{/else-if}}
    {{#else}}
<div class="code-line">
{{#pad}}{{/pad}}{{#kw}}else{{/kw}}
</div>
<div class="code-line">
{{#pad}}{{/pad}}{<!-- -->{{#partial}}btn_play{{/partial}}
</div>

{{#use}}body as stmt_list{{/use}}
 
<div class="code-line">
{{#pad}}{{/pad}}}{{#partial}}btn_stop{{/partial}}
 </div>

	{{/else}}{{/branches}}

