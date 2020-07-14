from time import sleep

from ctrlstrct_test import run_tests

def main():
    all_rules_ids = [
             "_s1", "_s2", "_s3", "_s4", "_s5", "_s6", "_s7", "_s8", "_s9", "_s10", 
             "_g1", "_g2", 
            ]
            
    # rule s1 constructs 'next' relation on top of given/inferred correct acts
    # rules s2..s5 construct 'next_sibling' relation (useful once on start)
    # rules s6..s10 construct acts' nesting relations on top of 'next' relation

    # rule g1 infers next FunctionBegin act
    # rule g2 infers next SequenceBegin act


    rules_turned_on = [
        # [],  # no one
        
        # # 'next_sibling' init only
        # ["_s2", ],
        # ["_s2", "_s3",  ],
        # ["_s2", "_s3", "_s4", ],
        # ["_s2", "_s3", "_s4", "_s5", ],
        
        # # 'next' relation on top of given
        # ["_s1", ],
        
        # # acts' nesting relations on top of 'next' relation
        # ["_s1", "_s6", ],
        # ["_s1", "_s6", "_s7", ],
        # ["_s1", "_s6", "_s7", "_s8", ],
        # ["_s1", "_s6", "_s7", "_s8", "_s9", ],
        # ["_s1", "_s6", "_s7", "_s8", "_s9", "_s10", ],
        
        
        # # generetive exclusively
        # ["_g1", ],
        # ["_g2", ],
        # ["_g1", "_g2", ],
        
        
        # with  all helpers
        # ["_s1", "_s2", "_s3", "_s4", "_s5", "_s6", "_s7", "_s8", "_s9", "_s10",  "_g1", ],
        # ["_s1", "_s2", "_s3", "_s4", "_s5", "_s6", "_s7", "_s8", "_s9", "_s10",  "_g2", ],
        ["_s1", "_s2", "_s3", "_s4", "_s5", "_s6", "_s7", "_s8", "_s9", "_s10",  "_g1", "_g2", ],
        
        
    ]


    persistent_kwargs = {
        "extra_act_entries": 0,
        "reasoning": "stardog",
    }


    # time_results

    # extra_act_entries=0, rules_filter=None, reasoning=None, on_done=None
    
    ### Debug!
    # rules_turned_on = rules_turned_on[:2]
    
    log2file("\n===============\nStarting...\n\n")
    
    for rule_set in rules_turned_on:
        
        def rules_filter(name):
            return name.endswith(tuple(rule_set))
            
        def on_done(seconds):
            log2file("%s:\n  %f seconds" % (str(rule_set), seconds))
            sleep(5)
            
        run_tests(process_kwargs=dict(rules_filter=rules_filter, on_done=on_done, **persistent_kwargs))
    
    
    log2file("\n\nCompleted.\n===============\n")
            
        
def log2file(s, filepath="./separate_run.log"):
    with open(filepath, "a") as f:
        f.write(s)
        f.write('\n')
        


if __name__ == '__main__':
    main()
