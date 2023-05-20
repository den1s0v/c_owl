{{#algorithm}}
{{#question_prompt}}
<div class="code-line">
{{!#comment}}
{{question_prompt}}
{{!/comment}}
</div> <br>
{{/question_prompt}}

<!-- <div>
{{#comment}}algorithm{{/comment}}
    {{^functions}}
{{#comment}}No functions defined.{{/comment}}
    {{/functions}}
</div> -->

{{#use}}functions/func as func{{/use}}

    {{#global_code}}
{{!#use} }sequence/sequence{{/use}}
{{#use}}sequence/body as stmt_list{{/use}}
    {{/global_code}}
<div class="code-line">
<!-- {{#comment}}End of code.{{/comment}} -->
{{/algorithm}}
{{^algorithm}}
{{#comment}}Nothing here.{{/comment}}
{{/algorithm}}
</div>

{{!#partial} }span | {class: atom, content: 'end-of-alg'}{{/partial}}

{{> css }}
