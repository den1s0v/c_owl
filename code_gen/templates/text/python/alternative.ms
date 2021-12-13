{{#branches}}
    {{#if}}
{{#pad}}{{/pad}}{{#partial}}btn_play{{/partial}}if{{#partial}}btn_stop{{/partial}} {{#use}}cond{{/use}}:  {{#comment}}{{name}}{{/comment}}
{{#pad}}{{/pad}} {{#partial}}btn_play{{/partial}}
{{#use}}body as stmt_list{{/use}}{{#pad}}
{{/pad}} {{#partial}}btn_stop{{/partial}}
    {{/if}}
    {{#else-if}}
{{#pad}}{{/pad}}elif {{#use}}cond{{/use}}
{{#pad}}{{/pad}} {{#partial}}btn_play{{/partial}}
{{#use}}body as stmt_list{{/use}}{{#pad}}
{{/pad}} {{#partial}}btn_stop{{/partial}}
    {{/else-if}}
    {{#else}}
{{#pad}}{{/pad}}else
{{#pad}}{{/pad}} {{#partial}}btn_play{{/partial}}
{{#use}}body as stmt_list{{/use}}{{#pad}}
{{/pad}} {{#partial}}btn_stop{{/partial}} {{/else}}{{/branches}}