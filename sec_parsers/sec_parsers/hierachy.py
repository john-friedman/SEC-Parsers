def assign_header_levels(headers, hierarchy_dict):
    levels = []
    previous_level = -1
    
    prev_header = None
    for header in headers:
        if header in hierarchy_dict:
            level = hierarchy_dict[header]
        elif prev_header is not None and prev_header == header:
            level = previous_level
        else:
            level = previous_level + 1
        
        levels.append(level)
        previous_level = level
        prev_header = header
    
    return levels