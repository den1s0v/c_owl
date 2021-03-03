// init_blockly.js

// Палитра Blockly
function get_toolbox_json() {
	return {
	"kind": "categoryToolbox",
	"contents": [
	  {
		"kind": "category",
		// "expanded": "true",  // does not work anyway (why?)
		"name": Blockly.Msg["CUSTOM_CATEGORY_ALTERNATIVES"],
		"contents": [
		  {
		    "kind": "label",
		    "text": Blockly.Msg["CUSTOM_LABEL_CONDITION_FOR_IF"]
		  },
		  {"kind": "sep", "gap": "8"},
  		  {
			"kind": "block",
			"type": "condition_with_values_block"
		  },
		  {
		    "kind": "label",
		    "text": Blockly.Msg["CUSTOM_LABEL_IF_CONFIGURABLE"]
		  },
		  {"kind": "sep", "gap": "8"},
		  {
			"kind": "block",
			"blockxml": `<block type="controls_named_if">
				<value name="NAME">
				  <shadow type="text_name_of_alternative"></shadow>
				</value>
			</block>`
		  },
		]
	  },
	  {
		"kind": "category",
		"name": Blockly.Msg["CUSTOM_CATEGORY_LOOPS"],
		"contents": [
		  {
		    "kind": "label",
		    "text": Blockly.Msg["CUSTOM_LABEL_CONDITION_FOR_LOOP"]
		  },
		  {"kind": "sep", "gap": "8"},
		  {
			"kind": "block",
			"blockxml": `<block type="condition_with_values_block">
		    	<field name="VALUES">1,1,(0)</field>
		    </block>`
		  },
		  {
		    "kind": "label",
		    "text": Blockly.Msg["CUSTOM_LABEL_LOOP_PRECOND"]
		  },
		  {"kind": "sep", "gap": "8"},
		  {
			"kind": "block",
			"blockxml": `<block type="controls_named_whileUntil">
				<value name="NAME">
				  <shadow type="text_name_of_loop"></shadow>
				</value>
			</block>`
		  },
		  {
		    "kind": "label",
		    "text": Blockly.Msg["CUSTOM_LABEL_LOOP_POSTCOND"]
		  },
		  {"kind": "sep", "gap": "8"},
		  {
			"kind": "block",
			"blockxml": `<block type="controls_named_doWhileUntil">
				<value name="NAME">
				  <shadow type="text_name_of_loop"></shadow>
				</value>
			</block>`
		  }
		]
	  },
	  {
		"kind": "category",
		"name": Blockly.Msg["CUSTOM_CATEGORY_ACTIONS"],
		"contents": [
		  {
		    "kind": "label",
		    "text": Blockly.Msg["CUSTOM_LABEL_ACTIONS"]
		  },
		  {"kind": "sep", "gap": "8"},
		  {
		    "kind": "label",
		    "text": Blockly.Msg["CUSTOM_LABEL_UNIQUE"]
		  },
		  {
			"kind": "block",
			"type": "action"
		  },
		  {
			"kind": "block",
			"blockxml": `<block type="text_print">
				<value name="TEXT">
				  <shadow type="text">
					<field name="TEXT">Wow</field>
				  </shadow>
				</value>
			</block>`
		  },
		]
	  }
	]
  };
}

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
		.appendField(new Blockly.FieldTextInput("%s".replace("%s", Blockly.Msg["CUSTOM_CONDITION_PROMPT"])), "COND_NAME")
		.appendField(Blockly.Msg["CUSTOM_YIELDS_VALUES"])  // "принимает значения"
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
		.replace('циклически', Blockly.Msg["CUSTOM_REPEATEDLY"])
		.replace('принимает значения', Blockly.Msg["CUSTOM_YIELDS_VALUES"]);
	}
	if (initial) {
	  initial = "последовательно принимает значения %1"
		.replace('%1', rstrip(initial, ","))
		.replace('последовательно', Blockly.Msg["CUSTOM_SEQUENTIALLY"])
		.replace('принимает значения', Blockly.Msg["CUSTOM_YIELDS_VALUES"]);
	}
	let sep = ''
	if (repeating && initial)
	  sep = ", %1 ".replace("%1", Blockly.Msg["CUSTOM_AND_THEN"]);  // "а затем"
	const values_tip = initial + sep + repeating;

	return Blockly.Msg["CUSTOM_CONDITION_WITH_VALUES_BLOCK_TOOLTIP"]  // 'Логическое условие с именем "%1". В ходе выполнения программы оно %2.'
	  .replace('%1', thisBlock.getFieldValue('COND_NAME'))
	  .replace('%2', values_tip);
	});
	
	this.setHelpUrl("");
  }
  };
  

  Blockly.defineBlocksWithJsonArray([
  {
	// Block for text value (modified)
	"type": "text_name_of_alternative",
	"message0": "%1",
	"args0": [{
	  "type": "field_input",
	  "name": "TEXT",
	  "text": "%{BKY_CUSTOM_NAME_OF_ALTERNATIVE_PROMPT}"
	}],
	"output": "String",
	"style": "text_blocks",
	"helpUrl": "%{BKY_TEXT_TEXT_HELPURL}",
	"tooltip": "%{BKY_CUSTOM_NAME_OF_ALTERNATIVE}",
	"extensions": [
	  "text_quotes",
	]
  },
  {
	// Block for text value (modified)
	"type": "text_name_of_loop",
	"message0": "%1",
	"args0": [{
	  "type": "field_input",
	  "name": "TEXT",
	  "text": "%{BKY_CUSTOM_NAME_OF_LOOP_PROMPT}"
	}],
	"output": "String",
	"style": "text_blocks",
	"helpUrl": "%{BKY_TEXT_TEXT_HELPURL}",
	"tooltip": "%{BKY_CUSTOM_NAME_OF_LOOP}",
	"extensions": [
	  "text_quotes",
	]
  },
  {
	// Block for if/elseif/else condition (modified to be named).
	"type": "controls_named_if",
	"message0": "// %{BKY_CUSTOM_NAME_OF_ALTERNATIVE}: %1",  // имя развилки
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
	"message0": "// %{BKY_CUSTOM_NAME_OF_LOOP}: %1",
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
		"align": "RIGHT",	
		// Hide the Dropdown control
		// "type": "field_dropdown",
		// "name": "MODE",
		// "options": [
		//   ["%{BKY_CONTROLS_WHILEUNTIL_OPERATOR_WHILE}", "WHILE"],
		//   ["%{BKY_CONTROLS_WHILEUNTIL_OPERATOR_UNTIL}", "UNTIL"]
		// ],
		"type": "field_label",
		"name": "MODE",
		"text": "%{BKY_CONTROLS_WHILEUNTIL_OPERATOR_WHILE}",
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
	"tooltip": "%{BKY_CONTROLS_WHILEUNTIL_TOOLTIP_WHILE}"
  },
  {
	// Block for 'postconditional do while/until' loop (modified to be named).
	"type": "controls_named_doWhileUntil",
	"message0": "// %{BKY_CUSTOM_NAME_OF_LOOP}: %1",
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
		"align": "RIGHT",
		// Hide the Dropdown control
		// "type": "field_dropdown",
		// "name": "MODE",
		// "options": [
		//   ["%{BKY_CONTROLS_WHILEUNTIL_OPERATOR_WHILE}", "WHILE"],
		//   ["%{BKY_CONTROLS_WHILEUNTIL_OPERATOR_UNTIL}", "UNTIL"]
		// ],
		"type": "field_label",
		"name": "MODE",
		"text": "%{BKY_CONTROLS_WHILEUNTIL_OPERATOR_WHILE}",
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
	"tooltip": "%{BKY_CUSTOM_DOWHILEUNTIL_TOOLTIP_WHILE}"
  },
  // Block for text value (modified)
  {
	"type": "action",
	"message0": "%1",
	"args0": [{
	  "type": "field_input",
	  "name": "NAME",
	  "text": "%{BKY_CUSTOM_ACTION_PROMPT}"  // "введите имя действия здесь"
	}],
	"previousStatement": null,
	"nextStatement": null,
	"style": "text_blocks",
	"helpUrl": "",
	"tooltip": "%{BKY_CUSTOM_ACTION_TOOLTIP}"  // "Выполняет произвольное действие"
  },

  ]);

}


function setup_blockly_workspace(workspace) {
  // workspace.addChangeListener(Blockly.Events.disableOrphans);
}

function which_language() {
	const ru = (Blockly.Msg["ADD_COMMENT"] === "Добавить комментарий");
	return ru? "ru" : "en";
}

function patch_localization() {
  // find out what lang is ON
  const en = (Blockly.Msg["ADD_COMMENT"] === "Add Comment");
  const ru = (Blockly.Msg["ADD_COMMENT"] === "Добавить комментарий");
  if (!en && !ru) {
	console.log("Warning: Blockly's i10n patch: unknown language used, defaulting to English.");
  }

  Blockly.Msg["CUSTOM_ACTION"] = (
	ru?
	  "выполнить"
	: "run"
	);
  Blockly.Msg["CUSTOM_ACTION_PROMPT"] = (
	ru?
	  "введите имя действия здесь"
	: "enter the name of an action here"
	);
  Blockly.Msg["CUSTOM_ACTION_TOOLTIP"] = (
	ru?
	  "Выполняет произвольное действие"
	: "Do the arbitrary action"
	);
  Blockly.Msg["CUSTOM_AND_THEN"] = (
	ru?
	  "а затем"
	: "and then"
	);
  Blockly.Msg["CUSTOM_CATEGORY_ACTIONS"] = (
	ru?
	  "Действия"
	: "Actions"
	);
  Blockly.Msg["CUSTOM_CATEGORY_ALTERNATIVES"] = (
	ru?
	  "Развилки"
	: "Alternatives"
	);
  Blockly.Msg["CUSTOM_CATEGORY_LOOPS"] = (
	ru?
	  "Циклы"
	: "Loops"
	);
  
  Blockly.Msg["CUSTOM_LABEL_ACTIONS"] = (
  	ru?
  	  "Действия подставляются как есть."
  	: "Actions are inserted as is."
  	);
  Blockly.Msg["CUSTOM_LABEL_CONDITION_FOR_IF"] = (
  	ru?
  	  "Условие для развилки:"
  	: "Condition for an alternative:"
  	);
  Blockly.Msg["CUSTOM_LABEL_CONDITION_FOR_LOOP"] = (
  	ru?
  	  "Условие для цикла:"
  	: "Condition for a loop:"
  	);
  Blockly.Msg["CUSTOM_LABEL_IF_CONFIGURABLE"] = (
  	ru?
  	  "Настраиваемая развилка:"
  	: "Configurable alternative:"
  	);
  Blockly.Msg["CUSTOM_LABEL_LOOP_PRECOND"] = (
  	ru?
  	  "Цикл с предусловием:"
  	: "Pre-conditional loop:"
  	);
  Blockly.Msg["CUSTOM_LABEL_LOOP_POSTCOND"] = (
  	ru?
  	  "Цикл с постусловием:"
  	: "Post-conditional loop:"
  	);
  Blockly.Msg["CUSTOM_LABEL_UNIQUE"] = (
  	ru?
  	  "Имена действий должны быть уникальными."
  	: "Each statement must have a unique name."
  	);

  // Blockly.Msg["CUSTOM_CONDITION"] = (
  //   ru?
  //     "условие"
  //   : "condition"
  //   );
  Blockly.Msg["CUSTOM_CONDITION_PROMPT"] = (
	ru?
	  "введите условие здесь"
	: "enter the condition here"
	);
  Blockly.Msg["CUSTOM_NAME_OF_ALTERNATIVE"] = (
	ru?
	  "имя развилки"
	: "name of the alternative"
	);
  Blockly.Msg["CUSTOM_NAME_OF_ALTERNATIVE_PROMPT"] = (
	ru?
	  "введите имя развилки здесь"
	: "enter the name of the alternative here"
	);
  Blockly.Msg["CUSTOM_NAME_OF_LOOP"] = (
	ru?
	  "имя цикла"
	: "name of the loop"
	);
  Blockly.Msg["CUSTOM_NAME_OF_LOOP_PROMPT"] = (
	ru?
	  "введите имя цикла здесь"
	: "enter the name of the loop here"
	);
  
  Blockly.Msg["CUSTOM_CONDITION_WITH_VALUES_BLOCK_TOOLTIP"] = (
	ru?
	  'Логическое условие с именем "%1". В ходе выполнения программы оно %2.'
	: 'A boolean condition named "%1". During the program execution it %2.'
	);
  Blockly.Msg["CUSTOM_DOWHILEUNTIL_TOOLTIP_UNTIL"] = (
	ru?
	  "Выполняет команды и, пока значение ложно, повторяет их."
	: "Do some statements and repeat them while a value is false."
	);
  Blockly.Msg["CUSTOM_DOWHILEUNTIL_TOOLTIP_WHILE"] = (
	ru?
	  "Выполняет команды и, пока значение истинно, повторяет их."
	: "Do some statements and repeat them while a value is true."
	);
  Blockly.Msg["CUSTOM_REPEATEDLY"] = (
	ru?
	  "циклически"
	: "repeatedly"
	);
  Blockly.Msg["CUSTOM_SEQUENTIALLY"] = (
	ru?
	  "последовательно"
	: "sequentially"
	);
  Blockly.Msg["CUSTOM_YIELDS_VALUES"] = (
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
