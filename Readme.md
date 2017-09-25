# Performance Tests Data Processor

## Purpouse

When working with performance tests you'll most probably require some input test data.
This might include user logins or any other business related information that need to drive your tests.

To be able to generate significant load on your application you'd like to have multiple machines with load generators.
E.g. in JMeter world this translates to single master controlling multiple slaves which execute test scenario.
 
Issues might arise when test data is not correctly shared between separate slaves.
E.g. it might not be desirable to reuse the same login on different machine. 
Or you can reuse the same set of test data but you'd like to have different _random_ order on each machine.

This small tool is meant to handle two types of issues: 

- protection between reusing test data across different load generation nodes 
- test data randomisation for each node
 
## Usage

    python process_input_data.py
    
Paths to data files to process stored in `input_files.json`

### Additioanal information

- Saves original files in separate files
- Determines separate test machines based on hostname pattern
- When data file is not found only warning is outputted to the user. Scripts continues execution
