// activity-vis.js


function redraw_activity_diagram(algorithm_json, options) {
	let entry_point = algorithm_json["entry_point"];
	let alg = create_alg_for(entry_point);


	alg.rebase(new paper.Point(80, 100));

	console.debug(" About to clear the canvas ...")
	if (globals.project) {
		globals.project.clear()
	}
	else
		console.debug("Nothing to clear ..?")

	alg.draw();

}
