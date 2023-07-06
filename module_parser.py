import sys

class module_parser:
    _state = "INIT"
    _file = ""
    _cur_line = ""
    _properties = {
        "module_name" : [],
        "parameters" : [],
        "inputs" : [],
        "outputs" : [],
        "inouts" : [],
        "input_clocks" : []
    }

    def __init__(self, file):
        self._file = file
        self._state = "INIT"
        self.__parse_input_file()
        self.__get_input_clocks()
        
    def __parse_input_file(self):
        fid = open(self._file, 'r')
        for line in fid:
            self._cur_line = line.lstrip().rstrip()

            line_array = self._cur_line.split(" ")            
            if self._state == "INIT":
                if line_array[0] == "module": # Skip initial lines until we find uncommented 'module' keyword first
                    self.__get_module_name_from_line(line_array)
                    self._state = "PARAM"
                    continue
            if self._state == "PARAM":
                if line_array[0] == "(": # No parameters in this module
                    self._state = "PORTS"
                elif line_array[0] == "#(": # Found parameter entry point
                    self.__get_parameters(fid)
                    self._state = "PORTS"
                    continue
            if self._state == "PORTS":
                if line_array[0] == "(":
                    self.__get_ports(fid)
                    self._state = "DONE"
            if self._state == "DONE":
                fid.close()
                return

        fid.close()
        sys.exit("Reached the end of the file")

    def __get_module_name_from_line(self, line_array):
        self._properties["module_name"].append(line_array[1]) # TODO: What if there's an open paren at the end of the module name without a space?

    def __get_parameters(self, fid):
        for line in fid:
            self._cur_line = line.lstrip().rstrip()
            line_array = self._cur_line.split(" ")
            if self._cur_line.find(")") != -1:
                return
            if not self.__line_is_comment(line_array):
                self.__get_parameter_from_line(line_array)
    
    def __line_is_comment(self, line_array): #TODO: Doesn't handle block comments
        if line_array[0][0] == "/" and line_array[0][1] == "/":
            return True
        else:
            return False

    def __get_parameter_from_line(self, line_array):
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

    def __get_ports(self, fid):
        for line in fid:
            self._cur_line = line.lstrip().rstrip()
            line_array = self._cur_line.split(" ")
            if self._cur_line.find(");") != -1:
                return
            if not self.__line_is_comment(line_array):
                self.__get_port_from_line(line_array)

    def __get_port_from_line(self, line_array):
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
                if sig.find("clk") or sig.find("clock"):
                    self._properties["input_clocks"].append(sig)
            is_sig_name = not is_sig_name

    def get_module_properties(self):
        return self._properties