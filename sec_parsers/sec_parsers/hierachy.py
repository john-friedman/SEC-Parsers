def assign_header_levels(headers,hierarchy_dict):
    levels = []
    previous_level = -1
    for header in headers:
        if header in hierarchy_dict:
            level = hierarchy_dict[header]
        else:
            level = previous_level + 1
            hierarchy_dict[header] = level
        
        levels.append(level)
        previous_level = level

    return levels