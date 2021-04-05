// diagram.js

const U = 25;  // Unit of length, in pixels (scale base)

const LINE_WIDTH = U * 0.33;
const ANGLE_OFFSET = U * 0.4;  // sorten right angles

const ARROW_WIDTH = LINE_WIDTH * 2;
const ARROW_LENGTH = ARROW_WIDTH * 0.86;

const FONT_SIZE = U * 0.5;
// get the reference later
var draw_shape = null;

let LBL = {
	1: "true",
	0: "false",
};


var g_allAlgAreas = {};  // {id -> object}
var g_allLinks = [];


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
	var node = entry_point.body[0].body;
	// console.log(node);
	var alg = create_alg_for(node);
	alg.rebase(new paper.Point(300, 10));
	alg.draw();
}

/*!
Translate point to vector of difference between bases
(or just move if one vector is given).
return the shift vector */
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

		// store link at slots
		this.from.links_out.push(this);
		this.to  .links_in .push(this);

		// store globally
		g_allLinks.push(this);
	}
	draw() {
		const path_data = {
			segments: connection_segments(this.from, this.to, this.config),
			strokeWidth: LINE_WIDTH,
		};
		draw_shape("path", path_data);

		if (this.config.text) {
			let p1 = path_data.segments[0];
			let p2 = path_data.segments[1];
			let point = new paper.Rectangle(p1, p2.point || p2).center;
			point.y += FONT_SIZE / 3;  // vertical centering workaround
			draw_shape("text", {
				point: point,
				content: this.config.text,
				justification: 'center',
				fillColor: '#f48',
				// fontFamily: 'Courier New',
				fontWeight: 'bold',
				fontSize: FONT_SIZE,
				// Set the shadow color of the circle to RGB black:
				shadowColor: "white",
				// Set the shadow blur radius to 12:
				shadowBlur: 12,

			});
			// console.log("text drawn: ", this.config.text, point);
		}

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
	constructor(corner, direction, owner) {
		super(corner, [0, 0]);
		this.direction = direction;  // 0 90 180 270
		this.owner = owner;
		this.links_in  = [];
		this.links_out = [];
	}
	draw() {
		draw_shape(this.constructor.name, this.corner);
	}
	clone() {
		// do not copy owner and links !
		return new Slot(this.corner, this.direction, null);
	}
}

class AlgArea extends Location {
	constructor(corner, config) {
		super(corner);
		this.inner = [];
		this.slots = {};  // {angle: Slot_obj}
		this.links = [];
		this.config = config || {};
		this.alg_id = false;    // assigned in create_alg_for()
		this.alg_name = false;  // assigned in create_alg_for()
	}
	slot(direction) {  // getter & default creator
		if (!this.slots[direction])
			return this.create_slot(direction);
		return this.slots[direction];
	}
	create_slot(direction, foreign_slot) {  // creator
		if (foreign_slot) {
			// adapt slot created for other node
			let slot = foreign_slot.clone();
			slot.owner = this;
			this.slots[direction] = slot;
			return slot;
		} else {
			return this._create_side_slot(direction);
		}
	}
	_create_side_slot(direction) {  // creator
		// create a new slot at middle of bbox side
		const bbox = this.bbox();
		let point = null;
		if (90 === direction) point = bbox.topCenter;
		else if (270 === direction) point = bbox.bottomCenter;
		else if (  0 === direction) point = bbox.rightCenter;
		else if (180 === direction) point = bbox.leftCenter;
		let slot = new Slot(point, direction, this);
		this.slots[direction] = slot;
		return slot;
	}
	find_slot(in_out, preferred_direction) {  // find slot for in or out connection
		if (this.slots[preferred_direction])
			return this.slots[preferred_direction];

		var links_field = null;
		if (in_out.includes('in')) {
			links_field = "links_in";
			preferred_direction = 90;
		} else if (in_out.includes('out')) {
			links_field = "links_out";
			preferred_direction = 270;
		} else {
			console.warn("*.find_slot(): bad in_out parameter");
		}
		for (let d in this.slots) {
			if (this.slots[d][links_field])  // not empty
				return this.slots[d];
		}
		// use default
		return this.slot(preferred_direction);
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
	constructor(corner, config) {
		super(corner, config);
		this.side = LINE_WIDTH / 2;
		// leave zero size -- ???
		this.size = new paper.Size(0, 0);
	}
	_create_side_slot(direction) {  // creator
		let point = null;
		if (90 === direction) 		point = this.corner.add([0, -this.side]);
		else if (270 === direction) point = this.corner.add([0,  this.side]);
		else if (  0 === direction) point = this.corner.add([ this.side, 0]);
		else if (180 === direction) point = this.corner.add([-this.side, 0]);
		let slot = new Slot(point, direction, this);
		this.slots[direction] = slot;
		return slot;
	}
	position_self() {
		return {
			rectangle: new paper.Rectangle(
				this.corner.subtract([this.side, this.side]),
				new paper.Size(this.side * 2, this.side * 2)),
			...this.config,
		};
	}
}

class SequenceArea extends AlgArea {
	fit(alg_node) {
		const sep = U * 0.4;
		const offset = new paper.Point(0, sep);
		let plug_point = this.corner;
		let node = null;
		let current_slot = null;

		/// add visual begin/end mark
		node = new TransitDiamond(plug_point)
		this.inner.push(node);
		// input of whole node
		this.create_slot(90, node.slot(90));

		let last_slot = node.slot(270);
		plug_point = plug_point.add(offset)

		// add all as vertial stack and align each by X coordinate
		for (let st of alg_node.body) {
			node = create_alg_for(st);
			if (node) {
				const current_slot = node.slot(90);
				// link a stmt
				this.links.push(new Link(last_slot, current_slot));
				const top = current_slot.corner;
				// node.rebase(plug_point, top);
				node.rebase(top, plug_point);
				this.inner.push(node);

				last_slot = node.slot(270);
				const bottom = last_slot.corner;
				plug_point = bottom.add(offset);
			}
		}

		/// add visual begin/end mark
		node = new TransitDiamond(plug_point, {hidden: true})
		this.inner.push(node);
		current_slot = node.slot(90);
		// link end of sequence
		this.links.push(new Link(last_slot, current_slot));
		// const current_slot = new Slot(plug_point, 270);

		// output of whole node
		this.create_slot(270, node.slot(270));

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

		const cond_bottom_y = branches_area.top - sepv * 2;

		// position all condition diamonds above their branches
		let last_cond = null;
		let input_diamond = null;
		let join_diamond = null;
		let output_diamond = null;
		for (branch of this.branches) {
			if (branch.cond) {
				// link cond with its branch
				this.inner.push(branch.cond);
				this.links.push(new Link(branch.cond.slot(270), branch.slot(90), {text: LBL[1], arrow: true}));

				// position the cond
				plug_point = branch.slot(90).corner.clone();
				plug_point.y = cond_bottom_y;
				let bottom = branch.cond.slot(270).corner;
				branch.cond.rebase(bottom, plug_point);

				let branch_output_slot = branch.slot(270);

				if (!last_cond) {
					// the first (IF) branch is currently processed
					// make the input of whole node
					plug_point = branch.cond.slot(90).corner.subtract(offsetv);
					input_diamond = new TransitDiamond(plug_point)
					this.inner.push(input_diamond);
					// input of whole node
					this.create_slot(90, input_diamond.slot(90));

					// link input to the first cond
					let cond_slot = branch.cond.slot(90);
					this.links.push(new Link(input_diamond.slot(270), cond_slot, {arrow: true}));


					// make the join_diamond
					plug_point = branch_output_slot.corner.add(offsetv);
					join_diamond = new TransitDiamond(plug_point);
					this.inner.push(join_diamond);

					// link current branch to the join_diamond
					this.links.push(new Link(branch_output_slot, join_diamond.slot(90), {arrow: true}));


					// make the output of whole node
					plug_point = join_diamond.slot(270).corner.add(offsetv);
					output_diamond = new TransitDiamond(plug_point)
					this.inner.push(output_diamond);
					// output of whole node
					this.create_slot(270, output_diamond.slot(270));

					// link join_diamond to the output
					this.links.push(new Link(join_diamond.slot(270), output_diamond.slot(90)));
				} else {
					// some "else-if" branch is currently processed

					// link from prev cond
					this.links.push(new Link(last_cond.slot(0), branch.cond.slot(180), {text: LBL[0], arrow: true}));

					// link current branch to the join_diamond
					this.links.push(new Link(branch_output_slot, join_diamond.slot(0), {arrow: true}));
				}

				last_cond = branch.cond;
			} else {
				// "else" branch

				// link from prev cond to current branch
				this.links.push(new Link(last_cond.slot(0), branch.slot(90), {text: LBL[0], arrow: true}));

				// link current branch to the join_diamond
				this.links.push(new Link(branch.slot(270), join_diamond.slot(0), {arrow: true}));
			}
		}
		if (branch.cond) {
			// no "else" branch
			// link from prev cond to the join_diamond
			const cond_slot = last_cond.slot(0);

			const helper_vertex = new TransitDiamond(new paper.Point(branch.bbox().rightCenter.add(offseth)), {hidden: true});
			this.inner.push(helper_vertex);

			// link from prev cond to the join_diamond
			this.links.push(new Link(cond_slot, helper_vertex.slot(90), {text: LBL[0]}));
			this.links.push(new Link(helper_vertex.slot(270), join_diamond.slot(0), {arrow: true}));

		}

		this.actualize_rect();
	}
}

class BoxArea extends AlgArea {
	fit(alg_node) {
		this.alg_node = alg_node;  // ???
		this.size = new paper.Size(U * 2, U * 1.41);
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
		// more config
		a.alg_id = alg_node.id;
		a.alg_name = alg_node.name;
		// store globally
		if (a.alg_id !== undefined)
			g_allAlgAreas[a.alg_id] = a;
		//
		a.fit(alg_node);
	} else {
		console.warn("No handler for node type: " + alg_node.type);
	}
	return a;  // can be null
}


// helpers

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
