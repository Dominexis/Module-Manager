# Import things

import os
import shutil
import sys
import json
from datetime import datetime
from pathlib import Path
from enum import Enum



# Check that correct Python version is running

if not (
    (sys.version_info[0] == 3 and sys.version_info[1] >= 9)
    or
    (sys.version_info[0] > 3)
):
    print("\n\n ERROR: Module Manager requires Python 3.9 or newer!")
    input()
    exit()



# Initialize variables

PROGRAM_PATH = Path(__file__).parent
MODULE_MANAGER_VERSION = "2.0.2"
PACK_FORMAT = 10

class State(Enum):
    """Enumeration which stores the IDs of the program states.

    Using plain strings to store these sorts of values risks typos breaking the system.

    An enumeration ensures that the values are accurate because the IDE can flag typos."""

    MAIN_MENU = "main_menu"

    CREATE_MODULE = "create_module"

    UPDATE_MODULE_MENU = "update_module_menu"
    UPDATE_MODULE_TARGET = "update_module_target"
    UPDATE_MODULE = "update_module"
    RENAME_MODULE = "rename_module"

    SETTINGS = "settings"
    SETTINGS_MODULE_INFO = "settings_module_info"
    SETTINGS_DEPENDENCIES = "settings_dependencies"
    SETTINGS_ADD_DEPENDENCY = "settings_add_dependency"
    SETTINGS_EDIT_DEPENDENCIES = "setting_edit_dependencies"
    SETTINGS_EDIT_DEPENDENCY = "settings_edit_dependency"
    SETTINGS_REMOVE_DEPENDENCY = "settings_remove_dependency"
    SETTINGS_FEATURES = "settings_features"
    IMPORT_SETTINGS = "import_settings"
    EXPORT_SETTINGS = "export_settings"

    EXIT = "exit"

class Setting_Category(Enum):
    """Enumeration which stores the IDs of the setting categories.

    Using plain strings to store these sorts of values risks typos breaking the system.

    An enumeration ensures that the values are accurate because the IDE can flag typos."""

    MODULE_INFO = "module_info"
    DEPENDENCIES = "dependencies"
    FEATURES = "features"

class Module_Setting(Enum):
    """Enumeration which stores the IDs of the module settings.

    Using plain strings to store these sorts of values risks typos breaking the system.

    An enumeration ensures that the values are accurate because the IDE can flag typos."""

    MODULE_NAME = "module_name"
    AUTHOR = "author"
    VERSION = "version"
    INTERNAL_ID = "internal_id"
    NAMESPACE = "namespace"
    DOWNLOAD_LINK = "download_link"

class Feature(Enum):
    """Enumeration which stores the IDs of the features in the feature list.

    Using plain strings to store these sorts of values risks typos breaking the system.

    An enumeration ensures that the values are accurate because the IDE can flag typos."""

    TIME_MANAGER = "time_manager"
    PLAYER_NBT = "player_nbt"
    PLAYER_HEALTH = "player_health"
    PLAYER_RESPAWN = "player_respawn"
    PLAYER_MOTION = "player_motion"
    ENTITY_PROCESSING = "entity_processing"
    ENTITY_HEALTH = "entity_health"
    CUSTOM_ENTITY_TICKING = "custom_entity_ticking"
    UNCONDITIONAL_ENTITY_TICKING = "unconditional_entity_ticking"
    DAMAGE_SENSOR_TICKING = "damage_sensor_ticking"
    VEHICLE = "vehicle"
    EVENT_ID_PLAYER_HURT_ENTITY = "event_id_player_hurt_entity"
    EVENT_ID_PLAYER_KILLED_ENTITY = "event_id_player_killed_entity"
    EVENT_ID_ENTITY_HURT_PLAYER = "event_id_entity_hurt_player"
    EVENT_ID_ENTITY_KILLED_PLAYER = "event_id_entity_killed_player"
    EVENT_ID_PLAYER_INTERACTED_WITH_ENTITY = "event_id_player_interacted_with_entity"
    OBJECT_TICKING = "object_ticking"
    MAXIMUM_ENTITY_TIME = "maximum_entity_time"
    MAXIMUM_OBJECT_TIME = "maximum_object_time"
    MINIMUM_ENTITY_TIME = "minimum_entity_time"
    MINIMUM_OBJECT_TIME = "minimum_object_time"
    MINIMUM_DIFFICULTY = "minimum_difficulty"

class Setting_Kind(Enum):
    """Enumeration which stores the IDs of the setting kinds, that is, their names.

    Using plain strings to store these sorts of values risks typos breaking the system.

    An enumeration ensures that the values are accurate because the IDE can flag typos."""

    GENERIC = "generic"
    PATH_PART = "path_part"
    VERSION = "version"
    INTERNAL = "internal"
    LINK = "link"
    BOOLEAN = "boolean"
    TIME = "time"
    DIFFICULTY = "difficulty"

class Setting_Template:
    """The generic class for settings used as a reference by the other setting types.

    It stores the value of the setting in `value`.

    This can be assigned with `assign()`, and returned in raw form with `export()`."""

    name = Setting_Kind.GENERIC

    def __init__(self, value: str):
        self.value = value

    def __str__(self) -> str:
        return self.value

    def assign(self, value: str, key: str) -> str:
        self.value = value
        return ""

    def export(self) -> str | int | bool:
        return self.value

class Path_Part(Setting_Template):
    """A path part represents any string which is used in a directory. This includes the name of the module, the author's name, etc.

    It stores the value of the setting in `value`.

    This can be assigned with `assign()`, and returned in raw form with `export()`."""

    name = Setting_Kind.PATH_PART

    def assign(self, value: str, key: str) -> str:
        if len(value) == 0:
            return f" ERROR: {key}: Cannot use an empty string!\n"
        for char in ["/", "\\", "?", "<", ">", ":", "\"", "|"]:
            if char in value:
                return f" ERROR: {key}: Cannot use illegal characters in file names!\n"
        self.value = value
        return ""

class Version(Setting_Template):
    """Represents a semver version in the format `MAJOR.MINOR.PATCH`.

    It stores the value of the version ID in `major`, `minor`, and `patch` respectively.

    These can be assigned with `assign()`, and returned in raw form with `export()`."""

    name = Setting_Kind.VERSION

    def __init__(self, major: int, minor: int, patch: int):
        self.major = major
        self.minor = minor
        self.patch = patch

    def __str__(self) -> str:
        return f'{self.major}.{self.minor}.{self.patch}'

    def assign(self, value: str | dict[str, int], key: str):
        # Manage dict type
        if isinstance(value, dict):
            if "major" not in value or "minor" not in value or "patch" not in value:
                return f' ERROR: {key}: Version must have "major", "minor", and "patch"!\n'
            for entry in value:
                if not isinstance(value[entry], int):
                    return f" ERROR: {key}: Cannot use non-numbers in version ID!\n"
                if value[entry] > 2147483647:
                    return f" ERROR: {key}: Cannot have values larger than the 32-bit integer limit!\n"
            self.major = value["major"]
            self.minor = value["minor"]
            self.patch = value["patch"]
            return ""

        if len(value) == 0:
            return f" ERROR: {key}: Cannot use an empty string!\n"
        if len(value.split(".")) != 3:
            return f" ERROR: {key}: Version must use the format MAJOR.MINOR.PATCH!\n"
        for entry in value.split("."):
            if not entry.isnumeric():
                return f" ERROR: {key}: Cannot use non-numbers in version ID!\n"
            if int(entry) > 2147483647:
                return f" ERROR: {key}: Cannot have values larger than the 32-bit integer limit!\n"
        self.major = int(value.split(".")[0])
        self.minor = int(value.split(".")[1])
        self.patch = int(value.split(".")[2])
        return ""

    def export(self) -> dict[str, int]:
        return {
            "major": self.major,
            "minor": self.minor,
            "patch": self.patch
        }

class Internal(Setting_Template):
    """An internal string is used in directories and file names within data packs. These may only have lowercase letters, numbers, and underscores.

    It stores the value of the setting in `value`.

    This can be assigned with `assign()`, and returned in raw form with `export()`."""

    name = Setting_Kind.INTERNAL

    def assign(self, value: str, key: str) -> str:
        if len(value) == 0:
            return f" ERROR: {key}: Cannot use an empty string!\n"
        for char in value:
            if char not in ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","0","1","2","3","4","5","6","7","8","9","-","_","."]:
                return f" ERROR: {key}: Cannot use illegal characters in an internal string!\n"
        self.value = value
        return ""

class Link(Setting_Template):
    """Used for a module's download link. Can be empty.

    It stores the value of the setting in `value`.

    This can be assigned with `assign()`, and returned in raw form with `export()`."""

    name = Setting_Kind.LINK

class Boolean(Setting_Template):
    """Stores a Boolean. Used in the feature list.

    It stores the value of the setting in `value`.

    This can be assigned with `assign()`, and returned in raw form with `export()`."""

    name = Setting_Kind.BOOLEAN

    def __init__(self, value: bool):
        self.value = value

    def __str__(self) -> str:
        if self.value:
            return "true"
        return "false"

    def assign(self, value: str | bool, key: str) -> str:
        if type(value).__name__ == "bool":
            self.value = value
            return ""
        if value in ["true", "True", "TRUE", "t", "T", "1"]:
            self.value = True
            return ""
        if value in ["false", "False", "FALSE", "f", "F", "0"]:
            self.value = False
            return ""
        return f" ERROR: {key} Input must be a boolean!\n"

class Time(Setting_Template):
    """Stores an integer which represents the number of ticks allotted to a specific task by the Nexus. Used in the feature list.

    It stores the value of the setting in `value`.

    This can be assigned with `assign()`, and returned in raw form with `export()`."""

    name = Setting_Kind.TIME

    def __init__(self, value: int):
        self.value = value

    def __str__(self):
        return str(self.value)

    def assign(self, value: str | int, key: str) -> str:
        if isinstance(value, int):
            self.value = value
            return ""
        if value.isnumeric():
            self.value = int(value)
            return ""
        return f" ERROR: {key}: Input must be a number!\n"

class Difficulty(Setting_Template):
    """Stores a string representing a difficulty mode. Can be `peaceful`, `easy`, `normal`, or `hard`.

    It stores the value of the setting in `value`.

    This can be assigned with `assign()`, and returned in raw form with `export()`."""

    name = Setting_Kind.DIFFICULTY

    def assign(self, value: str, key: str) -> str:
        if value in ["peaceful", "easy", "normal", "hard"]:
            self.value = value
            return ""
        if value in ["0", "1", "2", "3"]:
            self.value = ["peaceful", "easy", "normal", "hard"][["0", "1", "2", "3"].index(value)]
            return ""
        return f" ERROR: {key}: Input must be a valid difficulty!\n"

    def score(self) -> int:
        """Converts the difficulty into its numeric form for scores."""
        return ["peaceful", "easy", "normal", "hard"].index(self.value)





class Program:
    """The main class which runs the program.

    Most of the program is handled by a single class so that object variables
    can be accessed by the wide array of functions without having to make global variable calls."""

    __slots__ = (
        "state",
        "settings",
        "message",
        "dependency_index",
        "update_target",
        "update_settings"
    )

    state: State
    """State of the program."""
    settings: dict[str, dict[str, Setting_Template] | list[dict[str, Setting_Template]]]
    """Settings, stores everything configurable about the program."""
    message: str
    """Message to display on the terminal."""
    dependency_index: int
    """Which dependency is currently being edited."""
    update_target: Path
    """Which module is selected for updating."""
    update_settings: bool
    """Determines whether the settings were accessed from the update module menu or normally."""

    def __init__(self):
        STATE_HANDLER = {
            # Main menu
            State.MAIN_MENU: self.__handle_main_menu,
            # Module actions
            State.CREATE_MODULE: self.__handle_create_module,
            State.UPDATE_MODULE_MENU: self.__handle_update_module_menu,
            State.UPDATE_MODULE_TARGET: self.__handle_update_module_target,
            State.UPDATE_MODULE: self.__handle_update_module,
            State.RENAME_MODULE: self.__handle_rename_module,
            # Settings
            State.SETTINGS: self.__handle_settings,
            State.SETTINGS_MODULE_INFO: self.__handle_settings_module_info,
            State.SETTINGS_DEPENDENCIES: self.__handle_settings_dependencies,
            State.SETTINGS_ADD_DEPENDENCY: self.__handle_settings_add_dependency,
            State.SETTINGS_EDIT_DEPENDENCIES: self.__handle_settings_edit_dependencies,
            State.SETTINGS_EDIT_DEPENDENCY: self.__handle_settings_edit_dependency,
            State.SETTINGS_REMOVE_DEPENDENCY: self.__handle_settings_remove_dependency,
            State.SETTINGS_FEATURES: self.__handle_settings_features,
            State.IMPORT_SETTINGS: self.__handle_import_settings,
            State.EXPORT_SETTINGS: self.__handle_export_settings,
            # Exit
            State.EXIT: exit
        }

        # Initialize variables
        self.state = State.MAIN_MENU
        self.settings = {
            Setting_Category.MODULE_INFO.value: {
                Module_Setting.MODULE_NAME.value: Path_Part("Blank Module"),
                Module_Setting.AUTHOR.value: Path_Part("Dominexis"),
                Module_Setting.VERSION.value: Version(1,0,0),
                Module_Setting.INTERNAL_ID.value: Internal("blank_module"),
                Module_Setting.NAMESPACE.value: Internal("blank"),
                Module_Setting.DOWNLOAD_LINK.value: Link("")
            },
            Setting_Category.DEPENDENCIES.value: [
                self.default_dependency()
            ],
            Setting_Category.FEATURES.value: {
                Feature.TIME_MANAGER.value: Boolean(True),
                Feature.PLAYER_NBT.value: Boolean(False),
                Feature.PLAYER_HEALTH.value: Boolean(True),
                Feature.PLAYER_RESPAWN.value: Boolean(True),
                Feature.PLAYER_MOTION.value: Boolean(False),
                Feature.ENTITY_PROCESSING.value: Boolean(True),
                Feature.ENTITY_HEALTH.value: Boolean(True),
                Feature.CUSTOM_ENTITY_TICKING.value: Boolean(True),
                Feature.UNCONDITIONAL_ENTITY_TICKING.value: Boolean(False),
                Feature.DAMAGE_SENSOR_TICKING.value: Boolean(False),
                Feature.VEHICLE.value: Boolean(False),
                Feature.EVENT_ID_PLAYER_HURT_ENTITY.value: Boolean(True),
                Feature.EVENT_ID_PLAYER_KILLED_ENTITY.value: Boolean(True),
                Feature.EVENT_ID_ENTITY_HURT_PLAYER.value: Boolean(True),
                Feature.EVENT_ID_ENTITY_KILLED_PLAYER.value: Boolean(True),
                Feature.EVENT_ID_PLAYER_INTERACTED_WITH_ENTITY.value: Boolean(True),
                Feature.OBJECT_TICKING.value: Boolean(False),
                Feature.MAXIMUM_ENTITY_TIME.value: Time(45),
                Feature.MAXIMUM_OBJECT_TIME.value: Time(45),
                Feature.MINIMUM_ENTITY_TIME.value: Time(5),
                Feature.MINIMUM_OBJECT_TIME.value: Time(5),
                Feature.MINIMUM_DIFFICULTY.value: Difficulty("easy")
            }
        }
        self.message = ""

        # Execute state
        while True:
            STATE_HANDLER[self.state]()

    def __handle_main_menu(self):
        # Display menu
        display_title()
        self.display_config()
        print_lines(
            " Actions:",
            "  1) Create module",
            "  2) Update module",
            "  3) Edit settings",
            "  4) Exit program",
            ""
        )

        # Process action
        action, error, self.message = check_action(
            input(self.message + " Action: "), 1, 4)
        if error:
            return
        self.state = {
            1: State.CREATE_MODULE,
            2: State.UPDATE_MODULE_MENU,
            3: State.SETTINGS,
            4: State.EXIT
        }[action]
        self.message = ""
        self.update_settings = False

    def __handle_create_module(self):
        module_info: dict[str, Setting_Template] = self.settings[Setting_Category.MODULE_INFO.value]
        module_name = module_info[Module_Setting.MODULE_NAME.value]
        author = module_info[Module_Setting.AUTHOR.value]
        version: Version = module_info[Module_Setting.VERSION.value]
        internal_id = module_info[Module_Setting.INTERNAL_ID.value]
        namespace = module_info[Module_Setting.NAMESPACE.value]
        download_link = module_info[Module_Setting.DOWNLOAD_LINK.value]
        module_path = PROGRAM_PATH / f'{module_name} DP - By {author} - {version}'
        dependencies: list[dict[str, Setting_Template]] = self.settings[Setting_Category.DEPENDENCIES.value]
        features: dict[str, Setting_Template] = self.settings[Setting_Category.FEATURES.value]

        # Prepare old features
        old_features = features.copy()
        for feature in old_features:
            if isinstance(old_features[feature], Boolean):
                old_features[feature] = False

        # Check if the module already exists
        if module_path.exists():
            print_lines(
                " Module already exists! Are you sure you want to overwrite it?",
                "  0) No",
                "  1) Yes",
                ""
            )
            action, error, self.message = check_action(
                input(self.message + " Action: "), 0, 1)
            if error or action == 0:
                self.state = State.MAIN_MENU
                return
            shutil.rmtree(module_path)

        # Create files
        self.create_pack_mcmeta(module_path, module_name, author, version, dependencies)
        self.create_module_info_json(module_path)
        self.create_tags(module_path, namespace)
        self.create_entity_functions(module_path, namespace, features, old_features)
        self.create_event_id_functions(module_path, namespace, features, old_features)
        self.create_object_functions(module_path, namespace, features, old_features)
        self.create_player_functions(module_path, module_name, internal_id, version, namespace, features)
        self.create_setup_functions(module_path, internal_id, namespace, features)
        self.create_tick_functions(module_path, namespace)
        self.create_uninstall_functions(module_path, module_name, internal_id, namespace, features)
        self.create_verification_functions(module_path, module_name, version, internal_id, namespace, download_link, dependencies)

        self.message += " Module created\n"
        self.state = State.MAIN_MENU

    def __handle_update_module_menu(self):
        # Display menu
        display_title()
        print_lines(
            " Settings will be imported from the module that you select",
            "",
            " Update module:",
            "  0) Go back"
        )
        i = 1
        modules: dict[int, Path] = {}
        for path in PROGRAM_PATH.iterdir():
            if not path.is_dir():
                continue
            if not (path / "module_info.json").exists():
                continue
            print(f'  {i}) {path.name}')
            modules[i] = path
            i += 1
        print()

        # Process action
        action, error, self.message = check_action(
            input(self.message + " Action: "), 0, len(modules))
        if error:
            return
        if action == 0:
            self.state = State.MAIN_MENU
            self.message = ""
            return
        self.update_target = modules[action]
        settings_json, error = self.open_json(self.update_target / "module_info.json")
        if error:
            return
        self.update_settings = False
        self.import_settings(settings_json)
        self.state = State.UPDATE_MODULE_TARGET

    def __handle_update_module_target(self):
        # Display menu
        display_title()
        print_lines(
            f" Module to update: {self.update_target.name}",
            ""
        )
        self.display_config()
        print_lines(
            " Actions:",
            "  0) Go back",
            "  1) Update module",
            "  2) Rename module",
            "  3) Edit settings",
            ""
        )

        # Process action
        action, error, self.message = check_action(
            input(self.message + " Action: "), 0, 3)
        if error:
            return
        self.state = [
            State.UPDATE_MODULE_MENU,
            State.UPDATE_MODULE,
            State.RENAME_MODULE,
            State.SETTINGS
        ][action]
        self.update_settings = True
        self.message = ""
        
    def __handle_update_module(self):
        module_info: dict[str, Setting_Template] = self.settings[Setting_Category.MODULE_INFO.value]
        module_name = module_info[Module_Setting.MODULE_NAME.value]
        author = module_info[Module_Setting.AUTHOR.value]
        version: Version = module_info[Module_Setting.VERSION.value]
        internal_id = module_info[Module_Setting.INTERNAL_ID.value]
        namespace = module_info[Module_Setting.NAMESPACE.value]
        download_link = module_info[Module_Setting.DOWNLOAD_LINK.value]
        dependencies: list[dict[str, Setting_Template]] = self.settings[Setting_Category.DEPENDENCIES.value]
        features: dict[str, Setting_Template] = self.settings[Setting_Category.FEATURES.value]

        # Get old features
        settings_json, error = self.open_json(self.update_target / "module_info.json")
        if error:
            return
        old_features: dict[str, bool] = settings_json[Setting_Category.FEATURES.value]

        # Update files
        self.create_pack_mcmeta(self.update_target, module_name, author, version, dependencies)
        self.create_module_info_json(self.update_target)
        self.update_setup_functions(self.update_target, internal_id, namespace, features)
        self.create_entity_functions(self.update_target, namespace, features, old_features)
        self.create_event_id_functions(self.update_target, namespace, features, old_features)
        self.create_object_functions(self.update_target, namespace, features, old_features)
        
        folder_path = self.update_target / "data" / namespace.value / "functions" / "verify"
        if folder_path.exists():
            shutil.rmtree(folder_path)
        self.create_verification_functions(self.update_target, module_name, version, internal_id, namespace, download_link, dependencies)

        self.message += " Module updated\n"
        self.state = State.UPDATE_MODULE_TARGET

    def __handle_rename_module(self):
        module_info: dict[str, Setting_Template] = self.settings[Setting_Category.MODULE_INFO.value]
        module_name = module_info[Module_Setting.MODULE_NAME.value]
        author = module_info[Module_Setting.AUTHOR.value]
        version: Version = module_info[Module_Setting.VERSION.value]

        # Rename module
        module_path = PROGRAM_PATH / f'{module_name} DP - By {author} - {version}'
        os.rename(self.update_target, module_path)
        self.update_target = module_path

        self.message += " Module renamed\n"
        self.state = State.UPDATE_MODULE_TARGET

    def __handle_settings(self):
        # Display menu
        display_title()
        self.display_config()
        print_lines(
            " Actions:",
            "  0) Go back",
            "  1) Edit module info",
            "  2) Edit dependencies",
            "  3) Edit features",
            "  4) Import settings",
            "  5) Export settings",
            ""
        )

        # Process action
        action, error, self.message = check_action(
            input(self.message + " Action: "), 0, 5)
        if error:
            return
        self.state = [
            State.UPDATE_MODULE_TARGET if self.update_settings else State.MAIN_MENU,
            State.SETTINGS_MODULE_INFO,
            State.SETTINGS_DEPENDENCIES,
            State.SETTINGS_FEATURES,
            State.IMPORT_SETTINGS,
            State.EXPORT_SETTINGS
        ][action]
        self.message = ""

    def __handle_settings_module_info(self):
        # Display menu
        display_title()

        # Print list of settings
        print_lines(
            " Edit setting:",
            "  0) Go back"
        )
        module_info: dict[str, Setting_Template] = self.settings[Setting_Category.MODULE_INFO.value]
        settings_array: dict[int, str] = {}
        for entry in enumerate(module_info):
            print(f'  {entry[0] + 1}) {entry[1]}: {module_info[entry[1]]}')
            settings_array[entry[0] + 1] = entry[1]
        print()

        # Process action
        action, error, self.message = check_action(
            input(self.message + " Action: "), 0, len(settings_array))
        if error:
            return
        if action == 0:
            self.state = State.SETTINGS
            self.message = ""
            return

        # Abort if a setting cannot be changed
        if self.update_settings and settings_array[action] in [
            Module_Setting.MODULE_NAME.value,
            Module_Setting.AUTHOR.value,
            Module_Setting.INTERNAL_ID.value,
            Module_Setting.NAMESPACE.value
        ]:
            self.message += f" ERROR: Cannot edit {settings_array[action]} when updating a module!\n"
            return
        
        self.assign_setting(module_info, settings_array[action])

    def __handle_settings_dependencies(self):
        # Display menu
        display_title()

        # Print list of dependencies
        print(" Dependencies:")
        dependencies: list[dict[str, Setting_Template]] = self.settings[Setting_Category.DEPENDENCIES.value]
        for dependency in dependencies:
            print(f'  {dependency[Module_Setting.MODULE_NAME.value]} - {dependency[Module_Setting.VERSION.value]}')
        print()

        print_lines(
            " Actions:",
            "  0) Go back",
            "  1) Add dependency",
            "  2) Edit dependency",
            "  3) Remove dependency",
            ""
        )

        # Process action
        action, error, self.message = check_action(
            input(self.message + " Action: "), 0, 3)
        if error:
            return
        self.state = [
            State.SETTINGS,
            State.SETTINGS_ADD_DEPENDENCY,
            State.SETTINGS_EDIT_DEPENDENCIES,
            State.SETTINGS_REMOVE_DEPENDENCY
        ][action]
        self.message = ""

    def __handle_settings_add_dependency(self):
        self.settings[Setting_Category.DEPENDENCIES.value].append(
            {
                Module_Setting.MODULE_NAME.value: Path_Part("Blank Dependency"),
                Module_Setting.VERSION.value: Version(1,0,0),
                Module_Setting.INTERNAL_ID.value: Internal("blank_dependency"),
                Module_Setting.DOWNLOAD_LINK.value: Link("")
            }
        )
        self.message = " Dependency added\n"
        self.state = State.SETTINGS_DEPENDENCIES

    def __handle_settings_edit_dependencies(self):
        # Display menu
        display_title()

        # Print list of dependencies
        print_lines(
            " Edit dependency:",
            "  0) Go back"
        )
        dependencies: list[dict[str, Setting_Template]] = self.settings[Setting_Category.DEPENDENCIES.value]
        for i in range(len(dependencies)):
            dependency = dependencies[i]
            print(f'  {i+1}) {dependency[Module_Setting.MODULE_NAME.value]} - {dependency[Module_Setting.VERSION.value]}')
        print()
        
        # Process action
        action, error, self.message = check_action(
            input(self.message + " Action: "), 0, len(dependencies))
        if error:
            return
        if action == 0:
            self.state = State.SETTINGS_DEPENDENCIES
            self.message = ""
            return
        self.dependency_index = action-1
        self.state = State.SETTINGS_EDIT_DEPENDENCY

    def __handle_settings_edit_dependency(self):
        # Display menu
        display_title()

        # Print list of settings
        print_lines(
            " Edit setting:",
            "  0) Go back"
        )
        dependency: dict[str, Setting_Template] = self.settings[Setting_Category.DEPENDENCIES.value][self.dependency_index]
        settings_array: dict[int, str] = {}
        for entry in enumerate(dependency):
            print(f'  {entry[0] + 1}) {entry[1]}: {dependency[entry[1]]}')
            settings_array[entry[0] + 1] = entry[1]
        print()

        # Process action
        action, error, self.message = check_action(
            input(self.message + " Action: "), 0, len(settings_array))
        if error:
            return
        if action == 0:
            self.state = State.SETTINGS_EDIT_DEPENDENCIES
            self.message = ""
            return
        self.assign_setting(dependency, settings_array[action])

    def __handle_settings_remove_dependency(self):
        # Display menu
        display_title()

        # Print list of dependencies
        print_lines(
            " Remove dependency:",
            "  0) Go back"
        )
        dependencies: list[dict[str, Setting_Template]] = self.settings[Setting_Category.DEPENDENCIES.value]
        for i in range(len(dependencies)):
            dependency = dependencies[i]
            print(f'  {i+1}) {dependency[Module_Setting.MODULE_NAME.value]} - {dependency[Module_Setting.VERSION.value]}')
        print()
        
        # Process action
        action, error, self.message = check_action(
            input(self.message + " Action: "), 0, len(dependencies))
        if error:
            return
        if action == 0:
            self.state = State.SETTINGS_DEPENDENCIES
            self.message = ""
            return
        self.message = " Removed dependency\n"
        del self.settings[Setting_Category.DEPENDENCIES.value][action-1]

    def __handle_settings_features(self):
        # Display menu
        display_title()

        # Print list of settings
        print_lines(
            " Edit feature:",
            "  0) Go back"
        )
        features: dict[str, Setting_Template] = self.settings[Setting_Category.FEATURES.value]
        settings_array: dict[int, str] = {}
        for entry in enumerate(features):
            print(f'  {entry[0] + 1}) {entry[1]}: {features[entry[1]]}')
            settings_array[entry[0] + 1] = entry[1]
        print()

        # Process action
        action, error, self.message = check_action(
            input(self.message + " Action: "), 0, len(settings_array))
        if error:
            return
        if action == 0:
            self.state = State.SETTINGS
            self.message = ""
            return
        self.assign_setting(features, settings_array[action])

    def __handle_import_settings(self):
        settings_json, error = self.open_json(PROGRAM_PATH / "Module Manager Input.json")
        if error:
            self.state = State.SETTINGS
            return
        self.import_settings(settings_json)
        self.message += " Settings imported\n"
        self.state = State.SETTINGS

    def __handle_export_settings(self):
        self.state = State.SETTINGS
        settings_json = self.export_settings()
        with (PROGRAM_PATH / "Module Manager Input.json").open("w", encoding="utf-8") as file:
            json.dump(settings_json, file, indent=4)
        self.message = " Settings exported\n"
        self.state = State.SETTINGS

    def assign_setting(self, settings: dict[str, Setting_Template], key: str):
        """Used to assign settings from user input."""
        self.message = settings[key].assign(input(f' {key}: '), key)

    def import_settings(self, settings_json: dict[str, dict[str, Setting_Template] | list[dict[str, Setting_Template]]]):
        """Imports settings from `settings_json` and writes them to the stored settings dictionary."""
        for category in [Setting_Category.MODULE_INFO.value, Setting_Category.FEATURES.value]:
            if category not in settings_json:
                continue
            for setting in settings_json[category]:
                if setting not in self.settings[category]:
                    continue
                if self.update_settings and setting in [
                    Module_Setting.MODULE_NAME.value,
                    Module_Setting.AUTHOR.value,
                    Module_Setting.INTERNAL_ID.value,
                    Module_Setting.NAMESPACE.value
                ]:
                    continue
                self.message += self.settings[category][setting].assign(settings_json[category][setting], setting)

        category = Setting_Category.DEPENDENCIES.value
        if category in settings_json:
            self.settings[category] = []
            for dependency in settings_json[category]:
                new_dependency = self.default_dependency()
                for setting in dependency:
                    if setting not in new_dependency:
                        continue
                    self.message += new_dependency[setting].assign(dependency[setting], setting)
                self.settings[category].append(new_dependency)

    def export_settings(self) -> dict[str, dict[str, Setting_Template] | list[dict[str, Setting_Template]]]:
        """Exports settings from the stored settings dictionary and writes them to `settings_json`."""
        output: dict[str, dict[str, Setting_Template] | list[dict[str, Setting_Template]]] = {}

        category = Setting_Category.MODULE_INFO.value
        output[category] = {}
        for setting in self.settings[category]:
            output[category][setting] = self.settings[category][setting].export()

        category = Setting_Category.DEPENDENCIES.value
        output[category] = []
        for dependency in self.settings[category]:
            output[category].append(self.default_dependency())
            for setting in dependency:
                output[category][-1][setting] = dependency[setting].export()

        category = Setting_Category.FEATURES.value
        output[category] = {}
        for setting in self.settings[category]:
            output[category][setting] = self.settings[category][setting].export()

        return output

    def display_config(self):
        """Displays basic information about the module settings"""
        module_info: dict[str, Setting_Template] = self.settings[Setting_Category.MODULE_INFO.value]
        module_name = module_info[Module_Setting.MODULE_NAME.value]
        author = module_info[Module_Setting.AUTHOR.value]
        version = module_info[Module_Setting.VERSION.value]
        internal_id = module_info[Module_Setting.INTERNAL_ID.value]
        namespace = module_info[Module_Setting.NAMESPACE.value]
        download_link = module_info[Module_Setting.DOWNLOAD_LINK.value]
        dependencies: int = len(self.settings[Setting_Category.DEPENDENCIES.value])

        print_lines(
            f' Name: {module_name} DP - By {author} - {version}',
            f' Internal ID: {internal_id}',
            f' Namespace: {namespace}',
            f' Download link: {download_link}',
            f' {dependencies} dependenc{"y" if dependencies == 1 else "ies"}',
            ''
        )

    def open_json(self, file_path: Path) -> tuple[dict[str, dict[str, str]], bool]:
        """Safely opens up JSON files and returns an error if it is formatted incorrectly.

        The built-in JSON library doesn't handle certain encoding schemes properly,
        so this function is used to ensure the correct encoding is used."""
        if not file_path.exists():
            self.message += f" ERROR: {file_path.as_posix()} doesn't exist!\n"
            return {}, True
        try:
            with file_path.open("r", encoding="utf-8") as file:
                file_json: dict[str, dict[str, str]] = json.loads(file.read().encode(encoding="utf-8", errors="backslashreplace"))
                return file_json, False
        except json.JSONDecodeError:
            self.message += f" ERROR: {file_path.as_posix()} is not properly formatted!\n"
            return {}, True

    def create_pack_mcmeta(
        self,
        module_path: Path,
        module_name: Setting_Template,
        author: Setting_Template,
        version: Setting_Template,
        dependencies: list[dict[str, Setting_Template]]
    ):
        """Creates `pack.mcmeta` in the target module."""
        module_path.mkdir(exist_ok=True, parents=True)
        file_json = {
        	"pack": {
        		"pack_format": PACK_FORMAT,
        		"description": [
                    "",
                    { "text": module_name.value, "color": "gold", "bold": True },
                    "\n",
                    { "text": "By ", "color": "gray" },
                    { "text": author.value, "color": "blue" },
                    { "text": " - ", "color": "gray" },
                    { "text": str(version), "color": "gold" }
                ]
        	}
        }

        # Insert Nexus dependency
        for dependency in dependencies:
            if dependency[Module_Setting.MODULE_NAME.value].value == "Dom's Nexus":
                file_json["pack"]["description"].extend(
                    [
                        "\n",
                        { "text": "Powered by ", "color": "gray" },
                        { "text": "Dom's Nexus ", "color": "blue" },
                        { "text": str(dependency[Module_Setting.VERSION.value]) + "+", "color": "gold" }
                    ]
                )
                break

        with (module_path / "pack.mcmeta").open("w", encoding="utf-8") as file:
            json.dump(file_json, file, indent=4)

    def create_module_info_json(self, module_path: Path):
        """Creates `module_info.json` in the target module by exporting the stored settings dictionary into it."""
        module_path.mkdir(exist_ok=True, parents=True)
        settings_json = self.export_settings()
        with (module_path / "module_info.json").open("w", encoding="utf-8") as file:
            json.dump(settings_json, file, indent=4)

    def create_function(self, file_path: Path, contents: list[str]):
        """Creates a `.mcfunction` file from a list of lines."""
        file_path.parent.mkdir(exist_ok=True, parents=True)
        with file_path.open("w", encoding="utf-8") as file:
            file.write("\n".join(contents))

    def create_tags(self, module_path: Path, namespace: Setting_Template):
        """Creates a series of tags for a newly-created module."""
        self.create_tag(module_path / "data" / "minecraft" / "tags" / "functions" / "load.json", ["nexus:verify/main"])

        self.create_tag(module_path / "data" / "nexus" / "tags" / "entity_types" / "generic" / "entity.json",        [f"#{namespace}:generic/entity"])
        self.create_tag(module_path / "data" / "nexus" / "tags" / "entity_types" / "generic" / "damage_sensor.json", [f"#{namespace}:generic/damage_sensor"])
        self.create_tag(module_path / "data" / "nexus" / "tags" / "entity_types" / "generic" / "vehicle.json",       [f"#{namespace}:generic/vehicle"])

        self.create_tag(module_path / "data" / "nexus" / "tags" / "functions" / "player" / "main.json",         [f"{namespace}:player/main"])
        self.create_tag(module_path / "data" / "nexus" / "tags" / "functions" / "player" / "login.json",        [f"{namespace}:player/login/main"])
        self.create_tag(module_path / "data" / "nexus" / "tags" / "functions" / "setup" / "main.json",          [f"{namespace}:setup/main"])
        self.create_tag(module_path / "data" / "nexus" / "tags" / "functions" / "setup" / "last_modified.json", [f"{namespace}:setup/last_modified"])
        self.create_tag(module_path / "data" / "nexus" / "tags" / "functions" / "tick" / "main.json",           [f"{namespace}:tick/main"])
        self.create_tag(module_path / "data" / "nexus" / "tags" / "functions" / "uninstall" / "modules.json",   [f"{namespace}:uninstall/main"])

        self.create_tag(module_path / "data" / namespace.value / "tags" / "entity_types" / "generic" / "entity.json", ["#nexus:generic/system", f"#{namespace}:generic/damage_sensor", f"#{namespace}:generic/vehicle"])
        self.create_tag(module_path / "data" / namespace.value / "tags" / "entity_types" / "generic" / "damage_sensor.json", [])
        self.create_tag(module_path / "data" / namespace.value / "tags" / "entity_types" / "generic" / "vehicle.json", [])
        self.create_tag(module_path / "data" / namespace.value / "tags" / "items" / "generic" / "item.json", [])

    def create_tag(self, file_path: Path, contents: list[str]):
        """Creates a JSON data pack tag using a list of entries."""
        file_path.parent.mkdir(exist_ok=True, parents=True)
        with file_path.open("w", encoding="utf-8") as file:
            json.dump(
                {
                    "replace": False,
                    "values": contents
                },
                file,
                indent=4
            )

    def create_entity_functions(self, module_path: Path, namespace: Setting_Template, features: dict[str, Boolean], old_features: dict[str, bool]):
        """Creates functions and tags related to entity ticking and processing in the target module."""
        if features[Feature.CUSTOM_ENTITY_TICKING.value].value and not old_features[Feature.CUSTOM_ENTITY_TICKING.value]:
            self.create_tag(module_path / "data" / "nexus" / "tags" / "functions" / "entity" / "main.json", [f"{namespace}:entity/verify"])
            self.create_function(
                module_path / "data" / namespace.value / "functions" / "entity" / "verify.mcfunction",
                [
                    '# Run function if entity is from the right module', '',
                    f'execute if entity @s[tag={namespace}.entity] run function {namespace}:entity/main'
                ]
            )
            self.create_function(
                module_path / "data" / namespace.value / "functions" / "entity" / "main.mcfunction",
                [
                    '# Run function based on entity type', '', ''
                ]
            )

        if features[Feature.ENTITY_PROCESSING.value].value and not old_features[Feature.ENTITY_PROCESSING.value]:
            self.create_tag(    module_path / "data" / "nexus" / "tags" / "functions" / "entity" / "process.json", [f"{namespace}:entity/generic/process/main"])
            self.create_function(module_path / "data" / namespace.value / "functions" / "entity" / "generic" / "process" / "main.mcfunction", [])

    def create_event_id_functions(self, module_path: Path, namespace: Setting_Template, features: dict[str, Setting_Template], old_features: dict[str, bool]):
        """Creates functions and tags in the target module related to the event ID system of the Nexus,
        which detects interactions between players and entities and runs functions from either."""
        for criteria in [
            Feature.EVENT_ID_ENTITY_HURT_PLAYER.value,
            Feature.EVENT_ID_ENTITY_KILLED_PLAYER.value,
            Feature.EVENT_ID_PLAYER_HURT_ENTITY.value,
            Feature.EVENT_ID_PLAYER_KILLED_ENTITY.value,
            Feature.EVENT_ID_PLAYER_INTERACTED_WITH_ENTITY.value
        ]:
            if not features[criteria].value or old_features[criteria]:
                continue
            criteria_folder = criteria[9:]
            self.create_tag(    module_path / "data" / "nexus" / "tags" / "functions" / "generic" / "event_id" / criteria_folder / "player" / "pre.json",  [f"{namespace}:generic/event_id/{criteria_folder}/player/pre"])
            self.create_tag(    module_path / "data" / "nexus" / "tags" / "functions" / "generic" / "event_id" / criteria_folder / "player" / "post.json", [f"{namespace}:generic/event_id/{criteria_folder}/player/post"])
            self.create_tag(    module_path / "data" / "nexus" / "tags" / "functions" / "generic" / "event_id" / criteria_folder / "entity.json",          [f"{namespace}:generic/event_id/{criteria_folder}/entity"])
            self.create_function(module_path / "data" / namespace.value / "functions" / "generic" / "event_id" / criteria_folder / "player" / "pre.mcfunction", [])
            self.create_function(module_path / "data" / namespace.value / "functions" / "generic" / "event_id" / criteria_folder / "player" / "post.mcfunction", [])
            self.create_function(module_path / "data" / namespace.value / "functions" / "generic" / "event_id" / criteria_folder / "entity.mcfunction", [])

    def create_object_functions(self, module_path: Path, namespace: Setting_Template, features: dict[str, Setting_Template], old_features: dict[str, bool]):
        """Creates functions and tags related to object system in the target module."""
        if not features[Feature.OBJECT_TICKING.value].value or old_features[Feature.OBJECT_TICKING.value]:
            return
        self.create_tag(module_path / "data" / "nexus" / "tags" / "functions" / "object" / "main.json", [f"{namespace}:object/verify"])
        self.create_function(
            module_path / "data" / namespace.value / "functions" / "object" / "verify.mcfunction",
            [
                '# Run function if object is from the right module', '',
                f'execute if entity @s[tag={namespace}.object] run function {namespace}:object/main'
            ]
        )
        self.create_function(
            module_path / "data" / namespace.value / "functions" / "object" / "main.mcfunction",
            [
                '# Run function based on object type', '', ''
            ]
        )

    def create_player_functions(self, module_path: Path, module_name: Setting_Template, internal_id: Setting_Template, version: Version, namespace: Setting_Template, features: dict[str, Setting_Template]):
        """Creates the player functions in the target module."""
        self.create_function(module_path / "data" / namespace.value / "functions" / "player" / "main.mcfunction", [])
        self.create_function(
            module_path / "data" / namespace.value / "functions" / "player" / "login" / "main.mcfunction",
            [
                '# Send message', '',
                f'execute if score #debug_login_messages nexus.value matches 1 run tellraw @s ' +
                json.dumps(
                    [
                        " ",
                        { "text": "- ", "color": "gray" },
                        { "text": str(module_name), "color": "gold" },
                        { "text": " - ", "color": "gray" },
                        {
                            "nbt": f'modules[{{id:"{internal_id}"}}].version.major',
                            "storage": "nexus:data",
                            "color": "gold"
                        },
                        { "text": ".", "color": "gold" },
                        {
                            "nbt": f'modules[{{id:"{internal_id}"}}].version.minor',
                            "storage": "nexus:data",
                            "color": "gold"
                        },
                        { "text": ".", "color": "gold" },
                        {
                            "nbt": f'modules[{{id:"{internal_id}"}}].version.patch',
                            "storage": "nexus:data",
                            "color": "gold"
                        }
                    ]
                )
            ]
        )
        if features[Feature.PLAYER_RESPAWN.value]:
            self.create_tag(    module_path / "data" / "nexus" / "tags" / "functions" / "player" / "respawn.json", [f"{namespace}:player/respawn/main"])
            self.create_function(module_path / "data" / namespace.value / "functions" / "player" / "respawn" / "main.mcfunction", [])

    def create_setup_functions(self, module_path: Path, internal_id: Setting_Template, namespace: Setting_Template, features: dict[str, Setting_Template]):
        """Creates the setup functions in the target module."""
        self.create_function(
            module_path / "data" / namespace.value / "functions" / "setup" / "main.mcfunction",
            [
                '# Create scoreboard objectives', '',
                f'scoreboard objectives add {namespace}.value dummy',
                '\n'*6,
                '# Assign features', '',
                f'function {namespace}:setup/feature/assign',
                '\n'*6,
                '# Increment module count', '',
                'scoreboard players add #doms_nexus_module_count nexus.value 1'
            ]
        )

        self.update_setup_functions(module_path, internal_id, namespace, features)

    def update_setup_functions(self, module_path: Path, internal_id: Setting_Template, namespace: Setting_Template, features: dict[str, Setting_Template]):
        """Creates the `last_modified` and feature assignment functions in the target module."""
        time = datetime.now()
        self.create_function(
            module_path / "data" / namespace.value / "functions" / "setup" / "last_modified.mcfunction",
            [
                '# Set last modified value', '',
                f'scoreboard players set #last_modified nexus.value {time.year}{"0" if time.month < 10 else ""}{time.month}{"0" if time.day < 10 else ""}{time.day}{"0" if time.hour*4 + time.minute//15 < 10 else ""}{time.hour*4 + time.minute//15}',
                f'execute unless score #{internal_id}_last_modified nexus.value = #last_modified nexus.value run scoreboard players set #update_installation_boolean nexus.value 1',
                f'scoreboard players operation #{internal_id}_last_modified nexus.value = #last_modified nexus.value'
            ]
        )

        feature_list: list[str] = []
        for feature in features:
            feature_name = feature.replace(
                "player_hurt_entity",
                "phe"
            ).replace(
                "player_killed_entity",
                "pke"
            ).replace(
                "entity_hurt_player",
                "ehp"
            ).replace(
                "entity_killed_player",
                "ekp"
            ).replace(
                "player_interacted_with_entity",
                "piwe"
            )
            if isinstance(features[feature], Boolean) and features[feature].value:
                feature_list.append(
                    f'scoreboard players set #feature_{feature_name} nexus.value 1'
                )
            if isinstance(features[feature], Time):
                if "maximum" in feature_name:
                    feature_list.append(
                        f"execute if score #feature_{feature_name} nexus.value matches {features[feature]}.. run scoreboard players set #feature_{feature_name} nexus.value {features[feature]}"
                    )
                if "minimum" in feature_name:
                    feature_list.append(
                        f"execute if score #feature_{feature_name} nexus.value matches ..{features[feature]} run scoreboard players set #feature_{feature_name} nexus.value {features[feature]}"
                    )
            if isinstance(features[feature], Difficulty):
                feature_list.append(
                    f"execute if score #feature_{feature_name} nexus.value matches ..{features[feature].score()} run scoreboard players set #feature_{feature_name} nexus.value {features[feature].score()}"
                )
        self.create_function(
            module_path / "data" / namespace.value / "functions" / "setup" / "feature" / "assign.mcfunction",
            [
                '# Assign features', '',
                "\n".join(feature_list)
            ]
        )

    def create_tick_functions(self, module_path: Path, namespace: Setting_Template):
        """Creates a blank ticking function in the target module."""
        self.create_function(module_path / "data" / namespace.value / "functions" / "tick" / "main.mcfunction", [])

    def create_uninstall_functions(self, module_path: Path, module_name: Setting_Template, internal_id: Setting_Template, namespace: Setting_Template, features: dict[str, Setting_Template]):
        """Creates the uninstall function in the target module."""
        self.create_function(
            module_path / "data" / namespace.value / "functions" / "uninstall" / "main.mcfunction",
            [
                '# Remove scoreboard objectives', '',
                f'scoreboard objectives remove {namespace}.value',
                '\n'*6,
                '# Terminate entities', '',
                f'kill @e[type=#{namespace}:generic/entity,tag={namespace}.entity]',
                '\n'*6,
                '# Clear items', '',
                f'clear @a #{namespace}:generic/item{{{namespace}:{{item:1b}}}}',
                '\n'*6,
                '# Clear storage', '',
                f'data remove storage {namespace}:data tag',
                '\n'*6,
                '# Reset scores', '',
                f'scoreboard players reset #{internal_id}_last_modified nexus.value',
                '\n'*6,
                '# Send message to chat', '',
                f'execute if score #debug_system_messages nexus.value matches 1 run tellraw @a[tag=nexus.player.operator] ["",{{"text":"[","color":"gray"}},{{"text":"{module_name}","color":"gold"}},{{"text":"]","color":"gray"}}," ",{{"text":"Module was successfully uninstalled.","color":"gray"}}]'
            ]
        )

    def create_verification_functions(
        self,
        module_path: Path,
        module_name: Setting_Template,
        version: Version,
        internal_id: Setting_Template,
        namespace: Setting_Template,
        download_link: Setting_Template,
        dependencies: list[dict[str, Setting_Template]]
    ):
        """Creates the version-verification system in the target module.
        This system is used to ensure that every module has their dependencies installed,
        and that conflicting versions do not coexist. It is the primary thing which changes when automated updates occur."""
        # Create main file
        file_path = module_path / "data" / "nexus" / "functions" / "verify" / "main.mcfunction"
        self.create_function(
            file_path,
            [
                '# Create scoreboard objective', '',
                "scoreboard objectives add nexus.value dummy",
                '\n'*6,
                '# Initialize scores', '',
                'scoreboard players set #doms_nexus_error_boolean nexus.value 0',
                '\n'*6,
                '# Verify modules', '',
                "data modify storage nexus:data modules set value []",
                'function #nexus:verify/version',
                'function #nexus:verify/check',
                '\n'*6,
                '# Setup Nexus', '',
                'execute if score #doms_nexus_error_boolean nexus.value matches 1 run tellraw @a ["",{"text":"[","color":"red"},{"text":"Dom\'s Nexus","color":"blue"},{"text":"]","color":"red"}," ",{"text":"Nexus and modules were unable to install.","color":"red"}]',
                'execute if score #doms_nexus_error_boolean nexus.value matches 1 run schedule function nexus:verify/main 3s replace',
                'execute if score #doms_nexus_error_boolean nexus.value matches 0 run schedule clear nexus:verify/main',
                'execute if score #doms_nexus_error_boolean nexus.value matches 0 run function nexus:setup/main'
            ]
        )

        # Create module-specific files
        folder_path = module_path / "data" / namespace.value / "functions" / "verify" / str(version).replace(".", "_")

        self.create_function(
            folder_path / "version.mcfunction",
            [
                '# Add pack version ID to module list', '',
                f'data modify storage nexus:data modules append value {{id:"{internal_id}",version:{{major:{version.major},minor:{version.minor},patch:{version.patch}}}}}'
            ]
        )

        contents: list[str] = []
        module_download = ""
        if download_link.value != "":
            module_download = f'," ",{{"text":"Click here to download.","color":"red","underlined":true,"hoverEvent":{{"action":"show_text","value":[{{"text":"{module_name}","color":"gold"}},{{"text":" download","color":"gray"}}]}},"clickEvent":{{"action":"open_url","value":"{download_link}"}}}}'
        for dependency in dependencies:
            dependency_name = dependency[Module_Setting.MODULE_NAME.value].value
            dependency_version: Version = dependency[Module_Setting.VERSION.value]
            dependency_internal_id = dependency[Module_Setting.INTERNAL_ID.value].value
            dependency_download_link = dependency[Module_Setting.DOWNLOAD_LINK.value].value

            dependency_color = "gold"
            if dependency_name == "Dom's Nexus":
                dependency_color = "blue"
            dependency_download = ""
            if dependency_download_link != "":
                dependency_download = f'," ",{{"text":"Click here to download.","color":"red","underlined":true,"hoverEvent":{{"action":"show_text","value":[{{"text":"{dependency_name}","color":"{dependency_color}"}},{{"text":" download","color":"gray"}}]}},"clickEvent":{{"action":"open_url","value":"{dependency_download_link}"}}}}'

            contents.extend(
                [
                    f'# Throw error if "{dependency_name}" is not installed properly',
                    '',
                    f'execute store result score #module_count nexus.value if data storage nexus:data modules[{{id:"{dependency_internal_id}"}}]',
                    'execute unless score #module_count nexus.value matches 1 run scoreboard players set #doms_nexus_error_boolean nexus.value 1',
                    f'execute if score #module_count nexus.value matches 000 run tellraw @a ["",{{"text":"[","color":"red"}},{{"text":"{module_name}","color":"gold"}},{{"text":"]","color":"red"}}," ",{{"text":"Error: ","color":"dark_red"}},{{"text":"{dependency_name}","color":"{dependency_color}"}},{{"text":" is not installed.","color":"red"}}{dependency_download}]',
                    f'execute if score #module_count nexus.value matches 2.. run tellraw @a ["",{{"text":"[","color":"red"}},{{"text":"{module_name}","color":"gold"}},{{"text":"]","color":"red"}}," ",{{"text":"Error: ","color":"dark_red"}},{{"text":"Multiple copies of ","color":"red"}},{{"text":"{dependency_name}","color":"{dependency_color}"}},{{"text":" exist. Remove all outdated versions.","color":"red"}}]',
                    '',
                    f'scoreboard players set #expected_major nexus.value {dependency_version.major}',
                    f'scoreboard players set #expected_minor nexus.value {dependency_version.minor}',
                    f'scoreboard players set #expected_patch nexus.value {dependency_version.patch}',
                    'scoreboard players set #installed_major nexus.value 0',
                    'scoreboard players set #installed_minor nexus.value 0',
                    'scoreboard players set #installed_patch nexus.value 0',
                    '',
                    f'execute if score #module_count nexus.value matches 1 store result score #installed_major nexus.value run data get storage nexus:data modules[{{id:"{dependency_internal_id}"}}].version.major',
                    f'execute if score #module_count nexus.value matches 1 store result score #installed_minor nexus.value run data get storage nexus:data modules[{{id:"{dependency_internal_id}"}}].version.minor',
                    f'execute if score #module_count nexus.value matches 1 store result score #installed_patch nexus.value run data get storage nexus:data modules[{{id:"{dependency_internal_id}"}}].version.patch',
                    f'execute if score #module_count nexus.value matches 1 unless score #installed_major nexus.value = #expected_major nexus.value run scoreboard players set #doms_nexus_error_boolean nexus.value 1',
                    f'execute if score #module_count nexus.value matches 1 if score #installed_major nexus.value < #expected_major nexus.value run tellraw @a ["",{{"text":"[","color":"red"}},{{"text":"{module_name}","color":"gold"}},{{"text":"]","color":"red"}}," ",{{"text":"Error: ","color":"dark_red"}},{{"text":"{dependency_name}","color":"{dependency_color}"}}," ",{{"score":{{"name":"#installed_major","objective":"nexus.value"}},"color":"gold"}},{{"text":".x.x","color":"gold"}},{{"text":" is too old, update it to the latest version.","color":"red"}}{dependency_download}]',
                    f'execute if score #module_count nexus.value matches 1 if score #installed_major nexus.value > #expected_major nexus.value run tellraw @a ["",{{"text":"[","color":"red"}},{{"text":"{module_name}","color":"gold"}},{{"text":"]","color":"red"}}," ",{{"text":"Error: ","color":"dark_red"}},{{"text":"{dependency_name}","color":"{dependency_color}"}}," ",{{"score":{{"name":"#installed_major","objective":"nexus.value"}},"color":"gold"}},{{"text":".x.x","color":"gold"}},{{"text":" is too new, update ","color":"red"}},{{"text":"{module_name}","color":"gold"}},{{"text":" to the latest version.","color":"red"}}{module_download}]',
                    f'execute if score #module_count nexus.value matches 1 if score #installed_major nexus.value = #expected_major nexus.value unless score #installed_minor nexus.value = #expected_minor nexus.value run scoreboard players set #doms_nexus_error_boolean nexus.value 1',
                    f'execute if score #module_count nexus.value matches 1 if score #installed_major nexus.value = #expected_major nexus.value if score #installed_minor nexus.value < #expected_minor nexus.value run tellraw @a ["",{{"text":"[","color":"red"}},{{"text":"{module_name}","color":"gold"}},{{"text":"]","color":"red"}}," ",{{"text":"Error: ","color":"dark_red"}},{{"text":"{dependency_name}","color":"{dependency_color}"}}," ",{{"score":{{"name":"#installed_major","objective":"nexus.value"}},"color":"gold"}},{{"text":".","color":"gold"}},{{"score":{{"name":"#installed_minor","objective":"nexus.value"}},"color":"gold"}},{{"text":".x","color":"gold"}},{{"text":" is too old, update it to the latest version.","color":"red"}}{dependency_download}]',
                    f'execute if score #module_count nexus.value matches 1 if score #installed_major nexus.value = #expected_major nexus.value if score #installed_minor nexus.value > #expected_minor nexus.value run tellraw @a ["",{{"text":"[","color":"red"}},{{"text":"{module_name}","color":"gold"}},{{"text":"]","color":"red"}}," ",{{"text":"Error: ","color":"dark_red"}},{{"text":"{dependency_name}","color":"{dependency_color}"}}," ",{{"score":{{"name":"#installed_major","objective":"nexus.value"}},"color":"gold"}},{{"text":".","color":"gold"}},{{"score":{{"name":"#installed_minor","objective":"nexus.value"}},"color":"gold"}},{{"text":".x","color":"gold"}},{{"text":" is too new, update ","color":"red"}},{{"text":"{module_name}","color":"gold"}},{{"text":" to the latest version.","color":"red"}}{module_download}]',
                    f'execute if score #module_count nexus.value matches 1 if score #installed_major nexus.value = #expected_major nexus.value if score #installed_minor nexus.value = #expected_minor nexus.value unless score #installed_patch nexus.value >= #expected_patch nexus.value run scoreboard players set #doms_nexus_error_boolean nexus.value 1',
                    f'execute if score #module_count nexus.value matches 1 if score #installed_major nexus.value = #expected_major nexus.value if score #installed_minor nexus.value = #expected_minor nexus.value if score #installed_patch nexus.value < #expected_patch nexus.value run tellraw @a ["",{{"text":"[","color":"red"}},{{"text":"{module_name}","color":"gold"}},{{"text":"]","color":"red"}}," ",{{"text":"Error: ","color":"dark_red"}},{{"text":"{dependency_name}","color":"{dependency_color}"}}," ",{{"score":{{"name":"#installed_major","objective":"nexus.value"}},"color":"gold"}},{{"text":".","color":"gold"}},{{"score":{{"name":"#installed_minor","objective":"nexus.value"}},"color":"gold"}},{{"text":".","color":"gold"}},{{"score":{{"name":"#installed_patch","objective":"nexus.value"}},"color":"gold"}},{{"text":" is too old, update it to the latest version.","color":"red"}}{dependency_download}]',
                    '\n'*6
                ]
            )

        contents.extend(
            [
                '# Throw error if multiple copies of the module are loaded',
                '',
                f'execute store result score #module_count nexus.value if data storage nexus:data modules[{{id:"{internal_id}"}}]',
                f'execute if score #module_count nexus.value matches 2.. run scoreboard players set #doms_nexus_error_boolean nexus.value 1',
                f'execute if score #module_count nexus.value matches 2.. run tellraw @a ["",{{"text":"[","color":"red"}},{{"text":"{module_name}","color":"gold"}},{{"text":"]","color":"red"}}," ",{{"text":"Error: ","color":"dark_red"}},{{"text":"Multiple copies of ","color":"red"}},{{"text":"{module_name}","color":"gold"}},{{"text":" exist. Remove all outdated versions.","color":"red"}}]'
            ]
        )

        self.create_function(folder_path / "check.mcfunction", contents)
        self.create_tag(module_path / "data" / "nexus" / "tags" / "functions" / "verify" / "version.json", [f"{namespace}:verify/{str(version).replace('.', '_')}/version"])
        self.create_tag(module_path / "data" / "nexus" / "tags" / "functions" / "verify" / "check.json",   [f"{namespace}:verify/{str(version).replace('.', '_')}/check"])

    def default_dependency(self) -> dict[str, Setting_Template]:
        """Returns a copy of the default dependency."""
        return {
            Module_Setting.MODULE_NAME.value: Path_Part("Dom's Nexus"),
            Module_Setting.VERSION.value: Version(2,0,0),
            Module_Setting.INTERNAL_ID.value: Internal("doms_nexus"),
            Module_Setting.DOWNLOAD_LINK.value: Link("https://github.com/Dominexis/Doms-Nexus/releases")
        }
    




# Check functions

def check_action(action_string: str, minimum: int, maximum: int) -> tuple[int, bool, str]:
    """Checks if a numeric action command is a number and within range."""
    # Halt if string is not a number
    if not action_string.isnumeric():
        return 0, True, " ERROR: Input must be a number!\n"
    action = int(action_string)

    # Halt if number is out of range
    if not minimum <= action <= maximum:
        return action, True, " ERROR: Input is out of range!\n"
    return action, False, ""



# Display functions

def display_title():
    """Displays the title on the terminal."""
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
    print_lines(
        '\n',
        f' Module Manager - By Dominexis - {MODULE_MANAGER_VERSION}',
        ''
    )

def print_lines(*lines: str):
    """Prints several lines on the terminal from a series of arguments."""
    print("\n".join(lines))



# Run program

if __name__ == "__main__":
    Program()