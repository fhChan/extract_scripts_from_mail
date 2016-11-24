import os, sys, re


class VBSConverter:
    """
    """

    def __init__(self, vbs_file, conversion_rules_path, js_file):
        self.vbs_file_ = vbs_file
        self.conversion_rules_path_ = conversion_rules_path
        self.conversion_rules_ = []
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
            line = line.strip().lower()
            if 'dim ' in line and ',' in line:
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
            # don't need to convert to lower again
            # line = line.strip().lower()
            if ':' in line:
                statements = line.split(':')
                for statement in statements:
                    output_lines.append(statement)
            else:
                output_lines.append(line)
        return output_lines

    def process_by_lines(self):
        lines = self.content_.split('\n')
        lines = self.process_variables(lines)
        lines = self.process_statement_separator(lines)
        self.content_ = '\n'.join(lines)

    def process_function_calling_return(self):
        # print "process_function_return"
        re_function_name = re.compile(r'(?:Function|Sub)[ \t]+(\w+)', re.IGNORECASE | re.MULTILINE)
        function_name_list = re.findall(re_function_name, self.content_)
        for func_name in function_name_list:
            self.content_ = re.sub(r'\b' + func_name + r'\b[ \t]*?=', 'ret_val = ', self.content_, 0,
                                   re.IGNORECASE | re.MULTILINE)
            self.content_ = re.sub(r'\b' + func_name + r'\b[ \t]*?(\w+.*)', func_name + r'(\1)', self.content_, 0,
                                   re.IGNORECASE | re.MULTILINE)

    def apply_conversion_rules(self):
        # ptn_list = [
        # # comments
        # (r'(^[^\"\'\r\n]*?)\'', r'\1//'),
        # # variables
        # (r'(DIM|CONST)\s+([^\r\n]*)', r'var \2'),
        # # functions
        # (r'^(\w*?)[ \t]*?(FUNCTION|SUB)[ \t]+([^\r\n]+)\r?\n', r'function \3 {\n'),
        # (r'END (FUNCTION|SUB|IF)', r'}'),
        # (r'function (\w+)([\s\S]*?)\1[ \t]*=([^}]+?)}', r'function \1\2return \3}'),
        # ##('^([ \t/]*)(?:function)[ \t]+([a-z][a-z0-9]*\)_(on[a-z0-9]+)', '\1\2.\3 = function'),
        # #(r'(IF\s+\S+\s*)=(\s*\S+\s+THEN)', r'\1==\2'),
        # # if statement
        # # if
        # (r'(\b)IF(\s+)?', r'\1if ('),
        # # then
        # (r'(\s+)THEN(\b)', r') {\2'),
        # # else
        # (r'(\b)ELSE(\b)', r'\1} else {\2'),
        # # else if
        # (r'(\b)ELSEIF(\s+)', r'\1} else if ('),
        # # end if
        # (r'(\b)ENDIF|END IF(\b)', r'\1}\2'),
        # # On Error
        # (r'On[ \t]+?Error[ \t]+?GoTo[ \t]+?(\w*)([\s\S]*)\1:', r'try { \2 } catch (err) {}'),
        # (r'Error[ \t]*(\d{1,5})', r'throw \1'),
        # # for statement
        # (r'For\s*((\w*)\s*=\s*\w*)\s*To\s*([^\r\n]*)\r?\n([\s\S]*?)NEXT',r'for (\1; \2 < \3; \2++) {\n\4}\n'),
        # (r'For\s+Each\s+(\w+?)\s+In\s+(\w+)([\s\S]*?)Next', r'for (\1 in \2) {\n\3 }\n'),
        # # remove keywords
        # (r'As (Boolean|Integer|String|Object)', r''),
        # (r'ByVal', r''),
        # (r'call ', r''),
        # (r'Exit Sub', r''),
        # ]
        # print ptn_list
        for matched, replaced in self.conversion_rules_:
            self.content_ = re.sub(matched, replaced, self.content_, 0, re.IGNORECASE | re.MULTILINE)

    def dump_to_js_file(self):
        fh = open(self.js_file_, 'w')
        fh.write(self.content_)
        fh.close()

    def convert(self):
        self.content_ = open(self.vbs_file_, 'r').read()
        self.load_conversion_rules()
        self.remove_module_class_name()
        self.process_by_lines()
        self.process_function_calling_return()
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
