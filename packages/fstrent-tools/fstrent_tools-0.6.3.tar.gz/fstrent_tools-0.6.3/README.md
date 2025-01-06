# fstrent_tools

A comprehensive collection of Python utility functions.
version: "0.6.3"

## Modules


### Convert

- **convert_2_boolean**: Converts a value to a boolean.
- **convert_2_dict**: Converts a value to a dictionary.
- **convert_2_float**: Converts a value to a float.
- **convert_2_integer**: Converts a value to an integer.
- **convert_2_list**: Converts a value to a list.
- **convert_2_string**: Converts a value to a string.
- **dec**: converts a numeric string or float to a decimal.
- **dec_2_float**: converts a decimal to a float.
- **dec_prec**: converts a decimal to a float with a specified precision.
- **dict_2_obj**: converts a dictionary to an object.
- **int_2_tf**: converts an integer to a boolean.
- **tf**: converts a string 'true', 'True', 'TRUE', '1' or float 1 or decimal 1 to True. Converts a string 'false', 'False', 'FALSE', '0' or float 0 or decimal 0 to False.
- **tf_2_int**: converts a boolean to an integer.
- **to_float**: converts a value to a float.
- **to_int**: converts a value to an integer.
- **to_str**: converts a value to a string.

### Debug

- **debug_print**: Print debug information with specified level.
- **func_begin**: Mark the beginning of a function for timing.
- **func_end**: Mark the end of a function and return elapsed time.
- **func_timer**: Decorator to time function execution.
- **print_stack**: Print the current stack trace.
- **print_traceback**: Print the current exception traceback.

### Decorators

- **debug_class**: Class decorator that adds debug logging to all methods.
- **log_class**: Class decorator that adds logging functionality to all methods.
- **singleton**: Class decorator that ensures only one instance is created.
- **timing_class**: Class decorator that adds timing functionality to all methods.
- **my_func**: Decorator that times function execution and logs if it exceeds maximum time, and logs the function name. Optionally prints error message and/or halts execution.

### Dicts

- **class AttrDict**: A class that allows for attribute access and setting to dictionary keys.

- **AttrDictConv**: Convert a regular dictionary to AttrDict recursively.
- **AttrDictUpd**: Update an existing AttrDict with new keys from a dictionary.

- **DictContainsKeys**: Check if all keys in ks are present in in_dict.
- **DictKeyDel**: Delete key from dictionary if it exists.
- **DictKeyVal**: Check if key exists in dictionary.
- **DictKeyValFill**: Build key if absent or fill with default value if empty.
- **DictKeyValIfElse**: Return value if key is present and has value, else return default.
- **DictKeyValMult**: Returns Boolean if all key in ks return True using DictKeyVal function
- **DictValCheck**: Returns Boolean to verify all values in dict have value using HaveValue function
- **dict_of_dicts_sort**: Sort a dictionary of dictionaries by a specific key in the inner dictionaries.

### Docs

- **generate_module_docs**: Generate markdown documentation for all tools modules and their functions.
- **get_module_functions**: Extract functions and their docstrings from a Python file.
- **update_readme**: Update the README.md file with generated documentation.

### Errors

- **format_exception**: Format exception with traceback for logging.

### Eval

- **AllHaveVal**: Check if all values have non-empty values using HasVal.
- **HasVal**: Check if a value is non-empty.
- **is_even**: Check if a number is even.
- **is_odd**: Check if a number is odd.
- **is_valid_email**: Check if string is a valid email address.
- **is_valid_path**: Check if string is a valid file system path.

### Files

- **create_directory**: Creates a directory if it doesn't exist.
- **dir_val**: Check if a directory exists. If it doesn't, then create it.
- **ensure_dir**: Ensure directory exists, create if it doesn't.
- **file_copy**: Copy file from source to destination.
- **file_delete**: Delete file if it exists.
- **file_list**: List files in directory matching pattern.
- **file_move**: Move file from source to destination.
- **file_read**: Reads the contents of a file.
- **file_read_safe**: Safely read file content with error handling.
- **file_write**: Write content to a file.
- **file_write_safe**: Safely write content to file with directory creation if needed.
- **get_file_age_minutes**: Get file age in minutes.
- **is_valid_path**: Check if a path is valid for the current OS.
- **is_valid_path**: Check if a path is valid.

### Formatting

- **format_dict**: Format a dictionary with indentation.
- **format_list**: Format a list with bullets and indentation.
- **format_table**: Format data as a table with optional headers.
- **indent_text**: Indent each line of text by specified number of spaces.
- **print_adv**: Advanced print with indentation support.
- **print_func_name**: Print function name with optional arguments.
- **print_line**: Print a line of specified character and length.
- **print_obj**: Pretty print an object.

### Hyperlinks

- **extract_url**: Extract URL from a terminal hyperlink.
- **is_valid_url**: Check if string is a valid URL.
- **make_clickable**: Make text clickable with a URL.
- **print_clickable_link**: No description available
- **short_link**: Create a clickable terminal hyperlink with optional display text.

### Json

- **format_json**: Format JSON data with specified indentation.
- **merge_json**: Merge two JSON objects.
- **read_json**: Read and parse JSON data from a file.
- **search_json**: Search for a key in a JSON object.
- **validate_json**: Validate JSON data.
- **write_json**: Write data to a JSON file.
- **json_safe**: Convert object to JSON-safe format.
- **json_file_read**: Read JSON data from a file.
- **json_file_write**: Write data to a JSON file.

### Logging

- **log_debug**: Logs a debug message.
- **log_error**: Logs an error message.
- **log_exception**: Logs an exception message.
- **log_info**: Logs an info message.
- **log_warning**: Logs a warning message.
- **plogit**: print to screen and/or log to file.
- **setup_logger**: Sets up a logger with a file handler and a stream handler.

### Object

- **compare_objects**: Compares two objects for equality.
- **get_object_attributes**: Returns a dictionary of an object's attributes.
- **get_object_methods**: Returns a list of an object's methods.
- **get_object_size**: Returns the size of an object in bytes.
- **get_object_type**: Returns the type of an object.
- **is_object_empty**: Checks if an object is empty.
- **print_obj**: Pretty print an object.

### Print

- **clear_screen**: Clear the terminal screen.
- **print_adv**: Advanced print with indentation support.
- **print_clickable_link**: Print a clickable link in the terminal.
- **print_func_name**: Print the name of the current function.
- **print_line**: Print a line of specified character and length.
- **section_header**: Print a section header.

### Python

- **execute_python_script**: Executes a Python script in a separate process.
- **get_package_version**: Gets the version of an installed Python package.
- **install_package**: Installs a Python package using pip.
- **list_packages**: Lists all installed Python packages.
- **run_python_code**: Runs Python code in the current interpreter.
- **uninstall_package**: Uninstalls a Python package using pip.

### Settings

- **get_setting**: Retrieves a specific setting.
- **load_settings**: Loads settings from a JSON file.
- **reset_settings**: Resets the settings file to an empty dictionary.
- **save_settings**: Saves settings to a JSON file.
- **set_setting**: Sets a specific setting.
- **update_settings**: Updates existing settings with new values.

### Sounds

- **beep**: Play a beep sound.
- **beep_old**: Play a beep sound.
- **play_beep**: Play a beep sound.
- **play_cash**: Play a cash register sound.
- **play_doh**: Play a doh sound.
- **play_file**: Play a file sound.
- **play_sw_imperial_march**: Play the Star Wars Imperial March song.
- **play_sw_theme**: Play the Star Wars theme song.

### Speak

- **speak**: Speak text using gTTS with caching for faster repeated playback.
- **speak_async**: Speak text asynchronously using gTTS.

### Strings

- **IsEnglish**: Check if a string is English.

- **camel_to_snake**: Convert camelCase to snake_case.
- **snake_to_camel**: Convert snake_case to camelCase.

- **cpad**: Center pad string to specified length.
- **lpad**: Left pad string to specified length.
- **rpad**: Right pad string to specified length.
- **pad_string**: Pad string to specified length.


- **left**: Get left substring of specified length.
- **mid**: Get substring from start_position of specified length.
- **right**: Get right substring of specified length.

- **display_length**: Get display length of string (excluding ANSI escape sequences).
- **extract_numbers**: Extract only numbers from string.

- **remove_special_chars**: Remove special characters from string.
- **strip_formatting**: Remove ANSI escape sequences from string.
- **truncate_string**: Truncate string to max_length, adding suffix if truncated.

- **format_disp_age**: Format age in minutes to human-readable string.

### Terminal


### Time

- **calc_elapsed**: Calculate the elapsed time between two timestamps.
- **dttm_get**: Get the current date and time.
- **dttm_get**: Get the current date and time.
- **get_now**: Get the current date and time.
- **now_utc_get**: Get the current date and time.
- **now_utc_ts_get**: Get the current date and time.
- **prt_dttm_get**: Get the current date and time.
- **sleep**: Sleep for a specified number of seconds.
- **sleep_until**: Sleep until a specified timestamp.
- **temp_timer_begin**: Begin a temporary timer.
- **temp_timer_end**: End a temporary timer and return elapsed time.
- **temp_timing_begin**: Begin a temporary timing.
- **temp_timing_end**: End a temporary timing and return elapsed time.
- **utc_now**: Get the current date and time.

### Video

- **play_video**: Plays a video file.
- **record_video**: Records a video from the default camera.

### Voice

- **add_audio_to_video**: Adds audio to a video file using ffmpeg.
- **change_audio_volume**: Changes the volume of an audio file using ffmpeg.
- **convert_audio**: Converts an audio file to a different format using ffmpeg.
- **extract_audio_from_video**: Extracts audio from a video file using ffmpeg.
- **get_audio_duration**: Gets the duration of an audio file in seconds using ffprobe.
- **list_voices**: List all available voices with their properties.
- **merge_audio**: Merges multiple audio files into a single file using ffmpeg.
- **play_audio**: Plays an audio file.
- **set_voice_properties**: Set voice properties for speech synthesis.
- **speak**: Converts text to speech and plays the audio.
- **speak_async**: Speak text asynchronously using gTTS.
- **speak_cached**: Speak text using gTTS with caching for faster repeated playback.
- **speak_fast**: Fastest speech method using pyttsx3 with optimized settings.
- **split_audio**: Splits an audio file into a segment based on start and end times using ffmpeg.