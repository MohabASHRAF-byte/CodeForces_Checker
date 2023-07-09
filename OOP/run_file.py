import subprocess


class Run:
    cpp_file_path = r"/home/mohab/CLionProjects/untitled1/main.cpp"

    compile_command = f"g++ {cpp_file_path} -o compiled_cpp_file"
    input_string = str()

    def do_work(self, cppInput: str):
        self.input_string = cppInput
        # Compile the C++ file
        compile_command = f"g++ {self.cpp_file_path} -o compiled_cpp_file"
        subprocess.run(compile_command, shell=True, check=True)

        # Run the compiled C++ file
        run_command = "./compiled_cpp_file"
        process = subprocess.Popen(run_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   shell=True)

        # Pass input string to the running process
        output, error = process.communicate(input=self.input_string.encode())
        output = output.decode().strip()
        error = error.decode().strip()
        return len(error) != 0, error if error else output
