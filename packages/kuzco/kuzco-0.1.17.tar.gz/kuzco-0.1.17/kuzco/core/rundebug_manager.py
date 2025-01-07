import os
import xml.etree.ElementTree as ET


class RunDebugConfigurationGenerator:
    def __init__(self, base_dir, services_list):
        self.base_dir = base_dir
        self.services_list = services_list
        self.run_config_dir = os.path.join(base_dir, ".idea/runConfigurations")
        self.scripts_dir = os.path.join(base_dir, "src/scripts/bin")
        self.ensure_directories_exist()

    def ensure_directories_exist(self):
        os.makedirs(self.run_config_dir, exist_ok=True)
        os.makedirs(self.scripts_dir, exist_ok=True)

    def generate_run_configuration(self, name, script_path, parameters=None):
        config_path = os.path.join(self.run_config_dir, f"{name}.xml")
        if os.path.exists(config_path):
            return  # Skip if configuration already exists

        config = ET.Element("component", name="ProjectRunConfigurationManager")
        configuration = ET.SubElement(config, "configuration", {
            "default": "false",
            "name": name,
            "type": "PythonConfigurationType",
            "factoryName": "Python",
            "singleton": "true"
        })
        ET.SubElement(configuration, "module", name="dynamicPyCharmConfigurations")
        ET.SubElement(configuration, "option", name="SCRIPT_NAME", value=script_path)
        ET.SubElement(configuration, "option", name="WORKING_DIRECTORY", value="$PROJECT_DIR$")
        ET.SubElement(configuration, "option", name="EMULATE_TERMINAL", value="true")
        if parameters:
            ET.SubElement(configuration, "option", name="PARAMETERS", value=parameters)
        ET.SubElement(configuration, "method", v="2")

        tree = ET.ElementTree(config)
        with open(config_path, "wb") as f:
            tree.write(f, encoding="utf-8", xml_declaration=True)

#     def generate_python_script(self, script_name, command, interactive=False):
#         script_path = os.path.join(self.scripts_dir, f"{script_name}.py")
#         if os.path.exists(script_path):
#             return  # Skip if script already exists

#         if interactive:
#             target = script_name.split('_')[1] if '_' in script_name else 'item'
#             script_content = f"""#!/usr/bin/env python3
# import subprocess

# input_value = input("Enter the name for the {target}: ")
# command = {command}
# command.insert(-1, input_value)
# subprocess.run(command, check=True)
# """
#         else:
#             script_content = f"""#!/usr/bin/env python3
# import subprocess

# subprocess.run({command}, check=True)
# """

#         with open(script_path, "w") as f:
#             f.write(script_content)
    def generate_python_script(self, script_name, command, interactive=False):
        script_path = os.path.join(self.scripts_dir, f"{script_name}.py")
        if os.path.exists(script_path):
            return  # Skip if script already exists

        if interactive:
            if "uvicorn" in command:
                target = script_name.split('_')[2] if '_' in script_name else 'service'
                script_content = f"""#!/usr/bin/env python3
import subprocess

input_value = input("Enter the name for the {target}: ")
command = {command}
command.insert(3, input_value)  # Insert the input_value after the initial arguments
subprocess.run(command, check=True)
"""
            else:
                target = script_name.split('_')[1] if '_' in script_name else 'item'
                script_content = f"""#!/usr/bin/env python3
import subprocess

input_value = input("Enter the name for the {target}: ")
command = {command}
command.insert(-1, input_value)
subprocess.run(command, check=True)
"""
        else:
            script_content = f"""#!/usr/bin/env python3
import subprocess

subprocess.run({command}, check=True)
"""

        with open(script_path, "w") as f:
            f.write(script_content)

    # def cleanup_removed_service_files(self):
    #     # Get current service names
    #     current_services = set(self.services_list)

    #     # Identify files related to services
    #     for file_name in os.listdir(self.run_config_dir):
    #         if file_name.endswith(".xml"):
    #             service_name = self._extract_service_name(file_name)
    #             if service_name and service_name not in current_services:
    #                 os.remove(os.path.join(self.run_config_dir, file_name))

    #     for file_name in os.listdir(self.scripts_dir):
    #         if file_name.endswith(".py"):
    #             service_name = self._extract_service_name(file_name)
    #             if service_name and service_name not in current_services:
    #                 os.remove(os.path.join(self.scripts_dir, file_name))

    def _extract_service_name(self, file_name):
        # Extract the service name from a file name like `run_service_x.py` or `run-service-x.xml`
        if file_name.startswith("run-service-") and file_name.endswith(".xml"):
            return file_name[len("run-service-"):-len(".xml")]
        elif file_name.startswith("run_service_") and file_name.endswith(".py"):
            return file_name[len("run_service_"):-len(".py")]
        return None

    def generate_static_rundebug_configuration(self):
        static_name = "refresh-rundebug"
        static_script_name = "refresh_rundebug"
        static_command = ["kuzco", "create", "rundebug", "."]

        self.generate_python_script(static_script_name, repr(static_command))
        self.generate_run_configuration(
            static_name,
            os.path.join(self.scripts_dir, f"{static_script_name}.py")
        )

    def generate_all(self):
        unique_port = 8000
        for service_name in self.services_list:
            commands = {
                f"run-service-{service_name}": ["kuzco", "manage", "run", "service", service_name, "."],
                f"run-service-{service_name}-uvicorn": ["kuzco", "manage", "run", "service", service_name, ".", "--uvicorn", f"--port={unique_port}"],
                f"install-requirements-service-{service_name}": ["kuzco", "manage", "install", "service", service_name, "."],
                f"generate-dockerignore-service-{service_name}": ["kuzco", "manage", "ci", "service", service_name, "."],
                f"restart-service-{service_name}": ["kuzco", "manage", "restart", "service", service_name, "."],
                f"restart-service-{service_name}-uvicorn": ["kuzco", "manage", "restart", "service", service_name, ".", "--uvicorn", f"--port={unique_port}"],
                f"docker-build-service-{service_name}": ["docker", "build", "-f", f"src/services/{service_name}/Dockerfile", "-t", service_name, "."],
                f"docker-run-service-{service_name}": ["docker", "run", "--rm", f"-p {unique_port}:3000", service_name],
            }

            for name, command in commands.items():
                script_name = name.replace("-", "_")
                script_path = os.path.join(self.scripts_dir, f"{script_name}.py")
                self.generate_python_script(script_name, repr(command))
                self.generate_run_configuration(name, script_path)
                unique_port += 1

        # interactive_commands = {
        #     "create-service": ["kuzco", "create", "service", "."],
        #     "create-util": ["kuzco", "create", "util", "."],
        # }

        # for name, command in interactive_commands.items():
        #     script_name = name.replace("-", "_")
        #     self.generate_python_script(script_name, repr(command), interactive=True)
        #     self.generate_run_configuration(name, os.path.join(self.scripts_dir, f"{script_name}.py"))
        interactive_commands = {
            "create-service": ["kuzco", "create", "service", "."],
            "create-util": ["kuzco", "create", "util", "."],
            "create-uvicorn-service": ["kuzco", "create", "service", ".", "--uvicorn"],
        }

        for name, command in interactive_commands.items():
            script_name = name.replace("-", "_")
            interactive = True  # Mark all commands in this block as interactive
            self.generate_python_script(script_name, repr(command), interactive=interactive)
            self.generate_run_configuration(name, os.path.join(self.scripts_dir, f"{script_name}.py"))

        self.generate_static_rundebug_configuration()

        # Clean up files for removed services
        # self.cleanup_removed_service_files()


