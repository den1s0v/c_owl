<style type="text/css" media="screen">
	.comp-ph-question-text, div.code-line {
	  font-family: courier; font-size: 10pt;
	}
    span.string { color: #555; font-style: italic }
    span.atom { color: #f08; font-style: italic; font-weight: bold; }
	span.comment { color: #262; font-style: italic; line-height: 1em; }
	span.meta { color: #555; font-style: italic; line-height: 1em; }
	span.variable { color: #700; text-decoration: underline; }
	span.variable-2 { color: #b11; }
	span.struct { color: #07c; font-weight: bold; }
	span.number { color: #f00; font-weight: bold; font-style: normal; }
	span.program { color: #f70; font-weight: bold; }
	span.function { color: #707; font-weight: bold; }
	span.action { color: #077; font-weight: bold; }
	span.qualifier { color: #555; }
	span.keyword { color: #00a; font-weight: bold; }
	span.builtin { color: #30a; }
	span.link { color: #762; }
	span.value { color: #0aa; font-weight: bold; font-style: normal; }
	span.plain { color: #000; font-weight: normal; font-style: normal; }

	span.warning { background-color: #ff9; }
	span.error { background-color: #fdd; }
	span.button { background-color: #add; }

	i.small.icon
	{
		width: 14px;
		height: 13px;
		display: inline-block; /*not supported by IE7<*/
		background-repeat: no-repeat;
	}
	i.small.icon:hover {
		/* background:#53ea93; */
		box-shadow: inset 0 0 0 1px #53ea93;
	}
	i.play.icon
	{
		background: url(https://icons.bootstrap-4.ru/assets/icons/play-fill.svg) top left no-repeat;
	}
	i.stop.icon
	{
		background: url(https://icons.bootstrap-4.ru/assets/icons/stop-fill.svg) top left no-repeat;
	}
	
	span.left-border { /* https://stackoverflow.com/a/16363465/12824563 */
		position: relative;
	}
	span.left-border:after {
		content: '';
		display: block;
		position: absolute;
			top: -2; left: 1;  /* shift position by pixels */
		width: 1px;
		height: 130%;  /* make longer in height */
		background: #e0e0e0;
	}
</style>