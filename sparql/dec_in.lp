% make some input data for DEC
% run with DEC.lp


% Set length of timeline
#const maxstep=370.


% Declare fluents and events causing fluents to change

fluent(f0).
fluent(f1).
fluent(f2).
fluent(f3).
fluent(f4).
fluent(f5).
fluent(f6).
fluent(f7).
fluent(f8).
fluent(f9).
fluent(f10).
fluent(f11).
fluent(f12).
fluent(f13).
fluent(f14).
fluent(f15).
fluent(f16).
fluent(f17).
fluent(f18).
fluent(f19).
fluent(f20).
fluent(f21).
fluent(f22).
fluent(f23).
fluent(f24).
fluent(f25).
fluent(f26).
fluent(f27).
fluent(f28).
fluent(f29).
fluent(f30).
fluent(f31).
fluent(f32).
fluent(f33).
fluent(f34).
fluent(f35).
fluent(f36).
fluent(f37).
fluent(f38).
fluent(f39).
fluent(f40).
fluent(f41).
fluent(f42).
fluent(f43).
fluent(f44).
fluent(f45).
fluent(f46).
fluent(f47).
fluent(f48).
fluent(f49).
fluent(f50).
fluent(f51).
fluent(f52).
fluent(f53).
fluent(f54).
fluent(f55).
fluent(f56).
fluent(f57).
fluent(f58).
fluent(f59).
fluent(f60).
fluent(f61).
fluent(f62).
fluent(f63).
fluent(f64).
fluent(f65).
fluent(f66).
fluent(f67).
fluent(f68).
fluent(f69).
fluent(f70).
fluent(f71).
fluent(f72).
fluent(f73).

event(ev0).
event(ev1).
event(ev2).
event(ev3).
event(ev4).
event(ev5).
event(ev6).
event(ev7).
event(ev8).
event(ev9).
event(ev10).
event(ev11).
event(ev12).
event(ev13).
event(ev14).
event(ev15).
event(ev16).
event(ev17).
event(ev18).
event(ev19).
event(ev20).
event(ev21).
event(ev22).
event(ev23).
event(ev24).
event(ev25).
event(ev26).
event(ev27).
event(ev28).
event(ev29).
event(ev30).
event(ev31).
event(ev32).
event(ev33).
event(ev34).
event(ev35).
event(ev36).
event(ev37).
event(ev38).
event(ev39).
event(ev40).
event(ev41).
event(ev42).
event(ev43).
event(ev44).
event(ev45).
event(ev46).
event(ev47).
event(ev48).
event(ev49).
event(ev50).
event(ev51).
event(ev52).
event(ev53).
event(ev54).
event(ev55).
event(ev56).
event(ev57).
event(ev58).
event(ev59).
event(ev60).
event(ev61).
event(ev62).
event(ev63).
event(ev64).
event(ev65).
event(ev66).
event(ev67).
event(ev68).
event(ev69).
event(ev70).
event(ev71).
event(ev72).
event(ev73).
event(ev74).
event(ev75).
event(ev76).
event(ev77).
event(ev78).
event(ev79).
event(ev80).
event(ev81).
event(ev82).
event(ev83).
event(ev84).
event(ev85).
event(ev86).
event(ev87).
event(ev88).
event(ev89).
event(ev90).
event(ev91).


% Plug events to dependent fluents

initiates(ev0, f0).
terminates(ev91, f0).
initiates(ev1, f1).
terminates(ev90, f1).
initiates(ev2, f2).
terminates(ev89, f2).
initiates(ev3, f3).
terminates(ev88, f3).
initiates(ev4, f4).
terminates(ev87, f4).
initiates(ev5, f5).
terminates(ev86, f5).
initiates(ev6, f6).
terminates(ev85, f6).
initiates(ev7, f7).
terminates(ev84, f7).
initiates(ev8, f8).
terminates(ev83, f8).
initiates(ev9, f9).
terminates(ev82, f9).
initiates(ev10, f10).
terminates(ev81, f10).
initiates(ev11, f11).
terminates(ev80, f11).
initiates(ev12, f12).
terminates(ev79, f12).
initiates(ev13, f13).
terminates(ev78, f13).
initiates(ev14, f14).
terminates(ev77, f14).
initiates(ev15, f15).
terminates(ev76, f15).
initiates(ev16, f16).
terminates(ev75, f16).
initiates(ev17, f17).
terminates(ev74, f17).
initiates(ev18, f18).
terminates(ev73, f18).
initiates(ev19, f19).
terminates(ev72, f19).
initiates(ev20, f20).
terminates(ev71, f20).
initiates(ev21, f21).
terminates(ev70, f21).
initiates(ev22, f22).
terminates(ev69, f22).
initiates(ev23, f23).
terminates(ev68, f23).
initiates(ev24, f24).
terminates(ev67, f24).
initiates(ev25, f25).
terminates(ev66, f25).
initiates(ev26, f26).
terminates(ev65, f26).
initiates(ev27, f27).
terminates(ev64, f27).
initiates(ev28, f28).
terminates(ev63, f28).
initiates(ev29, f29).
terminates(ev62, f29).
initiates(ev30, f30).
terminates(ev61, f30).
initiates(ev31, f31).
terminates(ev60, f31).
initiates(ev32, f32).
terminates(ev59, f32).
initiates(ev33, f33).
terminates(ev58, f33).
initiates(ev34, f34).
terminates(ev57, f34).
initiates(ev35, f35).
terminates(ev56, f35).
initiates(ev36, f36).
terminates(ev55, f36).
initiates(ev37, f37).
terminates(ev54, f37).
initiates(ev38, f38).
terminates(ev53, f38).
initiates(ev39, f39).
terminates(ev52, f39).
initiates(ev40, f40).
terminates(ev51, f40).
initiates(ev41, f41).
terminates(ev50, f41).
initiates(ev42, f42).
terminates(ev49, f42).
initiates(ev43, f43).
terminates(ev48, f43).
initiates(ev44, f44).
terminates(ev47, f44).
initiates(ev45, f45).
terminates(ev46, f45).
initiates(ev46, f46).
terminates(ev45, f46).
initiates(ev47, f47).
terminates(ev44, f47).
initiates(ev48, f48).
terminates(ev43, f48).
initiates(ev49, f49).
terminates(ev42, f49).
initiates(ev50, f50).
terminates(ev41, f50).
initiates(ev51, f51).
terminates(ev40, f51).
initiates(ev52, f52).
terminates(ev39, f52).
initiates(ev53, f53).
terminates(ev38, f53).
initiates(ev54, f54).
terminates(ev37, f54).
initiates(ev55, f55).
terminates(ev36, f55).
initiates(ev56, f56).
terminates(ev35, f56).
initiates(ev57, f57).
terminates(ev34, f57).
initiates(ev58, f58).
terminates(ev33, f58).
initiates(ev59, f59).
terminates(ev32, f59).
initiates(ev60, f60).
terminates(ev31, f60).
initiates(ev61, f61).
terminates(ev30, f61).
initiates(ev62, f62).
terminates(ev29, f62).
initiates(ev63, f63).
terminates(ev28, f63).
initiates(ev64, f64).
terminates(ev27, f64).
initiates(ev65, f65).
terminates(ev26, f65).
initiates(ev66, f66).
terminates(ev25, f66).
initiates(ev67, f67).
terminates(ev24, f67).
initiates(ev68, f68).
terminates(ev23, f68).
initiates(ev69, f69).
terminates(ev22, f69).
initiates(ev70, f70).
terminates(ev21, f70).
initiates(ev71, f71).
terminates(ev20, f71).
initiates(ev72, f72).
terminates(ev19, f72).
initiates(ev73, f73).
terminates(ev18, f73).


	% Expand binary to trenary for each moment event happens
	initiates (E, F, T) :- initiates (E, F), happens(E, T).
	terminates(E, F, T) :- terminates(E, F), happens(E, T).



% Initial state of fluents

holdsAt(f1, 0).
holdsAt(f3, 0).
holdsAt(f5, 0).
holdsAt(f7, 0).
holdsAt(f9, 0).
holdsAt(f11, 0).
holdsAt(f13, 0).
holdsAt(f15, 0).
holdsAt(f17, 0).
holdsAt(f19, 0).
holdsAt(f21, 0).
holdsAt(f23, 0).
holdsAt(f25, 0).
holdsAt(f27, 0).
holdsAt(f29, 0).
holdsAt(f31, 0).
holdsAt(f33, 0).
holdsAt(f35, 0).
holdsAt(f37, 0).
holdsAt(f39, 0).
holdsAt(f41, 0).
holdsAt(f43, 0).
holdsAt(f45, 0).
holdsAt(f47, 0).
holdsAt(f49, 0).
holdsAt(f51, 0).
holdsAt(f53, 0).
holdsAt(f55, 0).
holdsAt(f57, 0).
holdsAt(f59, 0).
holdsAt(f61, 0).
holdsAt(f63, 0).
holdsAt(f65, 0).
holdsAt(f67, 0).
holdsAt(f69, 0).
holdsAt(f71, 0).
holdsAt(f73, 0).


% Moments when events occur

happens(ev0, 0).
happens(ev0, 192).
happens(ev0, 200).
happens(ev0, 204).
happens(ev0, 212).
happens(ev0, 216).
happens(ev0, 224).
happens(ev0, 252).
happens(ev0, 260).
happens(ev0, 272).
happens(ev0, 276).
happens(ev0, 296).
happens(ev0, 300).
happens(ev0, 312).
happens(ev0, 324).
happens(ev0, 332).
happens(ev0, 344).
happens(ev0, 356).
happens(ev0, 360).
happens(ev1, 1).
happens(ev1, 289).
happens(ev1, 301).
happens(ev1, 307).
happens(ev1, 319).
happens(ev1, 325).
happens(ev1, 337).
happens(ev2, 2).
happens(ev3, 3).
happens(ev4, 4).
happens(ev5, 5).
happens(ev6, 6).
happens(ev7, 7).
happens(ev8, 8).
happens(ev9, 9).
happens(ev9, 119).
happens(ev10, 10).
happens(ev11, 11).
happens(ev11, 141).
happens(ev11, 167).
happens(ev12, 12).
happens(ev13, 13).
happens(ev14, 14).
happens(ev15, 15).
happens(ev15, 117).
happens(ev15, 185).
happens(ev15, 219).
happens(ev15, 287).
happens(ev16, 16).
happens(ev17, 17).
happens(ev17, 93).
happens(ev17, 131).
happens(ev17, 207).
happens(ev17, 245).
happens(ev17, 321).
happens(ev17, 359).
happens(ev18, 18).
happens(ev19, 19).
happens(ev20, 20).
happens(ev20, 240).
happens(ev21, 21).
happens(ev21, 113).
happens(ev21, 159).
happens(ev21, 251).
happens(ev21, 297).
happens(ev22, 22).
happens(ev23, 23).
happens(ev23, 123).
happens(ev24, 24).
happens(ev24, 284).
happens(ev24, 336).
happens(ev25, 25).
happens(ev26, 26).
happens(ev27, 27).
happens(ev27, 143).
happens(ev27, 201).
happens(ev27, 317).
happens(ev28, 28).
happens(ev29, 29).
happens(ev29, 153).
happens(ev29, 215).
happens(ev29, 339).
happens(ev30, 30).
happens(ev31, 31).
happens(ev31, 97).
happens(ev31, 295).
happens(ev31, 361).
happens(ev32, 32).
happens(ev32, 236).
happens(ev33, 33).
happens(ev33, 103).
happens(ev33, 173).
happens(ev34, 34).
happens(ev35, 35).
happens(ev35, 109).
happens(ev35, 183).
happens(ev35, 257).
happens(ev35, 331).
happens(ev36, 36).
happens(ev36, 188).
happens(ev36, 264).
happens(ev37, 37).
happens(ev37, 115).
happens(ev37, 349).
happens(ev38, 38).
happens(ev39, 39).
happens(ev39, 121).
happens(ev39, 203).
happens(ev39, 285).
happens(ev39, 367).
happens(ev40, 40).
happens(ev41, 41).
happens(ev41, 127).
happens(ev41, 213).
happens(ev41, 299).
happens(ev42, 42).
happens(ev43, 43).
happens(ev43, 133).
happens(ev44, 44).
happens(ev44, 228).
happens(ev44, 320).
happens(ev45, 45).
happens(ev45, 92).
happens(ev45, 139).
happens(ev45, 186).
happens(ev45, 233).
happens(ev45, 280).
happens(ev45, 327).
happens(ev46, 46).
happens(ev46, 94).
happens(ev47, 47).
happens(ev47, 96).
happens(ev47, 145).
happens(ev47, 194).
happens(ev47, 243).
happens(ev47, 292).
happens(ev47, 341).
happens(ev48, 48).
happens(ev48, 98).
happens(ev48, 198).
happens(ev48, 248).
happens(ev49, 49).
happens(ev49, 100).
happens(ev49, 151).
happens(ev49, 304).
happens(ev49, 355).
happens(ev50, 50).
happens(ev50, 102).
happens(ev50, 206).
happens(ev51, 51).
happens(ev51, 104).
happens(ev51, 157).
happens(ev51, 210).
happens(ev51, 263).
happens(ev51, 316).
happens(ev51, 369).
happens(ev52, 52).
happens(ev52, 106).
happens(ev53, 53).
happens(ev53, 108).
happens(ev53, 163).
happens(ev53, 218).
happens(ev53, 273).
happens(ev54, 54).
happens(ev54, 110).
happens(ev54, 222).
happens(ev55, 55).
happens(ev55, 112).
happens(ev55, 169).
happens(ev55, 283).
happens(ev55, 340).
happens(ev56, 56).
happens(ev56, 114).
happens(ev56, 230).
happens(ev56, 288).
happens(ev57, 57).
happens(ev57, 116).
happens(ev57, 175).
happens(ev57, 234).
happens(ev57, 293).
happens(ev57, 352).
happens(ev58, 58).
happens(ev58, 118).
happens(ev59, 59).
happens(ev59, 120).
happens(ev59, 181).
happens(ev59, 242).
happens(ev59, 303).
happens(ev59, 364).
happens(ev60, 60).
happens(ev60, 122).
happens(ev60, 246).
happens(ev60, 308).
happens(ev61, 61).
happens(ev61, 124).
happens(ev61, 187).
happens(ev61, 313).
happens(ev62, 62).
happens(ev62, 126).
happens(ev62, 190).
happens(ev62, 254).
happens(ev63, 63).
happens(ev63, 128).
happens(ev63, 193).
happens(ev63, 258).
happens(ev63, 323).
happens(ev64, 64).
happens(ev64, 130).
happens(ev64, 196).
happens(ev64, 328).
happens(ev65, 65).
happens(ev65, 132).
happens(ev65, 199).
happens(ev65, 266).
happens(ev65, 333).
happens(ev66, 66).
happens(ev66, 134).
happens(ev66, 202).
happens(ev66, 270).
happens(ev67, 67).
happens(ev67, 136).
happens(ev67, 205).
happens(ev67, 343).
happens(ev68, 68).
happens(ev68, 138).
happens(ev68, 208).
happens(ev68, 278).
happens(ev68, 348).
happens(ev69, 69).
happens(ev69, 140).
happens(ev69, 211).
happens(ev69, 282).
happens(ev69, 353).
happens(ev70, 70).
happens(ev70, 142).
happens(ev70, 214).
happens(ev70, 286).
happens(ev71, 71).
happens(ev71, 144).
happens(ev71, 217).
happens(ev71, 290).
happens(ev71, 363).
happens(ev72, 72).
happens(ev72, 146).
happens(ev72, 220).
happens(ev72, 294).
happens(ev72, 368).
happens(ev73, 73).
happens(ev73, 148).
happens(ev73, 223).
happens(ev73, 298).
happens(ev74, 74).
happens(ev74, 150).
happens(ev74, 226).
happens(ev74, 302).
happens(ev75, 75).
happens(ev75, 152).
happens(ev75, 229).
happens(ev75, 306).
happens(ev76, 76).
happens(ev76, 154).
happens(ev76, 232).
happens(ev76, 310).
happens(ev77, 77).
happens(ev77, 156).
happens(ev77, 235).
happens(ev77, 314).
happens(ev78, 78).
happens(ev78, 158).
happens(ev78, 238).
happens(ev78, 318).
happens(ev79, 79).
happens(ev79, 160).
happens(ev79, 241).
happens(ev79, 322).
happens(ev80, 80).
happens(ev80, 162).
happens(ev80, 244).
happens(ev80, 326).
happens(ev81, 81).
happens(ev81, 164).
happens(ev81, 247).
happens(ev81, 330).
happens(ev82, 82).
happens(ev82, 166).
happens(ev82, 250).
happens(ev82, 334).
happens(ev83, 83).
happens(ev83, 168).
happens(ev83, 253).
happens(ev83, 338).
happens(ev84, 84).
happens(ev84, 170).
happens(ev84, 256).
happens(ev84, 342).
happens(ev85, 85).
happens(ev85, 172).
happens(ev85, 259).
happens(ev85, 346).
happens(ev86, 86).
happens(ev86, 174).
happens(ev86, 262).
happens(ev86, 350).
happens(ev87, 87).
happens(ev87, 176).
happens(ev87, 265).
happens(ev87, 354).
happens(ev88, 88).
happens(ev88, 178).
happens(ev88, 268).
happens(ev88, 358).
happens(ev89, 89).
happens(ev89, 180).
happens(ev89, 271).
happens(ev89, 362).
happens(ev90, 90).
happens(ev90, 182).
happens(ev90, 274).
happens(ev90, 366).
happens(ev91, 91).
happens(ev91, 184).
happens(ev91, 277).


#show holdsAt/2.
