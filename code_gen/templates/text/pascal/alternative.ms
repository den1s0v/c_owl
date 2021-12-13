{{#branches}}
    {{#if}}
{{#pad}}{{/pad}}{{#partial}}btn_play{{/partial}}if{{#partial}}btn_stop{{/partial}} {{#use}}cond{{/use}} then  {{#comment}}{{name}}{{/comment}}
{{#pad}}{{/pad}}begin {{#partial}}btn_play{{/partial}}
{{#use}}body as stmt_list{{/use}}{{#pad}}
{{/pad}}end{{#last}};{{/last}} {{#partial}}btn_stop{{/partial
    }}{{/if
    }}{{#else-if}}
{{#pad}}{{/pad}}else if ({{#use}}cond{{/use}})
{{#pad}}{{/pad}}begin {{#partial}}btn_play{{/partial}}
{{#use}}body as stmt_list{{/use}}{{#pad}}
{{/pad}}end{{#last}};{{/last}} {{#partial}}btn_stop{{/partial
    }}{{/else-if
    }}{{#else}}
{{#pad}}{{/pad}}else
{{#pad}}{{/pad}}begin {{#partial}}btn_play{{/partial}}
{{#use}}body as stmt_list{{/use}}{{#pad}}
{{/pad}}end;{{#partial}}btn_stop{{/partial}} {{/else}}{{/branches}}