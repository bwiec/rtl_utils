import sys

class module_parser:
    _properties = {
        "module_name" : [],
        "parameters" : [],
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
        self.__parse_input_file()
        self.__get_input_clocks()
        
    def __parse_input_file(self):
        self._fid = open(self._file, 'r')
        for line in self._fid:
            self._cur_line_idx = self._cur_line_idx + 1
            self._cur_line = line.lstrip().rstrip()
            if self._cur_line == '' or self.__line_is_comment():
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
            print("right: ", right)

            dimensions = right.split(":")

            msb = dimensions[0]
            lsb = dimensions[1]

        bit_width = int(msb) - int(lsb) + 1

        return bit_width

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
        
        return val
    
    def __line_is_only_end_parenthesis(self):
        if self._cur_line.find(")") == 0:
            return True
        else:
            return False

    def __line_has_end_parenthesis(self):
        if self._cur_line.find(")") != -1:
            return True
        else:
            return False

    def __get_port_from_line(self):
        line_array = self._cur_line.split(" ")
        if (line_array[0] == "input"):
            self._properties["inputs"].append(self.__get_dimensions_from_line(1))
            self._properties["inputs"].append(self.__get_signal_name_from_line())
        elif (line_array[0] == "output"):
            self._properties["outputs"].append(self.__get_dimensions_from_line(1))
            self._properties["outputs"].append(self.__get_signal_name_from_line())
        elif (line_array[0] == "inout"):
            self._properties["inouts"].append(self.__get_dimensions_from_line(1))
            self._properties["inouts"].append(self.__get_signal_name_from_line())
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
        is_sig_name = False
        for sig in self._properties["inputs"]:
            if is_sig_name:
                if (sig.find("clken") != -1):
                    continue
                if sig.find("clk") != -1 or sig.find("clock") != -1:
                    self._properties["input_clocks"].append(sig)
            is_sig_name = not is_sig_name

    def get_module_properties(self):
        return self._properties