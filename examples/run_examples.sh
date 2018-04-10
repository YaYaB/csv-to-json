csv-to-json --csv 'football_world_cup_finals.csv' --json './example_0/football_world_cup_finals.json' --delimiter '_' 
csv-to-json --csv 'football_world_cup_finals.csv' --json './example_1/football_world_cup_finals.json' --delimiter '_' --per_line 
csv-to-json --csv 'football_world_cup_finals.csv' --json './example_2/football_world_cup_finals.json' --delimiter '_' --infer_types
csv-to-json --csv 'football_world_cup_finals.csv' --json './example_3/football_world_cup_finals.json' --delimiter '_' --max_docs 1 
csv-to-json --csv 'football_world_cup_finals.csv' --json './example_4/football_world_cup_finals.json' --delimiter '_' --keep 
csv-to-json --csv 'football_world_cup_finals.csv' --json './example_5/football_world_cup_finals.json' --delimiter '_' --config 'config.json'
csv-to-json --csv 'football_world_cup_finals.csv' --json './example_6/football_world_cup_finals.json' --delimiter '_' --config 'config_incorrect_type.json'
csv-to-json --csv 'football_world_cup_finals.csv' --json './example_7/football_world_cup_finals.json' --delimiter '_' --config 'config_incorrect_type_no_default.json'
csv-to-json --csv 'football_world_cup_finals.csv' --json './example_8/football_world_cup_finals.json' --delimiter '_' --config 'config_null_no_default.json'

