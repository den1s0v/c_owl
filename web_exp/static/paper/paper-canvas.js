// paper-canvas.js

let canvas = null;
let P = 4;
// OUTER = 'outer'
// INNER = 'inner'
// let COLOR = {};
// COLOR[OUTER] = '#ffeeee';
// COLOR[INNER] = '#ffdddd';
// let COLOR2 = {};
// COLOR2[OUTER] = '#eeeeff';
// COLOR2[INNER] = '#ddddff';
// let COLOR3 = {};
// COLOR3[OUTER] = '#eeffee';
// COLOR3[INNER] = '#ddffdd';

// Both PaperScript and JavaScript have access to the Window scope, therefore you can use window.globals<code> from the JavaScript and <code>globals<code> from PaperScript to pass information back and forth.
window.globals = {};

function relative_coords(docX, docY) {
	let bb = canvas.getBoundingClientRect()
	return [docX - bb.left, docY - bb.top]
}

function segment_frac(point1, point2, frac) {
	let bb = canvas.getBoundingClientRect()
	return [
		point1.x + (point2.x - point1.x) * frac,
		point1.y + (point2.y - point1.y) * frac,
	];
}

function span_bbox(span) {
    let bb = span.getBoundingClientRect()
    let rectangle = new paper.Rectangle(
    	new paper.Point(relative_coords(bb.left-P, bb.top-P)),
    	new paper.Point(relative_coords(bb.right+P, bb.bottom+P))
	);
    return rectangle;
}
function draw_around(rectangle, inner_color, outer_color) {
    let path = new paper.Path.Rectangle(rectangle, 5);
    // Give the stroke a color
    path.fillColor = inner_color || COLOR2[INNER];
    path.strokeColor = outer_color || COLOR[OUTER];
    path.strokeWidth = 5;
    // Set the shadow color of the circle to RGB black:
    path.shadowColor = "gray";

    return rectangle;
}

function PathDiamond(rect) {
	let path = new paper.Path();
	path.add(rect.topCenter);
	path.add(rect.rightCenter);
	path.add(rect.bottomCenter);
	path.add(rect.leftCenter);
	path.closePath()
	return path;
}

let COL_LINE = "#77f";
let COL_BOX_BORDER = "#333";
let BOX_BORDER_WIDTH = 3;
let COL_BOX_FILL = "white";
let COL_BLOCK_BORDER = '#0006';

let COL_LINE_HIGHLIGHT = '#55ff77';
let COL_BOX_HIGHLIGHT = '#ccccff';

function draw_shape(type, config) {
	// if (["arrow"].includes(type)) {
	// 	path = new paper.Path(config);
	// 	path.strokeColor = 'red';
	// 	// path.dashArray = [10, 10];
	// 	return
	// }
	if ("path" === type) {
		// config.strokeColor = 'red';
		config.strokeColor = config.strokeColor || COL_LINE;
		if (config.fillColor === true)
			config.fillColor = COL_LINE;
		// config.strokeCap = 'butt';
		config.strokeCap = config.strokeCap || 'square';

		if (config.highlighted) {
			config[config.highlight_field] = COL_LINE_HIGHLIGHT;
			/// experiment:
			config.strokeWidth *= 1.15;
		}
		let path = new paper.Path(config);
		// path.strokeColor = 'red';
		// path.dashArray = [10, 10];
		// path.smooth();

		///
		if (config.flex) {
			// path.bringToFront()  // не помогает, т.к. объекты создаются и позже
			// path.reverse()
			path.tweenTo(
			    // { dashOffset: 50 },
			    { dashOffset: -20 },
			    2000
			).then(function() {
			    // ...tween color back to blue.
			    path.tweenTo({ dashOffset: 0 }, 2000)
				.then(function() {
				    // ...set solid line.
				    path.dashArray = [10, 0]
			})});
		}
		/// </>
		return;
	}
	if ("text" === type) {
		let text;
		if (config.outline_offset) {
			// draw several times with offset to mimic text outline
			let config_clone = Object.assign({}, config);
			config_clone.fillColor = config.shadowColor || "white";
			let d = config.outline_offset;
			let shift = new paper.Point(d, 0);

			for (let angle = 0; angle < 360; angle += 90) {
				config_clone.point = config.point + shift.rotate(angle);
				text = new paper.PointText(config_clone);
			}
		}
		// draw the text
		text = new paper.PointText(config);
		return;
	}
	if ("circle" === type) {
		let path = new paper.Path.Circle(config);
		return;
	}

	let path = null;
	if (["DoLoopArea", "WhileLoopArea", "AlternativeArea"].includes(type)) {
		path = new paper.Path.Rectangle(new paper.Rectangle(config.rectangle));
		path.strokeColor = COL_BLOCK_BORDER;
		path.dashArray = [10, 10];
	}
	else if (type === "SequenceArea") {
		if (config.highlighted) {
			path = new paper.Path.Rectangle(new paper.Rectangle(config.rectangle));
			path.strokeColor = COL_BLOCK_BORDER;
			path.dashArray = [3, 3];
		}
	}
	else if (type === "BoxArea") {
		path = new paper.Path.Rectangle(new paper.Rectangle(config.rectangle));
		path.strokeColor = COL_BOX_BORDER;
		path.strokeWidth = BOX_BORDER_WIDTH;
		path.fillColor = config.highlighted ? COL_BOX_HIGHLIGHT : COL_BOX_FILL;
	}
	else if (type === "Slot") {
		path = new paper.Path.Circle(config, 2);
		path.strokeColor = 'black';
		path.fillColor = 'yellow';
	}
	else if ("ConditionDiamond" === type) {
		path = PathDiamond(new paper.Rectangle(config.rectangle));
		path.strokeColor = COL_BOX_BORDER;
		path.strokeWidth = BOX_BORDER_WIDTH;
		path.fillColor = config.highlighted ? COL_BOX_HIGHLIGHT : COL_BOX_FILL;
	}
	else if ("TransitDiamond" === type) {
		// path = new paper.Path.Rectangle(config.rectangle);
		if (config.hidden) {
			path = PathDiamond(config.rectangle);
			if (config.visible !== undefined) {
				path.visible = config.visible;
			}
			path.fillColor = config.highlighted ? COL_LINE_HIGHLIGHT : config.color || COL_LINE;
			// path.strokeColor = 'grey'; ///
		} else {
			path = new paper.Path.Rectangle(config.rectangle);
			path.fillColor = config.highlighted ? COL_LINE_HIGHLIGHT : 'white';
			path.strokeColor = COL_LINE;
		}
		// if (config.color)
		// 	path.fillColor = config.color;

	}
	else {
		console.log("Do not draw: " + type);
	}
}
window.globals.draw_shape = draw_shape

function paper_init(canvas_id) {
    // console.log("main() started")

    // Get a reference to the canvas object
    canvas = document.getElementById(canvas_id);

	// Create an empty project and a view for the canvas:
	paper.setup(canvas);

	window.globals.project = paper.project;
	console.debug("paper_init() finished.");
}
window.globals.paper_init = paper_init;


function main() {
    // Create an empty project and a view for the canvas:
    // setup(canvas);
    // algorithm_element_id="36"
    let span1 = $("span[algorithm_element_id='33']").parent()[0];
    let rect1 = span_bbox(span1);
    let span2 = $("span[algorithm_element_id='29']").parent()[0];
    let rect2 = span_bbox(span2);
 //    bb = span.getBoundingClientRect()

 	let h = Math.max(10, (rect1.top - rect2.bottom) / 2);
 	// console.log(h)
 	let up = new paper.Point(0, -h);
 	let down = new paper.Point(0, h);
 	// let right = new paper.Point(h, 0);

    let path = new paper.Path();
    // path.strokeColor = COLOR[OUTER];
    // path.fillColor = COLOR[OUTER];

    // Create the gradient, passing it an array of colors to be converted
    // to evenly distributed color stops:
    let gradient = new paper.Gradient([COLOR3[OUTER], COLOR[OUTER]]);

    // Have the gradient color run between the topLeft and
    // bottomRight points we defined earlier:
    let gradientColor = new paper.Color(gradient, rect2.bottomCenter, rect1.topCenter);

    // Set the fill color of the path to the gradient color:
    path.fillColor = gradientColor;
    path.strokeColor = gradientColor;

    path.strokeWidth = 0*P;
    let startskew = rect2.width * 0.3;
    let endw = Math.min(5, rect1.width * 0.1);
    // path.dashArray = [20, 4];
    path.add(new paper.Segment(rect2.bottomRight + [-P,-0], null, down + [-startskew, 0]));

    path.add(new paper.Segment(rect1.center.add([endw, 0]),       up.add([0, 0])));
    path.add(new paper.Segment(rect1.center.add([-endw, 0]), null, up.add([-0, 0])));

    path.add(new paper.Segment(rect2.bottomLeft.add([P,-0]),        down.add([startskew, 0])));
    path.closePath();

    draw_around(rect1, COLOR[INNER], COLOR[OUTER]);
    draw_around(rect2, COLOR3[INNER], COLOR3[OUTER]);

 //    let rectangle = new paper.Rectangle(
 //    	new paper.Point(
 //    		...relative_coords(bb.left-P, bb.top-P)),
 //    	new paper.Point(
 //    		...relative_coords(bb.right+P, bb.bottom+P)),
	// );
 //    let path = new paper.Path.Rectangle(rectangle, 5);
 //    // Give the stroke a color
 //    path.strokeColor = '#ff557799';
 //    path.strokeWidth = 4;
 //    // path.dashArray = [10, 4];

    // http://paperjs.org/tutorials/geometry/point-size-and-rectangle/

    // // let rect = new paper.Rectangle(new paper.Point(bb.left, bb.top), new paper.Point(bb.right, bb.bottom));
    // path.lineTo(new paper.Point(...relative_coords(bb.left, bb.top)));
    // path.lineTo(new paper.Point(...relative_coords(bb.right, bb.top)));
    // path.lineTo(new paper.Point(...relative_coords(bb.right, bb.bottom)));
    // path.lineTo(new paper.Point(...relative_coords(bb.left, bb.bottom)));
    // path.closePath();

    // Draw the view now:
    // view.draw();
}


/*
function VisualNode(args)
{};
VisualNode.prototype.__init__ = function(self, args) {
	for (p in args) {
		// if (args.hasOwnProperty(p))
		self[p] = args[p];
	}
	self.connectors = [];
};

function Shape(center, bbox)
{};
Shape.prototype.__proto__ = VisualNode.prototype;
Shape.prototype.__init__ = function(self, center, bbox) {
	Shape.prototype.__proto__.__init__(self, {center: center})
	self.bbox = bbox;
};

function Diamond(center, bbox)
{
	// console.log(this)
	// console.log(this.constructor)
	this.constructor.prototype.__init__(this, center, bbox);
};
Diamond.prototype.__proto__ = Shape.prototype;
Diamond.prototype.__init__ = function(self, center, bbox) {
	Diamond.prototype.__proto__.__init__(self, center, bbox)
	self.connectors = [0, 90, 180, 270];
};
// Diamond.prototype.method_name = function(first_argument) {
// 	// body...
// };

function Box(center, bbox)
{
	this.constructor.prototype.__init__(this, center, bbox);
};
Diamond.prototype.__proto__ = Shape.prototype;
Diamond.prototype.__init__ = function(self, center, bbox) {
	Diamond.prototype.__proto__.__init__(self, center, bbox)
	self.connectors = [0, 90, 180, 270];
};



d = new Diamond([12,15], [0,0, 100,100])
console.log(d)
*/

// console.log("paper is ready ...")
// console.log("main() is starting ...")
// main();
// console.log("main() completed.")

// window.globals.paper_on_load();
