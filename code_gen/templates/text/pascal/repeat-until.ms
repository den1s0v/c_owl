{{#pad}}{{/pad}}{{#partial}}btn_play{{/partial}}repeat{{#partial}}btn_stop{{/partial}}  {{#comment}}{{ name }}{{/comment}}
{{#pad}}{{/pad}}begin {{#partial}}btn_play{{/partial}}
{{#use}}body/sequence/body as stmt_list{{/use}}
{{#pad}}{{/pad}}end {{#partial}}btn_stop{{/partial}}
until {{#use}}cond{{/use}};{{!

   repeat
   begin
      writeln('value of a: ', a);
      a := a + 1;
   end
   until a = 20;
}}