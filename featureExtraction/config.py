'''
black_white_list_use_mode:
- 'disabled' - ignore both lists, use all modules exist
- 'black' - black_list only, use all but in black_list;
- 'white' - white_list only, use modules only listed;
- 'both' - use both lists, use modules only listed in white but not in black;
'''
black_white_list_use_mode = 'disabled'
black_list = ['IpAdressScore']
white_list = ['IpAdressScore']

'''
run_level:
- 0 - call run() inside modules
- 1 - call run_aggr() inside modules, usually output more columns of features
'''
run_level = 1
