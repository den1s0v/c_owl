// diagram.js

const U = 30;  // Unit of length, in pixels


function test() {
	let r = new paper.Rectangle([2,2], [7,7]);
	console.log(r);
	r.x += 100; // [100, 200]
	console.log(r);

	// hidden = document.getElementById('algorithm_json');
	// algorithm_json = hidden.getAttribute("value")
	// algorithm_json = JSON.parse(algorithm_json)
	// // console.log(algorithm_json)

	// entry_point = algorithm_json["entry_point"];
	// delete algorithm_json;
}

/*!
Translate point to vector of difference between bases
(or just move if one vector is given)*/
function rebasePoint(p, old_base, new_base) {
	let move_by = null;
	if (!new_base) {
		move_by = old_base;
	} else {
		move_by = new_base.substract(old_base);
	}
	p.x += move_by.x;
	p.y += move_by.y;
	return move_by;
}


class Link {
	constructor(slot1, slot2, style) {
		super();
		this.from = slot1;
		this.to   = slot2;
		this.style = style;  // ???
	}
	// fit() {
	// 	console.error("fit() not implemented!")
	// }
}

class Location {
	constructor(corner, size) {
		super();
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
		this.direction = direction || 270;  // 0 90 180 270
	}
}

class AlgArea extends Location {
	constructor() {
		super();
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
		for (a of this.inner) {
			a.rebase(move_by);
		}
		for (a of this.slots) {
			a.rebase(move_by);
		}
	}
	actualize_rect(padding) {  // recalc size and position
		// find children' bounds
		let bbox = new paper.Rectangle(this.corner, [0,0]);
		for (node of this.inner) {
			bbox = bbox.unite(node.bbox());
		}
		// furthermore, apply padding
		padding = padding || this.padding || new paper.Size(U * 0.5, 0);
		bbox = bbox.expand(padding);
		// move origin if required
		if (!this.corner.equals(bbox.topLeft)) {
			this.rebase(this.corner, bbox.topLeft);
		}
		// save the calculated size
		this.size = bbox.size;
	}
}

class TransitDiamond extends AlgArea {  // two slots vertically
	constructor(corner) {
		super();
		this.side = U * 0.1;
		// leave zero size -- ???
		// this.size = new paper.Size(this.side * 2, this.side * 2)
		this.slots = {
			90:  new Slot(this.corner.add([0, -this.side]),  90),
			270: new Slot(this.corner.add([0,  this.side]), 270),
		};
	}
	clone() {
		return new TransitDiamond(this.corner);
	}
}

class SequenceArea extends AlgArea {
	fit(alg_node) {
		const sep = U;
		const offset = new paper.Point(0, sep);
		let plug_point = this.corner;
		let node = null;

		/// add visual begin/end mark
		node = new TransitDiamond(plug_point)
		this.inner.push(node);
		// input of whole node
		let current_slot = node.slots[90].clone();
		this.slots[90] = last_slot;

		let last_slot = node.slots[270].clone();
		plug_point = plug_point.add(offset)

		// add all as vertial stack and align each by X coordinate
		for (st of alg_node.body) {
			node = create_alg_for(st);
			if (node) {
				const current_slot = node.slots[90];
				this.links.push(new Link(last_slot, current_slot));
				const top = current_slot.corner;
				node.rebase(plug_point, top);
				this.inner.push(node);
				last_slot = node.slots[270];
				const bottom = last_slot.corner;
				plug_point = bottom.add(offset);
			}
		}

		/// add visual begin/end mark
		node = new TransitDiamond(plug_point)
		this.inner.push(node);
		let current_slot = node.slots[90].clone();
		this.links.push(new Link(last_slot, current_slot));
		// const current_slot = new Slot(plug_point, 270);

		// output of whole node
		last_slot = node.slots[270].clone();
		this.slots[270] = last_slot;

		this.actualize_rect();
	}
}

class BoxArea extends AlgArea {
	fit(alg_node) {
		this.alg_node = alg_node;  // ???

		this.size = new paper.Size(U * 3, U * 2);

		// input of the  node
		let slot = new Slot([this.size.width/2, 0], 270);
		this.slots[270] = slot;

		// output of whole node
		slot = new Slot([this.size.width/2, this.size.height], 90);
		this.slots[90] = slot;

		//// this.actualize_rect();
	}
}


function create_alg_for(alg_node) {
	let a = null;
	if (alg_node.type == "sequence") {
		a = new SequenceArea();
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


// class Animal {
//   constructor(name) {
//     this.speed = 0;
//     this.name = name;
//   }








function on_load() {
	test();
}
