{{#comment}}algorithm{{/comment}}
{{#algorithm}}
    {{^functions}}
{{#comment}}No functions defined.{{/comment}}
    {{/functions}}

    {{#global_code}}
{{!#use} }sequence/sequence{{/use}}
{{#use}}sequence/body as stmt_list{{/use}}
    {{/global_code}}
{{#comment}}End of code.{{/comment}}{{/algorithm}}
{{^algorithm}}
{{#comment}}Nothing here.{{/comment}}
{{/algorithm}}
