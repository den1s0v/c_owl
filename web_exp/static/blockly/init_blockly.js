// init_blockly.js


function init_blockly_environment(argument=null) {
  // set up block types ...
  patch_localization();
  
  // var condition_with_values_block_Json = {
  //   "type": "condition_with_values_block",
  //   "message0": "%1 принимает значения %2",
  //   "args0": [
  //     {
  //       "type": "field_input",
  //       "name": "COND_NAME",
  //       "text": "условие1"
  //     },
  //     {
  //       "type": "field_input",
  //       "name": "VALUES",
  //       "text": "1,(0)"
  //     }
  //   ],
  //   "output": "Boolean",
  //   "colour": 230,
  //   "tooltip": "",
  //   "helpUrl": ""
  // };

  // Blockly.Blocks['condition_with_values_block'] = {
  //   init: function() {
  //     this.jsonInit(condition_with_values_block_Json);
  //     // Assign 'this' to a variable for use in the tooltip closure below.
  //     var thisBlock = this;
      
  //     this.setTooltip(function() {
  //       const values = thisBlock.getFieldValue('VALUES')
  //       let initial = values, repeating = '';
  //       if (values.includes('(')) {
  //         [initial, repeating] = values.split('(');
  //       }
  //       let values_tip = ", которое последовательно принимает значения %1".replace('%1', rstrip(initial, ","))
  //       if (repeating) {
  //         values_tip += ", а затем (циклически) значения %1".replace('%1', repeating.replace(")", ""))
  //       }
  //       return 'Логическое условие с именем "%1"%2.'.replace('%1',
  //         thisBlock.getFieldValue('COND_NAME')).replace('%2', values_tip);
  //     });
  //   }
  // };
  
  
  var TRUTH_ALIASES = ["1","истина","да","true","yes"];
  var FALSE_ALIASES = ["0","ложь", "нет","false","no"];

  
  function clean_condition_values(values_str) {  // => Array<!String>
    let values = [];
    while (values_str) {
      let is_continue = false;
      for (const values_group of [TRUTH_ALIASES, FALSE_ALIASES]) {
        prefix = whichprefix(values_str, values_group)
        if (prefix !== null) {
          values.push(values_group[0])
          values_str = values_str.slice(prefix.length);
          is_continue = true;
          break;
        }
      }
      if (is_continue) continue;
      values_str = values_str.slice(1);
    }
    return values
  }
  
  function condition_values_validator(newValue) {
    newValue = newValue.toLowerCase()
    let initial = newValue, repeating = '';
    i = newValue.indexOf('(')
    if (i >= 0) {
      [initial, repeating] = newValue.split('(');
      repeating = clean_condition_values(repeating).join(",")
      repeating = '(' + repeating + ')'
    }
    initial = clean_condition_values(initial).join(",")
    let sep = ''
    if (repeating && initial)
      sep = ","

    return (initial + sep + repeating) || FALSE_ALIASES[0];  // 0 is default when empty
  };

  
  
  Blockly.Blocks['condition_with_values_block'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldTextInput("%s1".replace("%s", Blockly.Msg["CUSTOMS_CONDITION"])), "COND_NAME")
        .appendField(Blockly.Msg["CUSTOMS_YIELDS_VALUES"])  // "принимает значения"
        .appendField(new Blockly.FieldTextInput("0,1,1,(0)", condition_values_validator), "VALUES");
    this.setOutput(true, "Boolean");
    this.setColour(60);
    
    var thisBlock = this;

    // this.setTooltip("");
    this.setTooltip(function() {
    const values = thisBlock.getFieldValue('VALUES')
    let initial = values, repeating = '';
    if (values.includes('(')) {
      [initial, repeating] = values.split('(');
      repeating = "циклически принимает значения %1"
        .replace('%1', repeating.replace(")", ""))
        .replace('циклически', Blockly.Msg["CUSTOMS_REPEATEDLY"])
        .replace('принимает значения', Blockly.Msg["CUSTOMS_YIELDS_VALUES"]);
    }
    if (initial) {
      initial = "последовательно принимает значения %1"
        .replace('%1', rstrip(initial, ","))
        .replace('последовательно', Blockly.Msg["CUSTOMS_SEQUENTIALLY"])
        .replace('принимает значения', Blockly.Msg["CUSTOMS_YIELDS_VALUES"]);
    }
    let sep = ''
    if (repeating && initial)
      sep = ", а затем ";
    const values_tip = initial + sep + repeating;

    return Blockly.Msg["CUSTOMS_CONDITION_WITH_VALUES_BLOCK_TOOLTIP"]  // 'Логическое условие с именем "%1". В ходе выполнения программы оно %2.'
      .replace('%1', thisBlock.getFieldValue('COND_NAME'))
      .replace('%2', values_tip);
    });
    
    this.setHelpUrl("");
  }
  };
  

  Blockly.defineBlocksWithJsonArray([
  {
    // Block for if/elseif/else condition (modified to be named).
    "type": "controls_named_if",
    "message0": "// %{BKY_CUSTOMS_NAME_OF_ALTERNATIVE}: %1",  // имя развилки
    "args0": [
      {
        "type": "input_value",
        "name": "NAME",
        "check": "String",
        "align": "RIGHT"
      }
    ],
    "message1": "%{BKY_CONTROLS_IF_MSG_IF} %1",
    "args1": [
      {
        "type": "input_value",
        "name": "IF0",
        "check": "Boolean",
        "align": "RIGHT"
      }
    ],
    "message2": "%{BKY_CONTROLS_IF_MSG_THEN} %1",
    "args2": [
      {
        "type": "input_statement",
        "name": "DO0"
      }
    ],
    "previousStatement": null,
    "nextStatement": null,
    "style": "logic_blocks",
    "helpUrl": "%{BKY_CONTROLS_IF_HELPURL}",
    "mutator": "controls_if_mutator",
    "extensions": ["controls_if_tooltip"]
  },
  {
    // Block for 'do while/until' loop (modified to be named).
    "type": "controls_named_whileUntil",
    "message0": "// %{BKY_CUSTOMS_NAME_OF_LOOP}: %1",
    "args0": [
      {
        "type": "input_value",
        "name": "NAME",
        "check": "String",
        "align": "RIGHT"
      }
    ],
    "message1": "%1 %2",
    "args1": [
      {
        "type": "field_dropdown",
        "name": "MODE",
        "options": [
          ["%{BKY_CONTROLS_WHILEUNTIL_OPERATOR_WHILE}", "WHILE"],
          ["%{BKY_CONTROLS_WHILEUNTIL_OPERATOR_UNTIL}", "UNTIL"]
        ],
        "align": "RIGHT"
      },
      {
        "type": "input_value",
        "name": "BOOL",
        "check": "Boolean"
      }
    ],
    "message2": "%{BKY_CONTROLS_REPEAT_INPUT_DO} %1",
    "args2": [{
      "type": "input_statement",
      "name": "DO"
    }],
    "previousStatement": null,
    "nextStatement": null,
    "style": "loop_blocks",
    "helpUrl": "%{BKY_CONTROLS_WHILEUNTIL_HELPURL}",
    "extensions": ["controls_whileUntil_tooltip"]
  },
  {
    // Block for 'postconditional do while/until' loop (modified to be named).
    "type": "controls_named_doWhileUntil",
    "message0": "// %{BKY_CUSTOMS_NAME_OF_LOOP}: %1",
    "args0": [
      {
        "type": "input_value",
        "name": "NAME",
        "check": "String",
        "align": "RIGHT"
      }
    ],
    "message1": "%{BKY_CONTROLS_REPEAT_INPUT_DO} %1",
    "args1": [{
      "type": "input_statement",
      "name": "DO"
    }],
    "message2": "%1 %2",
    "args2": [
      {
        "type": "field_dropdown",
        "name": "MODE",
        "options": [
          ["%{BKY_CONTROLS_WHILEUNTIL_OPERATOR_WHILE}", "WHILE"],
          ["%{BKY_CONTROLS_WHILEUNTIL_OPERATOR_UNTIL}", "UNTIL"]
        ],
        "align": "RIGHT"
      },
      {
        "type": "input_value",
        "name": "BOOL",
        "check": "Boolean"
      }
    ],
    "previousStatement": null,
    "nextStatement": null,
    "style": "loop_blocks",
    "helpUrl": "%{BKY_CONTROLS_WHILEUNTIL_HELPURL}",
    "extensions": ["controls_doWhileUntil_tooltip"]
  },
  // Block for text value (modified)
  {
    "type": "action",
    "message0": "%1",
    "args0": [{
      "type": "field_input",
      "name": "NAME",
      "text": "%{BKY_CUSTOMS_ACTION}"  // "выполнить"
    }],
    "previousStatement": null,
    "nextStatement": null,
    "style": "text_blocks",
    "helpUrl": "",
    "tooltip": "%{BKY_CUSTOMS_ACTION_TOOLTIP}"  // "Выполняет произвольное действие"
  },

  ]);

	/** (Modified!)
	 * Tooltips for the 'controls_whileUntil' block, keyed by MODE value.
	 * @see {Blockly.Extensions#buildTooltipForDropdown}
	 * @package
	 * @readonly
	 */
	Blockly.Constants.Loops.DOWHILE_UNTIL_TOOLTIPS = {
	  'WHILE': '%{BKY_CUSTOMS_DOWHILEUNTIL_TOOLTIP_WHILE}',
	  'UNTIL': '%{BKY_CUSTOMS_DOWHILEUNTIL_TOOLTIP_UNTIL}'
	};

	Blockly.Extensions.register('controls_doWhileUntil_tooltip',
	    Blockly.Extensions.buildTooltipForDropdown(
	        'MODE', Blockly.Constants.Loops.DOWHILE_UNTIL_TOOLTIPS));

}


function setup_blockly_workspace(workspace) {
  // workspace.addChangeListener(Blockly.Events.disableOrphans);
}


function patch_localization() {
  // find out what lang is ON
  const en = (Blockly.Msg["ADD_COMMENT"] === "Add Comment");
  const ru = (Blockly.Msg["ADD_COMMENT"] === "Добавить комментарий");
  if (!en && !ru) {
    console.log("Warning: Blockly's i10n patch: unknown language used, defaulting to English.");
  }

  Blockly.Msg["CUSTOMS_ACTION"] = (
    ru?
      "выполнить"
    : "run"
    );
  Blockly.Msg["CUSTOMS_ACTION_TOOLTIP"] = (
    ru?
      "Выполняет произвольное действие"
    : "Do arbitrary action"
    );
  Blockly.Msg["CUSTOMS_CONDITION"] = (
    ru?
      "условие"
    : "condition"
    );
  Blockly.Msg["CUSTOMS_NAME_OF_ALTERNATIVE"] = (
    ru?
      "имя развилки"
    : "name of alternative"
    );
  Blockly.Msg["CUSTOMS_NAME_OF_LOOP"] = (
    ru?
      "имя цикла"
    : "name of loop"
    );
  Blockly.Msg["CUSTOMS_CONDITION_WITH_VALUES_BLOCK_TOOLTIP"] = (
    ru?
      'Логическое условие с именем "%1". В ходе выполнения программы оно %2.'
    : 'A boolean condition named "%1". During the program execution it %2.'
    );
  Blockly.Msg["CUSTOMS_DOWHILEUNTIL_TOOLTIP_UNTIL"] = (
    ru?
      "Выполняет команды и, пока значение ложно, повторяет их."
    : "Do some statements and repeat them while a value is false."
    );
  Blockly.Msg["CUSTOMS_DOWHILEUNTIL_TOOLTIP_WHILE"] = (
    ru?
      "Выполняет команды и, пока значение истинно, повторяет их."
    : "Do some statements and repeat them while a value is true."
    );
  Blockly.Msg["CUSTOMS_REPEATEDLY"] = (
    ru?
      "циклически"
    : "repeatedly"
    );
  Blockly.Msg["CUSTOMS_SEQUENTIALLY"] = (
    ru?
      "последовательно"
    : "sequentially"
    );
  Blockly.Msg["CUSTOMS_AND_THEN"] = (
    ru?
      "а затем"
    : "and then"
    );
  Blockly.Msg["CUSTOMS_YIELDS_VALUES"] = (
    ru?
      "принимает значения"
    : "yields values"
    );

}



// some utility functions

function rstrip(str, char) {
  while (str.endsWith(char)) {
    str = str.slice(0, -1);
  }
  return str;
}

function whichprefix(str, prefixes) {
  for (const prefix of prefixes) {
    if (str.startsWith(prefix))
      return prefix;
  }
  return null;
}
