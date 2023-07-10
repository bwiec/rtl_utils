import sys
import math

class module_parser:
    _properties = {
        "module_name" : [],
        "parameters" : [],
        "ordered_signals" : [],
        "inputs" : [],
        "outputs" : [],
        "inouts" : [],
        "input_clocks" : []
    }
    _state = "MODULE"
    _file = ""
    _fid = ""
    _cur_line = ""
    _cur_line_idx = 0

    def __init__(self, file):
        self._file = file
        self._properties["module_name"] = []
        self._properties["parameters"] = []
        self._properties["ordered_signals"] = []
        self._properties["inputs"] = []
        self._properties["outputs"] = []
        self._properties["inouts"] = []
        self._properties["input_clocks"] = []
        self.__parse_input_file()
        self.__get_input_clocks()
        
    def __parse_input_file(self):
        self._fid = open(self._file, 'r')
        for line in self._fid:
            self._cur_line_idx = self._cur_line_idx + 1
            self._cur_line = line.lstrip().rstrip()
            if self._cur_line == '' or self.__line_is_comment() or self.__line_is_macro():
                continue
            self.__parse_this_line()
            if self._state == "DONE":
                return

        self._fid.close()
        sys.exit("Reached the end of the file while still processing")

    def __line_is_comment(self): #TODO: Doesn't handle block comments
        line_array = self._cur_line.split(" ")
        if len(line_array) < 2:
            return False
        if line_array[0][0] == "/" and line_array[0][1] == "/":
            return True
        else:
            return False
        
    def __line_is_macro(self):
        line_array = self._cur_line.split(" ")
        if len(line_array) < 2:
            return False
        if line_array[0][0] == "(" and line_array[0][1] == "*":
            return True
        else:
            return False 

    def __parse_this_line(self):
        if self._state == "MODULE":
            if self.__get_module_name_from_line():
                self._state = "START_PARAM_OR_PORT"
            return
        elif self._state == "START_PARAM_OR_PORT":
            if self.__line_has_param_start():
                self._state = "PARAMS"
            elif self.__line_has_port_start():
                self._state = "PORTS"
            return
        elif self._state == "PARAMS":
            if self.__line_is_only_end_parenthesis():
                self._state = "START_PORTS"
            else:
                self.__get_parameter_from_line()
                if self.__line_has_end_parenthesis():
                    self._state = "START_PORTS"
            return
        elif self._state == "START_PORTS":
            if self.__line_has_port_start():
                self._state = "PORTS"
            return
        elif self._state == "PORTS":
            if self.__line_is_only_end_parenthesis():
                self._state = "DONE"
            else:
                self.__get_port_from_line()
                if self.__line_has_end_parenthesis():
                    self._state = "DONE"
            return
        elif self._state == "DONE":
            self._fid.close()
            return

    def __get_module_name_from_line(self):
        line_array = self._cur_line.split(" ")
        if line_array[0] == "module":
            self._properties["module_name"].append(line_array[1]) # TODO: What if there's an open paren at the end of the module name without a space?
            return True
        else:
            return False
        
    def __line_has_param_start(self):
        line_array = self._cur_line.split(" ")
        if self._cur_line.find("#(") != -1:
            return True
        else:
            return False

    def __line_has_port_start(self):
        line_array = self._cur_line.split(" ")
        if self._cur_line.find("(") != -1:
            return True
        else:
            return False

    def __get_parameter_from_line(self):
        line_array = self._cur_line.split(" ")
        self._properties["parameters"].append(line_array[1]) # Parameter name
        self._properties["parameters"].append(self.__get_dimensions_from_line(0))
        self._properties["parameters"].append(self.__get_val_from_line()) # Parameter default value

    def __get_dimensions_from_line(self, is_signal):
        left = self._cur_line.split("[")
        if self._cur_line == "".join(left): # Dimensionless parameter
            if (is_signal):
                msb = "0"
            else:
                msb = "31"
            lsb = "0"
        else: # With explicit dimensions
            left = "".join(left[1])

            right = left.split("]")
            right = "".join(right[0])

            dimensions = right.split(":")

            msb = dimensions[0]
            lsb = dimensions[1]

        return self.__calc_dimensions(msb.strip(), lsb.strip())

    def __calc_dimensions(self, msb, lsb):
        if msb.isdigit() and lsb.isdigit(): # Base case - both values are integers
            return int(msb) - int(lsb) + 1
        else: # One or both values are defined by parameters
            if not msb.isdigit():
                msb = self.__param_to_digit(msb)
            if not lsb.isdigit():
                lsb = self.__param_to_digit(lsb)
            if msb.isdigit() and lsb.isdigit(): # On successful attempt at evaluating both parameters, return calculated value
                return int(msb) - int(lsb) + 1
            else: # Couldn't successfully evaluate parameter value
                return "?"

    def __param_to_digit(self, param):
        loop_idx = 0
        for ii in self._properties["parameters"]:
            if loop_idx % 3 == 0:
                candidate_param_val = self._properties["parameters"][loop_idx+2]
            else:
                loop_idx = loop_idx + 1
                continue
            if ii == param: # Exact parameter value match
                return candidate_param_val

            if len(param.split("clog2")) == 1: # clog2 is not used
                if param.find(ii) != -1: # This parameter in the list is used in param string
                    return str(int(eval(param.replace(ii, candidate_param_val))))
                else: # Not the right parameter to use
                    loop_idx = loop_idx + 1
                    continue
            else: # Parameter match uses $clog2
                if param.find(ii) != -1: # This parameter in the list is used in param string               
                    val = candidate_param_val.split("clog2")
                    val = "".join(val[len(val)-1])
                    right = val.split("(")
                    right = "".join(right)
                    left = right.split(")")
                    left = "".join(left[0])
                    if left.isdigit(): # If argument to clog2 is an integer
                        return str(math.ceil(math.log2(int(left))))
                    else: # If argument to clog2 is another parameter
                        evaluated_arg = self.__param_to_digit(left)
                        if evaluated_arg.idigit():
                            return str(math.ceil(math.log2(int(evaluated_arg))))
                        else:
                            return "?"
                else: # Not the right parameter to use
                    loop_idx = loop_idx + 1
                    continue
            loop_idx = loop_idx + 1
        return "?" # Failed to evaluate parameter

    def __get_val_from_line(self):
        right = self._cur_line.split("=")
        right = "".join(right[len(right)-1])

        comma = right.split(",")
        if right != "".join(comma): # Comma found
            val = comma[0]
        else:
            comma = "".join(comma[0])
            
            comment = comma.split("//")
            if comma != "".join(comment): # Comment found
                val = comment[0]
            else:
                val = comma
        
        return val.strip()
    
    def __line_is_only_end_parenthesis(self):
        if self._cur_line.find(")") == 0:
            return True
        else:
            return False

    def __line_has_end_parenthesis(self):
        num_open_parenthesis = self.__get_num_occurrences(self._cur_line, "(")
        num_closed_parenthesis = self.__get_num_occurrences(self._cur_line, ")")

        if num_closed_parenthesis > num_open_parenthesis: # TODO: Fails for parenthesis in comments
            return True
        else:
            return False
    
    def __get_num_occurrences(self, total_string, substr_to_match):
        start_idx = 0
        cnt = 0
        for ii in range(len(total_string)):
            jj = total_string.find(substr_to_match, start_idx)
            if (jj != -1):
                start_idx = jj + 1
                cnt += 1
        return cnt

    def __get_port_from_line(self):
        line_array = self._cur_line.split(" ")
        if (line_array[0] == "input"):
            self._properties["inputs"].append(self.__get_signal_name_from_line())
            self._properties["inputs"].append(self.__get_dimensions_from_line(1))
            self._properties["ordered_signals"].append(self.__get_signal_name_from_line())
            self._properties["ordered_signals"].append(self.__get_dimensions_from_line(1))
        elif (line_array[0] == "output"):
            self._properties["outputs"].append(self.__get_signal_name_from_line())
            self._properties["outputs"].append(self.__get_dimensions_from_line(1))
            self._properties["ordered_signals"].append(self.__get_signal_name_from_line())
            self._properties["ordered_signals"].append(self.__get_dimensions_from_line(1))
        elif (line_array[0] == "inout"):
            self._properties["inouts"].append(self.__get_signal_name_from_line())
            self._properties["inouts"].append(self.__get_dimensions_from_line(1))
            self._properties["ordered_signals"].append(self.__get_signal_name_from_line())
            self._properties["ordered_signals"].append(self.__get_dimensions_from_line(1))
        else:
            sys.exit("Unknown port type")

    def __get_signal_name_from_line(self):
        right = self._cur_line.split(" ")
        right = "".join(right[len(right)-1])

        comma = right.split(",")
        if right != "".join(comma): # Comma found
            val = comma[0]
        else:
            comma = "".join(comma[0])
            
            comment = comma.split("//")
            if comma != "".join(comment): # Comment found
                val = comment[0]
            else:
                val = comma
        
        return val

    def __get_input_clocks(self):
        is_sig_name = True
        for sig in self._properties["inputs"]:
            if is_sig_name:
                if (sig.find("clken") != -1):
                    continue
                if sig.find("clk") != -1 or sig.find("clock") != -1:
                    self._properties["input_clocks"].append(sig)
            is_sig_name = not is_sig_name

    def get_module_properties(self):
        return self._properties