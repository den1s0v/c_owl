// activity-vis.js

const highlight_color = '#9fb';


function redraw_activity_diagram(algorithm_json, trace_json, options) {

	clear_global_diagram_arrays();

	let entry_point = algorithm_json["entry_point"];
	let alg = create_alg_for(entry_point);


	alg.rebase(new paper.Point(140, 70));

	// console.debug(" About to clear the canvas ...")
	if (globals.project) {
		globals.project.clear()
	}

	// else
	// 	console.debug("Nothing to clear ..?")

	if (trace_json && trace_json.length >= 2) {
		// const last_act = trace_json.slice(-1)[0];
		let [second_last_act, last_act] = trace_json.slice(-2);
		console.log("second_last_act, last_act:", second_last_act, last_act)
		highlight_or_connect(second_last_act, last_act);

	}


	alg.draw();

	// bring flex arrow to front
	for (link of g_allLinks) {
		if (link.config.flex)
			link.draw();
	}
}

function _phase_to_role(phase, default_role) {
	if (phase === "started")
		return "in";
	if (phase === "finished")
		return "out";
	if (phase === "performed")
		// return "whole";
		return default_role || "out";
	console.warn("Strange phase:", phase);
}


function highlight_or_connect(second_last_act, last_act) {
	const alg_area_from = g_allAlgAreas[second_last_act.executes];

	if (last_act.is_valid) {
		// find output slot and it's link
		// const alg_area_to = g_allAlgAreas[last_act.executes];
		/// console.log("area from:", alg_area_from)

		let outgoing_link;
		if (alg_area_from.output_link_by_cond) {
			outgoing_link = alg_area_from.output_link_by_cond(second_last_act.value);
		} else {
			const slot = alg_area_from.find_slot(_phase_to_role(second_last_act.phase))
			// console.log("slot:", slot)
			outgoing_link = slot.links_out[0];
		}
		// console.assert(outgoing_link)

		// let found_links = get_links_connecting(second_last_act.executes, last_act.executes);
		// console.log(found_links);
		// // find all links
		// // add styling
		// for (cond_link of found_links)

		// const highlight_color = '#55ff77';
		let link;
		for(link of outgoing_link.search_adjacent_links(last_act.executes, 1,1))
		{
			// link.config.color = highlight_color;
			link.config.highlighted = true;
			for (let diamond of [link.to.owner])
				if (link.to.corner.getDistance(link.from.corner) > 1)
				if (diamond instanceof TransitDiamond) {
					// diamond.config.color = highlight_color;
					diamond.highlight(false);
				}
		}
		// highlight the destination
		link.to.highlight()
	} else {
		let outgoing_slot;
		let input_slot;
		const alg_area_to = g_allAlgAreas[last_act.executes];
		let turn_outgoing_direction = 1;

		if (alg_area_from.output_link_by_cond) {
			let outgoing_link = alg_area_from.output_link_by_cond(second_last_act.value);
			outgoing_slot = outgoing_link.from;
			turn_outgoing_direction = 0;
		} else {
			outgoing_slot = alg_area_from.find_slot(_phase_to_role(second_last_act.phase))
			// console.log("slot:", slot)
		}
		input_slot = alg_area_to.find_slot(_phase_to_role(last_act.phase, "in"));

		// rotate by 90 and convert to Paper's angle
		let d1 = (360 - outgoing_slot.direction + (90 * turn_outgoing_direction)) % 360;
		let d2 = (360 - input_slot.direction + 90) % 360;

		let [h1, h2] = lay_curve_connection(
			outgoing_slot.corner, d1,
			input_slot.corner, d2,
		);

		// directions could be changed, get them
		d1 = (360 - h1.angle) % 360;
		d2 = (360 - h2.angle) % 360;

		// ensure there are slots there
		if (alg_area_from instanceof BoxArea ||
			alg_area_from instanceof ConditionDiamond)
		{
			outgoing_slot = alg_area_from.slot(d1);
		}
		if (alg_area_to instanceof BoxArea ||
			alg_area_to instanceof ConditionDiamond)
		{
			input_slot = alg_area_to.slot(d2);
		}

		// highlight framed area
		if (alg_area_from ) {
			alg_area_from.highlight(false);
		}
		if (alg_area_to instanceof SequenceArea) {
			alg_area_to.highlight(false);
		}

		const config =  {
			flex: true, arrow: true,
			color:'red',
			dashArray: [5, LINE_WIDTH*2],
			strokeCap: 'round',
			handles: [h1, h2],
		};

		alg_area_to.links.push(new Link(outgoing_slot, input_slot, config));
	}
}



function lay_curve_connection(p1,d1, p2,d2) { // -> h1, h2
	//// points and their directions in Paper.js convention
	let dx = (p2.x - p1.x);
	let dy = (p2.y - p1.y);

	const is_right = (dx > 0) ? 1 : -1;
	const is_down  = (dy > 0) ? 1 : -1;
	const is_tall  = (Math.abs(dy/dx) > 1) ? 1 : -1;

	let w = dy * 1.0;
	let h = dx * 0.8;
	let t1 = new paper.Point(1, 0).rotate(d1);
	let t2 = new paper.Point(1, 0).rotate(d2);

	// same direction
	if (d1 == d2 || Math.abs(d1 - d2) % 180 === 0) {
		return [
			new paper.Point(Math.abs(t1.x * w)*is_right,  Math.abs(t1.y * h)*is_down),
			new paper.Point(Math.abs(t2.x * w)*is_right*is_tall,  Math.abs(t2.y * h)*-is_down*is_tall)
		];

	// this works, too
	// 	// horizontal
	// 	if ((d1 == 0 || d1 == 180)) {
	// 		let w = dy * 1.2;
	// 		return [
	// 			new paper.Point(w*is_down*is_right, 0),
	// 			new paper.Point(w*is_down*is_right*is_tall, 0)
	// 		];
	// 	}
	// 	// vertical
	// 	if ((d1 == 90 || d1 == 270)) {
	// 		let h = dx * 0.8;
	// 		return [
	// 			new paper.Point(0,  h*is_down*is_right),
	// 			new paper.Point(0, -h*is_down*is_right*is_tall)
	// 		];
	// 	}
	}

	// different direction
	return [
		new paper.Point(Math.abs(t1.x * w)*is_right,  Math.abs(t1.y * h)*is_down),
		new paper.Point(Math.abs(t2.x * w)*-is_right,  Math.abs(t2.y * h)*-is_down)
	];

	// fallback
	return [new paper.Point(10,0), new paper.Point(10,0)];
}

function test_curve() {

	let segments = [
		new paper.Segment({
			point: new paper.Point(100,100),
			handleOut: new paper.Point(10,0),
		}),
		new paper.Segment({
			point: new paper.Point(100,200),
			handleIn: new paper.Point(10,0),
		}),
	]
	const path_data = {
		segments: segments,
		strokeWidth: 4,
		strokeColor: 'purple',
	};

	let curve = new paper.Path(path_data);

	const view = globals.project.view;

	view.onMouseMove = function(event) {
		curve.lastSegment.point = event.point;

		let [h1, h2] = lay_curve_connection(
			curve.firstSegment.point,
			90,
			curve.lastSegment.point,
			90,
		);

		// set new handlers
		curve.firstSegment.handleOut = h1;
		curve.lastSegment.handleIn = h2;
	}

	view.onMouseDown = function(event) {
		// console.log('clicked view :', event)
		curve.firstSegment.point = event.point;
	}

}
