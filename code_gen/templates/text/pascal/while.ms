{{#pad}}{{/pad}}{{#partial}}btn_play{{/partial}}while{{#partial}}btn_stop{{/partial}} {{#use}}cond{{/use}} do  {{#comment}}{{ name }}{{/comment}}
{{#pad}}{{/pad}}begin {{#partial}}btn_play{{/partial}}
{{#use}}body/sequence/body as stmt_list{{/use}}
{{#pad}}{{/pad}}end; {{#partial}}btn_stop{{/partial}}{{!

while number>0 do
begin
   sum := sum + number;
   number := number - 2;
end;
}}