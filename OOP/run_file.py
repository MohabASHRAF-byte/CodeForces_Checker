import subprocess

from timer import Timer


class Run:
    # Put cpp file full path in the pc
    cpp_file_path = r"main.cpp"

    compile_command = f"g++ {cpp_file_path} -o compiled_cpp_file"
    input_string = str()

    def compile(self):
        # Compile the C++ file using Clang
        compile_command = f"g++ {self.cpp_file_path} -o compiled_cpp_file"
        subprocess.run(compile_command, shell=True, check=True)

    @staticmethod
    def run(inp: str):
        run_command = "./compiled_cpp_file"
        process = subprocess.Popen(run_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   shell=True)

        # Pass input string to the running process
        output, error = process.communicate(input=inp.encode())
        output = output.decode().strip()
        error = error.decode().strip()
        return len(error) != 0, error if error else output

