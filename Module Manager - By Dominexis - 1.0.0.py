# Import things
import os
import shutil
import datetime



# Initialize variables
path = os.path.dirname(os.path.realpath(__file__))

class parameter_kind:
    def __init__(self, name, kind, value):
        self.name = name
        self.id = name.lower().replace(" ", "_").replace("'", "")
        self.kind = kind
        self.value = value

parameters = [
    parameter_kind("Module Name", "file", "Blank Module"),
    parameter_kind("Author", "file", "Dominexis"),
    parameter_kind("Version", "version", "1.0.0"),
    parameter_kind("Dom's Nexus Version", "version", "1.10.2"),
    parameter_kind("Internal ID", "internal", "blank_module"),
    parameter_kind("Namespace", "internal", "blank"),
    parameter_kind("Old Module Name", "file", "Blank Module - By Dominexis - 1.0.0"),

    parameter_kind("Feature Time Manager", "boolean", "true"),
    parameter_kind("Feature Player NBT", "boolean", "false"),
    parameter_kind("Feature Player Health", "boolean", "true"),
    parameter_kind("Feature Player Respawn", "boolean", "true"),
    parameter_kind("Feature Player Motion", "boolean", "false"),
    parameter_kind("Feature Entity Processing", "boolean", "true"),
    parameter_kind("Feature Entity Health", "boolean", "true"),
    parameter_kind("Feature Custom Entity Ticking", "boolean", "true"),
    parameter_kind("Feature Unconditional Entity Ticking", "boolean", "false"),
    parameter_kind("Feature Damage Sensor Ticking", "boolean", "false"),
    parameter_kind("Feature Vehicle", "boolean", "false"),
    parameter_kind("Feature Event ID Player Hurt Entity", "boolean", "true"),
    parameter_kind("Feature Event ID Player Killed Entity", "boolean", "true"),
    parameter_kind("Feature Event ID Entity Hurt Player", "boolean", "true"),
    parameter_kind("Feature Event ID Entity Killed Player", "boolean", "true"),
    parameter_kind("Feature Event ID Player Interacted With Entity", "boolean", "true"),
    parameter_kind("Feature Object Ticking", "boolean", "false"),
    parameter_kind("Minimum Difficulty", "difficulty", "easy")
]

error = False
message = ""



# Define functions
def dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
def tag(directory, functions):
    # Compile contents
    if len(functions) == 0:
        list = ""
    else:
        list = "\n        \"" + "\",\n        \"".join(functions) + "\"\n    "
    with open(directory, "w", encoding="utf-8") as file:
        file.write(
            "{\n" +
            "    \"replace\": false,\n" +
            "    \"values\": [" + list + "]\n" +
            "}"
        )
def clear():
    os.system("cls") if os.name == "nt" else os.system("clear")
def action_check(string, minumum, maximum):
    # Halt if string contains non-number characters
    try:
        action = int(string)
    except:
        return 0, True, " Error: Input must be a number!\n"
    else:
        if minumum <= action and action <= maximum:
            return action, False, ""
        else:
            return 0, True, " Error: Input is out of range!\n"
def file_check(string, id, message):
    # Halt if string is empty
    if len(string) == 0:
        return "", True, message + " Error: " + id + ": Cannot use an empty string!\n"
    # Halt if there are any illegal characters in the string
    for char in ["/", "\\", "?", "<", ">", ":", "\"", "|"]:
        if char in string:
            return "", True, message + " Error: " + id + ": Cannot use illegal characters in file names!\n"
    # Return
    return string, False, message + ""
def version_check(string, id, message):
    # Halt if string is empty
    if len(string) == 0:
        return "", True, message + " Error: " + id + ": Cannot use an empty string!\n"
    # Halt if version ID is invalid
    if len(string.split(".")) != 3:
        return "", True, message + " Error: " + id + ": Version must use the format MAJOR.MINOR.PATCH!\n"
    # Halt if any of the entries are non-positive or non-numbers
    for value in string.split("."):
        try:
            int(value)
        except:
            return "", True, message + " Error: " + id + ": Cannot use non-numbers in version ID!\n"
        else:
            if int(value) < 0:
                return "", True, message + " Error: " + id + ": Cannot use negative numbers in version ID!\n"
            elif int(value) > 2147483647:
                return "", True, message + " Error: " + id + ": Cannot have numbers larger than the 32-bit integer limit!\n"
    # Return
    return string, False, message + ""
def internal_check(string, id, message):
    # Halt if string is empty
    if len(string) == 0:
        return "", True, message + " Error: " + id + ": Cannot use an empty string!\n"
    # Halt if any one of the characters isn't allowed
    for char in string:
        if char not in ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","0","1","2","3","4","5","6","7","8","9","-","_","."]:
            return "", True, message + " Error: " + id + ": Cannot use illegal characters in an internal string!\n"
    # Return
    return string, False, message + ""
def boolean_check(string, id, message):
    # Halt if not a boolean
    if string not in ["false", "true", "0", "1"]:
        return "", True, message + " Error: " + id + ": Input must be a Boolean!\n"
    # Return
    if string in ["0", "1"]:
        string = ["false", "true"][["0", "1"].index(string)]
    return string, False, message + ""
def difficulty_check(string, id, message):
    # Halt if not a difficulty
    if string not in ["peaceful", "easy", "normal", "hard", "0", "1", "2", "3"]:
        return "", True, message + " Error: " + id + ": Input must be a valid difficulty level!\n"
    # Return
    if string in ["0", "1", "2", "3"]:
        string = ["peaceful", "easy", "normal", "hard"][["0", "1", "2", "3"].index(string)]
    return string, False, message + ""



# Main loop
while True:
    # Display main menu
    clear()
    print(
        "\n Module Manager - For Dom's Nexus\n By Dominexis - 1.0.0\n" +
        "\n Parameters:"
    )
    for i in range(len(parameters)):
        print("  " + parameters[i].name + ":   " + parameters[i].value)
    print(
        "\n Actions:" +
        "\n  1) Edit parameters" +
        "\n  2) Load parameters from file" +
        "\n  3) Create module" +
        "\n  4) Update module" +
        "\n  5) Exit program" +
        "\n"
    )

    # Get action input
    action, error, message = action_check(input(message + " Action: "), 1, 5)
    if not error:
        if action == 1:
            while True:
                # Display parameters menu
                clear()
                print(
                    "\n Module Manager - For Dom's Nexus\n By Dominexis - 1.0.0\n" +
                    "\n Edit parameter:" +
                    "\n  0) Go back"
                )
                for i in range(len(parameters)):
                    print("  " + str(i+1) + ") " + parameters[i].name + ":   " + parameters[i].value)
                print("\n")

                # Get action input
                action, error, message = action_check(input(message + " Action: "), 0, len(parameters))
                if not error:
                    if action == 0:
                        break
                    else:
                        # Set parameter
                        parameter = parameters[action-1]
                        if parameter.kind == "file":
                            value, error, message = file_check(input(" " + parameter.name + ": "), parameter.id, message)
                        elif parameter.kind == "version":
                            value, error, message = version_check(input(" " + parameter.name + ": "), parameter.id, message)
                        elif parameter.kind == "internal":
                            value, error, message = internal_check(input(" " + parameter.name + ": "), parameter.id, message)
                        elif parameter.kind == "boolean":
                            value, error, message = boolean_check(input(" " + parameter.name + ": "), parameter.id, message)
                        elif parameter.kind == "difficulty":
                            value, error, message = difficulty_check(input(" " + parameter.name + ": "), parameter.id, message)
                        if not error:
                            parameters[action-1].value = value

        elif action == 2:
            # Throw an error if the file does not exist
            if not os.path.exists(os.path.join(path, "Module Manager Input.txt")):
                error = True
                message = " Error: Input file does not exist!\n"
            else:
                # Read file contents
                with open(os.path.join(path, "Module Manager Input.txt"), "r", encoding="utf-8") as file:
                    input_file = file.read().split("\n")
                
                # Divide parameter names and values
                input_names = []
                input_values = []
                for entry in input_file:
                    if "=" not in entry:
                        continue
                    input_names.append(entry.split("=")[0])
                    input_values.append(entry.split("=")[1])

                # Iterate over parameters list
                for i in range(len(parameters)):
                    parameter = parameters[i]
                    if parameter.id in input_names:
                        value = input_values[input_names.index(parameter.id)]
                        if parameter.kind == "file":
                            value, error, message = file_check(value, parameter.id, message)
                        elif parameter.kind == "version":
                            value, error, message = version_check(value, parameter.id, message)
                        elif parameter.kind == "internal":
                            value, error, message = internal_check(value, parameter.id, message)
                        elif parameter.kind == "boolean":
                            value, error, message = boolean_check(value, parameter.id, message)
                        elif parameter.kind == "difficulty":
                            value, error, message = difficulty_check(value, parameter.id, message)
                        if not error:
                            parameters[i].value = value

                # Set message
                message += " Parameters loaded.\n"
                
        elif action == 3:
            # Extract parameters
            parameter_ids = []
            parameter_values = []
            for parameter in parameters:
                parameter_ids.append(parameter.id)
                parameter_values.append(parameter.value)
            
            module_name = parameter_values[parameter_ids.index("module_name")]
            author = parameter_values[parameter_ids.index("author")]
            version = parameter_values[parameter_ids.index("version")]
            doms_nexus_version = parameter_values[parameter_ids.index("doms_nexus_version")]
            internal_id = parameter_values[parameter_ids.index("internal_id")]
            namespace = parameter_values[parameter_ids.index("namespace")]

            # Compile pack name
            pack_name = module_name + " - By " + author + " - " + version

            # Check if the module already exists
            if os.path.exists(os.path.join(path, pack_name)):
                print(
                    "\n \"" + pack_name + "\" already exists, do you want to delete it?" +
                    "\n  1) Yes" +
                    "\n  2) No" +
                    "\n"
                )

                # Get action input
                action, error, message = action_check(input(message + " Action: "), 1, 2)
                if not error:
                    if action == 1:
                        shutil.rmtree(os.path.join(path, pack_name))

            # Create module if it doesn't exist
            if not os.path.exists(os.path.join(path, pack_name)):
                # Create folders
                dir(os.path.join(path, pack_name, "data", "minecraft", "tags", "functions"))

                dir(os.path.join(path, pack_name, "data", "nexus", "functions", "verify"))
                dir(os.path.join(path, pack_name, "data", "nexus", "tags", "functions", "player"))
                dir(os.path.join(path, pack_name, "data", "nexus", "tags", "functions", "setup"))
                dir(os.path.join(path, pack_name, "data", "nexus", "tags", "functions", "tick"))
                dir(os.path.join(path, pack_name, "data", "nexus", "tags", "functions", "uninstall"))
                dir(os.path.join(path, pack_name, "data", "nexus", "tags", "functions", "verify"))
                dir(os.path.join(path, pack_name, "data", "nexus", "tags", "entity_types", "generic"))

                dir(os.path.join(path, pack_name, "data", namespace, "tags", "entity_types", "generic"))
                dir(os.path.join(path, pack_name, "data", namespace, "tags", "items", "generic"))
                dir(os.path.join(path, pack_name, "data", namespace, "functions", "player", "login"))
                dir(os.path.join(path, pack_name, "data", namespace, "functions", "setup"))
                dir(os.path.join(path, pack_name, "data", namespace, "functions", "tick"))
                dir(os.path.join(path, pack_name, "data", namespace, "functions", "uninstall"))
                dir(os.path.join(path, pack_name, "data", namespace, "functions", "verify", version.replace(".", "_")))

                # Create pack.mcmeta
                with open(os.path.join(path, pack_name, "pack.mcmeta"), "w", encoding="utf-8") as file:
                    file.write(
                        "{\n" +
                        "    \"pack\": {\n" +
                        "        \"pack_format\": 10,\n" +
                        "        \"description\": \"§9§l" + module_name + "\\n§7By §9" + author + " §7- §6" + version + "\\n§7Powered by §9Dom's Nexus §6" + doms_nexus_version + "+\"\n" +
                        "    }\n" +
                        "}"
                    )

                # Create verification function
                with open(os.path.join(path, pack_name, "data", "nexus", "functions", "verify", "main.mcfunction"), "w", encoding="utf-8") as file:
                    file.write(
                        "# Create scoreboard objective" + "\n"*2 +
                        "scoreboard objectives add nexus.value dummy" + "\n"*8 +
                        "# Initialize scores" + "\n"*2 +
                        "scoreboard players set #doms_nexus_error_boolean nexus.value 0" + "\n"*8 +
                        "# Verify modules" + "\n"*2 +
                        "data modify storage nexus:data modules set value []\n" +
                        "function #nexus:verify/version\n" +
                        "function #nexus:verify/check" + "\n"*8 +
                        "# Setup Nexus" + "\n"*2 +
                        "execute if score #doms_nexus_error_boolean nexus.value matches 1 run tellraw @a [\"\",{\"text\":\"[\",\"color\":\"gray\"},{\"text\":\"Dom's Nexus\",\"color\":\"blue\"},{\"text\":\"]\",\"color\":\"gray\"},\" \",{\"text\":\"Nexus and modules were unable to install.\",\"color\":\"red\"}]\n" +
                        "execute if score #doms_nexus_error_boolean nexus.value matches 0 run function nexus:setup/main"
                    )

                # Create tags
                tag(os.path.join(path, pack_name, "data", "minecraft", "tags", "functions", "load.json"), ["nexus:verify/main"])

                tag(os.path.join(path, pack_name, "data", "nexus", "tags", "entity_types", "generic", "entity.json"), ["#" + namespace + ":generic/entity"])
                tag(os.path.join(path, pack_name, "data", "nexus", "tags", "entity_types", "generic", "damage_sensor.json"), ["#" + namespace + ":generic/damage_sensor"])
                tag(os.path.join(path, pack_name, "data", "nexus", "tags", "entity_types", "generic", "vehicle.json"), [])

                tag(os.path.join(path, pack_name, "data", "nexus", "tags", "functions", "player", "main.json"), [namespace + ":player/main"])
                tag(os.path.join(path, pack_name, "data", "nexus", "tags", "functions", "player", "login.json"), [namespace + ":player/login/main"])
                tag(os.path.join(path, pack_name, "data", "nexus", "tags", "functions", "setup", "main.json"), [namespace + ":setup/main"])
                tag(os.path.join(path, pack_name, "data", "nexus", "tags", "functions", "setup", "last_modified.json"), [namespace + ":setup/last_modified"])
                tag(os.path.join(path, pack_name, "data", "nexus", "tags", "functions", "tick", "main.json"), [namespace + ":tick/main"])
                tag(os.path.join(path, pack_name, "data", "nexus", "tags", "functions", "uninstall", "modules.json"), [namespace + ":uninstall/main"])
                tag(os.path.join(path, pack_name, "data", "nexus", "tags", "functions", "verify", "version.json"), [namespace + ":verify/" + version.replace(".", "_") + "/version"])
                tag(os.path.join(path, pack_name, "data", "nexus", "tags", "functions", "verify", "check.json"), [namespace + ":verify/" + version.replace(".", "_") + "/check"])

                tag(os.path.join(path, pack_name, "data", namespace, "tags", "entity_types", "generic", "entity.json"), ["#nexus:generic/system", "#" + namespace + ":generic/damage_sensor"])
                tag(os.path.join(path, pack_name, "data", namespace, "tags", "entity_types", "generic", "damage_sensor.json"), [])
                tag(os.path.join(path, pack_name, "data", namespace, "tags", "items", "generic", "item.json"), [])

                # Entity functions
                if parameter_values[parameter_ids.index("feature_custom_entity_ticking")] == "true":
                    dir(os.path.join(path, pack_name, "data", "nexus", "tags", "functions", "entity"))
                    tag(os.path.join(path, pack_name, "data", "nexus", "tags", "functions", "entity", "main.json"), [namespace + ":entity/verify"])

                    dir(os.path.join(path, pack_name, "data", namespace, "functions", "entity"))
                    with open(os.path.join(path, pack_name, "data", namespace, "functions", "entity", "verify.mcfunction"), "w", encoding="utf-8") as file:
                        file.write(
                            "# Run function if entity is from the right module" + "\n"*2 +
                            "execute if entity @s[tag=" + namespace + ".entity] run function " + namespace + ":entity/main"
                        )
                    with open(os.path.join(path, pack_name, "data", namespace, "functions", "entity", "main.mcfunction"), "w", encoding="utf-8") as file:
                        file.write(
                            "# Run function based on entity type" + "\n"*2
                        )
                if parameter_values[parameter_ids.index("feature_entity_processing")] == "true":
                    dir(os.path.join(path, pack_name, "data", "nexus", "tags", "functions", "entity"))
                    tag(os.path.join(path, pack_name, "data", "nexus", "tags", "functions", "entity", "process.json"), [namespace + ":entity/generic/process/main"])

                    dir(os.path.join(path, pack_name, "data", namespace, "functions", "entity", "generic", "process"))
                    with open(os.path.join(path, pack_name, "data", namespace, "functions", "entity", "generic", "process", "main.mcfunction"), "w", encoding="utf-8") as file:
                        file.write("")

                # Event ID functions
                for criteria in ["entity_hurt_player", "entity_killed_player", "player_hurt_entity", "player_killed_entity", "player_interacted_with_entity"]:
                    if parameter_values[parameter_ids.index("feature_event_id_" + criteria)] == "true":
                        dir(os.path.join(path, pack_name, "data", "nexus", "tags", "functions", "generic", "event_id", criteria, "player"))
                        tag(os.path.join(path, pack_name, "data", "nexus", "tags", "functions", "generic", "event_id", criteria, "player", "pre.json"), [namespace + ":generic/event_id/" + criteria + "/player/pre"])
                        tag(os.path.join(path, pack_name, "data", "nexus", "tags", "functions", "generic", "event_id", criteria, "player", "post.json"), [namespace + ":generic/event_id/" + criteria + "/player/post"])
                        tag(os.path.join(path, pack_name, "data", "nexus", "tags", "functions", "generic", "event_id", criteria, "entity.json"), [namespace + ":generic/event_id/" + criteria + "/entity"])

                        dir(os.path.join(path, pack_name, "data", namespace, "functions", "generic", "event_id", criteria, "player"))
                        with open(os.path.join(path, pack_name, "data", namespace, "functions", "generic", "event_id", criteria, "player", "pre.mcfunction"), "w", encoding="utf-8") as file:
                            file.write("")
                        with open(os.path.join(path, pack_name, "data", namespace, "functions", "generic", "event_id", criteria, "player", "post.mcfunction"), "w", encoding="utf-8") as file:
                            file.write("")
                        with open(os.path.join(path, pack_name, "data", namespace, "functions", "generic", "event_id", criteria, "entity.mcfunction"), "w", encoding="utf-8") as file:
                            file.write("")

                # Object functions
                if parameter_values[parameter_ids.index("feature_object_ticking")] == "true":
                    dir(os.path.join(path, pack_name, "data", "nexus", "tags", "functions", "object"))
                    tag(os.path.join(path, pack_name, "data", "nexus", "tags", "functions", "object", "main.json"), [namespace + ":object/verify"])

                    dir(os.path.join(path, pack_name, "data", namespace, "functions", "object"))
                    with open(os.path.join(path, pack_name, "data", namespace, "functions", "object", "verify.mcfunction"), "w", encoding="utf-8") as file:
                        file.write(
                            "# Run function if object is from the right module" + "\n"*2 +
                            "execute if entity @s[tag=" + namespace + ".object] run function " + namespace + ":object/main"
                        )
                    with open(os.path.join(path, pack_name, "data", namespace, "functions", "object", "main.mcfunction"), "w", encoding="utf-8") as file:
                        file.write(
                            "# Run function based on object type" + "\n"*2
                        )

                # Player functions
                with open(os.path.join(path, pack_name, "data", namespace, "functions", "player", "main.mcfunction"), "w", encoding="utf-8") as file:
                    file.write("")
                with open(os.path.join(path, pack_name, "data", namespace, "functions", "player", "login", "main.mcfunction"), "w", encoding="utf-8") as file:
                    file.write(
                        "# Send message" + "\n"*2 +
                        "execute if score #debug_login_messages nexus.value matches 1 run tellraw @s [\" \",{\"text\":\"- \",\"color\":\"gray\"},{\"text\":\"" + module_name + "\",\"color\":\"gold\"},{\"text\":\" - \",\"color\":\"gray\"},{\"text\":\"" + version + "\",\"color\":\"gold\"}]"
                    )
                if parameter_values[parameter_ids.index("feature_player_respawn")] == "true":
                    tag(os.path.join(path, pack_name, "data", "nexus", "tags", "functions", "player", "respawn.json"), [namespace + ":player/respawn/main"])
                    dir(os.path.join(path, pack_name, "data", namespace, "functions", "player", "respawn"))
                    with open(os.path.join(path, pack_name, "data", namespace, "functions", "player", "respawn", "main.mcfunction"), "w", encoding="utf-8") as file:
                        file.write("")

                # Setup functions
                list = []
                for parameter in parameters:
                    if parameter.id.split("_")[0] == "feature" and parameter.value == "true":
                        list.append("scoreboard players set #" + parameter.id.replace("player_hurt_entity", "phe").replace("player_killed_entity", "pke").replace("entity_hurt_player", "ehp").replace("entity_killed_player", "ekp").replace("player_interacted_with_entity", "piwe") + " nexus.value 1")
                minimum_difficulty = ["0", "1", "2", "3"][["peaceful", "easy", "normal", "hard"].index(parameter_values[parameter_ids.index("minimum_difficulty")])]
                with open(os.path.join(path, pack_name, "data", namespace, "functions", "setup", "main.mcfunction"), "w", encoding="utf-8") as file:
                    file.write(
                        "# Run installation function" + "\n"*2 +
                        "execute if score #update_installation_boolean nexus.value matches 1 run function temp:setup/install" + "\n"*8 +
                        "# Set feature booleans" + "\n"*2 +
                        "\n".join(list) + "\n"*8 +
                        "# Set minimum difficulty" + "\n"*2 +
                        "execute if score #minimum_difficulty nexus.value matches .." + minimum_difficulty + " run scoreboard players set #minimum_difficulty nexus.value " + minimum_difficulty + "\n"*8 +
                        "# Increment module count" + "\n"*2 +
                        "scoreboard players add #doms_nexus_module_count nexus.value 1"
                    )
                time = datetime.datetime.now()
                with open(os.path.join(path, pack_name, "data", namespace, "functions", "setup", "last_modified.mcfunction"), "w", encoding="utf-8") as file:
                    file.write(
                        "# Set last modified value\n" +
                        "\n" +
                        "scoreboard players set #last_modified nexus.value " + str(time.year) + ("0" if time.month < 10 else "") + str(time.month) + ("0" if time.day < 10 else "") + str(time.day) + ("0" if time.hour*4 + time.minute//15 < 10 else "") + str(time.hour*4 + time.minute//15) + "\n" +
                        "execute unless score #" + internal_id + "_last_modified nexus.value = #last_modified nexus.value run scoreboard players set #update_installation_boolean nexus.value 1\n" +
                        "scoreboard players operation #" + internal_id + "_last_modified nexus.value = #last_modified nexus.value\n"
                    )
                with open(os.path.join(path, pack_name, "data", namespace, "functions", "setup", "install.mcfunction"), "w", encoding="utf-8") as file:
                    file.write(
                        "# Create scoreboard objectives" + "\n"*2 +
                        "scoreboard objectives add " + namespace + ".value dummy"
                    )

                # Tick functions
                with open(os.path.join(path, pack_name, "data", namespace, "functions", "tick", "main.mcfunction"), "w", encoding="utf-8") as file:
                    file.write("")

                # Uninstall functions
                with open(os.path.join(path, pack_name, "data", namespace, "functions", "uninstall", "main.mcfunction"), "w", encoding="utf-8") as file:
                    file.write(
                        "# Remove scoreboard objectives" + "\n"*2 +
                        "scoreboard objectives remove " + namespace + ".value" + "\n"*8 +
                        "# Terminate entities" + "\n"*2 +
                        "kill @e[type=#" + namespace + ":generic/entity,tag=" + namespace + ".entity]" + "\n"*8 +
                        "# Clear items" + "\n"*2 +
                        "clear @a #" + namespace + ":generic/item{" + namespace + ":{item:1b}}" + "\n"*8 +
                        "# Clear storage" + "\n"*2 +
                        "data remove storage " + namespace + ":data tag" + "\n"*8 +
                        "# Reset scores" + "\n"*2 +
                        "scoreboard players reset #" + internal_id + "_last_modified nexus.value" + "\n"*8 +
                        "# Send message to chat" + "\n"*2 +
                        "execute if score #debug_system_messages nexus.value matches 1 run tellraw @a[tag=nexus.player.operator] [\"\",{\"text\":\"[\",\"color\":\"gray\"},{\"text\":\"" + module_name + "\",\"color\":\"gold\"},{\"text\":\"]\",\"color\":\"gray\"},\" \",{\"text\":\"Module was successfully uninstalled.\",\"color\":\"gray\"}]\n"
                    )

                # Verification functions
                with open(os.path.join(path, pack_name, "data", namespace, "functions", "verify", version.replace(".", "_"), "version.mcfunction"), "w", encoding="utf-8") as file:
                    file.write(
                        "# Add pack version ID to module list" + "\n"*2 +
                        "data modify storage nexus:data modules append value {id:\"" + internal_id + "\",version:{major:" + version.split(".")[0] + ",minor:" + version.split(".")[1] + ",patch:" + version.split(".")[2] + "}}"
                    )
                with open(os.path.join(path, pack_name, "data", namespace, "functions", "verify", version.replace(".", "_"), "check.mcfunction"), "w", encoding="utf-8") as file:
                    file.write(
                        "# Throw error if the Nexus is not installed properly" + "\n"*2 +
                        "execute store result score #module_count nexus.value if data storage nexus:data modules[{id:\"doms_nexus\"}]\n" + 
                        "execute unless score #module_count nexus.value matches 1 run scoreboard players set #doms_nexus_error_boolean nexus.value 1\n" + 
                        "execute if score #module_count nexus.value matches 000 run tellraw @a [\"\",{\"text\":\"[\",\"color\":\"gray\"},{\"text\":\"" + module_name + "\",\"color\":\"gold\"},{\"text\":\"]\",\"color\":\"gray\"},\" \",{\"text\":\"Error: \",\"color\":\"dark_red\"},{\"text\":\"Dom's Nexus\",\"color\":\"blue\",\"underlined\":true,\"hoverEvent\":{\"action\":\"show_text\",\"value\":[{\"text\":\"Dom's Nexus\",\"color\":\"blue\"},{\"text\":\" on \",\"color\":\"gray\"},{\"text\":\"GitHub\",\"color\":\"blue\"}]},\"clickEvent\":{\"action\":\"open_url\",\"value\":\"https://github.com/Dominexis/Doms-Nexus/releases\"}},{\"text\":\" is not installed.\",\"color\":\"red\"}]\n" + 
                        "execute if score #module_count nexus.value matches 2.. run tellraw @a [\"\",{\"text\":\"[\",\"color\":\"gray\"},{\"text\":\"" + module_name + "\",\"color\":\"gold\"},{\"text\":\"]\",\"color\":\"gray\"},\" \",{\"text\":\"Error: \",\"color\":\"dark_red\"},{\"text\":\"Multiple copies of \",\"color\":\"red\"},{\"text\":\"Dom's Nexus\",\"color\":\"blue\"},{\"text\":\" exist. Remove all outdated versions.\",\"color\":\"red\"}]" + "\n"*2 +
                        "scoreboard players set #expected_major nexus.value " + doms_nexus_version.split(".")[0] + "\n" + 
                        "scoreboard players set #expected_minor nexus.value " + doms_nexus_version.split(".")[1] + "\n" + 
                        "scoreboard players set #expected_patch nexus.value " + doms_nexus_version.split(".")[2] + "\n" + 
                        "scoreboard players set #installed_major nexus.value 0\n" + 
                        "scoreboard players set #installed_minor nexus.value 0\n" + 
                        "scoreboard players set #installed_patch nexus.value 0" + "\n"*2 +
                        "execute if score #module_count nexus.value matches 001 store result score #installed_major nexus.value run data get storage nexus:data modules[{id:\"doms_nexus\"}].version.major\n" + 
                        "execute if score #module_count nexus.value matches 001 store result score #installed_minor nexus.value run data get storage nexus:data modules[{id:\"doms_nexus\"}].version.minor\n" + 
                        "execute if score #module_count nexus.value matches 001 store result score #installed_patch nexus.value run data get storage nexus:data modules[{id:\"doms_nexus\"}].version.patch\n" + 
                        "execute if score #module_count nexus.value matches 001 unless score #installed_major nexus.value = #expected_major nexus.value run scoreboard players set #doms_nexus_error_boolean nexus.value 1\n" + 
                        "execute if score #module_count nexus.value matches 001 if score #installed_major nexus.value < #expected_major nexus.value run tellraw @a [\"\",{\"text\":\"[\",\"color\":\"gray\"},{\"text\":\"" + module_name + "\",\"color\":\"gold\"},{\"text\":\"]\",\"color\":\"gray\"},\" \",{\"text\":\"Error: \",\"color\":\"dark_red\"},{\"text\":\"Dom's Nexus\",\"color\":\"blue\",\"underlined\":true,\"hoverEvent\":{\"action\":\"show_text\",\"value\":[{\"text\":\"Dom's Nexus\",\"color\":\"blue\"},{\"text\":\" on \",\"color\":\"gray\"},{\"text\":\"GitHub\",\"color\":\"blue\"}]},\"clickEvent\":{\"action\":\"open_url\",\"value\":\"https://github.com/Dominexis/Doms-Nexus/releases\"}},\" \",{\"score\":{\"name\":\"#installed_major\",\"objective\":\"nexus.value\"},\"color\":\"gold\"},{\"text\":\".x.x\",\"color\":\"gold\"},{\"text\":\" is too old, update it to the latest version.\",\"color\":\"red\"}]\n" + 
                        "execute if score #module_count nexus.value matches 001 if score #installed_major nexus.value > #expected_major nexus.value run tellraw @a [\"\",{\"text\":\"[\",\"color\":\"gray\"},{\"text\":\"" + module_name + "\",\"color\":\"gold\"},{\"text\":\"]\",\"color\":\"gray\"},\" \",{\"text\":\"Error: \",\"color\":\"dark_red\"},{\"text\":\"Dom's Nexus\",\"color\":\"blue\"},\" \",{\"score\":{\"name\":\"#installed_major\",\"objective\":\"nexus.value\"},\"color\":\"gold\"},{\"text\":\".x.x\",\"color\":\"gold\"},{\"text\":\" is too new, update \",\"color\":\"red\"},{\"text\":\"" + module_name + "\",\"color\":\"gold\"},{\"text\":\" to the latest version.\",\"color\":\"red\"}]\n" + 
                        "execute if score #module_count nexus.value matches 001 if score #installed_major nexus.value = #expected_major nexus.value unless score #installed_minor nexus.value = #expected_minor nexus.value run scoreboard players set #doms_nexus_error_boolean nexus.value 1\n" + 
                        "execute if score #module_count nexus.value matches 001 if score #installed_major nexus.value = #expected_major nexus.value if score #installed_minor nexus.value < #expected_minor nexus.value run tellraw @a [\"\",{\"text\":\"[\",\"color\":\"gray\"},{\"text\":\"" + module_name + "\",\"color\":\"gold\"},{\"text\":\"]\",\"color\":\"gray\"},\" \",{\"text\":\"Error: \",\"color\":\"dark_red\"},{\"text\":\"Dom's Nexus\",\"color\":\"blue\",\"underlined\":true,\"hoverEvent\":{\"action\":\"show_text\",\"value\":[{\"text\":\"Dom's Nexus\",\"color\":\"blue\"},{\"text\":\" on \",\"color\":\"gray\"},{\"text\":\"GitHub\",\"color\":\"blue\"}]},\"clickEvent\":{\"action\":\"open_url\",\"value\":\"https://github.com/Dominexis/Doms-Nexus/releases\"}},\" \",{\"score\":{\"name\":\"#installed_major\",\"objective\":\"nexus.value\"},\"color\":\"gold\"},{\"text\":\".\",\"color\":\"gold\"},{\"score\":{\"name\":\"#installed_minor\",\"objective\":\"nexus.value\"},\"color\":\"gold\"},{\"text\":\".x\",\"color\":\"gold\"},{\"text\":\" is too old, update it to the latest version.\",\"color\":\"red\"}]\n" + 
                        "execute if score #module_count nexus.value matches 001 if score #installed_major nexus.value = #expected_major nexus.value if score #installed_minor nexus.value > #expected_minor nexus.value run tellraw @a [\"\",{\"text\":\"[\",\"color\":\"gray\"},{\"text\":\"" + module_name + "\",\"color\":\"gold\"},{\"text\":\"]\",\"color\":\"gray\"},\" \",{\"text\":\"Error: \",\"color\":\"dark_red\"},{\"text\":\"Dom's Nexus\",\"color\":\"blue\"},\" \",{\"score\":{\"name\":\"#installed_major\",\"objective\":\"nexus.value\"},\"color\":\"gold\"},{\"text\":\".\",\"color\":\"gold\"},{\"score\":{\"name\":\"#installed_minor\",\"objective\":\"nexus.value\"},\"color\":\"gold\"},{\"text\":\".x\",\"color\":\"gold\"},{\"text\":\" is too new, update \",\"color\":\"red\"},{\"text\":\"" + module_name + "\",\"color\":\"gold\"},{\"text\":\" to the latest version.\",\"color\":\"red\"}]\n" + 
                        "execute if score #module_count nexus.value matches 001 if score #installed_major nexus.value = #expected_major nexus.value if score #installed_minor nexus.value = #expected_minor nexus.value unless score #installed_patch nexus.value >= #expected_patch nexus.value run scoreboard players set #doms_nexus_error_boolean nexus.value 1\n" + 
                        "execute if score #module_count nexus.value matches 001 if score #installed_major nexus.value = #expected_major nexus.value if score #installed_minor nexus.value = #expected_minor nexus.value if score #installed_patch nexus.value < #expected_patch nexus.value run tellraw @a [\"\",{\"text\":\"[\",\"color\":\"gray\"},{\"text\":\"" + module_name + "\",\"color\":\"gold\"},{\"text\":\"]\",\"color\":\"gray\"},\" \",{\"text\":\"Error: \",\"color\":\"dark_red\"},{\"text\":\"Dom's Nexus\",\"color\":\"blue\",\"underlined\":true,\"hoverEvent\":{\"action\":\"show_text\",\"value\":[{\"text\":\"Dom's Nexus\",\"color\":\"blue\"},{\"text\":\" on \",\"color\":\"gray\"},{\"text\":\"GitHub\",\"color\":\"blue\"}]},\"clickEvent\":{\"action\":\"open_url\",\"value\":\"https://github.com/Dominexis/Doms-Nexus/releases\"}},\" \",{\"score\":{\"name\":\"#installed_major\",\"objective\":\"nexus.value\"},\"color\":\"gold\"},{\"text\":\".\",\"color\":\"gold\"},{\"score\":{\"name\":\"#installed_minor\",\"objective\":\"nexus.value\"},\"color\":\"gold\"},{\"text\":\".\",\"color\":\"gold\"},{\"score\":{\"name\":\"#installed_patch\",\"objective\":\"nexus.value\"},\"color\":\"gold\"},{\"text\":\" is too old, update it to the latest version.\",\"color\":\"red\"}]" + "\n"*8 +
                        "# Throw error if multiple copies of the module are loaded" + "\n"*2 +
                        "execute store result score #module_count nexus.value if data storage nexus:data modules[{id:\"" + internal_id + "\"}]\n" + 
                        "execute if score #module_count nexus.value matches 2.. run scoreboard players set #doms_nexus_error_boolean nexus.value 1\n" + 
                        "execute if score #module_count nexus.value matches 2.. run tellraw @a [\"\",{\"text\":\"[\",\"color\":\"gray\"},{\"text\":\"" + module_name + "\",\"color\":\"gold\"},{\"text\":\"]\",\"color\":\"gray\"},\" \",{\"text\":\"Error: \",\"color\":\"dark_red\"},{\"text\":\"Multiple copies of \",\"color\":\"red\"},{\"text\":\"" + module_name + "\",\"color\":\"gold\"},{\"text\":\" exist. Remove all outdated versions.\",\"color\":\"red\"}]"
                    )

                # Set message
                message += " Module created.\n"

        elif action == 4:
            # Extract parameters
            parameter_ids = []
            parameter_values = []
            for parameter in parameters:
                parameter_ids.append(parameter.id)
                parameter_values.append(parameter.value)
            
            module_name = parameter_values[parameter_ids.index("module_name")]
            author = parameter_values[parameter_ids.index("author")]
            version = parameter_values[parameter_ids.index("version")]
            doms_nexus_version = parameter_values[parameter_ids.index("doms_nexus_version")]
            internal_id = parameter_values[parameter_ids.index("internal_id")]
            namespace = parameter_values[parameter_ids.index("namespace")]
            old_module_name = parameter_values[parameter_ids.index("old_module_name")]

            # Compile pack name
            pack_name = module_name + " - By " + author + " - " + version

            # Check that module name is in old module name
            if module_name not in old_module_name:
                message += " Error: Old and current module names do not match!\n"
            else:
                # Check if the module already exists
                if not os.path.exists(os.path.join(path, old_module_name)):
                    message += " Error: \"" + old_module_name + "\" doesn't exist!\n"
                else:
                    # Get the old version ID from the version verification system
                    if not os.path.exists(os.path.join(path, old_module_name, "data", namespace, "functions", "verify")):
                        message += " Error: Version verification system does not exist!\n"
                    else:
                        directory_list = os.listdir(os.path.join(path, old_module_name, "data", namespace, "functions", "verify"))
                        if len(directory_list) == 0:
                            message += " Error: Version verification system does not exist!\n"
                        else:
                            old_version = directory_list[-1].replace("_", ".")

                            # Get old Nexus support version
                            if not os.path.exists(os.path.join(path, old_module_name, "data", namespace, "functions", "verify", old_version.replace(".", "_"), "check.mcfunction")):
                                message += " Error: Check function does not exist!\n"
                            else:
                                with open(os.path.join(path, old_module_name, "data", namespace, "functions", "verify", old_version.replace(".", "_"), "check.mcfunction"), "r", encoding="utf-8") as file:
                                    contents = file.read()
                                major_index = contents.index("scoreboard players set #expected_major nexus.value ") + 51
                                minor_index = contents.index("scoreboard players set #expected_minor nexus.value ") + 51
                                patch_index = contents.index("scoreboard players set #expected_patch nexus.value ") + 51
                                old_doms_nexus_version = contents[major_index: contents.index("\n", major_index)] + "." + contents[minor_index: contents.index("\n", minor_index)] + "." + contents[patch_index: contents.index("\n", patch_index)]

                                # Modify version verification system
                                with open(os.path.join(path, old_module_name, "data", namespace, "functions", "verify", old_version.replace(".", "_"), "check.mcfunction"), "w", encoding="utf-8") as file:
                                    file.write(
                                        contents[0: major_index] + 
                                        doms_nexus_version.split(".")[0] + contents[contents.index("\n", major_index): minor_index] +
                                        doms_nexus_version.split(".")[1] + contents[contents.index("\n", minor_index): patch_index] +
                                        doms_nexus_version.split(".")[2] + contents[contents.index("\n", patch_index):]
                                    )

                                if not os.path.exists(os.path.join(path, old_module_name, "data", namespace, "functions", "verify", old_version.replace(".", "_"), "version.mcfunction")):
                                    message += " Error: Version function does not exist!\n"
                                else:
                                    with open(os.path.join(path, old_module_name, "data", namespace, "functions", "verify", old_version.replace(".", "_"), "version.mcfunction"), "r", encoding="utf-8") as file:
                                        contents = file.read()
                                    major_index = contents.index("major:") + 6
                                    minor_index = contents.index("minor:") + 6
                                    patch_index = contents.index("patch:") + 6
                                    with open(os.path.join(path, old_module_name, "data", namespace, "functions", "verify", old_version.replace(".", "_"), "version.mcfunction"), "w", encoding="utf-8") as file:
                                        file.write(
                                            contents[0: major_index] +
                                            version.split(".")[0] + contents[contents.index(",", major_index): minor_index] +
                                            version.split(".")[1] + contents[contents.index(",", minor_index): patch_index] +
                                            version.split(".")[2] + contents[contents.index("}", patch_index):]
                                        )

                                # Modify pack.mcmeta
                                if not os.path.exists(os.path.join(path, old_module_name, "pack.mcmeta")):
                                    message += " Error: \"pack.mcmeta\" does not exist!\n"
                                else:
                                    with open(os.path.join(path, old_module_name, "pack.mcmeta"), "r", encoding="utf-8") as file:
                                        contents = file.read()
                                    module_version_index = contents.index(old_version, contents.index(module_name))
                                    doms_nexus_version_index = contents.index(old_doms_nexus_version, contents.index("Dom's Nexus"))
                                    with open(os.path.join(path, old_module_name, "pack.mcmeta"), "w", encoding="utf-8") as file:
                                        file.write(
                                            contents[0: module_version_index] + version +
                                            contents[contents.index("\\n", module_version_index): doms_nexus_version_index] + doms_nexus_version +
                                            contents[contents.index("+", doms_nexus_version_index):]
                                        )

                                # Modify login message
                                if not os.path.exists(os.path.join(path, old_module_name, "data", namespace, "functions", "player", "login", "main.mcfunction")):
                                    message += " Error: Login system does not exists!\n"
                                else:
                                    with open(os.path.join(path, old_module_name, "data", namespace, "functions", "player", "login", "main.mcfunction"), "r", encoding="utf-8") as file:
                                        contents = file.read()
                                    with open(os.path.join(path, old_module_name, "data", namespace, "functions", "player", "login", "main.mcfunction"), "w", encoding="utf-8") as file:
                                        file.write(contents.replace(old_version, version))

                                # Modify verification function tags
                                if not os.path.exists(os.path.join(path, old_module_name, "data", "nexus", "tags", "functions", "verify", "check.json")):
                                    message += " Error: Check function tag does not exist!\n"
                                else:
                                    with open(os.path.join(path, old_module_name, "data", "nexus", "tags", "functions", "verify", "check.json"), "r", encoding="utf-8") as file:
                                        contents = file.read()
                                    with open(os.path.join(path, old_module_name, "data", "nexus", "tags", "functions", "verify", "check.json"), "w", encoding="utf-8") as file:
                                        file.write(contents.replace(old_version.replace(".", "_"), version.replace(".", "_")))

                                if not os.path.exists(os.path.join(path, old_module_name, "data", "nexus", "tags", "functions", "verify", "version.json")):
                                    message += " Error: Version function tag does not exist!\n"
                                else:
                                    with open(os.path.join(path, old_module_name, "data", "nexus", "tags", "functions", "verify", "version.json"), "r", encoding="utf-8") as file:
                                        contents = file.read()
                                    with open(os.path.join(path, old_module_name, "data", "nexus", "tags", "functions", "verify", "version.json"), "w", encoding="utf-8") as file:
                                        file.write(contents.replace(old_version.replace(".", "_"), version.replace(".", "_")))

                                # Update last modified value
                                if not os.path.exists(os.path.join(path, old_module_name, "data", namespace, "functions", "setup", "last_modified.mcfunction")):
                                    message += " Error: Last modified function does not exist!\n"
                                else:
                                    with open(os.path.join(path, old_module_name, "data", namespace, "functions", "setup", "last_modified.mcfunction"), "r", encoding="utf-8") as file:
                                        contents = file.read()
                                    time = datetime.datetime.now()
                                    last_modified_index = contents.index("scoreboard players set #last_modified nexus.value ") + 50
                                    with open(os.path.join(path, old_module_name, "data", namespace, "functions", "setup", "last_modified.mcfunction"), "w", encoding="utf-8") as file:
                                        file.write(
                                            contents[0: last_modified_index] + 
                                            str(time.year) + ("0" if time.month < 10 else "") + str(time.month) + ("0" if time.day < 10 else "") + str(time.day) + ("0" if time.hour*4 + time.minute//15 < 10 else "") + str(time.hour*4 + time.minute//15) +
                                            contents[contents.index("\n", last_modified_index):]
                                        )

                                # Rename folders
                                os.rename(os.path.join(path, old_module_name, "data", namespace, "functions", "verify", old_version.replace(".", "_")), os.path.join(path, old_module_name, "data", namespace, "functions", "verify", version.replace(".", "_")))
                                os.rename(os.path.join(path, old_module_name), os.path.join(path, pack_name))

                                # Set message
                                message += " Module updated.\n"

        elif action == 5:
            exit()