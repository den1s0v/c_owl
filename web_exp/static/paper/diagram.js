// diagram.js

const U = 24;  // Unit of length, in pixels (scale base)

const LINE_WIDTH = U * 0.33;
const ANGLE_OFFSET = U * 0.4;  // sorten right angles

const ARROW_WIDTH = LINE_WIDTH * 2.3;
const ARROW_LENGTH = ARROW_WIDTH * 0.86;

const FONT_SIZE = U * 0.5;
const ALLOW_SQUEEZE = true;  // ex. hide borders of single-action sequence

let LBL = {
	1: "true",
	0: "false",
};

// get the reference later
var draw_shape = null;

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
	var node = entry_point;
	// console.log(node);
	var alg = create_alg_for(node);

	/// <->
	// link_ids(10, 'out', 9, "in", {
	// 	flex: true, arrow: true,
	// 	// text:"arbitrary",
	// 	color:'red',
	// 	dashArray: [5, LINE_WIDTH*2],
	// 	strokeCap: 'round',
	// });

	const highlight_color = '#9fb';
	for (let id of [3,4,5,6,7,8,9,10,11].slice(1, )) {
	// for (let id of [7]) {
		let found_links = get_links_connecting(id, null);
		// let found_links = get_links_connecting(null, id);
		// if (found_links.length === 0 || !(found_links[0].from.owner instanceof ConditionDiamond))
		// 	continue;
		let cond_link = found_links[0] //.from.owner.output_link_by_cond(0);
		// if (cond_link)
		for (cond_link of found_links)
		for(let link of cond_link.search_adjacent_links(null, 0,1))
		{
			// console.log(link);
			link.config.color = highlight_color;
			for (let diamond of [link.from.owner, link.to.owner])
				if (diamond instanceof TransitDiamond) {
					diamond.config.color = highlight_color;
				}
		}
		// for(let link of get_links_connecting(null, id)) {
		// 	// console.log(link);
		// 	link.config.color = highlight_color;
		// 	for (let diamond of [link.from.owner, link.to.owner])
		// 		if (diamond instanceof TransitDiamond) {
		// 			diamond.config.color = highlight_color;
		// 		}
		// }
	}
	/// </>

	alg.rebase(new paper.Point(350, 10));
	alg.draw();


	// /// bring flex arrow to front
	for (link of g_allLinks) {
		if (link.config.flex)
			link.draw();
	}

}

function get_links_connecting(from_id, to_id) {
	let res = [];
	for (link of g_allLinks) {
		if (
			(!from_id || link.from.owner.alg_id == from_id) &&
			(!to_id   || link.to.owner.alg_id   == to_id)
		) {
			// res.push(...link.search_adjacent_links(to_id, true, true));
			res.push(link);
		}
	}
	return res;
}
// function get_adjacent_links(base_link, to_id, _partial_result) {
// 	let res = _partial_result || [base_link];
// 	let link, links, proceed;
// 	let diamond, diamond2; /// = base_link.to.owner;
// 	let stack = [diamond];
// 	// find all consequent links
// 	proceed = true;
// 	// while (proceed && diamond instanceof TransitDiamond) {
// 	while (stack.length>0) {
// 		diamond = stack.pop();
// 		if (!(diamond instanceof TransitDiamond))
// 			continue;
// 		// proceed = false;
// 		/// console.log(diamond)
// 		for (direction in diamond.slots)
// 		for (link of diamond.slots[direction].links_out) {
// 			if (!res.includes(link)) {
// 				console.log('>', link)
// 				res.push(link);
// 				// res.push(...get_adjacent_links(link, res));
// 				diamond2 = link.to.owner;
// 				if (diamond2 instanceof TransitDiamond)
// 					stack.push(diamond2);
// 			}
// 		}
// 	}

// 	diamond = base_link.from.owner;
// 	// find all precedent links
// 	proceed = true;
// 	while (stack.length>0) {
// 		diamond = stack.pop();
// 		if (!(diamond instanceof TransitDiamond))
// 			continue;
// 		// proceed = false;
// 		for (direction in diamond.slots)
// 		for (link of diamond.slots[direction].links_in) {
// 			if (!res.includes(link)) {
// 				console.log('<', link)
// 				res.push(link);
// 				// res.push(...get_adjacent_links(link, res));
// 				diamond2 = link.to.owner;
// 				if (diamond2 instanceof TransitDiamond)
// 					stack.push(diamond2);
// 			}
// 		}
// 	}
// 	return res;
// }
function link_ids(from_id, from_phase, to_id, to_phase, config) {
	// debug
	// for (alg_id of Object.keys(g_allAlgAreas)) {
	// 	console.log(alg_id)
	// }

	let from_node = g_allAlgAreas[from_id];
	let to_node   = g_allAlgAreas[  to_id];
	if (!from_node || !to_node) {
		console.warn("No valid node(s) for ids:", from_id, to_id, ": ==> ", from_node, to_node);
		return;
	}
	let slot_from = from_node.find_slot(from_phase, 0);
	let slot_to   = to_node  .find_slot(to_phase, 180);
	// let slot_from = from_node.slot(270);
	// let slot_to   = to_node  .slot(180);
	/// console.log(slot_from.direction, slot_to.direction)
	to_node.links.push(new Link(slot_from, slot_to, config));
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

		if (this.config.propagate_arrow) {
			this.propagate_arrow(this.from.direction)
		}
	}
	propagate_arrow(direction) {
		// // return true if propagated ?
		let diamond = this.to.owner;
		if (!(diamond instanceof TransitDiamond))
			diamond = diamond.inner[0];
		if (diamond instanceof TransitDiamond) {
			diamond.actualize_config();
			if (diamond.config.hidden && diamond.slots[direction]) {
				diamond.slots[direction].links_out[0].propagate_arrow(direction)
				delete this.config.propagate_arrow;
				return;  // return true;
			} /// else console.log("Not hidden")
		} /// else console.log("Not TransitDiamond:", this.to.owner)
		// set arrow to this
		this.config.arrow = true;
		delete this.config.propagate_arrow;
		// return false;
	}
	search_adjacent_links(to_id, can_turn, through_hierarchy) {  /// , backward
		if (this.to.owner.alg_id === to_id)
			return [this];

		// search forward only
		let found_links = [];
		const reversed_direction = this.to.direction;
		const expected_direction = (reversed_direction + 180) % 360;

		let diamond = this.to.owner;

		// if first
		if (through_hierarchy && diamond && !(diamond instanceof TransitDiamond)) {
			// console.debug("Moving  deeper:", diamond)
			diamond = diamond.inner[0];
			// console.debug("diamond deeper:", diamond)
		} ///else console.debug("not TransitDiamond (3):", diamond)

		// const in_slots = this.from.owner.find_slots('in');
		if (diamond) {
			const out_slots = diamond.find_slots('out');
			if (diamond instanceof TransitDiamond || through_hierarchy && (
				// if last
				Object.values(out_slots).includes(this.to)
				// Object.values(in_slots).includes(this.from) ||
				)) {
				// console.debug(".search_adjacent_links():", diamond)
				for (let d in out_slots) {
					if (!can_turn && d != expected_direction && d != reversed_direction)  // reversed_direction ??
						continue;
					// let slot = diamond.slots[d];
					let slot = out_slots[d];
					for (let link of slot.links_out) {
						found_links.push(...link.search_adjacent_links(to_id, can_turn, through_hierarchy));
					}
				} /// else console.log("Not hidden")
			} /// else console.log("Not TransitDiamond:", this.to.owner)
		}
		// anything is valid if no target specified
		if (found_links.length > 0 || !to_id)
			found_links.unshift(this);
		// console.debug(".search_adjacent_links():", found_links)
		return found_links;
	}
	draw() {
		// refresh slots first
		this.from.owner.actualize_config && this.from.owner.actualize_config();
		this.to  .owner.actualize_config && this.to  .owner.actualize_config();

		const path_data = {
			segments: connection_segments(this.from, this.to, this.config),
			strokeWidth: LINE_WIDTH,
			strokeColor: this.config.color,
			...this.config,
		};
		draw_shape("path", path_data);

		if (this.config.arrow) {
			const path_data = {
				segments: make_arrow_head(this.to),
				strokeWidth: 0,
				fillColor: this.config.color || true,
			};
			draw_shape("path", path_data);
		}

		if (this.config.text) {
			let p1 = path_data.segments[0];
			let p2 = path_data.segments[1];
			let point = new paper.Rectangle(p1.point || p1, p2.point || p2).center;
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
	constructor(corner, direction, owner, role) {
		super(corner, [0, 0]);
		this.direction = direction;  // 0 90 180 270
		this.owner = owner;
		console.assert(role);
		this.role = role;
		this.links_in  = [];
		this.links_out = [];
	}
	draw() {
		draw_shape(this.constructor.name, this.corner);
	}
	clone() {
		// do not copy owner and links !
		return new Slot(this.corner, this.direction, null, this.role);
	}
}

class AlgArea extends Location {
	constructor(corner, config, parent) {
		super(corner);
		this.inner = [];
		this.slots = {};  // {angle: Slot_obj}
		this.links = [];
		this.parent = parent;
		this.config = config || {};
		this.alg_id = false;    // assigned in create_alg_for()
		this.alg_name = false;  // assigned in create_alg_for()
	}
	slot(direction, role) {  // getter & default creator
		if (!this.slots[direction])
			return this.create_slot(direction, null, role);
		return this.slots[direction];
	}
	create_slot(direction, foreign_slot, role) {  // creator
		if (foreign_slot) {
			// adapt slot created for other node
			let slot = foreign_slot.clone();
			slot.owner = this;
			if (role) slot.role = role;
			this.slots[direction] = slot;
			return slot;
		} else {
			return this._create_side_slot(direction, role);
		}
	}
	_guess_slot_role(direction) {  // returns "in" or "out"
		return ([0, 270].includes(direction))? "out" : "in";
	}
	_create_side_slot(direction, role) {  // creator
		// create a new slot at middle of bbox side
		const bbox = this.bbox();
		let point = null;
		if (90 === direction) point = bbox.topCenter;
		else if (270 === direction) point = bbox.bottomCenter;
		else if (  0 === direction) point = bbox.rightCenter;
		else if (180 === direction) point = bbox.leftCenter;
		if (!role) {
			role = this._guess_slot_role(direction);
			if ([0,180].includes(direction))
				console.debug("fallback slot role to:", role, "for direction", direction, ", for object:", this);
		}
		let slot = new Slot(point, direction, this, role);
		this.slots[direction] = slot;
		return slot;
	}
	find_slot(in_out, preferred_direction) {  // find slot for in or out connection
		if (this.slots[preferred_direction] || in_out == "whole")
			return this.slot(preferred_direction);

		let found_slots = this.find_slots(in_out);
		if (in_out.includes('in')) {
			preferred_direction = 90;
		} else {
			preferred_direction = 270;
		}
		for (let d in found_slots) {
			return found_slots[d];
		}
		// use default
		return this.slot(preferred_direction);
	}
	find_slots(in_out) {
		let found_slots = {}
		// let links_field = null;
		// if (in_out.includes('in')) {
		// 	links_field = "links_in";
		// } else if (in_out.includes('out')) {
		// 	links_field = "links_out";
		// } else {
		// 	console.warn("*.find_slots(): bad in_out parameter:", in_out);
		// }
		for (let d in this.slots) {
			if (this.slots[d].role == in_out)  // direct comparison
				found_slots[d] = (this.slots[d]);
		}
		return found_slots;
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
		// // move origin if required
		// if (!this.corner.equals(bbox.topLeft)) {
		// 	// this.rebase(this.corner, bbox.topLeft);
		// 	// this.rebase(bbox.topLeft, this.corner);
		// 	// this.corner = bbox.topLeft;
		// }
		// set origin so left top is zero
		let zero = new paper.Point(0,0)
		this.rebase(bbox.topLeft, zero);
		this.corner = zero;
		// save the calculated size
		this.size = bbox.size;
	}
	draw() {
		this.draw_self();
		this.draw_children();
	}
	draw_self() {
		draw_shape(this.constructor.name, this.position_self());
		/// debug
		return
		if (this.alg_name)
			draw_shape("text", {
				point: this.corner,
				content: this.alg_name,
				justification: 'right',
				// fillColor: '#f48',
				// // fontFamily: 'Courier New',
				// fontWeight: 'bold',
				// fontSize: FONT_SIZE,
				// // Set the shadow color of the circle to RGB black:
				// shadowColor: "white",
				// // Set the shadow blur radius to 12:
				// shadowBlur: 12,
			});
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
		/// debug connection point
		// for (let a in this.slots) {
		// 	this.slots[a].draw();
		// }
	}
}

class TransitDiamond extends AlgArea {  // links connection
	constructor(corner, parent, config) {
		super(corner, config, parent);
		this.side = LINE_WIDTH / 2;
		// leave zero size -- ???
		this.size = new paper.Size(0, 0);
		// this.config.hidden = true;
		// this.config.color = 'red';
	}
	_create_side_slot(direction, role) {  // creator
		let point = null;
		if (90 === direction) 		point = this.corner.add([0, -this.side]);
		else if (270 === direction) point = this.corner.add([0,  this.side]);
		else if (  0 === direction) point = this.corner.add([ this.side, 0]);
		else if (180 === direction) point = this.corner.add([-this.side, 0]);
		if (!role) {
			role = this._guess_slot_role(direction);
			if ([0,180].includes(direction))
				console.debug("fallback slot role to:", role, "for direction", direction, ", for object:", this);
		}
		let slot = new Slot(point, direction, this, role);
		this.slots[direction] = slot;
		return slot;
	}
	actualize_config() {
		// actualize "hidden" setting
		let hidden = true;
		var size = Object.keys(this.slots).length;  // https://stackoverflow.com/questions/5223/length-of-a-javascript-object
		if (size > 2) {
			hidden = false;
		} else {
			const keys = Object.keys(this.slots);
			const is_straight = (180 == Math.abs(
				this.slots[keys[0]].direction -
				this.slots[keys[1]].direction))

			hidden = is_straight;
		}
		this.config.hidden = hidden;
		/// this.config.hidden = false;
	}
	draw() {
		// actualize "hidden" setting
		this.actualize_config();
		super.draw();
	}
	position_self() {
		return {
			rectangle: new paper.Rectangle(
				this.corner.subtract(this.side),
				new paper.Size(this.side * 2, this.side * 2)),
			...this.config,
		};
	}
}

class SequenceArea extends AlgArea {
	fit(alg_node) {
		let node = null;
		let plug_point = this.corner;

		if (alg_node.body.length === 1) {
			// short laconic mode: equal to only one child
			let st = alg_node.body[0];
			node = create_alg_for(st, this);

			// input of whole node
			this.create_slot(90, node.slot(90));

			this.links.push(new Link(this.slot(90), node.slot(90)));

			node.rebase(node.corner, plug_point);
			this.inner.push(node);

			// output of whole node
			this.create_slot(270, node.slot(270));

			this.links.push(new Link(node.slot(270), this.slot(270)));

			this.size = node.size.clone();
			return;
		}

		const sep = U * 0.4;
		const offset = new paper.Point(0, sep);
		let current_slot = null;

		// input of whole node
		let diamond = new TransitDiamond(plug_point, this);
		this.inner.push(diamond);
		this.create_slot(90, diamond.slot(90));
		// connect through
		this.links.push(new Link(this.slot(90), diamond.slot(90)));


		let last_slot = diamond.slot(270);
		plug_point = plug_point.add(offset);

		// add all as vertial stack and align each by X coordinate
		for (let st of alg_node.body) {
			node = create_alg_for(st, this);
			if (node) {
				const current_slot = node.slot(90);
				// link a stmt
				this.links.push(new Link(last_slot, current_slot));
				const top = current_slot.corner;
				node.rebase(top, plug_point);
				this.inner.push(node);

				last_slot = node.slot(270);
				const bottom = last_slot.corner;
				plug_point = bottom.add(offset);
			}
		}

		/// add visual begin/end mark
		diamond = new TransitDiamond(plug_point, this, {hidden: true})
		this.inner.push(diamond);
		current_slot = diamond.slot(90);
		// link end of sequence
		this.links.push(new Link(last_slot, current_slot));

		// output of whole node
		this.create_slot(270, diamond.slot(270));
		// connect through
		this.links.push(new Link(diamond.slot(270), this.slot(270)));

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
	output_link_by_cond(cond_val) {
		cond_val = cond_val? 1 : 0;
		const text = LBL[cond_val];
		let found_slots = this.find_slots('out');
		for (let d in found_slots) {
			let link = found_slots[d].links_out[0];
			if (link.config.text === text)
				return link;
		}
		return null;
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
		let input_diamond = null;

		// make the input of whole node
		input_diamond = new TransitDiamond(null, this);
		this.inner.push(input_diamond);

		// size occupied by all branches - to be found
		let branches_area = new paper.Rectangle(this.corner, [0,0]);

		// align all branches hor centered, and get max size
		for (let st of alg_node.branches) {
			branch = create_alg_for(st, this);
			if (branch) {
				this.branches.push(branch)
				if (branch.cond) this.inner.push(branch.cond);
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
		let join_diamond = null;
		let output_diamond = null;
		for (branch of this.branches) {
			if (branch.cond) {
				// link cond with its branch
				// this.inner.push(branch.cond);
				this.links.push(new Link(branch.cond.slot(270), branch.slot(90), {text: LBL[1], propagate_arrow: true}));

				// position the cond
				plug_point = branch.slot(90).corner.clone();
				plug_point.y = cond_bottom_y;
				let bottom = branch.cond.slot(270).corner;
				branch.cond.rebase(bottom, plug_point);

				let branch_output_slot = branch.slot(270);

				if (!last_cond) {
					// the first (IF) branch is currently processed
					plug_point = branch.cond.slot(90).corner.subtract(offsetv);
					input_diamond.rebase(plug_point);
					// input of whole node
					this.create_slot(90, input_diamond.slot(90));
					// connect through
					this.links.push(new Link(this.slot(90), input_diamond.slot(90)));

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
					output_diamond = new TransitDiamond(plug_point, this);
					this.inner.push(output_diamond);
					// output of whole node
					this.create_slot(270, output_diamond.slot(270));

					// link join_diamond to the output
					this.links.push(new Link(join_diamond.slot(270), output_diamond.slot(90)));

					// connect end through
					this.links.push(new Link(output_diamond.slot(270), this.slot(270)));
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
				this.links.push(new Link(branch.slot(270), join_diamond.slot(0, "in"), {arrow: true}));
			}
		}
		if (branch.cond) {
			// no "else" branch
			// link from prev cond to the join_diamond
			const cond_slot = last_cond.slot(0);

			const helper_vertex = new TransitDiamond(new paper.Point(branch.bbox().rightCenter.add(offseth)), this, {hidden: true});
			this.inner.push(helper_vertex);

			// link from prev cond to the join_diamond
			this.links.push(new Link(cond_slot, helper_vertex.slot(90), {text: LBL[0]}));
			this.links.push(new Link(helper_vertex.slot(270), join_diamond.slot(0, "in"), {arrow: true}));

		}

		this.actualize_rect();
	}
}

class WhileLoopArea extends AlgArea {
	fit(alg_node) {

		const seph = U * 1.0;
		const sepv = U * 0.6;
		const offseth = new paper.Point(seph, 0);
		const offsetv = new paper.Point(0, sepv);
		let current_slot = null;
		let plug_point = this.corner;
		plug_point = plug_point.add(offsetv);

		const input_diamond = new TransitDiamond(plug_point, this);
		this.inner.push(input_diamond);
		// input of whole node
		this.create_slot(90, input_diamond.slot(90));
		// connect through
		this.links.push(new Link(this.slot(90), input_diamond.slot(90)));

		const cond = create_alg_for(alg_node.cond, this);
		const body = create_alg_for(alg_node.body, this);

		this.inner.push(cond);
		this.inner.push(body);

		// link cond
		cond.rebase(cond.slot(90).corner, plug_point);
		this.links.push(new Link(input_diamond.slot(270), cond.slot(90)));

		plug_point = cond.slot(270).corner.add(offsetv);

		// link body
		body.rebase(body.slot(90).corner, plug_point);
		this.links.push(new Link(cond.slot(270), body.slot(90), {text: LBL[1]}));

		const body_bbox = body.bbox();

		// link up to cond by left side ...
		const helper_vertex_left = new TransitDiamond(new paper.Point(body_bbox.topLeft.subtract(offseth)), this, {hidden: true});
		this.inner.push(helper_vertex_left);

		// rotate body's output lo left
		/// ???
		let body_out = body.slot(270, "out");
		body_out.direction = 180;

		// link from body to cond
		this.links.push(new Link(body_out, helper_vertex_left.slot(270, "in")));
		this.links.push(new Link(helper_vertex_left.slot(90, "out"), cond.slot(180), {arrow: true}));

		plug_point = body_out.corner.add(offsetv);

		const join_diamond = new TransitDiamond(plug_point, this);
		this.inner.push(join_diamond);

		// link down to join_diamond by right side ...
		const helper_vertex_right = new TransitDiamond(new paper.Point(body_bbox.bottomRight.add(offseth)), this, {hidden: true});
		this.inner.push(helper_vertex_right);

		// link from cond to the join_diamond
		this.links.push(new Link(cond.slot(0), helper_vertex_right.slot(90), {text: LBL[0]}));
		this.links.push(new Link(helper_vertex_right.slot(270), join_diamond.slot(0, "in"), {arrow: true}));

		plug_point = plug_point.add(offsetv);

		const output_diamond = new TransitDiamond(plug_point, this);
		this.inner.push(output_diamond);
		// output of whole node
		this.create_slot(270, output_diamond.slot(270));
		// connect end through
		this.links.push(new Link(output_diamond.slot(270), this.slot(270)));

		// link join_diamond to the output
		this.links.push(new Link(join_diamond.slot(270), output_diamond.slot(90)));

		this.actualize_rect();
	}
}

class DoLoopArea extends AlgArea {
	fit(alg_node) {

		const seph = U * 1.0;
		const sepv = U * 0.6;
		const offseth = new paper.Point(seph, 0);
		const offsetv = new paper.Point(0, sepv);
		let current_slot = null;
		let plug_point = this.corner;
		plug_point = plug_point.add(offsetv);

		const input_diamond = new TransitDiamond(plug_point, this);
		this.inner.push(input_diamond);
		// input of whole node
		this.create_slot(90, input_diamond.slot(90));
		// connect through
		this.links.push(new Link(this.slot(90), input_diamond.slot(90)));

		const cond = create_alg_for(alg_node.cond, this);
		const body = create_alg_for(alg_node.body, this);

		this.inner.push(cond);
		this.inner.push(body);

		plug_point = plug_point.add(offsetv);

		// upper join_diamond, above the body
		const join_diamond = new TransitDiamond(plug_point, this);
		this.inner.push(join_diamond);
		this.links.push(new Link(input_diamond.slot(270), join_diamond.slot(90)));

		plug_point = plug_point.add(offsetv);

		// link body
		body.rebase(body.slot(90).corner, plug_point);
		this.links.push(new Link(join_diamond.slot(270), body.slot(90)));

		plug_point = body_out.corner.add(offsetv);

		// link cond
		cond.rebase(cond.slot(90).corner, plug_point);
		this.links.push(new Link(body.slot(270), cond.slot(90)));

		const body_bbox = body.bbox();

		// link up to cond by left side ...
		const helper_vertex_left = new TransitDiamond(new paper.Point(body_bbox.topLeft.subtract(offseth)), this, {hidden: true});
		this.inner.push(helper_vertex_left);

		// link from cond to join_diamond
		this.links.push(new Link(cond.slot(180, "out"), helper_vertex_left.slot(270, "in"), {text: LBL[1]}));
		this.links.push(new Link(helper_vertex_left.slot(90, "out"), join_diamond.slot(180), {arrow: true}));

		plug_point = cond.slot(270).corner.add(offsetv);

		/// // add one more diamond to connect break arrow to ? ...
		/// ...
		/// plug_point = plug_point.add(offsetv);

		const output_diamond = new TransitDiamond(plug_point, this);
		this.inner.push(output_diamond);
		// output of whole node
		this.create_slot(270, output_diamond.slot(270));
		// connect end through
		this.links.push(new Link(output_diamond.slot(270), this.slot(270)));

		// link join_diamond to the output
		this.links.push(new Link(cond.slot(270), output_diamond.slot(90), {text: LBL[0]}));

		this.actualize_rect();
	}
}


class BoxArea extends AlgArea {
	fit(alg_node) {
		// this.alg_node = alg_node;  // ???
		this.size = new paper.Size(U * 2, U * 0.81);
	}
}


function create_alg_for(alg_node, parent) {
	let a = null;
	if (["sequence", "if", "else", "else-if"].includes(alg_node.type)) {
		a = new SequenceArea();
		if (alg_node.cond) {
			// the sequence is alternative branch
			a.cond = create_alg_for(alg_node.cond, parent);
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
	if (alg_node.type == "while_loop") {
		a = new WhileLoopArea();
	}
	// if (alg_node.type == "sequence") {
	// 	a = new SequenceArea();
	// }

	if (a) {
		// more config
		a.alg_id = alg_node.id;
		a.alg_name = alg_node.name;
		if (parent) {
			/// console.log("parent", parent)
			a.parent = parent;
		}
		// store globally
		if (a.alg_id !== undefined) {
			g_allAlgAreas[a.alg_id] = a;
			console.debug(a.alg_id, '  \t- ', a.alg_name)
		}
		// create a tree for alg_node
		a.fit(alg_node);
	} else {
		console.warn("No handler for node type: " + alg_node.type);
	}
	return a;  // can be null
}


// helpers

function connection_segments(from, to, config) {

	if (to.corner.getDistance(from.corner) < 1) {
		// link should not be shown
		return [];
	}

	let end = to.corner
	if (config.arrow && !to.owner.config.hidden) {
		// if the link is too short, draw nothing
		if (end.getDistance(from.corner) < ARROW_LENGTH-1) {
			// link should not be shown
			return [];
		}

		// shrink the end so that arrow will look good
		end = end.add(new paper.Point(ARROW_LENGTH-1, 0).rotate(-to.direction))
	}

	if (config.flex) {
		const offset_vec = new paper.Point(ANGLE_OFFSET * 15, 0);
		return [
			new paper.Segment({
				point: from.corner,
				handleOut: offset_vec.rotate(-from.direction + 30),
			}),
			new paper.Segment({
				point: end,
				handleIn: offset_vec.rotate(-to.direction - 5),
			}),
		];
	}

	// make segments for linear or right angle link
	/// console.log(from.direction, to.direction)

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
				point: middle.subtract(offset_vec.rotate( -to.direction)),
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
