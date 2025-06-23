def parse_config(cfg_file_name):
    with open(cfg_file_name) as f:
        lines = [line.rstrip() for line in f]
        lines = [line for line in lines if (line and '#' not in line)]

    config = {}
    for line in lines:
      # print(line.replace(" ",""))
      conf_line = line.replace(" ","").split('=')
      config[conf_line[0]] = conf_line[1]
    return config