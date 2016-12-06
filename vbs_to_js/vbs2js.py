import os, sys, re


class VBSConverter:
    """
    """

    def __init__(self, vbs_file, conversion_rules_path, js_file):
        self.vbs_file_ = vbs_file
        self.conversion_rules_path_ = conversion_rules_path
        self.conversion_rules_ = []
        self.array_name_list_ = []
        self.function_name_list_ = []
        self.js_file_ = js_file
        self.re_module_name_ = re.compile(r'VBA MACRO (\w*?)\.', re.IGNORECASE | re.MULTILINE)

    def load_conversion_rules(self):
        with open(self.conversion_rules_path_) as fh:
            for line in fh.readlines():
                if line.startswith('//') or len(line.strip()) == 0:
                    continue
                else:
                    matched, replaced = line.split('-->')
                    self.conversion_rules_.append((matched.strip(), replaced.strip()))

    def remove_module_class_name(self):
        name_list = re.findall(self.re_module_name_, self.content_)
        # print name_list
        for item in name_list:
            self.content_ = re.sub(item + '\\.', '', self.content_, 0, re.IGNORECASE | re.MULTILINE)

    def process_variables(self, lines):
        output_lines = []
        for line in lines:
            line = line.strip()
            if ('dim ' in line or 'const ' in line) and ',' in line:
                vars = line.split(',')
                output_lines.append(vars[0])
                for var in vars[1:]:
                    output_lines.append('dim ' + var)
            else:
                output_lines.append(line)
        return output_lines
    def process_statement_separator(self, lines):
        output_lines = []
        for line in lines:
            if ':' in line:
                if ("'" in line) or (re.match(r'^\s*\w+:', line)) or (re.match(r'"[^"]*:[^"]*"', line)):
                    output_lines.append(line)
                else:
                    statements = line.split(':')
                    for statement in statements:
                        output_lines.append(statement)
            else:
                output_lines.append(line)
        return output_lines

    def find_key(self, line, key_list):
        matched_key_list = []
        for array_name in key_list:
            if array_name in line:
                matched_key_list.append(array_name)
        return matched_key_list

    def get_bracket_dict(self, line):
        bracket_ops_stack = []
        bracket_dict = {}

        length_of_line = len(line)
        for i in xrange(length_of_line):
            each_char = line[i]
            if each_char == '(':
                bracket_ops_stack.append(i)
            elif each_char == ')':
                id = bracket_ops_stack.pop()
                bracket_dict[id] = i
        
        if len(bracket_ops_stack) != 0:
            print line
            print "left_bracket_count is not equal to right_bracket_count"
            return False
        else:
            return bracket_dict

    def process_array_op(self, lines):
        output_lines = []
        for line in lines:
            if 'dim ' in line:
                matched = re.search(r'(\w+)\(.*\)', line, re.IGNORECASE)
                if matched != None:
                    array_name = matched.group(1)
                    self.array_name_list_.append(array_name)
                    output_lines.append(line)
                    continue
            matched_array_name_list = self.find_key(line, self.array_name_list_)
            if len(matched_array_name_list) > 0:
                bracket_dict = self.get_bracket_dict(line)
                str_list = list(line)
                for array_name in matched_array_name_list:
                    pattern = array_name + r'\s*\('
                    for m in re.finditer(pattern, line):
                        match_str = m.group()
                        left_bracket_index = m.start() + len(match_str) - 1
                        str_list[left_bracket_index] = '['
                        str_list[bracket_dict[left_bracket_index]] = ']'
                output_lines.append(''.join(str_list))
            else:
                output_lines.append(line)
        return output_lines

    def find_all_function_name(self):
        re_function_name = re.compile(r'(?:Function|Sub)[ \t]+(\w+)', re.IGNORECASE | re.MULTILINE)
        self.function_name_list_ = re.findall(re_function_name, self.content_)

    def process_array_in_function_params(self, func_name, line):
        matched = re.search(r'(.*)(function|sub)[ \t]*?\b' + func_name + r'\b[ \t]*?\((.+)\)(.*)', line, re.IGNORECASE)
        if matched != None:
            params = matched.group(3).split(',')
            new_params = []
            for param in params:
                param_matched = re.search(r'\b(\w+)\b[ \t]*?\((.*)\).*', param.strip(), re.IGNORECASE)
                if param_matched != None:
                    new_params.append(param_matched.group(1))
                else:
                    new_params.append(param)
            line = matched.group(1) + matched.group(2) + ' ' + func_name + '(' + ', '.join(new_params) + ')' + matched.group(4)
        return line
    def process_function_op(self, lines):
        output_lines = []
        for line in lines:
            matched_func_name_list = self.find_key(line, self.function_name_list_)
            if len(matched_func_name_list) > 0:
                for matched_func_name in matched_func_name_list:
                    if None != re.search(r'\b' + matched_func_name + r'\b[ \t]*?=', line, re.IGNORECASE):
                        line = re.sub(r'(.*?)\b' + matched_func_name + r'\b[ \t]*?=(.*)', r'\1ret_val = \2', line)
                    elif None != re.search(r'\b' + matched_func_name + r'\b[ \t]*?\w+', line, re.IGNORECASE):
                        line = re.sub(r'(.*?)\b' + matched_func_name + r'\b[ \t]*?(\w+.*)', r'\1'+matched_func_name + r'(\2)', line)
                    else:
                        line = self.process_array_in_function_params(matched_func_name, line)
            output_lines.append(line)
        return output_lines

    def process_by_lines(self):
        lines = self.content_.split('\n')
        lines = self.process_variables(lines)
        lines = self.process_array_op(lines)
        lines = self.process_statement_separator(lines)
        self.content_ = '\n'.join(lines)
        self.find_all_function_name()
        lines = self.process_function_op(lines)
        self.content_ = '\n'.join(lines)

    def apply_conversion_rules(self):
        for matched, replaced in self.conversion_rules_:
            self.content_ = re.sub(matched, replaced, self.content_, 0, re.IGNORECASE | re.MULTILINE)

    def dump_to_js_file(self):
        fh = open(self.js_file_, 'w')
        fh.write(self.content_)
        fh.close()

    def convert(self):
        self.content_ = open(self.vbs_file_, 'r').read().lower()
        self.load_conversion_rules()
        self.remove_module_class_name()
        self.process_by_lines()
        self.apply_conversion_rules()
        self.dump_to_js_file()

def print_help():
    print """
Usage:
    python vbs2js.py input_vbs_file input_conversion_rules_file output_js_file
    """

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print_help()
        exit(-1)
    converter = VBSConverter(sys.argv[1], sys.argv[2], sys.argv[3])
    converter.convert()
