<!-- <div>
{{#comment}}algorithm{{/comment}}
{{#algorithm}}
    {{^functions}}
{{#comment}}No functions defined.{{/comment}}
    {{/functions}}
</div> -->
{{#question_prompt}}
<div class="code-line">
{{!#comment}}
{{question_prompt}}
{{!/comment}}
</div> <br>
{{/question_prompt}}

    {{#global_code}}
{{!#use} }sequence/sequence{{/use}}
{{#use}}sequence/body as stmt_list{{/use}}
    {{/global_code}}
<div class="code-line">
<!-- {{#comment}}End of code.{{/comment}}{{/algorithm}} -->
{{^algorithm}}
{{#comment}}Nothing here.{{/comment}}
{{/algorithm}}
</div>

{{!#partial} }span | {class: atom, content: 'end-of-alg'}{{/partial}}

{{> css }}
