// paper-canvas.js

var canvas = null;
var P = 4;
OUTER = 'outer'
INNER = 'inner'
var COLOR = {};
COLOR[OUTER] = '#ffeeee';
COLOR[INNER] = '#ffdddd';
var COLOR2 = {};
COLOR2[OUTER] = '#eeeeff';
COLOR2[INNER] = '#ddddff';
var COLOR3 = {};
COLOR3[OUTER] = '#eeffee';
COLOR3[INNER] = '#ddffdd';

// Both PaperScript and JavaScript have access to the Window scope, therefore you can use window.globals<code> from the JavaScript and <code>globals<code> from PaperScript to pass information back and forth.
globals = {};

function relative_coords(docX, docY) {
	var bb = canvas.getBoundingClientRect()
	return [docX - bb.left, docY - bb.top]
}

function segment_frac(point1, point2, frac) {
	var bb = canvas.getBoundingClientRect()
	return [
		point1.x + (point2.x - point1.x) * frac,
		point1.y + (point2.y - point1.y) * frac,
	];
}

function span_bbox(span) {
    bb = span.getBoundingClientRect()
    var rectangle = new Rectangle(
    	new Point(relative_coords(bb.left-P, bb.top-P)),
    	new Point(relative_coords(bb.right+P, bb.bottom+P))
	);
    return rectangle;
}
function draw_around(rectangle, inner_color, outer_color) {
    var path = new Path.Rectangle(rectangle, 5);
    // Give the stroke a color
    path.fillColor = inner_color || COLOR2[INNER];
    path.strokeColor = outer_color || COLOR[OUTER];
    path.strokeWidth = 5;
    // Set the shadow color of the circle to RGB black:
    path.shadowColor = "gray";

    return rectangle;
}

function draw_shape(type, config) {
	// if (["arrow"].includes(type)) {
	// 	path = new Path(config);
	// 	path.strokeColor = 'red';
	// 	// path.dashArray = [10, 10];
	// 	return
	// }
	if ("path" === type) {
		// config.strokeColor = 'red';
		config.strokeColor = config.strokeColor || 'lightgrey';
		if (config.fillColor === true)
			config.fillColor = 'lightgrey';
		// config.strokeCap = 'butt';
		config.strokeCap = config.strokeCap || 'square';
		path = new Path(config);
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
		var text = new PointText(config);
		return;
	}

	var path = null;
	if (["WhileLoopArea", "AlternativeArea"].includes(type)) {
		// return
		// path = new Path.Rectangle(new Rectangle(config));
		// path.strokeColor = 'black';
		// path.dashArray = [10, 10];
	}
	else if (type === "SequenceArea") {
		return
		// path = new Path.Rectangle(new Rectangle(config));
		// path.strokeColor = 'black';
		// path.dashArray = [10, 10];
	}
	else if (type === "BoxArea") {
		path = new Path.Rectangle(new Rectangle(config), 5);
		path.fillColor = 'grey';
	}
	else if (type === "Slot") {
		path = new Path.Circle(config, 2);
		path.strokeColor = 'black';
		path.fillColor = 'yellow';
	}
	else if ("ConditionDiamond" === type) {
		config = new Rectangle(config)
		path = new Path();
		path.add(config.topCenter);
		path.add(config.rightCenter);
		path.add(config.bottomCenter);
		path.add(config.leftCenter);
		path.closePath()
		path.fillColor = 'grey';
	}
	else if ("TransitDiamond" === type) {
		path = new Path.Rectangle(config.rectangle);
		// config = new Rectangle(config)
		// path = new Path();
		// path.add(config.topCenter);
		// path.add(config.rightCenter);
		// path.add(config.bottomCenter);
		// path.add(config.leftCenter);
		// path.closePath()
		if (config.hidden) {
			path.fillColor = config.color || 'lightgrey';
		} else {
			path.fillColor = 'white';
			path.strokeColor = 'grey';
		}
		// if (config.color)
		// 	path.fillColor = config.color;

	}
	else {
		console.log("Do not draw: " + type);
	}
}
globals.draw_shape = draw_shape

function main() {
    // console.log("main() started")

    // Get a reference to the canvas object
    canvas = document.getElementById('myCanvas');
    // Create an empty project and a view for the canvas:
    // setup(canvas);

    // algorithm_element_id="36"
    var span1 = $("span[algorithm_element_id='33']").parent()[0];
    var rect1 = span_bbox(span1);
    var span2 = $("span[algorithm_element_id='29']").parent()[0];
    var rect2 = span_bbox(span2);
 //    bb = span.getBoundingClientRect()

 	var h = Math.max(10, (rect1.top - rect2.bottom) / 2);
 	// console.log(h)
 	var up = new Point(0, -h);
 	var down = new Point(0, h);
 	// var right = new Point(h, 0);

    var path = new Path();
    // path.strokeColor = COLOR[OUTER];
    // path.fillColor = COLOR[OUTER];

    // Create the gradient, passing it an array of colors to be converted
    // to evenly distributed color stops:
    var gradient = new Gradient([COLOR3[OUTER], COLOR[OUTER]]);

    // Have the gradient color run between the topLeft and
    // bottomRight points we defined earlier:
    var gradientColor = new Color(gradient, rect2.bottomCenter, rect1.topCenter);

    // Set the fill color of the path to the gradient color:
    path.fillColor = gradientColor;
    path.strokeColor = gradientColor;

    path.strokeWidth = 0*P;
    var startskew = rect2.width * 0.3;
    var endw = Math.min(5, rect1.width * 0.1);
    // path.dashArray = [20, 4];
    path.add(new Segment(rect2.bottomRight + [-P,-0], null, down + [-startskew, 0]));

    path.add(new Segment(rect1.center.add([endw, 0]),       up.add([0, 0])));
    path.add(new Segment(rect1.center.add([-endw, 0]), null, up.add([-0, 0])));

    path.add(new Segment(rect2.bottomLeft.add([P,-0]),        down.add([startskew, 0])));
    path.closePath();

    draw_around(rect1, COLOR[INNER], COLOR[OUTER]);
    draw_around(rect2, COLOR3[INNER], COLOR3[OUTER]);

 //    var rectangle = new Rectangle(
 //    	new Point(
 //    		...relative_coords(bb.left-P, bb.top-P)),
 //    	new Point(
 //    		...relative_coords(bb.right+P, bb.bottom+P)),
	// );
 //    var path = new Path.Rectangle(rectangle, 5);
 //    // Give the stroke a color
 //    path.strokeColor = '#ff557799';
 //    path.strokeWidth = 4;
 //    // path.dashArray = [10, 4];

    // http://paperjs.org/tutorials/geometry/point-size-and-rectangle/

    // // var rect = new Rectangle(new Point(bb.left, bb.top), new Point(bb.right, bb.bottom));
    // path.lineTo(new Point(...relative_coords(bb.left, bb.top)));
    // path.lineTo(new Point(...relative_coords(bb.right, bb.top)));
    // path.lineTo(new Point(...relative_coords(bb.right, bb.bottom)));
    // path.lineTo(new Point(...relative_coords(bb.left, bb.bottom)));
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

console.log("main() is starting ...")
main();
console.log("main() completed.")
