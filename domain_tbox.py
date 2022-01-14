# domain_tbox.py

raise 'TODO: check status of domain_tbox.py ...'

def init_persistent_structure(onto, complete_vocabulary_mode=True):
    # types.new_class(temp_name, (domain >> range_, ))  # , Property

    skos = onto.get_namespace("http://www.w3.org/2004/02/skos/core#")

    with onto:
        # Статические определения

        if complete_vocabulary_mode:
            # skos:Concept
            class Concept(Thing):
                namespace = skos
        else:
            Concept = Thing

        # class related_to_concept(DatatypeProperty): pass

        # новое свойство id
        if not onto["id"]:
            id_prop = types.new_class("id", (Thing >> int, FunctionalProperty, ))
        # ->
        class act(Concept): pass
        # -->
        class act_begin(act): pass
        # --->
        class trace(act_begin): pass
        # -->
        class act_end(act): pass
        # # -->
        # class student_act(act): pass
        # -->
        class correct_act(act): pass
        # # -->
        class normal_flow_correct_act(correct_act): pass
        # hide so far
        # class breaking_flow_correct_act(correct_act): pass
        # AllDisjoint([
        #   normal_flow_correct_act,
        #   breaking_flow_correct_act
        # ])

        # ->
        class linked_list(Thing): pass

        # ->
        class action(Concept): pass
        class algorithm(Concept): pass

        class entry_point(algorithm >> action, FunctionalProperty): pass

        ##### Граф между действиями алгоритма
        class boundary(Thing): pass  # begin or end of an action
        class boundary_of(boundary >> action, FunctionalProperty): pass
        class begin_of(boundary_of): pass
        class   end_of(boundary_of): pass
        # class statement_begin(Thing): pass
        # class statement_end  (Thing): pass

        # hide so far
        # class hide_boundaries(action):
        #     """tells a complex action no to show (to skip) begin/end acts in not-collapsed mode."""
        #     pass

        # helper
        class gathered_child_exec_till(act >> act): pass
        # helper
        class gather_child_exec_till(gathered_child_exec_till): pass
        # helper
        class child_executes(act >> boundary): pass

        # новое свойство consequent - ребро графа переходов, заменяющего правильную трассу
        class consequent(Thing >> Thing, ): pass

        # class verbose_consequent(consequent): pass
        # class visible_consequent(consequent): pass

        # окрестность - ближайшее будушее, до условия
        class has_upcoming(boundary >> boundary, TransitiveProperty): pass

        # class interrupting_consequent(consequent): pass
        # + subclasses
        class normal_consequent(consequent): pass
        class always_consequent(normal_consequent, has_upcoming): pass
        class on_true_consequent(normal_consequent): pass
        class on_false_consequent(normal_consequent): pass
        ##### Граф связей между действиями алгоритма


        # ->
        class sequence(action): pass

        # признак first
        class first_item(Thing, ): pass
        # признак last
        class last_item(Thing, ): pass
        # индекс в списке
        class item_index(Thing >> int, FunctionalProperty): pass

        # ->
        class loop(action): pass

        if loop:  # hide a block under code folding
            # classes that regulate the use of condition in a loop

            # normal condition effect (false->stop, true->start a body) like in while, do-while, for loop types
            class conditional_loop(loop): pass

            # no condition at all: infinite loop like while(true){...}. The only act endlessly executed is the loop body.
            class unconditional_loop(loop): pass
            # # inverse condition effect (false->start a body, true->stop) like in do-until loop
            # inverse_conditional_loop = types.new_class("inverse_conditional_loop", (loop,))

            # The constraint is not useful so far
            # AllDisjoint([conditional_loop, unconditional_loop])

            class infinite_loop(unconditional_loop): pass
            class ntimes_loop(unconditional_loop): pass


            # classes that regulate a loop execution start (which act should be first)
            #
            # start with cond
            class start_with_cond(conditional_loop): pass
            # start with body
            class start_with_body(loop): pass
            # start with init
            class start_with_init(conditional_loop): pass

            # The constraint is not useful so far
            # AllDisjoint([start_with_cond, start_with_body, start_with_init])


            # classes that regulate the use of "update" step in a for-like loop (both subclasses of "loop_with_initialization" as that loop have "update" step too)
            #
            # update first, then the body, like in foreach loop type
            class pre_update_loop(conditional_loop): pass
            # body first, then the update, like in for(;;) loop type
            class post_update_loop(conditional_loop): pass

            AllDisjoint([pre_update_loop, post_update_loop])


            # classes that indicate whether condition and body follow each other instantly or not (note that: these classes are not disjointed; these classes are to be inferred from another defined features via equivalent_to definition so no direct inheritance required for known loops)
            # class body_then_cond(loop):
            #     equivalent_to = [inverse_conditional_loop | (conditional_loop & (Not(post_update_loop)))]
            # class cond_then_body(loop):
            #     equivalent_to = [conditional_loop & (Not(pre_update_loop))]

            # workaround: do not use the inference, declare explicitly
            class cond_then_body(conditional_loop): pass
            class body_then_cond(conditional_loop): pass

            # classes that define well-known loops as subclasses of the above defined loop-feature classes. These classes are to be used publicly
            class while_loop(start_with_cond): pass
            while_loop.is_a += [cond_then_body, body_then_cond]  # workaround

            class do_while_loop(start_with_body): pass
            do_while_loop.is_a += [cond_then_body, body_then_cond]  # workaround

            # class do_until_loop(inverse_conditional_loop, postconditional_loop): pass
            # do_until_loop.is_a += [body_then_cond]  # workaround

            class for_loop(post_update_loop, start_with_init): pass
            for_loop.is_a += [cond_then_body]  # workaround

            class foreach_loop(pre_update_loop, start_with_cond): pass
            foreach_loop.is_a += [body_then_cond]  # workaround



        # -->
        class alt_branch(sequence): pass
        class func(action): pass
        # class func(sequence): pass
        class alternative(action): pass

        # # make algorithm elements classes
        # for class_name in [
        #     "alternative",
        # ]:
        #     types.new_class(class_name, (action,))

        for class_name in [
            "expr", "stmt",
        ]:
            types.new_class(class_name, (action, ))  ### hide_boundaries

        for class_name in [
            "if", "else-if", "else",
        ]:
            types.new_class(class_name, (alt_branch,))

        # make some properties
        for prop_name in ("body", "cond", "init", "update", "wrong_next_act", ):
            if not onto[prop_name]:
                types.new_class(prop_name, (Thing >> Thing,))

        # новое свойство executes
        prop_executes = types.new_class("executes", (Thing >> Thing, FunctionalProperty, ))
        class executes_id(act >> int, FunctionalProperty): pass

        # новое свойство expr_value
        prop_expr_value = types.new_class("expr_value", (DataProperty, FunctionalProperty, ))

        # новое свойство stmt_name
        prop_stmt_name = types.new_class("stmt_name", (Thing >> str, DataProperty, FunctionalProperty))

        # новое свойство next
        types.new_class("next", (Thing >> Thing, ))
        types.new_class("next_act", (correct_act >> correct_act, FunctionalProperty, InverseFunctionalProperty))

        # новое свойство student_next
        types.new_class("student_next", (act >> Thing, ))
        types.new_class("student_next_latest", (act >> act, onto.student_next))

        # новое свойство next_sibling -- связывает акты, соседние по номеру раза выполнения (причём, начальные и конечные акты - раздельно)
        next_sibling = types.new_class("next_sibling", (Thing >> Thing, ))

        # новое свойство before
        # prop_before = types.new_class("before", (Thing >> Thing, TransitiveProperty))

        # новое свойство in_trace
        prop_in_trace = types.new_class("in_trace", (act >> trace, ))

        # свойство index
        types.new_class("index", (Thing >> int, FunctionalProperty, ))
        types.new_class("student_index", (Thing >> int, FunctionalProperty, ))
        # номер итерации
        types.new_class("student_iteration_n", (act >> int, FunctionalProperty, ))
        types.new_class("iteration_n", (act >> int, FunctionalProperty, ))

        types.new_class("after_act", (Thing >> act, ))

        # новое свойство exec_time
        prop_exec_time = types.new_class("exec_time", (Thing >> int, FunctionalProperty, ))
        # новое свойство depth
        class depth(Thing >> int, FunctionalProperty, ): pass
        # # новое свойство correct_depth
        # prop_correct_depth = types.new_class("correct_depth", (Thing >> int, FunctionalProperty, ))

        # новое свойство text_line
        prop_text_line = types.new_class("text_line", (Thing >> int, FunctionalProperty, ))

        # prop_has_student_act = types.new_class("has_student_act", (Thing >> act, ))
        # prop_has_correct_act = types.new_class("has_correct_act", (Thing >> act, ))
        # # новое свойство same_level
        # prop_same_level = types.new_class("same_level", (Thing >> Thing, SymmetricProperty))
        # # новое свойство child_level
        # prop_child_level = types.new_class("child_level", (Thing >> Thing, SymmetricProperty))

        # make string_placeholder properties
        class string_placeholder(Thing >> str): pass
        for suffix in (
            "A", # "B", "C", "D", "EX",
            "kind_of_loop", "TrueFalse",
            "BEGIN",  # для CorrespondingEndMismatched
            "EXTRA",  # для NotNeighbour
            "MISSING",  # пропущены перед текущим
            "COND",     # любое условие (общий случай)
            "INNER",    # для CorrespondingEndMismatched: несоответствующее начало, которое явл. вложенным действием несоответствующего конца
            "CONTEXT",    # (неверный) родитель (по трассе)
            "PARENT",   # верный родитель
            "PREVIOUS", # TooLateInSequence: тот, что должен быть после, но он перед текущим
            "LOOP",
            "LOOP_COND",
            "ALT",
            "ALT_COND", # любое из условий (перечисляет все условия)
            "CURRENT_ALT_COND", # текущее условие
            # "PREV_ALT_COND",
            "LATEST_ALT_COND", # выполн. последним, но не текущее условие
            "EXPECTED_ALT_COND", # ожидаемое, но отсутствующее
            "REQUIRED_COND", # условие, которое не вычислено
            "UNEXPECTED_ALT_COND", # не ожидаемое, но присутствующее
            "BRANCH",  # уже выполнилась
            "BRANCH2",
            "EXPECTED_BRANCH", "UNEXPECTED_BRANCH",
            # "ELSE_BRANCH", # "BRANCHES"
            "SEQ",
            "NEXT",
            "NEXT_COND",
        ):
            prop_name = "field_" + suffix
            if not onto[prop_name]:
                types.new_class(prop_name, (string_placeholder, ))

        class fetch_kind_of_loop(act >> action, ): pass
        class reason_kind(boundary >> Thing, ): pass
        class to_reason(Thing >> Thing, ): pass
        class from_reason(Thing >> Thing, ): pass

        # новое свойство corresponding_end
        class corresponding_end(act_begin >> act_end, ): pass
        class student_corresponding_end(act_begin >> act_end, ): pass

        class hasPartTransitive(Thing >> Thing, TransitiveProperty): pass
        # новое свойство parent_of
        # class parent_of(act_begin >> act, InverseFunctionalProperty): pass
        class parent_of(hasPartTransitive, InverseFunctionalProperty): pass
        class student_parent_of(Thing >> Thing, InverseFunctionalProperty): pass

        class branches_item(parent_of): pass
        class body(parent_of): pass
        class body_item(parent_of): pass

        # объекты, спровоцировавшие ошибку
        if not onto["Erroneous"]:
            Erroneous = types.new_class("Erroneous", (Thing,))

            # category2priority = None  # declare it later
            # class error_priority(Thing >> int): pass

            # make Erroneous subclasses
            # (class, [bases])
            for class_spec in [
                # (name, [bases], err_level, {related, concepts})

                # Sequence mistakes ...
                ("CorrespondingEndMismatched", (), "trace_structure", {'action'}),
                ("WrongNext", (), "general_wrong", {'action'}),

                # "CorrespondingEndPerformedDifferentTime",
                # "WrongExecTime",
                # "ActStartsAfterItsEnd", "ActEndsWithoutStart",
                # "AfterTraceEnd",
                # "DuplicateActInSequence",
                ("ConditionMisuse", ["WrongNext"], "general_wrong", {'expr'}),

                ("WrongContext", (), "wrong_context", {'action'}),
                # ("MisplacedBefore", ["WrongContext"]),
                # ("MisplacedAfter", ["WrongContext"]),
                ("MisplacedDeeper", ["WrongContext"], "wrong_context", {'action'}),
                ("EndedDeeper", ["WrongContext", ], "wrong_context", {'action'}),  # +
                ("EndedShallower", ["WrongContext", "CorrespondingEndMismatched"], "wrong_context", {'action'}), # не возникнет для первой ошибки в трассе.
                ("OneLevelShallower", ["WrongContext"], "concrete_wrong_context", {'action'}), # +

                ("NeighbourhoodError", ["WrongNext"], "general_wrong", {'action'}),  # check that one of the following is determined
                ("UpcomingNeighbour", ["NeighbourhoodError"], "missing", {'action'}), #
                ("NotNeighbour", ["NeighbourhoodError"], "extra", {'action'}), # disjoint with UpcomingNeighbour
                ("WrongCondNeighbour", ["NotNeighbour", "ConditionMisuse"], "by_different_cond", {'action'}), #

                # ("ExtraAct", ["WrongNext"]),
                ("DuplicateOfAct", [], "extra", {'sequence'}),
                # "MissingAct",
                # "TooEarly", # right after missing acts
                # ("DisplacedAct", ["TooEarly","ExtraAct","MissingAct"]), # act was moved somewhere
                ("TooLateInSequence", ["WrongNext"], "extra", {'sequence'}), # +
                ("TooEarlyInSequence", ["WrongNext"], "missing", {'sequence'}), # +
                ("SequenceFinishedNotInOrder", (), "extra", {'sequence'}),  # выполнены все действия, но в конце не последнее; не возникнет для первой ошибки в трассе.
                ("SequenceFinishedTooEarly", ["SequenceFinishedNotInOrder"], "missing", {'sequence'}), # +

                # Alternatives mistakes ...
                ("NoFirstCondition", (), "missing", {'alternative', 'if', 'expr'}), # +
                ("NoAlternativeEndAfterBranch", (), "missing", {'alternative', 'alt_branch'}), # +
                ("CondtionNotNextToPrevCondition", (), "extra", {'alternative', 'else-if', 'expr'}), # +
                ("ConditionAfterBranch", ["NoAlternativeEndAfterBranch", "CondtionNotNextToPrevCondition"], "extra", {'alternative', 'alt_branch', 'expr'}), # ~
                ("DuplicateOfCondition", ["CondtionNotNextToPrevCondition", "ConditionAfterBranch"], "extra", {'alternative', 'if', 'else-if', 'expr'}),  # +
                # ("WrongBranch", ["ExtraAct"]),
                ("BranchOfFalseCondition", ["ConditionMisuse"], "by_different_cond", {'alternative', 'alt_branch', 'expr'}),
                ("AnotherExtraBranch", ["NoAlternativeEndAfterBranch"], "extra", {'alternative', 'alt_branch'}), # +
                ("BranchWithoutCondition", (), "extra", {'alternative', 'alt_branch', 'expr'}), # +
                ("BranchNotNextToCondition", ["BranchWithoutCondition"], "missing", {'alternative', 'alt_branch', 'expr'}), # +
                ("ElseBranchNotNextToLastCondition", ["BranchWithoutCondition"], "extra", {'alternative', 'alt_branch', 'else', 'expr'}), # +
                ("ElseBranchAfterTrueCondition", ["BranchWithoutCondition", "ElseBranchNotNextToLastCondition", "ConditionMisuse"], "by_different_cond", {'alternative', 'alt_branch', 'else', 'expr'}), # ~
                ("NoBranchWhenConditionIsTrue", ["ConditionMisuse"], "by_different_cond", {'alternative', 'alt_branch', 'expr'}), # +
                ("LastConditionIsFalseButNoElse", (), "missing", {'alternative', 'alt_branch', 'else', 'expr'}), # +
                ("NoNextCondition", (), "missing", {'alternative', 'expr'}), # ~
                ("ConditionTooLate", ["NoNextCondition", "CondtionNotNextToPrevCondition"], "extra", {'alternative', 'expr'}), # - skip for now
                ("ConditionTooEarly", ["NoFirstCondition", "NoNextCondition", "CondtionNotNextToPrevCondition"], "extra", {'alternative', 'expr'}), # +
                ("LastFalseNoEnd", (), "missing", {'alternative', 'expr'}), # +
                ("AlternativeEndAfterTrueCondition", ["ConditionMisuse"], "by_different_cond", {'alternative', 'alt_branch', 'expr'}),  # +

                # Loops mistakes ...
                # a general Loop
                ("NoLoopEndAfterFailedCondition", (), "missing", {'loop', 'expr'}),  # +
                ("LoopContinuedAfterFailedCondition", ["NoLoopEndAfterFailedCondition", "ConditionMisuse"], "by_different_cond", {'loop', 'expr'}), # +
                ("IterationAfterFailedCondition", ["LoopContinuedAfterFailedCondition"], "extra", {'loop', 'expr'}), # +
                ("LoopEndsWithoutCondition", (), "extra", {'loop', 'expr'}),  # +
                # start_with_cond
                ("LoopStartIsNotCondition", (), "missing", {'while_loop', 'expr'}), # +
                # start_with_body
                ("LoopStartIsNotIteration", (), "missing", {'do_while_loop'}), # +
                # cond_then_body (-> true)
                ("NoIterationAfterSuccessfulCondition", (), "missing", {'while_loop', 'do_while_loop', 'for_loop', 'expr'}),  # +
                ("LoopEndAfterSuccessfulCondition", ["NoIterationAfterSuccessfulCondition", "ConditionMisuse"], "by_different_cond", {'while_loop', 'do_while_loop', 'for_loop', 'expr'}), # +
                # body_then_cond
                ("NoConditionAfterIteration", (), "missing", {'while_loop', 'do_while_loop', 'expr'}), # +
                ("NoConditionBetweenIterations", ["NoConditionAfterIteration"], "missing", {'while_loop', 'do_while_loop', 'expr'}), # +
                # ForLoop
                ("LoopStartsNotWithInit", (), "missing", {'for_loop', }),
                ("InitNotAtLoopStart", (), "extra", {'for_loop', }),
                ("NoConditionAfterForInit", (), "missing", {'for_loop', 'expr'}),
                ("IterationAfterForInit", ["NoConditionAfterForInit"], "extra", {'for_loop', }),
                ("NoUpdateAfterIteration", (), "missing", {'for_loop', }),
                ("UpdateNotAfterIteration", (), "extra", {'for_loop', }),
                ("ForConditionAfterIteration", ["UpdateNotAfterIteration"], "extra", {'for_loop', 'expr'}),
                ("NoConditionAfterForUpdate", (), "missing", {'for_loop', }),
                # ForeachLoop
                ("NoForeachUpdateAfterSuccessfulCondition", (), "missing", {'foreach_loop', }),
                ("ForeachUpdateNotAfterSuccessfulCondition", (), "extra", {'foreach_loop', }),
                ("NoIterationAfterForeachUpdate", (), "missing", {'foreach_loop', }),
                ("IterationNotAfterForeachUpdate", (), "extra", {'foreach_loop', }),
            ]:
                if isinstance(class_spec, str):
                    types.new_class(class_spec, (Erroneous,))
                elif isinstance(class_spec, tuple):
                    class_name, base_names = class_spec[:2]
                    bases = tuple((onto[base_name] if type(base_name) is str else base_name) for base_name in base_names)
                    # print(bases)
                    created_class = types.new_class(class_name, bases or (Erroneous,))
                    related_concepts = class_spec[3]
                    if complete_vocabulary_mode:
                        for related_concept in related_concepts:
                            # make a new subclass of both mistake and concept
                            types.new_class(class_name + '_related_to_' + related_concept, (created_class, onto[related_concept]))
                            ### make_triple(created_class, related_to_concept, related_concept)

                    # if len(class_spec) >= 3:
                    #     category = class_spec[2]
                    #     if not category2priority:
                    #         category2priority = {n:i for i,n in enumerate([
                    #             "trace_structure",
                    #             "general_wrong",
                    #             "wrong_context",
                    #             "concrete_wrong_context",
                    #             "extra",
                    #             "by_different_cond",
                    #             "missing",
                    #             # "",
                    #         ])}
                    # assert category in category2priority, (category, class_name)
                    # priority = category2priority[category]
                    # # set error_priority
                    # ## ??????
                    # make_triple(created_class, error_priority, priority)


        for prop_name in ("precursor", "cause", "has_causing_condition", "should_be", "should_be_before", "should_be_after", "context_should_be"):
            if not onto[prop_name]:
                types.new_class(prop_name, (onto["Erroneous"] >> Thing,))

        # make consequent subproperties (always_consequent is default base)
        for class_spec in [
            # "DebugObj",
            # "FunctionBegin",
            # "FunctionEnd",
            # "FunctionBodyBegin",
            "StmtEnd",
            "ExprEnd",
            "GlobalCodeBegin",
            "SequenceBegin",
            "SequenceNext",
            "SequenceEnd",
            "AltBegin",  # 1st condition
            ("AltBranchBegin", on_true_consequent),
            ("NextAltCondition", on_false_consequent),
            ("AltElseBranchBegin", on_false_consequent),
            ("AltEndAllFalse", on_false_consequent),
            "AltEndAfterBranch",
            "PreCondLoopBegin",
            "PostCondLoopBegin",
            ("IterationBeginOnTrueCond", on_true_consequent),
            # "IterationBeginOnFalseCond",
            # ("LoopUpdateOnTrueCond", on_true_consequent),
            # "LoopBodyAfterUpdate",
            ("LoopEndOnFalseCond", on_false_consequent),
            # "LoopEndOnTrueCond",  # no rule yet?
            "LoopCondBeginAfterIteration",
            # "LoopWithInitBegin",
            # "LoopCondBeginAfterInit",
            # "LoopUpdateAfterIteration",
            # "LoopCondAfterUpdate",
        ]:
            # types.new_class(class_name, (correct_act,))
            if isinstance(class_spec, str):
                types.new_class(class_spec, (always_consequent,))
            elif isinstance(class_spec, tuple):
                class_name, base_names = class_spec[:2]
                bases = tuple((onto[base_name] if type(base_name) is str else base_name) for base_name in [base_names])
                # print(bases)
                created_class = types.new_class(class_name, bases or (always_consequent,))

        for prop_name in ("reason", ):  # for correct acts !
            if not onto[prop_name]:
                types.new_class(prop_name, (correct_act >> Thing,))

