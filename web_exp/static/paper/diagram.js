// diagram.js

const U = 35;  // Unit of length, in pixels (scale base)

const LINE_WIDTH = U * 0.23;
const ANGLE_OFFSET = U * 0.4;  // sorten right angles

const ARROW_WIDTH = LINE_WIDTH * 2;
const ARROW_LENGTH = ARROW_WIDTH * 0.86;

// get the reference later
var draw_shape = null;


function test() {
	draw_shape = window.globals.draw_shape;

	// let r = new paper.Rectangle([2,2], [7,7]);
	// console.log(r);
	// r.x += 100; // [100, 200]
	// console.log(r);

	var hidden = document.getElementById('algorithm_json');
	var algorithm_json = hidden.getAttribute("value")
	algorithm_json = JSON.parse(algorithm_json)
	// console.log(algorithm_json)

	entry_point = algorithm_json["entry_point"];
	delete algorithm_json;

	// var node = entry_point.body[0].body.body[0].branches[0];
	var node = entry_point.body[0].body.body[0];
	// console.log(node);
	var alg = create_alg_for(node);
	alg.rebase(new paper.Point(500, 140));
	alg.draw();
}

/*!
Translate point to vector of difference between bases
(or just move if one vector is given)*/
function rebasePoint(p, old_base, new_base) {
	let move_by = null;
	if (!new_base) {
		move_by = old_base;
	} else {
		move_by = new_base.subtract(old_base);
	}
	p.x += move_by.x;
	p.y += move_by.y;
	return move_by;
}


class Link {
	constructor(slot1, slot2, config) {
		// super();  // do not use in root classes !
		this.from = slot1;
		this.to   = slot2;
		this.config = config || {};
	}
	draw() {
		const path_data = {
			segments: connection_segments(this.from, this.to, this.config),
			strokeWidth: LINE_WIDTH,
		};

		draw_shape("path", path_data);

		if (this.config.arrow) {
			const path_data = {
				segments: make_arrow_head(this.to),
				strokeWidth: 0,
				fillColor: true,
			};
			draw_shape("path", path_data);
		}
	}
}

class Location {
	constructor(corner, size) {
		// super();
		this.corner = new paper.Point(corner || [0,0]);
		this.size   = new paper.Size (size   || [U,U]);
	}
	rebase(...bases) {
		return rebasePoint(this.corner, ...bases);
	}
}

class Slot extends Location {
	constructor(corner, direction) {
		super(corner, [0, 0]);
		this.direction = direction;  // 0 90 180 270
	}
	draw() {
		draw_shape(this.constructor.name, this.corner);
	}
	clone() {
		return new Slot(this.corner, this.direction);
	}
}

class AlgArea extends Location {
	constructor(corner) {
		super(corner);
		this.inner = [];
		this.slots = {};  // {angle: Slot_obj}
		this.links = [];
	}
	bbox() {
		return new paper.Rectangle(this.corner, this.size);
	}
	fit(alg_node) {
		console.error("fit() not implemented!")
	}
	rebase(...bases) {
		const move_by = super.rebase(...bases);
		for (let st of this.inner) {
			st.rebase(move_by);
		}
		for (let a in this.slots) {
			this.slots[a].rebase(move_by);
		}
	}
	actualize_rect(padding) {  // recalc size and position
		// find children' bounds
		let bbox = new paper.Rectangle(this.corner, [0,0]);
		for (let node of this.inner) {
			bbox = bbox.unite(node.bbox());
		}
		// furthermore, apply padding
		padding = padding || this.padding || new paper.Size(U * 0.5, 0);
		bbox = bbox.expand(padding);
		// move origin if required
		if (!this.corner.equals(bbox.topLeft)) {
			// this.rebase(this.corner, bbox.topLeft);
			// this.rebase(bbox.topLeft, this.corner);
			this.corner = bbox.topLeft;
		}
		// save the calculated size
		this.size = bbox.size;
	}
	draw() {
		this.draw_self();
		this.draw_children();
	}
	draw_self() {
		draw_shape(this.constructor.name, this.position_self());
	}
	position_self() {
		return this.bbox();
	}
	draw_children() {
		for (let a of this.links) {
			a.draw();
		}
		for (let a of this.inner) {
			a.draw();
		}
		// for (let a in this.slots) {
		// 	this.slots[a].draw();
		// }
	}
}

class TransitDiamond extends AlgArea {  // two slots vertically
	constructor(corner, side_slots) {
		super(corner);
		this.side = LINE_WIDTH / 2;
		// leave zero size -- ???
		this.size = new paper.Size(0, 0);
		this.slots = {
			90:  new Slot(this.corner.add([0, -this.side]),  90),
			270: new Slot(this.corner.add([0,  this.side]), 270),
		};
		if (side_slots) {
			// add more slots
			if (side_slots.includes(0))
				this.slots[0  ] = new Slot(this.corner.add([ this.side, 0]), 0);
			if (side_slots.includes(180))
				this.slots[180] = new Slot(this.corner.add([-this.side, 0]), 180);

		}
	}
	position_self() {
		return new paper.Rectangle(
			this.corner.subtract([this.side, this.side]),
			new paper.Size(this.side * 2, this.side * 2)
		);
	}
}

class SequenceArea extends AlgArea {
	fit(alg_node) {
		const sep = U * 0.4;
		const offset = new paper.Point(0, sep);
		let plug_point = this.corner;
		let node = null;

		/// add visual begin/end mark
		node = new TransitDiamond(plug_point)
		this.inner.push(node);
		// input of whole node
		let current_slot = node.slots[90].clone();
		this.slots[90] = current_slot

		let last_slot = node.slots[270];
		plug_point = plug_point.add(offset)

		// add all as vertial stack and align each by X coordinate
		for (let st of alg_node.body) {
			node = create_alg_for(st);
			if (node) {
				const current_slot = node.slots[90];
				// link a stmt
				this.links.push(new Link(last_slot, current_slot));
				const top = current_slot.corner;
				// node.rebase(plug_point, top);
				node.rebase(top, plug_point);
				this.inner.push(node);
				last_slot = node.slots[270];
				const bottom = last_slot.corner;
				plug_point = bottom.add(offset);
			}
		}

		/// add visual begin/end mark
		node = new TransitDiamond(plug_point)
		this.inner.push(node);
		current_slot = node.slots[90];
		// link end of sequence
		this.links.push(new Link(last_slot, current_slot));
		// const current_slot = new Slot(plug_point, 270);

		// output of whole node
		last_slot = node.slots[270].clone();
		this.slots[270] = last_slot;

		this.actualize_rect();
	}
}

class ConditionDiamond extends AlgArea {  // two slots vertically
	constructor(corner) {
		super(corner);
	}
	fit(alg_node) {
		// this.alg_node = alg_node;  // ???
		const w = U * 2;
		const h = U * 1;
		this.size = new paper.Size(w, h);
		this.slots = {
			0:   new Slot(this.corner.add([w, h/2]),  0),
			90:  new Slot(this.corner.add([w/2, 0]),  90),
			180: new Slot(this.corner.add([0, h/2]),  180),
			270: new Slot(this.corner.add([w/2, h]),  270),
		};
	}
}

class AlternativeArea extends AlgArea {
	fit(alg_node) {
		this.branches = []

		const seph = U * 1.0;
		const sepv = U * 0.6;
		const offseth = new paper.Point(seph, 0);
		const offsetv = new paper.Point(0, sepv);
		let plug_point = this.corner;
		// let node = null;
		let branch = null;

		// size occupied by all branches - to be found
		let branches_area = new paper.Rectangle(this.corner, [0,0]);

		// align all branches hor centered, and get max size
		for (let st of alg_node.branches) {
			branch = create_alg_for(st);
			if (branch) {
				this.branches.push(branch)
				this.inner.push(branch);

				let branch_bbox = branch.bbox();
				const left = branch_bbox.leftCenter;
				branch.rebase(left, plug_point);
				branch_bbox = branch.bbox();
				branches_area = branches_area.unite(branch_bbox)
				plug_point = branch_bbox.rightCenter.add(offseth);
			}
		}

		const cond_bottom_y = branches_area.top - sepv;

		// position all condition diamonds above their branches
		let last_cond = null;
		let input_diamond = null;
		let join_diamond = null;
		let output_diamond = null;
		for (branch of this.branches) {
			if (branch.cond) {
				// link cond with its branch
				this.inner.push(branch.cond);
				this.links.push(new Link(branch.cond.slots[270], branch.slots[90], {text: "1", arrow: true}));

				// position the cond
				plug_point = branch.slots[90].corner.clone();
				plug_point.y = cond_bottom_y;
				let bottom = branch.cond.slots[270].corner;
				branch.cond.rebase(bottom, plug_point);

				let branch_output_slot = branch.slots[270];

				if (!last_cond) {
					// the first (IF) branch is currently processed
					// make the input of whole node
					plug_point = branch.cond.slots[90].corner.subtract(offsetv);
					input_diamond = new TransitDiamond(plug_point)
					this.inner.push(input_diamond);
					// input of whole node
					this.slots[90] = input_diamond.slots[90].clone();

					// link input to the first cond
					let cond_slot = branch.cond.slots[90];
					this.links.push(new Link(input_diamond.slots[270], cond_slot, {arrow: true}));


					// make the join_diamond
					plug_point = branch_output_slot.corner.add(offsetv);
					join_diamond = new TransitDiamond(plug_point, [0])
					this.inner.push(join_diamond);

					// link current branch to the join_diamond
					this.links.push(new Link(branch_output_slot, join_diamond.slots[90], {arrow: true}));


					// make the output of whole node
					plug_point = join_diamond.slots[270].corner.add(offsetv);
					output_diamond = new TransitDiamond(plug_point)
					this.inner.push(output_diamond);
					// output of whole node
					this.slots[270] = output_diamond.slots[270].clone();

					// link join_diamond to the output
					this.links.push(new Link(join_diamond.slots[270], output_diamond.slots[90]));
				} else {
					// some "else-if" branch is currently processed

					// link from prev cond
					this.links.push(new Link(last_cond.slots[0], branch.cond.slots[180], {text: "0", arrow: true}));

					// link current branch to the join_diamond
					this.links.push(new Link(branch_output_slot, join_diamond.slots[0], {arrow: true}));
				}

				last_cond = branch.cond;
			} else {
				// "else" branch

				// link from prev cond to current branch
				this.links.push(new Link(last_cond.slots[0], branch.slots[90], {text: "0", arrow: true}));

				// link current branch to the join_diamond
				this.links.push(new Link(branch.slots[270], join_diamond.slots[0], {arrow: true}));
			}
		}
		if (branch.cond) {
			// no "else" branch
			// link from prev cond to the join_diamond
			const cond_slot = last_cond.slots[0];

			const helper_vertex = new TransitDiamond(new paper.Point(
				branch.bbox().rightCenter.add(offseth))
			);
			this.inner.push(helper_vertex);

			// link from prev cond to the join_diamond
			this.links.push(new Link(cond_slot, helper_vertex.slots[90], {text: "0"}));
			this.links.push(new Link(helper_vertex.slots[270], join_diamond.slots[0], {arrow: true}));

		}

		this.actualize_rect();
	}
}

class BoxArea extends AlgArea {
	fit(alg_node) {
		this.alg_node = alg_node;  // ???

		this.size = new paper.Size(U * 3, U * 2);

		// input of the  node
		let slot = new Slot([this.size.width/2, 0], 90);
		this.slots[90] = slot;

		// output of whole node
		slot = new Slot([this.size.width/2, this.size.height], 270);
		this.slots[270] = slot;

		//// this.actualize_rect();
	}
}


function create_alg_for(alg_node) {
	let a = null;
	if (["sequence", "if", "else", "else-if"].includes(alg_node.type)) {
		a = new SequenceArea();
		if (alg_node.cond) {
			a.cond = create_alg_for(alg_node.cond);
		}
	}
	if (alg_node.type == "stmt") {
		a = new BoxArea();
	}
	if (alg_node.type == "expr") {
		a = new ConditionDiamond();
	}
	if (alg_node.type == "alternative") {
		a = new AlternativeArea();
	}
	// if (alg_node.type == "sequence") {
	// 	a = new SequenceArea();
	// }

	if (a) {
		a.fit(alg_node);
	} else {
		console.warn("No handler for node type: " + alg_node.type);
	}
	return a;  // can be null
}


function connection_segments(from, to, config) {
	// make segments for linear or right angle link
	/// console.log(from.direction, to.direction)

	let end = to.corner
	if (config.arrow) {
		// shrink the end so that arrow will look good
		end = end.add(new paper.Point(ARROW_LENGTH-1, 0).rotate(-to.direction))
	}

	if (180 == Math.abs(from.direction - to.direction)) {
		// opposite direction
		return [
			from.corner,
			end,
		];
	}

	const hor1 = (from.direction % 180) == 0;
	const hor2 = (  to.direction % 180) == 0;

	if (hor1 != hor2) {
		let middle = new paper.Point(
			(!hor1? from : to).corner.x,
			(!hor2? from : to).corner.y,
		);
		const offset_vec = new paper.Point(ANGLE_OFFSET, 0);
		return [
			from.corner,
			// middle,
			new paper.Segment({
				point: middle.subtract(offset_vec.rotate(-from.direction)),
				handleOut: offset_vec.multiply(0.5).rotate(-from.direction),
			}),
			new paper.Segment({
				point: middle.subtract(offset_vec.rotate(-to.direction)),
				handleIn: offset_vec.multiply(0.5).rotate(-to.direction),
			}),
			end,
		];
	}
	console.warn("Unknown connection case:", from, to);
}

function make_arrow_head(slot) {
	const p = slot.corner;
	const a = -slot.direction;
	// make a triangle
	return [
		p,
		p.add(new paper.Point(ARROW_LENGTH, ARROW_WIDTH/2).rotate(a)),
		p.add(new paper.Point(ARROW_LENGTH, -ARROW_WIDTH/2).rotate(a)),
	];
}



function on_load() {
	test();
}
