def read_tle_file(file_path):

    tle_data = []
    current_entry = {}
    
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        
    for line in lines:
        line = line.strip()
        if not line:  # 跳过空行
            continue
            
        # 检查是否是标题行
        if line.startswith('NORAD ID:') or line.startswith('下载时间:') or line.startswith('数据来源:'):
            continue
        if line.startswith('==='):  # 分隔线
            continue
            
        # 检查是否是TLE行
        if line[0] == '1':
            current_entry = {'line1': line}
        elif line[0] == '2':
            current_entry['line2'] = line
            tle_data.append(current_entry)
            
    return tle_data

def parse_tle_line1(line1):
    """解析TLE的第一行"""
    return {
        'norad_id': line1[2:7].strip(),
        'classification': line1[7],
        'international_designator': line1[9:17].strip(),
        'epoch_year': line1[18:20],
        'epoch_day': line1[20:32],
        'mean_motion_dot': line1[33:43],
        'mean_motion_ddot': line1[44:52],
        'bstar': line1[53:61],
        'ephemeris_type': line1[62],
        'element_number': line1[64:68]
    }

def parse_tle_line2(line2):
    """解析TLE的第二行"""
    return {
        'inclination': line2[8:16],
        'raan': line2[17:25],
        'eccentricity': line2[26:33],
        'argument_of_perigee': line2[34:42],
        'mean_anomaly': line2[43:51],
        'mean_motion': line2[52:63],
        'revolution_number': line2[63:68]
    }


# 使用示例
file_path = './GraceFo_tle.txt'  # 替换为你的文件路径
tle_entries = read_tle_file(file_path)

# # 打印解析结果
# for i, entry in enumerate(tle_entries, 1):
#     print(f"TLE条目 {i}:")
#     print(entry['line1'])
#     print(entry['line2'])
#     print()
# # 使用扩展解析
# for entry in tle_entries:
#     line1_data = parse_tle_line1(entry['line1'])
#     line2_data = parse_tle_line2(entry['line2'])
#     print(f"NORAD ID: {line1_data['norad_id']}")
#     print(f"轨道倾角: {line2_data['inclination']} 度")
#     print(f"偏心率: {float(line2_data['eccentricity']) * 1e-7}")
#     print()

